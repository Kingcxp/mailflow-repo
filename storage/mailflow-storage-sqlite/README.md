<!-- Generated from plugin.json by tools/gen_plugin_readmes.py. Edit plugin.json. -->

# SQLite storage

Component ID: `sqlite`. Stores mail, analysis, tasks, drafts, preferences and
recoverable trash in one local database, with compatible incremental migrations.

```toml
[storage]
provider = "sqlite"
path = "data/mailflow.db"
```

Parent directories are created as needed. `:memory:` is temporary and disappears
when closed. Retention is controlled by `[general]`, not fixed by this plugin;
mail defaults to indefinite retention and trash to seven days. Trash restore
preserves stored mail state and ingestion origin. Receipt-date filtering uses
the source mail timestamp. Reanalysis retains manual priority and local state.

Mail records keep text/HTML, attachment metadata and OCR text. Managed uploads
and fetched attachment caches are stored separately from those records and are
included by the service backup workflow when available. Uncached attachments
still need source access.

Use MailFlow backup/restore for a consistent portable archive and recovery
preview. If manually copying a database, stop its writer first; copying only
the main file while WAL is active is not a consistent backup.

---

<!-- zh-CN -->

# SQLite 存储

组件标识为 `sqlite`，保存邮件、分析、待办、草稿、偏好和可恢复回收站，兼容增量迁移。

```toml
[storage]
provider = "sqlite"
path = "data/mailflow.db"
```

父目录按需创建，`:memory:` 关闭即丢失。保留策略由 `[general]` 控制，
不是插件内固定天数；默认长期保留邮件、回收站七天。恢复保留邮件状态和导入来源，
日期筛选使用真实收件时间，重析保留人工优先级及本地状态。

邮件记录保存正文、HTML、附件信息和识别文字；受管上传与下载缓存另行保存，
服务备份会纳入已有文件。未缓存附件仍需访问原邮箱。

建议通过 MailFlow 创建一致备份并预览恢复。手工复制数据库前先停止写入，
运行中只复制主文件而忽略活动 WAL 不能保证备份一致。

---

[Catalog](../../README.md) · [Metadata](plugin.json) · [Plugin page](https://github.com/Kingcxp/mailflow-repo/tree/main/storage/mailflow-storage-sqlite)
