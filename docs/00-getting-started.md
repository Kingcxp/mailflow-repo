# Getting started

Implement against the main repository's
[plugin guide](https://github.com/Kingcxp/mailflow/blob/main/docs/plugin-development/overview.md)
and [core contracts](https://github.com/Kingcxp/mailflow/blob/main/packages/mailflow-core/src/mailflow/contracts.py).
The same interfaces cover bundled and marketplace plugins; category-specific
copies are intentionally not maintained here.

## Create a plugin

Use MailFlow's TUI Market → New wizard to choose a category and generate a
loadable package. Put the result in `<category>/<plugin-id>/` in this repository.
The categories are listed in [index.json](../index.json).

```text
notifier/mailflow-notify-example/
    plugin.json
    README.md
    pyproject.toml
    src/mailflow_notify_example/
        __init__.py
        plugin.py
```

`plugin.json` defines marketplace display/install metadata. `pyproject.toml`
defines the distribution, runtime dependencies and `mailflow.plugins` entry
point. `plugin.py` implements registration and the component. The generated
README is derived from the English and translated metadata, so do not edit it
independently.

Choose a unique plugin ID matching the folder, distribution name and entry-point
name. The registered component ID is the configuration `provider`; it may be
shorter. Declare every runtime dependency, including `mailflow-core`.

## Describe, validate and submit

Write concise English and Chinese descriptions, required options, a working
configuration example and relevant failure/recovery guidance. See the
[metadata reference](01-marketplace-metadata.md). Keep placeholders rather than
real credentials, and describe current behavior rather than future plans.

```bash
python tools/gen_plugin_readmes.py
python tools/gen_plugin_readmes.py --check
python tools/validate_plugin.py notifier/mailflow-notify-example --offline --core ../mailflow/packages/mailflow-core
```

Run offline validation using the paired MailFlow development interpreter; the
[validation guide](06-validation.md) explains dependency-install checks and CI.
For manual local installation, install the plugin into MailFlow's Python
environment and use `plugin list` in its shell, then restart when requested.

A pull request normally changes only the plugin folder. Update the category's
`INDEX.json` when adding or removing a plugin so HTTP mirrors stay in sync.
If an implementation is also bundled in the main repository, update its paired
copy and validate both. Avoid committing environments, generated exports,
credentials, caches or diagnostic reports.
