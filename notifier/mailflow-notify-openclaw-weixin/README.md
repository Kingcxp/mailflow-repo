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

Metadata: [`plugin.json`](plugin.json) · Marketplace: [https://github.com/Kingcxp/mailflow-repo/tree/main/notifier/mailflow-notify-openclaw-weixin](https://github.com/Kingcxp/mailflow-repo/tree/main/notifier/mailflow-notify-openclaw-weixin)
