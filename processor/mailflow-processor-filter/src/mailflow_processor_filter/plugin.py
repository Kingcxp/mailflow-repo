"""Rule-based filter processor: marks matching mail as junk (ad).

A cheap deterministic pre-filter (no LLM): exact sender addresses, subject
substrings and body keywords are matched case-insensitively. Matches are
classified as ``ad`` (gray) so they drop out of notifier thresholds
immediately. Options: ``senders`` (list), ``subjects`` (list of substrings),
``keywords`` (list of body substrings).
"""

from __future__ import annotations

from typing import Any

from mailflow.config import ProcessorConfig
from mailflow.contracts import LLMRouter, MailMessage, ProcessingContext, ProcessorResult
from mailflow.domain import ComponentKind, MailAnalysis, Urgency
from mailflow.plugins import PluginInfo
from mailflow.registry import PluginRegistrar

PLUGIN_INFO = PluginInfo(
    plugin_id="mailflow-processor-filter",
    name="Rule Filter Processor",
    version="0.1.0",
    description="Marks mail matching sender/subject/keyword rules as junk (gray)",
    kinds=[ComponentKind.MAIL_PROCESSOR],
)


class FilterProcessor:
    processor_id = "filter"

    def __init__(self, config: ProcessorConfig, router: LLMRouter | None = None) -> None:
        self._senders = {str(s).lower() for s in config.options.get("senders", [])}
        self._subjects = [str(s).lower() for s in config.options.get("subjects", [])]
        self._keywords = [str(k).lower() for k in config.options.get("keywords", [])]

    async def process(self, mail: MailMessage, context: ProcessingContext) -> ProcessorResult:
        sender = (mail.sender.address or "").lower()
        subject = (mail.subject or "").lower()
        body = (mail.body_text or "").lower()
        if sender in self._senders:
            return self._ad(f"sender {sender} is on the filter list")
        for sub in self._subjects:
            if sub and sub in subject:
                return self._ad(f"subject contains {sub!r}")
        for keyword in self._keywords:
            if keyword and keyword in body:
                return self._ad(f"body contains {keyword!r}")
        return ProcessorResult()

    @staticmethod
    def _ad(reason: str) -> ProcessorResult:
        return ProcessorResult(
            analysis=MailAnalysis(
                summary="Filtered mail", urgency=Urgency.AD, reason=reason, backend=""
            )
        )


class FilterPlugin:
    def mailflow_plugin_info(self) -> PluginInfo:
        return PLUGIN_INFO

    def mailflow_register(self, registrar: PluginRegistrar, config: Any) -> None:
        registrar.add_processor("filter", FilterProcessor)


plugin = FilterPlugin()

__all__ = ["FilterPlugin", "FilterProcessor", "plugin"]
