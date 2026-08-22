<!-- Generated from plugin.json by tools/gen_plugin_readmes.py. Edit plugin.json. -->

## Google Vertex AI Backend

Gemini models on Vertex AI: posts to your project's endpoint

```
POST {base}/v1/projects/{project}/locations/{location}/publishers/google/models/{model}:generateContent
Authorization: Bearer <token>
```

with bounded retries and sanitized errors, like the rest of the Google family.

Registers the LLM backend component id `google-vertex`.

### How it works

MailFlow's processors speak one chat format; this backend translates it to
Gemini's Vertex shape: system prompts travel in `systemInstruction`,
assistant turns become `model` role turns, and generation parameters merge
into `generationConfig`. Only transient failures — timeouts, transport
errors, HTTP 408/429/5xx — are retried up to three times with exponential
backoff capped at 5 s; headers are rebuilt per attempt so a refreshed token
is picked up mid-retry. Error text never contains URLs or token material.

### Authentication

Two supported ways, tried in this order:

1. **Service account** — set `options.service_account_file` to your key file
   and make it discoverable to Application Default Credentials (e.g.
   `GOOGLE_APPLICATION_CREDENTIALS=/path/to/key.json`). The OAuth2 token is
   minted through `google-auth`, cached, and refreshed ahead of expiry.
   Requires the optional dependency: `uv pip install google-auth`.
2. **Access token** — put a short-lived access token with the
   `cloud-platform` scope into `api_key` / `api_key_env`; it is sent as-is in
   the `Authorization: Bearer` header.

Without either credential the backend refuses to start.

### Options

Standard `[[llms]]` fields apply (`model`, `api_key`, `api_key_env`,
`base_url`, `headers`, `timeout_seconds`, `max_retries`, `fallback`):

| Option | Required | Default | Meaning |
| ------ | -------- | ------- | ------- |
| `project` | **yes** | `""` | GCP project id; missing → error at construction time. |
| `location` | no | `us-central1` | Region for the endpoint. |
| `service_account_file` | no | `""` | Service-account credential path; enables token minting (see Authentication). |
| `base_url` | no | `https://aiplatform.googleapis.com` | Override for private endpoints / proxies. |

### Usage

```toml
[[llms]]
llm_id = "vertex"
provider = "google-vertex"
model = "gemini-2.0-flash"
timeout_seconds = 60

[llms.options]
project = "my-gcp-project"
location = "us-central1"
# service_account_file = "/path/to/key.json"
# ...or skip it and set api_key_env = "VERTEX_ACCESS_TOKEN" above
```

### Requirements

`httpx` and `mailflow-core`; `google-auth` is optional and needed only for
service-account token minting.

### License

MIT — contributions welcome.

---

<!-- zh-CN -->

## Google Vertex AI 后端

Vertex AI 上的 Gemini 模型：请求发往项目端点

```
POST {base}/v1/projects/{project}/locations/{location}/publishers/google/models/{model}:generateContent
Authorization: Bearer <token>
```

与 Google 家族其他成员一样，具备有界重试与净化后的错误信息。

注册的大模型后端组件 id 为 `google-vertex`。

### 工作方式

MailFlow 的处理器只使用一种对话格式，本后端负责把它翻译成 Gemini 在 Vertex
上的结构：系统提示词放入 `systemInstruction`，assistant 回合转为 `model`
角色，生成参数合并进 `generationConfig`。只有瞬时故障 —— 超时、传输错误、
HTTP 408/429/5xx —— 会重试，最多三次，指数退避上限 5 秒；每次尝试都会重建
请求头，因此重试途中刷新的令牌能立即生效。错误文本绝不包含 URL 或令牌
材料。

### 认证方式

支持两种方式，按以下顺序尝试：

1. **服务账号** —— 把 `options.service_account_file` 设为密钥文件路径，并让
   应用默认凭据能够发现它(例如
   `GOOGLE_APPLICATION_CREDENTIALS=/path/to/key.json`)。OAuth2 令牌通过
   `google-auth` 签发、缓存，并在过期前自动刷新。需要可选依赖：
   `uv pip install google-auth`。
2. **访问令牌** —— 把带有 `cloud-platform` 权限范围的短期访问令牌放进
   `api_key` / `api_key_env`，它会原样作为 `Authorization: Bearer` 头发送。

两者都未配置时，后端会在启动时直接报错。

### 配置项

标准的 `[[llms]]` 字段均适用（`model`、`api_key`、`api_key_env`、`base_url`、
`headers`、`timeout_seconds`、`max_retries`、`fallback`）：

| 配置项 | 必填 | 默认值 | 说明 |
| ------ | ---- | ------ | ---- |
| `project` | **是** | `""` | GCP 项目 id；缺失时构造即报错。 |
| `location` | 否 | `us-central1` | 端点所在区域。 |
| `service_account_file` | 否 | `""` | 服务账号凭据路径；启用令牌签发（见认证方式）。 |
| `base_url` | 否 | `https://aiplatform.googleapis.com` | 私有端点 / 代理时覆盖。 |

### 用法

```toml
[[llms]]
llm_id = "vertex"
provider = "google-vertex"
model = "gemini-2.0-flash"
timeout_seconds = 60

[llms.options]
project = "my-gcp-project"
location = "us-central1"
# service_account_file = "/path/to/key.json"
# 或者不配置它，改为在上面的 api_key_env = "VERTEX_ACCESS_TOKEN" 提供访问令牌
```

### 依赖

`httpx` 与 `mailflow-core`；`google-auth` 为可选，仅服务账号令牌签发时需要。

### 协议

MIT —— 欢迎贡献。

---

Metadata: [`plugin.json`](plugin.json) · Marketplace: [https://github.com/Kingcxp/mailflow-repo/tree/main/llm_backend/mailflow-llm-google-vertex](https://github.com/Kingcxp/mailflow-repo/tree/main/llm_backend/mailflow-llm-google-vertex)
