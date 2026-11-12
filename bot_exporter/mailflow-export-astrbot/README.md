<!-- Generated from plugin.json by tools/gen_plugin_readmes.py. Edit plugin.json. -->

# AstrBot exporter

Exporter ID: `astrbot`. Creates a framework host from the current MailFlow
configuration without starting a mail runtime during export.

```bash
uv run mailflow export --framework astrbot --output dist/astrbot_plugin_mailflow -c configs/local.toml
```

Install the generated folder through your AstrBot plugin workflow and enable it. Configure MailFlow administrators through the matching enabled notifier binding described in the generated README; framework administrator flags are not imported automatically.
The generated README describes its file layout and command prefix. Its host
starts/stops the MailFlow service with the framework and forwards sender/chat identity to the shared layer.
Administration is resolved from a unique enabled notifier matching the platform
and instance, with the sender in options.admins; unmatched providers remain read-only.

Supported framework file events can upload managed files, and supported adapters
can send selected files back. Availability depends on the actual platform adapter;
exporting/importing Python successfully does not prove file delivery. Mutations
and sending keep their permission and confirmation rules.

The exported configuration is a snapshot, not a live link. Environment-backed
secrets remain references; literal credentials may still be present. Review the
output, supply needed environment variables in the bot host and regenerate after
configuration changes. Configured notifiers deliver notifications: the export
adapter does not imply an extra automatic broadcast to every framework chat.

---

<!-- zh-CN -->

# AstrBot 导出器

导出器标识为 `astrbot`，按当前配置生成框架宿主；导出过程不启动邮件运行时。

```bash
uv run mailflow export --framework astrbot --output dist/astrbot_plugin_mailflow -c configs/local.toml
```

按 AstrBot 插件流程安装并启用生成目录，按生成说明配置匹配通知器的管理员，框架管理员不会自动导入。
生成的 README 说明目录和命令前缀。宿主随框架启动／停止核心服务，
将发起人和会话传给共享层；管理员由唯一匹配平台、实例的启用通知器中 options.admins 决定，未匹配平台保留普通权限。

支持的框架文件事件可上传受管文件，适配器支持时可发送选中文件；具体能力取决于实际平台。
不能因为导出成功或代码能导入就声称真实文件收发已验证，修改和发信仍受权限与确认限制。

导出配置是快照，环境变量引用会保留，直接填写的凭据可能仍在文件中。
检查输出、在机器人宿主提供所需环境变量，配置变化后重新导出。
通知仍由已配置通知器投递，导出适配器不代表自动向所有框架会话额外广播。

---

[Catalog](../../README.md) · [Metadata](plugin.json) · [Plugin page](https://github.com/Kingcxp/mailflow-repo/tree/main/bot_exporter/mailflow-export-astrbot)
