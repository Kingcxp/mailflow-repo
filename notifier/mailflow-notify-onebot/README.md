<!-- Generated from plugin.json by tools/gen_plugin_readmes.py. Edit plugin.json. -->

# OneBot / QQ notifier and chat connection

Component ID: `onebot`. Supports mail delivery and shared text-based
reminders/commands; images and managed files are available through the channel's
rich-message capabilities and platform limits.

Automatic deployment uses the pinned [XingYunStar/NapCatQQ archive, v4.18.42](https://github.com/XingYunStar/NapCatQQ/releases/tag/v4.18.42), with SHA-256 verification. Windows installs the Shell ZIP and requires a local QQ client. Linux imports the archived QQ + NapCat Docker image for amd64 or arm64; Docker Engine must be installed, running and accessible to the current user. The container uses host networking with loopback-only HTTP and separate configuration, login data and QR cache per instance. Existing installations are reused without downloading again. For an existing managed QQ channel, choose **More → Reinstall and start** to download and install again for the same instance, keeping notification settings and saved login data. Advanced settings still accept `napcat_package_url` (Windows Shell ZIP) or `napcat_appimage_url` (Linux AppImage). You can also connect your own OneBot v11 HTTP service. The original upstream has ended; this archive is a fixed historical release, not an automatically updated continuation.

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

Choose automatic deployment without entering a package URL, reuse an existing managed installation, or connect your own OneBot v11 HTTP service. Installation, process startup, QQ login and delivery readiness are separate steps; scan/login when requested and then test delivery.

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

自动部署使用固定版本的 [XingYunStar/NapCatQQ 归档 v4.18.42](https://github.com/XingYunStar/NapCatQQ/releases/tag/v4.18.42)，并校验 SHA-256。Windows 安装 Shell ZIP，需要本机已安装 QQ；Linux 导入包含 QQ 和 NapCat 的 amd64／arm64 Docker 镜像，需要事先安装、启动 Docker Engine，并允许当前用户访问。容器使用主机网络，HTTP 仅监听本机；各实例独立保存配置、登录数据和二维码缓存。已有安装直接复用，不重复下载。 已配置的受管 QQ 渠道可选择**更多操作 → 重新安装并启动**，为原实例重新下载并安装程序，保留通知设置和已保存的登录数据。高级设置仍可填写 `napcat_package_url`（Windows Shell ZIP）或 `napcat_appimage_url`（Linux AppImage），也可连接自行部署的 OneBot v11 HTTP 服务。原上游已停止维护，此来源是固定历史归档，不会自动跟进其他分支。

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

选择自动部署即可，无需填写安装包地址；也可复用已有受管安装，或连接自行部署的 OneBot v11 HTTP 服务。安装、启动、QQ 登录和投递就绪是不同步骤，按提示完成登录后再测试投递。

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
