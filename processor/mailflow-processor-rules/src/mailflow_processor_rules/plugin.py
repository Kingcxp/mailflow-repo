"""Rule-templates processor: applies the first matching rule.

Options: ``rules`` is a list of dicts:
{ "match": {"field": "sender"|"subject"|"body", "contains": "..."},
  "action": {"urgency": "ad"|"info"|"important"|"urgent", "summary": "..."} }
The first rule whose ``contains`` substring appears in the chosen field is
applied; its action becomes the analysis overlay.
"""

from __future__ import annotations

from typing import Any

from mailflow.config import ProcessorConfig
from mailflow.contracts import LLMRouter, MailMessage, ProcessingContext, ProcessorResult
from mailflow.domain import ComponentKind, MailAnalysis, Urgency
from mailflow.plugins import PluginInfo
from mailflow.registry import PluginRegistrar

PLUGIN_INFO = PluginInfo(
    plugin_id="mailflow-processor-rules",
    name="Rule Templates Processor",
    version="0.1.0",
    description="Applies the first matching rule template to each mail",
    kinds=[ComponentKind.MAIL_PROCESSOR],
)


class RulesProcessor:
    processor_id = "rules"

    def __init__(self, config: ProcessorConfig, router: LLMRouter | None = None) -> None:
        self._rules: list[dict[str, Any]] = list(config.options.get("rules", []) or [])

    @staticmethod
    def _field_value(mail: MailMessage, field: str) -> str:
        return {
            "sender": mail.sender.address or "",
            "subject": mail.subject or "",
            "body": mail.body_text or "",
        }.get(field, "").lower()

    async def process(self, mail: MailMessage, context: ProcessingContext) -> ProcessorResult:
        for rule in self._rules:
            match = rule.get("match") or {}
            action = rule.get("action") or {}
            field = str(match.get("field", "subject")).lower()
            contains = str(match.get("contains", "")).lower()
            if not contains:
                continue
            if contains not in self._field_value(mail, field):
                continue
            try:
                urgency = Urgency(str(action.get("urgency", "info")).lower())
            except ValueError:
                urgency = Urgency.INFO
            summary = str(action.get("summary") or "Rule matched")
            return ProcessorResult(
                analysis=MailAnalysis(
                    summary=summary,
                    urgency=urgency,
                    reason=f"rule '{contains}' matched field {field}",
                    backend="",
                )
            )
        return ProcessorResult()


class RulesPlugin:
    def mailflow_plugin_info(self) -> PluginInfo:
        return PLUGIN_INFO

    def mailflow_register(self, registrar: PluginRegistrar, config: Any) -> None:
        registrar.add_processor("rules", RulesProcessor)


plugin = RulesPlugin()

__all__ = ["RulesPlugin", "RulesProcessor", "plugin"]
