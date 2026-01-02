# Streamlit Spacing Standards

**Version:** 1.0  
**Based on:** Home page (`app.py`)  
**Applies to:** All 21 pages in the HEDIS Portfolio Dashboard

---

## Table of Contents

1. [Overview](#overview)
2. [Quick Start](#quick-start)
3. [Spacing Values Reference](#spacing-values-reference)
4. [CSS Implementation](#css-implementation)
5. [Code Examples](#code-examples)
6. [Before/After Comparisons](#beforeafter-comparisons)
7. [Mobile Spacing Best Practices](#mobile-spacing-best-practices)
8. [Migration Guide](#migration-guide)
9. [Troubleshooting](#troubleshooting)

---

## Overview

This document defines the standard spacing system extracted from the Home page (`app.py`) to ensure consistent vertical spacing across all 21 pages in the Streamlit application.

### Key Principles

1. **Mobile-First Design**: Base styles optimized for mobile, enhanced for desktop
2. **Consistent Spacing**: All pages use identical spacing values
3. **Reduced White Space**: Tight spacing eliminates excessive gaps
4. **Responsive Breakpoints**: 
   - Mobile: `max-width: 768px`
   - Desktop: `min-width: 769px`
   - Large Desktop: `min-width: 1025px`

### Benefits

- ✅ Consistent visual appearance across all pages
- ✅ Reduced vertical white space by ~50%
- ✅ Proper desktop enhancements
- ✅ Mobile-optimized spacing
- ✅ Reusable CSS system

---

## Quick Start

### Option 1: Use Utility Function (Recommended)

```python
import streamlit as st
from utils.spacing_standards import apply_spacing_standards

# Apply standard spacing
apply_spacing_standards()
```

### Option 2: Import CSS Directly

```python
import streamlit as st
from utils.spacing_standards import get_spacing_css

# Apply standard spacing
st.markdown(get_spacing_css(), unsafe_allow_html=True)
```

### Option 3: Copy CSS Block

Copy the CSS from `utils/spacing_standards.py` and paste into your page:

```python
st.markdown("""
<style>
/* ... CSS from spacing_standards.py ... */
</style>
""", unsafe_allow_html=True)
```

---

## Spacing Values Reference

### Container Padding

| Breakpoint | Top | Bottom | Left/Right | Max Width |
|------------|-----|--------|------------|-----------|
| **Mobile** | `2.5rem` | `1rem` | `1rem` | `100%` |
| **Desktop (769px+)** | `2.5rem` | `2rem` | `4rem` | `1600px` |
| **Large Desktop (1025px+)** | `2.5rem` | `2rem` | `5rem` | `1800px` |

### Header Spacing

#### Mobile (Base)

| Element | Font Size | Margin Top | Margin Bottom |
|---------|-----------|------------|---------------|
| **h1** | `1.8rem` | `0.8rem` | `0.5rem` |
| **h2** | `1.4rem` | `0.6rem` | `0.4rem` |
| **h3** | `1.1rem` | `0.5rem` | `0.3rem` |

#### Desktop (769px+)

| Element | Font Size | Margin Top | Margin Bottom | Font Weight |
|---------|-----------|------------|---------------|-------------|
| **h1** | `2.5rem` | `1rem` | `1rem` | `700` |
| **h2** | `1.75rem` | `1.5rem` | `0.75rem` | `600` |
| **h3** | `1.35rem` | `1.25rem` | `0.5rem` | `600` |

#### Large Desktop (1025px+)

| Element | Font Size |
|---------|-----------|
| **h1** | `2.75rem` |
| **h2** | `2rem` |

### Element Spacing

| Element | Mobile | Desktop (769px+) |
|---------|--------|------------------|
| **Element Container** | `margin-bottom: 0.2rem` | `margin-bottom: 1rem`, `padding: 1rem` |
| **stMarkdown** | `margin-bottom: 0.2rem` | `margin-bottom: 0.75rem` |
| **Vertical Block Gap** | `gap: 0.2rem` | `gap: 0.75rem` |
| **Column Padding** | `padding: 0.2rem` | `padding: 0.75rem` |
| **HR Margin** | `margin: 0.3rem 0` | `margin: 1rem 0` |

### Chart & Data Spacing

| Element | Mobile | Desktop (769px+) |
|---------|--------|------------------|
| **Plotly Chart** | `margin-bottom: 0.3rem` | `margin: 1rem 0` |
| **DataFrame** | `margin-bottom: 0.3rem` | `margin: 1rem 0` |

### Interactive Elements

| Element | Mobile | Desktop (769px+) |
|---------|--------|------------------|
| **Expander** | `margin: 0` | `margin-bottom: 1rem` |
| **Tabs** | `margin-bottom: 0.3rem` | `margin-bottom: 1rem` |
| **Tab Gap** | `gap: 0.2rem` | N/A |
| **Tab Padding** | `padding: 0.4rem 0.8rem` | N/A |
| **Button Padding** | `padding: 0.5rem 1rem` | `padding: 0.7rem 1.5rem` |
| **Form Input Margin** | `margin-bottom: 0.2rem` | `margin-bottom: 1rem` |
| **Alert Padding** | `padding: 0.5rem` | `padding: 1rem` |
| **Alert Margin** | `margin-bottom: 0.3rem` | `margin-bottom: 1rem` |

### Metric Spacing

| Element | Mobile | Desktop (769px+) |
|---------|--------|------------------|
| **Metric Value Font** | `1.6rem` | `2.5rem`, `font-weight: 700` |
| **Metric Label Font** | `0.95rem` | `1rem`, `font-weight: 500` |
| **Metric Container Padding** | `0.5rem` | `1rem` |

---

## CSS Implementation

### Complete CSS Block

The complete CSS block is available in `utils/spacing_standards.py`. Key sections:

1. **Base Container** (Mobile-First)
2. **Header Spacing** (h1, h2, h3)
3. **Element Spacing** (containers, markdown, vertical blocks)
4. **Chart & Data Spacing**
5. **Interactive Elements** (expanders, tabs, buttons, inputs)
6. **Desktop Enhancements** (769px+)
7. **Large Desktop** (1025px+)
8. **Mobile Adjustments** (max-width: 768px)

### Breakpoint Strategy

```css
/* Mobile-First Base Styles */
/* ... base styles ... */

/* Desktop Enhancements */
@media (min-width: 769px) {
    /* ... desktop styles ... */
}

/* Large Desktop */
@media (min-width: 1025px) {
    /* ... large desktop styles ... */
}

/* Mobile Adjustments */
@media (max-width: 768px) {
    /* ... mobile-specific overrides ... */
}
```

---

## Code Examples

### Example 1: Basic Page Setup

```python
import streamlit as st
from utils.spacing_standards import apply_spacing_standards

st.set_page_config(
    page_title="My Page",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="auto"
)

# Apply standard spacing
apply_spacing_standards()

# Your page content
st.title("My Page Title")
st.markdown("Page description")
```

### Example 2: Section with Proper Spacing

```python
import streamlit as st
from utils.spacing_standards import apply_spacing_standards

apply_spacing_standards()

# Section 1
st.header("Section 1")
st.markdown("Content for section 1")
st.plotly_chart(fig1)

# Separator
st.markdown("---")

# Section 2
st.header("Section 2")
st.markdown("Content for section 2")
st.dataframe(df)
```

### Example 3: Form Inputs with Results

```python
import streamlit as st
from utils.spacing_standards import apply_spacing_standards

apply_spacing_standards()

# Input form
with st.form("calculator"):
    value1 = st.number_input("Value 1", value=0)
    value2 = st.number_input("Value 2", value=0)
    submitted = st.form_submit_button("Calculate")
    
    if submitted:
        result = value1 + value2
        st.metric("Result", result)
```

### Example 4: Metrics Display

```python
import streamlit as st
from utils.spacing_standards import apply_spacing_standards

apply_spacing_standards()

# Metrics row
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Metric 1", "100", "5%")
with col2:
    st.metric("Metric 2", "200", "-2%")
with col3:
    st.metric("Metric 3", "300", "10%")
```

### Example 5: Tabs with Content

```python
import streamlit as st
from utils.spacing_standards import apply_spacing_standards

apply_spacing_standards()

tab1, tab2, tab3 = st.tabs(["Tab 1", "Tab 2", "Tab 3"])

with tab1:
    st.header("Tab 1 Content")
    st.plotly_chart(fig1)

with tab2:
    st.header("Tab 2 Content")
    st.dataframe(df)

with tab3:
    st.header("Tab 3 Content")
    st.markdown("Content here")
```

---

## Before/After Comparisons

### Container Padding

**Before:**
```css
.main .block-container { 
    padding-top: 1rem !important;  /* Too small */
    padding-left: 1rem !important;
    padding-right: 1rem !important;
}
```

**After:**
```css
.main .block-container { 
    padding-top: 2.5rem !important;  /* ✅ Standard */
    padding-left: 1rem !important;
    padding-right: 1rem !important;
}

@media (min-width: 769px) {
    .main .block-container {
        padding-left: 4rem !important;  /* ✅ Desktop standard */
        padding-right: 4rem !important;
        max-width: 1600px !important;
    }
}
```

### Element Spacing

**Before:**
```css
.element-container { margin-bottom: 0.4rem !important; }  /* Too much */
.stMarkdown { margin-bottom: 0.4rem !important; }
div[data-testid="stVerticalBlock"] > div { gap: 0.4rem !important; }
```

**After:**
```css
.element-container { margin-bottom: 0.2rem !important; }  /* ✅ Standard */
.stMarkdown { margin-bottom: 0.2rem !important; }
div[data-testid="stVerticalBlock"] > div { gap: 0.2rem !important; }

@media (min-width: 769px) {
    .element-container {
        margin-bottom: 1rem !important;
        padding: 1rem !important;
    }
}
```

### Header Spacing

**Before:**
```css
h1 { 
    font-size: 1.8rem !important; 
    margin-top: 0.8rem !important; 
    margin-bottom: 0.5rem !important; 
}
/* No desktop enhancement */
```

**After:**
```css
h1 { 
    font-size: 1.8rem !important; 
    margin-top: 0.8rem !important; 
    margin-bottom: 0.5rem !important; 
}

@media (min-width: 769px) {
    h1 {
        font-size: 2.5rem !important;  /* ✅ Desktop standard */
        margin-top: 1rem !important;
        margin-bottom: 1rem !important;
        font-weight: 700 !important;
    }
}
```

### Separator Spacing

**Before:**
```css
hr { margin: 0.6rem 0 !important; }  /* Too much */
```

**After:**
```css
hr { margin: 0.3rem 0 !important; }  /* ✅ Standard */

@media (min-width: 769px) {
    hr {
        margin: 1rem 0 !important;  /* ✅ Desktop standard */
    }
}
```

---

## Mobile Spacing Best Practices

### 1. Use Mobile-First Approach

Always start with mobile spacing, then enhance for desktop:

```python
# ✅ Good: Mobile-first
apply_spacing_standards()  # Includes mobile base + desktop enhancements

# ❌ Bad: Desktop-first
# Don't create desktop-only styles without mobile base
```

### 2. Avoid Excessive Padding

**❌ Bad:**
```python
st.markdown('<style>div.block-container{padding-top:3rem!important}</style>', unsafe_allow_html=True)
```

**✅ Good:**
```python
apply_spacing_standards()  # Uses standard 2.5rem
```

### 3. Use Standard Separators

**❌ Bad:**
```python
st.markdown("")  # Empty markdown for spacing
st.markdown("")  # Multiple empty lines
```

**✅ Good:**
```python
st.markdown("---")  # Standard separator with proper spacing
```

### 4. Consistent Form Spacing

**❌ Bad:**
```python
st.number_input("Value 1")
st.markdown("")  # Manual spacing
st.number_input("Value 2")
```

**✅ Good:**
```python
apply_spacing_standards()  # Automatic spacing
st.number_input("Value 1")
st.number_input("Value 2")
```

### 5. Proper Section Flow

**❌ Bad:**
```python
st.header("Section 1")
st.plotly_chart(fig1)
st.markdown("")  # Manual spacing
st.markdown("")  # More manual spacing
st.header("Section 2")
```

**✅ Good:**
```python
apply_spacing_standards()  # Automatic spacing
st.header("Section 1")
st.plotly_chart(fig1)
st.markdown("---")  # Standard separator
st.header("Section 2")
```

### 6. Mobile-Specific Adjustments

The standard CSS includes mobile adjustments. Don't override unless necessary:

```css
/* ✅ Already handled in standard CSS */
@media (max-width: 768px) {
    .main .block-container { 
        padding-top: 2rem !important;
    }
    h1 { font-size: 1.5rem !important; }
}
```

---

## Migration Guide

### Step 1: Remove Old Spacing CSS

**Find and remove:**
- Inline spacing fixes: `st.markdown('<style>div.block-container{padding-top:1rem!important}</style>')`
- Old container padding values
- Inconsistent element spacing
- Missing desktop media queries

### Step 2: Add Standard Spacing

**Add at the top of your page (after imports, before content):**

```python
from utils.spacing_standards import apply_spacing_standards

# ... other imports ...

apply_spacing_standards()
```

### Step 3: Remove Redundant Spacing

**Remove:**
- Multiple `st.markdown("")` blank lines
- Manual spacing CSS that conflicts with standards
- Inconsistent padding/margin values

### Step 4: Test

**Verify:**
- [ ] Container padding matches Home page
- [ ] Headers have proper spacing
- [ ] Elements have consistent spacing
- [ ] Desktop view has proper enhancements
- [ ] Mobile view matches Home page
- [ ] No excessive white space

### Step 5: Update Custom Cards/Containers

**If you have custom CSS classes:**

```python
# Update custom card spacing to match standards
st.markdown("""
<style>
.custom-card {
    padding: 1rem;  /* Match standard element padding */
    margin-bottom: 0.5rem;  /* Match standard card margin */
}
</style>
""", unsafe_allow_html=True)
```

---

## Troubleshooting

### Issue: Spacing Not Applied

**Problem:** `apply_spacing_standards()` not working

**Solution:**
1. Check import: `from utils.spacing_standards import apply_spacing_standards`
2. Ensure it's called before any content
3. Check for conflicting CSS that uses `!important`

### Issue: Desktop Spacing Too Large

**Problem:** Desktop spacing seems excessive

**Solution:**
- This is intentional - desktop uses more generous spacing
- Verify breakpoint: `@media (min-width: 769px)`
- Check if mobile styles are being overridden

### Issue: Mobile Spacing Too Tight

**Problem:** Mobile spacing seems too tight

**Solution:**
- Mobile spacing is intentionally tight to reduce white space
- Verify mobile breakpoint: `@media (max-width: 768px)`
- Check if custom CSS is overriding standards

### Issue: Inconsistent Spacing Between Pages

**Problem:** Some pages have different spacing

**Solution:**
1. Ensure all pages use `apply_spacing_standards()`
2. Remove any custom spacing CSS
3. Check for conflicting inline styles

### Issue: Form Inputs Too Close Together

**Problem:** Form inputs appear cramped

**Solution:**
- Mobile: `0.2rem` margin is intentional (tight spacing)
- Desktop: `1rem` margin provides proper separation
- Verify desktop breakpoint is working

### Issue: Headers Not Spacing Correctly

**Problem:** Headers have wrong spacing

**Solution:**
1. Check if custom header CSS exists
2. Verify desktop media query is applied
3. Ensure header tags (h1, h2, h3) are used correctly

---

## Quick Reference

### Import Statement
```python
from utils.spacing_standards import apply_spacing_standards
```

### Apply to Page
```python
apply_spacing_standards()
```

### Spacing Values (Programmatic)
```python
from utils.spacing_standards import SPACING_VALUES

mobile_padding = SPACING_VALUES['mobile']['container_padding_top']
desktop_padding = SPACING_VALUES['desktop']['container_padding_sides']
```

### Files to Update

All pages in `pages/` directory:
- `1_📊_ROI_by_Measure.py`
- `2_💰_Cost_Per_Closure.py`
- `3_📈_Monthly_Trend.py`
- `4_💵_Budget_Variance.py`
- `5_🎯_Cost_Tier_Comparison.py`
- `6_🤖_AI_Executive_Insights.py`
- `7_📊_What-If_Scenario_Modeler.py`
- `8_📋_Campaign_Builder.py`
- `9_🔔_Alert_Center.py` ✅ (Already updated)
- `10_📈_Historical_Tracking.py`
- `11_💰_ROI_Calculator.py` ✅ (Already updated)
- `13_📋_Measure_Analysis.py`
- `14_⭐_Star_Rating_Simulator.py`
- `15_🔄_Gap_Closure_Workflow.py`
- `16_🤖_ML_Gap_Closure_Predictions.py`
- `17_📊_Competitive_Benchmarking.py`
- `18_📋_Compliance_Reporting.py`
- `18_🤖_Secure_AI_Chatbot.py`
- `19_⚖️_Health_Equity_Index.py`
- `z_Performance_Dashboard.py`

---

## Summary

The spacing standards system ensures:

1. ✅ **Consistency**: All pages use identical spacing values
2. ✅ **Reduced White Space**: ~50% reduction in vertical gaps
3. ✅ **Responsive Design**: Mobile-first with desktop enhancements
4. ✅ **Easy Implementation**: Single function call
5. ✅ **Maintainability**: Centralized CSS system

**Next Steps:**
1. Apply `apply_spacing_standards()` to all remaining pages
2. Remove old spacing CSS
3. Test on mobile and desktop
4. Verify consistency across all pages

---

**Document Version:** 1.0  
**Last Updated:** Based on Home page (`app.py`)  
**Maintained By:** Development Team




