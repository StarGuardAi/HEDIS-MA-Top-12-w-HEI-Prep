# Phase 7: Third Client — Enterprise Onboarding

## Profile
- **Tier:** ENTERPRISE
- **Plans:** 2+
- **Primary deliverable:** `run_multiplan_analysis()` — multi-plan aggregate RADV + peer benchmark
- **Rate:** $15K–$25K for 60-day engagement

## Capability Anchor
Multi-plan aggregate RADV + peer benchmark is a capability no spreadsheet can replicate.

## Key Issuance

When contract is signed and paid, provision the third client key:

```
# Example: Python
from starguard_core.db import get_db_adapter
from starguard_core.auth.tiers import Tier

adapter = get_db_adapter()
adapter.set(
    "enterprise-CLIENT3-<unique-id>",
    Tier.ENTERPRISE,
    email="client3@example.com",
    source="phase7_third_client",
    notes="Third Enterprise client, 2+ plans, 60-day engagement",
)
```

For Supabase: use migrate_to_supabase.py with a CSV containing the new key, or insert via Supabase dashboard.

## Timeline
- Day 1: Key issued
- Day 3: Plan data ingestion
- Day 7: run_multiplan_analysis() demo
- Day 14: peer_benchmark() + cohort comparison
- Day 30: Executive summary
- Day 60: Close-out, renewal discussion
