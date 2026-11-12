<!-- Generated from plugin.json by tools/gen_plugin_readmes.py. Edit plugin.json. -->

# Discord notifier

Component ID: `discord`. Delivers mail summaries through the configured
Discord endpoint. This package implements mail notification, not incoming chat
commands, arbitrary-text reminders, images or file exchange.

```toml
[[notifiers]]
notifier_id = "discord-alerts"
provider = "discord"
enabled = true
minimum_urgency = "important"

[notifiers.options]
webhook_url = "${DISCORD_WEBHOOK}"
timeout_seconds = 10
```

`webhook_url` is required; optional `username` overrides the displayed webhook sender.
`timeout_seconds` defaults to 10 seconds. Environment placeholders are resolved
by MailFlow; keep endpoint tokens private.

Missing required configuration, HTTP errors and recognized platform rejection
fail delivery. The runtime records the failure without losing the stored mail;
fix the endpoint/access settings and retry the failed notification. A successful
HTTP response is not enough if the platform reports a business error.

---

<!-- zh-CN -->

# Discord 通知器

组件标识为 `discord`，通过配置的 Discord 地址发送邮件摘要。
本插件提供邮件推送，不提供接收聊天命令、任意文字提醒、图片或文件收发。

```toml
[[notifiers]]
notifier_id = "discord-alerts"
provider = "discord"
enabled = true
minimum_urgency = "important"

[notifiers.options]
webhook_url = "${DISCORD_WEBHOOK}"
timeout_seconds = 10
```

`webhook_url` 必填，可选 `username` 覆盖显示的发送者名称。
`timeout_seconds` 默认 10 秒。环境变量由 MailFlow 展开，地址中的令牌需要保密。

缺少必要配置、HTTP 错误或可识别的平台拒绝均视为投递失败。
运行时保留已存邮件并记录失败，修正地址和访问设置后重试对应通知。
不能只因 HTTP 成功就把平台业务失败当成发送成功。

---

[Catalog](../../README.md) · [Metadata](plugin.json) · [Plugin page](https://github.com/Kingcxp/mailflow-repo/tree/main/notifier/mailflow-notify-discord)
