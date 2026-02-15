"""
Refine center-align styling - be more selective about what gets centered
"""
import os
import sys
from pathlib import Path
import re

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

def refine_styling(file_path):
    """Refine center-align CSS to be more selective"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace the alert/expander section
    old_pattern = r'/\* Center info boxes and alerts.*?\.streamlit-expanderHeader \{.*?text-align: center.*?\}'
    
    new_section = '''/* Center info boxes - selective (only for summary/metric displays) */
.stAlert[data-baseweb="notification"],
.stInfo[data-baseweb="notification"],
.stSuccess[data-baseweb="notification"],
.stWarning[data-baseweb="notification"],
.stError[data-baseweb="notification"] {
    text-align: center !important;
}

/* Keep expander headers left-aligned for readability */
.streamlit-expanderHeader {
    text-align: left !important;
}'''
    
    # Replace
    new_content = re.sub(old_pattern, new_section, content, flags=re.DOTALL)
    
    # Also update the text content section
    old_text_pattern = r'/\* Keep text content left-aligned.*?text-align: center.*?\}'
    
    new_text_section = '''/* Keep text content left-aligned (headings, paragraphs) for readability */
h1, h2, h3, h4, h5, h6 {
    text-align: left !important;
}

p, li {
    text-align: left !important;
}

/* Exception: Center specific summary/metric section headers */
h3:has-text("Summary"),
h3:has-text("Metrics"),
h3:has-text("Overview"),
h2:has-text("Summary"),
h2:has-text("Metrics") {
    text-align: center !important;
}'''
    
    new_content = re.sub(old_text_pattern, new_text_section, new_content, flags=re.DOTALL)
    
    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True, "Refined styling"
    
    return False, "No changes needed"

def main():
    """Refine styling on all files"""
    base_dir = Path(__file__).parent
    app_file = base_dir / 'app.py'
    pages_dir = base_dir / 'pages'
    
    print("Refining center-align styling...")
    print("=" * 60)
    
    files_to_update = [app_file] + list(pages_dir.glob('*.py'))
    
    stats = {'updated': 0, 'skipped': 0}
    
    for file_path in files_to_update:
        if not file_path.exists():
            continue
        
        file_name = file_path.name
        
        result, info = refine_styling(file_path)
        
        if result:
            print(f"[UPDATED] {file_name} - {info}")
            stats['updated'] += 1
        else:
            stats['skipped'] += 1
    
    print("=" * 60)
    print(f"[SUMMARY] Updated: {stats['updated']}, Skipped: {stats['skipped']}")

if __name__ == '__main__':
    main()


