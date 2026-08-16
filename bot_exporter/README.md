# Bot exporters

Plugins that turn a configured MailFlow instance into a plugin for a
chatbot framework (NoneBot, AstrBot, or any framework you add). The TUI
export wizard, the `mailflow export` command and the make targets all load
these through the plugin registry.

| Plugin | Description |
|---|---|
| [mailflow-export-nonebot](mailflow-export-nonebot/) | Exports a configured MailFlow instance as a NoneBot2 plugin |
| [mailflow-export-astrbot](mailflow-export-astrbot/) | Exports a configured MailFlow instance as an AstrBot plugin |

### Adding a plugin

Create a folder `bot_exporter/<plugin-id>/` with `plugin.json` and the plugin source, then open a pull request. The PR workflow validates it automatically.

See [docs/02-categories.md](../docs/02-categories.md) for the contract and [docs/bot-exporter.md](../docs/bot-exporter.md) for the bot-exporter capability guide.
