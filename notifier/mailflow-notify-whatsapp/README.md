<!-- Generated from plugin.json by tools/gen_plugin_readmes.py. Edit plugin.json. -->

# WhatsApp notifier and chat connection

Component ID: `whatsapp`. Supports mail delivery and shared text-based
reminders/commands; images and managed files are available through the channel's
rich-message capabilities and platform limits.

```toml
[[notifiers]]
notifier_id = "whatsapp-main"
provider = "whatsapp"
minimum_urgency = "important"

[notifiers.options]
gateway_url = "http://127.0.0.1:3000"
targets = ["user:15550001111"]
admins = ["15550001111"]
```

Use the managed Baileys bridge or a compatible configured bridge. The managed setup needs its detected Node/npm prerequisites and downloads dependencies; pair from WhatsApp Linked devices when requested. Stored sessions may reconnect, but an expired login still requires pairing again.

`gateway_url` is required. Targets use `user:<number-or-jid>` or `group:<id-or-jid>`; use stable platform identity rather than contact names. Keep administrator numbers consistent with the bridge callback identity.

Administrator identity controls mutations, sending, configuration and plugin
management. Ordinary allowed read commands do not require making everyone an
administrator. Natural-language management uses the shared assistant and requires
a configured model; changes and outbound mail retain confirmation checks.

Fixed targets and chat subscriptions are distinct. Unsubscribing reports whether
a separately configured fixed target still receives pushes. Global, channel and
chat switches, urgency and quiet hours determine actual delivery. Optional
`notification_images`, `summary_cards` and `send_interval_seconds` use the shared
notification settings; text is the fallback on unsupported output.

Configuration, HTTP and platform errors fail delivery visibly. Per-target
receipts prevent retries from repeating successful destinations. Run a delivery
test after login; process existence alone does not prove the connection works.

---

<!-- zh-CN -->

# WhatsApp 通知与聊天连接

组件标识为 `whatsapp`，支持邮件推送及共享文字提醒、命令；图片和受管文件由渠道能力
提供，并受平台限制。

```toml
[[notifiers]]
notifier_id = "whatsapp-main"
provider = "whatsapp"
minimum_urgency = "important"

[notifiers.options]
gateway_url = "http://127.0.0.1:3000"
targets = ["user:15550001111"]
admins = ["15550001111"]
```

使用受管 Baileys 桥或兼容的现有桥。受管安装需要检测到的 Node/npm 环境并下载依赖；按提示在 WhatsApp 已关联设备中配对。保存的会话可重连，登录失效时仍需重新配对。

桥地址必填，目标使用 `user:<号码或JID>`／`group:<群ID或JID>`，不依赖联系人显示名。管理员号码需与桥回调身份对应。

管理员身份控制修改、发信、配置和插件操作，不必为了允许普通查询而将所有人设为管理员。
自然语言管理使用共享助手并需要模型，修改和发信仍需确认。

固定目标与聊天订阅不同，取消订阅会说明是否还存在独立固定推送。
全局、渠道、聊天开关、重要程度及免打扰共同决定是否发送。
`notification_images`、`summary_cards`、`send_interval_seconds` 使用共享通知设置，
不支持的输出明确回退文字。

配置、HTTP 或平台错误会报告投递失败，按目标保留凭据，重试不重复发送成功目标。
登录后单独测试投递；进程存在并不代表可用。

---

[Catalog](../../README.md) · [Metadata](plugin.json) · [Plugin page](https://github.com/Kingcxp/mailflow-repo/tree/main/notifier/mailflow-notify-whatsapp)
