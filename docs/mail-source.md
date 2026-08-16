# Writing a mail source

A `mail_source` plugin adapts a mail provider (IMAP, feeds, …) into the
pipeline: it **streams normalized messages** and can **send replies**.

## Contract

```python
from collections.abc import Awaitable, Callable

MailEmitter = Callable[[MailMessage], Awaitable[None]]


class MailSource:
    async def run(self, emit: MailEmitter, stop_event: asyncio.Event) -> None:
        """Stream messages into emit until stop_event is set."""
        ...

    async def send_reply(self, mail_id: str, draft: ReplyDraft) -> None:
        """Send a confirmed reply for mail_id using this provider."""
        ...

    async def close(self) -> None:
        """Release provider resources."""
        ...
```

## Key points

- **`run` is the whole loop.** It blocks until `stop_event` is set, polling
  or streaming. Every new message goes through `await emit(MailMessage(...))`.
- **`MailMessage` requires** (among others) `message_id`, `account_id`,
  `subject`, `body`, `sender`, `recipients`, `date`, `received_at`. Give the
  provider's own message id to `message_id` so deduplication works across
  restarts.
- **Replies.** `send_reply` must send the reply through the provider. If the
  provider cannot reply (e.g. an RSS feed), raise `NotImplementedError` —
  MailFlow treats that as "reply unsupported" and hides the reply affordance.
- **Never emit duplicates.** Keep a per-account high-water mark (e.g. the
  last seen message id or date) if the provider does not deduplicate.

## Registration

```python
def mailflow_register(self, registrar: PluginRegistrar, config) -> None:
    registrar.add_source("my-source", MySource)
```

The component id (`"my-source"`) is what users write in the config:

```toml
[[sources]]
source_id = "my-source"
provider = "my-source"   # component id, not plugin id
enabled = true
[sources.options]
# any options your factory reads
```

## Reference implementation

[`mailflow-mail-rss`](../mail_source/mailflow-mail-rss/) — polls a feed,
derives a stable `message_id` from the item content, and refuses replies.
