<!-- Generated from plugin.json by tools/gen_plugin_readmes.py. Edit plugin.json. -->

# ServerChan notifier

Component ID: `serverchan`. Delivers mail summaries through the configured
ServerChan endpoint. This package implements mail notification, not incoming chat
commands, arbitrary-text reminders, images or file exchange.

```toml
[[notifiers]]
notifier_id = "serverchan-alerts"
provider = "serverchan"
enabled = true
minimum_urgency = "important"

[notifiers.options]
send_key = "${SERVERCHAN_SEND_KEY}"
timeout_seconds = 10
```

`send_key` is required and forms the `.send` endpoint. Optional `title` overrides the notification title.
`timeout_seconds` defaults to 10 seconds. Environment placeholders are resolved
by Waymark Mail; keep endpoint tokens private.

Missing required configuration, HTTP errors and recognized platform rejection
fail delivery. The runtime records the failure without losing the stored mail;
fix the endpoint/access settings and retry the failed notification. A successful
HTTP response is not enough if the platform reports a business error.

---

<!-- zh-CN -->

# Server酱 通知器

组件标识为 `serverchan`，通过配置的 Server酱 地址发送邮件摘要。
本插件提供邮件推送，不提供接收聊天命令、任意文字提醒、图片或文件收发。

```toml
[[notifiers]]
notifier_id = "serverchan-alerts"
provider = "serverchan"
enabled = true
minimum_urgency = "important"

[notifiers.options]
send_key = "${SERVERCHAN_SEND_KEY}"
timeout_seconds = 10
```

`send_key` 必填，用于构造 `.send` 地址；可选 `title` 覆盖通知标题。
`timeout_seconds` 默认 10 秒。环境变量由 Waymark Mail 展开，地址中的令牌需要保密。

缺少必要配置、HTTP 错误或可识别的平台拒绝均视为投递失败。
运行时保留已存邮件并记录失败，修正地址和访问设置后重试对应通知。
不能只因 HTTP 成功就把平台业务失败当成发送成功。

---

[Catalog](../../README.md) · [Metadata](plugin.json) · [Plugin page](https://github.com/Kingcxp/waymark-mail-plugins/tree/main/notifier/mailflow-notify-serverchan)
