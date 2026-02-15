"""
Fix summary headers CSS on all pages - replace invalid selectors with valid ones
"""
import os
import sys
from pathlib import Path
import re

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

VALID_CSS = '''/* ========== CENTER SUMMARY HEADERS AND NOTES ========== */

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
}'''

def fix_css(file_path):
    """Replace invalid CSS with valid CSS"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the section starting with CENTER SUMMARY HEADERS
    start_marker = '/* ========== CENTER SUMMARY HEADERS AND NOTES ========== */'
    end_marker = '}'
    
    if start_marker not in content:
        return False, "Section not found"
    
    # Find start position
    start_pos = content.find(start_marker)
    
    # Find end position - look for the closing brace of the last rule
    # Count opening and closing braces to find the end
    pos = start_pos
    brace_count = 0
    in_rule = False
    
    while pos < len(content):
        if content[pos] == '{':
            brace_count += 1
            in_rule = True
        elif content[pos] == '}':
            brace_count -= 1
            if brace_count == 0 and in_rule:
                # Found the end of the last rule
                end_pos = pos + 1
                break
        pos += 1
    else:
        # Fallback: look for next major section or </style>
        end_pos = content.find('/* ==========', start_pos + 100)
        if end_pos == -1:
            end_pos = content.find('</style>', start_pos)
        if end_pos == -1:
            return False, "Could not find end"
    
    # Replace the section
    new_content = content[:start_pos] + VALID_CSS + '\n' + content[end_pos:]
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    return True, "Fixed CSS"

def main():
    """Fix CSS on all files"""
    base_dir = Path(__file__).parent
    app_file = base_dir / 'app.py'
    pages_dir = base_dir / 'pages'
    
    print("Fixing summary headers CSS on all pages...")
    print("=" * 60)
    
    files_to_update = [app_file] + list(pages_dir.glob('*.py'))
    
    stats = {'fixed': 0, 'skipped': 0, 'errors': 0}
    
    for file_path in files_to_update:
        if not file_path.exists():
            continue
        
        file_name = file_path.name
        
        try:
            result, info = fix_css(file_path)
            
            if result:
                print(f"[FIXED] {file_name} - {info}")
                stats['fixed'] += 1
            else:
                if "not found" in info.lower():
                    stats['skipped'] += 1
                else:
                    print(f"[SKIP] {file_name} - {info}")
                    stats['skipped'] += 1
        except Exception as e:
            print(f"[ERROR] {file_name} - {str(e)}")
            stats['errors'] += 1
    
    print("=" * 60)
    print(f"[SUMMARY] Fixed: {stats['fixed']}, Skipped: {stats['skipped']}, Errors: {stats['errors']}")

if __name__ == '__main__':
    main()


