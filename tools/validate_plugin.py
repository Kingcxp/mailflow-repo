#!/usr/bin/env python3
"""Validate one or more plugin folders of the MailFlow plugin marketplace.

Run by the pull-request workflow (.github/workflows/validate-plugins.yml) and
usable locally. Checks that a plugin is legal (metadata consistent), loadable
(entry point imports, mailflow_plugin_info reports) and runnable (every
registered factory instantiates; processors additionally process a sample
mail).

Usage:
    python tools/validate_plugin.py notifier/mailflow-notify-ntfy
    python tools/validate_plugin.py --all
    python tools/validate_plugin.py --changed   # git diff against main (CI)

The environment must have mailflow-core importable.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

CATEGORIES = ("mail_source", "processor", "llm_backend", "notifier", "storage", "bot_exporter")
ROOT = Path(__file__).resolve().parent.parent


def _failures(folder: Path) -> list[str]:
    errors: list[str] = []
    plugin_json = folder / "plugin.json"
    if not plugin_json.is_file():
        return [f"{folder.name}: plugin.json missing"]
    try:
        metadata = json.loads(plugin_json.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"{folder.name}: plugin.json is not valid JSON: {exc}"]

    plugin_id = str(metadata.get("id", ""))
    if plugin_id != folder.name:
        errors.append(f"{folder.name}: plugin.json id {plugin_id!r} != folder name")
    categories = metadata.get("categories") or []
    if len(categories) != 1 or categories[0] not in CATEGORIES:
        errors.append(f"{folder.name}: categories must be exactly one of {CATEGORIES}")
    if not metadata.get("package"):
        errors.append(f"{folder.name}: package is required (must match pyproject name)")
    if not metadata.get("source"):
        errors.append(f"{folder.name}: source is required (where to install from)")
    if not (metadata.get("readme") or metadata.get("readmes")):
        errors.append(f"{folder.name}: readme (or readmes.*) is required")

    pyproject = folder / "pyproject.toml"
    if not pyproject.is_file():
        return errors + [f"{folder.name}: pyproject.toml missing"]
    text = pyproject.read_text(encoding="utf-8")
    name_match = re.search(r'^name\s*=\s*"([^"]+)"', text, re.MULTILINE)
    if not name_match or name_match.group(1) != metadata.get("package"):
        errors.append(
            f"{folder.name}: pyproject name {name_match and name_match.group(1)!r} "
            f"!= plugin.json package {metadata.get('package')!r}"
        )
    entry = re.search(
        r'\[\s*project\.entry-points\."mailflow\.plugins"\s*\](.*?)(?=\n\[|\Z)',
        text,
        re.DOTALL,
    )
    if not entry or plugin_id not in entry.group(1):
        errors.append(f"{folder.name}: pyproject entry point for {plugin_id!r} missing")
    return errors


def _install_and_run(folder: Path) -> list[str]:
    """Install into a scratch environment and run the mailflow checks."""
    errors: list[str] = []
    with tempfile.TemporaryDirectory(prefix="mailflow-validate-") as _scratch:
        python = Path(sys.executable).resolve()
        pip = [str(python), "-m", "pip", "install", "--quiet", "--disable-pip-version-check"]
        # --force-reinstall: a same-version core already present (e.g. from a
        # previous run) must not shadow the freshly published HEAD. Deps are
        # reinstalled too so a fresh CI environment gets everything.
        core = subprocess.run(
            pip
            + [
                "--force-reinstall",
                "mailflow-core@git+https://github.com/Kingcxp/mailflow.git"
                "#subdirectory=packages/mailflow-core",
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=900,
        )
        if core.returncode != 0:
            return [f"{folder.name}: could not install mailflow-core: {core.stderr[-400:]}"]

        install = subprocess.run(
            pip + ["--no-deps", "."], cwd=folder, capture_output=True, text=True, timeout=600
        )
        if install.returncode != 0:
            return [f"{folder.name}: pip install failed: {install.stderr[-400:]}"]

        script = """
import asyncio
import sys
from datetime import datetime, timezone

from mailflow.config import (
    LLMConfig, MailAccountConfig, MailFlowConfig, NotifierConfig,
    ProcessorConfig, StorageConfig,
)
from mailflow.contracts import ProcessingContext
from mailflow.domain import ComponentKind, MailAddress, MailMessage
from mailflow.plugins import make_manager

plugin_id = sys.argv[1]
manager = make_manager(discover_plugins=True)
infos = {i.plugin_id: i for i in manager.enabled_infos()}
if plugin_id not in infos:
    sys.exit("plugin not discovered via the mailflow.plugins entry point")
info = infos[plugin_id]
if not info.kinds:
    sys.exit("plugin reports no component kinds")
print("discovered:", info.plugin_id, [k.value for k in info.kinds])

registry = manager.build_registry()
config = MailFlowConfig()
registered = [(s.kind, s.component_id) for s in registry.snapshots() if s.plugin_id == plugin_id]
if not registered:
    sys.exit("plugin registered no components")

def make_factory_arg(kind):
    if kind is ComponentKind.MAIL_SOURCE:
        return (MailAccountConfig(account_id="validation", provider="validation"),)
    if kind is ComponentKind.LLM_BACKEND:
        return (LLMConfig(llm_id="validation", provider="validation"),)
    if kind is ComponentKind.MAIL_PROCESSOR:
        class NullRouter:
            async def chat(self, messages, **kwargs):
                raise RuntimeError("router not available during validation")
        return (ProcessorConfig(processor_id="validation", provider="validation"), NullRouter())
    if kind is ComponentKind.NOTIFIER:
        return (NotifierConfig(notifier_id="validation", provider="validation"),)
    if kind is ComponentKind.STORAGE:
        return (StorageConfig(provider="validation"),)
    if kind is ComponentKind.BOT_EXPORTER:
        from pathlib import Path
        import tempfile as _scratch_dir
        from mailflow.bot_export import BotExportContext
        return (
            BotExportContext(
                config=MailFlowConfig(),
                plugin_ids=[],
                output_dir=Path(_scratch_dir.mkdtemp()),
            ),
        )
    return ()

for kind, component_id in registered:
    instance = registry.factory(kind, component_id)(*make_factory_arg(kind))
    if instance is None:
        sys.exit(f"factory for {component_id} returned None")
    print("instantiated:", kind.value, component_id)

processors = [cid for k, cid in registered if k is ComponentKind.MAIL_PROCESSOR]
for component_id in processors:
    proc = registry.processor_factory(component_id)(*make_factory_arg(ComponentKind.MAIL_PROCESSOR))
    mail = MailMessage(
        message_id="validation-sample", account_id="validation",
        subject="Validation mail", sender=MailAddress(address="sender@example.com"),
        recipients=[MailAddress(address="me@example.com")],
        date=datetime.now(timezone.utc), received_at=datetime.now(timezone.utc),
    )
    result = asyncio.run(proc.process(mail, ProcessingContext(account_id="validation")))
    print("processor ran:", component_id, getattr(result, "notes", None))
"""
        run = subprocess.run(
            [str(python), "-c", script, folder.name],
            capture_output=True,
            text=True,
            timeout=600,
        )
        if run.returncode != 0:
            errors.append(f"{folder.name}: load/run check failed: {(run.stdout + run.stderr)[-600:]}")
    return errors


def changed_folders(base: str = "main") -> list[Path]:
    """Folders touched by the working tree / PR head vs base."""
    diff = subprocess.run(
        ["git", "diff", "--name-only", f"{base}...HEAD"],
        cwd=ROOT, capture_output=True, text=True, check=False,
    )
    if diff.returncode != 0:
        # fall back to a full sweep
        return [p for c in CATEGORIES for p in (ROOT / c).glob("*/") if (p / "plugin.json").is_file()]
    folders: list[Path] = []
    for line in diff.stdout.splitlines():
        path = ROOT / line
        if not path.exists():
            continue
        if (path / "plugin.json").is_file():
            folders.append(path)
        else:
            parent = path.parent
            if (parent / "plugin.json").is_file() and parent not in folders:
                folders.append(parent)
    return sorted(set(folders))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--all", action="store_true", help="validate every plugin folder")
    group.add_argument("--changed", action="store_true", help="validate only changed plugins")
    parser.add_argument("folders", nargs="*", help="plugin folders to validate")
    args = parser.parse_args()

    if args.all:
        folders = [p for c in CATEGORIES for p in (ROOT / c).glob("*/") if (p / "plugin.json").is_file()]
    elif args.changed:
        folders = changed_folders()
    else:
        folders = [ROOT / f for f in args.folders]
        if not folders:
            parser.error("pass plugin folders, or use --all / --changed")

    if not folders:
        print("no plugin changes to validate")
        return 0

    failures: list[str] = []
    for folder in folders:
        print(f"validating {folder.relative_to(ROOT)}")
        failures.extend(_failures(folder))
    if failures:
        print("\nFAILED:")
        for error in failures:
            print(" -", error)
        return 1
    for folder in folders:
        failures.extend(_install_and_run(folder))
    if failures:
        print("\nFAILED:")
        for error in failures:
            print(" -", error)
        return 1
    print(f"\nok: {len(folders)} plugin(s) valid, loadable and runnable")
    return 0


if __name__ == "__main__":
    sys.exit(main())
