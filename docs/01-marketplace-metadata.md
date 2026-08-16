# Marketplace metadata (`plugin.json`)

Every plugin folder contains one `plugin.json`. This is the single source of
truth for how MailFlow discovers, displays and installs the plugin. There is
no shared index of plugin metadata anywhere in the repository — the root
`index.json` only lists categories.

## Schema

| Field | Type | Required | Meaning |
|---|---|---|---|
| `id` | string | yes | Unique plugin id; must equal the folder name. Lowercase letters, digits and dashes. |
| `name` | string | no | Human-friendly name (falls back to `id`). |
| `version` | string | yes | Semver. |
| `description` | string | yes | One-line summary shown in `market list` / search. |
| `categories` | list[string] | yes | Exactly one of the known categories (see below). |
| `package` | string | yes | The distribution name in `pyproject.toml` (what `pip uninstall` uses). |
| `source` | string | yes* | Installable location. For this repository: `git+https://github.com/Kingcxp/mailflow-repo.git#subdirectory=<category>/<plugin-id>`. For your fork, point `source` at your fork so installs use your code. |
| `entry_point` | string | no | Entry-point group; defaults to `mailflow.plugins`. |
| `author` | string | no | Your name or handle. |
| `license` | string | no | SPDX id; MIT by convention here. |
| `homepage` | string | no | Where users can learn more. |
| `readme` | string | yes* | Markdown long description shown in the detail view. |
| `descriptions` | object | no | Locale code → translated one-line summary. |
| `readmes` | object | no | Locale code → translated markdown readme. |

`*` — `source` and `readme` are required in practice: the validation workflow
rejects a plugin without them (a plugin that cannot be installed or
described is not useful).

## Example

```json
{
  "id": "mailflow-notify-slack",
  "name": "Slack Notifier",
  "version": "0.1.0",
  "description": "Posts computed mail analyses to a Slack incoming webhook",
  "categories": ["notifier"],
  "package": "mailflow-notify-slack",
  "source": "git+https://github.com/you/mailflow-repo.git#subdirectory=notifier/mailflow-notify-slack",
  "author": "you",
  "license": "MIT",
  "homepage": "https://github.com/you/mailflow-notify-slack",
  "readme": "## Slack Notifier\n\nSends a message per analyzed mail…",
  "descriptions": {
    "zh-CN": "把邮件分析结果推送到 Slack 的 Webhook"
  },
  "readmes": {
    "zh-CN": "## Slack 通知器\n\n每封邮件分析完成后推送一条消息…"
  }
}
```

## Consistency rules enforced by CI

- `id` matches the folder name exactly.
- `categories` contains exactly one known category.
- `package` matches the distribution name in `pyproject.toml`.
- `source` is non-empty.
- `readme` (or `readmes.*`) is non-empty.
- The entry point resolves and the plugin registers (see
  [06-validation.md](06-validation.md)).

## Why one file per plugin?

Two contributors adding plugins never touch the same file — every PR is
independent. Categories themselves change only when MailFlow adds a new
component kind, which is rare and centrally coordinated.
