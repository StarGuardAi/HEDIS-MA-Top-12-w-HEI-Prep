---
title: Platform Hub
emoji: 🔗
colorFrom: blue
colorTo: indigo
sdk: docker
app_port: 7860
pinned: false
---

# Platform Hub — MA Compliance Intelligence

Cross-app KPI dashboard for AuditShield, StarGuard, and SovereignShield.

## Features

- **Platform KPIs**: open findings by source app, critical open, remediated total
- **Recent Findings**: cross_app_findings from Supabase
- **Supabase Integration**: uses shared ledger from platform_hub_schema.sql

## Secrets (Space Settings)

Add in **Settings → Repository secrets**:

| Secret | Description |
|--------|-------------|
| `SUPABASE_URL` | Supabase project URL |
| `SUPABASE_ANON_KEY` | Supabase anon or service role key |
| `SOVEREIGNSHIELD_URL` | Optional; defaults to `https://huggingface.co/spaces/rreichert/sovereignshield` (desktop Space slug is **sovereignshield**, not sovereignshield-desktop). |

Without secrets, the app shows demo placeholder data.

## Run locally

```bash
pip install -r requirements.txt
shiny run app.py --port 7860
```

## Schema

Requires `platform_hub_schema.sql` run in Supabase:
- `platform_hub_kpis` view
- `cross_app_findings` table
- `platform_sessions`, `platform_alerts`
