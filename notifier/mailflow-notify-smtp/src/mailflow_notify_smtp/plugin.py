"""SMTP notifier: forwards important mail alerts as emails via SMTP.

Supports STARTTLS (default) and implicit SSL, optional authentication, and
plain/HTML parts. ``smtplib`` runs in a worker thread so the event loop never
blocks. Credentials come from options (env placeholders supported by Core).
"""

from __future__ import annotations

import asyncio
import logging
import smtplib
from email.message import EmailMessage
from typing import Any

from mailflow.config import NotifierConfig
from mailflow.domain import ComponentKind, MailRecord
from mailflow.forms import FormField
from mailflow.notifications import DeliveryError
from mailflow.plugins import PluginInfo
from mailflow.registry import PluginRegistrar

logger = logging.getLogger("mailflow.notification.smtp")

PLUGIN_INFO = PluginInfo(
    plugin_id="mailflow-notify-smtp",
    name="SMTP Notifier",
    version="0.1.0",
    description="Forward important mail alerts as emails via any SMTP server",
    kinds=[ComponentKind.NOTIFIER],
)


class SmtpNotifier:
    def __init__(self, config: NotifierConfig) -> None:
        options = config.options
        self._host = str(options.get("host", ""))
        self._port = int(options.get("port", 587))
        self._use_tls = bool(options.get("use_tls", True))
        self._username = str(options.get("username", ""))
        self._password = str(options.get("password", ""))
        self._from_addr = str(options.get("from_addr", ""))
        self._to = [str(addr) for addr in options.get("to", [])]

    def _send_sync(self, record: MailRecord, recipients: list[str] | None = None) -> None:
        message = EmailMessage()
        message["From"] = self._from_addr
        message["To"] = ", ".join(recipients if recipients is not None else self._to)
        message["Subject"] = f"[{record.effective_urgency.value}] {record.mail.subject}"
        message.set_content(record.summary or record.mail.subject)
        if record.mail.body_text:
            message.add_alternative(record.mail.body_text, subtype="plain")

        if self._use_tls:
            with smtplib.SMTP(self._host, self._port, timeout=30) as server:
                server.starttls()
                if self._username:
                    server.login(self._username, self._password)
                refused = server.send_message(message)
                if refused:
                    raise DeliveryError("rejected")
        else:
            with smtplib.SMTP_SSL(self._host, self._port, timeout=30) as server:
                if self._username:
                    server.login(self._username, self._password)
                refused = server.send_message(message)
                if refused:
                    raise DeliveryError("rejected")

    async def notify(self, record: MailRecord) -> None:
        if not self._host or not self._from_addr or not self._to:
            raise DeliveryError("configuration")
        await asyncio.to_thread(self._send_sync, record)

    async def notify_to_target(
        self, target: str, record: MailRecord, *, text: str | None = None
    ) -> None:
        if not self._host or not self._from_addr or not target:
            raise DeliveryError("configuration")
        await asyncio.to_thread(self._send_sync, record, [target])


class SmtpPlugin:
    def mailflow_plugin_info(self) -> PluginInfo:
        return PLUGIN_INFO

    def mailflow_register(self, registrar: PluginRegistrar, config: Any) -> None:
        registrar.add_notifier("smtp", SmtpNotifier)
        registrar.add_form_fields(
            ComponentKind.NOTIFIER,
            "smtp",
            (
                FormField("host", required=True),
                FormField("port", kind="number", default=587),
                FormField(
                    "use_tls", kind="boolean", default=True, description_key="tui.smtp_tls_hint"
                ),
                FormField("username"),
                FormField("password", kind="password", secret=True),
                FormField("from_addr", required=True),
                FormField("to", kind="list", required=True),
            ),
        )


plugin = SmtpPlugin()

__all__ = ["SmtpNotifier", "SmtpPlugin", "plugin"]
