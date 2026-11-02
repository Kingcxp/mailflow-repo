# MailFlow Plugin Repository

Marketplace plugins for [MailFlow](https://github.com/Kingcxp/mailflow).
Each plugin has its own source, package metadata and bilingual usage instructions.

## Browse

| Category | Contents |
| --- | --- |
| [Mail sources](mail_source) | Fake mail, IMAP, Gmail, Outlook and RSS |
| [Processors](processor) | Filtering, blocklists, archiving and rule templates |
| [LLM backends](llm_backend) | Model transports and provider presets |
| [Notifiers](notifier) | Console, email, webhooks and chat-platform delivery |
| [Storage](storage) | SQLite persistence |
| [Framework exporters](bot_exporter) | NoneBot and AstrBot hosts |
| [LLM enhancers](llm_enhancer) | Extension category for analysis hooks |
| [Gateways](gateway) | Extension category for managed chat runtimes |

The root `index.json` lists categories; each `INDEX.json` supports HTTP mirrors.
These files are used by marketplace discovery. A plugin's `plugin.json` supplies
its in-app description, and its generated `README.md` presents the same content
on GitHub. Edit metadata first, then regenerate the README.

## Use a plugin

In MailFlow's command shell:

```text
plugin repo add mailflow-repo https://github.com/Kingcxp/mailflow-repo
plugin market list
plugin market show mailflow-notify-ntfy
plugin install mailflow-notify-ntfy
```

Or run a shared command from the CLI:

```bash
uv run mailflow command "plugin market list" -c configs/local.toml
```

The TUI Market tab provides the same operations. Follow the plugin's configuration
instructions and the installation result's restart requirement. Plugin management
requires administrator access.

## Develop and publish

| Need | Reference |
| --- | --- |
| Create a plugin and choose its folder | [Getting started](docs/00-getting-started.md) |
| Describe it and maintain both languages | [Metadata](docs/01-marketplace-metadata.md) |
| Validate and regenerate READMEs | [Validation](docs/06-validation.md) |
| Implement a component | [Canonical plugin guide](https://github.com/Kingcxp/mailflow/blob/main/docs/plugin-development/overview.md) |

The main repository's `mailflow-core` contracts are the interface source of
truth. Shared plugin implementations must stay aligned across both repositories;
this repository documents marketplace packaging rather than a second API.

License: MIT.
