<!-- Generated from plugin.json by tools/gen_plugin_readmes.py. Edit plugin.json. -->

## Console Notifier

Surfaces already-computed mail analyses through MailFlow's log system
(terminal + file sinks): every alert above the threshold shows up in the rich
log output you are already watching — no additional transport is needed and
the message content stays visible where the rest of MailFlow logs.

Registers the notifier component id `console`.

### How it works

Each notification is one warning-level log line:

```
NOTIFY [urgent] Collect your student ID card — Pick up the card before 17:00. (office@example.edu)
```

i.e. urgency level, subject, summary and sender address. Delivery goes through
the standard logging system, so it lands in the same terminal and file sinks
the rest of MailFlow uses — including the TUI's log view.

### Options

None. Any `[[notifiers]]` entry with `provider = "console"` works as-is;
the standard threshold fields still apply:

| Option | Required | Default | Meaning |
| ------ | -------- | ------- | ------- |
| `minimum_urgency` | no | — | Standard notifier field: lowest urgency that triggers delivery. |

### Usage

```toml
[[notifiers]]
notifier_id = "console"
provider = "console"
enabled = true
minimum_urgency = "important"
```

### Notes

- Delivery cannot fail: writing a log line has no network dependency, which
  makes this the safest notifier for exercising a pipeline end to end.
- Pair it with the webhook or Telegram notifiers while developing and keep
  console enabled as the always-on fallback channel.

### Requirements

Standard library only (`logging`), plus `mailflow-core`.

### License

MIT — contributions welcome.

---

<!-- zh-CN -->

## 控制台通知器

把已经计算好的邮件分析结果通过 MailFlow 的日志系统（终端与文件 sink）呈现出来：
超过阈值的每条提醒都会出现在你本来就在查看的富文本日志里 —— 无需任何额外
传输通道，消息内容也始终保留在 MailFlow 其他日志旁边。

注册的通知器组件 id 为 `console`。

### 工作方式

每条通知就是一行 warning 级别的日志：

```
NOTIFY [urgent] Collect your student ID card — Pick up the card before 17:00. (office@example.edu)
```

即紧急程度、主题、摘要与发件人地址。投递走标准日志系统，因此会落入 MailFlow
其余部分共用的终端与文件 sink —— 包括 TUI 的日志视图。

### 配置项

无需配置。任何 `provider = "console"` 的 `[[notifiers]]` 条目开箱即用；
标准的阈值字段仍然生效：

| 配置项 | 必填 | 默认值 | 说明 |
| ------ | ---- | ------ | ---- |
| `minimum_urgency` | 否 | — | 标准通知器字段：触发投递的最低紧急程度。 |

### 用法

```toml
[[notifiers]]
notifier_id = "console"
provider = "console"
enabled = true
minimum_urgency = "important"
```

### 说明

- 投递不可能失败：写一行日志没有任何网络依赖，这使它成为端到端演练流水线时
  最稳妥的通知器。
- 开发阶段可以与 webhook 或 Telegram 通知器搭配使用，并保持 console 作为
  永远在线的兜底通道。

### 依赖

仅使用标准库（`logging`），以及 `mailflow-core`。

### 协议

MIT —— 欢迎贡献。

---

Metadata: [`plugin.json`](plugin.json) · Marketplace: [https://github.com/Kingcxp/mailflow-repo/tree/main/notifier/mailflow-notify-console](https://github.com/Kingcxp/mailflow-repo/tree/main/notifier/mailflow-notify-console)
