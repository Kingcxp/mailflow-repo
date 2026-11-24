<!-- Generated from plugin.json by tools/gen_plugin_readmes.py. Edit plugin.json. -->

# SMTP notifier

Component ID: `smtp`. Sends mail summaries as notification emails, separate
from composing or replying through a source account.

```toml
[[notifiers]]
notifier_id = "email-alerts"
provider = "smtp"
minimum_urgency = "important"

[notifiers.options]
host = "smtp.example.com"
port = 587
use_tls = true
username = "alerts@example.com"
password = "${SMTP_PASSWORD}"
from_addr = "alerts@example.com"
to = ["you@example.com"]
```

`host`, `from_addr` and a nonempty recipient list `to` are required.
`use_tls = true` uses STARTTLS (default port 587); false selects implicit TLS,
so also set the correct port, usually 465. Username/password are optional for
servers permitting unauthenticated submission. No plaintext-only mode is exposed.

The notification contains the subject/priority, summary and available plain-text
body; it does not forward source attachments. Per-target mail delivery lets the
runtime retain successful recipient receipts. Missing configuration, rejected
recipients or SMTP/network failures are failures, not successful sends. This
plugin provides no incoming chat commands or managed file exchange.

---

<!-- zh-CN -->

# SMTP 通知器

组件标识为 `smtp`，将邮件摘要作为通知邮件发送，与来源账户的新建／回复邮件不同。

```toml
[[notifiers]]
notifier_id = "email-alerts"
provider = "smtp"
minimum_urgency = "important"

[notifiers.options]
host = "smtp.example.com"
port = 587
use_tls = true
username = "alerts@example.com"
password = "${SMTP_PASSWORD}"
from_addr = "alerts@example.com"
to = ["you@example.com"]
```

主机、发件地址和非空收件人列表必填。`use_tls = true` 使用 STARTTLS，默认端口 587；
设为 false 时使用隐式 TLS，应同时设置正确端口，通常为 465。服务器允许时可不填认证信息，
不提供纯明文模式。

通知包含主题、重要程度、摘要和已有纯文本正文，不转发原附件。
按目标投递可保留已成功收件人的凭据；配置缺失、拒收、SMTP 或网络错误均视为失败。
本插件不接收聊天命令，不提供受管文件交换。

---

[Catalog](../../README.md) · [Metadata](plugin.json) · [Plugin page](https://github.com/Kingcxp/waymark-mail-repo/tree/main/notifier/mailflow-notify-smtp)
