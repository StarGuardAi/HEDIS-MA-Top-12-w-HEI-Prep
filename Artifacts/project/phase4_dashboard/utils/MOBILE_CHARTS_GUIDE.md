# Mobile Charts Usage Guide

## Overview

Mobile-optimized Plotly charts for HEDIS Portfolio Optimizer, designed for touch interaction and readability on smartphones (375-428px width).

## Quick Start

```python
import streamlit as st
from utils.mobile_charts import (
    create_mobile_priority_bars,
    create_mobile_star_gauge,
    create_mobile_metric_bar,
    create_mobile_sparkline,
    MOBILE_CONFIG
)

# Create chart
fig = create_mobile_priority_bars(df)

# Display in Streamlit
st.plotly_chart(fig, use_container_width=True, config=MOBILE_CONFIG)
```

## Chart Functions

### 1. Mobile Priority Bars

**Purpose:** Show top N opportunities as horizontal bars

**Features:**
- Top 5 opportunities only (configurable)
- Horizontal bars (easier on mobile)
- Color-coded by closure rate
- Large, readable labels
- Financial impact in $K

**Usage:**
```python
df = pd.DataFrame({
    'measure_name': ['HbA1c Testing', 'Blood Pressure Control'],
    'financial_impact': [285000, 320000],
    'predicted_closure_rate': [0.93, 0.88]
})

fig = create_mobile_priority_bars(df, top_n=5, height=300)
st.plotly_chart(fig, use_container_width=True, config=MOBILE_CONFIG)
```

**Parameters:**
- `df`: DataFrame with measure data
- `measure_name_col`: Column name for measures (default: "measure_name")
- `financial_impact_col`: Column name for financial impact (default: "financial_impact")
- `closure_rate_col`: Column name for closure rate (default: "predicted_closure_rate")
- `top_n`: Number of top items to show (default: 5)
- `height`: Chart height in pixels (default: 300)

### 2. Mobile Star Gauge

**Purpose:** Simplified star rating display

**Features:**
- Large number display (48px font)
- Minimal gauge decoration
- Color zones (Red/Yellow/Green)
- No target/delta (simplified)

**Usage:**
```python
fig = create_mobile_star_gauge(4.5, height=250)
st.plotly_chart(fig, use_container_width=True, config=MOBILE_CONFIG)
```

**Parameters:**
- `current_value`: Current star rating (1.0 to 5.0)
- `min_value`: Minimum gauge value (default: 1.0)
- `max_value`: Maximum gauge value (default: 5.0)
- `height`: Chart height in pixels (default: 250)

### 3. Mobile Metric Bar

**Purpose:** Single measure comparison (current vs benchmark)

**Features:**
- One measure per chart
- Color-coded (Green if above benchmark, Red if below)
- Large percentage labels on bars
- Stack vertically for multiple measures

**Usage:**
```python
fig = create_mobile_metric_bar(
    "HbA1c Testing",
    current_value=45.2,
    benchmark_value=40.0,
    value_type="percentage",
    height=150
)
st.plotly_chart(fig, use_container_width=True, config=MOBILE_CONFIG)
```

**Parameters:**
- `measure_name`: Name of measure (will be abbreviated)
- `current_value`: Current rate (0-100 for percentage)
- `benchmark_value`: Benchmark rate (0-100 for percentage)
- `value_type`: "percentage" or "currency" (default: "percentage")
- `height`: Chart height in pixels (default: 150)

**Stacking Multiple Measures:**
```python
measures = [
    {'name': 'HbA1c Testing', 'current': 45.2, 'benchmark': 40.0},
    {'name': 'Blood Pressure', 'current': 52.8, 'benchmark': 45.0}
]

for measure in measures:
    fig = create_mobile_metric_bar(
        measure['name'],
        measure['current'],
        measure['benchmark']
    )
    st.plotly_chart(fig, use_container_width=True, config=MOBILE_CONFIG)
```

### 4. Mobile Sparkline

**Purpose:** Minimal trend visualization (last 90 days)

**Features:**
- Pure sparkline style (no axes, grid, legend)
- Last 90 days only
- Single measure at a time
- Trend direction indicator (📈 📉 ➡️)
- Subtle background

**Usage:**
```python
df = pd.DataFrame({
    'date': pd.date_range('2024-01-01', periods=90, freq='D'),
    'compliance_rate': [35 + i*0.15 for i in range(90)]
})

fig = create_mobile_sparkline(
    df,
    date_col='date',
    value_col='compliance_rate',
    measure_name='HbA1c Testing',
    days=90,
    height=100
)
st.plotly_chart(fig, use_container_width=True, config=MOBILE_CONFIG)
```

**Parameters:**
- `df`: DataFrame with time series data
- `date_col`: Column name for dates (default: "date")
- `value_col`: Column name for values (default: "compliance_rate")
- `measure_name`: Name of measure (optional, for title)
- `days`: Number of days to show (default: 90)
- `height`: Chart height in pixels (default: 100)

## Mobile Configuration

### MOBILE_CONFIG

Pre-configured Plotly config for mobile:

```python
MOBILE_CONFIG = {
    'displayModeBar': False,  # Hide toolbar
    'staticPlot': False,       # Keep interactivity
    'doubleClick': False,      # Prevent zoom
    'showTips': False,         # No hover tips
    'responsive': True,        # Resize with container
    'scrollZoom': False,       # Disable pinch zoom
    'displaylogo': False       # Remove Plotly logo
}
```

### MOBILE_COLORS

High-contrast color scheme:

```python
MOBILE_COLORS = {
    'primary': '#0066cc',      # Strong blue
    'success': '#00cc66',      # Bright green
    'warning': '#ffaa00',      # Orange
    'danger': '#cc0000',       # Red
    'text': '#000000',         # Black
    'background': '#ffffff',   # White
    'light_gray': '#f5f5f5'    # Light background
}
```

## Mobile Optimization Features

### Touch-Friendly

- ✅ No hover tooltips (tap-based)
- ✅ Large touch targets (44px+)
- ✅ No accidental zoom (disabled)
- ✅ Single tap for details

### Readability

- ✅ High contrast colors
- ✅ Large text (12px minimum)
- ✅ Abbreviated labels
- ✅ Clear visual hierarchy

### Performance

- ✅ Top N only (not all data)
- ✅ Reduced data points
- ✅ Simplified styling
- ✅ Fast rendering

### Layout

- ✅ Single column
- ✅ Stacked vertically
- ✅ Full-width charts
- ✅ Consistent spacing

## Best Practices

### 1. Limit Data Points

```python
# ✅ Good: Top 5 only
fig = create_mobile_priority_bars(df, top_n=5)

# ❌ Bad: All data
fig = create_mobile_priority_bars(df, top_n=100)
```

### 2. Stack Charts Vertically

```python
# ✅ Good: One chart per row
for measure in top_3:
    fig = create_mobile_metric_bar(...)
    st.plotly_chart(fig, use_container_width=True, config=MOBILE_CONFIG)

# ❌ Bad: Multiple charts in columns
col1, col2 = st.columns(2)  # Too narrow on mobile
```

### 3. Use Appropriate Heights

```python
# ✅ Good: Appropriate heights
fig1 = create_mobile_priority_bars(df, height=300)  # Main chart
fig2 = create_mobile_metric_bar(..., height=150)    # Smaller chart
fig3 = create_mobile_sparkline(..., height=100)     # Sparkline

# ❌ Bad: Too tall
fig = create_mobile_priority_bars(df, height=600)  # Takes too much space
```

### 4. Always Use MOBILE_CONFIG

```python
# ✅ Good: Mobile config
st.plotly_chart(fig, use_container_width=True, config=MOBILE_CONFIG)

# ❌ Bad: Default config (shows toolbar, allows zoom)
st.plotly_chart(fig, use_container_width=True)
```

## Common Patterns

### Pattern 1: Priority View

```python
# Top opportunities
st.markdown("### Top 5 Opportunities")
fig = create_mobile_priority_bars(df, top_n=5)
st.plotly_chart(fig, use_container_width=True, config=MOBILE_CONFIG)
```

### Pattern 2: Measure Comparison

```python
# Compare top 3 measures
st.markdown("### Key Measures")
for measure in top_3_measures:
    fig = create_mobile_metric_bar(
        measure['name'],
        measure['current'],
        measure['benchmark']
    )
    st.plotly_chart(fig, use_container_width=True, config=MOBILE_CONFIG)
```

### Pattern 3: Dashboard View

```python
# Star rating
st.markdown("### Current Star Rating")
fig_gauge = create_mobile_star_gauge(4.5)
st.plotly_chart(fig_gauge, use_container_width=True, config=MOBILE_CONFIG)

# Trend
st.markdown("### Recent Trend")
fig_spark = create_mobile_sparkline(df, measure_name="Overall")
st.plotly_chart(fig_spark, use_container_width=True, config=MOBILE_CONFIG)
```

## Troubleshooting

### Chart Not Displaying

- Check DataFrame is not empty
- Verify column names match parameters
- Ensure data types are correct

### Text Too Small

- Charts use 12px minimum font
- Labels are automatically abbreviated
- Check mobile CSS is applied

### Performance Issues

- Reduce `top_n` parameter
- Limit data to last 90 days
- Use caching for data loading

### Touch Not Working

- Ensure `MOBILE_CONFIG` is used
- Check `dragmode: False` in layout
- Verify `hovermode: False`

## Examples

See `mobile_charts.py` for complete examples and `mobile_view.py` for integration patterns.

---

## Support

For questions or issues:
- 📧 **Email**: reichert.starguardai@gmail.com
- 🔗 **LinkedIn**: [sentinel-analytics](https://www.linkedin.com/in/sentinel-analytics/)
- 💻 **GitHub**: [HEDIS-MA-Top-12-w-HEI-Prep](https://github.com/StarGuardAi/HEDIS-MA-Top-12-w-HEI-Prep/blob/main/README.md)
- 🎨 **Portfolio**: [Canva Portfolio](https://www.canva.com/design/DAG2WzhiLwM/N_iXUe3eEKL3dzQ2M_0PgQ/edit)

---

**Mobile Charts** | Touch-optimized | High contrast | Fast rendering 📱

