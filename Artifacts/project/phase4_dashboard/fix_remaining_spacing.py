"""
Fix remaining spacing CSS values that weren't caught
"""
import os
import sys
from pathlib import Path

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

def fix_remaining_spacing(file_path):
    """Fix remaining 0.1rem spacing values"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        changes = []
        
        # Fix spacing CSS - replace 0.1rem with 0rem in spacing rules
        if 'Reduce spacing after header' in content:
            # Replace margin-top: 0.1rem in spacing rules
            lines = content.split('\n')
            new_lines = []
            i = 0
            in_spacing_rule = False
            
            while i < len(lines):
                line = lines[i]
                
                # Track if we're in spacing rule
                if 'Reduce spacing after header' in line:
                    in_spacing_rule = True
                if in_spacing_rule and 'margin-top: 0.1rem !important;' in line:
                    line = line.replace('margin-top: 0.1rem !important;', 'margin-top: 0rem !important;')
                    changes.append('spacing_fixed')
                if in_spacing_rule and line.strip() == '}' and 'Reduce spacing' in '\n'.join(new_lines[max(0, len(new_lines)-5):]):
                    in_spacing_rule = False
                
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
    
    print("Fixing remaining spacing CSS values...")
    print("=" * 60)
    
    page_files = sorted([f for f in pages_dir.glob('*.py') if f.name != '__init__.py'])
    
    stats = {
        'fixed': 0,
        'skipped': 0,
        'errors': 0
    }
    
    for page_file in page_files:
        result, info = fix_remaining_spacing(page_file)
        
        if result is True:
            print(f"[OK] {page_file.name} - Fixed")
            stats['fixed'] += 1
        elif result is False:
            print(f"[SKIP] {page_file.name} - No changes needed")
            stats['skipped'] += 1
        else:
            print(f"[ERROR] {page_file.name} - {info}")
            stats['errors'] += 1
    
    print("=" * 60)
    print(f"[SUMMARY]")
    print(f"  Fixed: {stats['fixed']}")
    print(f"  Skipped: {stats['skipped']}")
    print(f"  Errors: {stats['errors']}")
    print(f"  Total: {len(page_files)} files")

if __name__ == '__main__':
    main()

