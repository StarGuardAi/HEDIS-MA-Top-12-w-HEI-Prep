"""
Utility CSS for consistent page title styling across all pages
Matches ROI Calculator page styling: large bold font, centered content
"""

PAGE_TITLE_CSS = """
/* ========== PAGE TITLE STYLING - MATCH ROI CALCULATOR ========== */
/* Large bold h1 titles matching ROI Calculator */
h1 {
    font-size: 2rem !important;
    font-weight: 700 !important;
    text-align: center !important;
    margin-top: 0.5rem !important;
    margin-bottom: 0.5rem !important;
    padding-top: 0 !important;
    line-height: 1.2 !important;
}

/* Center page title containers */
.page-title-container,
.roi-calculator-title-container {
    margin-top: 0.5rem !important;
    padding-top: 0.5rem !important;
    margin-bottom: 0 !important;
    padding-bottom: 0 !important;
    text-align: center !important;
}

.page-title-container h1,
.roi-calculator-title-container h1 {
    margin-top: 0 !important;
    padding-top: 0 !important;
    margin-bottom: 0.5rem !important;
    text-align: center !important;
    font-size: 2rem !important;
    font-weight: 700 !important;
}

/* Center subtitle text immediately after h1 */
h1 + p,
h1 ~ p:first-of-type,
.page-title-container + p,
.page-title-container ~ p:first-of-type {
    text-align: center !important;
    margin-top: 0 !important;
    margin-bottom: 0.75rem !important;
    font-size: 1rem !important;
}

/* Center content columns below page title */
h1 ~ div[data-testid="column"],
.page-title-container ~ div[data-testid="column"],
h1 + div[data-testid="stVerticalBlock"] div[data-testid="column"] {
    text-align: center !important;
}

/* Center info boxes and date range displays below title */
h1 ~ div[data-testid="stInfo"],
h1 ~ div[data-testid="stAlert"],
.page-title-container ~ div[data-testid="stInfo"],
.page-title-container ~ div[data-testid="stAlert"],
h1 + div[data-testid="stVerticalBlock"] div[data-testid="stInfo"],
h1 + div[data-testid="stVerticalBlock"] div[data-testid="stAlert"] {
    text-align: center !important;
}

/* Center markdown content immediately after h1 */
h1 + div[data-testid="stMarkdownContainer"],
h1 ~ div[data-testid="stMarkdownContainer"]:first-of-type,
.page-title-container + div[data-testid="stMarkdownContainer"],
.page-title-container ~ div[data-testid="stMarkdownContainer"]:first-of-type {
    text-align: center !important;
}

/* Center all content in the first vertical block after h1 */
h1 ~ div[data-testid="stVerticalBlock"]:first-of-type,
.page-title-container ~ div[data-testid="stVerticalBlock"]:first-of-type {
    text-align: center !important;
}

/* Mobile responsive */
@media (max-width: 768px) {
    h1 {
        font-size: 1.5rem !important;
        margin-top: 0.5rem !important;
        margin-bottom: 0.4rem !important;
    }
    
    .page-title-container h1,
    .roi-calculator-title-container h1 {
        font-size: 1.5rem !important;
    }
    
    h1 + p,
    h1 ~ p:first-of-type {
        font-size: 0.9rem !important;
    }
}
"""

def get_page_title_css():
    """Return CSS for page title styling"""
    return PAGE_TITLE_CSS

