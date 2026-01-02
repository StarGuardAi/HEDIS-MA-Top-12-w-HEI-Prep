# Responsive Layout System Usage Guide

## Overview

Universal responsive layout system for HEDIS Portfolio Optimizer that adapts to desktop, tablet, and mobile with a single codebase.

## Quick Start

```python
import streamlit as st
from utils.responsive_layout import (
    DeviceDetector,
    ResponsiveColumns,
    ResponsiveConfig,
    ResponsiveNav,
    ResponsiveChart,
    ResponsiveTable
)

# Initialize
DeviceDetector.init()

# Apply CSS
st.markdown(ResponsiveConfig.get_css(), unsafe_allow_html=True)

# Use responsive components
rc = ResponsiveColumns()
rc.metric_grid(metrics_data)
```

## Core Components

### 1. DeviceDetector

**Purpose:** Detect and manage device type

**Methods:**
- `init()` - Initialize device detection
- `get_device_type()` - Get current device ('desktop', 'tablet', 'mobile')
- `set_device_type(type)` - Manually set device type
- `render_device_toggle()` - Show device selector (for testing)

**Usage:**
```python
# Initialize
DeviceDetector.init()

# Get current device
device = DeviceDetector.get_device_type()  # 'desktop', 'tablet', or 'mobile'

# Set device manually
DeviceDetector.set_device_type('mobile')

# Show toggle (for testing)
DeviceDetector.render_device_toggle()
```

### 2. ResponsiveConfig

**Purpose:** Device-specific configuration values

**Configuration Keys:**
- `chart_height` - Chart height in pixels
- `table_height` - Table height in pixels
- `font_size_h1/h2/h3` - Heading font sizes
- `metric_font_size` - Metric value font size
- `container_padding` - Main container padding
- `show_sidebar` - Whether to show sidebar
- `use_tabs` - Whether to use tabs for navigation
- `max_table_columns` - Maximum table columns
- `items_per_page` - Items per page for pagination
- `show_tooltips` - Whether to show tooltips

**Usage:**
```python
# Get single config value
height = ResponsiveConfig.get('chart_height')  # 600 for desktop, 300 for mobile

# Get all config
config = ResponsiveConfig.get_all()

# Get CSS
css = ResponsiveConfig.get_css()
st.markdown(css, unsafe_allow_html=True)
```

### 3. ResponsiveColumns

**Purpose:** Create responsive column layouts

**Methods:**
- `get_columns(desktop, tablet, mobile)` - Get columns for current device
- `metric_grid(metrics_data)` - Display metrics in grid
- `card_grid(cards_data)` - Display cards in grid

**Usage:**
```python
rc = ResponsiveColumns()

# Get columns (4 on desktop, 2 on tablet, 1 on mobile)
cols = rc.get_columns(desktop=4, tablet=2, mobile=1)

# Display metrics
metrics = [
    {'label': 'ROI', 'value': '498%', 'delta': '+$935K'},
    {'label': 'Star Rating', 'value': '4.5 ⭐', 'delta': '+0.5'}
]
rc.metric_grid(metrics)

# Display cards
cards = [
    {'title': 'Card 1', 'content': 'Content 1'},
    {'title': 'Card 2', 'content': 'Content 2'}
]
rc.card_grid(cards)
```

### 4. ResponsiveNav

**Purpose:** Adaptive navigation system

**Usage:**
```python
views = {
    '📊 Dashboard': 'dashboard',
    '🎯 Opportunities': 'opportunities',
    '📈 Measures': 'measures'
}

nav = ResponsiveNav(views)

# Desktop/Tablet: Returns generator for tabs
if ResponsiveConfig.get('use_tabs'):
    for view_id in nav.render():
        if view_id == 'dashboard':
            render_dashboard()

# Mobile: Returns view_id string
else:
    view_id = nav.render()
    if view_id == 'dashboard':
        render_dashboard()
```

### 5. ResponsiveChart

**Purpose:** Device-adaptive Plotly charts

**Methods:**
- `get_plotly_config()` - Get Plotly config for device
- `get_layout_updates()` - Get layout updates for device
- `render(fig)` - Render chart with device settings

**Usage:**
```python
import plotly.express as px

fig = px.bar(x=[1,2,3], y=[1,2,3])
ResponsiveChart.render(fig)
```

### 6. ResponsiveTable

**Purpose:** Device-adaptive tables

**Usage:**
```python
df = pd.DataFrame({'A': [1,2,3], 'B': [4,5,6]})
ResponsiveTable.render(df)
```

## Complete App Template

```python
import streamlit as st
import pandas as pd
from utils.responsive_layout import (
    DeviceDetector,
    ResponsiveColumns,
    ResponsiveConfig,
    ResponsiveNav,
    ResponsiveChart,
    ResponsiveTable
)

# Page config
st.set_page_config(
    page_title="HEDIS Portfolio Optimizer",
    page_icon="⭐",
    layout="wide",
    initial_sidebar_state="auto"
)

# Initialize
DeviceDetector.init()

# Apply CSS
st.markdown(ResponsiveConfig.get_css(), unsafe_allow_html=True)

# Device toggle (for testing - remove in production)
with st.sidebar:
    DeviceDetector.render_device_toggle()

# Header
st.title("⭐ HEDIS Portfolio Optimizer")

# Responsive metrics
rc = ResponsiveColumns()
metrics = [
    {'label': 'ROI', 'value': '498%', 'delta': '+$935K'},
    {'label': 'Star Rating', 'value': '4.5 ⭐', 'delta': '+0.5'},
    {'label': 'Members', 'value': '10,000+', 'delta': '+1,200'},
    {'label': 'Compliance', 'value': '93%', 'delta': '+8%'}
]
rc.metric_grid(metrics)

# Responsive navigation
views = {
    '📊 Dashboard': 'dashboard',
    '🎯 Opportunities': 'opportunities'
}
nav = ResponsiveNav(views)

# Route views
if ResponsiveConfig.get('use_tabs'):
    for view_id in nav.render():
        render_view(view_id)
else:
    view_id = nav.render()
    render_view(view_id)
```

## Device-Specific Behaviors

### Desktop (Default)

- **Columns:** 4 columns for metrics
- **Navigation:** Tabs
- **Charts:** Full toolbar, 600px height
- **Tables:** All columns visible
- **Sidebar:** Visible
- **Tooltips:** Enabled

### Tablet

- **Columns:** 2 columns for metrics
- **Navigation:** Tabs
- **Charts:** Limited toolbar, 400px height
- **Tables:** Max 6 columns
- **Sidebar:** Visible
- **Tooltips:** Enabled

### Mobile

- **Columns:** 1 column (stacked)
- **Navigation:** Selectbox dropdown
- **Charts:** No toolbar, 300px height
- **Tables:** Max 3 columns
- **Sidebar:** Hidden
- **Tooltips:** Disabled

## Best Practices

### 1. Always Initialize

```python
# At top of app
DeviceDetector.init()
st.markdown(ResponsiveConfig.get_css(), unsafe_allow_html=True)
```

### 2. Use Responsive Components

```python
# ✅ Good: Use ResponsiveColumns
rc = ResponsiveColumns()
rc.metric_grid(metrics)

# ❌ Bad: Hard-coded columns
col1, col2, col3, col4 = st.columns(4)  # Breaks on mobile
```

### 3. Check Device Type

```python
device = DeviceDetector.get_device_type()

if device == 'mobile':
    # Mobile-specific code
    pass
elif device == 'tablet':
    # Tablet-specific code
    pass
else:
    # Desktop code
    pass
```

### 4. Use Config Values

```python
# ✅ Good: Use config
height = ResponsiveConfig.get('chart_height')
fig.update_layout(height=height)

# ❌ Bad: Hard-coded values
fig.update_layout(height=600)  # Too tall on mobile
```

### 5. Test All Devices

```python
# Use device toggle to test
DeviceDetector.render_device_toggle()
```

## Integration Examples

### Example 1: Responsive Metrics

```python
rc = ResponsiveColumns()

metrics = [
    {'label': 'ROI', 'value': '498%', 'delta': '+$935K'},
    {'label': 'Star Rating', 'value': '4.5 ⭐', 'delta': '+0.5'},
    {'label': 'Members', 'value': '10,000+', 'delta': '+1,200'},
    {'label': 'Compliance', 'value': '93%', 'delta': '+8%'}
]

rc.metric_grid(metrics)
# Desktop: 4 columns
# Tablet: 2 columns (2 rows)
# Mobile: 1 column (4 rows with separators)
```

### Example 2: Responsive Navigation

```python
views = {
    '📊 Dashboard': 'dashboard',
    '🎯 Opportunities': 'opportunities',
    '📈 Measures': 'measures'
}

nav = ResponsiveNav(views)

if ResponsiveConfig.get('use_tabs'):
    # Desktop/Tablet: Tabs
    for view_id in nav.render():
        render_view(view_id)
else:
    # Mobile: Selectbox
    view_id = nav.render()
    render_view(view_id)
```

### Example 3: Responsive Charts

```python
import plotly.express as px

fig = px.bar(df, x='measure', y='roi')
ResponsiveChart.render(fig)
# Automatically adjusts height, margins, toolbar for device
```

### Example 4: Responsive Tables

```python
ResponsiveTable.render(df)
# Desktop: All columns, 600px height
# Tablet: Max 6 columns, 500px height
# Mobile: Max 3 columns, 400px height
```

## Testing

### Manual Testing

1. Use device toggle in sidebar
2. Switch between desktop/tablet/mobile
3. Verify layout adapts correctly
4. Check all components render properly

### Testing Checklist

- [ ] Metrics display correctly on all devices
- [ ] Navigation works (tabs on desktop, selectbox on mobile)
- [ ] Charts render with appropriate size
- [ ] Tables limit columns on mobile
- [ ] Buttons are touch-friendly on mobile
- [ ] Text is readable on all devices
- [ ] Sidebar hidden on mobile
- [ ] CSS applies correctly

## Troubleshooting

### Layout Not Adapting

- Check `DeviceDetector.init()` is called
- Verify `ResponsiveConfig.get_css()` is applied
- Check device type in session state

### Columns Not Stacking

- Use `ResponsiveColumns.get_columns()` instead of `st.columns()`
- Check column parameters (desktop/tablet/mobile)

### Charts Too Large/Small

- Use `ResponsiveChart.render()` instead of `st.plotly_chart()`
- Check `chart_height` in config

### Navigation Not Working

- Verify `use_tabs` config value
- Check view handlers are defined
- Ensure state is initialized

## Performance

- CSS is cached in session state
- Config values are accessed efficiently
- No unnecessary re-renders
- Responsive components are lightweight

## Examples

See `responsive_layout.py` for complete examples and integration patterns.

---

## Support

For questions or issues:
- 📧 **Email**: reichert.starguardai@gmail.com
- 🔗 **LinkedIn**: [sentinel-analytics](https://www.linkedin.com/in/sentinel-analytics/)
- 💻 **GitHub**: [HEDIS-MA-Top-12-w-HEI-Prep](https://github.com/StarGuardAi/HEDIS-MA-Top-12-w-HEI-Prep/blob/main/README.md)
- 🎨 **Portfolio**: [Canva Portfolio](https://www.canva.com/design/DAG2WzhiLwM/N_iXUe3eEKL3dzQ2M_0PgQ/edit)

---

**Responsive Layout System** | Universal codebase | Desktop • Tablet • Mobile 📱🖥️

