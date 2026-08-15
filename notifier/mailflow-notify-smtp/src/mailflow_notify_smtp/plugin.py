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

    def _send_sync(self, record: MailRecord) -> None:
        message = EmailMessage()
        message["From"] = self._from_addr
        message["To"] = ", ".join(self._to)
        message["Subject"] = f"[{record.effective_urgency.value}] {record.mail.subject}"
        message.set_content(record.summary or record.mail.subject)
        if record.mail.body_text:
            message.add_alternative(record.mail.body_text, subtype="plain")

        if self._use_tls:
            with smtplib.SMTP(self._host, self._port, timeout=30) as server:
                server.starttls()
                if self._username:
                    server.login(self._username, self._password)
                server.send_message(message)
        else:
            with smtplib.SMTP_SSL(self._host, self._port, timeout=30) as server:
                if self._username:
                    server.login(self._username, self._password)
                server.send_message(message)

    async def notify(self, record: MailRecord) -> None:
        if not self._host or not self._from_addr or not self._to:
            logger.warning("smtp notifier is missing host/from_addr/to options; skipping")
            return
        await asyncio.to_thread(self._send_sync, record)


class SmtpPlugin:
    def mailflow_plugin_info(self) -> PluginInfo:
        return PLUGIN_INFO

    def mailflow_register(self, registrar: PluginRegistrar, config: Any) -> None:
        registrar.add_notifier("smtp", SmtpNotifier)


plugin = SmtpPlugin()

__all__ = ["SmtpNotifier", "SmtpPlugin", "plugin"]
