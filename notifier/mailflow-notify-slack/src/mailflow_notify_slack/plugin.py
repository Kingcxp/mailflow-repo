"""Slack notifier: pushes mail summaries to Slack.

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

logger = logging.getLogger("mailflow.notification.slack")

PLUGIN_INFO = PluginInfo(
    plugin_id="mailflow-notify-slack",
    name="Slack Notifier",
    version="0.1.0",
    description="Push mail alerts to a Slack incoming webhook",
    kinds=[ComponentKind.NOTIFIER],
)


class SlackNotifier:
    """Slack delivery channel. Options documented in plugin.json."""

    def __init__(self, config: NotifierConfig) -> None:
        self._options = dict(config.options)
        self._timeout = float(self._options.get("timeout_seconds", 10))

    def _target_url(self) -> str:
        raise NotImplementedError

    def _payload(self, record: MailRecord) -> dict[str, Any]:
        raise NotImplementedError

    def _target_url(self) -> str:
        return str(self._options.get("webhook_url", ""))

    def _payload(self, record: MailRecord) -> dict[str, Any]:
        payload = {"text": self._summary_text(record)}
        channel = str(self._options.get("channel", ""))
        if channel:
            payload["channel"] = channel
        return payload

    @staticmethod
    def _summary_text(record: MailRecord) -> str:
        return (
            f"[MailFlow] {record.effective_urgency.value.upper()} "
            f"{record.mail.subject}\n{record.summary}"
        )

    async def notify(self, record: MailRecord) -> None:
        url = self._target_url()
        if not url:
            logger.warning("%(log)s notifier has no endpoint; skipping", {"log": "slack"})
            return
        request = urllib.request.Request(
            url,
            data=json.dumps(self._payload(record)).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        await asyncio.to_thread(urllib.request.urlopen, request, timeout=self._timeout)


class SlackNotifierPlugin:
    def mailflow_plugin_info(self) -> PluginInfo:
        return PLUGIN_INFO

    def mailflow_register(self, registrar: PluginRegistrar, config: Any) -> None:
        registrar.add_notifier("slack", SlackNotifier)


plugin = SlackNotifierPlugin()

__all__ = ["SlackNotifier", "SlackNotifierPlugin", "plugin"]
