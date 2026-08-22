<!-- Generated from plugin.json by tools/gen_plugin_readmes.py. Edit plugin.json. -->

## OpenAI-family LLM Backends

One plugin exposing five fine-grained component ids, so a named LLM can target
the exact API shape instead of relying on `options.path` overrides:

- `openai-completions` — POST `{base}/chat/completions`
- `openai-responses` — POST `{base}/responses` (stateless)
- `openai-codex-responses` — responses shape with Codex defaults
  (`store=false`, instructions-first system prompt)
- `azure-openai-responses` — Azure deployment URL + `api-key` authentication
- `openai-compatible` — legacy alias for `openai-completions`, kept for old configs

### How it works

MailFlow's processors speak one chat format; these backends translate it to
the Chat Completions or Responses shape. The system prompt travels either as
a top-level system message (completions) or as `instructions` (responses).
Azure requests go to `{base}/openai/deployments/{model}/responses` with an
`api-version` query parameter.

Transient failures only — timeouts, transport errors, HTTP 408/429/5xx — are
retried up to three times with exponential backoff capped at 5 s. Error text
is sanitized before it surfaces: URLs never appear (query strings may carry
credentials), and the core router additionally redacts every configured API
key from aggregated failures.

### Options

Standard `[[llms]]` fields apply (`model`, `api_key`, `api_key_env`,
`base_url`, `headers`, `extra_body`, `timeout_seconds`, `max_retries`,
`fallback`). Backend-specific entries live in `[llms.options]`:

| Option | Default | Meaning |
| ------ | ------- | ------- |
| `path` | endpoint-specific (`chat/completions` / `responses`) | Path appended to `base_url`; override for non-standard gateways. |
| `api_version` | `"preview"` | Azure only: value of the `api-version` query parameter. |
| `headers` | `{}` | Per-call extra headers, merged over the configured ones. |
| `query` | `{}` | Per-call query parameters. |
| `body` | `{}` | Per-call request-body overrides, merged last. |
| `model` / `temperature` | from config | Per-call overrides of the model name / sampling temperature. |

Any `extra_body` map on the `[[llms]]` entry is merged into the request body.

### Usage

```toml
[[llms]]
llm_id = "gpt"
provider = "openai-responses"
model = "gpt-4.1-mini"
api_key_env = "OPENAI_API_KEY"
timeout_seconds = 60

[[llms]]
llm_id = "az-gpt"
provider = "azure-openai-responses"
model = "gpt-4.1-mini"                       # deployment name
base_url = "https://my-resource.openai.azure.com"
api_key_env = "AZURE_OPENAI_API_KEY"

[llms.options]
api_version = "preview"
```

In the TUI's **LLMs** tab the list order is the fallback chain: put the
primary entry first and others below it as fallbacks.

### Requirements

`httpx`, plus `mailflow-core`.

### License

MIT — contributions welcome.

---

<!-- zh-CN -->

## OpenAI 家族大模型后端

一个插件暴露五个细粒度的组件 id，让具名大模型可以直接指定确切的 API 形态，
而不必依赖 `options.path` 覆盖：

- `openai-completions` —— POST `{base}/chat/completions`
- `openai-responses` —— POST `{base}/responses`(无状态)
- `openai-codex-responses` —— responses 形态加 Codex 默认值（`store=false`、
  系统提示词前置为 instructions）
- `azure-openai-responses` —— Azure 部署 URL + `api-key` 鉴权
- `openai-compatible` —— `openai-completions` 的历史别名，兼容旧配置

### 工作方式

MailFlow 的处理器只使用一种对话格式，这些后端负责把它翻译成 Chat Completions
或 Responses 的结构。系统提示词要么作为顶层 system 消息（completions），
要么作为 `instructions`（responses）。Azure 请求发往
`{base}/openai/deployments/{model}/responses`，并携带 `api-version` 查询参数。

只有瞬时故障 —— 超时、传输错误、HTTP 408/429/5xx —— 会重试，最多三次，
指数退避上限 5 秒。错误文本在暴露前会被净化：绝不会出现 URL（查询串可能
携带凭据），核心路由器还会从汇总的失败信息中抹去所有已配置的 API 密钥。

### 配置项

标准的 `[[llms]]` 字段均适用（`model`、`api_key`、`api_key_env`、`base_url`、
`headers`、`extra_body`、`timeout_seconds`、`max_retries`、`fallback`）。
后端专属项写在 `[llms.options]`：

| 配置项 | 默认值 | 说明 |
| ------ | ------ | ---- |
| `path` | 因端点而异（`chat/completions` / `responses`) | 追加到 `base_url` 的路径；非标准网关时可覆盖。 |
| `api_version` | `"preview"` | 仅 Azure:`api-version` 查询参数的取值。 |
| `headers` | `{}` | 单次调用的额外请求头，合并覆盖已配置项。 |
| `query` | `{}` | 单次调用的查询参数。 |
| `body` | `{}` | 单次调用的请求体覆盖，最后合并。 |
| `model` / `temperature` | 取自配置 | 单次调用覆盖模型名 / 采样温度。 |

`[[llms]]` 条目上的任意 `extra_body` 映射都会合并进请求体。

### 用法

```toml
[[llms]]
llm_id = "gpt"
provider = "openai-responses"
model = "gpt-4.1-mini"
api_key_env = "OPENAI_API_KEY"
timeout_seconds = 60

[[llms]]
llm_id = "az-gpt"
provider = "azure-openai-responses"
model = "gpt-4.1-mini"                       # 部署名
base_url = "https://my-resource.openai.azure.com"
api_key_env = "AZURE_OPENAI_API_KEY"

[llms.options]
api_version = "preview"
```

在 TUI 的**大模型**标签页中，列表顺序即回退链：主条目放第一位，其余放在
下面作为后备。

### 依赖

`httpx`，以及 `mailflow-core`。

### 协议

MIT —— 欢迎贡献。

---

Metadata: [`plugin.json`](plugin.json) · Marketplace: [https://github.com/Kingcxp/mailflow-repo/tree/main/llm_backend/mailflow-llm-openai-compatible](https://github.com/Kingcxp/mailflow-repo/tree/main/llm_backend/mailflow-llm-openai-compatible)
