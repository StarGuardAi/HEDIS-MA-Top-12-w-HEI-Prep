"""
Final cleanup of summary headers CSS - remove duplicates and fix structure
"""
import os
import sys
from pathlib import Path
import re

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

def final_cleanup(file_path):
    """Final cleanup of CSS"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Remove excessive blank lines (more than 2 consecutive)
    content = re.sub(r'\n{4,}', '\n\n\n', content)
    
    # Remove duplicate "Center headers that come after dividers" rules
    divider_pattern = r'/\* Center headers that come after dividers.*?\}'
    matches = list(re.finditer(divider_pattern, content, re.DOTALL))
    if len(matches) > 1:
        # Keep first, remove rest
        for match in reversed(matches[1:]):
            content = content[:match.start()] + content[match.end():]
    
    # Remove duplicate "Center notes/details below metrics" rules
    notes_pattern = r'/\* Center notes/details below metrics.*?\}'
    matches = list(re.finditer(notes_pattern, content, re.DOTALL))
    if len(matches) > 1:
        for match in reversed(matches[1:]):
            content = content[:match.start()] + content[match.end():]
    
    # Remove duplicate "Center all section headers in main content" rules
    main_pattern = r'/\* Center all section headers in main content.*?\}'
    matches = list(re.finditer(main_pattern, content, re.DOTALL))
    if len(matches) > 1:
        for match in reversed(matches[1:]):
            content = content[:match.start()] + content[match.end():]
    
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True, "Final cleanup done"
    
    return False, "No changes needed"

def main():
    """Final cleanup on all files"""
    base_dir = Path(__file__).parent
    app_file = base_dir / 'app.py'
    pages_dir = base_dir / 'pages'
    
    print("Final cleanup of summary headers CSS...")
    print("=" * 60)
    
    files_to_update = [app_file] + list(pages_dir.glob('*.py'))
    
    stats = {'cleaned': 0, 'skipped': 0}
    
    for file_path in files_to_update:
        if not file_path.exists():
            continue
        
        file_name = file_path.name
        
        result, info = final_cleanup(file_path)
        
        if result:
            print(f"[CLEANED] {file_name} - {info}")
            stats['cleaned'] += 1
        else:
            stats['skipped'] += 1
    
    print("=" * 60)
    print(f"[SUMMARY] Cleaned: {stats['cleaned']}, Skipped: {stats['skipped']}")

if __name__ == '__main__':
    main()


