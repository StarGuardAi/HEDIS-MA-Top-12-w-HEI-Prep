"""
Add StarGuard header CSS to all page files
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
        
        # Find the first CSS block and add StarGuard CSS before closing </style>
        lines = content.split('\n')
        new_lines = []
        i = 0
        inserted = False
        
        while i < len(lines):
            line = lines[i]
            new_lines.append(line)
            
            # Look for closing </style> tag in first CSS block
            if line.strip() == '</style>' and not inserted:
                # Check if this is the first CSS block (before header HTML)
                lookback = '\n'.join(new_lines[max(0, len(new_lines)-30):])
                if 'starguard-header-container' in lookback or 'StarGuard Header HTML' in lookback:
                    # This is after header, skip
                    i += 1
                    continue
                
                # Check if next non-empty line is import or header HTML
                j = i + 1
                while j < len(lines) and lines[j].strip() == '':
                    j += 1
                
                if j < len(lines):
                    next_line = lines[j].strip()
                    # If next line is import, header HTML, or main code, insert CSS before </style>
                    if (next_line.startswith('import ') or 
                        next_line.startswith('from ') or
                        next_line.startswith('# StarGuard Header') or
                        next_line.startswith('st.markdown') or
                        'starguard-header-container' in next_line):
                        # Insert CSS before closing </style>
                        new_lines.pop()  # Remove the </style>
                        new_lines.append(STARGUARD_HEADER_CSS.strip())
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

