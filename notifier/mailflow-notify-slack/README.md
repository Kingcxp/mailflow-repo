<!-- Generated from plugin.json by tools/gen_plugin_readmes.py. Edit plugin.json. -->

# Slack notifier

Component ID: `slack`. Delivers mail summaries through the configured
Slack endpoint. This package implements mail notification, not incoming chat
commands, arbitrary-text reminders, images or file exchange.

```toml
[[notifiers]]
notifier_id = "slack-alerts"
provider = "slack"
enabled = true
minimum_urgency = "important"

[notifiers.options]
webhook_url = "${SLACK_WEBHOOK}"
timeout_seconds = 10
```

`webhook_url` is required. The destination channel is selected when creating the Slack webhook; it cannot be overridden here. Existing `channel` options are ignored. See [Slack's webhook rules](https://docs.slack.dev/messaging/sending-messages-using-incoming-webhooks/).
`timeout_seconds` defaults to 10 seconds. Environment placeholders are resolved
by Waymark Mail; keep endpoint tokens private.

Missing required configuration, HTTP errors and recognized platform rejection
fail delivery. The runtime records the failure without losing the stored mail;
fix the endpoint/access settings and retry the failed notification. A successful
HTTP response is not enough if the platform reports a business error.

---

<!-- zh-CN -->

# Slack 通知器

组件标识为 `slack`，通过配置的 Slack 地址发送邮件摘要。
本插件提供邮件推送，不提供接收聊天命令、任意文字提醒、图片或文件收发。

```toml
[[notifiers]]
notifier_id = "slack-alerts"
provider = "slack"
enabled = true
minimum_urgency = "important"

[notifiers.options]
webhook_url = "${SLACK_WEBHOOK}"
timeout_seconds = 10
```

`webhook_url` 必填；频道在创建 Slack webhook 时确定，不能在此覆盖；旧配置中的 `channel` 会忽略。[官方说明](https://docs.slack.dev/messaging/sending-messages-using-incoming-webhooks/)。
`timeout_seconds` 默认 10 秒。环境变量由 Waymark Mail 展开，地址中的令牌需要保密。

缺少必要配置、HTTP 错误或可识别的平台拒绝均视为投递失败。
运行时保留已存邮件并记录失败，修正地址和访问设置后重试对应通知。
不能只因 HTTP 成功就把平台业务失败当成发送成功。

---

[Catalog](../../README.md) · [Metadata](plugin.json) · [Plugin page](https://github.com/Kingcxp/waymark-mail-repo/tree/main/notifier/mailflow-notify-slack)
