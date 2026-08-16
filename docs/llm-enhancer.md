# LLM enhancers

LLM enhancers are processor plugins that extend the built-in LLM analysis
(`rules` + `llm-importance` processors live in `mailflow-core` and run with
zero plugins). An enhancer never reimplements classification; it shapes the
built-in analysis through three optional hooks.

## Contract

```python
class LLMEnhancer(Protocol):
    def system_prompt(self, base: str) -> str: ...
    def extra_messages(self, mail, context) -> list[dict[str, str]]: ...
    def post_process(self, analysis, mail, context): ...
```

- `system_prompt` — append guidance to the built-in prompt (results chain
  in registration order).
- `extra_messages` — chat turns appended after the user message.
- `post_process` — run in order over the parsed analysis; return a modified
  copy or `None` to leave it unchanged.

Every hook is optional. Aggregation is implemented by `mailflow-core`, so
enhancers never call the LLM router directly.

## Registration

```python
@PLUGIN.llm_enhancer("my-enhancer")
class MyEnhancer:
    def __init__(self, config: ProcessorConfig) -> None: ...

    def system_prompt(self, base: str) -> str:
        return f"{base}\nSummaries must be written in Chinese."
```

Enhancers are configured as ordinary processors:

```toml
[[processors]]
processor_id = "my-enhancer"
provider = "my-enhancer"
priority = 20
[processors.options]
lang = "zh-CN"
```

The category folder is `llm_enhancer/`; the scaffold template
(`llm_enhancer`) generates a matching plugin skeleton.

## Rules for authors

- Keep enhancers deterministic and cheap — they run on every analysis.
- Never log credentials or raw API keys; sanitize error text.
- A plugin that registers a `MAIL_PROCESSOR` component id used by core
  (`rules`, `llm-importance`) replaces the built-in implementation — use
  that only for a deliberate fork of the built-in step.
