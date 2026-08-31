# LLM backends

Chat-completions transports that power summaries, urgency and suggested replies.

| Plugin | Description |
|---|---|
| [mailflow-llm-deepseek](mailflow-llm-deepseek/) | OpenAI-compatible chat completions transport for DeepSeek (component id: deepseek) |
| [mailflow-llm-moonshot](mailflow-llm-moonshot/) | OpenAI-compatible chat completions transport for Moonshot AI / Kimi (component id: moonshot) |
| [mailflow-llm-qwen](mailflow-llm-qwen/) | OpenAI-compatible chat completions transport for Alibaba Qwen / DashScope (component id: qwen) |
| [mailflow-llm-zhipu](mailflow-llm-zhipu/) | OpenAI-compatible chat completions transport for Zhipu GLM / BigModel (component id: zhipu) |

### Adding a plugin

Create a folder `llm_backend/<plugin-id>/` with `plugin.json` and the plugin source, then open a pull request. The PR workflow validates it automatically.

See [docs/02-categories.md](../docs/02-categories.md) for the contract and [docs/00-getting-started.md](../docs/00-getting-started.md) for the full guide.
