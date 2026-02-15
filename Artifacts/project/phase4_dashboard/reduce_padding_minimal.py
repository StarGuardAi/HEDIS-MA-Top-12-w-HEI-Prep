"""
Reduce padding to minimal - very tight spacing
1. Reduce header margin-bottom from 0.1rem to 0rem
2. Reduce spacing CSS values from 0.1rem to 0rem
3. Reduce mobile margin-bottom to 0rem
"""
import os
import sys
import re
from pathlib import Path

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

def reduce_padding_minimal(file_path):
    """Reduce padding to minimal in a page file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        changes = []
        
        # 1. Reduce header margin-bottom from 0.1rem to 0rem
        if 'margin-bottom: 0.1rem !important;' in content:
            # Only replace in .starguard-header-container context
            content = re.sub(
                r'(\.starguard-header-container\s*\{[^}]*?margin-bottom:\s*)0\.1rem(\s*!important;)',
                r'\g<1>0rem\g<2>',
                content,
                flags=re.DOTALL
            )
            changes.append('header_margin')
        
        # 2. Reduce spacing CSS values from 0.1rem to 0rem
        if 'Reduce spacing after header' in content:
            content = re.sub(
                r'(\.starguard-header-container\s*[+~]\s*\*\{[^}]*?margin-top:\s*)0\.1rem(\s*!important;)',
                r'\g<1>0rem\g<2>',
                content
            )
            content = re.sub(
                r'(\.starguard-header-container\s*~\s*\.element-container[^}]*?margin-top:\s*)0\.1rem(\s*!important;)',
                r'\g<1>0rem\g<2>',
                content
            )
            content = re.sub(
                r'(\.starguard-header-container\s*~\s*div\[data-testid="stVerticalBlock"\][^}]*?margin-top:\s*)0\.1rem(\s*!important;)',
                r'\g<1>0rem\g<2>',
                content
            )
            changes.append('spacing_css')
        
        # 3. Reduce mobile margin-bottom to 0rem
        lines = content.split('\n')
        new_lines = []
        i = 0
        in_mobile_header = False
        
        while i < len(lines):
            line = lines[i]
            
            # Track if we're in mobile media query for header
            if '@media (max-width: 768px)' in line:
                in_mobile_header = False
            if '.starguard-header-container' in line and '@media' in '\n'.join(new_lines[max(0, len(new_lines)-10):]):
                in_mobile_header = True
            
            if in_mobile_header and 'margin-bottom: 0.1rem !important;' in line:
                line = line.replace('margin-bottom: 0.1rem !important;', 'margin-bottom: 0rem !important;')
                changes.append('mobile_margin')
            
            new_lines.append(line)
            i += 1
        
        content = '\n'.join(new_lines)
        
        if changes:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True, changes
        else:
            return False, []
            
    except Exception as e:
        return None, str(e)

def main():
    """Process all page files"""
    pages_dir = Path(__file__).parent / 'pages'
    
    if not pages_dir.exists():
        print(f"Error: {pages_dir} does not exist")
        return
    
    print("Reducing padding to minimal on all pages...")
    print("=" * 60)
    print("Fixes:")
    print("  1. Reduce header margin-bottom: 0.1rem -> 0rem")
    print("  2. Reduce spacing CSS: 0.1rem -> 0rem")
    print("  3. Reduce mobile margin-bottom: 0.1rem -> 0rem")
    print("=" * 60)
    
    page_files = sorted([f for f in pages_dir.glob('*.py') if f.name != '__init__.py'])
    
    stats = {
        'header_margin': 0,
        'spacing_css': 0,
        'mobile_margin': 0,
        'errors': 0,
        'skipped': 0
    }
    
    for page_file in page_files:
        result, info = reduce_padding_minimal(page_file)
        
        if result is True:
            changes = ', '.join(info)
            print(f"[OK] {page_file.name}")
            print(f"     Changes: {changes}")
            if 'header_margin' in info:
                stats['header_margin'] += 1
            if 'spacing_css' in info:
                stats['spacing_css'] += 1
            if 'mobile_margin' in info:
                stats['mobile_margin'] += 1
        elif result is False:
            print(f"[SKIP] {page_file.name} - No changes needed")
            stats['skipped'] += 1
        else:
            print(f"[ERROR] {page_file.name} - {info}")
            stats['errors'] += 1
    
    print("=" * 60)
    print(f"[SUMMARY]")
    print(f"  Header margin reduced: {stats['header_margin']}")
    print(f"  Spacing CSS reduced: {stats['spacing_css']}")
    print(f"  Mobile margin reduced: {stats['mobile_margin']}")
    print(f"  Skipped: {stats['skipped']}")
    print(f"  Errors: {stats['errors']}")
    print(f"  Total: {len(page_files)} files")

if __name__ == '__main__':
    main()

