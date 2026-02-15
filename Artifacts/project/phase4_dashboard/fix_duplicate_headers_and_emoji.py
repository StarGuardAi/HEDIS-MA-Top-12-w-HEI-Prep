"""
Fix duplicate headers and add Performance Dashboard emoji CSS backup to all pages
"""
import os
import sys
import re
from pathlib import Path

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# CSS backup for Performance Dashboard emoji
PERFORMANCE_DASHBOARD_CSS = """
/* CSS Backup: Add emoji via ::before for Performance Dashboard links */
[data-testid="stSidebarNav"] a[href*="Performance_Dashboard"]::before {
    content: "⚡ " !important;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI Emoji", "Apple Color Emoji", sans-serif !important;
    display: inline !important;
}
"""

def remove_duplicate_headers(content):
    """Remove old duplicate header (starguard-header with inline styles)"""
    # Pattern: Look for old header with inline styles that duplicates the new one
    # Remove the old "Responsive Header" section that has inline styles
    
    # Pattern 1: Remove old starguard-header div with inline styles
    pattern1 = r"# Responsive Header.*?<div class='starguard-header' style=.*?</div>\s*\"\"\", unsafe_allow_html=True\)"
    content = re.sub(pattern1, '', content, flags=re.DOTALL)
    
    # Pattern 2: Remove standalone old header div
    pattern2 = r"<div class='starguard-header' style='[^']*'>.*?</div>"
    # But keep the new starguard-header-container
    if 'starguard-header-container' in content:
        # Only remove if it's the old inline style version
        lines = content.split('\n')
        new_lines = []
        i = 0
        skip_until = None
        
        while i < len(lines):
            line = lines[i]
            
            # Check if this is the start of old header
            if "<div class='starguard-header' style='" in line and 'starguard-header-container' not in '\n'.join(lines[max(0, i-10):i]):
                # Skip until closing div and </style> or """
                skip_until = 'div_close'
                i += 1
                continue
            
            if skip_until == 'div_close':
                if '</div>' in line:
                    # Check if next line is """ or </style>
                    if i + 1 < len(lines) and ('"""' in lines[i+1] or '</style>' in lines[i+1]):
                        skip_until = None
                        i += 1
                        continue
                i += 1
                continue
            
            new_lines.append(line)
            i += 1
        
        content = '\n'.join(new_lines)
    
    return content

def add_performance_dashboard_css_backup(content):
    """Add CSS backup for Performance Dashboard emoji"""
    # Check if CSS backup already exists
    if 'CSS Backup: Add emoji via ::before for Performance Dashboard links' in content:
        return content, False
    
    # Find insertion point - after sidebar nav CSS, before closing </style>
    # Look for pattern: [data-testid="stSidebarNav"] a p { ... } followed by </style>
    
    lines = content.split('\n')
    new_lines = []
    i = 0
    inserted = False
    
    while i < len(lines):
        line = lines[i]
        new_lines.append(line)
        
        # Look for sidebar nav CSS ending, then add our CSS before closing </style>
        if '[data-testid="stSidebarNav"] a p' in line and not inserted:
            # Find the closing brace for this CSS block
            j = i + 1
            brace_count = 1
            while j < len(lines) and brace_count > 0:
                if '{' in lines[j]:
                    brace_count += lines[j].count('{')
                if '}' in lines[j]:
                    brace_count -= lines[j].count('}')
                j += 1
            
            # Check if next non-empty line after closing brace is </style> or another CSS rule
            while j < len(lines) and lines[j].strip() == '':
                j += 1
            
            if j < len(lines) and ('</style>' in lines[j] or lines[j].strip().startswith('/*') or lines[j].strip().startswith('[')):
                # Insert CSS backup before this line
                new_lines.append('')
                new_lines.append(PERFORMANCE_DASHBOARD_CSS.strip())
                inserted = True
        
        i += 1
    
    # If not inserted, try to add before any closing </style> in sidebar CSS section
    if not inserted:
        for i, line in enumerate(new_lines):
            if '</style>' in line and '[data-testid="stSidebarNav"]' in '\n'.join(new_lines[max(0, i-50):i]):
                new_lines.insert(i, '')
                new_lines.insert(i + 1, PERFORMANCE_DASHBOARD_CSS.strip())
                inserted = True
                break
    
    return '\n'.join(new_lines), inserted

def process_file(file_path):
    """Process a single page file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        changes = []
        
        # 1. Remove duplicate headers
        content = remove_duplicate_headers(content)
        if content != original_content:
            changes.append('duplicate_header')
            original_content = content
        
        # 2. Add Performance Dashboard CSS backup
        content, css_added = add_performance_dashboard_css_backup(content)
        if css_added:
            changes.append('emoji_css')
        
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
    
    print("Fixing duplicate headers and adding Performance Dashboard emoji CSS...")
    print("=" * 60)
    
    page_files = sorted([f for f in pages_dir.glob('*.py') if f.name != '__init__.py'])
    
    stats = {
        'headers': 0,
        'css': 0,
        'errors': 0,
        'skipped': 0
    }
    
    for page_file in page_files:
        result, info = process_file(page_file)
        
        if result is True:
            changes = ', '.join(info)
            print(f"[OK] {page_file.name}")
            print(f"     Changes: {changes}")
            if 'duplicate_header' in info:
                stats['headers'] += 1
            if 'emoji_css' in info:
                stats['css'] += 1
        elif result is False:
            print(f"[SKIP] {page_file.name} - No changes needed")
            stats['skipped'] += 1
        else:
            print(f"[ERROR] {page_file.name} - {info}")
            stats['errors'] += 1
    
    print("=" * 60)
    print(f"[SUMMARY]")
    print(f"  Duplicate headers removed: {stats['headers']}")
    print(f"  Emoji CSS added: {stats['css']}")
    print(f"  Skipped: {stats['skipped']}")
    print(f"  Errors: {stats['errors']}")
    print(f"  Total: {len(page_files)} files")

if __name__ == '__main__':
    main()

