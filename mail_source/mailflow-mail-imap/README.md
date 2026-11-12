<!-- Generated from plugin.json by tools/gen_plugin_readmes.py. Edit plugin.json. -->

# IMAP mail source

Receives IMAP mail and sends through SMTP. Component ID: `imap`. Presets are
`qq`, `163`, `gmail` and `outlook`; explicit hosts override the preset.

```toml
[[accounts]]
account_id = "personal"
provider = "imap"
email = "you@example.com"
state_sync = false

[accounts.options]
imap_host = "imap.example.com"
smtp_host = "smtp.example.com"
password = "${MAIL_PASSWORD}"
initial_sync = "new"
catch_up_missed = false
```

| Option | Default / purpose |
| --- | --- |
| `preset` | Optional server preset; otherwise set `imap_host` and the needed send host |
| `username` / `password` | Account email / required mailbox credential |
| `imap_port`, `imap_ssl`, `imap_folder` | `993`, `true`, `INBOX` |
| `smtp_port`, `smtp_ssl` | `465`; implicit TLS on 465, STARTTLS otherwise unless overridden |
| `initial_sync`, `initial_days` | `new`; `recent` imports 30 days by default, `all` explicitly imports history |
| `catch_up_missed`, `catch_up_summary` | `false` / `true`; optional catch-up from a valid saved cursor, normally with a summary |
| `include_past_actions` | `false`; opt in to past tasks from imported mail |
| `interval_seconds`, `limit` | `300` / `20`; polling interval and batch size, not implicit startup history |
| `archive_folder`, `trash_folder`, `sent_folder` | Optional overrides for detected source folders |

The default first connection receives only new mail. History browsing is separate;
restarts do not resume abandoned analysis. A valid account/folder-scoped UID and
UIDVALIDITY cursor is required for missed-mail catch-up; invalid progress asks for
an explicit resync range. Accepted messages advance progress only after handoff.

Account IDs isolate mail identity. MIME attachment bytes survive extraction, and
attachments can be fetched on demand independently of OCR. Receiving and sending
must be checked separately. Configured credentials must be accepted by the mail
service; presets do not implement native OAuth.

Optional account `state_sync` enables supported read/star/archive synchronization.
Source trash/restore requires confirmation and a reliable move capability; unknown
results are checked before retry. Local permanent deletion never expunges source
mail. See the [operation guide](https://github.com/Kingcxp/mailflow/blob/dev/docs/configuration/overview.md).

---

<!-- zh-CN -->

# IMAP 邮件源

通过 IMAP 收信、SMTP 发信，组件标识为 `imap`。支持 QQ、163、Gmail、Outlook
预设，也可填写实际服务器地址；显式主机设置优先于预设。

```toml
[[accounts]]
account_id = "personal"
provider = "imap"
email = "you@example.com"
state_sync = false

[accounts.options]
imap_host = "imap.example.com"
smtp_host = "smtp.example.com"
password = "${MAIL_PASSWORD}"
initial_sync = "new"
catch_up_missed = false
```

| 选项 | 默认值或用途 |
| --- | --- |
| `preset` | 可选预设；不用预设时填写收件及所需发件主机 |
| `username` / `password` | 默认账户邮箱／邮箱服务接受的凭据 |
| `imap_port`、`imap_ssl`、`imap_folder` | `993`、`true`、`INBOX` |
| `smtp_port`、`smtp_ssl` | 默认 `465`；465 默认隐式 TLS，其他端口默认 STARTTLS，可覆盖 |
| `initial_sync`、`initial_days` | 默认 `new`；`recent` 默认导入 30 天，`all` 明确导入历史 |
| `catch_up_missed`、`catch_up_summary` | 默认关闭补收、开启补收汇总，补收依赖有效游标 |
| `include_past_actions` | 默认不提取导入邮件的过期待办 |
| `interval_seconds`、`limit` | 默认 `300` 秒／每批 `20` 封，不表示启动自动导入最近邮件 |
| `archive_folder`、`trash_folder`、`sent_folder` | 可覆盖自动识别的归档、回收站和已发送目录 |

首次默认只接收新邮件，历史浏览单独进行；重启不恢复已取消的分析。
补收需要账户、文件夹及 UIDVALIDITY 匹配的游标，失效时要求主动选择重新同步范围。
成功交给运行时后才推进进度，账户标识参与去重，请保持稳定。

附件字节保留到识别完成，可按需获取附件，下载与 OCR 独立。
收件与发件分别检查；预设不提供原生 OAuth，也不绕过邮箱访问限制。
账户 `state_sync` 可开启受支持的已读、收藏、归档联动；原邮箱删除与恢复需确认，
未知结果先核对。永久清除仅作用于本地，不清空原邮箱其他邮件。

---

[Catalog](../../README.md) · [Metadata](plugin.json) · [Plugin page](https://github.com/Kingcxp/mailflow-repo/tree/main/mail_source/mailflow-mail-imap)
