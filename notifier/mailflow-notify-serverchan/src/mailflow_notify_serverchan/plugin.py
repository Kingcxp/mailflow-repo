"""ServerChan notifier: pushes mail summaries to ServerChan.

Standard library only (urllib); the endpoint URL and credentials come from
the notifier options. Delivery failures are logged by the runtime and never
fail mail processing.
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

logger = logging.getLogger("mailflow.notification.serverchan")

PLUGIN_INFO = PluginInfo(
    plugin_id="mailflow-notify-serverchan",
    name="ServerChan Notifier",
    version="0.1.0",
    description="Push mail alerts via ServerChan (方糖)",
    kinds=[ComponentKind.NOTIFIER],
)


class ServerChanNotifier:
    """ServerChan delivery channel. Options documented in plugin.json."""

    def __init__(self, config: NotifierConfig) -> None:
        self._options = dict(config.options)
        self._timeout = float(self._options.get("timeout_seconds", 10))

    def _target_url(self) -> str:
        raise NotImplementedError

    def _payload(self, record: MailRecord) -> dict[str, Any]:
        raise NotImplementedError

    def _target_url(self) -> str:
        key = str(self._options.get("send_key", ""))
        return f"https://sctapi.ftqq.com/{key}.send" if key else ""

    def _payload(self, record: MailRecord) -> dict[str, Any]:
        return {
            "title": str(self._options.get("title") or f"[MailFlow] {record.mail.subject}"),
            "desp": f"{record.effective_urgency.value.upper()} {record.summary}",
        }

    async def notify(self, record: MailRecord) -> None:
        url = self._target_url()
        if not url:
            logger.warning("%(log)s notifier has no endpoint; skipping", {"log": "serverchan"})
            return
        request = urllib.request.Request(
            url,
            data=json.dumps(self._payload(record)).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        await asyncio.to_thread(urllib.request.urlopen, request, timeout=self._timeout)


class ServerChanNotifierPlugin:
    def mailflow_plugin_info(self) -> PluginInfo:
        return PLUGIN_INFO

    def mailflow_register(self, registrar: PluginRegistrar, config: Any) -> None:
        registrar.add_notifier("serverchan", ServerChanNotifier)


plugin = ServerChanNotifierPlugin()

__all__ = ["ServerChanNotifier", "ServerChanNotifierPlugin", "plugin"]
