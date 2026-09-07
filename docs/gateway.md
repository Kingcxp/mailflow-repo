# Writing a gateway provisioner

A `gateway` plugin installs, starts, supervises and drives the login of one
chat-platform bot runtime — NapCat for QQ OneBot v11, WeChaty / OpenWeChat
for WeChat, and so on. The runtime it produces is what the platform's
`notifier` plugin (same plugin or a sibling) talks to when delivering mail
alerts.

## Contract

```python
class GatewayProvisioner:
    async def detect(self) -> str: ...                              # host state
    async def install(self, instance_id: str, options: dict) -> None: ...
    async def start(self, instance_id: str, options: dict) -> GatewayInstance: ...
    async def stop(self, instance_id: str) -> None: ...
    async def status(self, instance_id: str) -> GatewayInstance: ...
    async def qr(self, instance_id: str) -> str: ...
```

`GatewayInstance` (from `mailflow.contracts`) carries `provider`,
`instance_id`, `status` (`running` / `starting` / `stopped` / `error`),
`endpoint` and a free-form `extra` dict.

## Lifecycle (who calls what)

- `detect()` — the Notifications tab's guide opens: report whether the
  runtime is installed and/or running ("node …; installed; not running").
- `install(instance_id, options)` — download/unpack the runtime into
  `<data>/gateways/<provider>-<instance>/` (its own directory + port, so
  multiple instances never collide). No-op when already installed.
- `start(instance_id, options)` — launch the child process, wait until its
  HTTP endpoint answers, return the running `GatewayInstance`. The instance
  data dir (logs, QR cache) also lives under `<data>/gateways/`.
- `qr(instance_id)` — return the login QR as a **base64 PNG** (data URL
  stripped), the logged-in sentinel `"__MAILFLOW_LOGGED_IN__"` once the
  session is up, an `"ERROR: …"` diagnostic when the QR cannot be produced,
  or `""` while still pending. The TUI renders the PNG in the guide.
- `status(instance_id)` — probe the live state (endpoint up → `running`;
  process alive but not answering → `starting`; else `stopped` with a
  readable `error`).
- `stop(instance_id)` — terminate the process tree (gateways often spawn a
  child bot, e.g. the full QQ client — kill the whole tree).

## Key points

- **One instance = one account.** Each instance has its own data dir and
  HTTP port, derived deterministically from `instance_id`. State is
  persisted by `mailflow.gateway.GatewayManager`, not by the plugin.
- **Never block the event loop.** Use `await asyncio.to_thread(...)` for
  downloads, `subprocess.Popen` and `subprocess.run`; the guide runs every
  network/process call in a worker.
- **Honest probes.** A missing endpoint or a `get_login_info` that is not
  reachable yet must report "not configured / unreachable", never fake an
  online state. Login is confirmed only by the logged-in sentinel (or the
  user's explicit confirmation).
- **OOM-safe.** A gateway like NapCat runs a full QQ Electron client
  (~1.5–2 GB). Refuse to start on hosts without enough free memory and let
  `GatewayManager` serialize concurrent launches.
- **Config** comes from the notifier entry's `options` (the guided form
  merges its fields into the saved notifier config). Secrets stay in
  options and are redacted from logs like every other secret.

## Registration

```python
def mailflow_register(self, registrar: PluginRegistrar, config) -> None:
    registrar.add_gateway_provisioner("my-platform", MyProvisioner)
```

The component id is the provider key the Notifications tab's guided setup
uses; a plugin usually registers both the `GATEWAY_PROVISIONER` and the
`NOTIFIER` for the same platform (one notifier id per gateway id).

## Reference implementations

- [`mailflow-notify-onebot`](../notifier/mailflow-notify-onebot/) — the
  `napcat` provisioner: pinned GitHub release download (Windows zip / Linux
  AppImage), OneBot v11 HTTP config generation, QR-file → base64, login
  probe via `get_login_info`.
- [`mailflow-notify-openwechat`](../notifier/mailflow-notify-openwechat/) —
  the `openwechat` provisioner: builds a Go bridge (scan-to-login, session
  hot-reload).
