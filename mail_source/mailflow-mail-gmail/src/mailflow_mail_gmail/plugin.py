"""Gmail Mail Source mail source: IMAP poll + SMTP reply.

Standard library only (imaplib / smtplib / email). Credentials come from the
account config (username / password, usually as ``${{ENV_VAR}}`` placeholders);
Gmail Mail Source requires an app password, not the account password — the
readme documents how to create one. Never log credentials.
"""

from __future__ import annotations

import asyncio
import contextlib
import html as html_lib
import imaplib
import logging
import re
import smtplib
from datetime import UTC, datetime
from email import message_from_bytes
from email.header import decode_header
from email.message import EmailMessage, Message
from email.utils import formatdate, parseaddr, parsedate_to_datetime
from typing import Any, cast

from mailflow.config import MailAccountConfig
from mailflow.contracts import MailEmitter
from mailflow.domain import Attachment, ComponentKind, MailAddress, MailMessage
from mailflow.plugins import PluginInfo
from mailflow.registry import PluginRegistrar

logger = logging.getLogger("mailflow.mail.gmail")

IMAP_HOST = "imap.gmail.com"
IMAP_PORT = 993
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_SSL = False


def _decode(value: str | None) -> str:
    if not value:
        return ""
    decoded: list[str] = []
    for chunk, charset in decode_header(value):
        if isinstance(chunk, bytes):
            try:
                decoded.append(chunk.decode(charset or "utf-8", errors="replace"))
            except LookupError:
                decoded.append(chunk.decode("utf-8", errors="replace"))
        else:
            decoded.append(chunk)
    return "".join(decoded)


def _mail_address(raw: str | None) -> MailAddress:
    name, address = parseaddr(raw or "")
    return MailAddress(name=_decode(name), address=address)


def _html_to_text(html: str) -> str:
    text = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", html)
    text = re.sub(r"(?i)<br\s*/?>", "\n", text)
    text = re.sub(r"(?i)</p>", "\n\n", text)
    text = re.sub(r"<[^>]+>", " ", text)
    text = html_lib.unescape(text)
    text = re.sub(r"[ \t\r\f\v]+", " ", text)
    text = re.sub(r"\n\s+\n", "\n\n", text)
    return text.strip()


def _extract_body(message: Message) -> tuple[str, str, list[Attachment]]:
    text_parts: list[str] = []
    html_parts: list[str] = []
    attachments: list[Attachment] = []
    for part in message.walk():
        if part.get_content_maintype() == "multipart":
            continue
        filename = part.get_filename()
        disposition = part.get_content_disposition()
        payload = part.get_payload(decode=True)
        is_text = part.get_content_maintype() == "text"
        is_body_candidate = is_text and disposition != "attachment" and not filename
        if not is_body_candidate:
            attachments.append(
                Attachment(
                    filename=filename or "unnamed",
                    content_type=part.get_content_type(),
                    size=len(bytes(payload)) if payload else 0,
                    content_id=part.get("Content-ID"),
                    data=None,
                )
            )
            continue
        if payload is None:
            continue
        charset = part.get_content_charset() or "utf-8"
        try:
            content = bytes(payload).decode(charset, errors="replace")
        except (LookupError, TypeError):
            content = bytes(payload).decode("utf-8", errors="replace")
        if part.get_content_subtype() == "html":
            html_parts.append(content)
        else:
            text_parts.append(content)
    body_text = "\n".join(text_parts).strip()
    body_html = "\n".join(html_parts).strip()
    from mailflow.domain import looks_binary

    if looks_binary(body_text):
        body_text = ""
    if not body_text and body_html:
        body_text = _html_to_text(body_html)
    return body_text, body_html, attachments


def parse_mime(raw: bytes, account_id: str, provider: str) -> MailMessage:
    message = message_from_bytes(raw)
    subject = _decode(message.get("Subject")) or "(no subject)"
    sender = _mail_address(message.get("From"))
    recipients = [_mail_address(value) for value in (message.get_all("To") or [])]
    cc = [_mail_address(value) for value in (message.get_all("Cc") or [])]
    message_id = str(message.get("Message-ID") or "").strip("<>")
    date_raw = message.get("Date")
    try:
        date = parsedate_to_datetime(date_raw) if date_raw else datetime.now(UTC)
    except (TypeError, ValueError):
        date = datetime.now(UTC)
    if date.tzinfo is None:
        date = date.replace(tzinfo=UTC)
    body_text, body_html, attachments = _extract_body(message)
    return MailMessage(
        message_id=message_id,
        account_id=account_id,
        subject=subject,
        sender=sender,
        recipients=recipients,
        cc=cc,
        date=date,
        received_at=datetime.now(UTC),
        body_text=body_text,
        body_html=body_html,
        attachments=attachments,
        provider=provider,
    )


class GmailSource:
    """Polls the Gmail Mail Source IMAP INBOX and sends replies over SMTP."""

    def __init__(self, account: MailAccountConfig) -> None:
        self._account = account
        self._interval = int(account.options.get("interval_seconds", 300))
        self._limit = int(account.options.get("limit", 20))
        self._seen: set[str] = set()
        self._last_uid: int | None = None
        self._analyze_backlog = bool(account.options.get("analyze_backlog", False))
        self._folder = str(account.options.get("imap_folder", "INBOX"))
        self._username = str(account.options.get("username") or account.email)
        self._password = str(account.options.get("password") or "")

    def _imap_client(self) -> imaplib.IMAP4:
        client = imaplib.IMAP4_SSL(IMAP_HOST, IMAP_PORT, timeout=20.0)
        client.login(self._username, self._password)
        client.select(self._folder)
        return client

    def _fetch_once(self) -> list[MailMessage]:
        client = self._imap_client()
        try:
            _status, data = client.uid("search", cast(Any, None), "ALL")
            all_uids = sorted({int(u) for u in (data[0] or b"").split() if u.isdigit()})
            if self._last_uid is not None:
                wanted = [u for u in all_uids if u > self._last_uid]
            elif self._analyze_backlog:
                wanted = all_uids[-max(1, self._limit):]
            else:
                wanted = []
                if all_uids:
                    self._last_uid = max(all_uids)
            messages: list[MailMessage] = []
            for uid_int in wanted:
                _status, fetch = client.uid("fetch", str(uid_int), "(RFC822)")
                if not fetch or fetch[0] is None:
                    break
                mail = parse_mime(bytes(fetch[0][1]), self._account.account_id, provider="gmail")
                self._last_uid = uid_int
                if mail.normalized_message_id() not in self._seen:
                    self._seen.add(mail.normalized_message_id())
                    messages.append(mail)
            if len(self._seen) > 10000:
                self._seen.clear()
            return messages
        finally:
            with contextlib.suppress(Exception):
                client.logout()

    def _fetch_history(self, limit: int, offset: int) -> list[MailMessage]:
        client = self._imap_client()
        try:
            _status, data = client.uid("search", cast(Any, None), "ALL")
            all_uids = sorted({int(u) for u in (data[0] or b"").split() if u.isdigit()})
            newest_first = list(reversed(all_uids))
            window = newest_first[offset : offset + limit] if limit > 0 else []
            messages: list[MailMessage] = []
            for uid_int in window:
                _status, fetch = client.uid("fetch", str(uid_int), "(RFC822)")
                if not fetch or fetch[0] is None:
                    continue
                messages.append(
                    parse_mime(bytes(fetch[0][1]), self._account.account_id, provider="gmail")
                )
            return messages
        finally:
            with contextlib.suppress(Exception):
                client.logout()

    async def fetch_history(self, limit: int = 50, offset: int = 0) -> list[MailMessage]:
        return await asyncio.to_thread(self._fetch_history, limit, offset)

    async def run(self, emit: MailEmitter, stop_event: asyncio.Event) -> None:
        while not stop_event.is_set():
            try:
                for mail in await asyncio.to_thread(self._fetch_once):
                    await emit(mail)
            except Exception as exc:
                logger.warning("fetch failed for %r: %s", self._account.account_id, exc)
            with contextlib.suppress(TimeoutError, asyncio.CancelledError):
                await asyncio.wait_for(stop_event.wait(), timeout=self._interval)

    async def send_reply(self, mail_id: str, draft: Any) -> None:
        await asyncio.to_thread(self._send_smtp, draft)

    def _send_smtp(self, draft: Any) -> None:
        message = EmailMessage()
        message["From"] = self._account.email or self._username
        message["To"] = draft.to.address
        message["Subject"] = draft.subject
        message["Date"] = formatdate(localtime=True)
        body = str(getattr(draft, "body", "") or "")
        stripped = body.lstrip()
        looks_like_html = stripped.startswith("<") and "</" in body
        if looks_like_html:
            from mailflow.letters import html_to_text

            message.set_content(html_to_text(body) or "(see HTML version)")
            message.add_alternative(body, subtype="html")
        else:
            message.set_content(body)
        if SMTP_SSL:
            client: Any = smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, timeout=30)
        else:
            client = smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=30)
            client.starttls()
        try:
            client.login(self._username, self._password)
            client.send_message(message)
        finally:
            client.quit()

    async def close(self) -> None:
        pass


PLUGIN_INFO = PluginInfo(
    plugin_id="mailflow-mail-gmail",
    name="Gmail Mail Source",
    version="0.1.0",
    description="IMAP/SMTP mail source for Gmail with app-password auth",
    kinds=[ComponentKind.MAIL_SOURCE],
)


class GmailPlugin:
    def mailflow_plugin_info(self) -> PluginInfo:
        return PLUGIN_INFO

    def mailflow_register(self, registrar: PluginRegistrar, config: Any) -> None:
        registrar.add_source("gmail", GmailSource)


plugin = GmailPlugin()

__all__ = ["GmailPlugin", "GmailSource", "parse_mime", "plugin"]
