<!-- Generated from plugin.json by tools/gen_plugin_readmes.py. Edit plugin.json. -->

## Sender Blocklist Processor

A cheap, deterministic pre-filter that marks mail from unwanted senders or
whole domains as junk (`ad`, gray `#909399`) before any LLM work happens. Every
blocked mail costs zero tokens and finishes in microseconds.

Registers the processor component id `blocklist`.

### How it works

The processor compares the sender address, lower-cased, against two sets:

- **`senders`** — exact address matches (`ads@shop.example`)
- **`domains`** — domain suffix matches, i.e. the address ends with
  `@<domain>` (`shop.example` blocks `anything@shop.example`)

On a match it returns an analysis with `urgency = "ad"`, the summary
`"Blocked sender"` and a reason naming the address, then lets the chain
continue. On no match it contributes nothing, so later processors (and the LLM)
see the mail untouched.

Because MailFlow merges processor results in priority order, give the blocklist
a **lower `priority` than the LLM processor** so the LLM never runs for mail you
already rejected.

### Options

| Option | Required | Default | Meaning |
| ------ | -------- | ------- | ------- |
| `senders` | no | `[]` | Exact sender addresses to reject (case-insensitive). |
| `domains` | no | `[]` | Domains to reject; matches `*@domain` (case-insensitive). |

With both lists empty the processor is a no-op.

### Usage

```toml
[[processors]]
processor_id = "blocklist"
provider = "blocklist"
enabled = true
priority = 5              # before rules (10) and llm-importance (20)

[processors.options]
senders = ["ads@shop.example", "no-reply@spam.example"]
domains = ["marketing.example", "promo.example"]
```

### Recipes

- **Kill a newsletter flood** — add its domain instead of chasing individual
  `From` addresses; senders rotate, domains rarely do.
- **Keep it reviewable** — blocked mail is not deleted, only classified `ad`;
  it stays in the list (and the trash retention rules) so you can audit it.
- **Undo a mistake** — remove the entry and set the mail's urgency back with
  `mail urgency <id> auto`, or override it manually in the TUI.

### Requirements

No dependencies beyond `mailflow-core`; no network access, no LLM.

### License

MIT — contributions welcome.

---

<!-- zh-CN -->

## 发件人黑名单处理器

一个廉价、确定性的前置过滤器：在任何大模型工作之前，把来自不受欢迎发件人或整个
域名的邮件标记为垃圾（`ad`，灰色 `#909399`）。每封被拦截的邮件消耗零 token，
耗时为微秒级。

注册的处理器组件 id 为 `blocklist`。

### 工作方式

处理器把发件地址转为小写后与两个集合比对：

- **`senders`** —— 精确地址匹配（`ads@shop.example`）
- **`domains`** —— 域名后缀匹配，即地址以 `@<域名>` 结尾（`shop.example` 会拦截
  `anything@shop.example`）

命中时返回 `urgency = "ad"`、摘要为 `"Blocked sender"` 且理由中包含该地址的分析
结果，随后处理链继续。未命中则不产生任何结果，后续处理器（以及大模型）看到的是
未被改动的邮件。

由于 MailFlow 按优先级顺序合并处理器结果，请给黑名单设置**比大模型处理器更小的
`priority`**，这样已被拒绝的邮件就不会再触发大模型。

### 配置项

| 配置项 | 必填 | 默认值 | 说明 |
| ------ | ---- | ------ | ---- |
| `senders` | 否 | `[]` | 要拒收的精确发件地址（不区分大小写）。 |
| `domains` | 否 | `[]` | 要拒收的域名，匹配 `*@域名`（不区分大小写）。 |

两个列表都为空时，处理器不做任何事。

### 用法

```toml
[[processors]]
processor_id = "blocklist"
provider = "blocklist"
enabled = true
priority = 5              # 早于 rules（10）与 llm-importance（20）

[processors.options]
senders = ["ads@shop.example", "no-reply@spam.example"]
domains = ["marketing.example", "promo.example"]
```

### 实用技巧

- **压制订阅邮件轰炸** —— 直接加域名，而不是逐个追踪 `From` 地址；发件人常换，
  域名很少变。
- **保持可复查** —— 被拦截的邮件不会被删除，只是被分类为 `ad`，仍留在列表（以及
  回收站保留规则）中，方便事后审查。
- **误伤后撤回** —— 删掉对应条目，并用 `mail urgency <id> auto` 恢复自动紧急度，
  或在 TUI 中手动覆盖。

### 依赖

除 `mailflow-core` 外无依赖；不访问网络，也不调用大模型。

### 协议

MIT —— 欢迎贡献。

---

Metadata: [`plugin.json`](plugin.json) · Marketplace: [https://github.com/Kingcxp/mailflow-repo/tree/main/processor/mailflow-processor-blocklist](https://github.com/Kingcxp/mailflow-repo/tree/main/processor/mailflow-processor-blocklist)
