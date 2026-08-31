# Notifiers

Channels that deliver computed analyses and reminders: chat-platform robots,
webhook, ntfy, SMTP…

| Plugin | Description |
|---|---|
| [mailflow-notify-console](mailflow-notify-console/) | Prints alerts to the console (built-in, dev/demo) |
| [mailflow-notify-dingtalk](mailflow-notify-dingtalk/) | Push mail alerts to a DingTalk group robot webhook (component id: dingtalk) |
| [mailflow-notify-discord](mailflow-notify-discord/) | Push mail alerts to a Discord webhook (component id: discord) |
| [mailflow-notify-feishu](mailflow-notify-feishu/) | Push mail alerts to a Feishu custom-bot webhook (component id: feishu) |
| [mailflow-notify-ntfy](mailflow-notify-ntfy/) | Push mail alerts to any ntfy.sh topic (or self-hosted ntfy server) |
| [mailflow-notify-onebot](mailflow-notify-onebot/) | Push mail alerts to QQ via OneBot v11 HTTP (component id: onebot; gateway: napcat) |
| [mailflow-notify-openclaw-weixin](mailflow-notify-openclaw-weixin/) | Push mail alerts to WeChat via an OpenClaw ClawBot channel (component id: openclaw-weixin) |
| [mailflow-notify-serverchan](mailflow-notify-serverchan/) | Push mail alerts via ServerChan / 方糖 (component id: serverchan) |
| [mailflow-notify-slack](mailflow-notify-slack/) | Push mail alerts to a Slack incoming webhook (component id: slack) |
| [mailflow-notify-smtp](mailflow-notify-smtp/) | Forward important mail alerts as emails via any SMTP server |
| [mailflow-notify-telegram](mailflow-notify-telegram/) | Push mail alerts to a Telegram chat via the Bot API |
| [mailflow-notify-webhook](mailflow-notify-webhook/) | POSTs computed mail analyses and reminders to any HTTP webhook |
| [mailflow-notify-wechaty](mailflow-notify-wechaty/) | Push mail alerts to WeChat via a WeChaty pad/gateway bridge (component id: wechaty; gateway: wechaty) |
| [mailflow-notify-wecom](mailflow-notify-wecom/) | Push mail alerts to a WeCom group-robot webhook (component id: wecom) |

### Adding a plugin

Create a folder `notifier/<plugin-id>/` with `plugin.json` and the plugin source, then open a pull request. The PR workflow validates it automatically.

See [docs/02-categories.md](../docs/02-categories.md) for the contract and [docs/00-getting-started.md](../docs/00-getting-started.md) for the full guide.