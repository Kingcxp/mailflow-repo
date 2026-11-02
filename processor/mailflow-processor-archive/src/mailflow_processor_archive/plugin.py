"""Archive matching senders in MailFlow while preserving analysis and source mail."""

from __future__ import annotations

from typing import Any

from mailflow.config import ProcessorConfig
from mailflow.contracts import LLMRouter, MailMessage, ProcessingContext, ProcessorResult
from mailflow.domain import ComponentKind
from mailflow.plugins import PluginInfo
from mailflow.registry import PluginRegistrar

PLUGIN_INFO = PluginInfo(
    plugin_id="mailflow-processor-archive",
    name="Auto-Archive Processor",
    version="0.1.0",
    description="Archives matching senders/domains in MailFlow; source mail and priority are preserved",
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
        return ProcessorResult(archive=True, notes=["archive rule matched"])


class ArchivePlugin:
    def mailflow_plugin_info(self) -> PluginInfo:
        return PLUGIN_INFO

    def mailflow_register(self, registrar: PluginRegistrar, config: Any) -> None:
        registrar.add_processor("archive", ArchiveProcessor)


plugin = ArchivePlugin()

__all__ = ["ArchivePlugin", "ArchiveProcessor", "plugin"]
