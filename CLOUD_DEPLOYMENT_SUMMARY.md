<!-- CLOUD_DEPLOYMENT_SUMMARY_START -->
---
## ☁️ Cloud Services & Deployment Architecture

> **Robert Reichert** · Healthcare AI Architect · 22+ Years Medicare Advantage Analytics  
> 📧 reichert.starguardai@gmail.com · [LinkedIn](https://tinyurl.com/24523hmy) · [GitHub](https://github.com/reichert-science-intelligence)

---

### 🚀 Live Deployments

| Application | Platform | URL | Status |
|---|---|---|---|
| **AuditShield-Live** | HuggingFace Spaces | [tinyurl.com/2vj79bem](https://tinyurl.com/2vj79bem) | ![Live](https://img.shields.io/badge/status-live-brightgreen) |
| **StarGuard Desktop** | HuggingFace Spaces | [rreichert-starguard-desktop.hf.space](https://rreichert-starguard-desktop.hf.space) | ![Live](https://img.shields.io/badge/status-live-brightgreen) |
| **StarGuard Mobile** | HuggingFace Spaces | [rreichert-starguardai.hf.space](https://rreichert-starguardai.hf.space) | ![Live](https://img.shields.io/badge/status-live-brightgreen) |

---

### 🧩 Cloud Module Architecture
```
reichert-science-intelligence/
│
├── cloud_status_badge.py          # Shared — all 3 apps
│   ├── cloud_status_badge()       # Pulsing live-service sidebar badge
│   └── provenance_footer()        # Sticky Anthropic + HuggingFace footer
│
├── AuditShield-Live/
│   ├── audit_trail.py             # RADV Google Sheets persistence
│   │   ├── AuditTrailDB           # Connection manager
│   │   ├── push_audit_record()    # Append audit session to cloud
│   │   ├── fetch_recent_audits()  # Pull latest N records
│   │   └── update_audit_status()  # OPEN → REVIEWED → CLOSED
│   └── audit_trail_ui.py          # Push form, live table, status updater
│
├── StarGuard-Desktop/
├── StarGuard-Mobile/
│   ├── hedis_gap_trail.py         # HEDIS Google Sheets persistence
│   │   ├── HedisGapDB             # Connection manager
│   │   ├── push_hedis_gap()       # Append care gap to cloud
│   │   ├── fetch_hedis_gaps()     # Pull with status/measure filters
│   │   ├── fetch_gap_summary()    # KPI aggregates
│   │   └── close_hedis_gap()      # Mark gap CLOSED by ID
│   ├── hedis_gap_ui.py            # KPI row, push form, filter table
│   ├── star_rating_cache.py       # Star Forecast Google Sheets cache
│   │   ├── StarRatingCacheDB      # Connection manager
│   │   ├── cache_forecast()       # Write forecast run to cloud
│   │   ├── fetch_latest_forecast()# Most recent FRESH forecast
│   │   ├── fetch_forecast_history()# Trend data (N runs)
│   │   └── fetch_cache_summary()  # KPI aggregates
│   └── star_rating_cache_ui.py    # Hero card, KPI row, history table
```

---

### ☁️ Google Cloud Platform Setup

#### Required APIs (GCP Console)
- ✅ Google Sheets API
- ✅ Google Drive API

#### Service Account
1. Create a service account in GCP Console
2. Download the JSON key
3. Add as HuggingFace Space Secret: `GSHEETS_CREDS_JSON`

#### Google Sheets — 3 Dedicated Workbooks

| Sheet Name | App | Secret Key | Purpose |
|---|---|---|---|
| `AuditShield_RADV_Audit_Trail` | AuditShield-Live | `AUDIT_SHEET_ID` | RADV audit session log |
| `StarGuard_HEDIS_Gap_Tracker` | StarGuard D+M | `HEDIS_SHEET_ID` | Live HEDIS care gap panel |
| `StarGuard_Star_Rating_Cache` | StarGuard D+M | `STAR_CACHE_SHEET_ID` | Forecast run cache |

> Share each sheet with your service account `client_email` as **Editor**.

---

### 🔐 HuggingFace Space Secrets

Set these in **Settings → Secrets** for each Space:

#### AuditShield-Live Space
| Secret | Value |
|---|---|
| `GSHEETS_CREDS_JSON` | Full service account JSON contents |
| `AUDIT_SHEET_ID` | `AuditShield_RADV_Audit_Trail` |

#### StarGuard Desktop Space
| Secret | Value |
|---|---|
| `GSHEETS_CREDS_JSON` | Full service account JSON contents |
| `HEDIS_SHEET_ID` | `StarGuard_HEDIS_Gap_Tracker` |
| `STAR_CACHE_SHEET_ID` | `StarGuard_Star_Rating_Cache` |

#### StarGuard Mobile Space
| Secret | Value |
|---|---|
| `GSHEETS_CREDS_JSON` | Full service account JSON contents |
| `HEDIS_SHEET_ID` | `StarGuard_HEDIS_Gap_Tracker` |
| `STAR_CACHE_SHEET_ID` | `StarGuard_Star_Rating_Cache` |

> The same `GSHEETS_CREDS_JSON` key is shared across all 3 Spaces.  
> Desktop and Mobile StarGuard share the same Google Sheets — gaps closed on Desktop disappear on Mobile on next refresh.

---

### 📦 Python Dependencies
```text
# requirements.txt — all three apps
shiny>=0.10.0
gspread>=6.0.0
google-auth>=2.28.0
pandas>=2.0.0
anthropic>=0.25.0
```

---

### 🏗️ Local Development
```bash
# Clone repo
git clone https://github.com/reichert-science-intelligence/your-repo-name
cd your-repo-name

# Install dependencies
pip install -r requirements.txt

# Add local credentials (never commit this file)
cp /path/to/your/service_account.json ./service_account.json

# Run app
shiny run app.py --reload
```

> If `GSHEETS_CREDS_JSON` is not set and `service_account.json` is absent,  
> cloud tabs show **"⚠ Disconnected"** — the app still starts normally.

---

### 🎯 Recruiter Signals Built Into Every App

| UI Element | Location | What It Proves |
|---|---|---|
| Pulsing green dots | Sidebar top | Live production deployment, not a mockup |
| "Last sync" timestamp | Badge footer | Real-time cloud architecture thinking |
| "FRESH / STALE" banner | Forecast tab | Data freshness lifecycle management |
| Timestamped audit log | Audit Trail tab | RADV compliance workflow experience |
| KPI cards with live counts | HEDIS / Star tabs | Medicare Advantage domain expertise |
| Provenance footer | Every page | Anthropic API + HuggingFace credibility |
| LinkedIn / GitHub links | Footer | One-click to full professional profile |

---

### 📊 Platform Capabilities Summary

#### AuditShield-Live
- Agentic RAG pipeline for HEDIS audit intelligence
- M.E.A.T. validation engine for HCC documentation
- RADV Audit Trail with Google Sheets cloud persistence
- Mobile-first React UI on HuggingFace Spaces

#### StarGuard Desktop + Mobile
- HEDIS Gap Refresh with live Google Sheets backend
- Star Rating Forecast Cache with FRESH/STALE lifecycle
- HCC Risk Stratification and CAHPS analytics
- Shared cloud data layer — Desktop and Mobile in sync
- Powered by Anthropic Claude API for AI-generated narratives

---

*Last updated: March 2026 · Robert Reichert · [tinyurl.com/bdevpdz5](https://tinyurl.com/bdevpdz5)*

<!-- CLOUD_DEPLOYMENT_SUMMARY_END -->
