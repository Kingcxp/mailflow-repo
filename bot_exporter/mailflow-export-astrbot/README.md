<!-- Generated from plugin.json by tools/gen_plugin_readmes.py. Edit plugin.json. -->

# AstrBot exporter

Export the current Waymark Mail configuration as a AstrBot plugin. Exporter ID: `astrbot`.

```bash
uv run --no-sync waymark export --framework astrbot --output dist/astrbot_plugin_mailflow -c configs/local.toml
```

## Setup

Install and enable the folder through AstrBot plugin management. The generated README describes the files and command prefix. Waymark Mail starts and stops with the framework; exporting alone does not start the mail service.

For administrator commands, add the platform account to `options.admins` in the enabled notifier matching that platform and instance. Framework administrator settings are separate. If no notifier matches, the user has read-only access.

## Messages and files

Notifications go to the targets configured in Waymark Mail. File upload and sending are available where the platform adapter supports them. Changes and mail sending require the usual permissions and confirmation.

## Configuration

The export contains a copy of the current configuration. Provide its environment variables on the bot host, check for literal credentials before sharing, and export again after changing settings.

---

<!-- zh-CN -->

# AstrBot 导出器

将当前 Waymark Mail 配置导出为 AstrBot 插件，导出器标识为 `astrbot`。

```bash
uv run --no-sync waymark export --framework astrbot --output dist/astrbot_plugin_mailflow -c configs/local.toml
```

## 安装

在 AstrBot 插件管理中安装并启用生成目录。生成的 README 说明了文件和命令前缀。邮件服务随框架启动和停止，导出时不会启动服务。

需要管理员操作时，在匹配平台和实例的启用通知器中，将平台账号加入 `options.admins`。框架自身的管理员设置单独管理；没有匹配通知器时，只能查询。

## 消息与文件

通知发送到 Waymark Mail 中配置的目标。平台适配器支持时，可以上传和发送文件。修改数据和发信仍需权限及确认。

## 配置

导出文件保存的是当时的配置。请在机器人所在机器上设置所需环境变量，分享前检查文件中是否含有凭据；修改设置后需要重新导出。

---

[Catalog](../../README.md) · [Metadata](plugin.json) · [Plugin page](https://github.com/Kingcxp/waymark-mail-repo/tree/main/bot_exporter/mailflow-export-astrbot)
