# Writing an LLM backend

An `llm_backend` plugin plugs a chat-completions provider into MailFlow's
LLM routing: summaries, urgency classification and suggested replies.

## Contract

```python
class LLMBackend:
    backend_id: str  # component id

    async def chat(
        self,
        messages: list[dict[str, str]],          # [{"role": "system"|"user"|"assistant", "content": …}]
        *,
        temperature: float | None = None,
        options: dict[str, Any] | None = None,
    ) -> LLMCompletion: ...
```

`LLMCompletion` requires `text` and optionally carries `model`, `backend_id`
(should be your component id) and a `raw` dict for provider-specific detail.

## Key points

- **Return `LLMCompletion`, never a bare string.** The router stamps the
  actual backend used so the pipeline can report which model produced which
  result.
- **Honor `temperature`** when the provider supports it.
- **Streaming is optional.** The router consumes a single completion; if you
  need streaming, add it via `options` later — keep `chat` returning a
  complete `LLMCompletion`.
- **Authentication** comes from the LLM config the factory receives
  (`LLMConfig` with `api_key`, `base_url`, …). Never hardcode secrets; read
  environment variables via the config (e.g. `"${MY_API_KEY}"` is expanded by
  MailFlow config loading).

## Registration

```python
def mailflow_register(self, registrar: PluginRegistrar, config) -> None:
    registrar.add_llm("my-provider", MyBackend)
```

```toml
[[llms]]
llm_id = "my"
provider = "my-provider"          # component id
enabled = true
[llms.options]
model = "my-model-v2"
api_key = "${MY_API_KEY}"
```

## What the pipeline does with your completion

The configured `provider` for each `[[llms]]` entry is resolved to your
backend; the router calls `chat` with a system prompt plus the mail content,
then parses structured JSON (summary, urgency, reply suggestions) out of the
response. Keep your output formatted — follow the system prompt MailFlow
sends, or the parse fails loudly and MailFlow falls back to the next LLM.
