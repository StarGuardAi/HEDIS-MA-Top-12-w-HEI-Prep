# AuditShield-Live — Architecture

## Purpose

AuditShield-Live is an AI-powered Medicare Advantage RADV Audit Defense Platform. It provides integrated modules for provider scorecards, mock audits, financial impact analysis, RADV command center, chart selection AI, education automation, real-time validation, HCC reconciliation, compliance forecasting, regulatory intelligence, EMR rules, and executive dashboards. Phase 2 adds active suppression (audit-level), HITL Admin View, and hardening artifacts.

---

## Design Decisions

**starguard-core** — Shared library introduced to consolidate audit trail logic (AuditShield), HEDIS gap logic (Desktop/Mobile), and HCC suppression across all three apps. Single source of truth for `write_audit_trail`, `get_suppressed_hccs`, and gap CRUD reduces duplication and enables consistent behavior.

---

## Component Map (ASCII)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         AuditShield-Live (Shiny App)                         │
├─────────────────────────────────────────────────────────────────────────────┤
│  app.py (main)                                                               │
│    ├── app_complete.py (HuggingFace entry, uvicorn)                          │
│    ├── starguard_core.audit.trail ──► Google Sheets + Supabase               │
│    │   logic/ audit_trail.py deleted                                         │
│    │   └── .audit_suppressions.json (Phase 2)                                │
│    ├── audit_trail_ui.py                                                     │
│    ├── cloud_status_badge.py                                                 │
│    ├── suppression_banner.py (Phase 2)                                       │
│    ├── hitl_admin_view.py (Phase 2)                                          │
│    ├── meat_validator.py, radv_command_center.py                             │
│    ├── chart_selection_ai.py, education_automation.py                        │
│    ├── realtime_validation.py, hcc_reconciliation.py                         │
│    ├── compliance_forecasting.py, regulatory_intelligence.py                  │
│    ├── emr_rule_builder.py, dashboard_manager.py                             │
│    └── database.py, financial_calculator.py, mock_audit_simulator.py          │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Module Reference

| Module | Role |
|--------|------|
| `app.py` | Main Shiny UI + server |
| `app_complete.py` | HuggingFace entry, init check, uvicorn |
| `audit_trail.py` | RADV audit CRUD, Google Sheets, Supabase, Phase 2 suppression |
| `audit_trail_ui.py` | Audit Trail panel UI |
| `cloud_status_badge.py` | Cloud services badge (sidebar/strip) |
| `suppression_banner.py` | Phase 2 suppression status banner |
| `hitl_admin_view.py` | Phase 2 HITL Admin View (audit suppressions) |
| `meat_validator.py` | M.E.A.T. validation |
| `radv_command_center.py` | RADV command center |
| `chart_selection_ai.py` | Chart selection AI |
| `education_automation.py` | Education automation |
| `realtime_validation.py` | Real-time validation engine |
| `hcc_reconciliation.py` | HCC reconciliation |
| `compliance_forecasting.py` | Compliance forecasting |
| `regulatory_intelligence.py` | Regulatory intelligence |
| `emr_rule_builder.py` | EMR rule builder |
| `dashboard_manager.py` | Dashboard manager |
| `database.py` | SQLite/Supabase database |
| `financial_calculator.py` | Financial impact calculator |
| `mock_audit_simulator.py` | Mock audit simulator |

---

## Data Flow

```
User → Shiny UI → Server Handlers
         │
         ├──► starguard_core.audit.trail.write_audit_trail() → Google Sheets + Supabase
         ├──► starguard_core.audit.trail.fetch_recent_audits() → DataFrame
         ├──► starguard_core.audit.trail.get_suppressed_hccs() → .audit_suppressions.json
         ├──► add/remove_audit_suppression() → JSON CRUD
         └──► database, MEATValidator, etc. → SQLite / Supabase
```

---

## Supabase Schema

| Table | Purpose |
|------|---------|
| `audit_trail` | Parallel write from audit_trail.py; mirrors Google Sheets RADV audit records |

Primary persistence: Google Sheets. Supabase used for parallel write when `SUPABASE_URL` and `SUPABASE_ANON_KEY` are set.

---

## Deployment Topology

| Environment | Host | Port | Entry |
|-------------|------|------|-------|
| Local | localhost | 7860 | `python app_complete.py` |
| HuggingFace Spaces | rreichert/auditshield-live | 7860 | uvicorn via app_complete |
| Docker | python:3.11-slim | 7860 | `python app_complete.py` |

---

## Dependency Graph

```
app.py
  ├── shiny, pandas, plotly
  ├── audit_trail, audit_trail_ui, cloud_status_badge
  ├── suppression_banner, hitl_admin_view
  ├── meat_validator, radv_command_center, chart_selection_ai
  ├── education_automation, realtime_validation, hcc_reconciliation
  ├── compliance_forecasting, regulatory_intelligence, emr_rule_builder
  ├── dashboard_manager, database, financial_calculator, mock_audit_simulator
  └── gspread, supabase, google-auth, anthropic
```

---

## Configuration

| Variable | Purpose |
|----------|---------|
| `GSHEETS_CREDS_JSON` | Google Sheets credentials (HF Secret) |
| `AUDIT_SHEET` | Sheet name (default: AuditShield_RADV_Audit_Trail) |
| `SUPABASE_URL`, `SUPABASE_ANON_KEY` | Supabase parallel write |
| `AUDIT_SUPPRESSION_FILE` | Phase 2 suppression JSON path |
| `ANTHROPIC_API_KEY` | Claude API |
| `SQLITE_PATH` | SQLite path (default: /tmp/auditshield.db) |

---

## 4. starguard-core Import Chain

| starguard_core module | Replaces |
|----------------------|----------|
| `starguard_core.audit.trail` | `audit_trail.py` |

**Install:** `pip install starguard-core` (or `pip install -e path/to/starguard-core` for local dev)

**Usage:**
```python
from starguard_core.audit.trail import write_audit_trail, get_suppressed_hccs, fetch_recent_audits
```

---

## Supabase Schema

| Table | Purpose |
|-------|---------|
| `audit_trail` | Parallel write from starguard_core.audit.trail; mirrors Google Sheets RADV audit records |

Google Sheets is source of truth; Supabase receives fire-and-forget parallel writes when `SUPABASE_URL` and `SUPABASE_ANON_KEY` are set.

---

## Phase 2 Hardening Checklist

- [x] pyproject.toml (build, ruff, mypy, pytest)
- [x] Type hints (audit_trail, cloud_status_badge, suppression_banner, hitl_admin_view)
- [x] Unit tests (tests/test_auditshield.py) — 17 tests — 17 tests
- [x] CI workflow (.github/workflows/ci.yml) — strict mode
- [x] ARCHITECTURE.md
- [x] starguard-core import chain

---

## Phase 3 Complete

**starguard-core** — Shared library integrated. AuditShield consumes `starguard_core.audit.trail` for write_audit_trail, get_suppressed_hccs, fetch_recent_audits. `audit_trail.py` deleted.

---

## Rollback Procedure

**Revert → push → auto-redeploy.** No manual HuggingFace intervention needed in the normal case.

1. `git revert <commit>` (or `git revert HEAD` for last commit)
2. `git push origin main`
3. CI runs tests; deploy job syncs to HuggingFace Space
4. Space rebuilds from updated repo

If deploy fails, add `HF_TOKEN` secret (Settings → Secrets) with write access to the Space. One token covers all three repos.

---

## Rollback Procedure

If a bad deploy reaches production:

1. **Revert** the commit: `git revert HEAD --no-edit`
2. **Push** to main: `git push origin main`
3. **Auto-redeploy** — GitHub Actions deploy job runs on push; HuggingFace Space rebuilds from the reverted commit.

No manual HuggingFace intervention needed in the normal case. If the Space is connected via GitHub integration, the push alone triggers rebuild.

---

*Phase 3 Complete*

---

## Rollback Procedure

If a deploy introduces issues:

1. **Revert** the offending commit: `git revert <commit-hash>`
2. **Push** to main: `git push origin main`
3. **Auto-redeploy** — the deploy workflow runs on push; HuggingFace Space rebuilds from the reverted code.

No manual HuggingFace intervention needed in the normal case. If the Space is connected via GitHub integration, the push itself triggers rebuild.
