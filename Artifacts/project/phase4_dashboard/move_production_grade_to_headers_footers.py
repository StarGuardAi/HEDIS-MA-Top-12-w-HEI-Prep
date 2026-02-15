"""
Move Production-Grade Analytics text from home page to all page headers/footers
Remove from home page and blend into headers/footers for recruiter/hiring manager visibility
"""
import os
import sys
from pathlib import Path
import re

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

PRODUCTION_TEXT = "Production-Grade Analytics for Medicare Advantage Star Rating Optimization | Zero PHI Exposure | HIPAA-Compliant Architecture"

def remove_from_home_page(file_path):
    """Remove production-grade text from home page"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove the line
    old_line = 'st.markdown(\'<div style="text-align: center; margin: 0.5rem 0; font-size: 1rem; color: #666;">Production-Grade Analytics for Medicare Advantage Star Rating Optimization | Zero PHI Exposure | HIPAA-Compliant Architecture</div>\', unsafe_allow_html=True)'
    
    if old_line in content:
        content = content.replace(old_line + '\n\n', '')
        content = content.replace(old_line + '\n', '')
        content = content.replace(old_line, '')
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True, "Removed from home page"
    
    return False, "Not found in home page"

def add_to_page_header(file_path):
    """Add production-grade text to page header subtitle"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the starguard-subtitle section
    subtitle_pattern = r"<div class='starguard-subtitle'>.*?</div>"
    
    if re.search(subtitle_pattern, content, re.DOTALL):
        # Check if already added
        if PRODUCTION_TEXT in content:
            return False, "Already added"
        
        # Find and update subtitle
        def update_subtitle(match):
            subtitle_content = match.group(0)
            # Extract current content
            current_text = re.search(r'>([^<]+)<', subtitle_content)
            if current_text:
                current = current_text.group(1)
                # Add production text
                new_content = f"{current} | {PRODUCTION_TEXT}"
                return subtitle_content.replace(current, new_content)
            return subtitle_content
        
        new_content = re.sub(subtitle_pattern, update_subtitle, content, flags=re.DOTALL)
        
        if new_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return True, "Added to header subtitle"
    
    return False, "Header subtitle not found"

def add_to_footer(file_path):
    """Add production-grade text to footer"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if already added
    if PRODUCTION_TEXT in content and 'footer' in content.lower():
        return False, "Already in footer"
    
    # Find footer section
    footer_patterns = [
        r"# Footer.*?© 2024-2026",
        r"<div style='text-align: center; padding: 1.5rem.*?© 2024-2026",
    ]
    
    for pattern in footer_patterns:
        match = re.search(pattern, content, re.DOTALL)
        if match:
            footer_start = match.start()
            # Find where to insert (before copyright)
            insert_pos = content.rfind("© 2024-2026", footer_start)
            if insert_pos > 0:
                # Insert before copyright
                production_html = f"""
    <div style='background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%); border-left: 4px solid #2196f3; padding: 10px 16px; margin: 12px auto; max-width: 1200px; text-align: center; border-radius: 6px;'>
        <p style='color: #1565c0; font-size: 0.9rem; line-height: 1.4; margin: 0; font-weight: 600;'><strong>🏆 {PRODUCTION_TEXT}</strong></p>
    </div>
"""
                new_content = content[:insert_pos] + production_html + content[insert_pos:]
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                return True, "Added to footer"
    
    return False, "Footer not found"

def main():
    """Process all files"""
    base_dir = Path(__file__).parent
    app_file = base_dir / 'app.py'
    pages_dir = base_dir / 'pages'
    
    print("Moving Production-Grade Analytics text to headers/footers...")
    print("=" * 60)
    
    # Step 1: Remove from home page
    print("\n[STEP 1] Removing from home page...")
    result, info = remove_from_home_page(app_file)
    if result:
        print(f"[SUCCESS] Home page - {info}")
    else:
        print(f"[SKIP] Home page - {info}")
    
    # Step 2: Add to all page headers (blend into subtitle)
    print("\n[STEP 2] Adding to page headers (blended into subtitle)...")
    page_files = list(pages_dir.glob('*.py'))
    
    header_stats = {'added': 0, 'skipped': 0, 'errors': 0}
    footer_stats = {'added': 0, 'skipped': 0, 'errors': 0}
    
    for page_file in page_files:
        page_name = page_file.name
        
        # Try adding to header first
        result, info = add_to_page_header(page_file)
        if result:
            print(f"[HEADER] {page_name} - {info}")
            header_stats['added'] += 1
        elif "Already added" in info:
            header_stats['skipped'] += 1
        elif "Header subtitle not found" in info:
            # If header not found, try footer
            result2, info2 = add_to_footer(page_file)
            if result2:
                print(f"[FOOTER] {page_name} - {info2}")
                footer_stats['added'] += 1
            else:
                print(f"[SKIP] {page_name} - {info2}")
                footer_stats['skipped'] += 1
        else:
            print(f"[ERROR] {page_name} - {info}")
            header_stats['errors'] += 1
    
    print("\n" + "=" * 60)
    print("[SUMMARY]")
    print(f"  Removed from home page: {'Yes' if result else 'No'}")
    print(f"  Added to headers: {header_stats['added']}")
    print(f"  Added to footers: {footer_stats['added']}")
    print(f"  Skipped: {header_stats['skipped'] + footer_stats['skipped']}")
    print(f"  Errors: {header_stats['errors']}")

if __name__ == '__main__':
    main()


