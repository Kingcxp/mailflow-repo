# Validation

[Home](../README.md) · [简体中文](#简体中文)

Both repositories use the main checkout's `mailflow_testkit.plugin_smoke`.
Validation checks metadata, entry points, factory/method signatures, actual
arguments and return values, capabilities and simulated runtime behavior.
Instantiating a component alone does not prove compatibility.

## Offline checks

From this repository, use the paired MailFlow development interpreter. For a
standard environment layout, replace `python` below with
`../mailflow/.venv/Scripts/python.exe` on Windows or
`../mailflow/.venv/bin/python` on Linux/macOS.

```bash
python tools/gen_plugin_readmes.py --check
python -m unittest discover -s tests -q
python tools/validate_plugin.py --all --offline --core ../mailflow/packages/mailflow-core
```

A single folder may replace `--all`, for example
`notifier/mailflow-notify-slack`. Offline mode imports paired core/testkit sources
and uses the existing environment; it performs no installation or downloads.
HTTP, mail and subprocess I/O are simulated. Samples cover source handoff retry,
LLM `temperature`/`options`/`tools`, processor outputs, temporary SQLite storage,
notifier failure and export output. Gateway contracts are checked without
launching platform processes.

## Dependency installation and CI

Omit `--offline` to use `uv` to install core, testkit and the plugin with declared
dependencies into a disposable environment, then run `pip check` and the shared
samples. Shared MailFlow plugin dependencies use this checkout through dependency
overrides, so a dev plugin is not tested against an older shared plugin from main.
Other dependencies are installed normally; no dependency checks are bypassed.
`--core` selects core and testkit from one local checkout; without it, the script
uses the main repository's Git sources. This mode needs access to dependency
sources and is separate from offline verification.

The [workflow](../.github/workflows/validate-plugins.yml) always checks generated
READMEs and validator tests. Pull requests validate changed plugin folders;
shared validator/workflow changes validate every plugin. Documentation-only
changes need no component execution. Pushes to `main` and `dev` validate all plugins.
Failures identify the plugin, component and cause.

Metadata checks include folder/category, package/version, entry-point name,
source URL and usage text. Runtime metadata and declared capabilities must
match registration. Missing dependencies or rejected parameters must fail with
a concrete reason, rather than silently removing the plugin from discovery.

Regenerate usage documents after editing `plugin.json`:

```bash
python tools/gen_plugin_readmes.py
python tools/gen_plugin_readmes.py --check
```

The generator itself uses only the standard library. Do not hand-edit generated
READMEs, connect live services in tests or commit validation caches/reports.

## 简体中文

[返回首页](../README.md#简体中文) · [English](#validation)

两个仓库共用 `mailflow_testkit.plugin_smoke`，验证入口、工厂、真实参数、返回值、
能力声明和模拟行为，不能只检查“能实例化”。使用已安装依赖的主仓库解释器，
在本仓库依次运行上方 README 一致性、验证器测试和全插件离线检查命令。

`--offline` 不安装或下载依赖，不连接邮箱、模型、机器人或市场，HTTP、邮件和进程均模拟。
可用单个插件路径代替 `--all`。缺少本地依赖时先在配套环境安装，不能静默跳过失败插件。

不带 `--offline` 的模式使用 uv 创建临时环境，按声明安装依赖并运行 `pip check`，
因此需要依赖源网络；这与离线验证是不同流程。`--core` 指定同一主仓库的核心和测试工具包，
共享插件依赖使用当前配套检出，避免混用默认分支的旧实现。

CI 检查 README 生成结果和验证器本身；合并请求按变更选择插件，共享工具改动验证全部，
推送 main/dev 验证全部。每个失败应明确插件、组件与原因。真实平台登录和文件收发仍需实机验收。
不要手工修改生成的 README，也不要提交验证缓存和报告。
