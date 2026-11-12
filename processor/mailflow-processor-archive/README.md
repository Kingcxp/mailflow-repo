<!-- Generated from plugin.json by tools/gen_plugin_readmes.py. Edit plugin.json. -->

# Local auto-archive processor

Component ID: `archive`. Archives matching mail inside MailFlow while retaining
its priority, analysis and original content. It does not move source mailbox mail.

```toml
[[processors]]
processor_id = "local-archive"
provider = "archive"
priority = 5

[processors.options]
senders = ["reports@example.com"]
domains = ["news.example"]
```

`senders` and `domains` are optional lists, matched case-insensitively against
exact addresses and `@domain`. Empty lists do nothing. Archived mail remains
searchable and can be returned to the inbox. Archiving is separate from trash,
priority filtering and the account's optional source-state synchronization.

---

<!-- zh-CN -->

# 本地自动归档处理器

组件标识为 `archive`，将匹配邮件归档到 MailFlow，保留重要程度、分析和原文，
不移动原邮箱邮件。

```toml
[[processors]]
processor_id = "local-archive"
provider = "archive"
priority = 5

[processors.options]
senders = ["reports@example.com"]
domains = ["news.example"]
```

发件人和域名列表可选，按地址及 `@domain` 匹配，不区分大小写；为空时不处理。
归档邮件仍可搜索、恢复到收件箱。归档、回收站、重要程度过滤和账户原邮箱联动是不同操作。

---

[Catalog](../../README.md) · [Metadata](plugin.json) · [Plugin page](https://github.com/Kingcxp/mailflow-repo/tree/main/processor/mailflow-processor-archive)
