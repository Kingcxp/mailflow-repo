"""Sender blocklist processor: marks mail from blocked senders/domains as junk.

A cheap deterministic pre-filter (no LLM): exact sender addresses and full
domain suffixes are matched case-insensitively. Matches are classified as
``ad`` (gray) so they drop out of notifier thresholds immediately.
"""

from __future__ import annotations

from typing import Any

from mailflow.config import ProcessorConfig
from mailflow.contracts import LLMRouter, MailMessage, ProcessingContext, ProcessorResult
from mailflow.domain import ComponentKind, MailAnalysis, Urgency
from mailflow.plugins import PluginInfo
from mailflow.registry import PluginRegistrar

PLUGIN_INFO = PluginInfo(
    plugin_id="mailflow-processor-blocklist",
    name="Sender Blocklist Processor",
    version="0.1.0",
    description="Marks mail from blocked senders or domains as junk (gray)",
    kinds=[ComponentKind.MAIL_PROCESSOR],
)


class BlocklistProcessor:
    processor_id = "blocklist"

    def __init__(self, config: ProcessorConfig, router: LLMRouter | None = None) -> None:
        self._senders = {str(addr).lower() for addr in config.options.get("senders", [])}
        self._domains = {str(domain).lower() for domain in config.options.get("domains", [])}

    def _is_blocked(self, address: str) -> bool:
        normalized = address.lower()
        if normalized in self._senders:
            return True
        return any(normalized.endswith(f"@{domain}") for domain in self._domains)

    async def process(self, mail: MailMessage, context: ProcessingContext) -> ProcessorResult:
        if self._is_blocked(mail.sender.address):
            return ProcessorResult(
                analysis=MailAnalysis(
                    summary="Blocked sender",
                    urgency=Urgency.AD,
                    reason=f"sender {mail.sender.address} is on the blocklist",
                    backend="",
                )
            )
        return ProcessorResult()


class BlocklistPlugin:
    def mailflow_plugin_info(self) -> PluginInfo:
        return PLUGIN_INFO

    def mailflow_register(self, registrar: PluginRegistrar, config: Any) -> None:
        registrar.add_processor("blocklist", BlocklistProcessor)


plugin = BlocklistPlugin()

__all__ = ["BlocklistPlugin", "BlocklistProcessor", "plugin"]
