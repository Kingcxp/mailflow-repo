# Getting started

This repository is the official MailFlow plugin marketplace. Every plugin
lives in **its own folder under a category folder**, which means a plugin
pull request only ever touches that one folder — no shared index files, no
merge conflicts between contributors.

```
mailflow-repo/
├── README.md                 ← this page, links into docs/
├── index.json                ← only the category list (changed rarely)
├── docs/                     ← plugin development documentation
│   ├── 00-getting-started.md ← you are here
│   ├── 01-marketplace-metadata.md
│   ├── 02-categories.md
│   ├── mail-source.md
│   ├── processor.md
│   ├── llm-backend.md
│   ├── notifier.md
│   ├── storage.md
│   ├── 05-localization.md
│   └── 06-validation.md
├── mail_source/              ← category folder, one subfolder per plugin
│   ├── README.md             ← category overview + plugin list (browser)
│   ├── INDEX.json            ← structured index (generic HTTP servers)
│   └── <plugin-id>/
│       ├── plugin.json       ← marketplace metadata (incl. markdown readme)
│       ├── README.md         ← GENERATED from plugin.json; do not hand-edit
│       ├── pyproject.toml    ← entry point into the plugin
│       └── src/<package>/…
├── processor/
├── llm_backend/
├── llm_enhancer/
├── notifier/
├── storage/
├── bot_exporter/
└── tools/
    ├── validate_plugin.py       ← the script CI runs on pull requests
    └── gen_plugin_readmes.py    ← regenerates every plugin README.md
```

`plugin.json` is the single source of truth for a plugin's description:
MailFlow renders its `readme` (and `readmes.<lang>`) in `plugin market show`
and in the TUI detail view. The folder's `README.md` is derived from it so
GitHub and MailFlow show the same text — after editing `plugin.json`, run:

```bash
python tools/gen_plugin_readmes.py
```

CI runs `--check` and fails the pull request when the two disagree.
```

## 1. Use the scaffolding wizard (recommended)

The MailFlow TUI ships a **new-plugin wizard** that writes a complete,
loadable template for you:

1. Open the **Market** tab and press **New**.
2. In the directory tree, pick the target folder.
3. Tick **Create a new subfolder** and name it (recommended — keeps your
   checkout tidy), or scaffold straight into the selected folder.
4. Enter the plugin id (lowercase letters and dashes, e.g.
   `mailflow-notify-slack`).
5. Pick the **template category** — the generated stub implements exactly
   the contract that category requires.
6. Press **Generate**.

The wizard produces:

```
<target>/
├── plugin.json                 ← metadata (edit author, source, readme)
├── pyproject.toml              ← entry point: "<pkg>.plugin:plugin"
└── src/<package>/
    ├── __init__.py
    └── plugin.py               ← component stub + registration hooks
```

You can also generate a template from the command line:

```bash
python - <<'EOF'
from mailflow.plugin_template import scaffold_plugin
scaffold_plugin("mailflow-notify-slack", "mailflow-notify-slack", "notifier")
EOF
```

## 2. Implement

Open `src/<package>/plugin.py` and replace the `TODO` markers. The template
already registers cleanly, so you can iterate against a running MailFlow.

## 3. Fill in the metadata

Edit `plugin.json` — the reference is in
[docs/01-marketplace-metadata.md](01-marketplace-metadata.md). At minimum set
`author`, `source` (the installable location, usually the git URL of your
fork with a `#subdirectory=` fragment) and rewrite `readme`. Add
`descriptions` / `readmes` translations if your plugin speaks more than one
language — see [docs/05-localization.md](05-localization.md).

## 4. Open a pull request

Push a branch to your fork of this repository and open a PR against `main`.
The pull-request workflow (`.github/workflows/validate-plugins.yml`) detects
**which plugin folders changed** and validates exactly those:

- `plugin.json` is valid and consistent (id matches the folder, categories
  are known, package name matches)
- the plugin installs (`pip install .` against the current `mailflow-core`)
- the entry point loads and reports `mailflow_plugin_info()`
- every registered component instantiates, and processors additionally run
  `process()` on a sample mail

Unchanged plugins are **not** re-validated, so a one-line documentation
change costs seconds, not minutes. See
[docs/06-validation.md](06-validation.md) for details.

## 5. Local testing before the PR

```bash
# from the repository root, with a python env containing mailflow-core:
python tools/validate_plugin.py notifier/mailflow-notify-slack
```

or, if you have the MailFlow workspace checked out:

```bash
uv pip install -e notifier/mailflow-notify-slack
uv run mailflow plugin list   # plugin shows up as loaded
```

## Category contracts

Pick the guide for the category you are implementing:

| Category | Contract | Guide |
|---|---|---|
| `mail_source` | `MailSource` (run / send_reply / close) | [docs/mail-source.md](mail-source.md) |
| `processor` | `MailProcessor` (process → `ProcessorResult`) | [docs/processor.md](processor.md) |
| `llm_backend` | `LLMBackend` (chat → `LLMCompletion`) | [docs/llm-backend.md](llm-backend.md) |
| `notifier` | `Notifier` (notify → `None`) | [docs/notifier.md](notifier.md) |
| `storage` | `StorageBackend` (full persistence API) | [docs/storage.md](storage.md) |
