# Phase 4 Dashboard - Quick Start Guide

## 🚀 Run the Dashboard

### Option 1: Using the Batch Script (Windows)
```bash
cd Artifacts\project\phase4_dashboard
run_dashboard.bat
```

### Option 2: Using Streamlit Command
```bash
cd Artifacts/project/phase4_dashboard
streamlit run app.py
```

### Option 3: Using Python
```bash
cd Artifacts/project/phase4_dashboard
python -m streamlit run app.py
```

## 📊 Dashboard Access

Once running, the dashboard will be available at:
- **Local URL**: http://localhost:8501
- The browser will open automatically

## 🔧 Prerequisites Check

Before running, ensure:

1. ✅ **Python 3.8+** installed
2. ✅ **Packages installed**: `pip install streamlit pandas plotly psycopg2-binary sqlalchemy`
3. ✅ **PostgreSQL running** with `hedis_portfolio` database
4. ✅ **Phase 3 data loaded** in the database

## 🧪 Test Connection

Test database connection:
```bash
cd Artifacts/project/phase4_dashboard
python -c "from utils.database import test_connection; print('PASSED' if test_connection() else 'FAILED')"
```

## 📖 Navigation

- **Home Page**: Portfolio overview with KPI cards
- **ROI by Measure**: Bar chart comparing ROI across measures
- **Cost per Closure**: Scatter plot of activity effectiveness
- **Monthly Trend**: Line charts showing trends over time
- **Budget Variance**: Waterfall charts for budget analysis
- **Cost Tier Comparison**: Grouped bars for Low/Medium/High touch

## 🎯 Features

- ✅ Interactive Plotly charts
- ✅ Export to CSV from any page
- ✅ Professional medical theme
- ✅ Real-time data from Phase 3 database
- ✅ Date range filtering
- ✅ KPI summary cards

## ⚠️ Troubleshooting

### Connection Failed
- Check PostgreSQL is running
- Verify database credentials in environment variables
- Ensure Phase 3 data is loaded

### No Data Found
- Check date range filters match Phase 3 data period (Q4 2024)
- Verify tables exist in `hedis_portfolio` database

### Import Errors
- Run: `pip install -r requirements.txt`
- Check Python version: `python --version`

---

**Ready to go!** 🎉

