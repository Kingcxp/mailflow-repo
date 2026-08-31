<!-- Generated from plugin.json by tools/gen_plugin_readmes.py. Edit plugin.json. -->

## Zhipu LLM Backend

Thin preset over the OpenAI-compatible Chat Completions transport that points
MailFlow at Zhipu AI's GLM models (BigModel). Registers the LLM backend
component id `zhipu`.

### Endpoint

    POST https://open.bigmodel.cn/api/paas/v4/chat/completions
    Authorization: Bearer <api key>

Defaults: `base_url` `https://open.bigmodel.cn/api/paas/v4`, `model`
`glm-4-flash`. Both are used only when the `[[llms]]` entry does not set them;
an explicit `model` or `base_url` always wins.

### Authentication

Set `api_key` directly or reference an environment variable with
`api_key_env` (e.g. `ZHIPUAI_API_KEY`). MailFlow expands `${VAR}`
placeholders when loading configuration.

### Options

Standard `[[llms]]` fields apply (`model`, `api_key`, `api_key_env`,
`base_url`, `headers`, `extra_body`, `timeout_seconds`, `max_retries`,
`fallback`). Backend-specific entries live in `[llms.options]`:

| Option | Default | Meaning |
| ------ | ------- | ------- |
| `path` | `chat/completions` | Path appended to `base_url`; override for proxy gateways. |
| `headers` | `{}` | Per-call extra headers, merged over the configured ones. |
| `query` | `{}` | Per-call query parameters. |
| `body` | `{}` | Per-call request-body overrides, merged last. |
| `model` / `temperature` | from config | Per-call overrides of the model name / sampling temperature. |

### Usage

```toml
[[llms]]
llm_id = "zhipu"
provider = "zhipu"
api_key_env = "ZHIPUAI_API_KEY"
```

The request runs on a worker thread via the standard library (urllib) — no
third-party runtime dependency beyond `mailflow-core`. Only transient
failures (timeouts, transport errors, HTTP 408/429/5xx) are retried, with
exponential backoff capped at 5 s; error text is sanitized so no URL or key
material leaks.

### License

MIT — contributions welcome.

---

<!-- zh-CN -->

## 智谱大模型后端

基于 OpenAI 兼容的 Chat Completions 传输层的轻量预设，让 MailFlow 直接对接
智谱 AI 的 GLM 模型（BigModel）。注册的大模型后端组件 id 为 `zhipu`。

### 端点

    POST https://open.bigmodel.cn/api/paas/v4/chat/completions
    Authorization: Bearer <api key>

默认值：`base_url` 为 `https://open.bigmodel.cn/api/paas/v4`，`model` 为
`glm-4-flash`。仅当 `[[llms]]` 条目未设置时才使用默认值；显式配置的
`model` 或 `base_url` 始终优先。

### 鉴权

直接设置 `api_key`，或用 `api_key_env` 引用环境变量（例如
`ZHIPUAI_API_KEY`）。MailFlow 在加载配置时会展开 `${VAR}` 占位符。

### 配置项

标准的 `[[llms]]` 字段均适用（`model`、`api_key`、`api_key_env`、
`base_url`、`headers`、`extra_body`、`timeout_seconds`、`max_retries`、
`fallback`）。后端专属项写在 `[llms.options]`：

| 配置项 | 默认值 | 说明 |
| ------ | ------ | ---- |
| `path` | `chat/completions` | 追加到 `base_url` 的路径；代理网关时可覆盖。 |
| `headers` | `{}` | 单次调用的额外请求头，合并覆盖已配置项。 |
| `query` | `{}` | 单次调用的查询参数。 |
| `body` | `{}` | 单次调用的请求体覆盖，最后合并。 |
| `model` / `temperature` | 取自配置 | 单次调用覆盖模型名 / 采样温度。 |

### 用法

```toml
[[llms]]
llm_id = "zhipu"
provider = "zhipu"
api_key_env = "ZHIPUAI_API_KEY"
```

请求在工作线程中通过标准库（urllib）执行——除 `mailflow-core` 外无任何
第三方运行时依赖。仅重试瞬时故障（超时、传输错误、HTTP 408/429/5xx），
指数退避上限 5 秒；错误文本经过净化，绝不泄漏 URL 或密钥。

### 协议

MIT —— 欢迎贡献。

---

Metadata: [`plugin.json`](plugin.json) · Marketplace: [https://github.com/Kingcxp/mailflow-repo/tree/main/llm_backend/mailflow-llm-zhipu](https://github.com/Kingcxp/mailflow-repo/tree/main/llm_backend/mailflow-llm-zhipu)
