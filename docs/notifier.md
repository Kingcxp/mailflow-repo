# Writing a notifier

A `notifier` plugin delivers a computed analysis somewhere: a webhook, a
messaging service, email, a desktop notification.

## Contract

```python
class Notifier:
    async def notify(self, record: MailRecord) -> None:
        ...
```

`MailRecord` carries everything the pipeline computed:

- `record.mail` — the original message (subject, body, sender, …)
- `record.summary` — the LLM/processor summary
- `record.effective_urgency` — `ad` / `info` / `important` / `urgent`
- `record.analysis` — full analysis (reason, reply suggestions, action items)
- `record.record_id`, `record.received_at`

## Key points

- **Gate on urgency.** Notifiers are configured with `minimum_urgency`; still,
  skip politely when the configured endpoint is missing rather than raising.
- **Never block the pipeline.** `notify` runs after processing; a slow or
  failing channel should log and return, not crash the delivery loop.
- **Idempotent payloads.** Include `record_id` in whatever you send so
  downstream consumers can deduplicate retries.
- **Config** comes from `NotifierConfig` (the `[[notifiers]]` section): read
  `options` for endpoint/credentials, and support `"${ENV_VAR}"` expansion by
  reading from the config object (MailFlow expands these when loading).

## Registration

```python
def mailflow_register(self, registrar: PluginRegistrar, config) -> None:
    registrar.add_notifier("my-channel", MyNotifier)
```

```toml
[[notifiers]]
notifier_id = "my-channel"
provider = "my-channel"          # component id
enabled = true
minimum_urgency = "important"
[notifiers.options]
url = "https://…"
# token = "${MY_TOKEN}"
```

## Reference implementations

- [`mailflow-notify-webhook`](../notifier/mailflow-notify-webhook/) — JSON
  POST with optional Bearer auth, retry and timeout options.
- [`mailflow-notify-ntfy`](../notifier/mailflow-notify-ntfy/) — ntfy push
  with urgency mapped to ntfy priorities.
- [`mailflow-notify-smtp`](../notifier/mailflow-notify-smtp/) — forward
  alerts as email via STARTTLS/SSL SMTP.
