# MailFlow Plugin Repository

The official plugin marketplace for [MailFlow](https://github.com/Kingcxp/mailflow).

Plugins are grouped by category, one folder per plugin. Each plugin folder
contains `plugin.json` (the marketplace metadata, including the markdown
readme) plus the plugin source.

```
mail_source/    mailbox and feed source adapters
processor/      steps of the ordered classification chain
llm_backend/    chat-completions transports
notifier/       channels that deliver computed analyses and reminders
storage/        durable persistence backends
```

## Adding a plugin (pull requests)

1. Pick the category folder, create `<plugin-id>/`.
2. Put `plugin.json` inside it with the plugin metadata:
   ```json
   {
     "id": "mailflow-my-plugin",
     "name": "My Plugin",
     "version": "0.1.0",
     "description": "one-line summary",
     "categories": ["notifier"],
     "package": "mailflow-my-plugin",
     "source": "git+https://github.com/Kingcxp/mailflow-repo.git#subdirectory=notifier/mailflow-my-plugin",
     "author": "you",
     "license": "MIT",
     "homepage": "https://github.com/you/mailflow-my-plugin",
     "readme": "# My Plugin\n\nlong markdown description"
   }
   ```
3. Add the plugin source (`pyproject.toml` with a `mailflow.plugins` entry
   point + `src/...`), following the plugin-development guide in the main
   repo (`docs/plugin-development/`).

Because every plugin lives in its own folder with its own `plugin.json`,
pull requests never touch other plugins' files.

## Using the marketplace

```bash
uv run mailflow plugin repo add mailflow-repo https://github.com/Kingcxp/mailflow-repo
uv run mailflow plugin market list
uv run mailflow plugin market show mailflow-notify-ntfy
uv run mailflow plugin install mailflow-notify-ntfy   # restart to load
```
