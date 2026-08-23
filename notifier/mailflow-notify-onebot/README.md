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

- QR login happens in NapCat/go-cqhttp itself; this plugin only sends
  messages over the standard HTTP API.

---

Metadata: [`plugin.json`](plugin.json) · Marketplace: [https://github.com/Kingcxp/mailflow-repo/tree/main/notifier/mailflow-notify-onebot](https://github.com/Kingcxp/mailflow-repo/tree/main/notifier/mailflow-notify-onebot)
