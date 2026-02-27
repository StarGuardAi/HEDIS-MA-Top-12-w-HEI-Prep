# Demo Launch Guide

Curated for recruiters, influencers, and hiring managers who want to experience the HEDIS Star Rating Portfolio Optimizer demo in under five minutes. For a share-ready overview, see the new **[Influencer & Talent Partner Kit](./influencer_portal.md)**.

---

## 1. Fastest Path – Streamlit Cloud

1. Visit the hosted demo: **https://hedis-ma-top-12-w-hei-prep.streamlit.app/**
2. Walk through the sidebar tour:
   - `Executive Summary` → macro story & value
   - `Gap Prioritization` → member-level intelligence
   - `Star Rating Simulator` → “what if” levers recruiters love
3. Shareable highlights:
   - Screenshot the KPI panel for LinkedIn or outreach emails.
   - Use the “Copy Link” button in Streamlit to send tailored scenarios.

> **Tip:** Mention that the demo uses synthetic data while mirroring CMS Stars logic—perfect for interview storytelling.

---

## 2. Local Demo (Optional)

```bash
git clone https://github.com/bobareichert/HEDIS-MA-Top-12-w-HEI-Prep.git
cd HEDIS-MA-Top-12-w-HEI-Prep/project

# 1. Create & activate virtual environment (choose your tool)
python -m venv .venv
.venv\Scripts\activate      # Windows
source .venv/bin/activate   # macOS / Linux

# 2. Install dependencies (demo configuration)
pip install -r requirements.txt

# 3. Launch the Streamlit app with demo data
streamlit run streamlit_app.py
```

What to expect locally:
- Synthetic datasets under `data/processed/`
- Pre-baked model artifacts under `models/`
- Demo-friendly defaults (no credentials, no PHI)

---

## 3. Conversation Starters

| Audience | Hook | Suggested Talking Point |
|----------|------|-------------------------|
| Influencer / Thought Leader | “This demo condenses 12 HEDIS measures into a single Stars narrative.” | Offer a short screen recording or invite them to explore the simulator with their own assumptions. |
| Recruiter / Talent Partner | “Interactive ROI model shows the business story behind the models.” | Send the live link plus one KPI screenshot. Follow up with 2-3 bullet insights tailored to their client. |
| Hiring Manager | “I pair predictive insights with BI storytelling.” | Walk them through the Star Rating simulator, then reference the accompanying executive memo. |

---

## 4. Showcase Assets (Ready to Share)

- `project/reports/EXECUTIVE_PRESENTATION.md` – slide-ready story
- `project/reports/FINANCIAL_SUMMARY_QUICK_REF.md` – one-page ROI
- `project/reports/TIER_1_COMPLETE_FINAL.md` – narrative proof of delivery
- `project/docs/API_USAGE_GUIDE.md` – for technically inclined reviewers

Bundle the above into an email or LinkedIn message to demonstrate the full BI + DS value stack.

---

## 5. Optional Extras

- **Landing Page:** Use Netlify/Vercel to host a teaser page that links to the Streamlit demo and key PDFs (see `README.md` → Quick Demo Access).
- **Video Walkthrough:** Record a 90-second Loom walking through the simulator; embed the link in outreach notes.
- **Tailored Scenarios:** Duplicate the repo, tweak the synthetic inputs, and export custom CSVs for plan-size-specific storytelling.

---

### Reminder
This repository is intentionally demo-first. It showcases healthcare Stars expertise, predictive modeling, and BI storytelling without exposing protected health information or requiring production infrastructure.

