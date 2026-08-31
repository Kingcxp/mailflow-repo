"""Auto-archive processor: marks matching mail as info and notes it.

A cheap deterministic pre-filter (no LLM): exact sender addresses and full
domain suffixes are matched case-insensitively; matched mail is classified
as ``info`` and flagged 'auto-archived' in the notes. Options: ``senders``
(list), ``domains`` (list of domain suffixes, matched with ``@domain``).
"""

from __future__ import annotations

from typing import Any

from mailflow.config import ProcessorConfig
from mailflow.contracts import LLMRouter, MailMessage, ProcessingContext, ProcessorResult
from mailflow.domain import ComponentKind, MailAnalysis, Urgency
from mailflow.plugins import PluginInfo
from mailflow.registry import PluginRegistrar

PLUGIN_INFO = PluginInfo(
    plugin_id="mailflow-processor-archive",
    name="Auto-Archive Processor",
    version="0.1.0",
    description="Flags mail from matching senders/domains as info + auto-archived",
    kinds=[ComponentKind.MAIL_PROCESSOR],
)


class ArchiveProcessor:
    processor_id = "archive"

    def __init__(self, config: ProcessorConfig, router: LLMRouter | None = None) -> None:
        self._senders = {str(s).lower() for s in config.options.get("senders", [])}
        self._domains = {str(d).lower() for d in config.options.get("domains", [])}

    async def process(self, mail: MailMessage, context: ProcessingContext) -> ProcessorResult:
        sender = (mail.sender.address or "").lower()
        matched = sender in self._senders or any(
            sender.endswith(f"@{domain}") for domain in self._domains
        )
        if not matched:
            return ProcessorResult()
        return ProcessorResult(
            analysis=MailAnalysis(
                summary="Auto-archived",
                urgency=Urgency.INFO,
                reason=f"sender {sender} matched the archive rules",
                backend="",
            ),
            notes=["auto-archived"],
        )


class ArchivePlugin:
    def mailflow_plugin_info(self) -> PluginInfo:
        return PLUGIN_INFO

    def mailflow_register(self, registrar: PluginRegistrar, config: Any) -> None:
        registrar.add_processor("archive", ArchiveProcessor)


plugin = ArchivePlugin()

__all__ = ["ArchivePlugin", "ArchiveProcessor", "plugin"]
