<!-- Generated from plugin.json by tools/gen_plugin_readmes.py. Edit plugin.json. -->

# ntfy notifier

Component ID: `ntfy`. Delivers mail summaries through the configured
ntfy endpoint. This package implements mail notification, not incoming chat
commands, arbitrary-text reminders, images or file exchange.

```toml
[[notifiers]]
notifier_id = "ntfy-alerts"
provider = "ntfy"
enabled = true
minimum_urgency = "important"

[notifiers.options]
topic = "your-topic"
base_url = "https://ntfy.sh"
timeout_seconds = 10
```

`topic` is required. `base_url` defaults to `https://ntfy.sh`; optional `token` is sent as Bearer authorization. Choose server/topic access settings appropriate for mail content.
`timeout_seconds` defaults to 10 seconds. Environment placeholders are resolved
by MailFlow; keep endpoint tokens private.

Missing required configuration, HTTP errors and recognized platform rejection
fail delivery. The runtime records the failure without losing the stored mail;
fix the endpoint/access settings and retry the failed notification. A successful
HTTP response is not enough if the platform reports a business error.

---

<!-- zh-CN -->

# ntfy 通知器

组件标识为 `ntfy`，通过配置的 ntfy 地址发送邮件摘要。
本插件提供邮件推送，不提供接收聊天命令、任意文字提醒、图片或文件收发。

```toml
[[notifiers]]
notifier_id = "ntfy-alerts"
provider = "ntfy"
enabled = true
minimum_urgency = "important"

[notifiers.options]
topic = "your-topic"
base_url = "https://ntfy.sh"
timeout_seconds = 10
```

`topic` 必填，`base_url` 默认 `https://ntfy.sh`；可选 `token` 通过 Bearer 认证发送。请按邮件隐私需求配置服务器和主题权限。
`timeout_seconds` 默认 10 秒。环境变量由 MailFlow 展开，地址中的令牌需要保密。

缺少必要配置、HTTP 错误或可识别的平台拒绝均视为投递失败。
运行时保留已存邮件并记录失败，修正地址和访问设置后重试对应通知。
不能只因 HTTP 成功就把平台业务失败当成发送成功。

---

[Catalog](../../README.md) · [Metadata](plugin.json) · [Plugin page](https://github.com/Kingcxp/mailflow-repo/tree/main/notifier/mailflow-notify-ntfy)
