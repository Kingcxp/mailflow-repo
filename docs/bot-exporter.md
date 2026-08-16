# Bot exporters

A `bot_exporter` plugin turns a *configured* MailFlow instance into a
plugin for a chatbot framework (NoneBot, AstrBot, ...). This is how
`mailflow export --framework <id>` and the TUI export wizard work: both
load the exporter through the component registry, so adding support for a
new framework is a plugin — never a core change.

## Contract

The plugin registers one factory per framework id:

```python
from mailflow.domain import ComponentKind
from mailflow.plugins import PluginInfo
from mailflow.registry import PluginRegistrar
from mailflow.bot_export import BotExportContext, BotExportResult

PLUGIN_INFO = PluginInfo(
    plugin_id="mailflow-export-mybot",
    name="MyBot Exporter",
    version="0.1.0",
    description="Exports a configured MailFlow instance as a MyBot plugin",
    kinds=[ComponentKind.BOT_EXPORTER],
)


def export_mybot(context: BotExportContext) -> BotExportResult:
    # write the framework plugin package under context.output_dir
    return BotExportResult(
        framework="mybot",
        plugin_name="mybot_plugin_mailflow",
        created=["README.md", "main.py"],
        notes="any notes for the user",
    )


class MyPlugin:
    def mailflow_plugin_info(self) -> PluginInfo:
        return PLUGIN_INFO

    def mailflow_register(self, registrar: PluginRegistrar, config) -> None:
        registrar.add_bot_exporter("mybot", export_mybot)


plugin = MyPlugin()
```

The factory is called with one argument, a `BotExportContext`:

- `config` — the resolved live `MailFlowConfig` (accounts, LLMs, processors,
  notifiers, repositories, ...). Persist it with `mailflow.config.write_config`.
- `plugin_ids` — the enabled plugin ids; the generated plugin should declare
  these (plus `mailflow-core` / `mailflow-bundled`) as dependencies so the
  framework host installs everything the engine needs.
- `output_dir` — the directory to write the plugin package into (created for
  you; write relative paths).
- `version` / `language` — MailFlow version and active language, for
  generated metadata and text.

It must return a `BotExportResult` with the framework id, the generated
plugin name, the relative paths of every file written and optional notes
(shown to the user by the CLI/TUI).

The framework id (`"mybot"` above) is what the user passes to
`mailflow export --framework mybot` and what the TUI export wizard lists.

## Rules for authors

- **Do not require a running service.** The exporter receives the config and
  the registry, never a started MailFlow instance — the export must work
  offline (no mail fetching, no LLM calls).
- **Stay fast and synchronous.** Exporters are invoked from the CLI directly
  and from a TUI worker; plain file I/O is all you need.
- **Flag secrets.** The embedded config is the resolved live configuration.
  Note in `BotExportResult.notes` (and your README) that real tokens should
  be replaced with `${ENV_VAR}` placeholders before the plugin is shared.
- **Declare dependencies explicitly.** The generated plugin must install
  `mailflow-core`, `mailflow-bundled` and every `plugin_ids` package, then
  start the engine with `start_service(config, plugin_manager=create_plugin_manager(config))`
  — the framework plugin is a *host*, not a MailFlow component.
- **No chat commands.** Bot-command surfaces belong to the framework host
  and are out of scope for exporters; generate lifecycle-only plugins.

## Reference implementations

- `bot_exporter/mailflow-export-nonebot/` — NoneBot2 driver startup/shutdown
  hooks + wheel metadata.
- `bot_exporter/mailflow-export-astrbot/` — AstrBot `Star` lifecycle
  (`initialize` / `terminate`) + `metadata.yaml`.

Scaffold your own with the TUI wizard (Market tab → New → Bot exporter) or
`mailflow.plugin_template.scaffold_plugin(..., category="bot_exporter")`.
