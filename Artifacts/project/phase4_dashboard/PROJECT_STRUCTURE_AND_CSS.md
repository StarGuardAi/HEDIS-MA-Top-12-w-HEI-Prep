# HEDIS Portfolio Optimizer - Project Structure & CSS

## 📁 Main App File: `app.py`

**Location:** `Artifacts/project/phase4_dashboard/app.py`

**Key Structure:**
- **Lines 1-34:** Python 3.13 compatibility + imports + `st.set_page_config()`
- **Lines 36-621:** Main responsive CSS system (Desktop, Mobile, Tablet, Large Desktop)
- **Lines 623-629:** Responsive header HTML
- **Lines 631-626:** Additional spacing reduction CSS
- **Lines 636-747:** Purple sidebar theme CSS
- **Lines 749-900+:** Mobile detection JavaScript
- **Lines 1500-2700:** Sidebar configuration and filters
- **Lines 2750-4185:** Main content (Hero section, tabs, charts, etc.)

---

## 📂 Pages Directory Structure

```
Artifacts/project/phase4_dashboard/pages/
├── __init__.py
├── 1_📊_ROI_by_Measure.py
├── 2_💰_Cost_Per_Closure.py
├── 3_📈_Monthly_Trend.py
├── 4_💵_Budget_Variance.py
├── 5_🎯_Cost_Tier_Comparison.py
├── 6_🤖_AI_Executive_Insights.py
├── 7_📊_What-If_Scenario_Modeler.py
├── 8_🎓_AI_Capabilities_Demo.py
├── 8_📋_Campaign_Builder.py
├── 9_🔔_Alert_Center.py
├── 10_📈_Historical_Tracking.py
├── 11_💰_ROI_Calculator.py
├── 13_📋_Measure_Analysis.py
├── 14_⭐_Star_Rating_Simulator.py
├── 15_🔄_Gap_Closure_Workflow.py
├── 16_🤖_ML_Gap_Closure_Predictions.py
├── 17_📊_Competitive_Benchmarking.py
├── 18_📋_Compliance_Reporting.py
├── 18_🤖_Secure_AI_Chatbot.py
├── 19_⚖️_Health_Equity_Index.py
└── z_Performance_Dashboard.py
```

**Total Pages:** 22 pages (including main app.py)

---

## 🎨 Custom CSS System

### 1. Main Responsive CSS (Lines 39-621 in app.py)

#### Desktop Styles (769px+)
```css
/* Header Container */
.header-container {
    background: linear-gradient(180deg, #4A3D6F 0%, #6F5F96 100%);
    padding: 0.5rem 0.75rem 0.6rem 0.75rem;
    border-radius: 6px;
    margin-top: -1rem !important;
    margin-bottom: 0.1rem;
    text-align: center;
    box-shadow: 0 4px 12px rgba(74, 61, 111, 0.25);
}

/* Typography - Center Aligned */
h1 {
    margin-top: 0.2rem !important;
    margin-bottom: 0.15rem !important;
    font-size: 2.5rem !important;
    font-weight: 700 !important;
    text-align: center !important;
}

h2 {
    font-size: 1.75rem !important;
    font-weight: 600 !important;
    text-align: center !important;
}

/* Metrics - Center Aligned */
[data-testid="stMetricValue"] {
    font-size: 2.5rem !important;
    font-weight: 700 !important;
    text-align: center !important;
}

/* Buttons with Hover Effects */
button[kind="primary"],
button[kind="secondary"] {
    padding: 0.6rem 1.5rem !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
    border-radius: 6px !important;
    transition: all 0.2s ease !important;
}

button[kind="primary"]:hover,
button[kind="secondary"]:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15) !important;
}
```

#### Mobile Styles (max-width: 768px)
```css
@media (max-width: 768px) {
    /* Mobile spacing - optimized for touch */
    div.block-container {
        padding-top: 1.5rem !important;
        padding-left: 0.75rem !important;
        padding-right: 0.75rem !important;
        padding-bottom: 1rem !important;
    }
    
    h1 {
        font-size: 1.5rem !important;
        font-weight: 700 !important;
        text-align: center !important;
    }
    
    /* Mobile buttons - full width with better touch targets */
    button[kind="primary"],
    button[kind="secondary"],
    .stButton > button {
        width: 100% !important;
        min-height: 44px !important;
        margin-bottom: 0.75rem !important;
        padding: 0.75rem 1rem !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
        transition: all 0.2s ease !important;
    }
    
    button[kind="primary"]:active,
    button[kind="secondary"]:active {
        transform: scale(0.98) !important;
        opacity: 0.9 !important;
    }
    
    /* Mobile metrics - optimized sizing */
    [data-testid="stMetricValue"] {
        font-size: 1.75rem !important;
        font-weight: 700 !important;
    }
    
    /* Mobile tabs - stack vertically */
    .stTabs [data-baseweb="tab-list"] {
        flex-direction: column !important;
        width: 100% !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        width: 100% !important;
        min-height: 44px !important;
        padding: 0.875rem 1rem !important;
    }
}
```

#### Tablet Styles (769px - 1024px)
```css
@media (min-width: 769px) and (max-width: 1024px) {
    div.block-container {
        padding-left: 2rem !important;
        padding-right: 2rem !important;
    }
    
    h1 {
        font-size: 1.75rem !important;
    }
}
```

#### Large Desktop (1025px+)
```css
@media (min-width: 1025px) {
    div.block-container {
        max-width: 1600px !important;
        padding-left: 5rem !important;
        padding-right: 5rem !important;
    }
    
    h1 {
        font-size: 2.75rem !important;
    }
}
```

#### Ultra-Wide Desktop (1440px+)
```css
@media (min-width: 1440px) {
    div.block-container {
        max-width: 1800px !important;
        padding-left: 6rem !important;
        padding-right: 6rem !important;
    }
}
```

### 2. Purple Sidebar Theme CSS (Lines 636-747)

```css
/* Purple Sidebar Gradient */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #4A3D6F 0%, #6F5F96 100%) !important;
}

/* All Sidebar Text White */
[data-testid="stSidebar"] * {
    color: #FFFFFF !important;
}

/* Home Button Styling */
[data-testid="stSidebarNav"] ul li:first-child a {
    background: rgba(255, 255, 255, 0.2) !important;
    padding: 0.75rem 1rem !important;
    border-radius: 8px !important;
    border: 2px solid rgba(255, 255, 255, 0.3) !important;
}
```

### 3. Spacing Reduction CSS (Lines 631-626)

```css
.block-container {
    padding-top: 0.5rem !important;
    padding-bottom: 1rem !important;
}

h1, h2, h3, h4, h5, h6 {
    margin-top: 0.25rem !important;
    margin-bottom: 0.5rem !important;
}

div[data-testid="stVerticalBlock"] {
    gap: 0.25rem !important;
}
```

### 4. KPI Section Styling

```css
.kpi-section-wrapper {
    justify-content: center !important;
    align-items: center !important;
    gap: 0px !important;
}

.kpi-section-wrapper .element-container {
    margin-bottom: 0.5rem !important;
}
```

### 5. Print Styles

```css
@media print {
    [data-testid="stSidebar"] {
        display: none !important;
    }
    
    .header-container {
        page-break-after: avoid;
    }
}
```

---

## 🎯 Key CSS Features

### Responsive Breakpoints
- **Mobile:** max-width: 768px
- **Tablet:** 769px - 1024px
- **Desktop:** 1025px+
- **Large Desktop:** 1440px+

### Color Scheme
- **Primary Purple:** `#4A3D6F` to `#6F5F96` (gradient)
- **Accent Purple:** `#E8D4FF`
- **Success Green:** `#00cc66`
- **Info Blue:** `#0066cc`

### Typography
- **Desktop H1:** 2.5rem (2.75rem on large desktop)
- **Mobile H1:** 1.5rem
- **Font Weight:** 700 for headings, 600 for subheadings

### Touch Targets
- **Mobile buttons:** Minimum 44px height (accessibility standard)
- **Mobile tabs:** Full width, 44px minimum height

### Animations
- **Button hover:** `translateY(-1px)` with shadow
- **Button active:** `scale(0.98)` with opacity change
- **Transitions:** `all 0.2s ease`

---

## 📝 Notes

- All CSS is embedded in `app.py` using `st.markdown()` with `unsafe_allow_html=True`
- No external CSS files are used
- CSS is organized by breakpoint (Desktop → Mobile → Tablet → Large Desktop)
- Mobile-first approach with progressive enhancement for larger screens
- All text is center-aligned for consistency
- Metrics and KPIs are prominently displayed with large fonts

---

## 🔗 Related Files

- **Responsive utilities:** `utils/responsive_layout.py`
- **Responsive header:** `utils/responsive_header.py`
- **Mobile navigation:** `utils/mobile_navigation.py`
- **Mobile tables:** `utils/mobile_tables.py`

