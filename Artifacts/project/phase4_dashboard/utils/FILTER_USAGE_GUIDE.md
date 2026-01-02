# Advanced Filtering System Usage Guide

## Overview

Enterprise-grade filtering system for HEDIS Portfolio Optimizer with preset management, hierarchical organization, and comprehensive filter controls.

## Quick Start

```python
import streamlit as st
from utils.advanced_filters import (
    init_filter_state,
    render_sidebar_filters,
    apply_filters,
    get_filter_summary
)

# Initialize filters
init_filter_state()

# Render sidebar
render_sidebar_filters(available_measures=['HbA1c Testing', 'Blood Pressure Control'])

# Load and filter data
df = load_your_data()
filtered_df = apply_filters(df)

# Display results
st.dataframe(filtered_df)
```

## Filter Sections

### 1. Time Period 📅

**Presets:**
- Current Quarter
- Last 90 Days
- Year to Date
- Last Quarter
- Last 12 Months
- Custom (date range picker)

**Features:**
- Compare to Previous Period toggle
- Period summary display
- Automatic date range calculation

### 2. Measures & Metrics 📊

**Features:**
- Multi-select with search
- Quick presets:
  - Top 5 by ROI
  - All Diabetes Measures
  - Star Rating Critical
- Select All / Clear All buttons
- Gap Status filter
- Prediction Confidence filter
- Star Rating Impact filter

### 3. Member Demographics 👥

**Filters:**
- Age Bands (multi-select)
- Gender (radio: All, Male, Female, Other)
- Risk Score (slider range 0-10)
- Member Tenure (dropdown)

### 4. Financial Thresholds 💰

**Filters:**
- Minimum Member Count
- Minimum Financial Impact ($)
- Minimum Predicted Closure Rate (%)
- Total Budget Cap ($)

### 5. Advanced Options ⚙️

**Options:**
- Show Only High Confidence Predictions
- Include Historical Data
- Exclude Members with Recent Contact
- Minimum Data Quality Score
- Provider Networks (if available)
- Geographic Regions (if available)

### 6. Filter Presets 💾

**Features:**
- Save current filter configuration
- Load saved presets
- Delete presets
- Export/Import presets as JSON
- Built-in presets:
  - Executive Summary
  - Care Coordinator View
  - Financial Focus

## API Reference

### `init_filter_state()`

Initialize filter state in session_state with default values.

```python
init_filter_state()
```

### `render_sidebar_filters(available_measures: List[str] = None)`

Render complete filter sidebar with all sections.

```python
render_sidebar_filters(
    available_measures=['HbA1c Testing', 'Blood Pressure Control']
)
```

### `apply_filters(df: pd.DataFrame) -> pd.DataFrame`

Apply all active filters to DataFrame.

```python
filtered_df = apply_filters(df)
```

### `get_filter_summary() -> str`

Get human-readable summary of active filters.

```python
summary = get_filter_summary()
st.info(f"🔍 {summary}")
```

### `count_active_filters() -> int`

Count number of active (non-default) filters.

```python
active_count = count_active_filters()
st.metric("Active Filters", active_count)
```

### `validate_filters() -> Tuple[bool, Optional[str]]`

Validate filter combinations for logical consistency.

```python
is_valid, error_msg = validate_filters()
if not is_valid:
    st.error(f"Filter Error: {error_msg}")
```

### `reset_filters()`

Reset all filters to defaults.

```python
if st.button("Reset"):
    reset_filters()
    st.rerun()
```

### `save_preset(name: str)`

Save current filter state as a preset.

```python
save_preset("My Custom View")
```

### `load_preset(name: str)`

Load a saved preset into current filters.

```python
load_preset("Executive Summary")
```

## Filter State Structure

Filters are stored in `st.session_state.filters`:

```python
{
    # Time Period
    'time_preset': 'Current Quarter',
    'start_date': date(2024, 1, 1),
    'end_date': date(2024, 12, 31),
    'compare_previous': False,
    
    # Measures
    'measures': ['HbA1c Testing', 'Blood Pressure Control'],
    'gap_status': ['Open', 'Pending'],
    'prediction_confidence': ['High', 'Medium', 'Low'],
    'star_rating_impact': [],
    
    # Demographics
    'age_bands': ['65-74', '75-84'],
    'gender': 'All',
    'risk_score_min': 0.0,
    'risk_score_max': 10.0,
    'member_tenure': 'All',
    
    # Financial
    'min_member_count': 50,
    'min_financial_impact': 1000.0,
    'min_closure_rate': 30.0,
    'max_budget_cap': None,
    
    # Advanced
    'high_confidence_only': False,
    'include_historical': True,
    'exclude_recent_contact': False,
    'min_data_quality': 0.0
}
```

## Integration Patterns

### Pattern 1: Basic Integration

```python
init_filter_state()
render_sidebar_filters()
df = load_data()
filtered_df = apply_filters(df)
st.dataframe(filtered_df)
```

### Pattern 2: With Validation

```python
init_filter_state()
render_sidebar_filters()

is_valid, error = validate_filters()
if not is_valid:
    st.error(error)
    st.stop()

df = apply_filters(load_data())
```

### Pattern 3: With Caching

```python
@st.cache_data
def get_filtered_data(filters_hash):
    df = load_data()
    return apply_filters(df)

filters_hash = hash(str(st.session_state.filters))
filtered_df = get_filtered_data(filters_hash)
```

### Pattern 4: Auto-Apply

```python
init_filter_state()
render_sidebar_filters()

# Filters auto-apply on change
df = load_data()
filtered_df = apply_filters(df)

# Show impact
st.info(f"Showing {len(filtered_df)} of {len(df)} records")
```

## Preset Management

### Save Preset

```python
preset_name = st.text_input("Preset Name")
if st.button("Save"):
    save_preset(preset_name)
```

### Load Preset

```python
presets = list(st.session_state.filter_presets.keys())
selected = st.selectbox("Load Preset", presets)
if st.button("Load"):
    load_preset(selected)
    st.rerun()
```

### Export/Import

```python
# Export
export_json = export_presets()
st.download_button("Download", export_json, "presets.json")

# Import
uploaded = st.file_uploader("Upload Presets", type=['json'])
if uploaded:
    import_presets(uploaded)
```

## Data Requirements

Your DataFrame should include these columns for filters to work:

**Required:**
- `measure_name`: HEDIS measure names
- `gap_status`: Status values
- `date` or `intervention_date`: Date column

**Optional (for advanced filtering):**
- `age_band`: Age band categories
- `gender`: Gender values
- `risk_score`: Numeric risk score
- `member_tenure`: Tenure in years
- `financial_value`: Financial impact
- `predicted_closure_probability`: Prediction value (0-1)
- `prediction_confidence`: Confidence level
- `last_contact_date`: Last contact date
- `data_quality_score`: Quality score (0-100)

## Performance Tips

1. **Caching**: Use `@st.cache_data` for expensive filter operations
2. **Incremental Filtering**: Apply most selective filters first
3. **Debouncing**: Add small delay for rapid filter changes
4. **Lazy Loading**: Load data only when filters are applied

## Error Handling

```python
try:
    filtered_df = apply_filters(df)
    if filtered_df.empty:
        st.warning("No data matches filters")
        st.info("Try adjusting your criteria")
except Exception as e:
    st.error(f"Filter error: {str(e)}")
```

## Accessibility

- All inputs have clear labels
- Helpful tooltips on all controls
- Keyboard navigation supported
- Screen reader friendly

## Troubleshooting

### Filters Not Applying

- Check that `init_filter_state()` is called
- Verify column names match expected values
- Check data types match filter expectations

### Empty Results

- Validate filters with `validate_filters()`
- Check date ranges are valid
- Verify measure names exist in data
- Lower financial thresholds

### Performance Issues

- Enable caching for data loading
- Reduce number of active filters
- Filter data before passing to expensive operations

## Examples

See `filter_examples.py` for complete working examples:
- Basic integration
- Validation and error handling
- Performance optimization
- Full dashboard integration
- Auto-apply patterns
- Filter impact analysis

## Support

For questions or issues:
- 📧 **Email**: reichert.starguardai@gmail.com
- 🔗 **LinkedIn**: [sentinel-analytics](https://www.linkedin.com/in/sentinel-analytics/)
- 💻 **GitHub**: [HEDIS-MA-Top-12-w-HEI-Prep](https://github.com/StarGuardAi/HEDIS-MA-Top-12-w-HEI-Prep/blob/main/README.md)
- 🎨 **Portfolio**: [Canva Portfolio](https://www.canva.com/design/DAG2WzhiLwM/N_iXUe3eEKL3dzQ2M_0PgQ/edit)

