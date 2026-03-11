# Stage 4 AuditShield Migration v2 — Apply Instructions

File drop from `stage4-auditshield-migration/`. No new code to write.

## Exact sequence (from Artifacts/project/auditshield/)

```bash
# A-01: pyproject.toml (starguard-core[badge])
cp stage4-auditshield-migration/pyproject.toml .

# A-02: audit_trail shim (replaces full implementation)
cp stage4-auditshield-migration/audit_trail.py .

# A-03: cloud_status_badge shim
cp stage4-auditshield-migration/cloud_status_badge.py .
```

## Caller updates

No import changes required — shims preserve `from audit_trail import ...` and `from cloud_status_badge import ...`.

**Tests:** If tests patch suppression file/cache, use:
- `starguard_core.audit.trail._SUPPRESSION_FILE`
- `starguard_core.audit.trail._AUDIT_SUPPRESSIONS_CACHE`

## Verify

```bash
python verify_stage4_migration.py
```

Verifier checks: pyproject, audit_trail shim, cloud_status_badge shim, suppression round-trip, DataFrame columns, badge Tag instantiation, 7-item cross-repo deletion sweep.

Green gate → Stage 4 complete.
