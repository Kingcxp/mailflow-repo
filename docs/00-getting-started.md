# Getting started

[Home](../README.md) · [简体中文](#简体中文)

Implement against the main repository's
[plugin guide](https://github.com/Kingcxp/mailflow/blob/dev/docs/plugin-development/overview.md)
and [core contracts](https://github.com/Kingcxp/mailflow/blob/dev/packages/mailflow-core/src/mailflow/contracts.py).
The same interfaces cover bundled and marketplace plugins; category-specific
copies are intentionally not maintained here.

## Create a plugin

Use MailFlow's TUI Market → New wizard to choose a category and generate a
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
README is derived from the English and translated metadata, so do not edit it
independently.

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
python tools/validate_plugin.py notifier/mailflow-notify-example --offline --core ../mailflow/packages/mailflow-core
```

Run offline validation using the paired MailFlow development interpreter; the
[validation guide](06-validation.md) explains dependency-install checks and CI.
For manual local installation, install the plugin into MailFlow's Python
environment and use `plugin list` in its shell, then restart when requested.

Use paired `dev` checkouts for unreleased changes. From the main checkout,
`uv pip install -e ../mailflow-repo/<category>/<plugin-id>` installs a local
plugin into its environment; use `--python` to select the host interpreter if
needed. In the standard workspace environment, start it with
`uv run --no-sync mailflow tui -c configs/local.toml`, then check `plugin list`.
`make sync` or workspace-wide `--all-packages` synchronization restores locked
workspace sources, including a same-name plugin from the main checkout. Use
`--no-sync` while deliberately testing the paired local installation.
The marketplace index URL and metadata
`source` are separate: changing an index does not change the code installed from
a source URL that still names the default branch.

Target pull requests at `dev`; describe user behavior, compatibility and checks.
A pull request normally changes only the plugin folder. Update the category's
`INDEX.json` when adding or removing a plugin so HTTP mirrors stay in sync.
If an implementation is also bundled in the main repository, update its paired
copy and validate both. Avoid committing environments, generated exports,
credentials, caches or diagnostic reports.

## 简体中文

[返回首页](../README.md#简体中文) · [English](#getting-started)

以主仓库 `mailflow-core` 的接口为准，两个仓库使用匹配的 `dev` 分支。
可在终端插件市场的新建向导生成骨架，再放到 `<类别>/<插件标识>/`。
目录中包含 `plugin.json`、生成的 README、`pyproject.toml` 和实现代码。
安装包名、目录名和入口名保持一致，配置 `provider` 对应注册的组件标识。
所有运行依赖写入包配置，不复制另一套核心接口。

先修改中英文元数据，再运行生成和离线验证命令。使用主仓库已同步依赖的 Python 环境；
离线验证不会安装依赖或连接服务。本地安装方法见上方，可用 `--python` 明确选择宿主解释器。
测试本地安装时使用 `uv run --no-sync` 启动，避免 Make 的工作区同步将同名插件恢复为主仓库来源。
重新执行 `make sync` 会按锁文件恢复环境。
默认市场及元数据安装来源使用默认分支，索引地址与安装地址是不同字段。
未发布代码应使用本地路径安装，不能只改索引就声称用户会安装到开发代码。

修改提交到 `dev`，说明用户行为、兼容影响和验证结果；新增或移除插件同步类别索引。
同名内置插件同时更新主仓库。不要提交密钥、环境、缓存、报告或生成的机器人私有配置。
