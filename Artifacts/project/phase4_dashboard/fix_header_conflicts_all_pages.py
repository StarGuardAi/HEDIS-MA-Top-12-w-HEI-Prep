"""
Fix conflicting CSS - remove left-align for h2/h3 since they should be centered
"""
import os
import sys
from pathlib import Path
import re

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

def fix_conflicts(file_path):
    """Fix conflicting CSS rules"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Remove h2, h3 from left-align rule since they should be centered
    # Pattern: h1, h2, h3, h4, h5, h6 { text-align: left !important; }
    pattern1 = r'h1,\s*h2,\s*h3,\s*h4,\s*h5,\s*h6\s*\{[^}]*text-align:\s*left[^}]*\}'
    
    def replace_left_align(match):
        rule = match.group(0)
        # Remove h2 and h3 from the rule
        new_rule = rule.replace('h2,', '').replace('h3,', '').replace(', h2', '').replace(', h3', '')
        # Add comment
        if 'Keep text content left-aligned' not in new_rule:
            new_rule = new_rule.replace('h1,', '/* Exception: h2 and h3 are centered */\nh1,')
        return new_rule
    
    new_content = re.sub(pattern1, replace_left_align, content, flags=re.DOTALL)
    
    # Also handle the simpler pattern
    pattern2 = r'h1,\s*h2,\s*h3,\s*h4,\s*h5,\s*h6\s*\{'
    if re.search(pattern2, new_content):
        # More targeted replacement
        new_content = re.sub(
            r'h1,\s*h2,\s*h3,\s*h4,\s*h5,\s*h6',
            'h1, h4, h5, h6',
            new_content
        )
    
    if new_content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True, "Fixed conflicts"
    
    return False, "No conflicts found"

def main():
    """Fix conflicts on all files"""
    base_dir = Path(__file__).parent
    app_file = base_dir / 'app.py'
    pages_dir = base_dir / 'pages'
    
    print("Fixing conflicting CSS rules...")
    print("=" * 60)
    
    files_to_update = [app_file] + list(pages_dir.glob('*.py'))
    
    stats = {'fixed': 0, 'skipped': 0}
    
    for file_path in files_to_update:
        if not file_path.exists():
            continue
        
        file_name = file_path.name
        
        result, info = fix_conflicts(file_path)
        
        if result:
            print(f"[FIXED] {file_name} - {info}")
            stats['fixed'] += 1
        else:
            stats['skipped'] += 1
    
    print("=" * 60)
    print(f"[SUMMARY] Fixed: {stats['fixed']}, Skipped: {stats['skipped']}")

if __name__ == '__main__':
    main()


