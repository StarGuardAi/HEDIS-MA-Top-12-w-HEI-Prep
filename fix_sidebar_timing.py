#!/usr/bin/env python3
"""Verify fab_wiring retry loop for bslib Sidebar.getInstance timing."""
from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent
FAB = REPO / "Artifacts" / "project" / "auditshield" / "ui" / "fab_wiring.py"


def main() -> None:
    if not FAB.is_file():
        print(f"ERROR: missing {FAB}", file=sys.stderr)
        sys.exit(1)
    t = FAB.read_text(encoding="utf-8")
    checks = [
        ("toggleNativeSidebarFallback", "toggleNativeSidebarFallback" in t),
        ("maxAttempts = 10", "maxAttempts = 10" in t),
        ("delayMs = 200", "delayMs = 200" in t),
        ("recursive attempt + setTimeout", "attempt(i + 1)" in t and "setTimeout" in t),
        ("exhausted: toggleNativeSidebarFallback()", "toggleNativeSidebarFallback();" in t),
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
