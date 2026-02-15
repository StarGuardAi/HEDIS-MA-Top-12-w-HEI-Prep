"""
Center the mobile optimized badge on all pages
"""
import os
import sys
from pathlib import Path

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

def center_mobile_badge(file_path):
    """Center the mobile optimized badge"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find and replace the mobile badge div
        old_pattern = '<div class=\'mobile-optimized-badge\' style=\'background: linear-gradient(135deg, #10B981 0%, #059669 100%); border-radius: 50px; padding: 10px 24px; text-align: center; margin: 24px auto; color: white; font-weight: 700; font-size: 1rem; box-shadow: 0 4px 12px rgba(16, 185, 129, 0.4); border: 3px solid rgba(255, 255, 255, 0.5); max-width: 220px; display: inline-block;\'>'
        
        new_pattern = '<div class=\'mobile-optimized-badge\' style=\'background: linear-gradient(135deg, #10B981 0%, #059669 100%); border-radius: 50px; padding: 10px 24px; text-align: center; margin: 24px auto; color: white; font-weight: 700; font-size: 1rem; box-shadow: 0 4px 12px rgba(16, 185, 129, 0.4); border: 3px solid rgba(255, 255, 255, 0.5); max-width: 220px; display: block; width: fit-content;\'>'
        
        if old_pattern in content:
            content = content.replace(old_pattern, new_pattern)
            
            # Also add CSS to ensure centering
            if '.mobile-optimized-badge' not in content or 'display: block' not in content.split('.mobile-optimized-badge')[1][:200]:
                # Add CSS rule if not present
                css_rule = """
    .mobile-optimized-badge {
        display: block !important;
        margin-left: auto !important;
        margin-right: auto !important;
        width: fit-content !important;
    }
"""
                # Insert before closing </style> tag
                if '</style>' in content:
                    content = content.replace('</style>', css_rule + '</style>', 1)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True, "Centered"
        else:
            return False, "Badge not found"
            
    except Exception as e:
        return None, str(e)

def main():
    """Process all page files"""
    pages_dir = Path(__file__).parent / 'pages'
    
    if not pages_dir.exists():
        print(f"Error: {pages_dir} does not exist")
        return
    
    print("Centering mobile optimized badge on all pages...")
    print("=" * 60)
    
    page_files = sorted([
        f for f in pages_dir.glob('*.py') 
        if f.name != '__init__.py'
    ])
    
    stats = {
        'centered': 0,
        'skipped': 0,
        'errors': 0
    }
    
    for page_file in page_files:
        result, info = center_mobile_badge(page_file)
        
        if result is True:
            print(f"[CENTERED] {page_file.name}")
            stats['centered'] += 1
        elif result is False:
            print(f"[SKIP] {page_file.name} - {info}")
            stats['skipped'] += 1
        else:
            print(f"[ERROR] {page_file.name} - {info}")
            stats['errors'] += 1
    
    print("=" * 60)
    print(f"[SUMMARY]")
    print(f"  Centered: {stats['centered']}")
    print(f"  Skipped: {stats['skipped']}")
    print(f"  Errors: {stats['errors']}")
    print(f"  Total: {len(page_files)} files")

if __name__ == '__main__':
    main()


