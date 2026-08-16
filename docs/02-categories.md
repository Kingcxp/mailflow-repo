# Categories and contracts

A category is a folder at the repository root, and every plugin belongs to
exactly one category. Categories mirror the component kinds MailFlow can
load, so each category has one contract and one registration call.

| Category folder | Component kind | Registration | Guide |
|---|---|---|---|
| `mail_source/` | `MAIL_SOURCE` | `registrar.add_source(id, factory)` | [mail-source.md](mail-source.md) |
| `processor/` | `MAIL_PROCESSOR` | `registrar.add_processor(id, factory)` | [processor.md](processor.md) |
| `llm_backend/` | `LLM_BACKEND` | `registrar.add_llm(id, factory)` | [llm-backend.md](llm-backend.md) |
| `notifier/` | `NOTIFIER` | `registrar.add_notifier(id, factory)` | [notifier.md](notifier.md) |
| `storage/` | `STORAGE` | `registrar.add_storage(id, factory)` | [storage.md](storage.md) |
| `bot_exporter/` | `BOT_EXPORTER` | `registrar.add_bot_exporter(id, factory)` | [bot-exporter.md](bot-exporter.md) |

## Plugin anatomy (all categories)

A plugin is a pip distribution with one entry point in the `mailflow.plugins`
group, pointing at an object that implements two hooks:

```python
from mailflow.domain import ComponentKind
from mailflow.plugins import PluginInfo
from mailflow.registry import PluginRegistrar

PLUGIN_INFO = PluginInfo(
    plugin_id="mailflow-my-plugin",
    name="My Plugin",
    version="0.1.0",
    description="one-line summary",
    kinds=[ComponentKind.NOTIFIER],          # what the plugin provides
)


class MyPlugin:
    def mailflow_plugin_info(self) -> PluginInfo:
        return PLUGIN_INFO

    def mailflow_register(self, registrar: PluginRegistrar, config) -> None:
        registrar.add_notifier("my-channel", MyNotifier)   # category-specific


plugin = MyPlugin()
```

`pyproject.toml` maps the id to that object:

```toml
[project.entry-points."mailflow.plugins"]
mailflow-my-plugin = "mailflow_my_plugin.plugin:plugin"
```

## Config access

`mailflow_register(registrar, config)` receives the global `MailFlowConfig`.
Component-specific settings live in the config's `options` dicts:

```python
from mailflow.config import NotifierConfig

def mailflow_register(self, registrar, config):
    notifier_config = next(
        (n for n in config.notifiers if n.notifier_id == "my-channel"),
        None,
    )
    registrar.add_notifier("my-channel", lambda: MyNotifier(notifier_config))
```

The generated template reads the same way — component factories receive the
matching config section (e.g. `NotifierConfig`, `ProcessorConfig`,
`LLMConfig`). When the section is missing, construct with `None` and degrade
gracefully (log and skip) rather than crash the pipeline.

## Dependencies

- `mailflow-core` is available to every plugin (pulled in automatically via
  `dependencies = ["mailflow-core"]`).
- Prefer the standard library. The marketplace validates with the current
  published `mailflow-core`, so plugins cannot depend on unreleased core
  features.
- Pin no versions unless you have a hard requirement; the workflow installs
  in a fresh environment each run.
