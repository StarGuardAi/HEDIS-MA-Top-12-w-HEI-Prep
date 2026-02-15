"""
Script to update all page titles to match ROI Calculator styling:
- Large bold h1 titles (2rem, font-weight: 700)
- Centered content below titles
- Add CSS to all pages
"""

import os
import re
from pathlib import Path

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

/* Style first h3 on page as page title (if not using h1) */
.main h3:first-of-type,
div[data-testid="stVerticalBlock"] h3:first-of-type,
.stMarkdown h3:first-of-type {
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

/* Center subtitle text immediately after h1 or first h3 */
h1 + p,
h1 ~ p:first-of-type,
h3:first-of-type + p,
h3:first-of-type ~ p:first-of-type,
.page-title-container + p,
.page-title-container ~ p:first-of-type {
    text-align: center !important;
    margin-top: 0 !important;
    margin-bottom: 0.75rem !important;
    font-size: 1rem !important;
}

/* Center content columns below page title */
h1 ~ div[data-testid="column"],
h3:first-of-type ~ div[data-testid="column"],
.page-title-container ~ div[data-testid="column"],
h1 + div[data-testid="stVerticalBlock"] div[data-testid="column"],
h3:first-of-type + div[data-testid="stVerticalBlock"] div[data-testid="column"] {
    text-align: center !important;
}

/* Center info boxes and date range displays below title */
h1 ~ div[data-testid="stInfo"],
h1 ~ div[data-testid="stAlert"],
h3:first-of-type ~ div[data-testid="stInfo"],
h3:first-of-type ~ div[data-testid="stAlert"],
.page-title-container ~ div[data-testid="stInfo"],
.page-title-container ~ div[data-testid="stAlert"] {
    text-align: center !important;
}

/* Center markdown content immediately after h1 or first h3 */
h1 + div[data-testid="stMarkdownContainer"],
h1 ~ div[data-testid="stMarkdownContainer"]:first-of-type,
h3:first-of-type + div[data-testid="stMarkdownContainer"],
h3:first-of-type ~ div[data-testid="stMarkdownContainer"]:first-of-type {
    text-align: center !important;
}

/* Mobile responsive */
@media (max-width: 768px) {
    h1 {
        font-size: 1.5rem !important;
        margin-top: 0.5rem !important;
        margin-bottom: 0.4rem !important;
    }
    
    .main h3:first-of-type {
        font-size: 1.5rem !important;
    }
    
    h1 + p,
    h3:first-of-type + p {
        font-size: 0.9rem !important;
    }
}
"""

def update_page_file(file_path):
    """Update a single page file with CSS and title styling"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if CSS already added
        if 'PAGE TITLE STYLING - MATCH ROI CALCULATOR' in content:
            print(f"  [OK] CSS already exists in {os.path.basename(file_path)}")
            return False
        
        # Find where to insert CSS (before closing </style> tag)
        # Look for pattern: [data-testid="stMetricDelta"] * { ... } followed by </style>
        style_pattern = r'(\[data-testid="stMetricDelta"\] \* \{[^}]+\}\s*\n\s*</style>)'
        match = re.search(style_pattern, content, re.MULTILINE | re.DOTALL)
        
        if not match:
            # Try alternative pattern - find any </style> before unsafe_allow_html
            style_pattern = r'(</style>\s*""", unsafe_allow_html=True)'
            match = re.search(style_pattern, content, re.MULTILINE)
            if match:
                # Insert before </style>
                insert_pos = match.start()
                content = content[:insert_pos] + PAGE_TITLE_CSS + "\n\n" + content[insert_pos:]
            else:
                print(f"  [WARN] Could not find CSS insertion point in {os.path.basename(file_path)}")
                return False
        else:
            # Insert before the closing </style>
            insert_pos = match.start()
            closing_tag = match.group(1)
            content = content[:insert_pos] + PAGE_TITLE_CSS + "\n\n" + closing_tag
        
        # Write updated content
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"  [OK] Updated {os.path.basename(file_path)}")
        return True
        
    except Exception as e:
        print(f"  [ERROR] Error updating {os.path.basename(file_path)}: {e}")
        return False

def main():
    pages_dir = Path(__file__).parent / "pages"
    page_files = [f for f in pages_dir.glob("*.py") if not f.name.startswith("__")]
    
    print(f"Found {len(page_files)} page files")
    print("Updating CSS for page title styling...\n")
    
    updated_count = 0
    for page_file in sorted(page_files):
        if update_page_file(page_file):
            updated_count += 1
    
    print(f"\n✓ Updated {updated_count} page files")
    print("Note: Page titles still need to be converted from h3 to h1 format manually")

if __name__ == "__main__":
    main()

