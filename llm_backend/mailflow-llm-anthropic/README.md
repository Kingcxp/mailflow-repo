<!-- Generated from plugin.json by tools/gen_plugin_readmes.py. Edit plugin.json. -->

## Anthropic LLM Backend

The built-in Anthropic Messages API backend (Claude). Ships with every MailFlow
install alongside the OpenAI-compatible backend, so it needs no install step —
just add a named LLM.

Registers the LLM backend component id `anthropic`.

### How it works

MailFlow's processors speak one chat format; this backend translates it to the
Anthropic Messages shape: the system prompt travels in the top-level `system`
field and the remaining messages keep their `user`/`assistant` roles. The API
key is sent only through the `x-api-key` header, alongside
`anthropic-version: 2023-06-01`.

Requests are retried up to three times with exponential backoff (capped at 5s).
Errors are sanitized before they surface: anything containing a URL is reduced
to `transport error`, so a request URL — which may carry credentials — can never
reach a persisted `ProcessorNote`. The core router additionally redacts every
configured API key from aggregated failures.

### Options

Standard `[[llms]]` fields apply (`model`, `api_key`, `api_key_env`, `headers`,
`timeout_seconds`, `max_retries`, `fallback`). Backend-specific entries live in
`[llms.options]`:

| Option | Default | Meaning |
| ------ | ------- | ------- |
| `base_url` | `https://api.anthropic.com/v1/messages` | Full messages endpoint (not a prefix). |
| `max_tokens` | `1024` | Anthropic requires an explicit output cap. |

### Usage

```toml
[[llms]]
llm_id = "claude"
provider = "anthropic"
model = "claude-3-5-sonnet-latest"
api_key_env = "ANTHROPIC_API_KEY"    # or api_key = "${ANTHROPIC_API_KEY}"
timeout_seconds = 60

[llms.options]
max_tokens = 2048
```

In the TUI's **LLMs** tab the list order is the fallback chain: put Claude first
to make it the default, or below another entry to use it only as a fallback.

### Notes

- `api_key_env` is resolved at every start and is never written back into the
  config file, so rotating the key means changing the environment variable only.
- Raise `max_tokens` if long mails come back with truncated JSON; the built-in
  analysis prompt expects one complete JSON object.

### Requirements

`httpx`, plus `mailflow-core`.

### License

MIT — contributions welcome.

---

<!-- zh-CN -->

## Anthropic 大模型后端

内置的 Anthropic Messages API 后端（Claude）。它与 OpenAI 兼容后端一同随每个
MailFlow 安装提供，无需安装步骤 —— 直接添加一个具名大模型即可。

注册的大模型后端组件 id 为 `anthropic`。

### 工作方式

MailFlow 的处理器只使用一种对话格式，本后端负责把它翻译为 Anthropic Messages 的
结构：系统提示词放入顶层的 `system` 字段，其余消息保留各自的 `user`/`assistant`
角色。API 密钥仅通过 `x-api-key` 请求头发送，并附带
`anthropic-version: 2023-06-01`。

请求最多重试三次，采用指数退避（上限 5 秒）。错误在暴露前会被净化：任何包含 URL
的文本都会被替换为 `transport error`，因此可能携带凭据的请求地址绝不会写入持久化的
`ProcessorNote`。核心路由器还会从汇总的失败信息中抹去所有已配置的 API 密钥。

### 配置项

标准的 `[[llms]]` 字段均适用（`model`、`api_key`、`api_key_env`、`headers`、
`timeout_seconds`、`max_retries`、`fallback`）。后端专属项写在 `[llms.options]`：

| 配置项 | 默认值 | 说明 |
| ------ | ------ | ---- |
| `base_url` | `https://api.anthropic.com/v1/messages` | 完整的 messages 端点（不是前缀）。 |
| `max_tokens` | `1024` | Anthropic 要求显式指定输出上限。 |

### 用法

```toml
[[llms]]
llm_id = "claude"
provider = "anthropic"
model = "claude-3-5-sonnet-latest"
api_key_env = "ANTHROPIC_API_KEY"    # 或 api_key = "${ANTHROPIC_API_KEY}"
timeout_seconds = 60

[llms.options]
max_tokens = 2048
```

在 TUI 的**大模型**标签页中，列表顺序即回退链：把 Claude 放在第一位即设为默认，
放在其他条目之后则只作为后备使用。

### 说明

- `api_key_env` 在每次启动时解析，且绝不会被写回配置文件，因此轮换密钥只需修改
  环境变量。
- 如果长邮件返回的 JSON 被截断，请调高 `max_tokens`；内置分析提示词要求返回一个
  完整的 JSON 对象。

### 依赖

`httpx`，以及 `mailflow-core`。

### 协议

MIT —— 欢迎贡献。

---

Metadata: [`plugin.json`](plugin.json) · Marketplace: [https://github.com/Kingcxp/mailflow-repo/tree/main/llm_backend/mailflow-llm-anthropic](https://github.com/Kingcxp/mailflow-repo/tree/main/llm_backend/mailflow-llm-anthropic)
