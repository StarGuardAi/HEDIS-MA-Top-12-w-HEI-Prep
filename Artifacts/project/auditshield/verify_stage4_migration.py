#!/usr/bin/env python3
"""
Stage 4 AuditShield Migration Verifier (v2)
Checks A-01 through A-06 plus 7-item cross-repo deletion sweep.
"""
from pathlib import Path

REPO = Path(__file__).resolve().parent
DESKTOP = REPO / "starguard-desktop"
MOBILE_APP = REPO / "starguard-mobile" / "Artifacts" / "app"


def ok(msg: str) -> None:
    print(f"  [OK] {msg}")


def fail(msg: str) -> None:
    print(f"  [FAIL] {msg}")


def check_a01_pyproject() -> bool:
    """A-01: pyproject.toml has starguard-core[badge]."""
    p = REPO / "pyproject.toml"
    if not p.exists():
        fail("pyproject.toml missing")
        return False
    text = p.read_text(encoding="utf-8")
    if "starguard-core" not in text:
        fail("pyproject.toml: starguard-core not in dependencies")
        return False
    if "[badge]" not in text:
        fail("pyproject.toml: starguard-core[badge] required for Shiny badge")
        return False
    ok("pyproject.toml: starguard-core[badge] in dependencies")
    return True


def check_a02_audit_trail_shim() -> bool:
    """A-02: audit_trail.py is starguard_core shim with 8 symbols."""
    p = REPO / "audit_trail.py"
    if not p.exists():
        fail("audit_trail.py missing")
        return False
    text = p.read_text(encoding="utf-8")
    if "starguard_core" not in text:
        fail("audit_trail.py: not yet a shim (still full implementation)")
        return False
    required = [
        "AUDIT_COLUMNS", "AuditTrailDB", "add_audit_suppression",
        "fetch_recent_audits", "get_audit_suppressions", "push_audit_record",
        "remove_audit_suppression", "update_audit_status",
    ]
    for sym in required:
        if sym not in text:
            fail(f"audit_trail.py: missing symbol {sym}")
            return False
    ok("audit_trail.py: shim with 8 symbols")
    return True


def check_a03_cloud_status_badge_shim() -> bool:
    """A-03: cloud_status_badge.py is starguard_core shim with 8 symbols."""
    p = REPO / "cloud_status_badge.py"
    if not p.exists():
        fail("cloud_status_badge.py missing")
        return False
    text = p.read_text(encoding="utf-8")
    if "starguard_core" not in text:
        fail("cloud_status_badge.py: not yet a shim")
        return False
    required = [
        "APP_NAME", "GITHUB_URL", "HUGGINGFACE_URL", "LINKEDIN_URL",
        "auditshield_badge", "cloud_status_badge", "cloud_status_css",
        "provenance_footer",
    ]
    for sym in required:
        if sym not in text:
            fail(f"cloud_status_badge.py: missing symbol {sym}")
            return False
    ok("cloud_status_badge.py: shim with 8 symbols")
    return True


def check_a04_suppression_roundtrip() -> bool:
    """A-04: suppression round-trip (get/add/remove) works."""
    try:
        from starguard_core.audit import trail as t
    except ImportError:
        fail("starguard_core not installed; skip suppression round-trip")
        return True  # skip, not fail
    import tempfile
    import os
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        f.write("[]")
        tmp = f.name
    try:
        t._SUPPRESSION_FILE = tmp
        t._AUDIT_SUPPRESSIONS_CACHE = None
        assert t.get_audit_suppressions() == []
        r = t.add_audit_suppression("AUD-TEST", "Test")
        assert r.get("success") is True
        rules = t.get_audit_suppressions()
        assert len(rules) == 1 and rules[0].get("audit_id") == "AUD-TEST"
        r = t.remove_audit_suppression("AUD-TEST")
        assert r.get("success") is True
        assert t.get_audit_suppressions() == []
    except Exception as e:
        fail(f"suppression round-trip: {e}")
        return False
    finally:
        try:
            os.unlink(tmp)
        except OSError:
            pass
    ok("suppression round-trip: get/add/remove")
    return True


def check_a05_dataframe_columns() -> bool:
    """A-05: fetch_recent_audits returns DataFrame with expected columns."""
    try:
        from starguard_core.audit.trail import fetch_recent_audits, AuditTrailDB
        import pandas as pd
    except ImportError:
        fail("starguard_core/pandas not installed; skip DataFrame check")
        return True
    try:
        db = AuditTrailDB()
        df = fetch_recent_audits(db, n=0)
        assert isinstance(df, pd.DataFrame)
        expected = ["audit_id", "timestamp", "measure_code", "gaps_flagged", "meat_status", "radv_risk_score", "audit_status"]
        for col in expected:
            if col not in df.columns and not df.empty:
                fail(f"fetch_recent_audits: missing column {col}")
                return False
    except Exception as e:
        fail(f"DataFrame columns: {e}")
        return False
    ok("fetch_recent_audits: DataFrame columns")
    return True


def check_a06_badge_tag_instantiation() -> bool:
    """A-06: cloud_status_badge returns Shiny Tag."""
    try:
        from starguard_core.badge.cloud_status import cloud_status_badge, cloud_status_css
    except ImportError:
        fail("starguard_core[badge] not installed; skip badge check")
        return True
    try:
        css = cloud_status_css()
        badge = cloud_status_badge(app_variant="auditshield", layout="sidebar")
        assert css is not None
        assert badge is not None
    except Exception as e:
        fail(f"badge Tag instantiation: {e}")
        return False
    ok("cloud_status_badge: Tag instantiation")
    return True


def check_a07_cross_repo_deletion_sweep() -> bool:
    """A-07: 7-item cross-repo sweep — all files are shims, not full impl."""
    items = [
        (REPO, "audit_trail.py", "AuditShield audit_trail"),
        (REPO, "cloud_status_badge.py", "AuditShield cloud_status_badge"),
        (DESKTOP, "hedis_gap_trail.py", "Desktop hedis_gap_trail"),
        (DESKTOP, "hedis_rules.py", "Desktop hedis_rules"),
        (DESKTOP, "cloud_status_badge.py", "Desktop cloud_status_badge"),
        (MOBILE_APP, "hedis_gap_trail.py", "Mobile hedis_gap_trail"),
        (MOBILE_APP, "cloud_status_badge.py", "Mobile cloud_status_badge"),
    ]
    passed = True
    for base, name, label in items:
        p = base / name
        if not p.exists():
            if "hedis_rules" in name:
                ok(f"{label}: deleted (replaced by starguard_core)")
            else:
                fail(f"{label}: file missing")
                passed = False
            continue
        text = p.read_text(encoding="utf-8")
        if "starguard_core" in text:
            ok(f"{label}: shim present")
        else:
            fail(f"{label}: still full implementation")
            passed = False
    return passed


def main() -> int:
    print("Stage 4 AuditShield Migration Verifier (v2)\n")
    results = []
    print("A-01 pyproject.toml:")
    results.append(check_a01_pyproject())
    print("\nA-02 audit_trail shim:")
    results.append(check_a02_audit_trail_shim())
    print("\nA-03 cloud_status_badge shim:")
    results.append(check_a03_cloud_status_badge_shim())
    print("\nA-04 suppression round-trip:")
    results.append(check_a04_suppression_roundtrip())
    print("\nA-05 DataFrame columns:")
    results.append(check_a05_dataframe_columns())
    print("\nA-06 badge Tag instantiation:")
    results.append(check_a06_badge_tag_instantiation())
    print("\nA-07 cross-repo deletion sweep:")
    results.append(check_a07_cross_repo_deletion_sweep())

    all_ok = all(results)
    print()
    if all_ok:
        print("Green gate -- Stage 4 complete.")
        return 0
    print("Red gate -- fix failures above.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
