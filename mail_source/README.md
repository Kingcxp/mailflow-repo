# Mail sources

Provider adapters that stream normalized messages into the pipeline and send replies.

| Plugin | Description |
|---|---|
| [mailflow-mail-rss](mailflow-mail-rss/) | Turns RSS/Atom feeds into mail items (newsletters, blogs, release notes) |

### Adding a plugin

Create a folder `mail_source/<plugin-id>/` with `plugin.json` and the plugin source, then open a pull request. The PR workflow validates it automatically.

See [docs/02-categories.md](../docs/02-categories.md) for the contract and [docs/00-getting-started.md](../docs/00-getting-started.md) for the full guide.
