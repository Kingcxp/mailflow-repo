# Mail processors

Steps of the ordered classification chain: filtering, enrichment and routing.

| Plugin | Description |
|---|---|
| [mailflow-processor-archive](mailflow-processor-archive/) | Flags mail from matching senders/domains as info + auto-archived (component id: archive) |
| [mailflow-processor-blocklist](mailflow-processor-blocklist/) | Marks mail from blocked senders or domains as junk (gray) |
| [mailflow-processor-filter](mailflow-processor-filter/) | Marks mail matching sender/subject/keyword rules as junk (gray) (component id: filter) |
| [mailflow-processor-rules](mailflow-processor-rules/) | Applies the first matching rule template to each mail (component id: rules) |

### Adding a plugin

Create a folder `processor/<plugin-id>/` with `plugin.json` and the plugin source, then open a pull request. The PR workflow validates it automatically.

See [docs/02-categories.md](../docs/02-categories.md) for the contract and [docs/00-getting-started.md](../docs/00-getting-started.md) for the full guide.