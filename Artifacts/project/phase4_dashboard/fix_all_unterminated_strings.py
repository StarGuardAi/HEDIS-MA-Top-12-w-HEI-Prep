"""
Fix all pages with unterminated triple-quoted string literals
Adds closing tags and header HTML to all pages that need it
"""
import os
import sys
from pathlib import Path

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# Template for closing CSS and header HTML
CLOSING_TEMPLATE = '''

</style>
""", unsafe_allow_html=True)

# StarGuard Header HTML (CSS already defined above)
st.markdown("""
<div class='starguard-header-container'>
    <div class='starguard-title'>⭐ StarGuard AI | Turning Data Into Stars</div>
    <div class='starguard-subtitle'>Powered by Predictive Analytics & Machine Learning | Healthcare AI Architect | $148M+ Savings in HEDIS & Star Ratings | Context Engineering + Agentic RAG</div>
</div>
""", unsafe_allow_html=True)
'''

def fix_unterminated_string(file_path):
    """Fix unterminated triple-quoted string in a page file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if file ends with just } without closing tags
        lines = content.split('\n')
        
        # Find the last non-empty line
        last_non_empty = -1
        for i in range(len(lines) - 1, -1, -1):
            if lines[i].strip():
                last_non_empty = i
                break
        
        if last_non_empty == -1:
            return False, "File is empty"
        
        last_line = lines[last_non_empty].strip()
        
        # Check if it ends with just } (indicating unterminated CSS)
        if last_line == '}' and '</style>' not in content:
            # Check if there's a st.markdown(""" at the start
            if 'st.markdown("""' in content and '""", unsafe_allow_html=True)' not in content[-500:]:
                # Add closing template
                new_content = content.rstrip() + CLOSING_TEMPLATE
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                return True, "Fixed"
            else:
                return False, "Already has closing tags"
        else:
            return False, "No issue detected"
            
    except Exception as e:
        return None, str(e)

def main():
    """Process all page files"""
    pages_dir = Path(__file__).parent / 'pages'
    
    if not pages_dir.exists():
        print(f"Error: {pages_dir} does not exist")
        return
    
    print("Fixing unterminated triple-quoted strings in all pages...")
    print("=" * 60)
    
    # Exclude already fixed files
    excluded_files = ['1_📊_ROI_by_Measure.py', '2_💰_Cost_Per_Closure.py']
    
    page_files = sorted([
        f for f in pages_dir.glob('*.py') 
        if f.name != '__init__.py' and f.name not in excluded_files
    ])
    
    stats = {
        'fixed': 0,
        'skipped': 0,
        'errors': 0
    }
    
    for page_file in page_files:
        result, info = fix_unterminated_string(page_file)
        
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


