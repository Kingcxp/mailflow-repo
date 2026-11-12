<!-- Generated from plugin.json by tools/gen_plugin_readmes.py. Edit plugin.json. -->

# Google Vertex AI backend

Component ID: `google-vertex`. Sends shared chat/tool requests to Vertex
`generateContent`. A project and a valid access credential are required.

```toml
[[llms]]
llm_id = "primary"
provider = "google-vertex"
model = "your-model-id"
api_key_env = "VERTEX_ACCESS_TOKEN"

[llms.options]
project = "your-project-id"
location = "us-central1"
```

`options.project` is required; location defaults to `us-central1`. `base_url`
defaults to `https://aiplatform.googleapis.com`. Authentication uses a short-lived
OAuth access token in `api_key`/`api_key_env`, or
`options.service_account_file` with `google-auth` installed in the host.
An ordinary API key is not an OAuth token. Keep service-account files private.

Optional `max_tokens`, `temperature` and `thinking_budget` generation defaults,
shared headers/query/extra body, timeout and retry are supported. Select a model
and location available to your project; the transport does not grant project
access. Failed credentials or unsupported capabilities are reported normally.

---

<!-- zh-CN -->

# Google Vertex AI 后端

组件标识为 `google-vertex`，通过 Vertex `generateContent` 处理共享对话和工具请求。
需要项目和有效访问凭据。

```toml
[[llms]]
llm_id = "primary"
provider = "google-vertex"
model = "your-model-id"
api_key_env = "VERTEX_ACCESS_TOKEN"

[llms.options]
project = "your-project-id"
location = "us-central1"
```

`options.project` 必填，地区默认 `us-central1`，默认根地址为
`https://aiplatform.googleapis.com`。`api_key`／`api_key_env` 填短期 OAuth 访问令牌，
或配置 `options.service_account_file` 并在宿主安装 `google-auth`。
普通 API 密钥不等同于访问令牌，服务账号文件需要保密。

可设置生成长度、温度、思考预算，以及共享请求头、查询、额外请求体、超时和重试。
模型和地区必须在项目中可用，插件不提供额外访问权限；凭据或能力错误会明确报告。

---

[Catalog](../../README.md) · [Metadata](plugin.json) · [Plugin page](https://github.com/Kingcxp/mailflow-repo/tree/main/llm_backend/mailflow-llm-google-vertex)
