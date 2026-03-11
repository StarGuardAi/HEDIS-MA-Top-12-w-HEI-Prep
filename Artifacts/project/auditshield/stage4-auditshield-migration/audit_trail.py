# audit_trail.py — Stage 4 shim
# ─────────────────────────────────────────────────────────────
# Re-exports from starguard_core.audit.trail for backward compatibility.
# logic/ audit_trail.py (full implementation) deleted.
#
# Before: from audit_trail import get_audit_suppressions, push_audit_record, ...
# After:  same import works; implementation in starguard_core.
#
# Install: pip install starguard-core (or starguard-core[badge] for full app)
#
# Tests: If patching suppression file/cache, use:
#   starguard_core.audit.trail._SUPPRESSION_FILE
#   starguard_core.audit.trail._AUDIT_SUPPRESSIONS_CACHE
# ─────────────────────────────────────────────────────────────

from starguard_core.audit.trail import (
    AUDIT_COLUMNS,
    AuditTrailDB,
    add_audit_suppression,
    fetch_recent_audits,
    get_audit_suppressions,
    push_audit_record,
    remove_audit_suppression,
    update_audit_status,
)

__all__ = [
    "AUDIT_COLUMNS",
    "AuditTrailDB",
    "add_audit_suppression",
    "fetch_recent_audits",
    "get_audit_suppressions",
    "push_audit_record",
    "remove_audit_suppression",
    "update_audit_status",
]
