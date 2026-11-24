"""Provider preset using Waymark Mail's shared OpenAI transport."""

from __future__ import annotations

from mailflow.config import LLMConfig, MailFlowConfig
from mailflow.domain import ComponentKind
from mailflow.plugins import PluginInfo
from mailflow.registry import PluginRegistrar
from mailflow_llm_openai_compatible.plugin import OpenAIBackend


class OpenAICompatBackend(OpenAIBackend):
    """Resolve preset defaults; inherit tools, options and retries unchanged."""

    default_base_url = ""
    default_model = ""

    def __init__(self, config: LLMConfig) -> None:
        resolved = config.model_copy(deep=True)
        if not resolved.base_url or resolved.base_url == "https://api.openai.com/v1":
            resolved.base_url = self.default_base_url
        if not resolved.model or resolved.model == "gpt-4o-mini":
            resolved.model = self.default_model
        super().__init__(resolved)


class MoonshotBackend(OpenAICompatBackend):
    backend_id = "moonshot"
    default_base_url = "https://api.moonshot.cn/v1"
    default_model = "moonshot-v1-8k"


PLUGIN_INFO = PluginInfo(
    plugin_id="mailflow-llm-moonshot",
    name="Moonshot LLM Backend",
    version="0.1.0",
    description="OpenAI-compatible chat completions transport for Moonshot AI (component id: moonshot)",
    kinds=[ComponentKind.LLM_BACKEND],
)


class LLMPlugin:
    def mailflow_plugin_info(self) -> PluginInfo:
        return PLUGIN_INFO

    def mailflow_register(self, registrar: PluginRegistrar, config: MailFlowConfig) -> None:
        registrar.add_llm("moonshot", MoonshotBackend)


plugin = LLMPlugin()

__all__ = ["LLMPlugin", "MoonshotBackend", "OpenAICompatBackend", "plugin"]
