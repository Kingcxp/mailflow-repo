"""Webhook notifier: POSTs computed mail analyses to an HTTP endpoint.

Uses only the standard library (urllib), so the plugin depends on Core alone.
The endpoint URL comes from the notifier options (``url``). Delivery failures
are logged by the runtime and never fail mail processing.
"""

from __future__ import annotations

import asyncio
import json
import logging
import urllib.request
from typing import Any

from mailflow.config import NotifierConfig
from mailflow.domain import ComponentKind, MailRecord
from mailflow.plugins import PluginInfo
from mailflow.registry import PluginRegistrar

logger = logging.getLogger("mailflow.notification.webhook")

PLUGIN_INFO = PluginInfo(
    plugin_id="mailflow-notify-webhook",
    name="Webhook Notifier",
    version="0.1.0",
    description="POSTs computed mail analyses and reminders to an HTTP webhook",
    kinds=[ComponentKind.NOTIFIER],
)


class WebhookNotifier:
    def __init__(self, config: NotifierConfig) -> None:
        self._url = str(config.options.get("url", ""))
        self._timeout = float(config.options.get("timeout_seconds", 10))

    async def notify(self, record: MailRecord) -> None:
        if not self._url:
            logger.warning("webhook notifier has no url option; skipping")
            return
        payload = {
            "mail_id": record.record_id,
            "urgency": record.effective_urgency.value,
            "subject": record.mail.subject,
            "summary": record.summary,
            "from": record.mail.sender.address,
            "reply_required": bool(record.analysis and record.analysis.reply_required),
        }
        request = urllib.request.Request(
            self._url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        await asyncio.to_thread(urllib.request.urlopen, request, timeout=self._timeout)


class WebhookPlugin:
    def mailflow_plugin_info(self) -> PluginInfo:
        return PLUGIN_INFO

    def mailflow_register(self, registrar: PluginRegistrar, config: Any) -> None:
        registrar.add_notifier("webhook", WebhookNotifier)


plugin = WebhookPlugin()

__all__ = ["WebhookNotifier", "WebhookPlugin", "plugin"]
