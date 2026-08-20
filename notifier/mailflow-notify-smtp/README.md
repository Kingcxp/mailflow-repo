<!-- Generated from plugin.json by tools/gen_plugin_readmes.py. Edit plugin.json. -->

## SMTP Notifier

Forwards important mail alerts as e-mail through any SMTP server (Gmail,
Outlook, a university relay, or a self-hosted one). Useful when the final
channel has to be plain e-mail — a team distribution list, a ticketing inbox,
or an address your phone already pushes.

Registers the notifier component id `smtp`.

### How it works

For every mail above the threshold the notifier builds one message:

- **Subject** — `[<urgency>] <original subject>`, so filters can key on the level
- **Body** — the analysis summary (falling back to the subject), with the
  original mail text attached as an alternative part
- **Delivery** — STARTTLS on port 587 by default, or implicit SSL when
  `use_tls = false` (typically port 465). Sending runs off the event loop.

### Options

| Option | Required | Default | Meaning |
| ------ | -------- | ------- | ------- |
| `host` | **yes** | `""` | SMTP server hostname. |
| `from_addr` | **yes** | `""` | Envelope/From address of the alert. |
| `to` | **yes** | `[]` | List of recipient addresses. |
| `port` | no | `587` | SMTP port. |
| `use_tls` | no | `true` | `true` = STARTTLS (587); `false` = implicit SSL (465). |
| `username` | no | `""` | Login user; authentication is skipped when empty. |
| `password` | no | `""` | Login password — use a `${ENV_VAR}` placeholder. |

Missing `host`, `from_addr` or `to` makes the notifier log a warning and skip;
it never breaks the pipeline.

### Usage

```toml
[[notifiers]]
notifier_id = "smtp-forward"
provider = "smtp"
enabled = true
minimum_urgency = "urgent"

[notifiers.options]
host = "smtp.gmail.com"
port = 587
use_tls = true
username = "me@gmail.com"
password = "${SMTP_APP_PASSWORD}"
from_addr = "me@gmail.com"
to = ["team@example.com", "me@example.com"]
```

### Troubleshooting

- **Gmail/Outlook rejects the login** — use an app password, not the account
  password, and keep it in an environment variable.
- **Timeouts on port 465** — 465 is implicit SSL: set `use_tls = false`.
- **Alert loops** — never point `to` at a mailbox MailFlow itself polls, or
  each alert becomes new mail to classify.

### Requirements

Standard library only (`smtplib`, `email`).

### License

MIT — contributions welcome.

---

<!-- zh-CN -->

## SMTP 通知器

通过任意 SMTP 服务器（Gmail、Outlook、学校中继或自建服务）把重要邮件提醒转发为
电子邮件。当最终通知渠道必须是普通邮件时很有用 —— 例如团队邮件列表、工单邮箱，
或手机已经会推送的某个地址。

注册的通知器组件 id 为 `smtp`。

### 工作方式

对每封超过阈值的邮件，通知器会构造一封邮件：

- **主题** —— `[<紧急度>] <原始主题>`，便于按级别设置过滤规则
- **正文** —— 分析摘要（缺失时回退为主题），并把原始邮件正文作为备选部分附上
- **投递** —— 默认在 587 端口使用 STARTTLS；`use_tls = false` 时改用隐式 SSL
  （通常为 465 端口）。发送在事件循环之外执行。

### 配置项

| 配置项 | 必填 | 默认值 | 说明 |
| ------ | ---- | ------ | ---- |
| `host` | **是** | `""` | SMTP 服务器主机名。 |
| `from_addr` | **是** | `""` | 提醒邮件的发件地址。 |
| `to` | **是** | `[]` | 收件地址列表。 |
| `port` | 否 | `587` | SMTP 端口。 |
| `use_tls` | 否 | `true` | `true` 表示 STARTTLS（587）；`false` 表示隐式 SSL（465）。 |
| `username` | 否 | `""` | 登录用户名；为空时跳过鉴权。 |
| `password` | 否 | `""` | 登录密码 —— 建议使用 `${环境变量}` 占位符。 |

缺少 `host`、`from_addr` 或 `to` 时，通知器只记录警告并跳过，绝不会中断处理流程。

### 用法

```toml
[[notifiers]]
notifier_id = "smtp-forward"
provider = "smtp"
enabled = true
minimum_urgency = "urgent"

[notifiers.options]
host = "smtp.gmail.com"
port = 587
use_tls = true
username = "me@gmail.com"
password = "${SMTP_APP_PASSWORD}"
from_addr = "me@gmail.com"
to = ["team@example.com", "me@example.com"]
```

### 排查

- **Gmail/Outlook 拒绝登录** —— 请使用应用专用密码而非账户密码，并放进环境变量。
- **465 端口超时** —— 465 是隐式 SSL，请设置 `use_tls = false`。
- **提醒形成回环** —— 切勿把 `to` 指向 MailFlow 自己在轮询的邮箱，否则每条提醒
  又会变成一封需要分类的新邮件。

### 依赖

仅使用标准库（`smtplib`、`email`）。

### 协议

MIT —— 欢迎贡献。

---

Metadata: [`plugin.json`](plugin.json) · Marketplace: [https://github.com/Kingcxp/mailflow-repo/tree/main/notifier/mailflow-notify-smtp](https://github.com/Kingcxp/mailflow-repo/tree/main/notifier/mailflow-notify-smtp)
