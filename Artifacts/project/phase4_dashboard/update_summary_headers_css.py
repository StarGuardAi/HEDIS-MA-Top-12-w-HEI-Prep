"""
Update summary headers CSS to use valid selectors
"""
import os
import sys
from pathlib import Path
import re

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

VALID_CSS = '''
/* ========== CENTER SUMMARY HEADERS AND NOTES ========== */

/* Center all h2 and h3 headers (section headers) */
h2, h3 {
    text-align: center !important;
}

/* Center markdown headers */
.stMarkdown h2,
.stMarkdown h3,
div[data-testid="stMarkdownContainer"] h2,
div[data-testid="stMarkdownContainer"] h3 {
    text-align: center !important;
}

/* Center captions and notes */
.stCaption,
[data-testid="stCaption"],
p.stCaption,
div.stCaption {
    text-align: center !important;
}

/* Center headers that come after dividers (section headers) */
hr + h2,
hr + h3 {
    text-align: center !important;
}

/* Center notes/details below metrics */
[data-testid="stMetricContainer"] + .stMarkdown,
[data-testid="stMetricContainer"] ~ .stMarkdown,
.stMetric + .stMarkdown {
    text-align: center !important;
}

/* Center all section headers in main content */
.main h2,
.main h3,
section.main h2,
section.main h3 {
    text-align: center !important;
}
'''

def update_css(file_path):
    """Update CSS with valid selectors"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find and replace the invalid CSS
    pattern = r'/\* ========== CENTER SUMMARY HEADERS AND NOTES ========== \*/\s*/\*.*?\*/\s*/\* Center all section headers.*?\}'
    
    if re.search(pattern, content, re.DOTALL):
        new_content = re.sub(pattern, VALID_CSS.strip(), content, flags=re.DOTALL)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True, "Updated CSS"
    
    return False, "CSS section not found"

def main():
    """Update CSS on all files"""
    base_dir = Path(__file__).parent
    app_file = base_dir / 'app.py'
    pages_dir = base_dir / 'pages'
    
    print("Updating summary headers CSS with valid selectors...")
    print("=" * 60)
    
    files_to_update = [app_file] + list(pages_dir.glob('*.py'))
    
    stats = {'updated': 0, 'skipped': 0}
    
    for file_path in files_to_update:
        if not file_path.exists():
            continue
        
        file_name = file_path.name
        
        result, info = update_css(file_path)
        
        if result:
            print(f"[UPDATED] {file_name} - {info}")
            stats['updated'] += 1
        else:
            stats['skipped'] += 1
    
    print("=" * 60)
    print(f"[SUMMARY] Updated: {stats['updated']}, Skipped: {stats['skipped']}")

if __name__ == '__main__':
    main()


