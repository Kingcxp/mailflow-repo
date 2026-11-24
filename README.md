# <img src="https://raw.githubusercontent.com/Kingcxp/waymark-mail/dev/assets/icon.svg" width="36" alt=""> Waymark Mail Plugin Repository

[简体中文](#简体中文) · [Install](#using-a-plugin) ·
[Contribute](docs/00-getting-started.md) · [Issues](https://github.com/Kingcxp/waymark-mail-repo/issues)

[![Plugin validation](https://github.com/Kingcxp/waymark-mail-repo/actions/workflows/validate-plugins.yml/badge.svg?branch=dev)](https://github.com/Kingcxp/waymark-mail-repo/actions/workflows/validate-plugins.yml?query=branch%3Adev)

The plugin repository for [Waymark Mail](https://github.com/Kingcxp/waymark-mail/tree/dev).
It contains installable Python packages and the metadata used by the in-app
marketplace. Each plugin has English and Chinese setup instructions.

## Catalog

| Category | Contents |
| --- | --- |
| [Mail sources](mail_source) | IMAP/SMTP, Gmail and Outlook presets, RSS/Atom and fake mail |
| [Model backends](llm_backend) | OpenAI-compatible, Anthropic, Google and provider presets |
| [Processors](processor) | Sender blocklists, content filters, local archiving and rule templates |
| [Notifiers](notifier) | Console, SMTP, webhooks and chat-platform delivery |
| [Storage](storage) | SQLite |
| [Framework exporters](bot_exporter) | NoneBot and AstrBot |

Open a plugin folder for its provider ID, options and configuration example.
Gmail and Outlook use IMAP/SMTP rather than native OAuth. Notification plugins
list whether they support reminders, images, files or incoming commands.

The index also reserves categories for [themes](theme), [model enhancers](llm_enhancer)
and [gateways](gateway). Built-in color schemes ship with Waymark Mail itself.

## Using a plugin

Start Waymark Mail using its [quickstart](https://github.com/Kingcxp/waymark-mail/blob/dev/README.md#quickstart).
The official repository is available in the Market tab by default. You can also
inspect and install a plugin from the command shell:

```text
plugin repo list
plugin market list
plugin market show mailflow-notify-ntfy
plugin install mailflow-notify-ntfy
```

Installation requires administrator access. After installing, configure the
provider and follow any restart prompt. Plugins run code in Waymark Mail’s Python
environment, so use sources you trust.

These pages describe `dev`; the default marketplace installs from the default
branch specified by the metadata. To try unreleased changes, use matching local
`dev` checkouts as described in [development](docs/00-getting-started.md).

## Contributing

| Guide | Contents |
| --- | --- |
| [Getting started](docs/00-getting-started.md) | Package layout, registration, dependencies and local installation |
| [Marketplace metadata](docs/01-marketplace-metadata.md) | Descriptions, installation sources and usage pages |
| [Validation](docs/06-validation.md) | README generation, offline checks and CI |
| [Core plugin guide](https://github.com/Kingcxp/waymark-mail/blob/dev/docs/plugin-development/overview.md) | Interfaces and optional capabilities |

Edit `plugin.json`, then run `python tools/gen_plugin_readmes.py` to update the
plugin README. Add or remove plugins in the category’s `INDEX.json`. Submit pull
requests to `dev`; plugins also bundled in Waymark Mail need both copies updated.

The repository is named `waymark-mail-repo`. Plugin IDs and package names retain
their `mailflow-*` prefixes so existing configurations continue to work.

Licensed under the [MIT License](LICENSE).

## 简体中文

这里是 [Waymark Mail](https://github.com/Kingcxp/waymark-mail/tree/dev) 的插件仓库，
提供独立安装的 Python 插件和应用内市场使用的元数据。
插件按邮件源、模型、处理器、通知器、存储和框架导出器分类，目录见上表。
每个插件目录都有中英文说明，包含组件标识、配置示例和使用限制。

### 安装插件

按主仓库说明启动后，在“市场”中查看并安装插件，或在命令行中执行上面的命令。
官方仓库默认已添加。安装需要管理员权限，安装后配置对应服务，并按提示决定是否重启。

Gmail、Outlook 插件使用 IMAP/SMTP，不提供原生 OAuth。
各通知器支持的提醒、图片、文件和聊天命令不同，安装前可在插件详情中查看。
插件会在程序所在环境中执行代码，请选择可信来源。

本页对应 `dev`，默认市场按元数据指定的默认分支安装插件。
试用未发布的修改时，请使用两个本地 `dev` 仓库，方法见[开发入门](docs/00-getting-started.md#简体中文)。

### 参与开发

[开发入门](docs/00-getting-started.md#简体中文)、[元数据说明](docs/01-marketplace-metadata.md#简体中文)
和[验证方法](docs/06-validation.md#简体中文)介绍了完整流程。
插件 README 从 `plugin.json` 生成，修改中英文元数据后统一生成即可。
新增或删除插件时更新分类索引；主仓库也内置的插件需要两边一起维护。修改提交到 `dev`。

仓库名为 `waymark-mail-repo`，插件标识和包名保留 `mailflow-*` 前缀，已有配置可以继续使用。
反馈问题请附插件版本、系统和复现步骤，日志中不要包含凭据或私人邮件。
本仓库使用 [MIT 许可](LICENSE)。
