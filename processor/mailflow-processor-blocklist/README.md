<!-- Generated from plugin.json by tools/gen_plugin_readmes.py. Edit plugin.json. -->

# Sender blocklist processor

Component ID: `blocklist`. Classifies matching sender addresses or domains as
`ad` without deleting mail or changing the source mailbox.

```toml
[[processors]]
processor_id = "blocklist"
provider = "blocklist"
priority = 5

[processors.options]
senders = ["ads@example.com"]
domains = ["marketing.example"]
```

Matching is case-insensitive. `senders` matches exact addresses; `domains` matches
`@domain`, not arbitrary subdomains. Empty lists do nothing. The processor does
not stop the chain: later processors, including an LLM, may still run and update
the analysis. Priority alone does not guarantee zero model calls. Remove a rule
and reanalyze affected mail to reconsider its automatic classification; a manual
priority override remains a separate user choice.

---

<!-- zh-CN -->

# 发件人黑名单处理器

组件标识为 `blocklist`。匹配的发件地址或域名分类为 `ad`，不删除邮件、不修改原邮箱。

```toml
[[processors]]
processor_id = "blocklist"
provider = "blocklist"
priority = 5

[processors.options]
senders = ["ads@example.com"]
domains = ["marketing.example"]
```

匹配不区分大小写；地址精确匹配，域名匹配 `@domain`，不自动覆盖任意子域名。
列表为空时不处理。本处理器不终止处理链，后续模型仍可能运行并更新分析，
仅调整优先级不能保证零模型调用。移除规则后可重析相关邮件，人工优先级是独立设置。

---

[Catalog](../../README.md) · [Metadata](plugin.json) · [Plugin page](https://github.com/Kingcxp/mailflow-repo/tree/main/processor/mailflow-processor-blocklist)
