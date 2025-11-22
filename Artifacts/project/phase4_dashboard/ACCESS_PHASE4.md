# Phase 4 Dashboard - Access Instructions

## 🚨 Important: You're Currently Viewing a Different App

The page you're seeing ("Executive Summary") is from the **portfolio/marketing Streamlit app** located at:
- `Artifacts/project/streamlit_app.py`

The **Phase 4 ROI Dashboard** is a **separate application** located at:
- `Artifacts/project/phase4_dashboard/app.py`

## 🚀 How to Access Phase 4 Dashboard

### Option 1: Using the Batch Script
```bash
cd Artifacts\project\phase4_dashboard
start_phase4.bat
```

This will start the Phase 4 dashboard on **port 8502**.

### Option 2: Using Streamlit Command
```bash
cd Artifacts\project\phase4_dashboard
streamlit run app.py --server.port 8502
```

### Option 3: Using Python Module
```bash
cd Artifacts\project\phase4_dashboard
python -m streamlit run app.py --server.port 8502
```

## 🌐 Dashboard URLs

Once running, access the Phase 4 dashboard at:

- **Phase 4 Dashboard (ROI Analytics)**: http://localhost:8502
- **Portfolio App (Executive Summary)**: http://localhost:8501

## 📊 Phase 4 Dashboard Features

The Phase 4 dashboard includes:

1. **Home Page** - Portfolio overview with KPI cards
2. **ROI by Measure** - Bar chart comparing ROI across all 12 HEDIS measures
3. **Cost per Closure** - Scatter plot of activity effectiveness
4. **Monthly Trend** - Line charts showing trends over time
5. **Budget Variance** - Waterfall charts for budget analysis
6. **Cost Tier Comparison** - Grouped bars for Low/Medium/High touch

All pages connect to your Phase 3 PostgreSQL database (`hedis_portfolio`) and display live ROI analysis data.

## 🔧 Troubleshooting

### If you see the Executive Summary page:
- You're accessing the wrong app
- Use port 8502 for Phase 4 dashboard
- Or stop the existing Streamlit app first

### If Phase 4 dashboard doesn't load:
- Make sure you're in the `phase4_dashboard` directory
- Check that all packages are installed: `pip install -r requirements.txt`
- Verify database connection: `python -c "from utils.database import test_connection; print('PASSED' if test_connection() else 'FAILED')"`

## 📁 File Locations

- **Portfolio App**: `Artifacts/project/streamlit_app.py` (port 8501)
- **Phase 4 Dashboard**: `Artifacts/project/phase4_dashboard/app.py` (port 8502)

---

**Quick Start**: Run `start_phase4.bat` from the `phase4_dashboard` directory, then visit http://localhost:8502

