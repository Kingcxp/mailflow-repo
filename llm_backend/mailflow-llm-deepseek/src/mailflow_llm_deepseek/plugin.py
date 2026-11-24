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


class DeepSeekBackend(OpenAICompatBackend):
    backend_id = "deepseek"
    default_base_url = "https://api.deepseek.com/v1"
    default_model = "deepseek-chat"


PLUGIN_INFO = PluginInfo(
    plugin_id="mailflow-llm-deepseek",
    name="DeepSeek LLM Backend",
    version="0.1.0",
    description="OpenAI-compatible chat completions transport for DeepSeek (component id: deepseek)",
    kinds=[ComponentKind.LLM_BACKEND],
)


class LLMPlugin:
    def mailflow_plugin_info(self) -> PluginInfo:
        return PLUGIN_INFO

    def mailflow_register(self, registrar: PluginRegistrar, config: MailFlowConfig) -> None:
        registrar.add_llm("deepseek", DeepSeekBackend)


plugin = LLMPlugin()

__all__ = ["DeepSeekBackend", "LLMPlugin", "OpenAICompatBackend", "plugin"]
