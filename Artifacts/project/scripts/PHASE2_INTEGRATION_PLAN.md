# Phase 2 Integration Plan - Database to Streamlit

## 🎯 Goal

Integrate the Phase 1 PostgreSQL database with your existing Streamlit application to create data-driven dashboards using real 10K member data.

---

## 📊 Current Streamlit App Structure

Your app already has:
- ✅ Financial Overview page
- ✅ Operations Command Center
- ✅ Predictive Priority dashboard
- ✅ Individual measure pages (GSD, KED, EED, BPD, CBP, COL, BCS, PDC-DR, PDC-RASA, PDC-STA, SUPD)
- ✅ HEI Dashboard

**Next:** Connect these to the PostgreSQL database for real-time data.

---

## 🔌 Integration Strategy

### Step 1: Create Database Connection Module

**File:** `src/data/database.py`

```python
"""
Database connection utilities for HEDIS Portfolio Optimizer
"""
import psycopg2
from psycopg2.extras import RealDictCursor
import streamlit as st
import pandas as pd
from typing import List, Dict, Optional

@st.cache_resource
def get_db_connection():
    """Get cached database connection."""
    try:
        return psycopg2.connect(
            host=st.secrets.get("DB_HOST", "localhost"),
            database=st.secrets.get("DB_NAME", "hedis_portfolio"),
            user=st.secrets.get("DB_USER", "hedis_api"),
            password=st.secrets.get("DB_PASSWORD", "hedis_password"),
            port=st.secrets.get("DB_PORT", 5432)
        )
    except Exception as e:
        st.error(f"Database connection failed: {e}")
        return None

@st.cache_data(ttl=300)  # Cache for 5 minutes
def query_to_dataframe(query: str, params: Optional[Dict] = None) -> pd.DataFrame:
    """Execute query and return as DataFrame."""
    conn = get_db_connection()
    if conn is None:
        return pd.DataFrame()
    
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, params or {})
            rows = cur.fetchall()
            return pd.DataFrame(rows)
    except Exception as e:
        st.error(f"Query failed: {e}")
        return pd.DataFrame()
    finally:
        conn.close()

# Convenience functions for common views
def get_revenue_at_risk(plan_id: Optional[str] = None) -> pd.DataFrame:
    """Get revenue at risk data."""
    query = "SELECT * FROM vw_revenue_at_risk WHERE measurement_year = 2024"
    if plan_id:
        query += f" AND plan_id = %(plan_id)s"
    return query_to_dataframe(query, {"plan_id": plan_id} if plan_id else None)

def get_velocity_dashboard() -> pd.DataFrame:
    """Get current velocity dashboard data."""
    return query_to_dataframe("SELECT * FROM vw_current_velocity")

def get_portfolio_roi() -> pd.DataFrame:
    """Get portfolio ROI data."""
    return query_to_dataframe("SELECT * FROM vw_portfolio_roi")

def get_member_segmentation(filters: Optional[Dict] = None) -> pd.DataFrame:
    """Get member segmentation data."""
    query = "SELECT * FROM vw_member_segmentation WHERE 1=1"
    params = {}
    
    if filters:
        if filters.get("plan_id"):
            query += " AND plan_id = %(plan_id)s"
            params["plan_id"] = filters["plan_id"]
        if filters.get("risk_category"):
            query += " AND risk_category = %(risk_category)s"
            params["risk_category"] = filters["risk_category"]
    
    return query_to_dataframe(query, params if params else None)

def get_geographic_performance() -> pd.DataFrame:
    """Get geographic performance data."""
    return query_to_dataframe("SELECT * FROM vw_geographic_performance WHERE member_count > 0")

def get_executive_summary(plan_id: str) -> Dict:
    """Get executive financial summary."""
    conn = get_db_connection()
    if conn is None:
        return {}
    
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                "SELECT * FROM get_executive_financial_summary(%(plan_id)s, 2024)",
                {"plan_id": plan_id}
            )
            rows = cur.fetchall()
            return {row["summary_metric"]: row["metric_value"] for row in rows}
    except Exception as e:
        st.error(f"Failed to get executive summary: {e}")
        return {}
    finally:
        conn.close()
```

---

### Step 2: Update Streamlit Configuration

**File:** `.streamlit/secrets.toml` (create if doesn't exist)

```toml
[db]
host = "localhost"
database = "hedis_portfolio"
user = "hedis_api"
password = "hedis_password"
port = 5432
```

**For Docker:**
```toml
[db]
host = "localhost"  # Docker exposes on localhost
database = "hedis_portfolio"
user = "hedis_api"
password = "hedis_password"
port = 5432
```

---

### Step 3: Enhance Existing Pages

#### A. Financial Overview Page

**File:** `streamlit_pages/financial_overview.py`

Add database integration:

```python
from src.data.database import get_revenue_at_risk, get_portfolio_roi, get_executive_summary

# Replace mock data with real data
revenue_data = get_revenue_at_risk()
roi_data = get_portfolio_roi()

# Add plan selector
plan_id = st.selectbox("Select Plan", ["All"] + revenue_data["plan_id"].unique().tolist())

if plan_id != "All":
    revenue_data = revenue_data[revenue_data["plan_id"] == plan_id]
    summary = get_executive_summary(plan_id)
    
    # Display executive summary
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Revenue at Risk", f"${summary.get('Total Revenue at Risk', 0):,.0f}")
    with col2:
        st.metric("Gaps to Close", f"{summary.get('Total Member Gaps to Close', 0):,.0f}")
    with col3:
        st.metric("Avg Cost/Closure", f"${summary.get('Average Cost per Gap Closed', 0):,.2f}")
```

#### B. Operations Command Center

**File:** `streamlit_pages/operations_command.py`

Add velocity tracking:

```python
from src.data.database import get_velocity_dashboard, get_member_segmentation

velocity_data = get_velocity_dashboard()

# Velocity metrics by plan
st.subheader("Gap Closure Velocity")
velocity_summary = velocity_data.groupby("plan_id").agg({
    "gaps_per_week": "mean",
    "closure_rate_pct": "mean",
    "gaps_open_end": "sum"
}).reset_index()

st.dataframe(velocity_summary, use_container_width=True)
```

---

### Step 4: Create New Database-Driven Pages

#### A. Revenue at Risk Dashboard

**File:** `streamlit_pages/revenue_dashboard.py`

```python
import streamlit as st
import plotly.express as px
from src.data.database import get_revenue_at_risk

st.title("💰 Revenue at Risk Dashboard")

data = get_revenue_at_risk()

# Filters
col1, col2 = st.columns(2)
with col1:
    selected_plan = st.selectbox("Plan", ["All"] + data["plan_id"].unique().tolist())
with col2:
    selected_domain = st.selectbox("Domain", ["All"] + data["domain"].unique().tolist())

# Apply filters
filtered_data = data.copy()
if selected_plan != "All":
    filtered_data = filtered_data[filtered_data["plan_id"] == selected_plan]
if selected_domain != "All":
    filtered_data = filtered_data[filtered_data["domain"] == selected_domain]

# Summary metrics
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Revenue at Risk", f"${filtered_data['revenue_at_risk'].sum():,.0f}")
with col2:
    st.metric("Total Gaps", f"{filtered_data['members_needed'].sum():,.0f}")
with col3:
    st.metric("Measures at Risk", filtered_data["measure_id"].nunique())
with col4:
    st.metric("Avg Value/Gap", f"${filtered_data['revenue_per_member_closed'].mean():,.2f}")

# Charts
col1, col2 = st.columns(2)

with col1:
    fig = px.bar(
        filtered_data.groupby("plan_id")["revenue_at_risk"].sum().reset_index(),
        x="plan_id",
        y="revenue_at_risk",
        title="Revenue at Risk by Plan"
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig = px.bar(
        filtered_data.groupby("domain")["revenue_at_risk"].sum().reset_index(),
        x="domain",
        y="revenue_at_risk",
        title="Revenue at Risk by Domain"
    )
    st.plotly_chart(fig, use_container_width=True)

# Detailed table
st.subheader("Detailed View")
st.dataframe(filtered_data, use_container_width=True)
```

#### B. Velocity Tracking Dashboard

**File:** `streamlit_pages/velocity_dashboard.py`

```python
import streamlit as st
import plotly.express as px
from src.data.database import get_velocity_dashboard

st.title("📈 Gap Closure Velocity Dashboard")

data = get_velocity_dashboard()

# Summary
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Avg Weekly Velocity", f"{data['gaps_per_week'].mean():.2f} gaps/week")
with col2:
    st.metric("Avg Closure Rate", f"{data['closure_rate_pct'].mean():.1f}%")
with col3:
    st.metric("Total Open Gaps", f"{data['gaps_open_end'].sum():,.0f}")

# Velocity by plan
fig = px.bar(
    data.groupby("plan_id")["gaps_per_week"].mean().reset_index(),
    x="plan_id",
    y="gaps_per_week",
    title="Average Weekly Velocity by Plan"
)
st.plotly_chart(fig, use_container_width=True)

# Status breakdown
status_counts = data["closure_status"].value_counts()
fig = px.pie(
    values=status_counts.values,
    names=status_counts.index,
    title="Closure Status Distribution"
)
st.plotly_chart(fig, use_container_width=True)
```

#### C. Member Segmentation Dashboard

**File:** `streamlit_pages/segmentation_dashboard.py`

```python
import streamlit as st
import plotly.express as px
from src.data.database import get_member_segmentation

st.title("👥 Member Segmentation Dashboard")

# Filters
col1, col2 = st.columns(2)
with col1:
    selected_plan = st.selectbox("Plan", ["All"] + ["H1234-001", "H5678-002", "H9012-003"])
with col2:
    selected_risk = st.selectbox("Risk Category", ["All", "Low Risk", "Medium Risk", "High Risk", "Very High Risk"])

filters = {}
if selected_plan != "All":
    filters["plan_id"] = selected_plan
if selected_risk != "All":
    filters["risk_category"] = selected_risk

data = get_member_segmentation(filters)

# Summary cards
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Members", f"{data['member_count'].sum():,.0f}")
with col2:
    st.metric("Avg Risk Score", f"{data['avg_risk_score'].mean():.3f}")
with col3:
    st.metric("Total Gaps", f"{data['total_care_gaps'].sum():,.0f}")
with col4:
    st.metric("Gaps/Member", f"{data['gaps_per_member'].mean():.2f}")

# Risk distribution
fig = px.bar(
    data.groupby("risk_category")["member_count"].sum().reset_index(),
    x="risk_category",
    y="member_count",
    title="Member Distribution by Risk Category"
)
st.plotly_chart(fig, use_container_width=True)
```

---

### Step 5: Update Main App Navigation

**File:** `streamlit_app.py`

Add new pages to navigation:

```python
# In sidebar or navigation
pages = {
    "Financial Overview": streamlit_pages.financial_overview,
    "Revenue at Risk": streamlit_pages.revenue_dashboard,  # NEW
    "Velocity Tracking": streamlit_pages.velocity_dashboard,  # NEW
    "Member Segmentation": streamlit_pages.segmentation_dashboard,  # NEW
    "Operations Command": streamlit_pages.operations_command,
    "Predictive Priority": streamlit_pages.predictive_priority,
    # ... existing pages
}
```

---

## 🚀 Implementation Checklist

### Phase 2A: Database Connection (1-2 hours)
- [ ] Create `src/data/database.py`
- [ ] Create `.streamlit/secrets.toml`
- [ ] Test database connection
- [ ] Verify all views are accessible

### Phase 2B: Enhance Existing Pages (2-3 hours)
- [ ] Update Financial Overview with real data
- [ ] Update Operations Command with velocity data
- [ ] Add database queries to Predictive Priority
- [ ] Test all existing pages with real data

### Phase 2C: Create New Pages (3-4 hours)
- [ ] Create Revenue at Risk Dashboard
- [ ] Create Velocity Tracking Dashboard
- [ ] Create Member Segmentation Dashboard
- [ ] Create Geographic Heat Map page
- [ ] Create ROI Analysis Dashboard

### Phase 2D: Polish & Testing (1-2 hours)
- [ ] Add error handling
- [ ] Add loading states
- [ ] Test with different filters
- [ ] Optimize query performance
- [ ] Add export functionality

---

## 📋 Quick Start Commands

### 1. Create Database Module
```bash
# I can create this file for you
# Just say: "Create database connection module"
```

### 2. Update Streamlit Config
```bash
# Create .streamlit/secrets.toml with database credentials
```

### 3. Test Connection
```python
# In Streamlit app
from src.data.database import get_revenue_at_risk
st.write(get_revenue_at_risk())
```

### 4. Run Streamlit
```bash
streamlit run streamlit_app.py
```

---

## 🎯 Next Actions

**Option 1: Quick Integration (Recommended)**
- Create database connection module
- Update 2-3 existing pages with real data
- Add 1-2 new dashboard pages
- **Time:** 4-6 hours

**Option 2: Full Integration**
- Complete database connection
- Update all existing pages
- Create all new dashboard pages
- Add advanced features
- **Time:** 1-2 days

**Option 3: Phase 2 SQL First**
- Create additional operational views
- Enhance database analytics
- Then integrate with Streamlit
- **Time:** 2-3 hours for SQL, then integration

---

## 💡 Recommendations

1. **Start with database connection module** - Foundation for everything
2. **Enhance Financial Overview first** - High impact, uses existing page
3. **Add Revenue at Risk Dashboard** - New page, showcases database
4. **Then add Velocity and Segmentation** - Complete the suite

---

**Ready to proceed?** Let me know which option you prefer:
- "Create database connection module"
- "Create Phase 2 operational views"
- "Integrate database with Streamlit"
- "Create new dashboard pages"

