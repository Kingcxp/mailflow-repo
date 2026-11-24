<!-- Generated from plugin.json by tools/gen_plugin_readmes.py. Edit plugin.json. -->

# Moonshot model preset

Component ID: `moonshot`. Reuses the OpenAI-compatible Chat Completions
transport; its dependency is installed with this package.

```toml
[[llms]]
llm_id = "primary"
provider = "moonshot"
model = "your-model-id"
api_key_env = "MOONSHOT_API_KEY"
```

The implementation defaults to `https://api.moonshot.cn/v1` and
model `moonshot-v1-8k` when those fields are omitted. These are code
defaults, not a guarantee that the provider still offers that model. Set your
available model explicitly; an explicit `base_url` also overrides the preset.

See [shared transport options](../mailflow-llm-openai-compatible/README.md) for
credentials, timeout/retries, request overrides and tool calls. The model and
endpoint must support the requested tools. Primary/fallback selection uses
the shared model defaults and processor bindings described in that guide.

---

<!-- zh-CN -->

# Moonshot 模型预设

组件标识为 `moonshot`，复用 OpenAI 兼容的 Chat Completions 传输，安装时处理所需依赖。

```toml
[[llms]]
llm_id = "primary"
provider = "moonshot"
model = "your-model-id"
api_key_env = "MOONSHOT_API_KEY"
```

代码默认地址为 `https://api.moonshot.cn/v1`，默认模型为
`moonshot-v1-8k`；这仅说明实现默认值，不保证服务仍提供该模型。
请明确填写实际可用模型，显式 `base_url` 可覆盖地址。

凭据、超时、重试、请求覆盖和工具调用见[共享后端说明](../mailflow-llm-openai-compatible/README.md)。
真实模型和端点也必须支持相应工具能力，主模型与后备遵守共享模型默认值和处理器绑定。

---

[Catalog](../../README.md) · [Metadata](plugin.json) · [Plugin page](https://github.com/Kingcxp/waymark-mail-repo/tree/main/llm_backend/mailflow-llm-moonshot)
