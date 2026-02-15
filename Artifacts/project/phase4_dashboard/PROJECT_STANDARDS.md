# HEDIS Portfolio Optimizer - Project Standards

## 📋 Table of Contents
1. [Metric Display Standards](#metric-display-standards)
2. [Code Style Guidelines](#code-style-guidelines)
3. [UI/UX Standards](#uiux-standards)

---

## 🎯 Metric Display Standards

### RULE: All Metrics Must Use `centered_metric()` Function

**Status:** ✅ **MANDATORY** - All metrics across all pages must use this function.

### Why This Rule Exists

Streamlit's native `st.metric()` component cannot be reliably centered via CSS due to deeply nested DOM structures. The custom `centered_metric()` function guarantees perfect centering through:
- Custom HTML with inline styles
- CSS class with `!important` flags
- JavaScript runtime enforcement

### Implementation

**Location:** `utils/page_components.py`

**Function Signature:**
```python
def centered_metric(label, value, delta=None, delta_color="normal", help_text=None):
    """
    Custom metric display with GUARANTEED centered alignment.
    Replaces st.metric() which cannot be reliably centered via CSS.
    
    Args:
        label: The metric label (e.g., "Potential ROI")
        value: The metric value (e.g., "33%")
        delta: Optional delta text (e.g., "+$1,264,020 annually")
        delta_color: "normal" (green for positive), "inverse" (red for positive), or "off" (gray)
        help_text: Optional tooltip text
    """
```

### Usage Example

**❌ WRONG - Do NOT use:**
```python
with col1:
    st.metric(
        label="Potential ROI",
        value="33%",
        delta="+$1,264,020 annually"
    )
```

**✅ CORRECT - Always use:**
```python
from utils.page_components import centered_metric

with col1:
    centered_metric(
        label="Potential ROI",
        value="33%",
        delta="+$1,264,020 annually",
        help_text="Projected return on investment"
    )
```

### Requirements

1. **All new metrics** must use `centered_metric()`
2. **All existing `st.metric()` calls** must be replaced with `centered_metric()`
3. **Import statement** must be added to page files:
   ```python
   from utils.page_components import centered_metric
   ```

### Visual Standard

All metrics must display with:
- ✅ Label centered above value
- ✅ Value centered (large, bold)
- ✅ Delta centered below value (if provided)
- ✅ Help icon (ⓘ) appears next to label when `help_text` is provided

### Files Affected

- ✅ `app.py` - Home page (Portfolio Performance Overview)
- ✅ All page files in `pages/` directory
- ✅ Any utility functions that display metrics

---

## 📐 Code Style Guidelines

### Import Order

1. Standard library imports
2. Third-party imports (Streamlit, pandas, etc.)
3. Local utility imports (`from utils.page_components import ...`)

### Metric Display Pattern

Always follow this pattern for metric displays:

```python
# Create columns
col1, col2, col3, col4 = st.columns(4, gap="small")

# Display metrics
with col1:
    centered_metric(
        label="Metric Name",
        value=f"{calculated_value}",
        delta="Optional delta text",
        help_text="Optional tooltip"
    )
```

---

## 🎨 UI/UX Standards

### Metric Layout

- **First Row (Primary KPIs):** 4 columns, larger values (2rem font)
- **Second Row (Supporting Metrics):** 5 columns, standard values
- **Spacing:** Use `gap="small"` for column spacing
- **Alignment:** All metrics MUST be centered (enforced by `centered_metric()`)

### Color Standards

- **Delta Colors:**
  - Green (`#10b981`) for positive changes (default)
  - Red (`#ef4444`) for negative changes
  - Gray (`#6b7280`) for neutral/off state

### Typography

- **Label:** 0.875rem, gray (#6b7280), medium weight (500)
- **Value:** 2rem, dark gray (#1f2937), bold (700)
- **Delta:** 0.85rem, colored based on direction

---

## 🔄 Migration Checklist

When updating existing pages:

- [ ] Import `centered_metric` from `utils.page_components`
- [ ] Replace all `st.metric()` calls with `centered_metric()`
- [ ] Update parameter names: `label` (not `label=`), `value` (not `value=`), `delta` (not `delta=`), `help_text` (not `help=`)
- [ ] Verify metrics are centered after changes
- [ ] Test on mobile viewport (metrics should stack and remain centered)

---

## 📝 Notes

- The `centered_metric()` function uses a triple-layer approach:
  1. CSS class with `!important` flags
  2. Inline HTML styles
  3. JavaScript runtime enforcement
  
- This ensures centering works even if Streamlit rerenders content

- The function is backward-compatible with `st.metric()` parameters (except `help` → `help_text`)

---

**Last Updated:** 2025-01-20  
**Version:** 1.0  
**Status:** Active Standard


