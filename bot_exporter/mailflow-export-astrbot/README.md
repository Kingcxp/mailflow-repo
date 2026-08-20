<!-- Generated from plugin.json by tools/gen_plugin_readmes.py. Edit plugin.json. -->

## AstrBot Exporter

Registers the `astrbot` framework exporter. Running `mailflow export --framework
astrbot --output <dir>` (or the TUI's Market → Export wizard) generates an
AstrBot plugin folder from your configured MailFlow instance.

Registers the bot exporter component id `astrbot`.

### What it generates

| File | Purpose |
| ---- | ------- |
| `main.py` | AstrBot `Star` plugin with `initialize` / `terminate` wired to the MailFlow service lifecycle |
| `metadata.yaml` | AstrBot plugin metadata (name, version, author, description) |
| `config.toml` | Your resolved configuration, secrets kept as `${ENV_VAR}` placeholders |
| `requirements.txt` | Runtime dependencies of the generated plugin |
| `README.md` | Install and usage notes |

### Chat surface

The generated plugin embeds the shared command router, so `/mailflow <command>`
in chat reaches the same management commands as the CLI and TUI (`mail list`,
`action list`, `reply prepare`, `plugin list`, ...). Long replies are split into
several messages and the daily digest is paginated into the chat.

### Usage

```bash
uv run mailflow export --framework astrbot --output dist/astrbot_plugin_mailflow \
    -c configs/development.toml
# or: make bot-plugin-astrbot
```

Copy the generated folder into AstrBot's `data/plugins/` directory and enable it
from the AstrBot dashboard.

### Notes

- Secrets stay placeholders: provide the environment variables where AstrBot
  runs, so the plugin folder itself carries no credentials.
- The plugin owns the MailFlow lifecycle — `terminate` stops the service, so
  reloading the plugin does not leave a second runtime polling your mailboxes.
- Re-export after configuration changes; `config.toml` is a snapshot.

### Requirements

`mailflow-core`; the generated plugin runs inside AstrBot.

### License

MIT — contributions welcome.

---

<!-- zh-CN -->

## AstrBot 导出器

注册 `astrbot` 框架导出器。执行 `mailflow export --framework astrbot --output
<目录>`（或使用 TUI 的“插件市场 → 导出”向导），即可根据已配置的 MailFlow 实例
生成一个 AstrBot 插件目录。

注册的机器人导出器组件 id 为 `astrbot`。

### 生成的内容

| 文件 | 作用 |
| ---- | ---- |
| `main.py` | AstrBot `Star` 插件，其 `initialize` / `terminate` 已接入 MailFlow 服务生命周期 |
| `metadata.yaml` | AstrBot 插件元数据（名称、版本、作者、描述） |
| `config.toml` | 解析后的配置，密钥保留为 `${环境变量}` 占位符 |
| `requirements.txt` | 生成插件的运行时依赖 |
| `README.md` | 安装与使用说明 |

### 聊天能力

生成的插件内嵌共享命令路由器，因此在聊天中使用 `/mailflow <命令>` 即可访问与 CLI、
TUI 相同的管理命令（`mail list`、`action list`、`reply prepare`、`plugin list`
等）。过长的回复会拆分为多条消息，每日摘要也会分页发送到聊天中。

### 用法

```bash
uv run mailflow export --framework astrbot --output dist/astrbot_plugin_mailflow \
    -c configs/development.toml
# 或：make bot-plugin-astrbot
```

把生成的目录复制到 AstrBot 的 `data/plugins/` 下，并在 AstrBot 控制台中启用。

### 说明

- 密钥保持为占位符：请在运行 AstrBot 的环境中提供相应环境变量，插件目录本身不携带
  任何凭据。
- 插件负责 MailFlow 的生命周期 —— `terminate` 会停止服务，因此重载插件不会留下
  第二个仍在轮询邮箱的运行时。
- 配置变更后请重新导出；`config.toml` 只是快照。

### 依赖

`mailflow-core`；生成的插件在 AstrBot 内运行。

### 协议

MIT —— 欢迎贡献。

---

Metadata: [`plugin.json`](plugin.json) · Marketplace: [https://github.com/Kingcxp/mailflow-repo/tree/main/bot_exporter/mailflow-export-astrbot](https://github.com/Kingcxp/mailflow-repo/tree/main/bot_exporter/mailflow-export-astrbot)
