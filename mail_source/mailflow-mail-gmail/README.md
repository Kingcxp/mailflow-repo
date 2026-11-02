<!-- Generated from plugin.json by tools/gen_plugin_readmes.py. Edit plugin.json. -->

## Gmail Mail Source

Component ID: `gmail`. Uses the shared IMAP/SMTP source with the Gmail
preset; this adapter does not implement native OAuth. Configure the credentials
accepted by your mailbox service and enable the required receive/send access.

```toml
[[accounts]]
account_id = "gmail-main"
provider = "gmail"
email = "you@example.com"

[accounts.options]
password = "${MAIL_PASSWORD}"
```

For host overrides, polling options, history and retry behavior, see the
[IMAP source](../mailflow-mail-imap/README.md). Mail identity remains account-scoped.

---

<!-- zh-CN -->

## Gmail 邮件源

组件标识为 `gmail`，使用共享 IMAP/SMTP 实现及 Gmail 预设，
目前未实现原生 OAuth。请配置邮箱服务接受的凭据，并开启所需的收发访问权限。

```toml
[[accounts]]
account_id = "gmail-main"
provider = "gmail"
email = "you@example.com"

[accounts.options]
password = "${MAIL_PASSWORD}"
```

主机覆盖、轮询选项、历史浏览及重试规则见
[IMAP 邮件源](../mailflow-mail-imap/README.md)。邮件按账户范围区分。

---

Metadata: [`plugin.json`](plugin.json) · Marketplace: [https://github.com/Kingcxp/mailflow-repo/tree/main/mail_source/mailflow-mail-gmail](https://github.com/Kingcxp/mailflow-repo/tree/main/mail_source/mailflow-mail-gmail)
