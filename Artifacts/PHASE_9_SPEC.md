# Phase 9 Spec — Cursor-Ready

## Objectives (Execute in Order)

### Objective 1: Usage Analytics Dashboard (Infrastructure)
- **Scope:** Supabase PostgreSQL connector to Looker Studio. Four dashboard pages: API usage, key-level detail, lead funnel, rate limit health.
- **usage_log indexes** — Critical for Looker Studio queries at scale. Migration/schema defines table + indexes.
- **Pure wiring** — No new application code. Schema + Looker connector only.

### Objective 2: Stripe Integration (Engineering)
- **Scope:** `starguard_core/billing/` — `webhook_handler.py`, verified Stripe event → `upgrade_to_paid()` → paid key provisioned automatically.
- **checkout.session.completed** — Handles trial-to-paid (revokes trial key) and direct purchase (provisions fresh paid key).
- **No manual intervention** — End-to-end self-serve.
- **Tests:** Six tests including full trial revoke path.

### Objective 3: v1.4.0 (Release)
- **Scope:** Build + publish. `billing/` added. `multiplan/` stable.
- **Expected test count:** 165.

### Objective 4: Fifth Client (Business)
- **Scope:** First client via self-serve funnel end-to-end. Trial form → trial key → Stripe checkout → paid key automatic.
- **No manual contract** if funnel works.

### Objective 5: SOC 2 Readiness (Compliance)
- **Scope:** `starguard_core/audit/` — `log_event()`, `CONTROL_REGISTRY`. Six SOC 2 criteria mapped to implementation.
- **get_controls_summary()** — Generates living document.
- **Phase 10** closes certification loop.
