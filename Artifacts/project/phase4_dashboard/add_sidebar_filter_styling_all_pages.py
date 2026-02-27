"""
Add sidebar filter styling CSS to all pages
"""
import os
import sys
from pathlib import Path
import re

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

SIDEBAR_FILTER_CSS = '''
/* ========== SIDEBAR FILTER STYLING ========== */
/* Filter section header */
[data-testid="stSidebar"] h3 {
    color: white !important;
    font-size: 1rem !important;
    margin-bottom: 0.5rem !important;
    padding-bottom: 0.25rem !important;
    border-bottom: 1px solid rgba(255,255,255,0.2) !important;
}

/* Compact filter widgets */
[data-testid="stSidebar"] .stSelectbox,
[data-testid="stSidebar"] .stMultiSelect,
[data-testid="stSidebar"] .stSlider,
[data-testid="stSidebar"] .stRadio {
    margin-bottom: 0.75rem !important;
}

/* Filter labels */
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stMultiSelect label,
[data-testid="stSidebar"] .stSlider label,
[data-testid="stSidebar"] .stRadio label {
    color: white !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
}

/* Dropdown styling on purple background */
[data-testid="stSidebar"] .stSelectbox > div > div,
[data-testid="stSidebar"] .stMultiSelect > div > div {
    background-color: rgba(255,255,255,0.95) !important;
    border-radius: 5px !important;
}
'''

def add_sidebar_filter_css(file_path):
    """Add sidebar filter CSS to a file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if already added
    if 'SIDEBAR FILTER STYLING' in content:
        return False, "Already added"
    
    # Find where to insert (before closing </style> tag)
    style_close_pattern = r'(</style>)'
    
    match = re.search(style_close_pattern, content)
    if match:
        insert_pos = match.start()
        # Insert before </style>
        new_content = content[:insert_pos] + SIDEBAR_FILTER_CSS + '\n' + content[insert_pos:]
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True, "Added sidebar filter CSS"
    
    return False, "Style block not found"

def main():
    """Add sidebar filter CSS to all pages"""
    base_dir = Path(__file__).parent
    app_file = base_dir / 'app.py'
    pages_dir = base_dir / 'pages'
    
    print("Adding sidebar filter styling CSS...")
    print("=" * 60)
    
    files_to_update = [app_file] + list(pages_dir.glob('*.py'))
    
    stats = {'added': 0, 'skipped': 0, 'errors': 0}
    
    for file_path in files_to_update:
        if not file_path.exists():
            continue
        
        file_name = file_path.name
        
        try:
            result, info = add_sidebar_filter_css(file_path)
            
            if result:
                print(f"[ADDED] {file_name} - {info}")
                stats['added'] += 1
            else:
                if "Already added" in info:
                    print(f"[SKIP] {file_name} - {info}")
                else:
                    print(f"[SKIP] {file_name} - {info}")
                stats['skipped'] += 1
        except Exception as e:
            print(f"[ERROR] {file_name} - {str(e)}")
            stats['errors'] += 1
    
    print("=" * 60)
    print(f"[SUMMARY] Added: {stats['added']}, Skipped: {stats['skipped']}, Errors: {stats['errors']}")

if __name__ == '__main__':
    main()


