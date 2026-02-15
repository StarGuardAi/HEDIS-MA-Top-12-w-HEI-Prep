"""
Fix st.set_page_config() to be the first Streamlit command in all pages
Move it before any st.markdown() calls
"""
import os
import sys
import re
from pathlib import Path

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

def fix_page_config_order(file_path):
    """Move st.set_page_config() to be the first Streamlit command"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Find st.set_page_config() call
        page_config_match = re.search(
            r'st\.set_page_config\([^)]+\)',
            content,
            re.DOTALL
        )
        
        if not page_config_match:
            return False, "No st.set_page_config() found"
        
        page_config_block = page_config_match.group(0)
        page_config_start = page_config_match.start()
        page_config_end = page_config_match.end()
        
        # Check if there are any st.* calls before st.set_page_config()
        before_config = content[:page_config_start]
        
        # Check for Streamlit commands before set_page_config
        streamlit_commands = re.findall(r'st\.\w+\(', before_config)
        
        if not streamlit_commands:
            return False, "Already correct order"
        
        # Find the first non-comment, non-import line
        lines = content.split('\n')
        first_streamlit_line = -1
        
        for i, line in enumerate(lines):
            stripped = line.strip()
            # Skip comments, imports, docstrings
            if (stripped.startswith('#') or 
                stripped.startswith('"""') or 
                stripped.startswith("'''") or
                'import' in stripped or
                'from' in stripped):
                continue
            
            # Check if this line has a Streamlit command
            if 'st.' in stripped and 'st.set_page_config' not in stripped:
                first_streamlit_line = i
                break
        
        if first_streamlit_line == -1:
            return False, "Could not find first Streamlit command"
        
        # Extract the page_config block with its full context
        # Find the line number where page_config starts
        page_config_line_start = content[:page_config_start].count('\n')
        
        # Get the full page_config block including any comments before it
        page_config_lines = []
        for i in range(max(0, page_config_line_start - 2), min(len(lines), page_config_line_start + 10)):
            page_config_lines.append(lines[i])
            if 'st.set_page_config' in lines[i]:
                # Find where it ends
                j = i
                paren_count = 0
                while j < len(lines):
                    line = lines[j]
                    paren_count += line.count('(') - line.count(')')
                    if paren_count == 0 and ')' in line:
                        break
                    j += 1
                # Include all lines up to j
                if j > i:
                    page_config_lines = lines[max(0, page_config_line_start - 2):j+1]
                break
        
        # Remove page_config from its current location
        # Find the exact range to remove
        page_config_start_line = content[:page_config_start].count('\n')
        # Find where page_config ends (including the closing paren and newline)
        page_config_end_pos = content.find(')', page_config_start) + 1
        page_config_end_line = content[:page_config_end_pos].count('\n')
        
        # Remove from original location
        lines_before = lines[:page_config_start_line]
        lines_after = lines[page_config_end_line + 1:]
        
        # Find where to insert (after imports, before first st.* command)
        insert_pos = 0
        for i, line in enumerate(lines_before):
            stripped = line.strip()
            # Stop before first st.* command that's not set_page_config
            if 'st.' in stripped and 'st.set_page_config' not in stripped:
                insert_pos = i
                break
            # Also stop after imports
            if i > 0 and ('import' in lines_before[i-1] or 'from' in lines_before[i-1]):
                if not (stripped.startswith('#') or stripped.startswith('"""') or 'import' in stripped or 'from' in stripped):
                    insert_pos = i
                    break
        
        # Reconstruct with page_config in the right place
        new_lines = (
            lines_before[:insert_pos] + 
            [''] +  # Add blank line
            lines[page_config_start_line:page_config_end_line + 1] +
            [''] +  # Add blank line
            lines_before[insert_pos:] +
            lines_after
        )
        
        new_content = '\n'.join(new_lines)
        
        # Verify st.set_page_config is before any other st.* calls
        first_st_pos = new_content.find('st.')
        if first_st_pos != -1:
            if 'st.set_page_config' not in new_content[:first_st_pos + 20]:
                return False, "Could not properly reorder"
        
        if new_content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return True, "Fixed"
        else:
            return False, "No changes needed"
            
    except Exception as e:
        return None, str(e)

def main():
    """Process all page files"""
    pages_dir = Path(__file__).parent / 'pages'
    
    if not pages_dir.exists():
        print(f"Error: {pages_dir} does not exist")
        return
    
    print("Fixing st.set_page_config() order in all pages...")
    print("=" * 60)
    
    page_files = sorted([
        f for f in pages_dir.glob('*.py') 
        if f.name != '__init__.py'
    ])
    
    stats = {
        'fixed': 0,
        'skipped': 0,
        'errors': 0
    }
    
    for page_file in page_files:
        result, info = fix_page_config_order(page_file)
        
        if result is True:
            print(f"[FIXED] {page_file.name}")
            stats['fixed'] += 1
        elif result is False:
            print(f"[SKIP] {page_file.name} - {info}")
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


