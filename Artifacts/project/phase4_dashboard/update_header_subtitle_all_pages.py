"""
Update StarGuard header subtitle text on all pages
Replace with new two-line version focused on recruiter/hiring manager appeal
"""
import os
import sys
from pathlib import Path
import re

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

OLD_SUBTITLE_PATTERNS = [
    r'Powered by Predictive Analytics & Machine Learning \| Healthcare AI Architect \| \$148M\+ Savings in HEDIS & Star Ratings \| Context Engineering \+ Agentic RAG \| Production-Grade Analytics for Medicare Advantage Star Rating Optimization \| Zero PHI Exposure \| HIPAA-Compliant Architecture',
    r'Powered by Predictive Analytics.*?HIPAA-Compliant Architecture',
]

NEW_SUBTITLE = 'Healthcare AI Architect • $148M+ Documented Savings • HEDIS & Star Rating Expert<br>🔒 Zero PHI Exposure • Context Engineering + Agentic RAG • Production-Grade Analytics'

def update_subtitle(file_path):
    """Update subtitle text in a file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Find the subtitle div
    subtitle_pattern = r"(<div class='starguard-subtitle'>)(.*?)(</div>)"
    
    def replace_subtitle(match):
        opening_tag = match.group(1)
        old_content = match.group(2)
        closing_tag = match.group(3)
        
        # Replace the content, keeping the tags
        return opening_tag + NEW_SUBTITLE + closing_tag
    
    new_content = re.sub(subtitle_pattern, replace_subtitle, content, flags=re.DOTALL)
    
    if new_content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True, "Updated subtitle"
    
    return False, "Subtitle not found or already updated"

def main():
    """Update subtitle on all pages"""
    base_dir = Path(__file__).parent
    app_file = base_dir / 'app.py'
    pages_dir = base_dir / 'pages'
    
    print("Updating StarGuard header subtitle on all pages...")
    print("=" * 60)
    
    files_to_update = [app_file] + list(pages_dir.glob('*.py'))
    
    stats = {'updated': 0, 'skipped': 0, 'errors': 0}
    
    for file_path in files_to_update:
        if not file_path.exists():
            continue
        
        file_name = file_path.name
        
        try:
            result, info = update_subtitle(file_path)
            
            if result:
                print(f"[UPDATED] {file_name} - {info}")
                stats['updated'] += 1
            else:
                if "not found" in info.lower():
                    stats['skipped'] += 1
                else:
                    print(f"[SKIP] {file_name} - {info}")
                    stats['skipped'] += 1
        except Exception as e:
            print(f"[ERROR] {file_name} - {str(e)}")
            stats['errors'] += 1
    
    print("=" * 60)
    print(f"[SUMMARY] Updated: {stats['updated']}, Skipped: {stats['skipped']}, Errors: {stats['errors']}")

if __name__ == '__main__':
    main()


