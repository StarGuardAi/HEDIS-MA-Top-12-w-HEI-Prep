"""
Add sidebar separator styling to all page files
"""
import os
import sys
from pathlib import Path

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# Sidebar separator CSS to add
SEPARATOR_CSS = """
/* ========== SIDEBAR SEPARATOR STYLING - SUBTLE GREEN GRADIENT ========== */
/* Sidebar separator styling - subtle green gradient (thicker for visibility) */
[data-testid="stSidebar"] hr {
    border: none !important;
    height: 4px !important;
    margin: 1rem 0 !important;
    background: linear-gradient(
        90deg,
        transparent 0%,
        rgba(74, 222, 128, 0.8) 50%,
        transparent 100%
    ) !important;
}
"""

def add_separator_css_to_file(file_path):
    """Add sidebar separator CSS to a page file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if separator CSS already exists
        if 'SIDEBAR SEPARATOR STYLING' in content:
            print(f"  [SKIP] {file_path.name} - Already has separator CSS")
            return False
        
        # Find the sidebar CSS block and add separator before closing </style>
        # Look for pattern: sidebar CSS ending with } followed by </style>
        # We want to add before the closing </style> tag of the sidebar CSS block
        
        # Find the last occurrence of sidebar-related CSS before </style>
        # Pattern: look for [data-testid="stSidebar"] CSS block ending
        
        # More reliable: find where sidebar CSS ends (before </style>)
        # Look for closing brace + </style> pattern in sidebar context
        
        # Strategy: Find the closing </style> tag that comes after sidebar CSS
        # Insert separator CSS right before it
        
        # Find the position right before </style> that's after sidebar CSS
        # Look for pattern: } followed by </style> with sidebar context before it
        
        # Simple approach: Find the </style> tag that comes after sidebar-related CSS
        # and insert before it
        
        lines = content.split('\n')
        modified = False
        new_lines = []
        i = 0
        
        while i < len(lines):
            line = lines[i]
            new_lines.append(line)
            
            # Check if this is a closing </style> tag
            if line.strip() == '</style>':
                # Check if previous lines contain sidebar CSS
                # Look back a few lines to see if we're in sidebar CSS context
                lookback_start = max(0, i - 20)
                context = '\n'.join(lines[lookback_start:i])
                
                # If we see sidebar CSS context, add separator before </style>
                if '[data-testid="stSidebar"]' in context and 'SIDEBAR SEPARATOR STYLING' not in context:
                    # Insert separator CSS before this </style>
                    new_lines.pop()  # Remove the </style> we just added
                    new_lines.append(SEPARATOR_CSS)
                    new_lines.append('</style>')
                    modified = True
                    print(f"  [OK] {file_path.name} - Added separator CSS")
            
            i += 1
        
        if modified:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(new_lines))
            return True
        else:
            print(f"  [WARN] {file_path.name} - Could not find insertion point")
            return False
            
    except Exception as e:
        print(f"  [ERROR] {file_path.name} - Error: {e}")
        return False

def main():
    """Add sidebar separator CSS to all page files"""
    pages_dir = Path(__file__).parent / 'pages'
    
    if not pages_dir.exists():
        print(f"Error: {pages_dir} does not exist")
        return
    
    print("Adding sidebar separator styling to all page files...")
    print("=" * 60)
    
    page_files = sorted([f for f in pages_dir.glob('*.py') if f.name != '__init__.py'])
    
    success_count = 0
    skip_count = 0
    error_count = 0
    
    for page_file in page_files:
        result = add_separator_css_to_file(page_file)
        if result is True:
            success_count += 1
        elif result is False:
            # Check if it was skipped (already has CSS) or error
            with open(page_file, 'r', encoding='utf-8') as f:
                content = f.read()
            if 'SIDEBAR SEPARATOR STYLING' in content:
                skip_count += 1
            else:
                error_count += 1
    
    print("=" * 60)
    print(f"[SUCCESS] Successfully updated: {success_count} files")
    print(f"[SKIP] Already had CSS: {skip_count} files")
    print(f"[ERROR] Errors/Skipped: {error_count} files")
    print(f"[TOTAL] Total processed: {len(page_files)} files")

if __name__ == '__main__':
    main()

