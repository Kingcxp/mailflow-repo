<!-- Generated from plugin.json by tools/gen_plugin_readmes.py. Edit plugin.json. -->

# OpenAI-compatible model backends

Provides Chat Completions and Responses transports, including configured proxy
and Azure endpoints. Component IDs: `openai-completions`, `openai-responses`,
`openai-codex-responses`, `azure-openai-responses`; `openai-compatible` is the
compatible Chat Completions alias.

```toml
[[llms]]
llm_id = "primary"
provider = "openai-compatible"
base_url = "https://your-provider.example/v1"
model = "your-model-id"
api_key_env = "MAILFLOW_MODEL_KEY"
timeout_seconds = 60
max_retries = 2
```

Choose the transport supported by your endpoint. `openai-codex-responses` selects
a Responses request format, not account login or a subscription credential flow.
Azure uses the deployment name as `model` and the resource address as `base_url`.
Its `options.api_version` defaults to the transport's `preview` value; set a value
accepted by your endpoint.

| Configuration | Purpose |
| --- | --- |
| `api_key` / `api_key_env` | Literal/environment credential; environment references are preferred |
| `headers`, `query`, `extra_body` | Additional configured headers, URL parameters and JSON body fields |
| `timeout_seconds`, `max_retries` | Request timeout and retry policy |
| `options.path` | Override the transport-specific `chat/completions` or `responses` path |
| `options.max_tokens`, `options.temperature`, `options.stream` | Optional request defaults where supported by the chosen transport/model |

The shared chat contract accepts temperature, per-call options and tools, and
returns text plus structured tool calls. The actual model/endpoint must support
the requested capability. Use model IDs available to your account, not a fixed
example alias. Valid explicit processor llm/fallback_llms bindings take priority. Otherwise the marked default (or first entry) is primary, and unspecified fallbacks use the remaining list. Test a
connection before requesting analysis; authentication or unsupported parameters
are reported as failures, not empty successful completions.

---

<!-- zh-CN -->

# OpenAI 兼容模型后端

提供 Chat Completions 和 Responses 传输，支持配置的代理与 Azure 地址。
组件标识包括 `openai-completions`、`openai-responses`、`openai-codex-responses`、
`azure-openai-responses`；旧标识 `openai-compatible` 对应 Chat Completions。

```toml
[[llms]]
llm_id = "primary"
provider = "openai-compatible"
base_url = "https://your-provider.example/v1"
model = "your-model-id"
api_key_env = "MAILFLOW_MODEL_KEY"
timeout_seconds = 60
max_retries = 2
```

按实际端点选择协议。`openai-codex-responses` 选择请求格式，不提供账号登录或订阅凭据流程。
Azure 的 `model` 填部署名，`base_url` 填资源地址，`options.api_version` 需为服务接受的版本。

额外请求头、查询参数和请求体分别使用 `headers`、`query`、`extra_body`；
`options.path` 覆盖请求路径，`max_tokens`、`temperature`、`stream` 提供受支持的请求默认值。
超时和重试由 `timeout_seconds`、`max_retries` 控制，密钥优先用环境变量。

后端传递工具、温度和单次调用选项，并返回结构化工具调用；真实模型也必须支持相应能力。
模型名填写账户实际可用值。处理器有效的 llm/fallback_llms 绑定优先；未指定时取默认模型或首项，后备由剩余列表补齐。先测试连接，认证和参数错误不会当成成功。

---

[Catalog](../../README.md) · [Metadata](plugin.json) · [Plugin page](https://github.com/Kingcxp/mailflow-repo/tree/main/llm_backend/mailflow-llm-openai-compatible)
