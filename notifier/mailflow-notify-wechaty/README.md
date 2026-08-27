<!-- Generated from plugin.json by tools/gen_plugin_readmes.py. Edit plugin.json. -->

## WeChaty Gateway Notifier

Delivers MailFlow alerts to WeChat contacts and group rooms through a
small HTTP gateway in front of [WeChaty](https://github.com/wechaty/wechaty).

### Options

| Option | Required | Description |
|---|---|---|
| `gateway_url` | yes | Gateway root implementing `POST /send` + `GET /health` |
| `token` | no | Bearer token forwarded to the gateway |
| `targets` | yes | List of `contact:<name>` / `room:<topic>` recipients |

### Notes

- WeChat login (QR scanning) is performed by the WeChaty puppet runtime;
  the gateway exposes health for MailFlow to verify the session.

---

<!-- zh-CN -->

## WeChaty 网关通知器

通过 [WeChaty](https://github.com/wechaty/wechaty) 前面的小型 HTTP 网关，把 MailFlow 提醒推送到微信联系人与群聊。

### 配置项

| 选项 | 必填 | 说明 |
|---|---|---|
| `gateway_url` | 是 | 网关根地址，需实现 `POST /send` 与 `GET /health` |
| `token` | 否 | 转发给网关的 Bearer 令牌 |
| `targets` | 是 | 接收人列表：`contact:<名称>` / `room:<话题>` |

### 说明

- 微信登录（扫码）由 WeChaty 的运行时完成；网关暴露健康检查接口供 MailFlow 验证会话。
- **登录必须走平板协议**（如 WeChatFerry / PaPad），官方 puppet-wechat 网页协议已失效且有封号风险；请使用小号并自行评估风险。

---

Metadata: [`plugin.json`](plugin.json) · Marketplace: [https://github.com/Kingcxp/mailflow-repo/tree/main/notifier/mailflow-notify-wechaty](https://github.com/Kingcxp/mailflow-repo/tree/main/notifier/mailflow-notify-wechaty)
