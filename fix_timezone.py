#!/usr/bin/env python3
"""
fix_timezone.py — Fix timezone label across all 3 apps

Replaces incorrect "EST" (was showing UTC) with actual 12-hour EST.
Uses datetime.timezone(timedelta(hours=-5)) — no pytz needed.

Run from project root:
    python fix_timezone.py
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent
AUDIT = ROOT / "Artifacts" / "project" / "auditshield"
DESKTOP = AUDIT / "starguard-desktop"
MOBILE = AUDIT / "starguard-mobile" / "Artifacts" / "app"

# Files and patterns to patch
PATCHES = [
    # (file, old_pattern, new_pattern)
    # cloud_status_badge — add EST, fix now line
    (AUDIT / "cloud_status_badge.py", "from datetime import datetime", "from datetime import datetime, timezone, timedelta"),
    (AUDIT / "cloud_status_badge.py", "now = datetime.now().strftime(\"%H:%M:%S EST\")", "EST = timezone(timedelta(hours=-5))\n    now = datetime.now(EST).strftime(\"%I:%M:%S %p EST\")"),
    (DESKTOP / "cloud_status_badge.py", "from datetime import datetime", "from datetime import datetime, timezone, timedelta"),
    (DESKTOP / "cloud_status_badge.py", "now = datetime.now().strftime(\"%H:%M:%S EST\")", "EST = timezone(timedelta(hours=-5))\n    now = datetime.now(EST).strftime(\"%I:%M:%S %p EST\")"),
    (MOBILE / "cloud_status_badge.py", "from datetime import datetime", "from datetime import datetime, timezone, timedelta"),
    (MOBILE / "cloud_status_badge.py", "now = datetime.utcnow().strftime(\"%H:%M:%S\") + \" UTC\"", "EST = timezone(timedelta(hours=-5))\n    now = datetime.now(EST).strftime(\"%I:%M:%S %p EST\")"),
    # audit_trail
    (AUDIT / "audit_trail.py", "from datetime import datetime", "from datetime import datetime, timezone, timedelta"),
    (AUDIT / "audit_trail.py", '"timestamp": datetime.now().strftime("%H:%M:%S EST")', '"timestamp": datetime.now(timezone(timedelta(hours=-5))).strftime("%I:%M:%S %p EST")'),
    (AUDIT / "audit_trail.py", 'now.strftime("%H:%M:%S EST")', 'now.strftime("%I:%M:%S %p EST")'),
    # Need to fix audit_trail: now = datetime.now() should be now = datetime.now(tz=timezone(timedelta(hours=-5))) for the row that uses now.strftime
    (AUDIT / "audit_trail.py", "now = datetime.now()", "now = datetime.now(timezone(timedelta(hours=-5)))"),
    # hedis_gap_trail — desktop
    (DESKTOP / "hedis_gap_trail.py", "from datetime import datetime", "from datetime import datetime, timezone, timedelta"),
    (DESKTOP / "hedis_gap_trail.py", '"timestamp": datetime.now().strftime("%H:%M:%S EST")', '"timestamp": datetime.now(timezone(timedelta(hours=-5))).strftime("%I:%M:%S %p EST")'),
    (DESKTOP / "hedis_gap_trail.py", "now = datetime.now()", "now = datetime.now(timezone(timedelta(hours=-5)))"),
    (DESKTOP / "hedis_gap_trail.py", 'now.strftime("%H:%M:%S EST")', 'now.strftime("%I:%M:%S %p EST")'),
    # hedis_gap_trail — mobile (has UTC)
    (MOBILE / "hedis_gap_trail.py", "from datetime import datetime", "from datetime import datetime, timezone, timedelta"),
    (MOBILE / "hedis_gap_trail.py", '"timestamp": datetime.utcnow().strftime("%H:%M:%S") + " UTC"', '"timestamp": datetime.now(timezone(timedelta(hours=-5))).strftime("%I:%M:%S %p EST")'),
    (MOBILE / "hedis_gap_trail.py", "now = datetime.now()", "now = datetime.now(timezone(timedelta(hours=-5)))"),
    (MOBILE / "hedis_gap_trail.py", 'now.strftime("%H:%M:%S") + " UTC"', 'now.strftime("%I:%M:%S %p EST")'),
    # star_rating_cache — desktop
    (DESKTOP / "star_rating_cache.py", "from datetime import datetime", "from datetime import datetime, timezone, timedelta"),
    (DESKTOP / "star_rating_cache.py", '"timestamp":      datetime.now().strftime("%H:%M:%S EST")', '"timestamp": datetime.now(timezone(timedelta(hours=-5))).strftime("%I:%M:%S %p EST")'),
    (DESKTOP / "star_rating_cache.py", "now = datetime.now()", "now = datetime.now(timezone(timedelta(hours=-5)))"),
    (DESKTOP / "star_rating_cache.py", '"timestamp":   now.strftime("%H:%M:%S EST")', '"timestamp": now.strftime("%I:%M:%S %p EST")'),
    # star_rating_cache — mobile (has UTC)
    (MOBILE / "star_rating_cache.py", "from datetime import datetime", "from datetime import datetime, timezone, timedelta"),
    (MOBILE / "star_rating_cache.py", '"timestamp": datetime.utcnow().strftime("%H:%M:%S") + " UTC"', '"timestamp": datetime.now(timezone(timedelta(hours=-5))).strftime("%I:%M:%S %p EST")'),
    (MOBILE / "star_rating_cache.py", "now = datetime.now()", "now = datetime.now(timezone(timedelta(hours=-5)))"),
    (MOBILE / "star_rating_cache.py", 'now.strftime("%H:%M:%S") + " UTC"', 'now.strftime("%I:%M:%S %p EST")'),
]


def main():
    print("Applying timezone fix across all 3 apps...")
    done = set()
    for path, old, new in PATCHES:
        if not path.exists():
            print(f"[SKIP] {path.relative_to(ROOT)} — not found")
            continue
        text = path.read_text(encoding="utf-8")
        if new in text:
            print(f"[OK]   {path.relative_to(ROOT)} — already patched")
            done.add(path)
            continue
        if old not in text:
            print(f"[WARN] {path.relative_to(ROOT)} — pattern not found")
            continue
        text = text.replace(old, new, 1)
        path.write_text(text, encoding="utf-8")
        print(f"[FIX]  {path.relative_to(ROOT)}")
    print("\nDone. Restart apps and push to deploy.")


if __name__ == "__main__":
    main()
