<!-- Generated from plugin.json by tools/gen_plugin_readmes.py. Edit plugin.json. -->

# RSS/Atom mail source

Brings feed entries into MailFlow as read-only mail. Component ID: `rss`.

```toml
[[accounts]]
account_id = "feeds"
provider = "rss"

[accounts.options]
feeds = ["https://example.com/feed.xml"]
interval_seconds = 900
```

`feeds` is the required URL list; `interval_seconds` defaults to 900 seconds.
Titles become subjects and summaries/descriptions become bodies. Entry identity
uses the feed URL plus guid/id/link, with a content fallback when none exists.
Progress is marked after successful runtime handoff. One failing feed is reported
without preventing other feeds from running.

The first poll reads entries currently exposed by the feed. In-process repeats
are suppressed; after restart, stable IDs let storage deduplicate old entries.
This is not an IMAP cursor, historical archive or sending account: replies,
mailbox-state synchronization and source trash/restore are unsupported.

---

<!-- zh-CN -->

# RSS/Atom 邮件源

将订阅条目放入 MailFlow，作为只读邮件查看。组件标识为 `rss`。

```toml
[[accounts]]
account_id = "feeds"
provider = "rss"

[accounts.options]
feeds = ["https://example.com/feed.xml"]
interval_seconds = 900
```

`feeds` 填写订阅地址列表，轮询默认每 900 秒执行。
标题和摘要分别作为主题与正文；标识结合订阅地址和 guid/id/link，缺失时使用内容摘要。
成功交给运行时后才记录进度，单个订阅失败不阻止其他订阅。

首次读取订阅当前公开的条目，同次运行去重；重启后由稳定标识帮助存储去重。
本插件不提供 IMAP 游标、历史存档、发信或原邮箱状态修改能力。

---

[Catalog](../../README.md) · [Metadata](plugin.json) · [Plugin page](https://github.com/Kingcxp/mailflow-repo/tree/main/mail_source/mailflow-mail-rss)
