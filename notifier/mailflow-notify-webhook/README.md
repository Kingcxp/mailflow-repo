<!-- Generated from plugin.json by tools/gen_plugin_readmes.py. Edit plugin.json. -->

## Webhook Notifier

Delivers computed mail analyses to any HTTP endpoint as JSON — the shortest
path to a chat bridge, a team dashboard, a Home Assistant automation or a
serverless function.

Registers the notifier component id `webhook`.

### Payload

One POST per mail above the threshold, `Content-Type: application/json`:

```json
{
  "mail_id": "3f9c…",
  "urgency": "urgent",
  "subject": "Collect your student ID card",
  "summary": "Pick up the card at the office before 17:00.",
  "from": "office@example.edu",
  "reply_required": false
}
```

`urgency` is one of `ad`, `info`, `important`, `urgent` — the same four-level
contract the rest of MailFlow uses, so a receiver can colour-code on it
(`#909399`, `#67C23A`, `#E6A23C`, `#F56C6C`).

### Options

| Option | Required | Default | Meaning |
| ------ | -------- | ------- | ------- |
| `url` | **yes** | `""` | Endpoint that receives the POST. Missing → warn and skip. |
| `timeout_seconds` | no | `10` | Per-request HTTP timeout. |

### Usage

```toml
[[notifiers]]
notifier_id = "webhook"
provider = "webhook"
enabled = true
minimum_urgency = "important"

[notifiers.options]
url = "https://example.com/hooks/mailflow"
timeout_seconds = 10
```

### Notes

- Delivery failures are logged by the runtime and never abort mail processing,
  so a flaky endpoint cannot lose mail.
- Need custom auth headers? Copy this plugin as a starting point — it is ~60
  lines of standard library code.

### Requirements

Standard library only (`urllib`, `json`).

### License

MIT — contributions welcome.

---

<!-- zh-CN -->

## Webhook 通知器

以 JSON 形式把邮件分析结果投递到任意 HTTP 端点 —— 这是接入聊天桥、团队看板、
Home Assistant 自动化或无服务器函数的最短路径。

注册的通知器组件 id 为 `webhook`。

### 请求体

每封超过阈值的邮件发送一次 POST，`Content-Type: application/json`：

```json
{
  "mail_id": "3f9c…",
  "urgency": "urgent",
  "subject": "请领取你的学生证",
  "summary": "请在 17:00 前到办公室领取证件。",
  "from": "office@example.edu",
  "reply_required": false
}
```

`urgency` 取值为 `ad`、`info`、`important`、`urgent` —— 与 MailFlow 其他部分一致
的四级契约，接收端可据此配色（`#909399`、`#67C23A`、`#E6A23C`、`#F56C6C`）。

### 配置项

| 配置项 | 必填 | 默认值 | 说明 |
| ------ | ---- | ------ | ---- |
| `url` | **是** | `""` | 接收 POST 的端点。未设置时记录警告并跳过。 |
| `timeout_seconds` | 否 | `10` | 单次请求的 HTTP 超时秒数。 |

### 用法

```toml
[[notifiers]]
notifier_id = "webhook"
provider = "webhook"
enabled = true
minimum_urgency = "important"

[notifiers.options]
url = "https://example.com/hooks/mailflow"
timeout_seconds = 10
```

### 说明

- 投递失败由运行时记录，绝不会中断邮件处理，因此端点不稳定也不会丢邮件。
- 需要自定义鉴权头？可以直接拷贝本插件作为起点 —— 它只有约 60 行标准库代码。

### 依赖

仅使用标准库（`urllib`、`json`）。

### 协议

MIT —— 欢迎贡献。

---

Metadata: [`plugin.json`](plugin.json) · Marketplace: [https://github.com/Kingcxp/mailflow-repo/tree/main/notifier/mailflow-notify-webhook](https://github.com/Kingcxp/mailflow-repo/tree/main/notifier/mailflow-notify-webhook)
