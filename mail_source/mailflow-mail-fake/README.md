<!-- Generated from plugin.json by tools/gen_plugin_readmes.py. Edit plugin.json. -->

# Fake mail source

Provides deterministic messages for local development and demonstrations without
connecting to a mailbox. Component ID: `fake`.

```toml
[[accounts]]
account_id = "demo"
provider = "fake"
email = "demo@local.test"

[accounts.options]
base_time = "2026-01-01T08:00:00+00:00"
mails = [{ message_id = "welcome", subject = "Welcome", sender = "team@example.com", body = "Your workspace is ready." }]
```

`mails` accepts `message_id`, `subject`, `sender`, `sender_name`, `body`,
`body_html` and an optional `urgency` hint. Keep message IDs stable to exercise
retry deduplication. Timestamps use `base_time` plus the message index in minutes.
`fail = true` and `delay` (seconds) simulate source failures and slow handoff.
This is a development source, not a way to send real email.

---

<!-- zh-CN -->

# 假邮件源

用于本地开发和演示，不连接真实邮箱。组件标识为 `fake`。

```toml
[[accounts]]
account_id = "demo"
provider = "fake"
email = "demo@local.test"

[accounts.options]
base_time = "2026-01-01T08:00:00+00:00"
mails = [{ message_id = "welcome", subject = "欢迎使用", sender = "team@example.com", body = "工作区已就绪。" }]
```

邮件支持标识、主题、发件人、显示名、纯文本、HTML 和可选重要程度提示。
同一邮件保持相同标识以验证重试去重；时间按基础时间和序号分钟数生成。
`fail = true` 模拟读取失败，`delay` 设置延迟秒数。本插件不发送真实邮件。

---

[Catalog](../../README.md) · [Metadata](plugin.json) · [Plugin page](https://github.com/Kingcxp/mailflow-repo/tree/main/mail_source/mailflow-mail-fake)
