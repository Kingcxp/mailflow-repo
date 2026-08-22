<!-- Generated from plugin.json by tools/gen_plugin_readmes.py. Edit plugin.json. -->

## Fake Mail Source

Deterministic local mails for development and demo setups: declare messages
right in the config file and run the whole pipeline — analysis, notifications,
storage — without ever touching a real mailbox.

Registers the mail source component id `fake`.

### How it works

Mails are declared in the account options as a `mails` list of dicts.
Timestamps are deterministic: message *n* gets the base time plus *n* minutes,
so repeated runs see identical data and demos are reproducible. Fetch failures and delays can be simulated deliberately through the `fail`
and `delay` options.

### Account options

| Option | Required | Default | Meaning |
| ------ | -------- | ------- | ------- |
| `mails` | **yes** | `[]` | List of message dicts (fields below). |
| `base_time` | no | `2026-01-01T08:00:00+00:00` | ISO timestamp of the first mail; each later one adds its index in minutes. |
| `fail` | no | `false` | Make fetches raise, to exercise error paths. |
| `delay` | no | `0.0` | Artificial per-fetch delay in seconds. |

Each entry in `mails` accepts:

| Field | Default | Meaning |
| ----- | ------- | ------- |
| `message_id` | `fake-<index>` | Stable identity (dedup key). |
| `subject` | `(no subject)` | Subject line. |
| `sender` | `sender@example.com` | Sender address. |
| `sender_name` | `""` | Sender display name. |
| `body` | `""` | Plain-text body. |
| `body_html` | `""` | HTML body. |
| `urgency` | — | Pre-set urgency hint (`ad`/`info`/`important`/`urgent`). |

### Usage

```toml
[[accounts]]
account_id = "demo"
provider = "fake"
email = "demo@local.test"
enabled = true

[accounts.options]
base_time = "2026-01-01T08:00:00+00:00"

[[accounts.options.mails]]
message_id = "welcome"
subject = "Collect your student ID card"
sender = "office@example.edu"
sender_name = "Student Office"
body = "Pick up the card at the office before 17:00."
urgency = "urgent"

[[accounts.options.mails]]
subject = "Weekly digest"
sender = "news@example.org"
body = "Everything that happened this week."
```

### Requirements

Standard library only (`asyncio`), plus `mailflow-core`.

### License

MIT — contributions welcome.

---

<!-- zh-CN -->

## 假邮件源

面向开发与演示环境的确定性本地邮件源：直接在配置文件里声明邮件，就能跑通
整条流水线 —— 分析、通知、存储 —— 完全不必碰真实邮箱。

注册的邮件源组件 id 为 `fake`。

### 工作方式

邮件以字典列表的形式声明在账户选项的 `mails` 里。时间戳是确定性的：第 *n*
封邮件的时间为基础时间加 *n* 分钟，因此重复运行看到的数据完全一致，演示
可以精确复现。还可以通过 `fail` 与 `delay` 选项主动模拟拉取失败与延迟。

### 账户配置项

| 配置项 | 必填 | 默认值 | 说明 |
| ------ | ---- | ------ | ---- |
| `mails` | **是** | `[]` | 邮件字典列表（字段见下）。 |
| `base_time` | 否 | `2026-01-01T08:00:00+00:00` | 第一封邮件的 ISO 时间戳；后续邮件依次加自身序号对应的分钟数。 |
| `fail` | 否 | `false` | 让拉取抛出异常，用于演练错误路径。 |
| `delay` | 否 | `0.0` | 每次拉取的人为延迟秒数。 |

`mails` 中每一项支持：

| 字段 | 默认值 | 说明 |
| ---- | ------ | ---- |
| `message_id` | `fake-<index>` | 稳定标识（去重键）。 |
| `subject` | `(no subject)` | 主题。 |
| `sender` | `sender@example.com` | 发件人地址。 |
| `sender_name` | `""` | 发件人显示名。 |
| `body` | `""` | 纯文本正文。 |
| `body_html` | `""` | HTML 正文。 |
| `urgency` | — | 预设的紧急程度提示（`ad`/`info`/`important`/`urgent`）。 |

### 用法

```toml
[[accounts]]
account_id = "demo"
provider = "fake"
email = "demo@local.test"
enabled = true

[accounts.options]
base_time = "2026-01-01T08:00:00+00:00"

[[accounts.options.mails]]
message_id = "welcome"
subject = "Collect your student ID card"
sender = "office@example.edu"
sender_name = "Student Office"
body = "Pick up the card at the office before 17:00."
urgency = "urgent"

[[accounts.options.mails]]
subject = "Weekly digest"
sender = "news@example.org"
body = "Everything that happened this week."
```

### 依赖

仅使用标准库（`asyncio`），以及 `mailflow-core`。

### 协议

MIT —— 欢迎贡献。

---

Metadata: [`plugin.json`](plugin.json) · Marketplace: [https://github.com/Kingcxp/mailflow-repo/tree/main/mail_source/mailflow-mail-fake](https://github.com/Kingcxp/mailflow-repo/tree/main/mail_source/mailflow-mail-fake)
