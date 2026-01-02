# Spacing Fix Quick Reference

## Exact Spacing Values from Home Page (app.py)

Use these values to update Alert Center and ROI Calculator pages.

---

## 1. Container Padding

### Desktop (Add Media Query)

```css
@media (min-width: 769px) {
    .main .block-container {
        padding-top: 2.5rem !important;
        padding-bottom: 2rem !important;
        padding-left: 4rem !important;
        padding-right: 4rem !important;
        max-width: 1600px !important;
        margin: 0 auto !important;
    }
}
```

### Base (Mobile-First)

```css
.main .block-container { 
    padding-top: 2.5rem !important;  /* Changed from 1rem */
    padding-bottom: 1rem !important; 
    padding-left: 1rem !important; 
    padding-right: 1rem !important; 
    max-width: 100% !important; 
}
```

**Location in Alert/ROI pages:** Lines 233-239 (Alert), 236-242 (ROI)

---

## 2. Element Container Spacing

### Base (Mobile-First)

```css
.element-container { margin-bottom: 0.2rem !important; }  /* Changed from 0.4rem */
.stMarkdown { margin-bottom: 0.2rem !important; }  /* Changed from 0.4rem */
div[data-testid="stVerticalBlock"] > div { gap: 0.2rem !important; }  /* Changed from 0.4rem */
```

### Desktop (Add Media Query)

```css
@media (min-width: 769px) {
    .element-container {
        margin-bottom: 1rem !important;
        padding: 1rem !important;
    }
}
```

**Location in Alert/ROI pages:** Lines 264-265, 305 (Alert), 267-268, 308 (ROI)

---

## 3. Header Spacing

### Base (Mobile-First) - Already Correct

```css
h1 { 
    font-size: 1.8rem !important; 
    margin-top: 0.8rem !important; 
    margin-bottom: 0.5rem !important; 
    line-height: 1.2 !important; 
}

h2 { 
    font-size: 1.4rem !important; 
    margin-top: 0.6rem !important; 
    margin-bottom: 0.4rem !important; 
    line-height: 1.2 !important; 
}

h3 { 
    font-size: 1.1rem !important; 
    margin-top: 0.5rem !important; 
    margin-bottom: 0.3rem !important; 
    line-height: 1.2 !important; 
}
```

### Desktop (ADD THIS - Currently Missing)

```css
@media (min-width: 769px) {
    h1 {
        font-size: 2.5rem !important;
        margin-top: 1rem !important;
        margin-bottom: 1rem !important;
        font-weight: 700 !important;
    }
    
    h2 {
        font-size: 1.75rem !important;
        margin-top: 1.5rem !important;
        margin-bottom: 0.75rem !important;
        font-weight: 600 !important;
    }
    
    h3 {
        font-size: 1.35rem !important;
        margin-top: 1.25rem !important;
        margin-bottom: 0.5rem !important;
        font-weight: 600 !important;
    }
}
```

**Location in Alert/ROI pages:** Add after mobile media query (after line 447 in Alert, after line 450 in ROI)

---

## 4. Horizontal Rule Spacing

### Change This:

```css
hr { margin: 0.6rem 0 !important; }  /* OLD */
```

### To This:

```css
hr { margin: 0.3rem 0 !important; }  /* NEW - Match Home page */
```

**Location in Alert/ROI pages:** Line 308 (Alert), Line 311 (ROI)

---

## 5. Mobile Spacing

### ✅ NO CHANGES NEEDED

Mobile spacing already matches Home page:
- `padding-top: 2rem`
- `padding-left/right: 1rem`
- Header margins match

---

## Complete CSS Block to Add/Update

### For Alert Center (pages/9_🔔_Alert_Center.py)

**Replace lines 233-239:**
```css
.main .block-container { 
    padding-top: 2.5rem !important;  /* Changed from 1rem */
    padding-bottom: 1rem !important; 
    padding-left: 1rem !important; 
    padding-right: 1rem !important; 
    max-width: 100% !important; 
}
```

**Replace lines 264-265:**
```css
.element-container { margin-bottom: 0.2rem !important; }  /* Changed from 0.4rem */
.stMarkdown { margin-bottom: 0.2rem !important; }  /* Changed from 0.4rem */
```

**Replace line 305:**
```css
div[data-testid="stVerticalBlock"] > div { gap: 0.2rem !important; }  /* Changed from 0.4rem */
```

**Replace line 308:**
```css
hr { margin: 0.3rem 0 !important; }  /* Changed from 0.6rem */
```

**Add after line 447 (after mobile media query closes):**
```css
/* ========== DESKTOP ENHANCEMENTS (769px+) ========== */
@media (min-width: 769px) {
    .main .block-container {
        padding-top: 2.5rem !important;
        padding-bottom: 2rem !important;
        padding-left: 4rem !important;
        padding-right: 4rem !important;
        max-width: 1600px !important;
        margin: 0 auto !important;
    }
    
    h1 {
        font-size: 2.5rem !important;
        margin-top: 1rem !important;
        margin-bottom: 1rem !important;
        font-weight: 700 !important;
    }
    
    h2 {
        font-size: 1.75rem !important;
        margin-top: 1.5rem !important;
        margin-bottom: 0.75rem !important;
        font-weight: 600 !important;
    }
    
    h3 {
        font-size: 1.35rem !important;
        margin-top: 1.25rem !important;
        margin-bottom: 0.5rem !important;
        font-weight: 600 !important;
    }
    
    .element-container {
        margin-bottom: 1rem !important;
        padding: 1rem !important;
    }
}
```

### For ROI Calculator (pages/11_💰_ROI_Calculator.py)

**Replace lines 236-242:**
```css
.main .block-container { 
    padding-top: 2.5rem !important;  /* Changed from 1rem */
    padding-bottom: 1rem !important; 
    padding-left: 1rem !important; 
    padding-right: 1rem !important; 
    max-width: 100% !important; 
}
```

**Replace lines 267-268:**
```css
.element-container { margin-bottom: 0.2rem !important; }  /* Changed from 0.4rem */
.stMarkdown { margin-bottom: 0.2rem !important; }  /* Changed from 0.4rem */
```

**Replace line 308:**
```css
div[data-testid="stVerticalBlock"] > div { gap: 0.2rem !important; }  /* Changed from 0.4rem */
```

**Replace line 311:**
```css
hr { margin: 0.3rem 0 !important; }  /* Changed from 0.6rem */
```

**Add after line 450 (after mobile media query closes):**
```css
/* ========== DESKTOP ENHANCEMENTS (769px+) ========== */
@media (min-width: 769px) {
    .main .block-container {
        padding-top: 2.5rem !important;
        padding-bottom: 2rem !important;
        padding-left: 4rem !important;
        padding-right: 4rem !important;
        max-width: 1600px !important;
        margin: 0 auto !important;
    }
    
    h1 {
        font-size: 2.5rem !important;
        margin-top: 1rem !important;
        margin-bottom: 1rem !important;
        font-weight: 700 !important;
    }
    
    h2 {
        font-size: 1.75rem !important;
        margin-top: 1.5rem !important;
        margin-bottom: 0.75rem !important;
        font-weight: 600 !important;
    }
    
    h3 {
        font-size: 1.35rem !important;
        margin-top: 1.25rem !important;
        margin-bottom: 0.5rem !important;
        font-weight: 600 !important;
    }
    
    .element-container {
        margin-bottom: 1rem !important;
        padding: 1rem !important;
    }
}
```

---

## Summary Table

| Element | Home Page Value | Alert/ROI Current | Change Required |
|---------|----------------|-------------------|-----------------|
| **Desktop container padding-top** | `2.5rem` | `1rem` | ✅ Change to `2.5rem` |
| **Desktop container padding-left/right** | `4rem` | `1rem` | ✅ Add media query with `4rem` |
| **Desktop container padding-bottom** | `2rem` | `1rem` | ✅ Add media query with `2rem` |
| **Desktop container max-width** | `1600px` | `100%` | ✅ Add media query with `1600px` |
| **element-container margin-bottom** | `0.2rem` (base) / `1rem` (desktop) | `0.4rem` | ✅ Change to `0.2rem` + add desktop `1rem` |
| **stMarkdown margin-bottom** | `0.2rem` | `0.4rem` | ✅ Change to `0.2rem` |
| **stVerticalBlock gap** | `0.2rem` | `0.4rem` | ✅ Change to `0.2rem` |
| **hr margin** | `0.3rem 0` | `0.6rem 0` | ✅ Change to `0.3rem 0` |
| **Desktop h1 margin-top** | `1rem` | N/A (uses `0.8rem`) | ✅ Add desktop media query |
| **Desktop h1 margin-bottom** | `1rem` | N/A (uses `0.5rem`) | ✅ Add desktop media query |
| **Desktop h2 margin-top** | `1.5rem` | N/A (uses `0.6rem`) | ✅ Add desktop media query |
| **Desktop h2 margin-bottom** | `0.75rem` | N/A (uses `0.4rem`) | ✅ Add desktop media query |
| **Desktop h3 margin-top** | `1.25rem` | N/A (uses `0.5rem`) | ✅ Add desktop media query |
| **Desktop h3 margin-bottom** | `0.5rem` | N/A (uses `0.3rem`) | ✅ Add desktop media query |

---

## Quick Copy-Paste Values

### Container Padding
- Base: `padding-top: 2.5rem` (change from `1rem`)
- Desktop: `padding-top: 2.5rem`, `padding-left/right: 4rem`, `padding-bottom: 2rem`, `max-width: 1600px`

### Element Spacing
- Base: `margin-bottom: 0.2rem` (change from `0.4rem`)
- Desktop: `margin-bottom: 1rem`, `padding: 1rem`

### Header Spacing
- Base: Already correct
- Desktop: Add media query with larger margins and font sizes

### Separators
- `hr { margin: 0.3rem 0 }` (change from `0.6rem 0`)

---

## Files to Update

1. ✅ `pages/9_🔔_Alert_Center.py`
2. ✅ `pages/11_💰_ROI_Calculator.py`

## Testing

After applying fixes:
- [ ] Desktop view: Container padding matches Home page
- [ ] Desktop view: Headers have proper spacing
- [ ] Desktop view: Elements have consistent spacing
- [ ] Desktop view: Separators use correct spacing
- [ ] Mobile view: No changes (already matches)
- [ ] Visual comparison: Pages look consistent




