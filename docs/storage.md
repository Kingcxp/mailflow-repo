# Writing a storage backend

A `storage` plugin is the durable persistence layer: records, trash, reply
drafts and preferences. MailFlow ships a SQLite backend; this category is for
teams that need another database or object store.

## Contract

```python
class StorageBackend:
    async def initialize(self) -> None: ...
    async def close(self) -> None: ...

    # active mail
    async def save_mail(self, record: MailRecord) -> None: ...
    async def get_mail(self, record_id: str) -> MailRecord | None: ...
    async def list_mails(self, limit: int | None = None) -> list[MailRecord]: ...
    async def count_mails(self) -> int: ...
    async def set_manual_urgency(self, record_id: str, urgency: Urgency | None) -> MailRecord | None: ...
    async def delete_mail(self, record_id: str) -> None: ...   # moves the full record to trash

    # trash (recovery)
    async def list_trash(self) -> list[TrashRecord]: ...
    async def restore_from_trash(self, record_id: str) -> MailRecord | None: ...
    async def purge_trash(self, before: datetime) -> int: ...
    async def cleanup_mail(self, before: datetime) -> int: ...  # old active -> trash

    # reply drafts
    async def save_draft(self, draft: ReplyDraft) -> None: ...
    async def get_draft(self, draft_id: str) -> ReplyDraft | None: ...
    async def delete_draft(self, draft_id: str) -> None: ...

    # preferences
    async def get_preference(self, key: str) -> str | None: ...
    async def set_preference(self, key: str, value: str) -> None: ...
```

## Key points

- **Implement everything.** The pipeline calls every method; missing pieces
  surface as runtime errors, not at load time. The generated template is a
  complete in-memory implementation — replace storage, keep behavior.
- **`delete_mail` moves to trash**; it is not a hard delete. `purge_trash`
  hard-deletes old trash; `cleanup_mail` ages old active mail into trash.
- **Precision matters.** `set_manual_urgency(record_id, None)` must reset the
  override and return the updated record. `count_mails` should not load all
  rows.
- **`Urgency | None`** — returning `None` from `set_manual_urgency` means
  "record not found".

## Registration

```python
def mailflow_register(self, registrar: PluginRegistrar, config) -> None:
    registrar.add_storage("my-storage", MyStorage)
```

```toml
[storage]
provider = "my-storage"   # component id
[storage.options]
# connection details, path, etc.
```
