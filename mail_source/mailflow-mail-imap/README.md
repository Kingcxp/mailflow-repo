<!-- Generated from plugin.json by tools/gen_plugin_readmes.py. Edit plugin.json. -->

## IMAP Mail Source

Receives mail over IMAP and sends confirmed replies over SMTP. Component ID:
`imap`. Presets cover QQ, 163, Gmail and Outlook; explicit host settings override
a preset for other servers.

### Options

Configure these under `[accounts.options]`:

| Option | Default | Meaning |
| --- | --- | --- |
| `preset` | empty | `qq`, `163`, `gmail` or `outlook` |
| `imap_host` / `imap_port` | preset / `993` | Receive endpoint; host is required without a preset |
| `imap_ssl` / `imap_folder` | `true` / `INBOX` | Implicit TLS and mailbox folder |
| `smtp_host` / `smtp_port` | preset / `465` | Send endpoint, required for replies |
| `smtp_ssl` | port is 465 | Implicit TLS when true, STARTTLS otherwise |
| `username` | account email | Login name |
| `password` | empty | Required credential; prefer an environment placeholder |
| `interval_seconds` | `300` | Poll interval |
| `limit` | `20` | Recent messages read on the first poll |

```toml
[[accounts]]
account_id = "qq-main"
provider = "imap"
email = "me@qq.com"

[accounts.options]
preset = "qq"
password = "${QQ_AUTH_CODE}"
```

For a generic server, replace `preset` with its `imap_host`, `smtp_host` and
ports/TLS settings. Use the credentials required by that mailbox service.

### Receive, history and retry

The first poll reads the newest `limit` messages. Later polls use incremental
UIDs. Progress advances only after successful runtime handoff; rejected messages
remain retryable, and a later failure does not discard earlier accepted mail.

Identity includes the provider/account scope and message identity. The same mail
retried within one account is deduplicated; equal Message-ID values in different
accounts remain separate. Keep account IDs stable.

The history browser lets you select older mail for analysis without changing
live receive progress. MIME parsing preserves text/HTML, attachment metadata and
bytes needed by the optional OCR stage. Extracted image text is searchable.

If login fails, check the mailbox's IMAP access and configured credentials. If
nothing arrives, check the selected folder, enabled account and first-poll limit;
use history browsing to import older messages. Reconnecting or restarting may
revisit mail, but stored mail in the same account remains deduplicated.

---

<!-- zh-CN -->

## IMAP 邮件源

通过 IMAP 收信，通过 SMTP 发送已确认的回复，组件标识为 `imap`。
内置 QQ、163、Gmail 和 Outlook 预设；自定义主机配置可以覆盖预设。

### 配置项

以下选项放在 `[accounts.options]`：

| 选项 | 默认值 | 说明 |
| --- | --- | --- |
| `preset` | 空 | `qq`、`163`、`gmail` 或 `outlook` |
| `imap_host` / `imap_port` | 预设 / `993` | 收信地址；未用预设时必须填写主机 |
| `imap_ssl` / `imap_folder` | `true` / `INBOX` | 隐式 TLS 和邮箱文件夹 |
| `smtp_host` / `smtp_port` | 预设 / `465` | 回复所需的发信地址 |
| `smtp_ssl` | 端口为 465 | 为真时使用隐式 TLS，否则使用 STARTTLS |
| `username` | 账户邮箱 | 登录名 |
| `password` | 空 | 必填凭据，建议使用环境变量占位符 |
| `interval_seconds` | `300` | 轮询间隔秒数 |
| `limit` | `20` | 首次读取的最近邮件数 |

```toml
[[accounts]]
account_id = "qq-main"
provider = "imap"
email = "me@qq.com"

[accounts.options]
preset = "qq"
password = "${QQ_AUTH_CODE}"
```

通用服务器可用 `imap_host`、`smtp_host` 及端口和 TLS 选项替代 `preset`，
凭据以对应邮箱服务的要求为准。

### 接收、历史与重试

首次读取最近的 `limit` 封邮件，之后按 UID 增量读取。只有运行时成功接收邮件后
才推进进度；交付失败的邮件可以重试，后续失败不会丢掉之前已经接收的邮件。

邮件标识包含来源、账户和消息标识。同一账户内重试不会重复入库，不同账户即使
具有相同的 Message-ID 也分别保存。请保持账户标识稳定。

历史浏览可以选择旧邮件进行分析，不改变实时接收进度。MIME 解析保留正文、HTML、
附件信息及图片识别所需字节；识别出的图片文字可参与搜索。

登录失败时检查邮箱的 IMAP 设置和凭据。收不到邮件时检查文件夹、账户开关和首次
读取数量，较早邮件可从历史浏览导入。重连或重启可能再次读取邮件，但同一账户中
已经保存的邮件不会重复入库。

---

Metadata: [`plugin.json`](plugin.json) · Marketplace: [https://github.com/Kingcxp/mailflow-repo/tree/main/mail_source/mailflow-mail-imap](https://github.com/Kingcxp/mailflow-repo/tree/main/mail_source/mailflow-mail-imap)
