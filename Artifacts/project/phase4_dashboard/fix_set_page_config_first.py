"""
Fix st.set_page_config() to be the first Streamlit command
Simple approach: find it and move it right after imports
"""
import os
import sys
import re
from pathlib import Path

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

def fix_set_page_config_first(file_path):
    """Move st.set_page_config() to be the first Streamlit command"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        original_lines = lines.copy()
        
        # Find st.set_page_config() block
        page_config_start = -1
        page_config_end = -1
        
        for i, line in enumerate(lines):
            if 'st.set_page_config' in line:
                page_config_start = i
                # Find where it ends (multiline)
                paren_count = 0
                for j in range(i, len(lines)):
                    paren_count += lines[j].count('(') - lines[j].count(')')
                    if paren_count == 0 and ')' in lines[j]:
                        page_config_end = j
                        break
                break
        
        if page_config_start == -1:
            return False, "No st.set_page_config() found"
        
        # Extract the page_config block
        page_config_block = lines[page_config_start:page_config_end + 1]
        
        # Check if there are any st.* calls before it
        has_st_before = False
        for i in range(page_config_start):
            if 'st.' in lines[i] and 'st.set_page_config' not in lines[i]:
                has_st_before = True
                break
        
        if not has_st_before:
            return False, "Already correct order"
        
        # Find where to insert (after last import, before first st.*)
        insert_pos = 0
        for i in range(len(lines)):
            stripped = lines[i].strip()
            # Skip comments and docstrings
            if stripped.startswith('#') or stripped.startswith('"""') or stripped.startswith("'''"):
                continue
            # Stop at first st.* command
            if 'st.' in stripped and 'st.set_page_config' not in stripped:
                insert_pos = i
                break
            # Also track last import
            if 'import' in stripped or 'from' in stripped:
                insert_pos = i + 1
        
        # Remove page_config from original location
        new_lines = (
            lines[:page_config_start] + 
            lines[page_config_end + 1:]
        )
        
        # Insert page_config at the right position
        new_lines = (
            new_lines[:insert_pos] + 
            [''] +  # blank line
            page_config_block +
            [''] +  # blank line
            new_lines[insert_pos:]
        )
        
        new_content = ''.join(new_lines)
        
        # Verify it's correct
        first_st_pos = new_content.find('st.')
        if first_st_pos != -1:
            if 'st.set_page_config' not in new_content[:first_st_pos + 50]:
                return False, "Verification failed"
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        return True, "Fixed"
            
    except Exception as e:
        return None, str(e)

def main():
    """Process all page files"""
    pages_dir = Path(__file__).parent / 'pages'
    
    if not pages_dir.exists():
        print(f"Error: {pages_dir} does not exist")
        return
    
    print("Moving st.set_page_config() to be first Streamlit command...")
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
        result, info = fix_set_page_config_first(page_file)
        
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


