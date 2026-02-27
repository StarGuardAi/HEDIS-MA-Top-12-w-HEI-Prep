"""
Apply Home Page Fixes to All Pages:
1. Add StarGuard header HTML
2. Update padding-top to 1rem
3. Add Performance Dashboard emoji JavaScript fix
"""
import os
import sys
import re
from pathlib import Path

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# StarGuard Header HTML
STARGUARD_HEADER = """
# StarGuard Header HTML (CSS already defined in Nuclear Option above)
st.markdown(\"\"\"
<div class='starguard-header-container'>
    <div class='starguard-title'>⭐ StarGuard AI | Turning Data Into Stars</div>
    <div class='starguard-subtitle'>Powered by Predictive Analytics & Machine Learning | Healthcare AI Architect | $148M+ Savings in HEDIS & Star Ratings | Context Engineering + Agentic RAG</div>
</div>
\"\"\", unsafe_allow_html=True)

st.markdown("---")
"""

# Performance Dashboard Emoji JavaScript Fix
PERFORMANCE_DASHBOARD_JS = """
# ============================================================================
# ADDITIONAL JAVASCRIPT FIX FOR PERFORMANCE DASHBOARD EMOJI
# ============================================================================
st.markdown(\"\"\"
<script>
// Fix Performance Dashboard emoji rendering - Enhanced version
(function() {
    'use strict';
    
    function fixPerformanceDashboardEmoji() {
        // Find all sidebar links
        const sidebarLinks = document.querySelectorAll('[data-testid="stSidebarNav"] a');
        
        sidebarLinks.forEach(link => {
            const href = link.getAttribute('href') || '';
            const text = (link.textContent || link.innerText || '').trim();
            
            // Check if this is the Performance Dashboard link (by href - most reliable)
            const isPerformanceDashboard = (
                href.includes('Performance_Dashboard') ||
                href.includes('Performance-Dashboard') ||
                href.toLowerCase().includes('performance') && href.toLowerCase().includes('dashboard')
            );
            
            // Also check by text as backup
            const textMatches = (
                text === 'Performance Dashboard' ||
                text.includes('Performance Dashboard') ||
                text.match(/Performance\\s*Dashboard/i)
            );
            
            const hasEmoji = text.includes('⚡') || text.includes('\\u26A1') || link.innerHTML.includes('⚡');
            
            // If it's Performance Dashboard but missing emoji, add it
            if ((isPerformanceDashboard || textMatches) && !hasEmoji) {
                // Method 1: Clear and rebuild the entire link content
                const originalHTML = link.innerHTML;
                
                // Try to preserve any icons/spans but update text
                if (link.querySelector('span, div')) {
                    // Has child elements - update them
                    const children = link.querySelectorAll('span, div, p');
                    children.forEach(child => {
                        const childText = (child.textContent || child.innerText || '').trim();
                        if (childText === 'Performance Dashboard' || childText.includes('Performance Dashboard')) {
                            child.textContent = '⚡ Performance Dashboard';
                            child.innerText = '⚡ Performance Dashboard';
                        }
                    });
                } else {
                    // No children - replace entire content
                    link.textContent = '⚡ Performance Dashboard';
                    link.innerText = '⚡ Performance Dashboard';
                }
                
                // Method 2: Use innerHTML as backup
                if (!link.textContent.includes('⚡')) {
                    link.innerHTML = '⚡ Performance Dashboard';
                }
                
                // Method 3: Create a new text node
                const newText = document.createTextNode('⚡ Performance Dashboard');
                if (link.childNodes.length === 0 || !link.textContent.includes('⚡')) {
                    link.innerHTML = '';
                    link.appendChild(newText);
                }
                
                // Force proper font rendering
                link.style.fontFamily = '-apple-system, BlinkMacSystemFont, "Segoe UI Emoji", "Segoe UI", sans-serif';
                link.style.whiteSpace = 'normal';
                
                // Add data attribute to mark as fixed
                link.setAttribute('data-emoji-fixed', 'true');
            }
        });
    }
    
    // Run immediately
    fixPerformanceDashboardEmoji();
    
    // Run on DOM changes (Streamlit reruns)
    const observer = new MutationObserver(function() {
        fixPerformanceDashboardEmoji();
    });
    
    observer.observe(document.body, {
        childList: true,
        subtree: true,
        characterData: true
    });
    
    // Also run after delays to catch late-rendering elements
    setTimeout(fixPerformanceDashboardEmoji, 50);
    setTimeout(fixPerformanceDashboardEmoji, 100);
    setTimeout(fixPerformanceDashboardEmoji, 300);
    setTimeout(fixPerformanceDashboardEmoji, 500);
    setTimeout(fixPerformanceDashboardEmoji, 1000);
    setTimeout(fixPerformanceDashboardEmoji, 2000);
    setTimeout(fixPerformanceDashboardEmoji, 3000);
    
    // Periodic check as backup (every 2 seconds)
    setInterval(fixPerformanceDashboardEmoji, 2000);
    
    // Also run when page becomes visible (user switches tabs back)
    document.addEventListener('visibilitychange', function() {
        if (!document.hidden) {
            setTimeout(fixPerformanceDashboardEmoji, 100);
        }
    });
})();
</script>
\"\"\", unsafe_allow_html=True)
"""

def update_padding_top(content):
    """Update padding-top from 0rem to 1rem"""
    # Pattern 1: .main .block-container { padding-top: 0rem
    content = re.sub(
        r'(\.main\s+\.block-container\s*\{[^}]*?padding-top:\s*)0rem',
        r'\g<1>1rem',
        content,
        flags=re.DOTALL
    )
    
    # Pattern 2: .block-container { padding-top: 0rem
    content = re.sub(
        r'(\.block-container\s*\{[^}]*?padding-top:\s*)0rem',
        r'\g<1>1rem',
        content,
        flags=re.DOTALL
    )
    
    # Pattern 3: .main > div:first-child { padding-top: 0
    content = re.sub(
        r'(\.main\s*>\s*div:first-child\s*\{[^}]*?padding-top:\s*)0\s*!important',
        r'\g<1>1rem !important',
        content,
        flags=re.DOTALL
    )
    
    return content

def add_starguard_header(content):
    """Add StarGuard header HTML after imports and before main content"""
    # Check if header already exists
    if 'starguard-header-container' in content:
        return content, False
    
    # Find a good insertion point - after st.set_page_config and CSS blocks
    # Look for pattern: after closing </style> tag, before imports or main code
    
    lines = content.split('\n')
    new_lines = []
    i = 0
    inserted = False
    
    while i < len(lines):
        line = lines[i]
        new_lines.append(line)
        
        # Look for closing </style> tag followed by imports or main code
        if line.strip() == '</style>' and not inserted:
            # Check if next non-empty line is import or main code
            j = i + 1
            while j < len(lines) and lines[j].strip() == '':
                j += 1
            
            if j < len(lines):
                next_line = lines[j].strip()
                # If next line is import or starts main code, insert header here
                if (next_line.startswith('import ') or 
                    next_line.startswith('from ') or
                    next_line.startswith('# ') or
                    next_line.startswith('st.') or
                    next_line.startswith('def ') or
                    next_line.startswith('class ')):
                    # Insert header after this </style> block
                    new_lines.append('')
                    new_lines.append(STARGUARD_HEADER.strip())
                    inserted = True
        
        i += 1
    
    # If not inserted yet, try to insert after first CSS block
    if not inserted:
        for i, line in enumerate(new_lines):
            if '</style>' in line and 'unsafe_allow_html=True' in new_lines[min(i+1, len(new_lines)-1)]:
                # Insert after this CSS block
                insert_pos = i + 2
                new_lines.insert(insert_pos, '')
                new_lines.insert(insert_pos + 1, STARGUARD_HEADER.strip())
                inserted = True
                break
    
    return '\n'.join(new_lines), inserted

def add_performance_dashboard_js(content):
    """Add Performance Dashboard emoji JavaScript fix"""
    # Check if JS already exists
    if 'fixPerformanceDashboardEmoji' in content:
        return content, False
    
    # Find insertion point - before footer or at end of file
    # Look for footer functions or end of file
    
    lines = content.split('\n')
    new_lines = []
    i = 0
    inserted = False
    
    # Try to find before footer functions
    while i < len(lines):
        line = lines[i]
        
        # Look for footer or end of main code
        if (('render_page_footer' in line or 
             'add_page_footer' in line or
             'render_footer' in line) and not inserted):
            # Insert JS before footer
            new_lines.append('')
            new_lines.append(PERFORMANCE_DASHBOARD_JS.strip())
            new_lines.append('')
            inserted = True
        
        new_lines.append(line)
        i += 1
    
    # If not inserted, add at end
    if not inserted:
        new_lines.append('')
        new_lines.append(PERFORMANCE_DASHBOARD_JS.strip())
        inserted = True
    
    return '\n'.join(new_lines), inserted

def process_file(file_path):
    """Process a single page file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        changes = []
        
        # 1. Update padding-top
        content = update_padding_top(content)
        if content != original_content:
            changes.append('padding-top')
        
        # 2. Add StarGuard header
        content, header_added = add_starguard_header(content)
        if header_added:
            changes.append('header')
        
        # 3. Add Performance Dashboard JS
        content, js_added = add_performance_dashboard_js(content)
        if js_added:
            changes.append('js')
        
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
    
    print("Applying Home Page Fixes to All Pages...")
    print("=" * 60)
    print("Fixes:")
    print("  1. Add StarGuard header HTML")
    print("  2. Update padding-top: 0rem -> 1rem")
    print("  3. Add Performance Dashboard emoji JavaScript fix")
    print("=" * 60)
    
    page_files = sorted([f for f in pages_dir.glob('*.py') if f.name != '__init__.py'])
    
    stats = {
        'header': 0,
        'padding': 0,
        'js': 0,
        'errors': 0,
        'skipped': 0
    }
    
    for page_file in page_files:
        result, info = process_file(page_file)
        
        if result is True:
            changes = ', '.join(info)
            print(f"[OK] {page_file.name}")
            print(f"     Changes: {changes}")
            if 'header' in info:
                stats['header'] += 1
            if 'padding' in info:
                stats['padding'] += 1
            if 'js' in info:
                stats['js'] += 1
        elif result is False:
            print(f"[SKIP] {page_file.name} - No changes needed")
            stats['skipped'] += 1
        else:
            print(f"[ERROR] {page_file.name} - {info}")
            stats['errors'] += 1
    
    print("=" * 60)
    print(f"[SUMMARY]")
    print(f"  Headers added: {stats['header']}")
    print(f"  Padding updated: {stats['padding']}")
    print(f"  JS fixes added: {stats['js']}")
    print(f"  Skipped: {stats['skipped']}")
    print(f"  Errors: {stats['errors']}")
    print(f"  Total: {len(page_files)} files")

if __name__ == '__main__':
    main()

