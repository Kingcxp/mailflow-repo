# Mail processors

Steps of the ordered classification chain: filtering, enrichment and routing.

| Plugin | Description |
|---|---|
| [mailflow-processor-blocklist](mailflow-processor-blocklist/) | Marks mail from blocked senders or domains as junk (gray) |

### Adding a plugin

Create a folder `processor/<plugin-id>/` with `plugin.json` and the plugin source, then open a pull request. The PR workflow validates it automatically.

See [docs/02-categories.md](../docs/02-categories.md) for the contract and [docs/00-getting-started.md](../docs/00-getting-started.md) for the full guide.
