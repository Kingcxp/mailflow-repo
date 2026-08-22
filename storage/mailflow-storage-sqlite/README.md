<!-- Generated from plugin.json by tools/gen_plugin_readmes.py. Edit plugin.json. -->

## SQLite Storage

Durable SQLite persistence: records, trash, reply drafts and preferences
survive restarts in a single database file, with a seven-day recovery trash.

Registers the storage component id `sqlite`.

### How it works

- One connection guarded by an asyncio lock; WAL journal mode plus a 5 s busy
  timeout absorb brief write contention.
- Full domain records are serialized into JSON columns; attachment payloads
  are stripped before persisting, while the original mail text/HTML stays
  intact.
- Deletion — manual or retention cleanup — moves the *full* record to trash
  with a deletion timestamp; restoring returns the identical record.
- Purging compares the trash deletion timestamp, never the receipt time, and
  first-deletion timestamps survive restore → re-trash cycles
  (`INSERT OR IGNORE`).

### Options

The database file comes from the standard `[storage]` section; there are no
backend-specific `[storage.options]` entries:

| Option | Required | Default | Meaning |
| ------ | -------- | ------- | ------- |
| `path` | no | `":memory:"` | SQLite file path; the parent directory is created automatically. Leave empty for an in-memory database. |

### Usage

```toml
[storage]
provider = "sqlite"
path = "data/mailflow.db"
```

### Notes

- WAL mode keeps concurrent reads cheap; the busy timeout rides out short
  writer contention instead of failing the request.
- Attachment binaries are never persisted — downstream consumers work from
  the original text/HTML bodies.

### Requirements

Standard library only (`sqlite3`), plus `mailflow-core`.

### License

MIT — contributions welcome.

---

<!-- zh-CN -->

## SQLite 存储

基于 SQLite 的持久化存储：记录、回收站、回复草稿与偏好设置都保存在单个
数据库文件中，重启不丢，并附带七天可恢复的回收站。

注册的存储组件 id 为 `sqlite`。

### 工作方式

- 单个连接由 asyncio 锁保护；WAL 日志模式加上 5 秒 busy timeout，可以吸收
  短暂的写入竞争。
- 完整的领域记录序列化进 JSON 列；持久化前会剥离附件二进制内容，而原始
  邮件的文本/HTML 正文原样保留。
- 删除（手动或保留期清理）会把*完整*记录连同删除时间戳一起移入回收站；
  还原时返回与原来完全一致的记录。
- 清空回收站比较的是回收站删除时间戳而非接收时间，且首次删除的时间戳在
  「还原 → 再次删除」循环中得以保留（`INSERT OR IGNORE`）。

### 配置项

数据库文件来自标准的 `[storage]` 段，没有后端专属的 `[storage.options]`
配置项：

| 配置项 | 必填 | 默认值 | 说明 |
| ------ | ---- | ------ | ---- |
| `path` | 否 | `":memory:"` | SQLite 文件路径；父目录会自动创建。留空则使用内存数据库。 |

### 用法

```toml
[storage]
provider = "sqlite"
path = "data/mailflow.db"
```

### 说明

- WAL 模式让并发读取开销很低；busy timeout 能扛住短时的写入竞争而不是让
  请求失败。
- 附件二进制从不落盘 —— 下游消费依赖原始的文本/HTML 正文。

### 依赖

仅使用标准库（`sqlite3`），以及 `mailflow-core`。

### 协议

MIT —— 欢迎贡献。

---

Metadata: [`plugin.json`](plugin.json) · Marketplace: [https://github.com/Kingcxp/mailflow-repo/tree/main/storage/mailflow-storage-sqlite](https://github.com/Kingcxp/mailflow-repo/tree/main/storage/mailflow-storage-sqlite)
