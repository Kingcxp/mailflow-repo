## RSS/Atom Source

Turns any RSS or Atom feed into mail items, so newsletters, blogs, release notes and CI feeds flow through the same pipeline (classification, summaries, reminders).

### Features

- Multiple feeds per account; configurable poll interval
- Deduplication by entry id/link; entries seen once stay seen
- Standard library only (urllib + xml.etree)
- Read-only: replies are rejected with a clear error

### Usage

```toml
[[accounts]]
account_id = "news"
provider = "rss"
enabled = true
[accounts.options]
feeds = [
  "https://example.com/feed.xml",
  "https://another.example/atom.xml",
]
interval_seconds = 900   # poll interval (default 900)
```

### License

MIT — contributions welcome.
