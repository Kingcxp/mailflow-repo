## ntfy Notifier

Pushes mail alerts to [ntfy](https://ntfy.sh) topics — works with the public ntfy.sh service or any self-hosted ntfy server, so alerts land on your phone via the ntfy app.

### Features

- Optional auth token for private topics (`Authorization: Bearer`)
- Urgency mapped to ntfy priorities (ad=min, info=default, important=high, urgent=urgent)
- Standard library only (urllib)

### Usage

```toml
[[notifiers]]
notifier_id = "ntfy"
provider = "ntfy"
enabled = true
minimum_urgency = "important"
[notifiers.options]
base_url = "https://ntfy.sh"      # or your self-hosted server
# token = "${NTFY_TOKEN}"         # optional, for private topics
```

### License

MIT — contributions welcome.
