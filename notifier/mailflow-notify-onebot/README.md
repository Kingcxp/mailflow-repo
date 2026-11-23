<!-- Generated from plugin.json by tools/gen_plugin_readmes.py. Edit plugin.json. -->

# OneBot / QQ notifier and chat connection

Component ID: `onebot`. Supports mail delivery and shared text-based
reminders/commands; images and managed files are available through the channel's
rich-message capabilities and platform limits.

NapCat has ended and its official releases and installers have been removed. New automatic downloads are unavailable. Existing managed installations remain supported; otherwise connect your own OneBot v11 HTTP service. Advanced setup accepts a trusted `napcat_package_url` (Windows Shell ZIP) or `napcat_appimage_url` (Linux). MailFlow never selects an unofficial mirror. See [upstream status](https://github.com/NapNeko/NapCatQQ).

```toml
[[notifiers]]
notifier_id = "onebot-main"
provider = "onebot"
minimum_urgency = "important"

[notifiers.options]
http_url = "http://127.0.0.1:3000"
access_token = "${ONEBOT_ACCESS_TOKEN}"
targets = ["user:123456"]
admins = ["123456"]
```

Use an existing OneBot v11 HTTP service or reuse an already installed managed gateway. Installation, process startup, QQ login and delivery readiness are separate steps; follow detected prerequisites and scan/login when requested.

`http_url` is required. `access_token` must match the gateway. Targets use `user:<id>` or `group:<id>`; administrators use stable platform user IDs. HTTP 200 with a failing OneBot retcode is a failure.

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

# OneBot／QQ 通知与聊天连接

组件标识为 `onebot`，支持邮件推送及共享文字提醒、命令；图片和受管文件由渠道能力
提供，并受平台限制。

NapCat 已结束维护，官方发布和安装器已移除，无法再自动下载安装。已有受管实例仍可复用；也可以连接自行部署的 OneBot v11 HTTP 服务。高级设置可填写可信的 `napcat_package_url`（Windows Shell ZIP）或 `napcat_appimage_url`（Linux）。MailFlow 不会自行选择第三方镜像。[上游状态](https://github.com/NapNeko/NapCatQQ)。

```toml
[[notifiers]]
notifier_id = "onebot-main"
provider = "onebot"
minimum_urgency = "important"

[notifiers.options]
http_url = "http://127.0.0.1:3000"
access_token = "${ONEBOT_ACCESS_TOKEN}"
targets = ["user:123456"]
admins = ["123456"]
```

可连接已有 OneBot v11 HTTP 服务，或复用已安装的受管网关。安装、启动、QQ 登录和投递就绪是不同步骤，按检测出的前置条件安装并完成登录。

`http_url` 必填，令牌需与网关一致。目标使用 `user:<ID>`／`group:<ID>`，管理员填写稳定平台用户标识；HTTP 200 但 retcode 失败仍算失败。

管理员身份控制修改、发信、配置和插件操作，不必为了允许普通查询而将所有人设为管理员。
自然语言管理使用共享助手并需要模型，修改和发信仍需确认。

固定目标与聊天订阅不同，取消订阅会说明是否还存在独立固定推送。
全局、渠道、聊天开关、重要程度及免打扰共同决定是否发送。
`notification_images`、`summary_cards`、`send_interval_seconds` 使用共享通知设置，
不支持的输出明确回退文字。

配置、HTTP 或平台错误会报告投递失败，按目标保留凭据，重试不重复发送成功目标。
登录后单独测试投递；进程存在并不代表可用。

---

[Catalog](../../README.md) · [Metadata](plugin.json) · [Plugin page](https://github.com/Kingcxp/mailflow-repo/tree/main/notifier/mailflow-notify-onebot)
