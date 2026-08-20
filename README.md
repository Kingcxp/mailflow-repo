# MailFlow Plugin Repository

[![validate-plugins](https://github.com/Kingcxp/mailflow-repo/actions/workflows/validate-plugins.yml/badge.svg)](https://github.com/Kingcxp/mailflow-repo/actions/workflows/validate-plugins.yml)

The official plugin marketplace for [MailFlow](https://github.com/Kingcxp/mailflow).
Every plugin is a folder under a category folder — adding a plugin is one
pull request that never touches anyone else's files.

## Browse the catalog

| Category | Plugins |
|---|---|
| [Mail sources](mail_source/) | [mailflow-mail-rss](mail_source/mailflow-mail-rss/) — RSS/Atom → inbox · [mailflow-mail-imap](mail_source/mailflow-mail-imap/) — IMAP/SMTP with QQ/163/Outlook/Gmail presets |
| [Processors](processor/) | [mailflow-processor-blocklist](processor/mailflow-processor-blocklist/) — sender/domain blocklist |
| [LLM backends](llm_backend/) | [mailflow-llm-anthropic](llm_backend/mailflow-llm-anthropic/) — Anthropic Messages API (Claude) |
| [Notifiers](notifier/) | [mailflow-notify-webhook](notifier/mailflow-notify-webhook/) · [mailflow-notify-ntfy](notifier/mailflow-notify-ntfy/) · [mailflow-notify-smtp](notifier/mailflow-notify-smtp/) · [mailflow-notify-telegram](notifier/mailflow-notify-telegram/) |
| [Storage backends](storage/) | _yours could be the first_ |
| [LLM enhancers](llm_enhancer/) | _yours could be the first_ — bounded customization of the built-in LLM analysis (system prompt, extra messages, post-processing) |
| [Bot exporters](bot_exporter/) | [mailflow-export-nonebot](bot_exporter/mailflow-export-nonebot/) — NoneBot2 plugin · [mailflow-export-astrbot](bot_exporter/mailflow-export-astrbot/) — AstrBot plugin |

Each category folder has a README listing its plugins and an `INDEX.json`
that generic HTTP mirrors use. Each plugin folder contains `plugin.json`
(marketplace metadata, including the markdown readme MailFlow renders), a
`README.md` **generated** from it by `tools/gen_plugin_readmes.py`, and the
plugin source. Edit `plugin.json`; CI fails when the two disagree.

## Using the marketplace

```bash
uv run mailflow plugin repo add mailflow-repo https://github.com/Kingcxp/mailflow-repo
uv run mailflow plugin market list
uv run mailflow plugin market show mailflow-notify-ntfy
uv run mailflow plugin install mailflow-notify-ntfy   # restart to load
```

`market show` renders the plugin readme with markdown effects — **bold**,
~~strike~~, `<span style="color:#ff5500">colors</span>` — and shows the
translation matching your app language when the plugin ships one.

## Repository layout

```
docs/            ← plugin development documentation (start here)
├── 00-getting-started.md
├── 01-marketplace-metadata.md
├── 02-categories.md
├── mail-source.md · processor.md · llm-backend.md · llm-enhancer.md · notifier.md · storage.md · bot-exporter.md
├── 05-localization.md
└── 06-validation.md
index.json       ← the category list (nothing else — one file, rarely touched)
mail_source/     ← category folder; one subfolder per plugin
processor/
llm_backend/
llm_enhancer/
notifier/
storage/
bot_exporter/
tools/           ← validation script used by CI
.github/workflows/validate-plugins.yml
```

## Writing a plugin

1. Use the **TUI wizard** (Market tab → New): pick a folder, optionally
   create a subfolder, choose the template category, and MailFlow generates a
   complete, loadable template. See
   [docs/00-getting-started.md](docs/00-getting-started.md).
2. Implement the stub and fill in `plugin.json`
   ([reference](docs/01-marketplace-metadata.md), including multi-language
   `descriptions` / `readmes`).
3. Open a pull request — CI validates **exactly the plugins you changed**
   (metadata consistency, install, entry-point load, component registration,
   and a real `process()` run for processors). Unchanged plugins are never
   re-validated. Details: [docs/06-validation.md](docs/06-validation.md).

```bash
# validate locally before pushing
python tools/validate_plugin.py notifier/mailflow-notify-slack
```

## Development documentation

| Guide | Contents |
|---|---|
| [Getting started](docs/00-getting-started.md) | wizard, layout, PR flow, local testing |
| [Marketplace metadata](docs/01-marketplace-metadata.md) | `plugin.json` reference + CI rules |
| [Categories](docs/02-categories.md) | contracts, registration, config access |
| [Mail sources](docs/mail-source.md) | `MailSource` contract + reference plugin |
| [Processors](docs/processor.md) | `MailProcessor` + `ProcessorResult` |
| [LLM backends](docs/llm-backend.md) | `LLMBackend` + `LLMCompletion` |
| [Notifiers](docs/notifier.md) | `Notifier` + `MailRecord` payload |
| [Storage backends](docs/storage.md) | full `StorageBackend` API |
| [Bot exporters](docs/bot-exporter.md) | `BotExportContext`/`BotExportResult`, framework ids |
| [Localization](docs/05-localization.md) | translated descriptions/readmes |
| [Validation](docs/06-validation.md) | what CI checks and why |
