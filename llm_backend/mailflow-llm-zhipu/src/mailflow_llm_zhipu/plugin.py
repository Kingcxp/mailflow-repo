"""Zhipu LLM backend (OpenAI-compatible chat completions).

Component id ``zhipu``. Thin config preset over the OpenAI-compatible
Chat Completions transport:

    POST https://open.bigmodel.cn/api/paas/v4/chat/completions
    Authorization: Bearer <api key>

Defaults: base_url ``https://open.bigmodel.cn/api/paas/v4``,
model ``glm-4-flash``. The standard library's urllib performs the POST on a
worker thread, so the plugin has no third-party runtime dependency beyond
``mailflow-core``. Only transient failures — timeouts, transport errors,
HTTP 408/429/5xx — are retried, with exponential backoff capped at 5 s.
Error text is sanitized so no URL or key material ever surfaces.
"""

from __future__ import annotations

import asyncio
import json
import logging
import socket
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

from mailflow.config import LLMConfig
from mailflow.contracts import LLMCompletion, MessageDict
from mailflow.domain import ComponentKind
from mailflow.plugins import PluginInfo
from mailflow.registry import PluginRegistrar

logger = logging.getLogger("mailflow.llm.zhipu")

_MAX_BACKOFF_SECONDS = 5.0
_RETRYABLE_STATUS = {408, 429, *range(500, 600)}
# LLMConfig ships OpenAI defaults; a value still equal to one of these means
# the field was not explicitly set, so this provider preset's default applies.
_UNSET = ("https://api.openai.com/v1", "gpt-4o-mini")


def _retryable(exc: Exception) -> bool:
    if isinstance(exc, urllib.error.HTTPError):
        return exc.code in _RETRYABLE_STATUS
    if isinstance(exc, (urllib.error.URLError, socket.timeout, TimeoutError, OSError)):
        return True
    return False


class OpenAICompatBackend:
    """Standard-library OpenAI-compatible chat completions transport.

    Subclass and override ``backend_id``, ``default_base_url`` and
    ``default_model`` to target a concrete provider preset.
    """

    backend_id = "openai-compat"
    default_base_url = ""
    default_model = ""

    def __init__(self, config: LLMConfig) -> None:
        self._config = config
        self._path = str(config.options.get("path", "chat/completions"))
        self._base = self._resolve(config.base_url, self.default_base_url).rstrip("/")
        self._model = self._resolve(config.model, self.default_model)

    @staticmethod
    def _resolve(value: str, default: str) -> str:
        if not value or value in _UNSET:
            return default or value
        return value

    def _query(self, options: dict[str, Any] | None) -> dict[str, str]:
        merged: dict[str, str] = {str(k): str(v) for k, v in self._config.query.items()}
        if options and isinstance(options.get("query"), dict):
            merged.update({str(k): str(v) for k, v in options["query"].items()})
        return merged

    def _url(self, options: dict[str, Any] | None) -> str:
        url = f"{self._base}/{self._path.lstrip('/')}"
        params = self._query(options)
        if params:
            url = f"{url}?{urllib.parse.urlencode(params)}"
        return url

    def _headers(self, options: dict[str, Any] | None) -> dict[str, str]:
        merged: dict[str, str] = {"Content-Type": "application/json"}
        merged.update({str(k): str(v) for k, v in self._config.headers.items()})
        if self._config.api_key:
            merged.setdefault("Authorization", f"Bearer {self._config.api_key}")
        if options and isinstance(options.get("headers"), dict):
            merged.update({str(k): str(v) for k, v in options["headers"].items()})
        return merged

    def _body(
        self,
        messages: list[MessageDict],
        temperature: float | None,
        options: dict[str, Any] | None,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"model": self._model, "messages": messages}
        if temperature is not None:
            body["temperature"] = temperature
        body.update(self._config.extra_body)
        if options:
            if isinstance(options.get("body"), dict):
                body.update(options["body"])
            if "model" in options:
                body["model"] = options["model"]
            if "temperature" in options:
                body["temperature"] = options["temperature"]
        return body

    @staticmethod
    def _sanitize(exc: Exception) -> str:
        """Error text without URLs, query strings or header details."""
        if isinstance(exc, urllib.error.HTTPError):
            return f"HTTP {exc.code}: {exc.reason or 'request failed'}"
        if isinstance(exc, (socket.timeout, TimeoutError)):
            return "request timed out"
        if isinstance(exc, urllib.error.URLError):
            return "transport error"
        return str(exc)

    @staticmethod
    def _post(
        url: str,
        headers: dict[str, str],
        body: dict[str, Any],
        timeout: float,
    ) -> LLMCompletion:
        request = urllib.request.Request(
            url,
            data=json.dumps(body).encode("utf-8"),
            headers=headers,
            method="POST",
        )
        with urllib.request.urlopen(request, timeout=timeout) as response:
            payload: dict[str, Any] = json.loads(response.read().decode("utf-8"))
        return _parse(payload)

    async def chat(
        self,
        messages: list[MessageDict],
        *,
        temperature: float | None = None,
        options: dict[str, Any] | None = None,
    ) -> LLMCompletion:
        url = self._url(options)
        headers = self._headers(options)
        body = self._body(messages, temperature, options)
        max_retries = max(0, min(self._config.max_retries, 20))

        last_error: Exception | None = None
        for attempt in range(max_retries + 1):
            try:
                return await asyncio.to_thread(
                    self._post, url, headers, body, self._config.timeout_seconds
                )
            except Exception as exc:
                last_error = exc
                if attempt >= max_retries or not _retryable(exc):
                    break
                backoff = min(2**attempt, _MAX_BACKOFF_SECONDS)
                logger.debug(
                    "%s attempt %d/%d failed (%s); retrying in %.1fs",
                    self.backend_id,
                    attempt + 1,
                    max_retries + 1,
                    self._sanitize(exc),
                    backoff,
                )
                await asyncio.sleep(backoff)

        assert last_error is not None
        raise RuntimeError(f"llm request failed: {self._sanitize(last_error)}")


def _parse(payload: dict[str, Any]) -> LLMCompletion:
    choices: Any = payload.get("choices") or []
    if not choices:
        raise RuntimeError("response contained no choices")
    message: Any = choices[0].get("message") or {}
    content: Any = message.get("content") or ""
    if isinstance(content, list):
        # some endpoints return content parts (e.g. [{"type": "text", "text": ...}])
        parts: list[str] = []
        for part in content:
            if isinstance(part, dict):
                text = part.get("text")
                if text:
                    parts.append(str(text))
            elif isinstance(part, str):
                parts.append(part)
        content = "".join(parts)
    raw_model: Any = payload.get("model") or ""
    return LLMCompletion(text=str(content), model=str(raw_model), raw=payload)


class ZhipuBackend(OpenAICompatBackend):
    backend_id = "zhipu"
    default_base_url = "https://open.bigmodel.cn/api/paas/v4"
    default_model = "glm-4-flash"


PLUGIN_INFO = PluginInfo(
    plugin_id="mailflow-llm-zhipu",
    name="Zhipu LLM Backend",
    version="0.1.0",
    description="OpenAI-compatible chat completions transport for Zhipu GLM (component id: zhipu)",
    kinds=[ComponentKind.LLM_BACKEND],
)


class LLMPlugin:
    def mailflow_plugin_info(self) -> PluginInfo:
        return PLUGIN_INFO

    def mailflow_register(self, registrar: PluginRegistrar, config) -> None:
        registrar.add_llm("zhipu", ZhipuBackend)


plugin = LLMPlugin()

__all__ = ["LLMPlugin", "OpenAICompatBackend", "ZhipuBackend", "plugin"]
