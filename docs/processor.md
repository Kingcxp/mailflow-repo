# Writing a processor

A `processor` plugin is one step in the ordered classification chain. It
looks at a mail and contributes a decision, an analysis overlay and/or notes.

## Contract

```python
class MailProcessor:
    processor_id: str

    async def process(self, mail: MailMessage, context: ProcessingContext) -> ProcessorResult:
        ...
```

- `ProcessorResult.decision` — `CONTINUE` (default) or `STOP` (skip the
  remaining processors).
- `ProcessorResult.analysis` — optional `MailAnalysis` overlay merged into
  the accumulated analysis (summary, urgency, reply suggestions, …).
- `ProcessorResult.notes` — human-readable audit lines shown in the mail
  detail view.
- `ProcessingContext` — `account_id`, `timezone`, `options`, and an injected
  `now` clock for deterministic processors (use it for anything time-based).

## Key points

- **Be cheap and safe.** Processors run on every mail. Pure, idempotent,
  dependency-light processors are welcome; anything else belongs in a
  notifier or a dedicated service.
- **Never raise** for malformed input — return `CONTINUE` with a note.
- **Order matters.** The pipeline runs processors in config order; if your
  processor must run after another (e.g. after an LLM summary), say so in the
  readme and document the `[[processors]]` ordering.

## Registration

```python
def mailflow_register(self, registrar: PluginRegistrar, config) -> None:
    registrar.add_processor("blocklist", BlocklistProcessor)
```

```toml
[[processors]]
processor_id = "blocklist"
provider = "blocklist"   # component id
enabled = true
[processors.options]
blocked = ["spammer@example.com"]
```

## Reference implementation

[`mailflow-processor-blocklist`](../processor/mailflow-processor-blocklist/)
— marks mail from blocked senders/domains as `ad`, with wildcard domain
support and a clean audit note.
