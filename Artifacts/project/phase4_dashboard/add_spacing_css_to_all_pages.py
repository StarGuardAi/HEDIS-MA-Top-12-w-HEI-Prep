"""
Add spacing reduction CSS to all pages
"""
import os
import sys
from pathlib import Path

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# Spacing reduction CSS
SPACING_CSS = """
/* Reduce spacing after header */
.starguard-header-container + *,
.starguard-header-container ~ * {
    margin-top: 0.25rem !important;
}

/* Reduce spacing for first content element after header */
.starguard-header-container ~ .element-container:first-of-type,
.starguard-header-container ~ div[data-testid="stVerticalBlock"]:first-of-type {
    margin-top: 0.25rem !important;
    padding-top: 0 !important;
}
"""

def add_spacing_css(file_path):
    """Add spacing reduction CSS to a page file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if CSS already exists
        if 'Reduce spacing after header' in content:
            return False, 'already_exists'
        
        # Find insertion point - before closing </style> tag in first CSS block
        lines = content.split('\n')
        new_lines = []
        i = 0
        inserted = False
        
        while i < len(lines):
            line = lines[i]
            new_lines.append(line)
            
            # Look for closing </style> tag before header HTML
            if line.strip() == '</style>' and not inserted:
                lookback = '\n'.join(new_lines[max(0, len(new_lines)-20):])
                lookahead = '\n'.join(lines[i+1:min(i+5, len(lines))])
                
                # If header HTML comes after this </style>, insert spacing CSS before it
                if 'starguard-header-container' in lookahead and 'starguard-header-container' not in lookback:
                    new_lines.pop()  # Remove </style>
                    new_lines.append(SPACING_CSS.strip())
                    new_lines.append('</style>')
                    inserted = True
            
            i += 1
        
        if inserted:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(new_lines))
            return True, 'inserted'
        else:
            return False, 'no_insertion_point'
            
    except Exception as e:
        return None, str(e)

def main():
    """Process all page files"""
    pages_dir = Path(__file__).parent / 'pages'
    
    if not pages_dir.exists():
        print(f"Error: {pages_dir} does not exist")
        return
    
    print("Adding spacing reduction CSS to all pages...")
    print("=" * 60)
    
    page_files = sorted([f for f in pages_dir.glob('*.py') if f.name != '__init__.py'])
    
    stats = {
        'inserted': 0,
        'already_exists': 0,
        'no_point': 0,
        'errors': 0
    }
    
    for page_file in page_files:
        result, info = add_spacing_css(page_file)
        
        if result is True:
            print(f"[OK] {page_file.name} - CSS added")
            stats['inserted'] += 1
        elif result is False:
            if info == 'already_exists':
                print(f"[SKIP] {page_file.name} - CSS already exists")
                stats['already_exists'] += 1
            else:
                print(f"[WARN] {page_file.name} - Could not find insertion point")
                stats['no_point'] += 1
        else:
            print(f"[ERROR] {page_file.name} - {info}")
            stats['errors'] += 1
    
    print("=" * 60)
    print(f"[SUMMARY]")
    print(f"  CSS added: {stats['inserted']}")
    print(f"  Already had CSS: {stats['already_exists']}")
    print(f"  No insertion point: {stats['no_point']}")
    print(f"  Errors: {stats['errors']}")
    print(f"  Total: {len(page_files)} files")

if __name__ == '__main__':
    main()

