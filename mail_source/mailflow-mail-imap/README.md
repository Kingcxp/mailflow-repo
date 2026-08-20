<!-- Generated from plugin.json by tools/gen_plugin_readmes.py. Edit plugin.json. -->

## IMAP Mail Source

The built-in IMAP/SMTP mail source: polls a mailbox over IMAP, normalizes every
message into MailFlow's provider-independent form, and sends confirmed replies
over SMTP. It ships with every MailFlow install, so there is nothing to install
— just add an account.

Registers the mail source component id `imap`.

### Provider presets

Set `options.preset` to fill in hosts, ports and TLS modes:

| Preset | IMAP | SMTP | Password to use |
| ------ | ---- | ---- | --------------- |
| `qq` | imap.qq.com:993 (SSL) | smtp.qq.com:465 (SSL) | authorization code, not the login password |
| `163` | imap.163.com:993 (SSL) | smtp.163.com:465 (SSL) | authorization code |
| `outlook` | outlook.office365.com:993 (SSL) | smtp.office365.com:587 (STARTTLS) | account or app password |
| `gmail` | imap.gmail.com:993 (SSL) | smtp.gmail.com:587 (STARTTLS) | app password (2FA required) |

Any preset field can be overridden, and a generic school or company server
works by setting the hosts directly.

### Options

| Option | Required | Default | Meaning |
| ------ | -------- | ------- | ------- |
| `preset` | no | `""` | `qq`, `163`, `outlook`, `gmail`. |
| `imap_host` / `imap_port` | yes unless preset | — / `993` | IMAP server. |
| `imap_ssl` | no | `true` | Implicit TLS (`IMAP4_SSL`). |
| `imap_folder` | no | `INBOX` | Mailbox to poll. |
| `smtp_host` / `smtp_port` | needed for replies | — / `465` | SMTP server. |
| `smtp_ssl` | no | `port == 465` | `true` = implicit SSL, `false` = STARTTLS. |
| `username` | no | account `email` | Login user. |
| `password` | **yes** | `""` | Login secret — use `${ENV_VAR}`. |
| `interval_seconds` | no | `300` | Seconds between polls. |
| `limit` | no | `20` | How many recent mails the *first* poll ingests. |

### Fetch semantics

- The first poll takes the newest `limit` messages so a decade-old mailbox does
  not flood the pipeline.
- After that the source is incremental by **UID**: only mails with a UID above
  the previous high-water mark are fetched, and the mark only advances once a
  message has actually been parsed — a transient server error retries the same
  UID next poll instead of skipping it.
- Identity is the RFC `Message-ID`, so a mail forwarded into two configured
  accounts is stored once.
- MIME handling decodes encoded-word headers, walks multipart bodies and keeps
  the original text and HTML parts separately.

### Browsing history

This source implements the optional history capability, so the TUI's
**Mailboxes** tab can page through mail that arrived *before* MailFlow was
configured and analyze only the messages you pick. Browsing never disturbs the
live UID water-mark.

### Usage

```toml
[[accounts]]
account_id = "qq-main"
provider = "imap"
email = "me@qq.com"
enabled = true

[accounts.options]
preset = "qq"
username = "me@qq.com"
password = "${QQ_AUTH_CODE}"
interval_seconds = 300
limit = 20
```

Generic server:

```toml
[accounts.options]
imap_host = "mail.university.edu"
imap_port = 993
imap_ssl = true
imap_folder = "INBOX"
smtp_host = "smtp.university.edu"
smtp_port = 587
smtp_ssl = false            # STARTTLS
username = "student123"
password = "${MAIL_PASSWORD}"
```

### Troubleshooting

- **Login rejected on QQ/163** — those providers need an *authorization code*
  generated in the web mail settings, not your account password.
- **Gmail rejects the password** — enable 2FA and create an app password.
- **`no imap_host configured`** — set `preset` or `imap_host`.
- **Nothing new appears** — the UID mark is per process; restarting re-reads
  from the last seen UID, and already-stored mail is skipped by design.

### Requirements

Standard library only (`imaplib`, `smtplib`, `email`).

### License

MIT — contributions welcome.

---

<!-- zh-CN -->

## IMAP 邮件源

内置的 IMAP/SMTP 邮件源：通过 IMAP 轮询邮箱，把每封邮件规范化为 MailFlow 与厂商
无关的结构，并通过 SMTP 发送确认后的回复。它随每个 MailFlow 安装一同提供，无需
安装 —— 直接添加账户即可。

注册的邮件源组件 id 为 `imap`。

### 服务商预设

设置 `options.preset` 即可自动填入主机、端口与 TLS 模式：

| 预设 | IMAP | SMTP | 应使用的密码 |
| ---- | ---- | ---- | ------------ |
| `qq` | imap.qq.com:993（SSL） | smtp.qq.com:465（SSL） | 授权码，而非登录密码 |
| `163` | imap.163.com:993（SSL） | smtp.163.com:465（SSL） | 授权码 |
| `outlook` | outlook.office365.com:993（SSL） | smtp.office365.com:587（STARTTLS） | 账户密码或应用密码 |
| `gmail` | imap.gmail.com:993（SSL） | smtp.gmail.com:587（STARTTLS） | 应用密码（需开启两步验证） |

预设中的任何字段都可以被覆盖；直接填写主机即可对接学校或公司的通用服务器。

### 配置项

| 配置项 | 必填 | 默认值 | 说明 |
| ------ | ---- | ------ | ---- |
| `preset` | 否 | `""` | `qq`、`163`、`outlook`、`gmail`。 |
| `imap_host` / `imap_port` | 未用预设时必填 | — / `993` | IMAP 服务器。 |
| `imap_ssl` | 否 | `true` | 隐式 TLS（`IMAP4_SSL`）。 |
| `imap_folder` | 否 | `INBOX` | 要轮询的邮箱文件夹。 |
| `smtp_host` / `smtp_port` | 需要回复时必填 | — / `465` | SMTP 服务器。 |
| `smtp_ssl` | 否 | `port == 465` | `true` 为隐式 SSL，`false` 为 STARTTLS。 |
| `username` | 否 | 账户的 `email` | 登录用户名。 |
| `password` | **是** | `""` | 登录密码 —— 建议使用 `${环境变量}`。 |
| `interval_seconds` | 否 | `300` | 轮询间隔秒数。 |
| `limit` | 否 | `20` | **首次**轮询摄取多少封最近邮件。 |

### 抓取语义

- 首次轮询只取最新的 `limit` 封邮件，避免十年老邮箱一次性冲垮处理流程。
- 之后按 **UID** 增量抓取：只拉取 UID 高于上次水位线的邮件，且水位线只在邮件真正
  解析成功后才前移 —— 临时的服务器错误会在下次轮询重试同一 UID，而不是跳过它。
- 邮件标识使用 RFC `Message-ID`，因此转发到两个已配置账户的同一封邮件只会存一份。
- MIME 处理会解码 encoded-word 头部、遍历 multipart 结构，并分别保留原始纯文本与
  HTML 部分。

### 浏览历史邮件

该邮件源实现了可选的历史能力，因此 TUI 的**邮箱**标签页可以分页浏览 MailFlow
配置*之前*就已收到的邮件，并只解析你勾选的那些。浏览不会干扰实时抓取的 UID 水位线。

### 用法

```toml
[[accounts]]
account_id = "qq-main"
provider = "imap"
email = "me@qq.com"
enabled = true

[accounts.options]
preset = "qq"
username = "me@qq.com"
password = "${QQ_AUTH_CODE}"
interval_seconds = 300
limit = 20
```

通用服务器：

```toml
[accounts.options]
imap_host = "mail.university.edu"
imap_port = 993
imap_ssl = true
imap_folder = "INBOX"
smtp_host = "smtp.university.edu"
smtp_port = 587
smtp_ssl = false            # STARTTLS
username = "student123"
password = "${MAIL_PASSWORD}"
```

### 排查

- **QQ/163 登录被拒** —— 这些服务商需要在网页邮箱设置中生成的*授权码*，而不是账户
  密码。
- **Gmail 拒绝密码** —— 请开启两步验证并创建应用密码。
- **提示 `no imap_host configured`** —— 请设置 `preset` 或 `imap_host`。
- **收不到新邮件** —— UID 水位线是进程内的；重启后会从最后见过的 UID 继续，已入库
  的邮件按设计会被跳过。

### 依赖

仅使用标准库（`imaplib`、`smtplib`、`email`）。

### 协议

MIT —— 欢迎贡献。

---

Metadata: [`plugin.json`](plugin.json) · Marketplace: [https://github.com/Kingcxp/mailflow-repo/tree/main/mail_source/mailflow-mail-imap](https://github.com/Kingcxp/mailflow-repo/tree/main/mail_source/mailflow-mail-imap)
