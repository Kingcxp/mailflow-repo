<!-- Generated from plugin.json by tools/gen_plugin_readmes.py. Edit plugin.json. -->

# Console notifier

Component ID: `console`. Writes mail notifications to the MailFlow logger,
useful for local development without an external delivery service.

```toml
[[notifiers]]
notifier_id = "console"
provider = "console"
minimum_urgency = "important"
```

There are no plugin-specific options. Enable console/file logging as needed to
see the output. The configured urgency threshold still applies. This is not a
chat platform: it has no subscriptions, incoming commands, image or file transport.

---

<!-- zh-CN -->

# 控制台通知器

组件标识为 `console`，将邮件通知写入 MailFlow 日志，适合本地开发，无需外部服务。

```toml
[[notifiers]]
notifier_id = "console"
provider = "console"
minimum_urgency = "important"
```

没有额外配置项，请按需开启控制台或文件日志查看输出，重要程度阈值仍然生效。
本插件不是聊天平台，不提供订阅、接收命令或图片文件传输。

---

[Catalog](../../README.md) · [Metadata](plugin.json) · [Plugin page](https://github.com/Kingcxp/mailflow-repo/tree/main/notifier/mailflow-notify-console)
