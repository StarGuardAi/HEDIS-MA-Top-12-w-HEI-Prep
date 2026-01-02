# Mobile Tables Usage Guide

## Overview

Mobile-friendly alternatives to traditional data tables for HEDIS Portfolio Optimizer. Optimized for touch interaction and readability on smartphones (375-428px width).

## Quick Start

```python
import streamlit as st
from utils.mobile_tables import (
    create_mobile_member_cards,
    create_mobile_simple_table,
    create_mobile_summary_with_drilldown,
    create_swipeable_member_cards
)

# Card-based view (recommended for small lists)
create_mobile_member_cards(df, limit=10)

# Simplified table (for quick reference)
create_mobile_simple_table(df)

# Summary with drill-down (for larger datasets)
create_mobile_summary_with_drilldown(df)
```

## Solution 1: Card-Based List View

**Best for:** Small to medium lists (10-50 items)

**Features:**
- Expandable cards with key metrics
- Touch-friendly (large tap targets)
- Pagination with "Load More"
- Action buttons (Contact, Details)
- Visual status indicators

**Usage:**
```python
df = pd.DataFrame({
    'member_name': ['John Doe', 'Jane Smith'],
    'measure_name': ['HbA1c Testing', 'Blood Pressure Control'],
    'member_id': ['M12345678', 'M12345679'],
    'predicted_closure_probability': [0.93, 0.88],
    'financial_value': [1500, 2000],
    'gap_status': ['Open', 'Pending'],
    'priority_score': [85, 72]
})

create_mobile_member_cards(df, limit=10)
```

**Parameters:**
- `df`: Member DataFrame
- `limit`: Initial number of cards (default: 10)
- Column name parameters (customizable)

**Pagination:**
- Shows top N cards initially
- "Load More" button loads 10 more
- "Reset" button returns to top 10

## Solution 2: Simplified Table (3 Columns)

**Best for:** Quick reference lookups

**Features:**
- Only 3 essential columns
- Status with emoji indicators
- Sorted by priority
- Export functionality
- Fixed height (400px)

**Usage:**
```python
create_mobile_simple_table(df)
```

**Columns Shown:**
1. Member/Measure Name (abbreviated if >30 chars)
2. Status (with emoji: 🔴 🟡 ✅ ⚪)
3. Priority Score (number)

**Customization:**
- Automatically abbreviates long names
- Color-coded status
- Sortable by priority

## Solution 3: Summary with Drill-Down

**Best for:** Large datasets (100+ items)

**Features:**
- Aggregated summary by measure
- Select measure to drill down
- Shows member cards for selected measure
- Efficient for large datasets

**Usage:**
```python
create_mobile_summary_with_drilldown(df, limit=5)
```

**Summary Columns:**
- Measure Name
- Member Count
- Total Value ($)
- Average Closure Rate (%)

**Drill-Down:**
- Select measure from dropdown
- Shows member cards for that measure
- Limited to top N members (default: 5)

## Solution 4: Swipeable Cards (HTML/CSS)

**Best for:** Visual card-based browsing

**Features:**
- Custom HTML/CSS styling
- Touch-optimized cards
- Visual hierarchy
- Priority badges
- Smooth interactions

**Usage:**
```python
current_limit = create_swipeable_member_cards(df, limit=10)
```

**Card Contents:**
- Member name (large, bold)
- Measure name (subtitle)
- Status emoji (large)
- Closure rate (metric)
- Financial value (metric)
- Priority badge (color-coded)
- Member ID

**Styling:**
- White cards with shadow
- Rounded corners (12px)
- Grid layout for metrics
- Color-coded priority badges

## Choosing the Right Solution

### Small Lists (≤20 items)
✅ **Use:** Card-based view
- Best user experience
- All details visible
- Easy navigation

### Medium Lists (21-100 items)
✅ **Use:** Summary with drill-down
- Efficient navigation
- Quick overview first
- Details on demand

### Large Lists (101-500 items)
✅ **Use:** Simplified table
- Quick scanning
- Essential info only
- Export for details

### Very Large Lists (500+ items)
✅ **Use:** Summary view only
- Too large for mobile detail
- Focus on aggregated insights
- Use desktop for details

## Mobile Table Best Practices

### 1. Limit Data Shown

```python
# ✅ Good: Show top 10-20
create_mobile_member_cards(df.head(20), limit=10)

# ❌ Bad: Show all data
create_mobile_member_cards(df, limit=1000)
```

### 2. Use Pagination

```python
# ✅ Good: Load more on demand
create_mobile_member_cards(df, limit=10)  # Shows "Load More" button

# ❌ Bad: Load all at once
create_mobile_member_cards(df, limit=len(df))
```

### 3. Abbreviate Long Text

```python
# ✅ Good: Automatic abbreviation
# Function automatically shortens names >25-30 chars

# ❌ Bad: Long names break layout
```

### 4. Use Icons/Emojis

```python
# ✅ Good: Visual status indicators
# 🔴 Open, 🟡 Pending, ✅ Closed

# ❌ Bad: Text-only status
```

### 5. Stack Vertically

```python
# ✅ Good: Single column layout
# All solutions use vertical stacking

# ❌ Bad: Multi-column on mobile
```

## Performance Optimization

### Initial Render

- Limit to 10-20 items initially
- Use caching for data loading
- Lazy load details on expand

### Load More

- Load 10 items at a time
- Update session state
- Smooth scrolling

### Data Size Limits

- Cards: Max 50 items loaded
- Table: Max 100 rows
- Summary: Unlimited (aggregated)

## Touch Optimization

### Touch Targets

- Cards: Full card is tappable
- Buttons: 48px minimum height
- Expandable: Large header area

### Gestures

- Tap: Expand card / Show details
- Scroll: Navigate list
- Long press: (Future: Context menu)

## Common Patterns

### Pattern 1: Member Lookup

```python
# Quick member ID lookup
st.text_input("Search Member ID:")
# Show simplified table with results
create_mobile_simple_table(filtered_df)
```

### Pattern 2: Measure Overview

```python
# Show summary, drill down to members
create_mobile_summary_with_drilldown(df)
```

### Pattern 3: Priority List

```python
# Show top priority members as cards
priority_df = df.nlargest(20, 'priority_score')
create_mobile_member_cards(priority_df, limit=10)
```

## Integration with Mobile View

The mobile tables are integrated into `mobile_view.py`:

```python
# In mobile view
if view == "👥 Members":
    # Use card-based view
    create_mobile_member_cards(df, limit=10)
```

## Troubleshooting

### Cards Not Showing

- Check DataFrame is not empty
- Verify column names match parameters
- Check session state for pagination

### Performance Issues

- Reduce `limit` parameter
- Use summary view for large datasets
- Enable caching for data loading

### Text Too Small

- Cards use large, readable fonts
- Tables use 12px minimum
- Abbreviation prevents overflow

### Touch Not Working

- Ensure full-width buttons
- Check card expander is working
- Verify no overlapping elements

## Examples

See `mobile_tables.py` for complete examples and `mobile_view.py` for integration patterns.

---

## Support

For questions or issues:
- 📧 **Email**: reichert.starguardai@gmail.com
- 🔗 **LinkedIn**: [sentinel-analytics](https://www.linkedin.com/in/sentinel-analytics/)
- 💻 **GitHub**: [HEDIS-MA-Top-12-w-HEI-Prep](https://github.com/StarGuardAi/HEDIS-MA-Top-12-w-HEI-Prep/blob/main/README.md)
- 🎨 **Portfolio**: [Canva Portfolio](https://www.canva.com/design/DAG2WzhiLwM/N_iXUe3eEKL3dzQ2M_0PgQ/edit)

---

**Mobile Tables** | Touch-optimized | Card-based | Fast loading 📱

