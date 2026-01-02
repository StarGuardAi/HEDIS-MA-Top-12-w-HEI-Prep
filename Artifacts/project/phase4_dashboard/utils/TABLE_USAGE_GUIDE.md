# Interactive Member Tables Usage Guide

## Overview

Two production-ready AgGrid table implementations for healthcare member management:

1. **Master Member List** - Full-featured Excel-like table with selection, filtering, grouping
2. **Summary Measures** - Simplified aggregated view for quick insights

## Installation

Ensure `streamlit-aggrid` is installed:

```bash
pip install streamlit-aggrid>=0.3.4
```

## Quick Start

### Master Member List Table

```python
import streamlit as st
from utils.member_tables import create_member_grid, get_selection_summary

# Load your data
df = load_member_data()  # Your DataFrame

# Display grid
grid_response, selected_members = create_member_grid(
    df,
    height=600,
    enable_sidebar=True,
    enable_grouping=True,
    page_size=50
)

# Handle selections
if len(selected_members) > 0:
    st.success(f"Selected {len(selected_members)} members")
    
    # Get summary
    summary = get_selection_summary(selected_members)
    st.metric("Total Value", f"${summary['total_financial_value']:,.2f}")
```

### Summary Measures Table

```python
from utils.member_tables import create_summary_grid

# Display summary grid
grid_response, clicked_row = create_summary_grid(
    df,
    height=400,
    page_size=20
)

# Handle drill-down
if clicked_row:
    measure_name = clicked_row['Measure']
    st.info(f"Selected: {measure_name}")
    
    # Filter and show details
    filtered_df = df[df['measure_name'] == measure_name]
    # ... show member details
```

## Required DataFrame Columns

### Master Member List

Your DataFrame must include these columns:

- `member_id`: String (e.g., "M12345678")
- `member_name`: String (PHI - Protected Health Information)
- `date_of_birth`: Date
- `measure_name`: String (HEDIS measure)
- `gap_status`: String ("Open", "Pending", "Closed", "Excluded")
- `predicted_closure_probability`: Float 0-1
- `financial_value`: Float (dollars)
- `last_contact_date`: Date
- `assigned_care_coordinator`: String
- `priority_score`: Integer 1-100
- `days_until_deadline`: Integer

### Summary Measures

Requires:
- `measure_name`
- `gap_status`
- `financial_value`
- `predicted_closure_probability`

(Will be aggregated automatically)

## Features

### Master Member List

✅ **Multi-row selection** with checkboxes  
✅ **Column grouping** by measure_name  
✅ **Row grouping** capability  
✅ **Inline editing** for assigned_care_coordinator  
✅ **Column pinning** (member_id always visible)  
✅ **Sidebar filters** for all columns  
✅ **Color coding** by gap_status (Open=red, Pending=yellow, Closed=green)  
✅ **Formatted currency** for financial_value  
✅ **Formatted dates** (MM/DD/YYYY)  
✅ **Priority badges** (High/Medium/Low)  
✅ **Aggregation footer** with counts and sums  
✅ **Export selected rows** functionality  

### Summary Measures

✅ **Aggregated view** by measure_name  
✅ **Sortable, filterable** columns  
✅ **Conditional formatting** by thresholds  
✅ **Click row to drill down**  
✅ **Quick search** box support  
✅ **Auto-fit columns**  

## Configuration Options

### create_member_grid()

```python
create_member_grid(
    df,                    # Required: DataFrame
    height=600,            # Grid height in pixels
    theme='streamlit',     # 'streamlit' or 'alpine'
    enable_sidebar=True,   # Enable sidebar filters
    enable_grouping=True,   # Enable row grouping
    enable_pagination=True, # Enable pagination
    page_size=50           # Rows per page
)
```

### create_summary_grid()

```python
create_summary_grid(
    df,                    # Required: DataFrame
    height=400,            # Grid height in pixels
    theme='streamlit',     # 'streamlit' or 'alpine'
    page_size=20           # Rows per page
)
```

## Handling Selections

### Extract Selected Rows

```python
grid_response, selected_members = create_member_grid(df)

# selected_members is a DataFrame with selected rows
if len(selected_members) > 0:
    # Work with selected data
    member_ids = selected_members['member_id'].tolist()
    total_value = selected_members['financial_value'].sum()
```

### Get Selection Summary

```python
from utils.member_tables import get_selection_summary

summary = get_selection_summary(selected_members)

# Returns:
# {
#     'count': 25,
#     'total_financial_value': 50000.0,
#     'avg_priority_score': 65.5,
#     'gap_status_counts': {'Open': 15, 'Pending': 10},
#     'measures': ['HbA1c Testing', 'Blood Pressure Control']
# }
```

### Export to Excel Format

```python
from utils.member_tables import export_selected_to_excel_format

export_df = export_selected_to_excel_format(selected_members)

# Use with pandas to_excel or streamlit download_button
csv = export_df.to_csv(index=False)
st.download_button("Download", csv, "members.csv", "text/csv")
```

## Bulk Actions Example

```python
grid_response, selected_members = create_member_grid(df)

if len(selected_members) > 0:
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📧 Assign Coordinator"):
            # Your assignment logic
            assign_coordinator(selected_members)
    
    with col2:
        if st.button("📥 Export Excel"):
            export_df = export_selected_to_excel_format(selected_members)
            csv = export_df.to_csv(index=False)
            st.download_button("Download", csv, "members.csv", "text/csv")
    
    with col3:
        if st.button("📊 View Details"):
            st.dataframe(selected_members, use_container_width=True)
```

## Drill-Down Pattern

```python
# Summary view
summary_response, clicked_row = create_summary_grid(df)

if clicked_row:
    measure_name = clicked_row['Measure']
    
    # Filter original data
    filtered_df = df[df['measure_name'] == measure_name]
    
    # Show detailed member list
    member_response, selected = create_member_grid(filtered_df, height=400)
```

## Session State Management

```python
# Initialize
if 'selected_ids' not in st.session_state:
    st.session_state.selected_ids = []

# Update on selection
grid_response, selected = create_member_grid(df)
if len(selected) > 0:
    st.session_state.selected_ids = selected['member_id'].tolist()

# Use persisted selections
if st.session_state.selected_ids:
    persisted_df = df[df['member_id'].isin(st.session_state.selected_ids)]
```

## Performance Tips

1. **Large Datasets (>10K rows)**: Consider server-side pagination
2. **Filtering**: Apply filters before passing to grid for better performance
3. **Grouping**: Disable if not needed (`enable_grouping=False`)
4. **Virtualization**: Enabled by default for large datasets

## Styling

Tables use healthcare theme colors:
- Primary: `#0066cc` (blue)
- Success: `#00cc66` (green)
- Warning: `#ffcc00` (yellow)
- Error: `#cc0000` (red)

Status badges are styled as pills with color coding.

## Troubleshooting

### Empty DataFrame
- Check that required columns exist
- Verify data types match expected formats

### No Selections
- Ensure `update_mode` includes `SELECTION_CHANGED`
- Check that checkboxes are enabled

### Performance Issues
- Reduce `page_size`
- Disable grouping if not needed
- Filter data before passing to grid

## Examples

See `table_examples.py` for complete working examples:
- Basic usage
- Bulk actions
- Drill-down patterns
- Session state management
- Full integration examples

## Support

For questions or issues:
- 📧 **Email**: reichert.starguardai@gmail.com
- 🔗 **LinkedIn**: [sentinel-analytics](https://www.linkedin.com/in/sentinel-analytics/)
- 💻 **GitHub**: [HEDIS-MA-Top-12-w-HEI-Prep](https://github.com/StarGuardAi/HEDIS-MA-Top-12-w-HEI-Prep/blob/main/README.md)
- 🎨 **Portfolio**: [Canva Portfolio](https://www.canva.com/design/DAG2WzhiLwM/N_iXUe3eEKL3dzQ2M_0PgQ/edit)

