## Webhook Notifier

Delivers computed mail analyses to any HTTP webhook — a practical starting point for chat bridges, team dashboards and home automation.

### Features

- POSTs a JSON payload per processed mail (mail id, urgency, subject, summary, sender, reply flag)
- Standard-library only (urllib): no extra dependencies beyond mailflow-core
- Failure-tolerant: delivery errors are logged and never fail processing

### Usage

```toml
[[notifiers]]
notifier_id = "webhook"
provider = "webhook"
enabled = true
minimum_urgency = "important"
[notifiers.options]
url = "https://your-webhook.example/hook"
timeout_seconds = 10
```

### License

MIT — contributions welcome.
