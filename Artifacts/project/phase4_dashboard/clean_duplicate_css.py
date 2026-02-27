"""
Remove duplicate CSS and invalid selectors from all pages
"""
import os
import sys
from pathlib import Path
import re

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

def clean_css(file_path):
    """Remove invalid selectors and duplicates"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Remove invalid :has-text() selectors
    content = re.sub(r'h[23]:has-text\("[^"]+"\),?\s*', '', content)
    content = re.sub(r'\.stMarkdown:has-text\("[^"]+"\)\s*\+\s*h[23],?\s*', '', content)
    
    # Remove duplicate markdown header rules (keep first occurrence)
    markdown_header_pattern = r'/\* Center markdown headers \*/\s*\.stMarkdown h2,.*?div\[data-testid="stMarkdownContainer"\] h3 \{.*?text-align: center.*?\}'
    matches = list(re.finditer(markdown_header_pattern, content, re.DOTALL))
    if len(matches) > 1:
        # Keep first, remove rest
        for match in matches[1:]:
            content = content[:match.start()] + content[match.end():]
    
    # Remove duplicate caption rules
    caption_pattern = r'/\* Center captions and notes \*/\s*\.stCaption,.*?div\.stCaption \{.*?text-align: center.*?\}'
    matches = list(re.finditer(caption_pattern, content, re.DOTALL))
    if len(matches) > 1:
        for match in matches[1:]:
            content = content[:match.start()] + content[match.end():]
    
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True, "Cleaned CSS"
    
    return False, "No changes needed"

def main():
    """Clean CSS on all files"""
    base_dir = Path(__file__).parent
    app_file = base_dir / 'app.py'
    pages_dir = base_dir / 'pages'
    
    print("Cleaning duplicate CSS and invalid selectors...")
    print("=" * 60)
    
    files_to_update = [app_file] + list(pages_dir.glob('*.py'))
    
    stats = {'cleaned': 0, 'skipped': 0}
    
    for file_path in files_to_update:
        if not file_path.exists():
            continue
        
        file_name = file_path.name
        
        result, info = clean_css(file_path)
        
        if result:
            print(f"[CLEANED] {file_name} - {info}")
            stats['cleaned'] += 1
        else:
            stats['skipped'] += 1
    
    print("=" * 60)
    print(f"[SUMMARY] Cleaned: {stats['cleaned']}, Skipped: {stats['skipped']}")

if __name__ == '__main__':
    main()


