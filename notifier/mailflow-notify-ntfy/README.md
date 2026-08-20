<!-- Generated from plugin.json by tools/gen_plugin_readmes.py. Edit plugin.json. -->

## ntfy Notifier

Pushes mail alerts to an [ntfy](https://ntfy.sh) topic. Works with the public
`ntfy.sh` service or any self-hosted ntfy server, so alerts arrive on your
phone through the ntfy app without running a bot or an SMTP relay.

Registers the notifier component id `ntfy`.

### How it works

Every mail that clears the notifier's `minimum_urgency` threshold is POSTed as
one JSON message: the mail subject becomes the ntfy *title*, the analysis
summary becomes the *message body*, and the effective urgency becomes the ntfy
priority. Delivery runs off the event loop, so a slow server never stalls mail
processing.

| MailFlow urgency | ntfy priority |
| ---------------- | ------------- |
| `ad` (gray)      | `1` (min)     |
| `info` (green)   | `3` (default) |
| `important` (orange) | `4` (high) |
| `urgent` (red)   | `5` (urgent)  |

### Options

| Option | Required | Default | Meaning |
| ------ | -------- | ------- | ------- |
| `topic` | **yes** | — | ntfy topic to publish to. Without it the notifier logs a warning and skips every message. |
| `base_url` | no | `https://ntfy.sh` | Server base URL; point it at your self-hosted instance. |
| `token` | no | `""` | Access token for a protected topic, sent as `Authorization: Bearer`. |
| `timeout_seconds` | no | `10` | Per-request HTTP timeout. |

### Usage

```toml
[[notifiers]]
notifier_id = "ntfy"
provider = "ntfy"
enabled = true
minimum_urgency = "important"   # ad | info | important | urgent

[notifiers.options]
topic = "my-mailflow-alerts"    # required
base_url = "https://ntfy.sh"    # or your own server
token = "${NTFY_TOKEN}"         # only needed for protected topics
timeout_seconds = 10
```

Subscribe to the same topic in the ntfy mobile app (or `ntfy subscribe
my-mailflow-alerts`) and you are done.

### Troubleshooting

- **Nothing arrives, no errors** — `topic` is unset; the notifier warns once
  and skips. Check `mailflow.notification.ntfy` in the log.
- **`403`/`401`** — the topic is protected: set `token`, ideally through a
  `${NTFY_TOKEN}` placeholder so the value never lands in the config file.
- **Too many messages** — raise `minimum_urgency` to `urgent`.

### Requirements

Standard library only (`urllib`); no dependency beyond `mailflow-core`.

### License

MIT — contributions welcome.

---

<!-- zh-CN -->

## ntfy 通知器

把邮件提醒推送到 [ntfy](https://ntfy.sh) 主题。支持公共 `ntfy.sh` 服务或任何自建
ntfy 服务器，无需运行机器人或 SMTP 中继，提醒直达手机上的 ntfy 应用。

注册的通知器组件 id 为 `ntfy`。

### 工作方式

每封达到 `minimum_urgency` 阈值的邮件都会以一条 JSON 消息 POST 出去：邮件主题作为
ntfy 的*标题*，分析摘要作为*正文*，有效紧急度映射为 ntfy 优先级。推送在事件循环之外
执行，服务器再慢也不会阻塞邮件处理。

| MailFlow 紧急度 | ntfy 优先级 |
| --------------- | ----------- |
| `ad`（灰）      | `1`（最低） |
| `info`（绿）    | `3`（默认） |
| `important`（橙）| `4`（高）   |
| `urgent`（红）  | `5`（紧急） |

### 配置项

| 配置项 | 必填 | 默认值 | 说明 |
| ------ | ---- | ------ | ---- |
| `topic` | **是** | — | 要发布到的 ntfy 主题。未设置时通知器只记录一条警告并跳过所有消息。 |
| `base_url` | 否 | `https://ntfy.sh` | 服务器地址，可指向自建实例。 |
| `token` | 否 | `""` | 受保护主题的访问令牌，通过 `Authorization: Bearer` 发送。 |
| `timeout_seconds` | 否 | `10` | 单次请求的 HTTP 超时秒数。 |

### 用法

```toml
[[notifiers]]
notifier_id = "ntfy"
provider = "ntfy"
enabled = true
minimum_urgency = "important"   # ad | info | important | urgent

[notifiers.options]
topic = "my-mailflow-alerts"    # 必填
base_url = "https://ntfy.sh"    # 或你的自建服务器
token = "${NTFY_TOKEN}"         # 仅受保护主题需要
timeout_seconds = 10
```

在 ntfy 手机应用中订阅同一主题（或执行 `ntfy subscribe my-mailflow-alerts`）即可。

### 排查

- **收不到消息且没有报错** —— `topic` 未设置，通知器会警告一次后跳过。请查看日志中的
  `mailflow.notification.ntfy`。
- **返回 `403`/`401`** —— 主题受保护：请设置 `token`，建议使用 `${NTFY_TOKEN}`
  占位符，避免明文写入配置文件。
- **消息太多** —— 把 `minimum_urgency` 调高到 `urgent`。

### 依赖

仅使用标准库（`urllib`），除 `mailflow-core` 外无额外依赖。

### 协议

MIT —— 欢迎贡献。

---

Metadata: [`plugin.json`](plugin.json) · Marketplace: [https://github.com/Kingcxp/mailflow-repo/tree/main/notifier/mailflow-notify-ntfy](https://github.com/Kingcxp/mailflow-repo/tree/main/notifier/mailflow-notify-ntfy)
