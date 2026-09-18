<!-- Generated from plugin.json by tools/gen_plugin_readmes.py. Edit plugin.json. -->

## WhatsApp Notifier (auto-deploy)

Pushes MailFlow mail alerts into WhatsApp chats and lets those chats run
MailFlow commands, through a local Node bridge built on
[Baileys](https://github.com/WhiskeySockets/Baileys) (the WhatsApp Web
multi-device protocol).

### Guided setup

Add the notifier in the Notifications tab and press Next: MailFlow installs
the bridge (npm), starts it, and shows the pairing QR in the terminal. Scan it
once from *WhatsApp → Linked devices*; the session is kept on disk, so later
restarts reconnect without scanning again.

### Options

| Option | Required | Description |
|---|---|---|
| `gateway_url` | yes | Local bridge root, written by the guided setup |
| `targets` | yes | Recipients: `group:<id>` / `user:<number>` |
| `admins` | for commands | WhatsApp ids allowed to run chat commands |
| `gateway` | auto | Marks the entry as auto-deployed |

### Notes

- Requires Node 20+ and npm on the host; nothing else is downloaded.
- Delivery is one message per target; a chat that fails does not stop the rest.
- Chat commands arrive through the same bridge and are answered in-chat.

---

<!-- zh-CN -->

## WhatsApp 通知器（自动部署）

通过基于 [Baileys](https://github.com/WhiskeySockets/Baileys)（WhatsApp Web 多设备协议）的本地 Node 桥，
把 MailFlow 邮件提醒推送到 WhatsApp 会话，并让这些会话可以直接运行 MailFlow 命令。

### 引导式部署

在「通知」页添加本通知器并点击「下一步」：MailFlow 会安装桥（npm）、启动它，并在终端里显示配对二维码。
用手机打开 *WhatsApp → 已关联的设备* 扫一次即可；会话会保存在磁盘上，之后重启无需再次扫码。

### 配置项

| 选项 | 必填 | 说明 |
|---|---|---|
| `gateway_url` | 是 | 本地桥地址，由引导式部署写入 |
| `targets` | 是 | 接收人:`group:<群ID>` / `user:<号码>` |
| `admins` | 使用命令时必填 | 允许执行聊天命令的 WhatsApp ID |
| `gateway` | 自动 | 标记该条目为自动部署 |

### 说明

- 需要宿主机有 Node 20+ 与 npm，除此之外不下载任何东西。
- 每个目标一条消息；某个会话发送失败不会影响其余目标。
- 聊天命令通过同一个桥进入，并在会话内回复。

---

Metadata: [`plugin.json`](plugin.json) · Marketplace: [https://github.com/Kingcxp/mailflow-repo/tree/main/notifier/mailflow-notify-whatsapp](https://github.com/Kingcxp/mailflow-repo/tree/main/notifier/mailflow-notify-whatsapp)
