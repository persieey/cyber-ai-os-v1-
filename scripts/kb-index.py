#!/usr/bin/env python3
"""
scripts/kb-index.py — List and search the Knowledge Base
Usage:
  python3 scripts/kb-index.py              # list all entries
  python3 scripts/kb-index.py <keyword>    # search by keyword
"""

import sys
import os
from pathlib import Path

ROOT = Path(__file__).parent.parent
KB = ROOT / "knowledge"


def list_entries(keyword: str = "") -> None:
    entries = []

    for md in sorted(KB.rglob("*.md")):
        if md.name == "README.md":
            continue
        rel = md.relative_to(KB)
        content = md.read_text(encoding="utf-8", errors="ignore")
        title_line = next((l for l in content.splitlines() if l.startswith("# ")), str(rel))
        title = title_line.lstrip("# ").strip()

        if keyword and keyword.lower() not in (title + content).lower():
            continue

        entries.append((str(rel), title))

    if not entries:
        print(f"  (no results for '{keyword}')")
        return

    cat = ""
    for path, title in entries:
        top = path.split(os.sep)[0]
        if top != cat:
            cat = top
            print(f"\n  [{cat}]")
        print(f"    {title}")
        print(f"      → knowledge/{path}")


def main():
    kw = sys.argv[1] if len(sys.argv) > 1 else ""
    print("=" * 50)
    if kw:
        print(f"  Knowledge Base — Search: '{kw}'")
    else:
        print("  Knowledge Base — All Entries")
    print("=" * 50)
    list_entries(kw)
    print()


if __name__ == "__main__":
    main()
