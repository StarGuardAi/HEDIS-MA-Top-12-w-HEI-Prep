"""
Center-align summary metrics and tables on all pages and sidebars
Apply where it improves UX and clean viewing
"""
import os
import sys
from pathlib import Path
import re

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

CENTER_STYLING_CSS = '''
/* ========== CENTER-ALIGN METRICS AND TABLES FOR CLEAN VIEWING ========== */

/* Center metric cards - values and labels */
[data-testid="stMetricValue"],
[data-testid="stMetricLabel"],
[data-testid="stMetricDelta"] {
    text-align: center !important;
    justify-content: center !important;
}

/* Center metric containers */
div[data-testid="stMetricContainer"] {
    text-align: center !important;
}

/* Center metric value text */
[data-testid="stMetricValue"] > div {
    text-align: center !important;
    margin: 0 auto !important;
}

/* Center metric labels */
[data-testid="stMetricLabel"] > div {
    text-align: center !important;
    margin: 0 auto !important;
}

/* Center data tables - cell content */
.stDataFrame,
.stDataFrame table,
.stDataFrame td,
.stDataFrame th {
    text-align: center !important;
}

/* Center table headers */
.stDataFrame thead th {
    text-align: center !important;
    font-weight: 600 !important;
}

/* Center table cells */
.stDataFrame tbody td {
    text-align: center !important;
}

/* Center sidebar metrics */
[data-testid="stSidebar"] [data-testid="stMetricValue"],
[data-testid="stSidebar"] [data-testid="stMetricLabel"],
[data-testid="stSidebar"] [data-testid="stMetricDelta"] {
    text-align: center !important;
}

[data-testid="stSidebar"] div[data-testid="stMetricContainer"] {
    text-align: center !important;
}

/* Center summary tables in sidebars */
[data-testid="stSidebar"] .stDataFrame,
[data-testid="stSidebar"] .stDataFrame table,
[data-testid="stSidebar"] .stDataFrame td,
[data-testid="stSidebar"] .stDataFrame th {
    text-align: center !important;
}

/* Center caption text */
.stCaption {
    text-align: center !important;
}

/* Center info boxes and alerts (where appropriate) */
.stAlert,
.stInfo,
.stSuccess,
.stWarning,
.stError {
    text-align: center !important;
}

/* Center expander headers (but keep content left-aligned) */
.streamlit-expanderHeader {
    text-align: center !important;
}

/* Center column headers in tables */
.stDataFrame th {
    text-align: center !important;
}

/* Center numeric values in tables */
.stDataFrame td {
    text-align: center !important;
}

/* Keep text content left-aligned (headings, paragraphs) */
h1, h2, h3, h4, h5, h6,
p, li, span:not([data-testid="stMetricValue"]):not([data-testid="stMetricLabel"]),
div:not([data-testid="stMetricContainer"]):not(.stDataFrame):not(.stDataFrame *) {
    /* Default left-align for text content */
}

/* Exception: Center specific summary sections */
.stMarkdown:has-text("Summary") h3,
.stMarkdown:has-text("Metrics") h3,
.stMarkdown:has-text("Overview") h3 {
    text-align: center !important;
}
'''

def add_center_styling(file_path):
    """Add center-align CSS to a file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if already added
    if 'CENTER-ALIGN METRICS AND TABLES' in content:
        return False, "Already added"
    
    # Find the CSS style block (look for existing style tag)
    style_pattern = r'(</style>)'
    
    # Try to find where to insert (before closing </style> tag)
    match = re.search(style_pattern, content)
    if match:
        insert_pos = match.start()
        # Insert before </style>
        new_content = content[:insert_pos] + CENTER_STYLING_CSS + '\n' + content[insert_pos:]
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True, "Added center-align CSS"
    
    # If no </style> found, look for <style> tag and add after it
    style_open_pattern = r'(<style>)'
    match = re.search(style_open_pattern, content)
    if match:
        insert_pos = match.end()
        # Find the end of the style block (look for </style> or end of markdown block)
        style_close = content.find('</style>', insert_pos)
        if style_close > 0:
            insert_pos = style_close
        else:
            # Look for end of triple-quoted string
            next_quotes = content.find('"""', insert_pos)
            if next_quotes > 0:
                insert_pos = next_quotes
        
        new_content = content[:insert_pos] + CENTER_STYLING_CSS + '\n' + content[insert_pos:]
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True, "Added center-align CSS"
    
    return False, "Style block not found"

def main():
    """Add center-align styling to all pages"""
    base_dir = Path(__file__).parent
    app_file = base_dir / 'app.py'
    pages_dir = base_dir / 'pages'
    
    print("Adding center-align styling to metrics and tables...")
    print("=" * 60)
    
    files_to_update = [app_file] + list(pages_dir.glob('*.py'))
    
    stats = {'added': 0, 'skipped': 0, 'errors': 0}
    
    for file_path in files_to_update:
        if not file_path.exists():
            continue
        
        file_name = file_path.name
        
        result, info = add_center_styling(file_path)
        
        if result is True:
            print(f"[ADDED] {file_name} - {info}")
            stats['added'] += 1
        elif result is False:
            if "Already added" in info:
                print(f"[SKIP] {file_name} - {info}")
                stats['skipped'] += 1
            else:
                print(f"[SKIP] {file_name} - {info}")
                stats['skipped'] += 1
        else:
            print(f"[ERROR] {file_name} - {info}")
            stats['errors'] += 1
    
    print("=" * 60)
    print("[SUMMARY]")
    print(f"  Added: {stats['added']}")
    print(f"  Skipped: {stats['skipped']}")
    print(f"  Errors: {stats['errors']}")

if __name__ == '__main__':
    main()


