# Phase 7 Spec — Cursor-Ready

## Objectives (Execute in Order)

### Objective 1: Supabase (Operational)
- **Scope:** Three env var swaps + data migration script. No new Python modules.
- **Env vars:** `DB_ADAPTER=supabase`, `SUPABASE_URL`, `SUPABASE_SERVICE_KEY`
- **Migration:** Script to migrate api_keys from local/sheets → Supabase `api_keys` table.
- **verify_phase7_close.py:** Gracefully falls back to local if Supabase not configured. CI never breaks.

### Objective 2: Multi-plan (Engineering)
- **Scope:** `starguard_core/multiplan/` with `run_multiplan_analysis()` and `peer_benchmark()`.
- **Tests:** Five tests. Gated strictly to ENTERPRISE tier — Pro cannot access.

### Objective 3: v1.2.0 (Release)
- **Scope:** Build + publish. Same pattern as v1.1.0.
- **Expected test count:** 149.

### Objective 4: LinkedIn Campaign
- **Scope:** Four posts for Buffer. Tuesday/Thursday cadence.
- **Post 3:** References PyPI package — technical credibility anchor for CTOs/CIOs.

### Objective 5: Third Client
- **Scope:** Enterprise tier, 2+ plans, `run_multiplan_analysis()` as primary deliverable.
- **Rate guidance:** $15K–$25K for 60-day engagement.
- **Anchor:** Multi-plan aggregate RADV + peer benchmark — no spreadsheet can replicate.

---

## Phase 8 Seed (Staged)
Rate limiting, webhook direct-fire, v1.3.0, fourth client, self-serve trial form.
