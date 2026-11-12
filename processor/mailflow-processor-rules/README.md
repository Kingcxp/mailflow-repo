<!-- Generated from plugin.json by tools/gen_plugin_readmes.py. Edit plugin.json. -->

# Rule-template processor

Component ID: `rule-templates`, separate from the core `rules` processor.
Applies the first matching configured template.

```toml
[[processors]]
processor_id = "templates"
provider = "rule-templates"
priority = 15

[processors.options]
rules = [{ match = { field = "subject", contains = "invoice" }, action = { urgency = "important", summary = "Review the invoice." } }]
```

Each rule has `match.field` (`sender`, `subject` or `body`), a nonempty `contains`
substring, and `action.urgency`/`summary`. Matching is case-insensitive; empty
conditions are skipped. The first match contributes an analysis overlay and
later processors may still run. Supported urgency values are `ad`, `info`,
`important` and `urgent`. No match leaves the current processing result unchanged.

---

<!-- zh-CN -->

# 规则模板处理器

组件标识为 `rule-templates`，与核心 `rules` 处理器不同，按顺序应用首条匹配模板。

```toml
[[processors]]
processor_id = "templates"
provider = "rule-templates"
priority = 15

[processors.options]
rules = [{ match = { field = "subject", contains = "invoice" }, action = { urgency = "important", summary = "请核对账单。" } }]
```

每条规则包含字段、非空匹配子串和重要程度／摘要。字段可选 `sender`、`subject`、`body`，
匹配不区分大小写，空条件跳过。首次命中提供分析结果，但后续处理器仍可运行。
重要程度支持 `ad`、`info`、`important`、`urgent`；无命中时不改变当前结果。

---

[Catalog](../../README.md) · [Metadata](plugin.json) · [Plugin page](https://github.com/Kingcxp/mailflow-repo/tree/main/processor/mailflow-processor-rules)
