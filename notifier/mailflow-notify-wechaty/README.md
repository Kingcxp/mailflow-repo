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

Metadata: [`plugin.json`](plugin.json) · Marketplace: [https://github.com/Kingcxp/mailflow-repo/tree/main/notifier/mailflow-notify-wechaty](https://github.com/Kingcxp/mailflow-repo/tree/main/notifier/mailflow-notify-wechaty)
