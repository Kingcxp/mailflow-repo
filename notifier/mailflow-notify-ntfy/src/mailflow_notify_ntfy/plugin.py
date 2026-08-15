"""ntfy notifier: pushes mail alerts to an ntfy topic.

Works with the public ntfy.sh service or a self-hosted ntfy server. The topic
is taken from the notifier options (``topic``) or the account-independent
``base_url`` + ``topic``. An optional ``token`` enables private topics via the
Bearer auth header. Standard library only (urllib).
"""

from __future__ import annotations

import asyncio
import json
import logging
import urllib.request
from typing import Any

from mailflow.config import NotifierConfig
from mailflow.domain import ComponentKind, MailRecord, Urgency
from mailflow.plugins import PluginInfo
from mailflow.registry import PluginRegistrar

logger = logging.getLogger("mailflow.notification.ntfy")

PLUGIN_INFO = PluginInfo(
    plugin_id="mailflow-notify-ntfy",
    name="ntfy Notifier",
    version="0.1.0",
    description="Push mail alerts to any ntfy.sh topic (or a self-hosted ntfy server)",
    kinds=[ComponentKind.NOTIFIER],
)

_NTFY_PRIORITY = {
    Urgency.AD: 1,  # min
    Urgency.INFO: 3,  # default
    Urgency.IMPORTANT: 4,  # high
    Urgency.URGENT: 5,  # urgent
}


class NtfyNotifier:
    def __init__(self, config: NotifierConfig) -> None:
        self._base_url = str(config.options.get("base_url", "https://ntfy.sh")).rstrip("/")
        self._topic = str(config.options.get("topic", ""))
        self._token = str(config.options.get("token", ""))
        self._timeout = float(config.options.get("timeout_seconds", 10))

    async def notify(self, record: MailRecord) -> None:
        if not self._topic:
            logger.warning("ntfy notifier has no topic option; skipping")
            return
        url = f"{self._base_url}/{self._topic}"
        headers = {"Content-Type": "application/json"}
        if self._token:
            headers["Authorization"] = f"Bearer {self._token}"
        payload = {
            "topic": self._topic,
            "title": record.mail.subject,
            "message": record.summary,
            "priority": _NTFY_PRIORITY[record.effective_urgency],
            "tags": ["envelope"],
        }
        request = urllib.request.Request(
            url, data=json.dumps(payload).encode("utf-8"), headers=headers, method="POST"
        )
        await asyncio.to_thread(urllib.request.urlopen, request, timeout=self._timeout)


class NtfyPlugin:
    def mailflow_plugin_info(self) -> PluginInfo:
        return PLUGIN_INFO

    def mailflow_register(self, registrar: PluginRegistrar, config: Any) -> None:
        registrar.add_notifier("ntfy", NtfyNotifier)


plugin = NtfyPlugin()

__all__ = ["NtfyNotifier", "NtfyPlugin", "plugin"]
