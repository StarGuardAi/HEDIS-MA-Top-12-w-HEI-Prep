# Page Components Quick Start Guide

## ✅ Step 1: Import (Add at top of your page)

```python
from utils.page_components import apply_header_spacing, add_mobile_ready_badge, add_page_footer
```

## ✅ Step 2: Apply Header Spacing (After st.set_page_config)

```python
st.set_page_config(
    page_title="Your Page Title",
    page_icon="📊",
    layout="wide"
)
apply_header_spacing()  # ← ADD THIS LINE
```

## ✅ Step 3: Add Mobile Badge (In Sidebar)

```python
with st.sidebar:
    # ... your sidebar widgets ...
    add_mobile_ready_badge()  # ← ADD THIS LINE
```

## ✅ Step 4: Add Footer (At End of Page)

```python
# ... your page content ...

add_page_footer()  # ← ADD THIS LINE AT THE END
```

---

## 📋 Complete Example

```python
import streamlit as st
from utils.page_components import apply_header_spacing, add_mobile_ready_badge, add_page_footer

# Step 1: Page config
st.set_page_config(
    page_title="ROI Calculator",
    page_icon="💰",
    layout="wide"
)
apply_header_spacing()  # ← ADDED

# Step 2: Sidebar
with st.sidebar:
    st.title("Filters")
    # ... your filters ...
    add_mobile_ready_badge()  # ← ADDED

# Step 3: Main content
st.title("💰 ROI Calculator")
# ... your page content ...

# Step 4: Footer
add_page_footer()  # ← ADDED
```

---

## 🎯 What Each Function Does

### `apply_header_spacing()`
- Applies consistent spacing CSS for headers
- Optimizes padding for desktop and mobile
- Ensures consistent look across all pages
- **Call immediately after `st.set_page_config()`**

### `add_mobile_ready_badge()`
- Adds a "📱 Mobile Optimized" badge in sidebar
- Only visible on desktop (hidden on mobile)
- Indicates page is mobile-friendly
- **Call inside `with st.sidebar:` block**

### `add_page_footer()`
- Adds standardized footer with author and version
- Includes HIPAA compliance messaging
- Consistent branding across all pages
- **Call at the very end of your page**

---

## 📝 Notes

- All three functions are optional but recommended for consistency
- The footer uses default values (Robert Reichert, Version 4.0) but can be customized
- The mobile badge automatically hides on mobile devices
- Header spacing works with existing CSS in `app.py`

---

## 🔧 Customization

### Custom Footer

```python
add_page_footer(
    author="Your Name",
    version="5.0"
)
```

### Using Other Components

```python
from utils.page_components import (
    apply_header_spacing,
    add_mobile_ready_badge,
    add_page_footer,
    render_metric_grid,
    render_success_box
)

# Use other components as needed
render_metric_grid([
    {"label": "ROI", "value": "498%", "delta": "+$935K"}
])
```

