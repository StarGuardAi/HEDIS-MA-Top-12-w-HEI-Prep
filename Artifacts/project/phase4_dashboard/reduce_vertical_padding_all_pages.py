"""
Reduce excessive vertical padding on all pages
1. Reduce header margin-bottom from 0.75rem to 0.25rem
2. Remove separator line (st.markdown("---")) after header
3. Add CSS to reduce spacing after header
"""
import os
import sys
import re
from pathlib import Path

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

def reduce_vertical_padding(file_path):
    """Reduce vertical padding in a page file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        changes = []
        
        # 1. Reduce header margin-bottom from 0.75rem to 0.25rem
        if 'margin-bottom: 0.75rem !important;' in content:
            content = content.replace(
                'margin-bottom: 0.75rem !important;',
                'margin-bottom: 0.25rem !important;'
            )
            changes.append('header_margin')
        
        # Also check for other margin-bottom values on header
        content = re.sub(
            r'(\.starguard-header-container\s*\{[^}]*?margin-bottom:\s*)0\.75rem',
            r'\g<1>0.25rem',
            content,
            flags=re.DOTALL
        )
        
        # 2. Remove separator line after header
        # Pattern: header HTML followed by st.markdown("---")
        if 'starguard-header-container' in content:
            # Look for pattern: </div>""" followed by st.markdown("---")
            content = re.sub(
                r"(</div>\s*\"\"\", unsafe_allow_html=True)\s*\n\s*st\.markdown\(\"---\"\)",
                r'\1',
                content,
                flags=re.MULTILINE
            )
            
            # Also check for just st.markdown("---") on its own line after header
            lines = content.split('\n')
            new_lines = []
            i = 0
            removed_separator = False
            
            while i < len(lines):
                line = lines[i]
                
                # Check if this is the separator line after header
                if (line.strip() == 'st.markdown("---")' or 
                    line.strip() == "st.markdown('---')" or
                    line.strip() == 'st.markdown("""---""")'):
                    # Check if previous lines contain header
                    lookback = '\n'.join(new_lines[max(0, len(new_lines)-10):])
                    if 'starguard-header-container' in lookback and not removed_separator:
                        # Skip this separator line
                        removed_separator = True
                        i += 1
                        continue
                
                new_lines.append(line)
                i += 1
            
            if removed_separator:
                content = '\n'.join(new_lines)
                changes.append('separator_removed')
        
        # 3. Add CSS to reduce spacing after header
        if '.starguard-header-container' in content and 'Reduce spacing after header' not in content:
            # Add CSS rule to reduce spacing
            spacing_css = """
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
            
            # Insert before closing </style> tag in first CSS block
            lines = content.split('\n')
            new_lines = []
            i = 0
            inserted = False
            
            while i < len(lines):
                line = lines[i]
                new_lines.append(line)
                
                # Look for closing </style> tag in first CSS block (before header HTML)
                if line.strip() == '</style>' and not inserted:
                    lookback = '\n'.join(new_lines[max(0, len(new_lines)-20):])
                    lookahead = '\n'.join(lines[i+1:min(i+5, len(lines))])
                    
                    # If header HTML comes after this </style>, insert spacing CSS before it
                    if 'starguard-header-container' in lookahead and 'starguard-header-container' not in lookback:
                        new_lines.pop()  # Remove </style>
                        new_lines.append(spacing_css.strip())
                        new_lines.append('</style>')
                        inserted = True
                        changes.append('spacing_css')
                
                i += 1
            
            if inserted:
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
    
    print("Reducing excessive vertical padding on all pages...")
    print("=" * 60)
    print("Fixes:")
    print("  1. Reduce header margin-bottom: 0.75rem -> 0.25rem")
    print("  2. Remove separator line after header")
    print("  3. Add CSS to reduce spacing after header")
    print("=" * 60)
    
    page_files = sorted([f for f in pages_dir.glob('*.py') if f.name != '__init__.py'])
    
    stats = {
        'header_margin': 0,
        'separator_removed': 0,
        'spacing_css': 0,
        'errors': 0,
        'skipped': 0
    }
    
    for page_file in page_files:
        result, info = reduce_vertical_padding(page_file)
        
        if result is True:
            changes = ', '.join(info)
            print(f"[OK] {page_file.name}")
            print(f"     Changes: {changes}")
            if 'header_margin' in info:
                stats['header_margin'] += 1
            if 'separator_removed' in info:
                stats['separator_removed'] += 1
            if 'spacing_css' in info:
                stats['spacing_css'] += 1
        elif result is False:
            print(f"[SKIP] {page_file.name} - No changes needed")
            stats['skipped'] += 1
        else:
            print(f"[ERROR] {page_file.name} - {info}")
            stats['errors'] += 1
    
    print("=" * 60)
    print(f"[SUMMARY]")
    print(f"  Header margin reduced: {stats['header_margin']}")
    print(f"  Separators removed: {stats['separator_removed']}")
    print(f"  Spacing CSS added: {stats['spacing_css']}")
    print(f"  Skipped: {stats['skipped']}")
    print(f"  Errors: {stats['errors']}")
    print(f"  Total: {len(page_files)} files")

if __name__ == '__main__':
    main()

