"""Gmail preset using the shared IMAP receive, MIME and SMTP implementation."""

from __future__ import annotations

from datetime import datetime

from mailflow.config import MailAccountConfig, MailFlowConfig
from mailflow.domain import ComponentKind, MailMessage
from mailflow.plugins import PluginInfo
from mailflow.registry import PluginRegistrar
from mailflow_mail_imap.plugin import IMAPSource, account_form
from mailflow_mail_imap.plugin import parse_mime as _parse_mime


def parse_mime(
    raw: bytes,
    account_id: str,
    provider: str = "gmail",
    *,
    ocr_enabled: bool = False,
    internal_date: datetime | None = None,
) -> MailMessage:
    return _parse_mime(
        raw, account_id, provider, ocr_enabled=ocr_enabled, internal_date=internal_date
    )


class GmailSource(IMAPSource):
    provider = "gmail"

    def __init__(self, account: MailAccountConfig) -> None:
        options = {"preset": "gmail", **account.options}
        super().__init__(account.model_copy(update={"options": options}))


PLUGIN_INFO = PluginInfo(
    plugin_id="mailflow-mail-gmail",
    name="Gmail Mail Source",
    version="0.1.0",
    description="IMAP/SMTP mail source for Gmail",
    kinds=[ComponentKind.MAIL_SOURCE],
)


class GmailPlugin:
    def mailflow_plugin_info(self) -> PluginInfo:
        return PLUGIN_INFO

    def mailflow_register(self, registrar: PluginRegistrar, config: MailFlowConfig) -> None:
        registrar.add_source("gmail", GmailSource)
        registrar.add_form_fields(ComponentKind.MAIL_SOURCE, "gmail", account_form("gmail"))


plugin = GmailPlugin()

__all__ = ["GmailPlugin", "GmailSource", "parse_mime", "plugin"]
