# Validation

The pull-request workflow `.github/workflows/validate-plugins.yml` makes sure
every submitted plugin has consistent metadata, loads through its entry point,
and follows the current `mailflow-core` contracts. Both repositories use
`mailflow_testkit.plugin_smoke` for runtime samples with simulated I/O.

## What CI does

1. **Check the generated READMEs.** `tools/gen_plugin_readmes.py --check`
   fails when a plugin folder's `README.md` no longer matches the `readme`
   in its `plugin.json`. This runs on every pull request, docs-only ones
   included, because it is the cheapest way to catch two texts drifting apart.
2. **Detect changed plugins.** The workflow compares the PR with its target
   branch. Plugin edits validate the affected folders; shared validator or
   workflow edits validate all plugins. Documentation-only edits need no plugin
   execution. Pushes to `main` validate all plugins.
3. **Select core and testkit from one main-repository checkout.** For each
   selected plugin, install core, testkit and the plugin together into a disposable
   environment with declared dependencies, then run `pip check`.
4. **Run the shared samples.** Plugin failures name the plugin, component and cause.

## The script checks

| Check | Failure |
|---|---|
| `plugin.json` exists and parses | invalid metadata |
| `id` equals the folder name | inconsistent identity |
| `categories` is exactly one known category | unknown category |
| `package` matches the `pyproject.toml` name | broken uninstall metadata |
| `source` non-empty | not installable |
| `readme` or `readmes.*` non-empty | undocumented |
| declared dependencies install together and `pip check` succeeds | broken build or missing/conflicting dependencies |
| entry point loads; `mailflow_plugin_info()` reports id + kinds | not loadable |
| runtime version and capabilities match metadata | incompatible declaration |
| factories and method signatures match core contracts | incompatible interface |
| LLM routing accepts temperature, options and tools | broken routing/tool support |
| processors, sources, notifiers, storage and exporters return valid sample results | broken runtime behavior |

HTTP, mail transports and subprocess probes are simulated. Uncaught real network
connections or process launches fail validation. Source samples also check rejected
handoff retry; storage uses a temporary database. Gateway installation and startup
are checked through their contracts without launching real runtimes.

## Running locally

```bash
python tools/validate_plugin.py notifier/mailflow-notify-slack --offline --core ../mailflow/packages/mailflow-core
# validate everything:
python tools/validate_plugin.py --all --offline --core ../mailflow/packages/mailflow-core
# use a disposable environment and resolve declared dependencies:
python tools/validate_plugin.py notifier/mailflow-notify-slack --core ../mailflow/packages/mailflow-core
```

Offline mode uses the existing development interpreter and paired core/testkit
sources without installation or downloads. Run it with the MailFlow workspace
interpreter. Without `--offline`, installation happens only in the disposable
environment. If `--core` is omitted, core and testkit use the main repository Git
sources; `--core` selects both packages from one local checkout.

Regenerate the plugin READMEs after editing any `plugin.json`:

```bash
python tools/gen_plugin_readmes.py          # write
python tools/gen_plugin_readmes.py --check  # what CI runs
```

This one needs no `mailflow-core`: it only reads `plugin.json`.
