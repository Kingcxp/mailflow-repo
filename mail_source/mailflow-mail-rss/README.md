<!-- Generated from plugin.json by tools/gen_plugin_readmes.py. Edit plugin.json. -->

## RSS/Atom Mail Source

Turns any RSS or Atom feed into mail items, so newsletters, blogs, release
notes, course announcements and CI feeds flow through the same pipeline as real
mail: urgency classification, summaries, timed action items and reminders.

Registers the mail source component id `rss`.

### How it works

Each poll fetches every configured feed and walks both `<item>` (RSS) and
`<entry>` (Atom) elements. Per entry:

| Mail field | Taken from |
| ---------- | ---------- |
| `subject` | `title` (else `(no title)`) |
| `body_text` | `summary`, else `description` |
| `sender` | `feed@<feed domain>` with the domain as display name |
| `date` | `pubDate`, else `published` (falls back to "now") |
| `message_id` | `rss-<sha256 of guid/id/link>` — stable across restarts |

Identity comes from `guid`, then `id`, then `link`, so an edited title does not
resurface an entry. Feeds are read-only: replies are rejected, and a broken feed
is logged without stopping the other feeds or accounts.

### Options

| Option | Required | Default | Meaning |
| ------ | -------- | ------- | ------- |
| `feeds` | **yes** | `[]` | Feed URLs to poll. Empty means nothing to do. |
| `interval_seconds` | no | `900` | Seconds between polls (15 minutes by default). |

### Usage

```toml
[[accounts]]
account_id = "feeds"
provider = "rss"
enabled = true

[accounts.options]
feeds = [
  "https://example.com/blog/feed.xml",
  "https://github.com/Kingcxp/mailflow/releases.atom",
]
interval_seconds = 900
```

### Notes

- Give feed accounts their own notifier threshold: most feed items land on
  `info`, so `minimum_urgency = "important"` keeps them out of your phone.
- Polling is per-account, and a feed failure is isolated — one dead URL never
  blocks the rest of your mailboxes.
- The first poll ingests everything the feed currently exposes; after that only
  new entries arrive.

### Requirements

Standard library only (`urllib`, `xml.etree`).

### License

MIT — contributions welcome.

---

<!-- zh-CN -->

## RSS/Atom 邮件源

把任意 RSS 或 Atom 订阅源转换为邮件条目，让订阅邮件、博客、发布说明、课程公告和
CI 通知都走与真实邮件相同的流程：紧急度分类、摘要、定时事项与提醒。

注册的邮件源组件 id 为 `rss`。

### 工作方式

每次轮询会拉取所有配置的订阅源，并同时遍历 `<item>`（RSS）与 `<entry>`（Atom）
元素。对每个条目：

| 邮件字段 | 取值来源 |
| -------- | -------- |
| `subject` | `title`（缺失时为 `(no title)`） |
| `body_text` | `summary`，其次 `description` |
| `sender` | `feed@<源域名>`，显示名为该域名 |
| `date` | `pubDate`，其次 `published`（都缺失时取当前时间） |
| `message_id` | `rss-<guid/id/link 的 sha256>` —— 重启后依然稳定 |

标识优先取 `guid`，其次 `id`，再次 `link`，因此仅修改标题不会让旧条目重新出现。
订阅源是只读的：回复会被拒绝；某个源出错只会被记录，不会影响其他源或账户。

### 配置项

| 配置项 | 必填 | 默认值 | 说明 |
| ------ | ---- | ------ | ---- |
| `feeds` | **是** | `[]` | 要轮询的订阅源 URL。为空则无事可做。 |
| `interval_seconds` | 否 | `900` | 轮询间隔秒数（默认 15 分钟）。 |

### 用法

```toml
[[accounts]]
account_id = "feeds"
provider = "rss"
enabled = true

[accounts.options]
feeds = [
  "https://example.com/blog/feed.xml",
  "https://github.com/Kingcxp/mailflow/releases.atom",
]
interval_seconds = 900
```

### 说明

- 建议为订阅源单独设置通知阈值：大多数条目会落在 `info`，把
  `minimum_urgency` 设为 `"important"` 可避免它们推送到手机。
- 轮询按账户独立进行，且单个源的失败是隔离的 —— 一个失效 URL 不会阻塞其他邮箱。
- 首次轮询会摄取该源当前暴露的全部条目，之后只接收新条目。

### 依赖

仅使用标准库（`urllib`、`xml.etree`）。

### 协议

MIT —— 欢迎贡献。

---

Metadata: [`plugin.json`](plugin.json) · Marketplace: [https://github.com/Kingcxp/mailflow-repo/tree/main/mail_source/mailflow-mail-rss](https://github.com/Kingcxp/mailflow-repo/tree/main/mail_source/mailflow-mail-rss)
