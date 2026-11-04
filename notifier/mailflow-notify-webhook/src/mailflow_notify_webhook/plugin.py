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
from mailflow.forms import FormField
from mailflow.notifications import DeliveryError, post_webhook
from mailflow.plugins import PluginInfo
from mailflow.registry import PluginRegistrar

logger = logging.getLogger("mailflow.notification.webhook")

PLUGIN_INFO = PluginInfo(
    plugin_id="mailflow-notify-webhook",
    name="Webhook Notifier",
    version="0.1.0",
    description="POSTs computed mail analyses to an HTTP webhook",
    kinds=[ComponentKind.NOTIFIER],
)


class WebhookNotifier:
    def __init__(self, config: NotifierConfig) -> None:
        self._url = str(config.options.get("url", ""))
        self._timeout = float(config.options.get("timeout_seconds", 10))

    async def notify(self, record: MailRecord) -> None:
        if not self._url:
            raise DeliveryError("configuration")
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
        await asyncio.to_thread(post_webhook, request, self._timeout, provider="webhook")


class WebhookPlugin:
    def mailflow_plugin_info(self) -> PluginInfo:
        return PLUGIN_INFO

    def mailflow_register(self, registrar: PluginRegistrar, config: Any) -> None:
        registrar.add_notifier("webhook", WebhookNotifier)
        registrar.add_form_fields(
            ComponentKind.NOTIFIER,
            "webhook",
            (
                FormField("url", required=True),
                FormField("timeout_seconds", kind="number", default=10),
            ),
        )


plugin = WebhookPlugin()

__all__ = ["WebhookNotifier", "WebhookPlugin", "plugin"]
