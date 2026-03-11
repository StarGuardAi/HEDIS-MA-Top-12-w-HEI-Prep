#!/usr/bin/env python3
"""Stage 4 AuditShield auth verifier - 7 checks for starguard-core integration."""
import subprocess
import sys


def run(cmd: list[str], cwd: str | None = None) -> tuple[bool, str]:
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=cwd, timeout=60)
    return r.returncode == 0, (r.stdout or "") + (r.stderr or "")


def main() -> int:
    root = __file__.replace("\\", "/").rsplit("/", 1)[0]
    py = sys.executable

    checks = [
        ("Step 1 - importable", [py, "-c", "from starguard_core.auth import validate_api_key, is_feature_enabled; print('OK importable')"]),
        (
            "Step 2 - all tiers (FREE, PRO)",
            [
                py,
                "-c",
                "from starguard_core.auth import validate_api_key, Tier; assert validate_api_key(None).tier == Tier.FREE; assert validate_api_key('pro-TESTKEY0000000001').tier == Tier.PRO; print('OK All tiers correct')",
            ],
        ),
        (
            "Step 3 - RADV gating (hedis_predictions = Pro)",
            [
                py,
                "-c",
                "from starguard_core.auth import get_tier_config, is_feature_enabled; assert not is_feature_enabled('hedis_predictions', get_tier_config(None)); assert is_feature_enabled('hedis_predictions', get_tier_config('pro-TESTKEY0000000001')); print('OK RADV gating correct')",
            ],
        ),
        (
            "Step 4 - lead capture",
            [
                py,
                "-c",
                "from starguard_core.auth import capture_lead; capture_lead('test@example.com', source='auditshield_radv'); print('OK Lead capture')",
            ],
        ),
        (
            "Step 5 - usage tracking",
            [
                py,
                "-c",
                "from starguard_core.auth import increment_usage, get_usage_count; increment_usage('pro-TESTKEY0000000001', 'hedis_predictions', 'AuditShield-Live'); assert get_usage_count('pro-TESTKEY0000000001', 'hedis_predictions') >= 1; print('OK Usage tracking')",
            ],
        ),
        ("Step 6 — existing test suite", [py, "-m", "pytest", "tests/", "-v", "--tb=short"]),
        ("Step 7 - app smoke test", [py, "-c", "import app; print('OK AuditShield imports clean')"]),
    ]

    failed = []
    for name, cmd in checks:
        ok, out = run(cmd, cwd=root)
        if ok:
            print(f"[OK] {name}")
        else:
            print(f"[FAIL] {name}")
            print(out[:800])
            failed.append(name)

    if failed:
        print(f"\nFailed: {failed}")
        return 1
    print("\n[OK] AuditShield gate clear - all 7 checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
