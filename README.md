# MailFlow plugins

[![Plugin validation](https://github.com/Kingcxp/mailflow-repo/actions/workflows/validate-plugins.yml/badge.svg?branch=dev)](https://github.com/Kingcxp/mailflow-repo/actions/workflows/validate-plugins.yml?query=branch%3Adev)

Plugins and marketplace metadata for [MailFlow](https://github.com/Kingcxp/mailflow/tree/dev).
Each plugin is an independently installable Python package with English and
Chinese instructions. This repository and the main workspace share one core
contract; plugins shipped in both places must behave identically.

[简体中文](#简体中文) · [Install](#using-a-plugin) ·
[Contribute](docs/00-getting-started.md) · [Validation](docs/06-validation.md) ·
[Issues](https://github.com/Kingcxp/mailflow-repo/issues)

## Catalog

| Category | Available plugins |
| --- | --- |
| [Mail sources](mail_source) | IMAP/SMTP, Gmail and Outlook presets, RSS/Atom and fake mail |
| [Model backends](llm_backend) | OpenAI-compatible, Anthropic, Google and provider presets |
| [Processors](processor) | Sender blocklists, content filters, local archiving and rule templates |
| [Notifiers](notifier) | Console, SMTP, webhooks and supported chat-platform delivery |
| [Storage](storage) | SQLite persistence and recovery |
| [Framework exporters](bot_exporter) | NoneBot and AstrBot hosts |
| [Color schemes](theme) | Extension category; the four built-in Catppuccin palettes ship with MailFlow |
| [Enhancer category](llm_enhancer) / [Gateway category](gateway) | Extension slots; inspect their indexes for packaged entries |

Open a plugin folder for its provider ID, options, example and limitations.
Capabilities differ: a webhook mail notifier is not automatically a chatbot,
reminder channel or image/file transport. Model presets reuse their declared
transport dependency; Gmail/Outlook adapters use IMAP/SMTP, not native OAuth.

## Using a plugin

Start with the [MailFlow quickstart](https://github.com/Kingcxp/mailflow/blob/dev/README.md#quickstart).
The official marketplace is registered by default. In MailFlow's command shell:

```text
plugin repo list
plugin market list
plugin market show mailflow-notify-ntfy
plugin install mailflow-notify-ntfy
```

The terminal's plugin management provides the same discovery and installation.
Plugin installation needs administrator access. Configure the selected provider,
check the reported capabilities and follow any restart requirement. Install
only trusted code: Python plugins execute inside the MailFlow environment.

These pages describe `dev`. The built-in official market and the metadata's
installation sources currently use the default branch. For unreleased changes,
use paired local `dev` checkouts as described in [development](docs/00-getting-started.md);
viewing a different index alone does not change a plugin's installation source.

## Contributing

| Guide | Purpose |
| --- | --- |
| [Getting started](docs/00-getting-started.md) | Layout, registration, dependencies and submitting changes |
| [Marketplace metadata](docs/01-marketplace-metadata.md) | Bilingual descriptions, install source and usage content |
| [Validation](docs/06-validation.md) | Generated README checks, offline contracts and dependency checks |
| [Core plugin guide](https://github.com/Kingcxp/mailflow/blob/dev/docs/plugin-development/overview.md) | Authoritative interfaces and optional capabilities |

`plugin.json` is the source for the in-app page and generated `README.md`.
Edit it first, then run `python tools/gen_plugin_readmes.py`. Root `index.json`
and category `INDEX.json` files support discovery and HTTP mirrors; keep them
aligned when adding/removing a plugin.

Target changes at `dev`, use focused commits and validate against the matching
MailFlow core. Report reproducible issues with plugin/version, host revision,
platform and sanitized diagnostics. Never include credentials or private mail.
Offline checks simulate delivery; real installation, login and file exchange
need separate platform testing.

## License

[MIT](LICENSE). Third-party platforms, dependencies and gateway runtimes retain
their own licenses and service requirements.

## 简体中文

本仓库提供 [MailFlow](https://github.com/Kingcxp/mailflow/tree/dev) 插件和市场元数据。
插件独立安装，与主仓库共用唯一核心接口；两边同名实现需要同步维护。
上表按邮件源、模型、处理器、通知器、存储、导出器和配色方案分类，进入插件目录查看具体选项。
Catppuccin 四套配色由 MailFlow 内置；配色插件安装启用后，可直接在设置中选择，无需重启连接。
通知器能力不同，不能把普通推送当成聊天机器人、待办提醒或图片文件传输。
Gmail/Outlook 是 IMAP/SMTP 预设，不提供原生 OAuth。

按主仓库说明启动 MailFlow 后，在命令行或插件管理页面查看、安装和配置插件。
官方市场默认已注册，不需要重复添加；命令示例见上方。
安装需要管理员权限，依赖由安装流程处理，是否重启以结果提示为准。
插件会在宿主中执行代码，请仅使用可信来源。

本页对应 `dev`，内置市场和现有元数据安装来源仍使用默认分支。
测试未发布修改时使用两个本地 `dev` 仓库；只切换市场索引不会自动改变安装代码来源。

[入门](docs/00-getting-started.md#简体中文)、[元数据](docs/01-marketplace-metadata.md#简体中文)
和[验证](docs/06-validation.md#简体中文)说明贡献流程。
插件 README 由 `plugin.json` 生成，修改中英文元数据后统一生成，不单独维护两份内容。
提交到 `dev`，新增或删除插件时同步索引，共享实现同时更新主仓库。
反馈包含插件版本、宿主版本、系统和脱敏复现信息，不上传凭据或邮件。
自动验证使用模拟服务，真实安装、登录和文件收发另行实测。本仓库使用 [MIT 许可](LICENSE)。
