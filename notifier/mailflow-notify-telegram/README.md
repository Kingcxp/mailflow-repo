<!-- Generated from plugin.json by tools/gen_plugin_readmes.py. Edit plugin.json. -->

# Telegram notifier and chat connection

Component ID: `telegram`. Supports mail delivery and shared text-based
reminders/commands; images and managed files are available through the channel's
rich-message capabilities and platform limits.

```toml
[[notifiers]]
notifier_id = "telegram-main"
provider = "telegram"
minimum_urgency = "important"

[notifiers.options]
bot_token = "${TELEGRAM_BOT_TOKEN}"
chat_id = "123456789"
admins = ["123456789"]
```

Provide a bot token and enable the in-process Telegram bridge for commands. No external gateway process is required. The user must start a private chat with the bot, or add it to the intended group with the required permissions. Long polling needs a working API connection.

`bot_token` is required. `chat_id` is an optional fixed target; subscriptions or `targets` may supply destinations instead. Groups use their stable chat ID. `api_base` defaults to `https://api.telegram.org`; administrators use numeric sender IDs, not display names.

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

# Telegram 通知与聊天连接

组件标识为 `telegram`，支持邮件推送及共享文字提醒、命令；图片和受管文件由渠道能力
提供，并受平台限制。

```toml
[[notifiers]]
notifier_id = "telegram-main"
provider = "telegram"
minimum_urgency = "important"

[notifiers.options]
bot_token = "${TELEGRAM_BOT_TOKEN}"
chat_id = "123456789"
admins = ["123456789"]
```

提供机器人令牌，通过进程内 Telegram 桥接收命令，无需额外网关进程。用户先与机器人私聊，或将其加入目标群并授予必要权限；长轮询需要能够访问配置的 API。

令牌必填，`chat_id` 是可选固定目标，也可使用订阅或 `targets`。群聊使用稳定聊天标识，`api_base` 默认 `https://api.telegram.org`，管理员填写数字用户标识，不填显示名。

管理员身份控制修改、发信、配置和插件操作，不必为了允许普通查询而将所有人设为管理员。
自然语言管理使用共享助手并需要模型，修改和发信仍需确认。

固定目标与聊天订阅不同，取消订阅会说明是否还存在独立固定推送。
全局、渠道、聊天开关、重要程度及免打扰共同决定是否发送。
`notification_images`、`summary_cards`、`send_interval_seconds` 使用共享通知设置，
不支持的输出明确回退文字。

配置、HTTP 或平台错误会报告投递失败，按目标保留凭据，重试不重复发送成功目标。
登录后单独测试投递；进程存在并不代表可用。

---

[Catalog](../../README.md) · [Metadata](plugin.json) · [Plugin page](https://github.com/Kingcxp/mailflow-repo/tree/main/notifier/mailflow-notify-telegram)
