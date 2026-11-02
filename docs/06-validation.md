# Validation

Both repositories use the main checkout's `mailflow_testkit.plugin_smoke`.
Validation checks metadata, entry points, factory/method signatures, actual
arguments and return values, capabilities and simulated runtime behavior.
Instantiating a component alone does not prove compatibility.

## Offline checks

From this repository, use the paired MailFlow development interpreter. For a
standard environment layout, replace `python` below with
`../mailflow/.venv/Scripts/python.exe` on Windows or
`../mailflow/.venv/bin/python` on Linux/macOS.

```bash
python tools/gen_plugin_readmes.py --check
python -m unittest discover -s tests -q
python tools/validate_plugin.py --all --offline --core ../mailflow/packages/mailflow-core
```

A single folder may replace `--all`, for example
`notifier/mailflow-notify-slack`. Offline mode imports paired core/testkit sources
and uses the existing environment; it performs no installation or downloads.
HTTP, mail and subprocess I/O are simulated. Samples cover source handoff retry,
LLM `temperature`/`options`/`tools`, processor outputs, temporary SQLite storage,
notifier failure and export output. Gateway contracts are checked without
launching platform processes.

## Dependency installation and CI

Omit `--offline` to install core, testkit and the plugin with declared dependencies
into a disposable environment, then run `pip check` and the shared samples.
`--core` selects core and testkit from one local checkout; without it, the script
uses the main repository's Git sources. This mode needs access to dependency
sources and is separate from offline verification.

The [workflow](../.github/workflows/validate-plugins.yml) always checks generated
READMEs and validator tests. Pull requests validate changed plugin folders;
shared validator/workflow changes validate every plugin. Documentation-only
changes need no component execution. Pushes to `main` validate all plugins.
Failures identify the plugin, component and cause.

Metadata checks include folder/category, package/version, entry-point name,
source URL and usage text. Runtime metadata and declared capabilities must
match registration. Missing dependencies or rejected parameters must fail with
a concrete reason, rather than silently removing the plugin from discovery.

Regenerate usage documents after editing `plugin.json`:

```bash
python tools/gen_plugin_readmes.py
python tools/gen_plugin_readmes.py --check
```

The generator itself uses only the standard library. Do not hand-edit generated
READMEs, connect live services in tests or commit validation caches/reports.
