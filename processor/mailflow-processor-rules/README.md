<!-- Generated from plugin.json by tools/gen_plugin_readmes.py. Edit plugin.json. -->

# Rule Templates Processor

Registers the processor component id `rule-templates`. Options: `rules` as a list of `{match: {field, contains}, action: {urgency, summary}}` dicts; the first match wins.


Uses `rule-templates` to keep the core `rules` processor available. Existing template configurations should select `provider = "rule-templates"`.

---

<!-- zh-CN -->

# Rule Templates Processor

Registers the processor component id `rule-templates`. Options: `rules` as a list of `{match: {field, contains}, action: {urgency, summary}}` dicts; the first match wins.


组件使用 `rule-templates`，避免覆盖核心内置的 `rules`。已有规则模板配置请改用 `provider = "rule-templates"`。

---

Metadata: [`plugin.json`](plugin.json) · Marketplace: [https://github.com/Kingcxp/mailflow-repo/tree/main/processor/mailflow-processor-rules](https://github.com/Kingcxp/mailflow-repo/tree/main/processor/mailflow-processor-rules)
