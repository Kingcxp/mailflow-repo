# Gateways

Auto-provisioners for chat-platform bot runtimes: installing, starting,
supervising and driving the QR login for a platform's bot process (NapCat
for QQ OneBot v11, WeChaty / OpenWeChat for WeChat, ...). Each gateway
provides the runtime the `notifier` side of the same platform talks to.

| Plugin | Description |
|---|---|
| _(yours could be the first)_ | Auto-install and supervise one chat-platform bot runtime |

### Gateway contract

A gateway provisioner implements the `GatewayProvisioner` contract:
`detect` (host state), `install` (download/install under `data/gateways/`),
`start` / `stop` (process lifecycle), `status` (probe) and `qr` (login QR
as base64 PNG, the logged-in sentinel, or a diagnostic `ERROR: ...`). The
component id is the provider key used by the Notifications tab's guided
setup.

### Adding a plugin

Create a folder `gateway/<plugin-id>/` with `plugin.json` and the plugin
source, then open a pull request. The PR workflow validates it automatically.

See [docs/02-categories.md](../docs/02-categories.md) for the contract and
[docs/00-getting-started.md](../docs/00-getting-started.md) for the full
guide.