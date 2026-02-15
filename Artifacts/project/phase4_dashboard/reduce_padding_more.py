"""
Reduce padding even more - tighter spacing
1. Reduce header margin-bottom from 0.25rem to 0.1rem
2. Reduce spacing CSS values from 0.25rem to 0.1rem
"""
import os
import sys
import re
from pathlib import Path

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

def reduce_padding_more(file_path):
    """Reduce padding even more in a page file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        changes = []
        
        # 1. Reduce header margin-bottom from 0.25rem to 0.1rem
        if 'margin-bottom: 0.25rem !important;' in content:
            content = content.replace(
                'margin-bottom: 0.25rem !important;',
                'margin-bottom: 0.1rem !important;'
            )
            changes.append('header_margin')
        
        # Also check for other margin-bottom values on header
        content = re.sub(
            r'(\.starguard-header-container\s*\{[^}]*?margin-bottom:\s*)0\.25rem',
            r'\g<1>0.1rem',
            content,
            flags=re.DOTALL
        )
        
        # 2. Reduce spacing CSS values from 0.25rem to 0.1rem
        if 'Reduce spacing after header' in content:
            content = re.sub(
                r'(margin-top:\s*)0\.25rem(\s*!important;)',
                r'\g<1>0.1rem\g<2>',
                content
            )
            changes.append('spacing_css')
        
        # 3. Also reduce mobile margin-bottom if it's 0.5rem
        if 'margin-bottom: 0.5rem !important;' in content:
            # Only replace in mobile media query for header
            lines = content.split('\n')
            new_lines = []
            i = 0
            in_mobile_header = False
            
            while i < len(lines):
                line = lines[i]
                
                # Track if we're in mobile media query for header
                if '@media (max-width: 768px)' in line:
                    in_mobile_header = False
                if '.starguard-header-container' in line and '@media' in '\n'.join(new_lines[max(0, len(new_lines)-5):]):
                    in_mobile_header = True
                
                if in_mobile_header and 'margin-bottom: 0.5rem !important;' in line:
                    line = line.replace('margin-bottom: 0.5rem !important;', 'margin-bottom: 0.1rem !important;')
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
    
    print("Reducing padding even more on all pages...")
    print("=" * 60)
    print("Fixes:")
    print("  1. Reduce header margin-bottom: 0.25rem -> 0.1rem")
    print("  2. Reduce spacing CSS: 0.25rem -> 0.1rem")
    print("  3. Reduce mobile margin-bottom: 0.5rem -> 0.1rem")
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
        result, info = reduce_padding_more(page_file)
        
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

