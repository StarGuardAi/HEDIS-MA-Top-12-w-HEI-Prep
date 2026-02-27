"""
Add KPI/metric header and sidebar centering CSS to all pages
"""
import os
import sys
from pathlib import Path
import re

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

KPI_SIDEBAR_CSS = '''
/* ========== CENTER KPI/METRIC HEADERS ========== */
/* Center metric labels (Potential ROI, Star Rating Impact, etc.) */
[data-testid="stMetricLabel"] {
    display: flex !important;
    justify-content: center !important;
    text-align: center !important;
}

[data-testid="stMetricLabel"] > div {
    text-align: center !important;
    width: 100% !important;
}

/* Center metric values */
[data-testid="stMetricValue"] {
    display: flex !important;
    justify-content: center !important;
    text-align: center !important;
}

/* Center metric delta (the +/- change indicators) */
[data-testid="stMetricDelta"] {
    display: flex !important;
    justify-content: center !important;
}

/* Center content in metric containers */
[data-testid="metric-container"] {
    text-align: center !important;
}

/* Center column content for KPI cards */
[data-testid="column"] {
    text-align: center !important;
}

/* ========== CENTER SIDEBAR CONTENT ========== */
/* Center sidebar text and labels */
[data-testid="stSidebar"] [data-testid="stMarkdown"] {
    text-align: center !important;
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] p {
    text-align: center !important;
}

/* Center sidebar metric cards */
[data-testid="stSidebar"] [data-testid="stMetricLabel"],
[data-testid="stSidebar"] [data-testid="stMetricValue"],
[data-testid="stSidebar"] [data-testid="stMetricDelta"] {
    justify-content: center !important;
    text-align: center !important;
}

/* Center expander headers in sidebar */
[data-testid="stSidebar"] .streamlit-expanderHeader {
    justify-content: center !important;
}
'''

def add_kpi_sidebar_css(file_path):
    """Add KPI and sidebar centering CSS to a file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if already added
    if 'CENTER KPI/METRIC HEADERS' in content:
        return False, "Already added"
    
    # Find where to insert (before closing </style> tag)
    style_close_pattern = r'(</style>)'
    
    match = re.search(style_close_pattern, content)
    if match:
        insert_pos = match.start()
        # Insert before </style>
        new_content = content[:insert_pos] + KPI_SIDEBAR_CSS + '\n' + content[insert_pos:]
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True, "Added KPI/sidebar centering CSS"
    
    return False, "Style block not found"

def check_conflicting_css(file_path):
    """Check for conflicting CSS that might override centering"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    conflicts = []
    
    # Check for left-align in metric/KPI contexts
    left_align_pattern = r'\[data-testid="stMetric.*?"\].*?text-align:\s*left'
    if re.search(left_align_pattern, content, re.DOTALL | re.IGNORECASE):
        conflicts.append("Left-align found in metric styling")
    
    # Check for flex-start in metric contexts
    flex_start_pattern = r'\[data-testid="stMetric.*?"\].*?justify-content:\s*flex-start'
    if re.search(flex_start_pattern, content, re.DOTALL | re.IGNORECASE):
        conflicts.append("Flex-start found in metric styling")
    
    return conflicts

def main():
    """Add KPI/sidebar centering CSS to all pages"""
    base_dir = Path(__file__).parent
    app_file = base_dir / 'app.py'
    pages_dir = base_dir / 'pages'
    
    print("Adding KPI/metric header and sidebar centering CSS...")
    print("=" * 60)
    
    files_to_update = [app_file] + list(pages_dir.glob('*.py'))
    
    stats = {'added': 0, 'skipped': 0, 'conflicts': 0, 'errors': 0}
    
    for file_path in files_to_update:
        if not file_path.exists():
            continue
        
        file_name = file_path.name
        
        try:
            # Check for conflicts first
            conflicts = check_conflicting_css(file_path)
            if conflicts:
                print(f"[CONFLICT] {file_name} - {', '.join(conflicts)}")
                stats['conflicts'] += 1
            
            # Add CSS
            result, info = add_kpi_sidebar_css(file_path)
            
            if result:
                print(f"[ADDED] {file_name} - {info}")
                stats['added'] += 1
            else:
                if "Already added" in info:
                    print(f"[SKIP] {file_name} - {info}")
                    stats['skipped'] += 1
                else:
                    stats['skipped'] += 1
        except Exception as e:
            print(f"[ERROR] {file_name} - {str(e)}")
            stats['errors'] += 1
    
    print("=" * 60)
    print("[SUMMARY]")
    print(f"  Added: {stats['added']}")
    print(f"  Skipped: {stats['skipped']}")
    print(f"  Conflicts found: {stats['conflicts']}")
    print(f"  Errors: {stats['errors']}")

if __name__ == '__main__':
    main()


