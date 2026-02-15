# Intervention Portfolio Optimizer — Implementation Notes

## Two UIs in This Repo

This repo has **two** dashboard applications with different page structures:

| App | Framework | Location | Page discovery |
|-----|------------|----------|-----------------|
| **Phase 4 Dashboard** | **Streamlit** | `Artifacts/project/phase4_dashboard/` | **Auto-discovered**: files in `pages/` (e.g. `12_🎯_Intervention_Portfolio_Optimizer.py`) appear in the sidebar automatically. |
| **StarGuard Shiny** | **Shiny for Python** | `starguard-shiny/` | **Manual**: all navigation is defined in `app.py` via `ui.navset_hidden()` and `ui.nav_panel()`. No auto-discovery. |

---

## Dual-App Architecture (Why Two Apps)

| Aspect | Streamlit (Prototyping) | Shiny (Production) |
|--------|-------------------------|---------------------|
| **Purpose** | Rapid prototyping, exploratory analytics | Client-facing demo, production-ready |
| **Audience** | Internal testing, quick iterations | Recruiters, clients, April 2026 launch |
| **Speed** | Fast iteration | More structured |
| **Features** | Basic analytics | Advanced (self-correction, validation, compound engineering) |
| **Error handling** | Basic | Production-grade |
| **UI polish** | Functional | Professional |
| **Demo use** | Personal/testing | **Show recruiters and clients** |

**Recommendation:** Use Streamlit for quick experiments; use the Shiny app for demos and client presentations.

---

## Verification

**Streamlit**
```bash
cd Artifacts/project/phase4_dashboard
streamlit run app.py
```
- **Expected:** Sidebar shows **Intervention Portfolio Optimizer** (page 12). Budget input and three strategy expanders work.

**Shiny**
```bash
cd starguard-shiny
shiny run app.py
```
- **Expected:** Sidebar → **Portfolio Optimizer** (or under Financial Analysis). Budget input ($25K–$1M) works; three strategy tabs populate; **Financial Impact by Intervention** table shows default interventions.

---

## Streamlit (Phase 4 Dashboard)

### Behavior
- **Pages** live in `phase4_dashboard/pages/` with numeric prefixes (e.g. `11_💰_ROI_Calculator.py`, `12_🎯_Intervention_Portfolio_Optimizer.py`).
- Streamlit discovers them by filename; no need to register in `app.py`.
- **Do not delete** `pages/12_🎯_Intervention_Portfolio_Optimizer.py` — it is the correct way to add the feature in the Streamlit app.

### Files
- **Logic:** `Artifacts/project/phase4_dashboard/utils/intervention_analysis.py`
- **UI:** `Artifacts/project/phase4_dashboard/pages/12_🎯_Intervention_Portfolio_Optimizer.py`

### Run
```bash
cd Artifacts/project/phase4_dashboard
streamlit run app.py
```
Then open **Intervention Portfolio Optimizer** in the sidebar.

---

## Shiny (StarGuard Shiny)

### Behavior
- **Single entry point:** `starguard-shiny/app.py`.
- Every page is a `ui.nav_panel("id", content())` inside `ui.navset_hidden()`.
- To add a page, you must add a nav_panel and any server outputs it needs.

### Files
- **Logic:** `starguard-shiny/utils/intervention_analysis.py` (copy of the same module so Shiny runs standalone).
- **UI + server:** Implemented inside `starguard-shiny/app.py` (optimizer content function + server renderers).

### Run
```bash
cd starguard-shiny
shiny run app.py
```
Navigate via sidebar to **Portfolio Optimizer** (or **Intervention Portfolio Optimizer**).

---

## Shared Backend API

Both UIs use the same interface from `utils/intervention_analysis.py`:

| Function | Purpose |
|----------|---------|
| `calculate_intervention_roi(intervention_type, target_measure, expected_gap_closure, intervention_cost, member_count, ...)` | ROI for one intervention: cost per closure, financial impact, star bonus, confidence. |
| `get_default_interventions()` | List of 8 example interventions (BCS, CDC, CBP, COL, etc.) with cost and gap closure %. |
| `optimize_intervention_portfolio(budget, available_interventions=None, constraints=None)` | Returns three strategies: `approach_1_max_star`, `approach_2_max_roi`, `approach_3_balanced`, each with `selected_interventions`, `total_cost`, `total_financial_impact`, `total_star_rating_bonus`, `net_benefit`. |

---

## Demo Talking Points

- **Portfolio optimization:** “Not just what gaps exist, but how to allocate our intervention budget.”
- **Three strategies:** (1) Max Star Rating, (2) Max Financial Return, (3) Balanced (quick wins + strategic).
- **Per-intervention:** Cost per closure, expected rate improvement, financial impact, ROI ratio, confidence scores.
- **Trust:** “Validated against 20+ historical interventions.”

---

## Validation / Option C (Streamlit only)

- **Validation badges** and “Why Trust This?” live in `phase4_dashboard/utils/validation_badges.py` and are used on Cost Per Closure, Compliance, Historical Tracking, AI Executive Insights, and the Intervention Portfolio Optimizer page.
- The Shiny app can add similar messaging in its optimizer panel if desired.

---

## Summary

| Question | Streamlit (phase4_dashboard) | Shiny (starguard-shiny) |
|----------|------------------------------|--------------------------|
| Where is the Optimizer? | `pages/12_🎯_Intervention_Portfolio_Optimizer.py` (auto in sidebar) | Implemented in `app.py` as a nav_panel; must be added manually. |
| Delete the Streamlit page? | **No** — it is the correct implementation for Streamlit. | N/A |
| Add to Shiny? | N/A | Yes — add nav_panel + server logic in `app.py`; use `utils/intervention_analysis.py` in `starguard-shiny/utils/`. |
