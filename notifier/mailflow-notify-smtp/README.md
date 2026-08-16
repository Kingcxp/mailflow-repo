## SMTP Notifier

Forwards important mail alerts as emails through any SMTP server (Gmail, Outlook, self-hosted). Useful when the final alert channel is plain email — e.g. forwarding to a team list.

### Features

- STARTTLS and SSL connection modes
- Optional username/password authentication (env-var or config token)
- Plain-text and HTML parts, urgency label in the subject

### Usage

```toml
[[notifiers]]
notifier_id = "smtp"
provider = "smtp"
enabled = true
minimum_urgency = "urgent"
[notifiers.options]
host = "smtp.example.com"
port = 587
use_tls = true            # false + port 465 uses implicit SSL
username = "alerts@example.com"
password = "${SMTP_PASSWORD}"
from_addr = "alerts@example.com"
to = ["ops@example.com"]
```

### License

MIT — contributions welcome.
