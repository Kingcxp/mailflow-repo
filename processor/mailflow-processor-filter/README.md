<!-- Generated from plugin.json by tools/gen_plugin_readmes.py. Edit plugin.json. -->

# Content filter processor

Component ID: `filter`. Marks a match as `ad` while keeping the original mail.

```toml
[[processors]]
processor_id = "content-filter"
provider = "filter"
priority = 5

[processors.options]
senders = ["ads@example.com"]
subjects = ["Promotion"]
keywords = ["unsubscribe"]
```

The lists default to empty. Matching is case-insensitive: sender addresses are
exact, while subjects and plain-text bodies use substrings. Any match contributes
an analysis result. This does not delete mail or stop later processors; a later
analysis may replace the classification. Notification thresholds are configured
on notifiers, separately from filtering.

---

<!-- zh-CN -->

# 内容过滤处理器

组件标识为 `filter`，匹配时标为 `ad`，保留原始邮件。

```toml
[[processors]]
processor_id = "content-filter"
provider = "filter"
priority = 5

[processors.options]
senders = ["ads@example.com"]
subjects = ["促销"]
keywords = ["退订"]
```

列表默认为空。匹配不区分大小写：发件地址精确匹配，主题与纯文本正文按子串匹配。
任一条件命中即提供分析结果，但不删除邮件、不终止后续处理，后面的分析可以更新分类。
是否推送还取决于通知器的重要程度阈值。

---

[Catalog](../../README.md) · [Metadata](plugin.json) · [Plugin page](https://github.com/Kingcxp/waymark-mail-plugins/tree/main/processor/mailflow-processor-filter)
