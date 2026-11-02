#!/usr/bin/env python3
"""Check plugin metadata and core contracts with simulated, offline I/O.

Use --offline with an existing development environment (no installation), or
omit it to install declared dependencies in a disposable virtual environment.
--core can select a local mailflow-core folder instead of the Git source.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
import tomllib
import venv
from pathlib import Path
from typing import Any

CATEGORIES = (
    "mail_source",
    "processor",
    "llm_backend",
    "llm_enhancer",
    "notifier",
    "storage",
    "bot_exporter",
    "gateway",
)
ROOT = Path(__file__).resolve().parent.parent
CORE_SOURCE = (
    "mailflow-core@git+https://github.com/Kingcxp/mailflow.git#subdirectory=packages/mailflow-core"
)
TESTKIT_SOURCE = "mailflow-testkit@git+https://github.com/Kingcxp/mailflow.git#subdirectory=packages/mailflow-testkit"


def _project(folder: Path) -> dict[str, Any]:
    return tomllib.loads((folder / "pyproject.toml").read_text(encoding="utf-8"))["project"]


def _failures(folder: Path) -> list[str]:
    try:
        metadata = json.loads((folder / "plugin.json").read_text(encoding="utf-8"))
        project = _project(folder)
    except (OSError, ValueError, KeyError) as exc:
        return [f"{folder.name}: {exc}"]
    errors: list[str] = []
    plugin_id = metadata.get("id")
    if plugin_id != folder.name:
        errors.append("plugin.json id must match the folder name")
    categories = metadata.get("categories", [])
    if len(categories) != 1 or categories[0] not in CATEGORIES:
        errors.append(f"categories must contain exactly one of {CATEGORIES}")
    elif folder.parent.name != categories[0]:
        errors.append("category must match the parent folder")
    if not metadata.get("package") or project.get("name") != metadata["package"]:
        errors.append("pyproject name must match plugin.json package")
    if project.get("version") != metadata.get("version"):
        errors.append("pyproject version must match plugin.json version")
    if not metadata.get("source"):
        errors.append("source is required")
    if not (metadata.get("readme") or metadata.get("readmes")):
        errors.append("readme or readmes is required")
    entries = project.get("entry-points", {}).get("mailflow.plugins", {})
    if plugin_id not in entries:
        errors.append(f"mailflow.plugins entry point {plugin_id!r} is missing")
    dependencies = project.get("dependencies", [])
    if not any(dependency.startswith("mailflow-core") for dependency in dependencies):
        errors.append("mailflow-core must be a declared dependency")
    return [f"{folder.name}: {error}" for error in errors]


def all_folders() -> list[Path]:
    return sorted(p.parent for c in CATEGORIES for p in (ROOT / c).glob("*/plugin.json"))


def _run(python: Path, folder: Path, *, offline: bool, core: Path | None) -> list[str]:
    env = os.environ.copy()
    if not offline:
        env.pop("PYTHONPATH", None)
    paths: list[str] = []
    if core is not None:
        paths.append(str(core / "src"))
        paths.append(str(core.parent / "mailflow-testkit" / "src"))
    if offline:
        # Local peers resolve shared transports without downloading the market.
        paths.extend(str(p / "src") for p in all_folders())
        paths.insert(0, str(folder / "src"))
    if paths:
        env["PYTHONPATH"] = os.pathsep.join([*paths, env.get("PYTHONPATH", "")])
    result = subprocess.run(
        [
            str(python),
            "-X",
            "utf8",
            "-B",
            str(ROOT / "tools/plugin_smoke.py"),
            str(folder),
            "--source" if offline else "--installed",
        ],
        cwd=ROOT,
        env=env,
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=60,
        check=False,
    )
    if result.returncode:
        lines = (result.stdout + result.stderr).strip().splitlines()
        reason = lines[-1] if lines else f"process exited with {result.returncode}"
        return [f"{folder.name}: contract check failed: {reason}"]
    return []


def _install_and_run(folder: Path, *, offline: bool = False, core: Path | None = None) -> list[str]:
    if offline:
        return _run(Path(sys.executable), folder, offline=True, core=core)
    with tempfile.TemporaryDirectory(prefix="mailflow-validate-") as scratch:
        environment = Path(scratch) / "venv"
        venv.EnvBuilder(with_pip=True).create(environment)
        python = environment / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
        pip = [
            str(python),
            "-m",
            "pip",
            "install",
            "--quiet",
            "--disable-pip-version-check",
        ]
        # Resolve core, shared samples and plugin together, so a conflicting
        # plugin cannot silently replace the selected core. Keep the host untouched.
        testkit = str(core.parent / "mailflow-testkit") if core else TESTKIT_SOURCE
        result = subprocess.run(
            [*pip, str(core) if core else CORE_SOURCE, testkit, str(folder)],
            cwd=ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=900,
            check=False,
        )
        if result.returncode:
            return [f"{folder.name}: install failed: {(result.stderr or result.stdout)[-1000:]}"]
        check = subprocess.run(
            [str(python), "-m", "pip", "check"],
            capture_output=True,
            text=True,
            check=False,
        )
        if check.returncode:
            return [f"{folder.name}: dependency check failed: {check.stdout.strip()}"]
        return _run(python, folder, offline=False, core=None)


def changed_folders(base: str = "main") -> list[Path]:
    """Include nested source edits, local edits, and shared validator changes."""
    names: set[str] = set()
    for args in (
        ["diff", "--name-only", f"{base}...HEAD"],
        ["diff", "--name-only", "HEAD"],
        ["ls-files", "--others", "--exclude-standard"],
    ):
        result = subprocess.run(
            ["git", *args],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode:
            return all_folders()
        names.update(result.stdout.splitlines())
    if any(name.startswith(("tools/", ".github/workflows/")) for name in names):
        return all_folders()
    folders: set[Path] = set()
    for name in names:
        parts = Path(name).parts
        if len(parts) >= 2 and parts[0] in CATEGORIES:
            folder = ROOT / parts[0] / parts[1]
            if (folder / "plugin.json").is_file():
                folders.add(folder)
    return sorted(folders)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--all", action="store_true")
    group.add_argument("--changed", action="store_true")
    parser.add_argument(
        "--offline",
        action="store_true",
        help="use local sources; never install or download",
    )
    parser.add_argument("--core", type=Path, help="local mailflow-core project folder")
    parser.add_argument("--base", default="main", help="base ref for --changed")
    parser.add_argument("folders", nargs="*")
    args = parser.parse_args()
    folders = (
        all_folders()
        if args.all
        else changed_folders(args.base)
        if args.changed
        else [(ROOT / f).resolve() for f in args.folders]
    )
    if not folders and not (args.all or args.changed):
        parser.error("pass folders, --all or --changed")
    core = args.core.resolve() if args.core else None
    failures = [error for folder in folders for error in _failures(folder)]
    if not failures:
        for folder in folders:
            print(f"validating {folder.name}", flush=True)
            try:
                failures.extend(_install_and_run(folder, offline=args.offline, core=core))
            except (OSError, subprocess.TimeoutExpired) as exc:
                failures.append(f"{folder.name}: {exc}")
    for error in failures:
        print(error)
    if not failures:
        print(f"ok: {len(folders)} plugin(s); signatures, capabilities and offline results checked")
    return int(bool(failures))


if __name__ == "__main__":
    sys.exit(main())
