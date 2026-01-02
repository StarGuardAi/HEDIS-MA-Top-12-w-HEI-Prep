"""Fix import order in app.py - Ensure st.set_page_config() is first Streamlit command"""

import re

def fix_imports():
    import os
    print(f"Current directory: {os.getcwd()}")
    print(f"Looking for app.py in: {os.path.join(os.getcwd(), 'app.py')}")
    
    if not os.path.exists('app.py'):
        print(f"❌ app.py not found in current directory!")
        return False
    
    with open('app.py', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    print(f"✅ Loaded {len(lines)} lines from app.py")
    
    # Find all lines with imports and st.set_page_config
    import_streamlit_idx = None
    page_config_start = None
    page_config_end = None
    
    for i, line in enumerate(lines):
        # Look for actual import statement (not in comments or docstrings)
        if line.strip().startswith('import streamlit') and import_streamlit_idx is None:
            import_streamlit_idx = i
            print(f"Found streamlit import at line {i+1}: {line.strip()}")
        # Look for actual st.set_page_config call (not in comments or docstrings)
        if line.strip().startswith('st.set_page_config') and page_config_start is None:
            page_config_start = i
            print(f"Found st.set_page_config at line {i+1}: {line.strip()[:50]}")
        if page_config_start is not None and page_config_end is None:
            # Find the closing parenthesis
            if line.strip().endswith(')'):
                # Check if this completes the function call
                paren_count = line.count('(') - line.count(')')
                if paren_count <= 0:
                    page_config_end = i + 1
                    break
    
    if import_streamlit_idx is None:
        print("❌ Could not find 'import streamlit as st'")
        return False
    
    if page_config_start is None or page_config_end is None:
        print("❌ Could not find st.set_page_config()")
        return False
    
    # Check if page_config is already right after streamlit import
    if page_config_start == import_streamlit_idx + 1:
        print("✅ Import order is already correct!")
        print(f"   - streamlit import at line {import_streamlit_idx + 1}")
        print(f"   - st.set_page_config() at line {page_config_start + 1}")
        return True
    
    # Extract page_config block
    page_config_block = lines[page_config_start:page_config_end]
    
    # Remove page_config from current location
    del lines[page_config_start:page_config_end]
    
    # Adjust import_streamlit_idx if page_config was before it
    if page_config_start < import_streamlit_idx:
        import_streamlit_idx -= len(page_config_block)
    
    # Insert page_config right after streamlit import
    insert_at = import_streamlit_idx + 1
    
    # Add blank line and comment before page_config
    lines.insert(insert_at, '\n')
    lines.insert(insert_at + 1, '# ============================================================================\n')
    lines.insert(insert_at + 2, '# STEP 3: PAGE CONFIG - MUST BE FIRST STREAMLIT COMMAND\n')
    lines.insert(insert_at + 3, '# ============================================================================\n')
    
    # Insert page_config block
    for j, config_line in enumerate(page_config_block):
        lines.insert(insert_at + 4 + j, config_line)
    
    # Write back
    with open('app.py', 'w', encoding='utf-8') as f:
        f.writelines(lines)
    
    print("✅ Fixed! st.set_page_config() moved to correct position")
    print(f"   - streamlit import at line {import_streamlit_idx + 1}")
    print(f"   - st.set_page_config() now at line {insert_at + 5}")
    return True

if __name__ == "__main__":
    fix_imports()

