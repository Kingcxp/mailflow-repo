<!-- Generated from plugin.json by tools/gen_plugin_readmes.py. Edit plugin.json. -->

## OpenClaw WeChat (ClawBot) Notifier

Sends MailFlow alerts through an [OpenClaw](https://openclaw.ai) gateway
with Tencent's official `@tencent-weixin/openclaw-weixin` channel plugin
(iLink protocol).

### Options

| Option | Required | Description |
|---|---|---|
| `base_url` | yes | OpenClaw gateway root URL |
| `endpoint` | no | Send endpoint path, default `/v1/messages` |
| `api_key` | yes | Gateway API key (`api_key_env` also accepted) |
| `targets` | yes | List of WeChat user ids |

### Notes

- Experimental: the upstream iLink API is still evolving; adjust
  `endpoint` when your gateway version differs.

---

<!-- zh-CN -->

## OpenClaw 微信（ClawBot）通知器

通过 [OpenClaw](https://openclaw.ai) 网关与腾讯官方的 `@tencent-weixin/openclaw-weixin` 渠道插件（iLink 协议）发送 MailFlow 提醒。

### 配置项

| 选项 | 必填 | 说明 |
|---|---|---|
| `base_url` | 是 | OpenClaw 网关根地址 |
| `endpoint` | 否 | 发送接口路径，默认 `/v1/messages` |
| `api_key` | 是 | 网关 API 密钥（也接受 `api_key_env` 环境变量） |
| `targets` | 是 | 微信用户 id 列表 |

### 说明

- 实验性：上游 iLink API 仍在演进；网关版本不同时可调整 `endpoint`。

---

Metadata: [`plugin.json`](plugin.json) · Marketplace: [https://github.com/Kingcxp/mailflow-repo/tree/main/notifier/mailflow-notify-openclaw-weixin](https://github.com/Kingcxp/mailflow-repo/tree/main/notifier/mailflow-notify-openclaw-weixin)
