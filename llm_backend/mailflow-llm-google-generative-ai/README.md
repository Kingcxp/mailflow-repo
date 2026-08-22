<!-- Generated from plugin.json by tools/gen_plugin_readmes.py. Edit plugin.json. -->

## Google Generative AI Backend

The public Gemini API backend: talks to
`https://generativelanguage.googleapis.com` out of the box, and to any
self-hosted proxy through `base_url`.

Registers the LLM backend component id `google-generative-ai`.

### How it works

MailFlow's processors speak one chat format; this backend translates it to
Gemini's shape: system prompts travel in `systemInstruction`, assistant turns
become `model` role turns, and everything posts to

```
POST {base_url}/v1beta/models/{model}:generateContent
x-goog-api-key: <api key>
```

Only transient failures — timeouts, transport errors, HTTP 408/429/5xx — are
retried up to three times with exponential backoff capped at 5 s. Error text
is sanitized before it surfaces (no URLs, no key material); the core router
additionally redacts the configured key from aggregated failures.

### Authentication

Set the key through the standard fields: `api_key` inline or, preferably,
`api_key_env = "GEMINI_API_KEY"`. The value is sent only as the
`x-goog-api-key` header and is never written back into the config file.
(Vertex AI users need `mailflow-llm-google-vertex` instead.)

### Options

Standard `[[llms]]` fields apply (`model`, `api_key`, `api_key_env`,
`base_url`, `headers`, `timeout_seconds`, `max_retries`, `fallback`).

| Option | Default | Meaning |
| ------ | ------- | ------- |
| `base_url` | `https://generativelanguage.googleapis.com` | Override for a self-hosted proxy. |
| `extra_body.generationConfig` | — | Merged into the request's `generationConfig` (e.g. temperature presets). |
| `extra_body.*` | — | Any other keys go straight into the request body. |

### Usage

```toml
[[llms]]
llm_id = "gemini"
provider = "google-generative-ai"
model = "gemini-2.0-flash"
api_key_env = "GEMINI_API_KEY"
timeout_seconds = 60
```

In the TUI's **LLMs** tab the list order is the fallback chain: put Gemini
first to make it the default, or below another entry to use it only as a
fallback.

### Requirements

`httpx`, plus `mailflow-core`.

### License

MIT — contributions welcome.

---

<!-- zh-CN -->

## Google Generative AI 后端

公开的 Gemini API 后端：默认直连
`https://generativelanguage.googleapis.com`，也可通过 `base_url` 指向
自建代理。

注册的大模型后端组件 id 为 `google-generative-ai`。

### 工作方式

MailFlow 的处理器只使用一种对话格式，本后端负责把它翻译成 Gemini 的结构：
系统提示词放入 `systemInstruction`，assistant 回合转为 `model` 角色，请求
发往：

```
POST {base_url}/v1beta/models/{model}:generateContent
x-goog-api-key: <api key>
```

只有瞬时故障 —— 超时、传输错误、HTTP 408/429/5xx —— 会重试，最多三次，
指数退避上限 5 秒。错误文本在暴露前会被净化（不含 URL、不含密钥材料），
核心路由器还会从汇总的失败信息中抹去已配置的密钥。

### 认证方式

通过标准字段提供密钥：内联 `api_key`，或更推荐的
`api_key_env = "GEMINI_API_KEY"`。该值只通过 `x-goog-api-key` 请求头发送，
绝不会被写回配置文件。（Vertex AI 用户请改用 `mailflow-llm-google-vertex`。）

### 配置项

标准的 `[[llms]]` 字段均适用（`model`、`api_key`、`api_key_env`、`base_url`、
`headers`、`timeout_seconds`、`max_retries`、`fallback`）。

| 配置项 | 默认值 | 说明 |
| ------ | ------ | ---- |
| `base_url` | `https://generativelanguage.googleapis.com` | 自建代理时覆盖。 |
| `extra_body.generationConfig` | — | 合并进请求的 `generationConfig`（如预设温度等生成参数）。 |
| `extra_body.*` | — | 其余键直接进入请求体。 |

### 用法

```toml
[[llms]]
llm_id = "gemini"
provider = "google-generative-ai"
model = "gemini-2.0-flash"
api_key_env = "GEMINI_API_KEY"
timeout_seconds = 60
```

在 TUI 的**大模型**标签页中，列表顺序即回退链：把 Gemini 放在第一位即设为
默认，放在其他条目之后则只作为后备使用。

### 依赖

`httpx`，以及 `mailflow-core`。

### 协议

MIT —— 欢迎贡献。

---

Metadata: [`plugin.json`](plugin.json) · Marketplace: [https://github.com/Kingcxp/mailflow-repo/tree/main/llm_backend/mailflow-llm-google-generative-ai](https://github.com/Kingcxp/mailflow-repo/tree/main/llm_backend/mailflow-llm-google-generative-ai)
