<!-- Generated from plugin.json by tools/gen_plugin_readmes.py. Edit plugin.json. -->

# Outlook mail source

Component ID: `outlook`. Reuses the shared IMAP/SMTP source with the Outlook
server preset. It does not implement native OAuth; use credentials and access
settings accepted by your mailbox service.

```toml
[[accounts]]
account_id = "outlook-personal"
provider = "outlook"
email = "you@example.com"

[accounts.options]
password = "${MAIL_PASSWORD}"
initial_sync = "new"
catch_up_missed = false
```

See [IMAP options and behavior](../mailflow-mail-imap/README.md) for server
overrides, sending, history, catch-up, attachments and opt-in source-state sync.
The default receives new mail only; account IDs remain part of mail identity.

---

<!-- zh-CN -->

# Outlook 邮件源

组件标识为 `outlook`，复用共享 IMAP/SMTP 实现及 Outlook 服务器预设。
不提供原生 OAuth；凭据和收发权限必须符合实际邮箱服务要求。

```toml
[[accounts]]
account_id = "outlook-personal"
provider = "outlook"
email = "you@example.com"

[accounts.options]
password = "${MAIL_PASSWORD}"
initial_sync = "new"
catch_up_missed = false
```

服务器覆盖、发信、历史导入、补收、附件和原邮箱联动选项见
[IMAP 说明](../mailflow-mail-imap/README.md)。默认只接收新邮件，账户标识参与去重。

---

[Catalog](../../README.md) · [Metadata](plugin.json) · [Plugin page](https://github.com/Kingcxp/waymark-mail-plugins/tree/main/mail_source/mailflow-mail-outlook)
