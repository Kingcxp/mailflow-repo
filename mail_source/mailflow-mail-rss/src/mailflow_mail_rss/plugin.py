"""RSS/Atom mail source: turns feed entries into normalized MailMessages.

Polls the configured feeds on an interval, deduplicates by entry id/link and
emits each new entry once. The source is read-only: replying to an RSS mail
raises a clear error (there is no outbound channel for a feed).
"""

from __future__ import annotations

import asyncio
import hashlib
import logging
import urllib.request
import xml.etree.ElementTree as ET
from datetime import UTC, datetime
from typing import Any
from urllib.parse import urlparse

from mailflow.config import MailAccountConfig
from mailflow.contracts import MailEmitter, ReplyDraft
from mailflow.domain import ComponentKind, MailAddress, MailMessage
from mailflow.plugins import PluginInfo
from mailflow.registry import PluginRegistrar

logger = logging.getLogger("mailflow.source.rss")

PLUGIN_INFO = PluginInfo(
    plugin_id="mailflow-mail-rss",
    name="RSS/Atom Source",
    version="0.1.0",
    description="Turns RSS/Atom feeds into mail items",
    kinds=[ComponentKind.MAIL_SOURCE],
)


def _parse_date(raw: str | None) -> datetime:
    """Best-effort RFC-822 / ISO-8601 date parsing; falls back to now."""
    if not raw:
        return datetime.now(UTC)
    try:
        from email.utils import parsedate_to_datetime

        return parsedate_to_datetime(raw).astimezone(UTC)
    except (TypeError, ValueError):
        pass
    try:
        return datetime.fromisoformat(raw.replace("Z", "+00:00")).astimezone(UTC)
    except ValueError:
        return datetime.now(UTC)


def _entry_parts(entry: ET.Element, tag: str) -> list[str]:
    values: list[str] = []
    for node in entry.iter(tag):
        if node.text and node.text.strip():
            values.append(node.text.strip())
    return values


class RssSource:
    def __init__(self, account: MailAccountConfig) -> None:
        self._account_id = account.account_id
        self._feeds = [str(url) for url in account.options.get("feeds", [])]
        self._interval = float(account.options.get("interval_seconds", 900))
        self._seen: set[str] = set()

    def _fetch(self, url: str) -> ET.Element:
        with urllib.request.urlopen(url, timeout=30) as response:
            data = response.read()
        return ET.fromstring(data)

    def _entries(self, url: str) -> list[MailMessage]:
        root = self._fetch(url)
        mails: list[MailMessage] = []
        entries = list(root.iterfind(".//item")) + list(
            root.iterfind("{http://www.w3.org/2005/Atom}entry")
        )
        for index, entry in enumerate(entries):
            titles = _entry_parts(entry, "title")
            links = _entry_parts(entry, "link")
            summaries = _entry_parts(entry, "summary") or _entry_parts(entry, "description")
            ids = _entry_parts(entry, "guid") or _entry_parts(entry, "id") or links
            dates = _entry_parts(entry, "pubDate") or _entry_parts(entry, "published")
            entry_id = ids[0] if ids else f"{url}#{index}"
            if entry_id in self._seen:
                continue
            feed_domain = urlparse(url).netloc
            mails.append(
                MailMessage(
                    message_id=f"rss-{hashlib.sha256(entry_id.encode('utf-8')).hexdigest()[:12]}",
                    account_id=self._account_id,
                    subject=titles[0] if titles else "(no title)",
                    sender=MailAddress(name=feed_domain, address=f"feed@{feed_domain}"),
                    recipients=[],
                    cc=[],
                    date=_parse_date(dates[0] if dates else None),
                    received_at=datetime.now(UTC),
                    body_text=summaries[0] if summaries else "",
                    body_html="",
                    provider="mailflow-mail-rss",
                    provider_message_id=entry_id,
                )
            )
        return mails

    async def run(self, emit: MailEmitter, stop_event: asyncio.Event) -> None:
        while not stop_event.is_set():
            for url in self._feeds:
                try:
                    for mail in await asyncio.to_thread(self._entries, url):
                        self._seen.add(mail.provider_message_id)
                        await emit(mail)
                except Exception as exc:  # noqa: BLE001 — one bad feed must not stop others
                    logger.warning("rss feed %r failed: %s", url, exc)
            try:
                await asyncio.wait_for(stop_event.wait(), timeout=self._interval)
            except TimeoutError:
                pass

    async def send_reply(self, mail_id: str, draft: ReplyDraft) -> None:
        raise RuntimeError("rss sources are read-only; replies are not supported")

    async def close(self) -> None:
        return None


class RssPlugin:
    def mailflow_plugin_info(self) -> PluginInfo:
        return PLUGIN_INFO

    def mailflow_register(self, registrar: PluginRegistrar, config: Any) -> None:
        registrar.add_source("rss", RssSource)


plugin = RssPlugin()

__all__ = ["RssPlugin", "RssSource", "plugin"]
