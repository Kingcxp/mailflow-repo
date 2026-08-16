# Localization

MailFlow is language-aware (English and Chinese ship by default; more can be
added). Plugins participate: **when the app language has a matching
translation, the plugin's summary and readme are shown in that language —
in the CLI, the TUI and chat frontends alike.** Otherwise the default
(English) fields are used.

## Two optional fields

```json
{
  "description": "Posts computed analyses to a webhook",
  "readme": "## Webhook notifier\n\n…default (English)…",

  "descriptions": { "zh-CN": "把邮件分析结果推送到 Webhook" },
  "readmes": { "zh-CN": "## Webhook 通知器\n\n…中文说明…" }
}
```

| Field | Type | Fallback |
|---|---|---|
| `descriptions` | `{locale: string}` | `description` |
| `readmes` | `{locale: markdown}` | `readme` |

Locale codes are the same ones MailFlow's language packs use (`en`,
`zh-CN`, …).

## What gets translated

- `market list` / `plugin search` — the description column
- `market show` — the metadata summary line and the markdown readme
- TUI market tab — the description cell and the readme detail pane

Search also matches translated descriptions: searching for a Chinese term
finds plugins whose `descriptions["zh-CN"]` contains it, even when the
default description is English.

## Writing good localized readmes

- Keep the two languages in sync; stale translations confuse more than
  missing ones.
- The readme is full markdown and is rendered with rich text effects in the
  CLI and TUI: **bold**, *italic*, ~~strikethrough~~, `code`, headings,
  lists, quotes, fenced code blocks — and inline colors:

  ```markdown
  <span style="color:#ff5500">This text renders orange</span>
  ```

  Colors work in the CLI (ANSI) and in the TUI markdown widget; plain-text
  frontends (chat) fall back to the uncolored text.
