"""
Add nuclear option metric centering CSS to all pages
"""
import os
import sys
from pathlib import Path
import re

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

NUCLEAR_METRIC_CSS = '''
/* ========== NUCLEAR OPTION: FORCE CENTER ALL METRIC TEXT ========== */
/* Target every possible element inside metric containers */
div[data-testid="stMetricContainer"] {
    text-align: center !important;
    align-items: center !important;
    justify-content: center !important;
}

div[data-testid="stMetricContainer"] * {
    text-align: center !important;
    margin-left: auto !important;
    margin-right: auto !important;
}

/* Force center for label text specifically */
div[data-testid="stMetricContainer"] > div:first-child,
div[data-testid="stMetricContainer"] > div:first-child * {
    text-align: center !important;
    display: block !important;
    width: 100% !important;
    margin-left: auto !important;
    margin-right: auto !important;
}

/* Force center for value text */
div[data-testid="stMetricContainer"] > div:nth-child(2),
div[data-testid="stMetricContainer"] > div:nth-child(2) * {
    text-align: center !important;
    display: block !important;
    width: 100% !important;
    margin-left: auto !important;
    margin-right: auto !important;
}

/* Force center for delta text */
div[data-testid="stMetricContainer"] > div:nth-child(3),
div[data-testid="stMetricContainer"] > div:nth-child(3) * {
    text-align: center !important;
    display: block !important;
    width: 100% !important;
    margin-left: auto !important;
    margin-right: auto !important;
}
'''

def add_nuclear_metric_css(file_path):
    """Add nuclear option metric centering CSS to a file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if already added
    if 'NUCLEAR OPTION: FORCE CENTER ALL METRIC TEXT' in content:
        return False, "Already added"
    
    # Find where to insert (before "Center data tables" or before closing </style>)
    insert_patterns = [
        r'(/\* Center data tables)',
        r'(</style>)',
    ]
    
    insert_pos = None
    for pattern in insert_patterns:
        match = re.search(pattern, content)
        if match:
            insert_pos = match.start()
            break
    
    if insert_pos:
        new_content = content[:insert_pos] + NUCLEAR_METRIC_CSS + '\n' + content[insert_pos:]
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True, "Added nuclear option metric centering CSS"
    
    return False, "Insertion point not found"

def main():
    """Add nuclear option metric centering CSS to all pages"""
    base_dir = Path(__file__).parent
    app_file = base_dir / 'app.py'
    pages_dir = base_dir / 'pages'
    
    print("Adding nuclear option metric centering CSS...")
    print("=" * 60)
    
    files_to_update = list(pages_dir.glob('*.py'))
    
    stats = {'added': 0, 'skipped': 0, 'errors': 0}
    
    for file_path in files_to_update:
        if not file_path.exists():
            continue
        
        file_name = file_path.name
        
        try:
            result, info = add_nuclear_metric_css(file_path)
            
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


