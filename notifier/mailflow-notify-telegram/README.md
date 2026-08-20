<!-- Generated from plugin.json by tools/gen_plugin_readmes.py. Edit plugin.json. -->

## Telegram Notifier

Pushes processed mail alerts into a Telegram chat through the Bot API. Create a
bot with [@BotFather](https://t.me/BotFather), copy its token, tell the plugin
which chat to post into, and triage from your phone.

Registers the notifier component id `telegram`.

### How it works

Each mail above the threshold becomes one `sendMessage` call whose text is
`[<urgency>] <subject>` followed by the analysis summary, so the level is
visible in the notification preview without opening the chat. The HTTP call
runs off the event loop.

### Getting the two values

1. **`bot_token`** — message `@BotFather`, send `/newbot`, follow the prompts;
   the token looks like `123456789:AA...`.
2. **`chat_id`** — send any message to your bot, then open
   `https://api.telegram.org/bot<token>/getUpdates` and read
   `result[].message.chat.id`. Group chats have negative ids; for a channel use
   `@channelusername`.

### Options

| Option | Required | Default | Meaning |
| ------ | -------- | ------- | ------- |
| `bot_token` | **yes** | `""` | Bot API token from BotFather. |
| `chat_id` | **yes** | `""` | Target chat, group (negative id) or `@channel`. |

With either value missing the notifier logs a warning naming the record and
skips — a misconfigured channel never breaks mail processing.

### Usage

```toml
[[notifiers]]
notifier_id = "telegram"
provider = "telegram"
enabled = true
minimum_urgency = "important"

[notifiers.options]
bot_token = "${TELEGRAM_BOT_TOKEN}"
chat_id = "123456789"
```

### Troubleshooting

- **`400 chat not found`** — the bot has never met that chat: send it a message
  first, or add it to the group.
- **Nothing in a group** — Telegram privacy mode hides group messages from
  bots; either disable it in BotFather or just re-check the `chat_id`.
- **Only some mails arrive** — that is `minimum_urgency` doing its job.

### Requirements

Standard library only (`urllib`).

### License

MIT — contributions welcome.

---

<!-- zh-CN -->

## Telegram 通知器

通过 Bot API 把处理完的邮件提醒推送到 Telegram 会话。用
[@BotFather](https://t.me/BotFather) 创建机器人、复制令牌，再告诉插件要发到哪个
会话，就能在手机上分流处理。

注册的通知器组件 id 为 `telegram`。

### 工作方式

每封超过阈值的邮件都会触发一次 `sendMessage`，文本为 `[<紧急度>] <主题>` 加上分析
摘要，因此在通知预览里就能看到级别，无需打开会话。HTTP 调用在事件循环之外执行。

### 如何获取两个值

1. **`bot_token`** —— 给 `@BotFather` 发消息，发送 `/newbot` 并按提示操作；令牌
   形如 `123456789:AA...`。
2. **`chat_id`** —— 先给你的机器人随便发一条消息，然后打开
   `https://api.telegram.org/bot<令牌>/getUpdates`，读取
   `result[].message.chat.id`。群聊 id 为负数；频道可直接填 `@频道用户名`。

### 配置项

| 配置项 | 必填 | 默认值 | 说明 |
| ------ | ---- | ------ | ---- |
| `bot_token` | **是** | `""` | BotFather 提供的 Bot API 令牌。 |
| `chat_id` | **是** | `""` | 目标会话、群聊（负数 id）或 `@频道`。 |

任一值缺失时，通知器会记录一条带记录 id 的警告并跳过 —— 配置错误的渠道绝不会中断
邮件处理。

### 用法

```toml
[[notifiers]]
notifier_id = "telegram"
provider = "telegram"
enabled = true
minimum_urgency = "important"

[notifiers.options]
bot_token = "${TELEGRAM_BOT_TOKEN}"
chat_id = "123456789"
```

### 排查

- **返回 `400 chat not found`** —— 机器人从未与该会话交互：先给它发条消息，或把它
  拉进群里。
- **群里收不到** —— Telegram 的隐私模式会让机器人看不到群消息；可在 BotFather 中
  关闭，或重新确认 `chat_id`。
- **只收到部分邮件** —— 这是 `minimum_urgency` 在正常工作。

### 依赖

仅使用标准库（`urllib`）。

### 协议

MIT —— 欢迎贡献。

---

Metadata: [`plugin.json`](plugin.json) · Marketplace: [https://github.com/Kingcxp/mailflow-repo/tree/main/notifier/mailflow-notify-telegram](https://github.com/Kingcxp/mailflow-repo/tree/main/notifier/mailflow-notify-telegram)
