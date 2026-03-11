# Phase 8 Spec — Cursor-Ready

## Objectives (Execute in Order)

### Objective 1: Rate Limiting (Engineering)
- **Scope:** `auth/usage.py` — `check_rate_limit()`, `RateLimitResult`. Non-blocking. Enterprise always `allowed=True`, `remaining=None`.
- **Tests:** Five tests. Integration into `validate_api_key(api_key, feature=...)`.

### Objective 2: Webhook (Engineering)
- **Scope:** `_fire_webhook()` in `capture.py`. urllib.request only, no new deps. Fires on trial provision when `WEBHOOK_URL` set.
- **Tests:** Four tests, including mock for urlopen.
- **Docs:** Make.com scenario wiring step-by-step.

### Objective 3: v1.3.0 (Release)
- **Scope:** Build + publish. multiplan/ promoted to stable in changelog.
- **Expected test count:** 159.

### Objective 4: Fourth Client (Business)
- **Scope:** HEDIS + Stars Pro engagement. Single contract MA plan, 3.5 stars targeting 4.0 QBP threshold.
- **Rate:** $8K–$12K. Entry: LinkedIn Post 4 ("50:1 ROI") conversion asset.

### Objective 5: Self-Serve Trial (Engineering)
- **Scope:** HTML form on landing page → `/request-trial` endpoint in AuditShield → `capture_lead(auto_provision_trial=True)` → webhook fires → trial key emailed.
- **Full funnel** closes without manual intervention. No new starguard-core code — uses Phase 7–8.

---

## Phase 9 Seed (Staged)
Stripe integration — self-serve paid upgrade from trial key. Revenue loop without manual contract execution.
