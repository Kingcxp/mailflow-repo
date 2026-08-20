# Validation

The pull-request workflow `.github/workflows/validate-plugins.yml` makes sure
every submitted plugin is **legal** (metadata consistent), **loadable**
(entry point imports, info reports) and **runnable** (components instantiate,
processors actually process). It validates only what changed, so unchanged
plugins are never re-tested.

## What CI does

1. **Check the generated READMEs.** `tools/gen_plugin_readmes.py --check`
   fails when a plugin folder's `README.md` no longer matches the `readme`
   in its `plugin.json`. This runs on every pull request, docs-only ones
   included, because it is the cheapest way to catch two texts drifting apart.
2. **Detect changed plugins.** The workflow diffs the PR against `main`,
   collects every changed path, and maps them to plugin folders. Only folders
   with actual changes are validated.
   - A PR that touches no plugin folder (e.g. docs only) is skipped — the
     check passes immediately.
   - A PR that updates an existing plugin re-validates exactly that plugin.
3. **Install `mailflow-core`** (the version this repo pins) into a fresh
   Python environment.
4. **Run `tools/validate_plugin.py <folder>…`** for each changed plugin.

## The script checks

| Check | Failure |
|---|---|
| `plugin.json` exists and parses | invalid metadata |
| `id` equals the folder name | inconsistent identity |
| `categories` is exactly one known category | unknown category |
| `package` matches the `pyproject.toml` name | broken uninstall metadata |
| `source` non-empty | not installable |
| `readme` or `readmes.*` non-empty | undocumented |
| `pip install .` succeeds | broken build |
| entry point loads; `mailflow_plugin_info()` reports id + kinds | not loadable |
| every registered factory instantiates via `build_registry()` | not runnable |
| processors additionally run `process()` on a sample mail | processor broken |

Notifiers and sources are instantiated but not invoked over the network —
delivery is environment-dependent and out of scope for CI; correctness of
registration and construction is what "runnable" means for them.

## Running locally

```bash
python tools/validate_plugin.py notifier/mailflow-notify-slack
# validate everything:
python tools/validate_plugin.py --all
```

`validate_plugin.py` needs a Python environment with `mailflow-core`
importable (create one with `uv venv` + `uv pip install mailflow-core` from
the repo git URL, or use your MailFlow workspace virtualenv).

Regenerate the plugin READMEs after editing any `plugin.json`:

```bash
python tools/gen_plugin_readmes.py          # write
python tools/gen_plugin_readmes.py --check  # what CI runs
```

This one needs no `mailflow-core`: it only reads `plugin.json`.
