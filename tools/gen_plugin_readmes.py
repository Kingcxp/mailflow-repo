#!/usr/bin/env python3
"""Generate each plugin's README.md from its plugin.json readme.

`plugin.json` is the single source of truth: the marketplace client renders
`readme` (and `readmes.<lang>`) in `plugin market show` and in the TUI detail
view. A separate hand-written README.md drifts from it — this script derives
the file instead, so browsing the repository on GitHub and browsing it from
inside MailFlow show the same text.

Usage:
    python tools/gen_plugin_readmes.py          # write/refresh every README
    python tools/gen_plugin_readmes.py --check  # fail if any is out of date
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

HEADER = "<!-- Generated from plugin.json by tools/gen_plugin_readmes.py. Edit plugin.json. -->"


def render(metadata: dict[str, object], folder: Path) -> str:
    """The README body for one plugin: English readme plus translations."""
    readme = str(metadata.get("readme", "")).rstrip()
    if not readme:
        raise SystemExit(f"{folder.name}: plugin.json has no 'readme'")

    parts = [HEADER, "", readme, ""]

    raw_translations = metadata.get("readmes")
    if isinstance(raw_translations, dict):
        translations: dict[str, str] = {
            str(code): str(text) for code, text in raw_translations.items()
        }
        for code in sorted(translations):
            text = translations[code].rstrip()
            if text:
                parts += ["---", "", f"<!-- {code} -->", "", text, ""]

    homepage = str(metadata.get("homepage", ""))
    if homepage:
        parts += [
            "---",
            "",
            f"Metadata: [`plugin.json`](plugin.json) · Marketplace: [{homepage}]({homepage})",
            "",
        ]
    return "\n".join(parts)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="only report stale files")
    args = parser.parse_args()

    stale: list[str] = []
    written = 0
    for plugin_json in sorted(ROOT.glob("*/mailflow-*/plugin.json")):
        folder = plugin_json.parent
        metadata: dict[str, object] = json.loads(
            plugin_json.read_text(encoding="utf-8")
        )
        expected = render(metadata, folder)
        target = folder / "README.md"
        current = target.read_text(encoding="utf-8") if target.is_file() else ""
        if current == expected:
            continue
        relative = target.relative_to(ROOT).as_posix()
        if args.check:
            stale.append(relative)
            continue
        target.write_text(expected, encoding="utf-8")
        print(f"wrote {relative}")
        written += 1

    if args.check:
        if stale:
            print("plugin READMEs are out of date with plugin.json:")
            for path in stale:
                print(f"  - {path}")
            print("run: python tools/gen_plugin_readmes.py")
            return 1
        print("plugin READMEs match plugin.json")
        return 0

    print(f"{written} README(s) refreshed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
