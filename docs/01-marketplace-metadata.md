# Marketplace metadata

Each plugin's `plugin.json` is the source for the description shown in MailFlow
and the generated README shown on GitHub. Root/category indexes locate folders;
they do not duplicate the plugin's metadata.

## Fields

| Field | Meaning |
| --- | --- |
| `id` | Unique plugin ID, matching the folder and entry-point name |
| `name` | Display name; falls back to ID |
| `version` | Release version, matching package and runtime metadata |
| `description` | Concise English summary |
| `categories` | Exactly one category from [index.json](../index.json), matching the parent folder |
| `package` | Distribution name from `pyproject.toml`, used for installation/uninstallation |
| `source` | Installable URL; normally a Git URL with the plugin subdirectory |
| `entry_point` | Entry-point group; default `mailflow.plugins` |
| `author`, `license`, `homepage`, `updated` | Attribution, SPDX license, project link and update date |
| `readme` | English Markdown usage instructions |
| `descriptions`, `readmes` | Locale-to-text maps, including `zh-CN` |

ID, version, description, category, package, source and useful usage instructions
must be present. The validator checks installability and consistency with the
package and core contracts; see [validation](06-validation.md).

```json
{
  "id": "mailflow-notify-example",
  "name": "Example Notifier",
  "version": "0.1.0",
  "description": "Delivers analyzed mail to an example endpoint",
  "categories": ["notifier"],
  "package": "mailflow-notify-example",
  "source": "git+https://github.com/you/mailflow-repo.git#subdirectory=notifier/mailflow-notify-example",
  "license": "MIT",
  "readme": "## Example notifier\n\nConfigure the endpoint and token in notifier options.",
  "descriptions": {"zh-CN": "向指定地址推送邮件分析结果"},
  "readmes": {"zh-CN": "## 示例通知器\n\n在通知器选项中配置地址和令牌。"}
}
```

Point `source` at the repository containing the code users should install;
a fork's unpublished changes are not available from the official repository URL.

## Localization and concise usage

MailFlow selects the current locale's translated description/README, falling
back to the English fields. Search also matches translated descriptions.
Keep both languages aligned when behavior or options change.

A useful README needs the plugin's purpose, required options, one configuration
example and any specific limitations or recovery steps. Avoid repeating the
core API, generic installation instructions, license paragraphs or development
history in every plugin. License and dependency declarations already have
structured fields.

Markdown supports tables, code blocks and normal emphasis. Inline color spans
are optional; plain-text chat output drops color. Never depend on a color to
explain a required action. Plugin form labels and runtime messages use the main
translation component, separately from marketplace description fields.

After editing metadata, run `python tools/gen_plugin_readmes.py` and commit the
regenerated README with it. CI checks that the two stay identical.
