# Getting started

[Home](../README.md) · [简体中文](#简体中文)

Implement against the main repository's
[plugin guide](https://github.com/Kingcxp/waymark-mail/blob/dev/docs/plugin-development/overview.md)
and [core contracts](https://github.com/Kingcxp/waymark-mail/blob/dev/packages/mailflow-core/src/mailflow/contracts.py).
Bundled and marketplace plugins use the same interfaces.

## Create a plugin

Use Waymark Mail's TUI Market → New wizard to choose a category and generate a
loadable package. Put the result in `<category>/<plugin-id>/` in this repository.
The categories are listed in [index.json](../index.json).

```text
notifier/mailflow-notify-example/
    plugin.json
    README.md
    pyproject.toml
    src/mailflow_notify_example/
        __init__.py
        plugin.py
```

`plugin.json` defines marketplace display/install metadata. `pyproject.toml`
defines the distribution, runtime dependencies and `mailflow.plugins` entry
point. `plugin.py` implements registration and the component. The generated
README uses the English and translated metadata from `plugin.json`.

Choose a unique plugin ID matching the folder, distribution name and entry-point
name. The registered component ID is the configuration `provider`; it may be
shorter. Declare every runtime dependency, including `mailflow-core`.

## Describe, validate and submit

Write concise English and Chinese descriptions, required options, a working
configuration example and relevant failure/recovery guidance. See the
[metadata reference](01-marketplace-metadata.md). Keep placeholders rather than
real credentials, and describe current behavior rather than future plans.

```bash
python tools/gen_plugin_readmes.py
python tools/gen_plugin_readmes.py --check
python tools/validate_plugin.py notifier/mailflow-notify-example --offline --core ../waymark-mail/packages/mailflow-core
```

Run offline validation using the paired Waymark Mail development interpreter; the
[validation guide](06-validation.md) explains dependency-install checks and CI.
For manual local installation, install the plugin into Waymark Mail's Python
environment and use `plugin list` in its shell, then restart when requested.

Use paired `dev` checkouts for unreleased changes. From the main checkout,
`uv pip install -e ../waymark-mail-repo/<category>/<plugin-id>` installs a local
plugin into its environment; use `--python` to select the host interpreter if
needed. In the standard workspace environment, start it with
`uv run --no-sync waymark tui -c configs/local.toml`, then check `plugin list`.
`make tui` also uses the selected environment directly and preserves this local
installation. An explicit `make sync` or `uv sync --all-packages` restores locked
workspace sources, including a same-name plugin from the main checkout.
The marketplace index URL and metadata
`source` are separate: changing an index does not change the code installed from
a source URL that still names the default branch.

Target pull requests at `dev`; describe user behavior, compatibility and checks.
A pull request normally changes only the plugin folder. Update the category's
`INDEX.json` when adding or removing a plugin so HTTP mirrors stay in sync.
If an implementation is also bundled in the main repository, update its paired
copy and validate both. Avoid committing environments, generated exports,
credentials, caches or diagnostic reports.

## Theme plugins

Put color-scheme packages in `theme/`. Register a zero-argument factory with
`@PLUGIN.theme("unique-theme-id")`, returning `mailflow.themes.ColorScheme`.
Omitted colors inherit from a Catppuccin base; no Textual dependency is needed.
Optional `buttons` entries use `mailflow.themes.ButtonColors` for default,
primary, success, warning and error buttons, including hover/focus, pressed and
disabled states. See the core plugin guide for the fields and an example.

## 简体中文

[返回首页](../README.md#简体中文) · [English](#getting-started)

以主仓库 `mailflow-core` 的接口为准，两个仓库使用匹配的 `dev` 分支。
可在终端插件市场的新建向导生成骨架，再放到 `<类别>/<插件标识>/`。
目录中包含 `plugin.json`、生成的 README、`pyproject.toml` 和实现代码。
安装包名、目录名和入口名保持一致，配置 `provider` 对应注册的组件标识。
所有运行依赖写入包配置，不复制另一套核心接口。

### 配色插件

配色包放在 `theme/`，用 `@PLUGIN.theme("唯一配色标识")` 注册无参数工厂，返回
`mailflow.themes.ColorScheme`。未指定的颜色继承 Catppuccin 基础配色，不需要依赖
Textual。可选的 `buttons` 使用 `mailflow.themes.ButtonColors`，分别覆盖次要、主要、
保存确认、警告和删除按钮（`default`、`primary`、`success`、`warning`、`error`）
的背景、文字，以及悬停／聚焦、按下、禁用状态。未填写的部分自动从主题继承清晰可读的
颜色，旧主题继续兼容；完整字段和契约见主仓库插件说明。

### 本地验证与提交

先修改中英文元数据，再运行生成和离线验证命令。使用主仓库已同步依赖的 Python 环境；
离线验证不会安装依赖或连接服务。本地安装方法见上方，可用 `--python` 明确选择宿主解释器。
测试本地安装时使用 `uv run --no-sync` 或 `make tui` 启动，两者都保留现有安装。
只有主动执行 `make sync` 或 `uv sync --all-packages` 才会按锁文件恢复环境，可能替换同名插件。
默认市场及元数据安装来源使用默认分支，索引地址与安装地址是不同字段。
测试未发布代码时使用本地路径安装；修改索引不会改变元数据中的安装来源。

修改提交到 `dev`，说明用户行为、兼容影响和验证结果；新增或移除插件同步类别索引。
同名内置插件同时更新主仓库。不要提交密钥、环境、缓存、报告或生成的机器人私有配置。
