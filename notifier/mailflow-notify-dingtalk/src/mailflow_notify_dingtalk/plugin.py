"""DingTalk notifier: pushes mail summaries to DingTalk.

Standard library only (urllib); the endpoint URL and credentials come from
the notifier options. Delivery failures are logged by the runtime and never
fail mail processing.
"""

from __future__ import annotations

import asyncio
import base64
import hashlib
import hmac
import json
import logging
import time
import urllib.request
from typing import Any
from urllib.parse import urlencode

from mailflow.config import NotifierConfig
from mailflow.domain import ComponentKind, MailRecord
from mailflow.forms import FormField
from mailflow.notifications import DeliveryError, post_webhook
from mailflow.plugins import PluginInfo
from mailflow.registry import PluginRegistrar

logger = logging.getLogger("mailflow.notification.dingtalk")

PLUGIN_INFO = PluginInfo(
    plugin_id="mailflow-notify-dingtalk",
    name="DingTalk Notifier",
    version="0.1.0",
    description="Push mail alerts to a DingTalk group robot webhook",
    kinds=[ComponentKind.NOTIFIER],
)


class DingTalkNotifier:
    """DingTalk delivery channel. Options documented in plugin.json."""

    def __init__(self, config: NotifierConfig) -> None:
        self._options = dict(config.options)
        self._timeout = float(self._options.get("timeout_seconds", 10))

    def _target_url(self) -> str:
        token = str(self._options.get("access_token", ""))
        url = (
            f"https://oapi.dingtalk.com/robot/send?{urlencode({'access_token': token})}"
            if token
            else str(self._options.get("webhook_url", ""))
        )
        secret = str(self._options.get("secret") or "")
        if url and secret:
            timestamp = str(int(time.time() * 1000))
            sign = base64.b64encode(
                hmac.new(
                    secret.encode(), f"{timestamp}\n{secret}".encode(), hashlib.sha256
                ).digest()
            ).decode()
            url += ("&" if "?" in url else "?") + urlencode({"timestamp": timestamp, "sign": sign})
        return url

    def _payload(self, record: MailRecord) -> dict[str, Any]:
        return {
            "msgtype": "text",
            "text": {"content": self._summary_text(record)},
        }

    @staticmethod
    def _summary_text(record: MailRecord) -> str:
        return (
            f"[MailFlow] {record.effective_urgency.value.upper()} "
            f"{record.mail.subject}\n{record.summary}"
        )

    async def notify(self, record: MailRecord) -> None:
        url = self._target_url()
        if not url:
            raise DeliveryError("configuration")
        request = urllib.request.Request(
            url,
            data=json.dumps(self._payload(record)).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        await asyncio.to_thread(post_webhook, request, self._timeout, provider="dingtalk")


class DingTalkNotifierPlugin:
    def mailflow_plugin_info(self) -> PluginInfo:
        return PLUGIN_INFO

    def mailflow_register(self, registrar: PluginRegistrar, config: Any) -> None:
        registrar.add_notifier("dingtalk", DingTalkNotifier)
        registrar.add_form_fields(
            ComponentKind.NOTIFIER,
            "dingtalk",
            (
                FormField("webhook_url", secret=True),
                FormField("access_token", kind="password", secret=True),
                FormField("secret", kind="password", secret=True),
                FormField("timeout_seconds", kind="number", default=10),
            ),
        )


plugin = DingTalkNotifierPlugin()

__all__ = ["DingTalkNotifier", "DingTalkNotifierPlugin", "plugin"]
