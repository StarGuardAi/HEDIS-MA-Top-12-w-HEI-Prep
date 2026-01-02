# Spacing Standards - Quick Reference

**One-page cheat sheet for applying spacing standards**

---

## Quick Import & Apply

```python
from utils.spacing_standards import apply_spacing_standards

# Add this after imports, before content
apply_spacing_standards()
```

---

## Spacing Values Cheat Sheet

### Container Padding
- **Mobile**: `2.5rem` top, `1rem` sides/bottom
- **Desktop**: `2.5rem` top, `4rem` sides, `2rem` bottom, `1600px` max-width
- **Large Desktop**: `5rem` sides, `1800px` max-width

### Headers
- **Mobile h1**: `1.8rem` font, `0.8rem/0.5rem` margins
- **Desktop h1**: `2.5rem` font, `1rem/1rem` margins, `700` weight
- **Mobile h2**: `1.4rem` font, `0.6rem/0.4rem` margins
- **Desktop h2**: `1.75rem` font, `1.5rem/0.75rem` margins, `600` weight

### Elements
- **Mobile**: `0.2rem` margin/gap
- **Desktop**: `1rem` margin, `1rem` padding

### Charts/Data
- **Mobile**: `0.3rem` margin-bottom
- **Desktop**: `1rem` margin top/bottom

### Separators
- **Mobile**: `0.3rem` margin
- **Desktop**: `1rem` margin

---

## Common Patterns

### Page Setup
```python
import streamlit as st
from utils.spacing_standards import apply_spacing_standards

st.set_page_config(page_title="Page", layout="wide")
apply_spacing_standards()  # Add this line
```

### Section Separator
```python
st.markdown("---")  # Standard separator (don't use empty markdown)
```

### Form Inputs
```python
apply_spacing_standards()  # Automatic spacing
st.number_input("Value 1")
st.number_input("Value 2")  # Proper spacing between inputs
```

### Metrics Row
```python
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Metric 1", "100")
with col2:
    st.metric("Metric 2", "200")
with col3:
    st.metric("Metric 3", "300")
```

---

## Migration Checklist

- [ ] Remove old spacing CSS
- [ ] Add `apply_spacing_standards()` import
- [ ] Call `apply_spacing_standards()` after imports
- [ ] Remove `st.markdown("")` blank lines
- [ ] Replace with `st.markdown("---")` for separators
- [ ] Test on mobile and desktop
- [ ] Verify consistency with Home page

---

## Don't Do This ❌

```python
# ❌ Don't add inline spacing fixes
st.markdown('<style>div.block-container{padding-top:1rem!important}</style>')

# ❌ Don't use empty markdown for spacing
st.markdown("")
st.markdown("")

# ❌ Don't override standard spacing
st.markdown('<style>.element-container{margin-bottom:0.5rem!important}</style>')
```

---

## Do This Instead ✅

```python
# ✅ Use standard spacing function
from utils.spacing_standards import apply_spacing_standards
apply_spacing_standards()

# ✅ Use standard separator
st.markdown("---")

# ✅ Let standards handle spacing automatically
st.header("Section")
st.plotly_chart(fig)
```

---

## Breakpoints

- **Mobile**: `max-width: 768px`
- **Desktop**: `min-width: 769px`
- **Large Desktop**: `min-width: 1025px`

---

## Files Already Updated ✅

- `pages/9_🔔_Alert_Center.py`
- `pages/11_💰_ROI_Calculator.py`

## Files Remaining

- All other pages in `pages/` directory (19 pages)

---

**Full Documentation:** See `SPACING_STANDARDS.md`




