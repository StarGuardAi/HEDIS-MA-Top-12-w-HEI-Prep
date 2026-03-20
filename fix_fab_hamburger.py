#!/usr/bin/env python3
"""Verify FAB wiring: no Shiny.setInputValue for nav; injected #rsi-hamburger script present."""
from __future__ import annotations

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent
FAB = REPO / "Artifacts" / "project" / "auditshield" / "ui" / "fab_wiring.py"


def main() -> None:
    if not FAB.is_file():
        print(f"ERROR: missing {FAB}", file=sys.stderr)
        sys.exit(1)
    t = FAB.read_text(encoding="utf-8")
    bad = bool(re.search(r"setInputValue\s*\(\s*MT", t))
    good_h = "rsi-hamburger" in t and "ensureMobileHamburger" in t
    good_toggle = "toggleNativeSidebar" in t and "collapse-toggle" in t
    checks = [
        ("No Shiny.setInputValue(MT, …) in fab_wiring", not bad),
        ("Injected mobile hamburger (#rsi-hamburger)", good_h),
        ("collapse-toggle / Offcanvas fallback", good_toggle),
    ]
    ok_all = True
    for name, ok in checks:
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}")
        if not ok:
            ok_all = False
    if not ok_all:
        sys.exit(1)
    print("\nAll checks passed.")


if __name__ == "__main__":
    main()
