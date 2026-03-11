# cloud_status_badge.py — Stage 4 shim
# ─────────────────────────────────────────────────────────────
# Re-exports from starguard_core.badge.cloud_status for backward compatibility.
# AuditShield config: APP_NAME=AuditShield-Live, HF_SPACE_URL=tinyurl.com/2vj79bem
#
# Before: from cloud_status_badge import cloud_status_css, cloud_status_badge, ...
# After:  same import works; implementation in starguard_core.
#
# Install: pip install starguard-core[badge]
# ─────────────────────────────────────────────────────────────

import os

# AuditShield defaults (override via env in app_complete.py)
os.environ.setdefault("APP_NAME", "AuditShield-Live")
os.environ.setdefault("HF_SPACE_URL", "https://tinyurl.com/2vj79bem")

from starguard_core.badge.cloud_status import (
    APP_NAME,
    GITHUB_URL,
    HUGGINGFACE_URL,
    LINKEDIN_URL,
    auditshield_badge,
    cloud_status_badge,
    cloud_status_css,
    provenance_footer,
)

__all__ = [
    "APP_NAME",
    "GITHUB_URL",
    "HUGGINGFACE_URL",
    "LINKEDIN_URL",
    "auditshield_badge",
    "cloud_status_badge",
    "cloud_status_css",
    "provenance_footer",
]
