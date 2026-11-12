<!-- Generated from plugin.json by tools/gen_plugin_readmes.py. Edit plugin.json. -->

# Anthropic Messages backend

Component IDs: `anthropic-messages` and compatible alias `anthropic`. Translates
the shared chat/tool format into Messages requests and returns structured tool calls.

```toml
[[llms]]
llm_id = "primary"
provider = "anthropic"
model = "your-model-id"
api_key_env = "ANTHROPIC_API_KEY"

[llms.options]
max_tokens = 2048
```

The default endpoint is `https://api.anthropic.com/v1/messages`. A top-level
`base_url` may name a proxy root, `/v1` prefix or complete `/messages` endpoint;
legacy `options.base_url` is a complete endpoint override. `options.max_tokens`
defaults to 1024. Optional `thinking_budget` requests a budget supported by the
selected model and raises the output cap as needed.

Standard timeout, retry, headers, query and extra-body configuration applies.
The backend accepts temperature, per-call options and tools; the selected model
must support the requested features. Choose a currently available model ID and
check credentials/endpoint on failure. Do not put real keys in configuration
examples or logs. Model ordering and fallback use the shared MailFlow settings.

---

<!-- zh-CN -->

# Anthropic Messages 后端

组件标识为 `anthropic-messages`，兼容旧标识 `anthropic`。
将共享对话和工具格式转换为 Messages 请求，并返回结构化工具调用。

```toml
[[llms]]
llm_id = "primary"
provider = "anthropic"
model = "your-model-id"
api_key_env = "ANTHROPIC_API_KEY"

[llms.options]
max_tokens = 2048
```

默认端点为 `https://api.anthropic.com/v1/messages`。
顶层 `base_url` 可填写代理根地址、`/v1` 前缀或完整端点；兼容的 `options.base_url`
按完整端点覆盖。`max_tokens` 默认 1024，按需设置模型支持的 `thinking_budget`。

支持共享超时、重试、请求头、查询和额外请求体配置，传递温度、单次选项和工具。
模型本身也需支持所用能力，请填写实际可用模型名，失败时检查凭据与端点。
主模型和后备使用 MailFlow 的统一设置，不在示例或日志中填写真实密钥。

---

[Catalog](../../README.md) · [Metadata](plugin.json) · [Plugin page](https://github.com/Kingcxp/mailflow-repo/tree/main/llm_backend/mailflow-llm-anthropic)
