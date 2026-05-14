"""One-off smoke test — cross_app_findings insert verification.

Run from any app directory that has shared/ on the path, e.g.:
    cd Artifacts/project/auditshield
    python ../../../scripts/smoke_test_findings.py

Or from Artifacts/ root with PYTHONPATH set:
    cd Artifacts
    PYTHONPATH=shared python scripts/smoke_test_findings.py

Requires env vars (or .env loaded below):
    PLATFORM_SUPABASE_URL      https://jdvtlonnejybqivcjtsj.supabase.co
    PLATFORM_SUPABASE_ANON_KEY  <anon key>
  OR
    SUPABASE_URL
    SUPABASE_ANON_KEY
"""
from __future__ import annotations

import os
import sys
import uuid

# ---------------------------------------------------------------------------
# Optional: load .env if python-dotenv is available
# ---------------------------------------------------------------------------
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("[smoke] .env loaded")
except ImportError:
    print("[smoke] python-dotenv not installed — using existing env vars")

# ---------------------------------------------------------------------------
# Resolve path so shared/ is importable regardless of cwd
# ---------------------------------------------------------------------------
_HERE = os.path.dirname(os.path.abspath(__file__))
_SHARED = os.path.join(_HERE, "..", "shared")
if os.path.isdir(_SHARED):
    sys.path.insert(0, _SHARED)
    print(f"[smoke] shared/ found at {os.path.abspath(_SHARED)}")
else:
    print(f"[smoke] WARNING: shared/ not found at {_SHARED} — adjust path if import fails")

from supabase_findings import insert_finding  # noqa: E402

# ---------------------------------------------------------------------------
# Test matrix — one insert per app bucket
# ---------------------------------------------------------------------------
TEST_CASES = [
    dict(
        source_app="auditshield",
        finding_type="audit_flag",
        severity="info",
        status="open",
        title="[SMOKE TEST] Mock audit run",
        trigger_type="action",
        extra_metadata={"action": "smoke_test", "env": "local"},
    ),
    dict(
        source_app="starguard",
        finding_type="star_gap",
        severity="info",
        status="open",
        title="[SMOKE TEST] HEDIS run",
        trigger_type="action",
        extra_metadata={"action": "smoke_test", "env": "local"},
    ),
    dict(
        source_app="sovereignshield",
        finding_type="policy_violation",
        severity="medium",
        status="open",
        title="[SMOKE TEST] OPA eval",
        trigger_type="action",
        extra_metadata={"action": "smoke_test", "env": "local"},
    ),
]

# ---------------------------------------------------------------------------
# Run inserts
# ---------------------------------------------------------------------------
_SESSION_ID = str(uuid.uuid4())
print(f"\n[smoke] session_id: {_SESSION_ID}")
print(f"[smoke] PLATFORM_SUPABASE_URL: {os.environ.get('PLATFORM_SUPABASE_URL') or os.environ.get('SUPABASE_URL', 'NOT SET')}\n")

passed = 0
failed = 0

for tc in TEST_CASES:
    ok = insert_finding(session_id=_SESSION_ID, **tc)
    status = "PASS" if ok else "FAIL"
    if ok:
        passed += 1
    else:
        failed += 1
    print(f"  [{status}] source_app={tc['source_app']} finding_type={tc['finding_type']}")

# Session-end row (remediated — should not inflate open counts)
ok = insert_finding(
    source_app="auditshield",
    finding_type="session_end",
    severity="info",
    status="remediated",
    title="[SMOKE TEST] Session ended",
    trigger_type="session_end",
    session_id=_SESSION_ID,
    extra_metadata={"action": "smoke_test_teardown"},
)
print(f"  [{'PASS' if ok else 'FAIL'}] session-end row (status=remediated)")
if ok:
    passed += 1
else:
    failed += 1

print(f"\n[smoke] Results: {passed} passed / {failed} failed")

if failed == 0:
    print("[smoke] All inserts succeeded.")
    print("[smoke] Next: open Supabase Table Editor → cross_app_findings")
    print("         Filter: title LIKE '[SMOKE TEST]%' to see your rows.")
    print("         Then open Platform Hub — KPI strip should show non-zero counts.")
else:
    print("[smoke] One or more inserts failed — check stderr above for details.")
    print("        Common causes:")
    print("          1. PLATFORM_SUPABASE_URL / SUPABASE_URL not set")
    print("          2. Column name mismatch — run schema verification queries")
    print("          3. severity CHECK constraint excludes 'info' — run migration")
    sys.exit(1)
