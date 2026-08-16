## Sender Blocklist Processor

A cheap, deterministic pre-filter that marks mail from unwanted senders or domains as junk (gray / `ad`) before any LLM work — exact sender addresses and full domains are matched case-insensitively.

### Features

- Exact sender-address matches and domain-suffix matches
- No LLM involved; runs in milliseconds

### Usage

```toml
[[processors]]
processor_id = "blocklist"
provider = "blocklist"
priority = 5              # run before the rules processor
retries = 0
[processors.options]
senders = ["spam@example.com"]
domains = ["spammy-newsletter.example"]
```

### License

MIT — contributions welcome.
