<!-- Generated from plugin.json by tools/gen_plugin_readmes.py. Edit plugin.json. -->

# Google Generative AI backend

Component ID: `google-generative-ai`. Uses Gemini `generateContent`, translating
system messages and structured tool calls from the shared MailFlow contract.

```toml
[[llms]]
llm_id = "primary"
provider = "google-generative-ai"
model = "your-model-id"
api_key_env = "GEMINI_API_KEY"
```

The default root is `https://generativelanguage.googleapis.com`; `base_url`
overrides it for a compatible proxy. Requests use
`/v1beta/models/{model}:generateContent` and the `x-goog-api-key` header.
`options.max_tokens`, `temperature` and `thinking_budget` set optional generation
defaults. Standard headers/query, `extra_body`, timeout and retry settings apply.

Use a model available to your account. Tool and generation capabilities depend
on that model; connection/parameter failures remain visible and can fall back
through the configured model chain. This plugin is an API transport, not a
browser-login integration.

---

<!-- zh-CN -->

# Google Generative AI 后端

组件标识为 `google-generative-ai`，使用 Gemini 的 `generateContent`，
转换共享系统消息和结构化工具调用。

```toml
[[llms]]
llm_id = "primary"
provider = "google-generative-ai"
model = "your-model-id"
api_key_env = "GEMINI_API_KEY"
```

默认根地址为 `https://generativelanguage.googleapis.com`，可用 `base_url` 覆盖代理地址。
请求路径为 `/v1beta/models/{model}:generateContent`，密钥通过 `x-goog-api-key` 发送。
`options.max_tokens`、`temperature`、`thinking_budget` 可设置生成默认值，
也支持共享请求头、查询、额外请求体、超时和重试。

选择账户实际可用且支持所需工具能力的模型。连接或参数失败会明确报告，并按配置回退。
本插件是 API 传输，不提供浏览器账号登录。

---

[Catalog](../../README.md) · [Metadata](plugin.json) · [Plugin page](https://github.com/Kingcxp/mailflow-repo/tree/main/llm_backend/mailflow-llm-google-generative-ai)
