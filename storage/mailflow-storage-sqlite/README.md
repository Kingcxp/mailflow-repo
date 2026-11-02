<!-- Generated from plugin.json by tools/gen_plugin_readmes.py. Edit plugin.json. -->

## SQLite Storage

Component ID: `sqlite`. Persists mail, analysis, tasks, reply drafts, preferences
and recoverable trash in one database. Data survives application restarts.

```toml
[storage]
provider = "sqlite"
path = "data/mailflow.db"
```

`path` defaults to `data/mailflow.db`; parent directories are created as needed.
Use `:memory:` only for temporary data that may disappear on shutdown. There are
no backend-specific storage options.

Deleting mail moves it into trash; restoring recovers its stored state. Mail
and trash retention are controlled by `[general]`, not fixed by this plugin.
Trash expiry uses the deletion timestamp. Manual urgency, feedback and local
task state are preserved when analysis is updated.

Mail text/HTML, attachment metadata and OCR text are persisted; attachment
binaries are omitted. SQLite uses WAL and a busy timeout to handle brief write
contention. Back up the database together with its active WAL when the service
is running, or stop the service before making a file copy.

---

<!-- zh-CN -->

## SQLite 存储

组件标识为 `sqlite`。在一个数据库中保存邮件、分析结果、待办、回复草稿、偏好和
可恢复的回收站内容，应用重启后仍然保留。

```toml
[storage]
provider = "sqlite"
path = "data/mailflow.db"
```

`path` 默认为 `data/mailflow.db`，按需创建父目录。`:memory:` 仅适合关闭后可以丢失的
临时数据。此插件没有额外的存储选项。

删除邮件会移入回收站，恢复时保留已保存状态。邮件和回收站保留时间由 `[general]`
控制，并非插件内固定天数。回收站按删除时间计算过期；更新分析结果时保留手动
优先级、用户反馈和本地待办状态。

保存正文、HTML、附件信息和图片识别文本，不保存附件原始字节。SQLite 使用 WAL 和
繁忙等待处理短暂写入竞争。运行中备份时需要连同活动 WAL 一起处理，也可以先停止
服务再复制数据库文件。

---

Metadata: [`plugin.json`](plugin.json) · Marketplace: [https://github.com/Kingcxp/mailflow-repo/tree/main/storage/mailflow-storage-sqlite](https://github.com/Kingcxp/mailflow-repo/tree/main/storage/mailflow-storage-sqlite)
