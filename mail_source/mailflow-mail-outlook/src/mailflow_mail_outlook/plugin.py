"""Outlook preset using the shared IMAP receive, MIME and SMTP implementation."""

from __future__ import annotations

from datetime import datetime

from mailflow.config import MailAccountConfig, MailFlowConfig
from mailflow.domain import ComponentKind, MailMessage
from mailflow.plugins import PluginInfo
from mailflow.registry import PluginRegistrar
from mailflow_mail_imap.plugin import IMAPSource
from mailflow_mail_imap.plugin import parse_mime as _parse_mime


def parse_mime(
    raw: bytes,
    account_id: str,
    provider: str = "outlook",
    *,
    ocr_enabled: bool = False,
    internal_date: datetime | None = None,
) -> MailMessage:
    return _parse_mime(
        raw, account_id, provider, ocr_enabled=ocr_enabled, internal_date=internal_date
    )


class OutlookSource(IMAPSource):
    provider = "outlook"

    def __init__(self, account: MailAccountConfig) -> None:
        options = {"preset": "outlook", **account.options}
        super().__init__(account.model_copy(update={"options": options}))


PLUGIN_INFO = PluginInfo(
    plugin_id="mailflow-mail-outlook",
    name="Outlook Mail Source",
    version="0.1.0",
    description="IMAP/SMTP mail source for Outlook",
    kinds=[ComponentKind.MAIL_SOURCE],
)


class OutlookPlugin:
    def mailflow_plugin_info(self) -> PluginInfo:
        return PLUGIN_INFO

    def mailflow_register(self, registrar: PluginRegistrar, config: MailFlowConfig) -> None:
        registrar.add_source("outlook", OutlookSource)


plugin = OutlookPlugin()

__all__ = ["OutlookPlugin", "OutlookSource", "parse_mime", "plugin"]
