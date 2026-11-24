# Validation

[Home](../README.md) · [简体中文](#简体中文)

Both repositories use the main checkout's `mailflow_testkit.plugin_smoke`.
Validation checks metadata, entry points, factory/method signatures, actual
arguments and return values, capabilities and simulated runtime behavior.

## Offline checks

From this repository, use the paired Waymark Mail development interpreter. For a
standard environment layout, replace `python` below with
`../waymark-mail/.venv/Scripts/python.exe` on Windows or
`../waymark-mail/.venv/bin/python` on Linux/macOS.

```bash
python tools/gen_plugin_readmes.py --check
python -m unittest discover -s tests -q
python tools/validate_plugin.py --all --offline --core ../waymark-mail/packages/mailflow-core
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
samples. Shared Waymark Mail plugin dependencies use this checkout through dependency
overrides, so a dev plugin is not tested against an older shared plugin from main.
Other dependencies are installed normally.
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

The generator needs only the standard library. Edit `plugin.json` to change a
generated README. Validation uses temporary data and simulated external services.

## 简体中文

[返回首页](../README.md#简体中文) · [English](#validation)

两个仓库共用 `mailflow_testkit.plugin_smoke`，检查入口、工厂、参数、返回值、
能力声明和运行结果。使用已安装依赖的主仓库解释器，在本仓库依次运行上方的
README 一致性、验证器测试和全插件离线检查命令。

`--offline` 不安装或下载依赖，不连接邮箱、模型、机器人或市场，HTTP、邮件和进程均模拟。
可用单个插件路径代替 `--all`。缺少本地依赖时，先在配套环境安装后再运行。

不带 `--offline` 的模式使用 uv 创建临时环境，按声明安装依赖并运行 `pip check`，
因此需要依赖源网络；这与离线验证是不同流程。`--core` 指定同一主仓库的核心和测试工具包，
共享插件依赖使用当前配套检出，避免混用默认分支的旧实现。

CI 检查 README 生成结果和验证器本身；合并请求按变更选择插件，共享工具改动验证全部，
推送 main/dev 验证全部。失败信息会指出插件、组件和原因。
真实平台登录和文件收发需要另行实测。
