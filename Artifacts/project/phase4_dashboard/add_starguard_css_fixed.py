"""
Add StarGuard header CSS to all page files - Fixed version
"""
import os
import sys
from pathlib import Path

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# StarGuard Header CSS (from app.py)
STARGUARD_HEADER_CSS = """
/* StarGuard Header Container - NO BOTTOM BORDER HERE */
.starguard-header-container {
    background: linear-gradient(135deg, #4A3D6F 0%, #6F5F96 100%);
    padding: 1rem 1.5rem !important;
    border-radius: 10px;
    margin-top: 0 !important;
    margin-bottom: 0.75rem !important;
    text-align: center;
    box-shadow: 0 4px 12px rgba(74, 61, 111, 0.25);
    border-bottom: none !important;
}

/* Title - GREEN LINE HERE (between title and subtitle) */
.starguard-title {
    color: white !important;
    font-size: 1.8rem !important;
    font-weight: 700 !important;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    margin: 0 0 0.5rem 0 !important;
    padding: 0 0 0.5rem 0 !important;
    line-height: 1.2 !important;
    border-bottom: 3px solid #4ade80 !important;
}

/* Subtitle - NO BORDER HERE */
.starguard-subtitle {
    color: rgba(255, 255, 255, 0.92) !important;
    font-size: 0.85rem !important;
    margin: 0.5rem 0 0 0 !important;
    padding: 0 !important;
    line-height: 1.3 !important;
    border-bottom: none !important;
}

/* Mobile */
@media (max-width: 768px) {
    .starguard-header-container {
        padding: 0.8rem 1rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    .starguard-title {
        font-size: 1.2rem !important;
        margin-bottom: 0.4rem !important;
        padding-bottom: 0.4rem !important;
    }
    
    .starguard-subtitle {
        font-size: 0.7rem !important;
        margin-top: 0.4rem !important;
    }
}
"""

def add_starguard_css_to_file(file_path):
    """Add StarGuard header CSS to a page file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if CSS already exists
        if '.starguard-header-container' in content and 'border-bottom: 3px solid #4ade80' in content:
            return False, 'already_exists'
        
        # Find where to insert - after .starguard-header CSS rule, before sidebar separator CSS
        # Look for pattern: .starguard-header { ... } followed by other CSS
        
        lines = content.split('\n')
        new_lines = []
        i = 0
        inserted = False
        
        while i < len(lines):
            line = lines[i]
            
            # Look for .starguard-header CSS rule ending
            if '.starguard-header {' in line or '.starguard-header{' in line:
                # Add this line and find the closing brace
                new_lines.append(line)
                i += 1
                brace_count = 1
                
                # Copy until closing brace
                while i < len(lines) and brace_count > 0:
                    new_lines.append(lines[i])
                    if '{' in lines[i]:
                        brace_count += lines[i].count('{')
                    if '}' in lines[i]:
                        brace_count -= lines[i].count('}')
                    i += 1
                
                # Now insert StarGuard CSS after this block
                if not inserted:
                    new_lines.append('')
                    new_lines.append(STARGUARD_HEADER_CSS.strip())
                    inserted = True
                continue
            
            new_lines.append(line)
            i += 1
        
        if inserted:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(new_lines))
            return True, 'inserted'
        else:
            # Try alternative: insert before first </style> tag
            lines = content.split('\n')
            new_lines = []
            i = 0
            
            while i < len(lines):
                line = lines[i]
                new_lines.append(line)
                
                if line.strip() == '</style>' and not inserted:
                    # Check if header HTML comes after this
                    lookahead = '\n'.join(lines[i+1:min(i+10, len(lines))])
                    if 'starguard-header-container' in lookahead:
                        # Insert CSS before </style>
                        new_lines.pop()
                        new_lines.append(STARGUARD_HEADER_CSS.strip())
                        new_lines.append('</style>')
                        inserted = True
                
                i += 1
            
            if inserted:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(new_lines))
                return True, 'inserted_alt'
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
    
    print("Adding StarGuard Header CSS to all page files...")
    print("=" * 60)
    
    page_files = sorted([f for f in pages_dir.glob('*.py') if f.name != '__init__.py'])
    
    stats = {
        'inserted': 0,
        'already_exists': 0,
        'no_point': 0,
        'errors': 0
    }
    
    for page_file in page_files:
        result, info = add_starguard_css_to_file(page_file)
        
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

