---
title: SovereignShield Mobile
emoji: 📱
colorFrom: indigo
colorTo: purple
sdk: docker
app_port: 7860
app_file: app.py
pinned: false
---

# SovereignShield Mobile — Compliance Remediation

Evaluate / Policy / History tabs. Real OPA subprocess eval, batch remediation plan, Supabase logging.

## Secrets (Space Settings)

| Secret | Description |
|--------|-------------|
| `SUPABASE_ANON_KEY` | Supabase anon key for audit_runs/audit_results |

History tab degrades silently without it.

## Run locally

```bash
pip install -r requirements.txt
shiny run app.py --port 7860
```
