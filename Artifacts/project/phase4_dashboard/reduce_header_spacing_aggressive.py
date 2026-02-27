"""
Aggressively reduce spacing between header and page title
1. Reduce header padding-bottom
2. Add aggressive CSS to eliminate all spacing after header
"""
import os
import sys
import re
from pathlib import Path

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# Aggressive spacing reduction CSS
AGGRESSIVE_SPACING_CSS = """
/* Reduce spacing after header - AGGRESSIVE */
.starguard-header-container + *,
.starguard-header-container ~ * {
    margin-top: 0rem !important;
    padding-top: 0 !important;
}

/* Reduce spacing for first content element after header */
.starguard-header-container ~ .element-container:first-of-type,
.starguard-header-container ~ div[data-testid="stVerticalBlock"]:first-of-type,
.starguard-header-container ~ div[data-testid="stVerticalBlock"] {
    margin-top: 0rem !important;
    padding-top: 0 !important;
}

/* Target markdown containers immediately after header */
.starguard-header-container ~ div[data-testid="stMarkdownContainer"],
.starguard-header-container ~ .stMarkdown {
    margin-top: 0rem !important;
    padding-top: 0 !important;
    margin-bottom: 0rem !important;
}

/* Target headings immediately after header */
.starguard-header-container ~ h1,
.starguard-header-container ~ h2,
.starguard-header-container ~ h3,
.starguard-header-container ~ div[data-testid="stMarkdownContainer"] h1,
.starguard-header-container ~ div[data-testid="stMarkdownContainer"] h2,
.starguard-header-container ~ div[data-testid="stMarkdownContainer"] h3 {
    margin-top: 0rem !important;
    padding-top: 0 !important;
}

/* Reduce padding on header subtitle */
.starguard-subtitle {
    margin-bottom: 0rem !important;
    padding-bottom: 0rem !important;
}
"""

def reduce_header_spacing_aggressive(file_path):
    """Aggressively reduce spacing after header"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        changes = []
        
        # 1. Reduce header padding-bottom (change padding from 1rem 1.5rem to 1rem 1.5rem 0.5rem 1.5rem)
        if '.starguard-header-container' in content:
            # Replace padding: 1rem 1.5rem with padding: 1rem 1.5rem 0.5rem 1.5rem
            content = re.sub(
                r'(\.starguard-header-container\s*\{[^}]*?padding:\s*)1rem\s+1\.5rem(\s*!important;)',
                r'\g<1>1rem 1.5rem 0.5rem 1.5rem\g<2>',
                content,
                flags=re.DOTALL
            )
            changes.append('header_padding')
        
        # 2. Replace existing spacing CSS with more aggressive version
        if 'Reduce spacing after header' in content:
            # Find and replace the spacing CSS block
            lines = content.split('\n')
            new_lines = []
            i = 0
            in_spacing_block = False
            replaced = False
            
            while i < len(lines):
                line = lines[i]
                
                # Detect start of spacing block
                if 'Reduce spacing after header' in line:
                    in_spacing_block = True
                    if not replaced:
                        # Replace entire block
                        new_lines.append('/* Reduce spacing after header - AGGRESSIVE */')
                        new_lines.extend(AGGRESSIVE_SPACING_CSS.strip().split('\n')[1:])  # Skip first line as we added it
                        replaced = True
                        changes.append('spacing_css')
                        # Skip until end of block
                        while i < len(lines) and '}' in lines[i] and in_spacing_block:
                            if lines[i].strip() == '}' and 'starguard-header-container' in '\n'.join(new_lines[max(0, len(new_lines)-10):]):
                                in_spacing_block = False
                                i += 1
                                break
                            i += 1
                        continue
                
                if not in_spacing_block:
                    new_lines.append(line)
                
                i += 1
            
            if replaced:
                content = '\n'.join(new_lines)
            else:
                # If replacement didn't work, try simpler approach - just add after existing
                if 'Reduce spacing after header' in content and 'AGGRESSIVE' not in content:
                    # Find the closing brace of spacing block and add more CSS
                    content = re.sub(
                        r'(\.starguard-header-container\s*~\s*div\[data-testid="stVerticalBlock"\][^}]*?\})',
                        r'\g<1>\n\n/* Target markdown containers immediately after header */\n.starguard-header-container ~ div[data-testid="stMarkdownContainer"],\n.starguard-header-container ~ .stMarkdown {\n    margin-top: 0rem !important;\n    padding-top: 0 !important;\n    margin-bottom: 0rem !important;\n}\n\n/* Target headings immediately after header */\n.starguard-header-container ~ h1,\n.starguard-header-container ~ h2,\n.starguard-header-container ~ h3,\n.starguard-header-container ~ div[data-testid="stMarkdownContainer"] h1,\n.starguard-header-container ~ div[data-testid="stMarkdownContainer"] h2,\n.starguard-header-container ~ div[data-testid="stMarkdownContainer"] h3 {\n    margin-top: 0rem !important;\n    padding-top: 0 !important;\n}\n\n/* Reduce padding on header subtitle */\n.starguard-subtitle {\n    margin-bottom: 0rem !important;\n    padding-bottom: 0rem !important;\n}',
                        content
                    )
                    changes.append('spacing_css_added')
        
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
    
    print("Aggressively reducing spacing between header and page title...")
    print("=" * 60)
    print("Fixes:")
    print("  1. Reduce header padding-bottom")
    print("  2. Add aggressive CSS to eliminate all spacing")
    print("=" * 60)
    
    page_files = sorted([f for f in pages_dir.glob('*.py') if f.name != '__init__.py'])
    
    stats = {
        'header_padding': 0,
        'spacing_css': 0,
        'errors': 0,
        'skipped': 0
    }
    
    for page_file in page_files:
        result, info = reduce_header_spacing_aggressive(page_file)
        
        if result is True:
            changes = ', '.join(info)
            print(f"[OK] {page_file.name}")
            print(f"     Changes: {changes}")
            if 'header_padding' in info:
                stats['header_padding'] += 1
            if 'spacing_css' in info or 'spacing_css_added' in info:
                stats['spacing_css'] += 1
        elif result is False:
            print(f"[SKIP] {page_file.name} - No changes needed")
            stats['skipped'] += 1
        else:
            print(f"[ERROR] {page_file.name} - {info}")
            stats['errors'] += 1
    
    print("=" * 60)
    print(f"[SUMMARY]")
    print(f"  Header padding reduced: {stats['header_padding']}")
    print(f"  Spacing CSS updated: {stats['spacing_css']}")
    print(f"  Skipped: {stats['skipped']}")
    print(f"  Errors: {stats['errors']}")
    print(f"  Total: {len(page_files)} files")

if __name__ == '__main__':
    main()

