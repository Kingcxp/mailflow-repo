<!-- Generated from plugin.json by tools/gen_plugin_readmes.py. Edit plugin.json. -->

## NoneBot Exporter

Registers the `nonebot` framework exporter. Running `mailflow export --framework
nonebot --output <dir>` (or the TUI's Market → Export wizard) turns your
configured MailFlow instance into a ready-to-install `nonebot-plugin-mailflow`
package.

Registers the bot exporter component id `nonebot`.

### What it generates

| File | Purpose |
| ---- | ------- |
| `pyproject.toml` | Installable package metadata with the needed dependencies |
| `src/nonebot_plugin_mailflow/__init__.py` | Plugin metadata plus driver `on_startup` / `on_shutdown` hooks that start and stop the service |
| `src/nonebot_plugin_mailflow/config.toml` | Your resolved configuration, with secrets kept as `${ENV_VAR}` placeholders |
| `README.md` | Install and usage notes for the generated plugin |

### Chat surface

The generated plugin embeds the shared command router, so the full management
surface is available in chat: messages starting with `mailflow` are dispatched to
the same commands the CLI and TUI use (`mail list`, `action list`, `reply
prepare`, `config get`, ...). Long responses are split across several messages,
and the daily digest is paginated into the chat.

### Usage

```bash
uv run mailflow export --framework nonebot --output dist/nonebot_plugin_mailflow \
    -c configs/development.toml
# or: make bot-plugin-nonebot
```

Then install it into your bot project and load it as usual:

```bash
uv pip install ./dist/nonebot_plugin_mailflow
```

```python
nonebot.load_plugin("nonebot_plugin_mailflow")
```

### Notes

- Secrets are never inlined: an `api_key` that came from `${VAR}` or
  `api_key_env` stays a placeholder, so the generated package is safe to commit.
- Regenerate after changing the configuration — the exported `config.toml` is a
  snapshot, not a live link.
- Exporters are plugins themselves, so supporting another framework is an
  install away, never a core change.

### Requirements

`mailflow-core`; the generated plugin additionally needs `nonebot2`.

### License

MIT — contributions welcome.

---

<!-- zh-CN -->

## NoneBot 导出器

注册 `nonebot` 框架导出器。执行 `mailflow export --framework nonebot --output
<目录>`（或使用 TUI 的“插件市场 → 导出”向导），即可把已配置好的 MailFlow 实例
打包成可直接安装的 `nonebot-plugin-mailflow`。

注册的机器人导出器组件 id 为 `nonebot`。

### 生成的内容

| 文件 | 作用 |
| ---- | ---- |
| `pyproject.toml` | 可安装包的元数据与所需依赖 |
| `src/nonebot_plugin_mailflow/__init__.py` | 插件元数据，以及启动/停止服务的 `on_startup` / `on_shutdown` 钩子 |
| `src/nonebot_plugin_mailflow/config.toml` | 解析后的配置，其中密钥仍保留为 `${环境变量}` 占位符 |
| `README.md` | 生成插件的安装与使用说明 |

### 聊天能力

生成的插件内嵌共享命令路由器，因此完整的管理能力可直接在聊天中使用：以
`mailflow` 开头的消息会被分派到与 CLI、TUI 相同的命令（`mail list`、
`action list`、`reply prepare`、`config get` 等）。过长的回复会拆分为多条消息，
每日摘要也会分页发送到聊天中。

### 用法

```bash
uv run mailflow export --framework nonebot --output dist/nonebot_plugin_mailflow \
    -c configs/development.toml
# 或：make bot-plugin-nonebot
```

随后安装到你的机器人项目并按常规方式加载：

```bash
uv pip install ./dist/nonebot_plugin_mailflow
```

```python
nonebot.load_plugin("nonebot_plugin_mailflow")
```

### 说明

- 密钥绝不会被内联：来自 `${VAR}` 或 `api_key_env` 的 `api_key` 仍保持为占位符，
  因此生成的包可以安全提交到仓库。
- 修改配置后请重新导出 —— 导出的 `config.toml` 是快照，不是实时链接。
- 导出器本身也是插件，因此支持新框架只需安装一个插件，无需改动核心。

### 依赖

`mailflow-core`；生成的插件还需要 `nonebot2`。

### 协议

MIT —— 欢迎贡献。

---

Metadata: [`plugin.json`](plugin.json) · Marketplace: [https://github.com/Kingcxp/mailflow-repo/tree/main/bot_exporter/mailflow-export-nonebot](https://github.com/Kingcxp/mailflow-repo/tree/main/bot_exporter/mailflow-export-nonebot)
