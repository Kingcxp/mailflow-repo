<!-- Generated from plugin.json by tools/gen_plugin_readmes.py. Edit plugin.json. -->

## OneBot v11 (QQ) Notifier

Pushes MailFlow mail alerts to QQ users and group chats through an
[OneBot v11](https://github.com/botuniverse/onebot-11) HTTP server such as
[NapCat](https://github.com/NapNeko/NapCatQQ) or go-cqhttp.

### Options

| Option | Required | Description |
|---|---|---|
| `http_url` | yes | OneBot HTTP server root, e.g. `http://127.0.0.1:3000` |
| `access_token` | no | Shared secret sent as `Authorization: Bearer …` |
| `targets` | yes | List of `user:<qq>` / `group:<group_id>` recipients |

### Notes

- This notifier sends through the OneBot HTTP API. Use MailFlow's guided
  notification setup for a managed gateway, or log in through your external server.

---

<!-- zh-CN -->

## OneBot v11（QQ）通知器

通过 [OneBot v11](https://github.com/botuniverse/onebot-11) HTTP 服务器（如 [NapCat](https://github.com/NapNeko/NapCatQQ) 或 go-cqhttp）把 MailFlow 邮件提醒推送到 QQ 用户与群聊。

### 配置项

| 选项 | 必填 | 说明 |
|---|---|---|
| `http_url` | 是 | OneBot HTTP 服务器根地址，如 `http://127.0.0.1:3000` |
| `access_token` | 否 | 共享密钥，以 `Authorization: Bearer …` 发送 |
| `targets` | 是 | 接收人列表：`user:<QQ号>` / `group:<群号>` |

### 说明

- 此通知器通过 OneBot HTTP 接口发送消息。托管网关可在 MailFlow 通知向导中登录，
  外部服务器则按其自身方式登录。

---

Metadata: [`plugin.json`](plugin.json) · Marketplace: [https://github.com/Kingcxp/mailflow-repo/tree/main/notifier/mailflow-notify-onebot](https://github.com/Kingcxp/mailflow-repo/tree/main/notifier/mailflow-notify-onebot)
