"""
Ensure top data headers are centered on all pages
Add comprehensive CSS targeting for Streamlit markdown headers
"""
import os
import sys
from pathlib import Path
import re

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

ENHANCED_HEADER_CSS = '''
/* Enhanced center-align for top data headers */
.stMarkdown h2,
.stMarkdown h3,
div[data-testid="stMarkdownContainer"] h2,
div[data-testid="stMarkdownContainer"] h3,
[data-testid="stMarkdownContainer"] h2,
[data-testid="stMarkdownContainer"] h3,
.element-container h2,
.element-container h3,
div[data-testid="stVerticalBlock"] h2,
div[data-testid="stVerticalBlock"] h3 {
    text-align: center !important;
}

/* Center all markdown content headers */
.stMarkdown:has(h2),
.stMarkdown:has(h3) {
    text-align: center !important;
}
'''

def enhance_header_css(file_path):
    """Enhance header CSS with comprehensive targeting"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if enhanced CSS already exists
    if 'Enhanced center-align for top data headers' in content:
        return False, "Already enhanced"
    
    # Find the markdown headers section
    pattern = r'/\* Center markdown headers.*?div\[data-testid="stMarkdownContainer"\] h3 \{.*?text-align: center.*?\}'
    
    enhanced_section = '''/* Center markdown headers - comprehensive targeting */
.stMarkdown h2,
.stMarkdown h3,
div[data-testid="stMarkdownContainer"] h2,
div[data-testid="stMarkdownContainer"] h3,
[data-testid="stMarkdownContainer"] h2,
[data-testid="stMarkdownContainer"] h3,
.element-container h2,
.element-container h3,
div[data-testid="stVerticalBlock"] h2,
div[data-testid="stVerticalBlock"] h3 {
    text-align: center !important;
}

/* Center all markdown content headers */
.stMarkdown:has(h2),
.stMarkdown:has(h3) {
    text-align: center !important;
}'''
    
    # Replace the section
    new_content = re.sub(pattern, enhanced_section, content, flags=re.DOTALL)
    
    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True, "Enhanced header CSS"
    
    return False, "Could not find section"

def main():
    """Enhance header CSS on all pages"""
    base_dir = Path(__file__).parent
    app_file = base_dir / 'app.py'
    pages_dir = base_dir / 'pages'
    
    print("Ensuring top data headers are centered...")
    print("=" * 60)
    
    files_to_update = [app_file] + list(pages_dir.glob('*.py'))
    
    stats = {'enhanced': 0, 'skipped': 0}
    
    for file_path in files_to_update:
        if not file_path.exists():
            continue
        
        file_name = file_path.name
        
        result, info = enhance_header_css(file_path)
        
        if result:
            print(f"[ENHANCED] {file_name} - {info}")
            stats['enhanced'] += 1
        else:
            stats['skipped'] += 1
    
    print("=" * 60)
    print(f"[SUMMARY] Enhanced: {stats['enhanced']}, Skipped: {stats['skipped']}")

if __name__ == '__main__':
    main()


