# Notifiers

Channels that deliver computed analyses and reminders: webhook, ntfy, SMTP…

| Plugin | Description |
|---|---|
| [mailflow-notify-ntfy](mailflow-notify-ntfy/) | Push mail alerts to any ntfy.sh topic (or self-hosted ntfy server) |
| [mailflow-notify-smtp](mailflow-notify-smtp/) | Forward important mail alerts as emails via any SMTP server |
| [mailflow-notify-webhook](mailflow-notify-webhook/) | POSTs computed mail analyses and reminders to any HTTP webhook |

### Adding a plugin

Create a folder `notifier/<plugin-id>/` with `plugin.json` and the plugin source, then open a pull request. The PR workflow validates it automatically.

See [docs/02-categories.md](../docs/02-categories.md) for the contract and [docs/00-getting-started.md](../docs/00-getting-started.md) for the full guide.
