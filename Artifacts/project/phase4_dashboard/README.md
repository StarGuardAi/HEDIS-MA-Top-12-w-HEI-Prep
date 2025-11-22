# Phase 4 Dashboard - HEDIS Portfolio Optimizer

Interactive Streamlit dashboard for visualizing Phase 3 ROI analysis data from the HEDIS Portfolio Optimizer.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- PostgreSQL database with Phase 3 data loaded
- Required packages (see requirements.txt)

### Installation

1. Install dependencies:
```bash
pip install streamlit pandas plotly psycopg2-binary sqlalchemy
```

2. Set environment variables (optional, uses defaults if not set):
```bash
export DB_HOST=localhost
export DB_PORT=5432
export DB_NAME=hedis_portfolio
export DB_USER=hedis_api
export DB_PASSWORD=hedis_password
```

3. Run the dashboard:
```bash
cd Artifacts/project/phase4_dashboard
streamlit run app.py
```

The dashboard will open in your default web browser at `http://localhost:8501`

## 📊 Dashboard Features

### Home Page
- Portfolio overview KPIs
- Total investment, closures, ROI ratio, net benefit
- Quick insights and navigation

### Page 1: ROI by Measure
- Bar chart comparing ROI across all 12 HEDIS measures
- Measure-level metrics and insights
- Export to CSV functionality

### Page 2: Cost per Closure by Activity
- Scatter plot (cost vs success rate)
- Bubble size indicates usage frequency
- Activity-level cost-effectiveness analysis

### Page 3: Monthly Intervention Trend
- Multi-line trend charts
- Intervention volume over time
- Success rate tracking

### Page 4: Budget Variance by Measure
- Waterfall variance charts
- Budget vs actual spending
- Over/under budget indicators

### Page 5: Cost Tier Comparison
- Grouped bar charts
- Low/Medium/High touch comparison
- Strategic recommendations

## 📁 Project Structure

```
phase4_dashboard/
├── app.py                 # Main Streamlit application
├── pages/                 # Multi-page app pages
│   ├── 1_roi_by_measure.py
│   ├── 2_cost_per_closure.py
│   ├── 3_monthly_trend.py
│   ├── 4_budget_variance.py
│   └── 5_cost_tier_comparison.py
├── utils/                 # Utility modules
│   ├── database.py       # Database connection utilities
│   ├── queries.py        # Phase 3 SQL queries
│   ├── charts.py         # Chart generation functions
│   └── __init__.py
└── README.md
```

## 🎨 Features

- **Professional Medical Theme**: Custom styling with healthcare color scheme
- **Interactive Charts**: Plotly visualizations with hover tooltips
- **Export Functionality**: Download data as CSV from any page
- **Database Integration**: Live data from Phase 3 PostgreSQL database
- **Responsive Design**: Works on desktop and tablet devices
- **Multi-page Navigation**: Easy navigation via sidebar menu

## 🔧 Configuration

Database connection settings can be configured via environment variables:

- `DB_HOST`: PostgreSQL host (default: localhost)
- `DB_PORT`: PostgreSQL port (default: 5432)
- `DB_NAME`: Database name (default: hedis_portfolio)
- `DB_USER`: Database user (default: hedis_api)
- `DB_PASSWORD`: Database password (default: hedis_password)

## 📊 Data Requirements

The dashboard requires Phase 3 data loaded in the `hedis_portfolio` database:

- `member_interventions` table
- `hedis_measures` table
- `intervention_activities` table
- `budget_allocations` table
- `actual_spending` table

Data period: Q4 2024 (October 1 - December 31, 2024)

## 🐛 Troubleshooting

### Database Connection Failed
- Check PostgreSQL service is running
- Verify database credentials
- Ensure Phase 3 data is loaded

### No Data Found
- Verify Phase 3 data is in the database
- Check date range filters
- Ensure tables contain data for Q4 2024

### Import Errors
- Install all required packages: `pip install -r requirements.txt`
- Check Python version (3.8+ required)

## 📝 Notes

- All queries use Phase 3 demo queries from `phase3_demo_queries.sql`
- Date filters default to Q4 2024 but can be adjusted
- Charts are interactive with Plotly tooltips
- Data can be exported to CSV from any page

## 👤 Author

**Robert Reichert**
- Email: reichert.starguardai@gmail.com
- Portfolio: HEDIS Portfolio Optimizer - Phase 4 Dashboard

## 📄 License

Part of the HEDIS Portfolio Optimizer project.

---

**Phase 4 Dashboard** | Built with Streamlit, Plotly, and PostgreSQL

