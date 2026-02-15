# -*- coding: utf-8 -*-
"""
FINAL FIX SCRIPT - Updates all pages with improved JavaScript
Run this script to update all remaining pages.
"""

import re
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent

# The improved JavaScript block (from page 2)
IMPROVED_JS = '''# Fix sidebar label: Replace "z Performance Dashboard" with "⚡ Performance Dashboard"
st.markdown("""
<script>
(function() {
    'use strict';
    
    function fixPerformanceDashboardLabel() {
        // Try multiple selectors for sidebar navigation
        const selectors = [
            '[data-testid="stSidebarNav"]',
            '[data-testid="stSidebar"] [role="navigation"]',
            '[data-testid="stSidebar"] nav'
        ];
        
        let sidebarNav = null;
        for (const selector of selectors) {
            sidebarNav = document.querySelector(selector);
            if (sidebarNav) break;
        }
        
        if (!sidebarNav) return false;
        
        const links = sidebarNav.querySelectorAll('a, [role="link"]');
        let found = false;
        
        links.forEach(link => {
            const fullText = (link.textContent || link.innerText || '').trim();
            const lowerText = fullText.toLowerCase();
            
            // Check if it matches "z Performance Dashboard" pattern
            const shouldReplace = (
                /^z\\s+performance\\s+dashboard/i.test(fullText) ||
                /^z_performance_dashboard/i.test(fullText) ||
                (lowerText.includes('performance dashboard') && (fullText.startsWith('z') || fullText.startsWith('z ')))
            );
            
            if (shouldReplace) {
                link.textContent = '⚡ Performance Dashboard';
                link.innerText = '⚡ Performance Dashboard';
                
                // Update child elements
                link.querySelectorAll('span, div, p').forEach(child => {
                    const childText = (child.textContent || child.innerText || '').trim();
                    if (childText.toLowerCase().includes('performance dashboard') && 
                        (childText.startsWith('z') || childText.startsWith('z '))) {
                        child.textContent = '⚡ Performance Dashboard';
                        child.innerText = '⚡ Performance Dashboard';
                    }
                });
                found = true;
            }
        });
        
        return found;
    }
    
    // Run immediately and on delays
    fixPerformanceDashboardLabel();
    setTimeout(fixPerformanceDashboardLabel, 100);
    setTimeout(fixPerformanceDashboardLabel, 500);
    setTimeout(fixPerformanceDashboardLabel, 1000);
    setTimeout(fixPerformanceDashboardLabel, 2000);
    setTimeout(fixPerformanceDashboardLabel, 3000);
    
    // Use MutationObserver to watch for DOM changes
    const observer = new MutationObserver(function(mutations) {
        let shouldCheck = false;
        mutations.forEach(function(mutation) {
            if (mutation.addedNodes.length > 0 || mutation.type === 'childList') {
                shouldCheck = true;
            }
        });
        if (shouldCheck) {
            setTimeout(fixPerformanceDashboardLabel, 100);
        }
    });
    
    // Observe sidebar and document
    const sidebar = document.querySelector('[data-testid="stSidebar"]');
    if (sidebar) {
        observer.observe(sidebar, { childList: true, subtree: true, characterData: true });
    }
    observer.observe(document.body, { childList: true, subtree: true });
    
    // Periodic check
    setInterval(fixPerformanceDashboardLabel, 2000);
    
    // Also run on page load events
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', fixPerformanceDashboardLabel);
    }
    window.addEventListener('load', fixPerformanceDashboardLabel);
})();
</script>
""", unsafe_allow_html=True)'''

FILES_TO_UPDATE = [
    "pages/7_📊_What-If_Scenario_Modeler.py",
    "pages/8_🎓_AI_Capabilities_Demo.py",
    "pages/8_📋_Campaign_Builder.py",
    "pages/9_🔔_Alert_Center.py",
    "pages/10_📈_Historical_Tracking.py",
    "pages/11_💰_ROI_Calculator.py",
    "pages/13_📋_Measure_Analysis.py",
    "pages/14_⭐_Star_Rating_Simulator.py",
    "pages/15_🔄_Gap_Closure_Workflow.py",
    "pages/16_🤖_ML_Gap_Closure_Predictions.py",
    "pages/17_📊_Competitive_Benchmarking.py",
    "pages/18_📋_Compliance_Reporting.py",
    "pages/18_🤖_Secure_AI_Chatbot.py",
    "pages/19_⚖️_Health_Equity_Index.py",
    "pages/z_Performance_Dashboard.py",
    "app.py",
    "pages/1_📊_ROI_by_Measure.py",
]

def update_file(filepath):
    full_path = SCRIPT_DIR / filepath
    if not full_path.exists():
        return False, "File not found"
    
    try:
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if it has the old JavaScript
        if 'fixPerformanceDashboardLabel' not in content:
            return False, "No JS fix found"
        
        # Find the old JavaScript block - look for the comment and script tag
        # Pattern: from "# Fix sidebar label" to closing script tag
        old_pattern = r'# Fix sidebar label: Replace.*?</script>""", unsafe_allow_html=True\)'
        
        if re.search(old_pattern, content, re.DOTALL):
            # Replace it
            content = re.sub(old_pattern, IMPROVED_JS, content, flags=re.DOTALL)
            
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True, "Updated successfully"
        else:
            return False, "Pattern not found - may already be updated"
            
    except Exception as e:
        return False, f"Error: {str(e)[:40]}"

if __name__ == "__main__":
    print("=" * 70)
    print("FINAL FIX SCRIPT - Updating all pages with improved JavaScript")
    print("=" * 70)
    print()
    
    updated_count = 0
    for filepath in FILES_TO_UPDATE:
        success, message = update_file(filepath)
        if success:
            updated_count += 1
            print(f"OK: {filepath}")
        else:
            print(f"SKIP: {filepath}: {message}")
    
    print()
    print("=" * 70)
    print(f"Updated {updated_count}/{len(FILES_TO_UPDATE)} files")
    print("=" * 70)
    print()
    print("NOTE: If JavaScript still doesn't work, consider renaming the file:")
    print("  z_Performance_Dashboard.py -> Performance_Dashboard.py")
    print("  (This is more reliable than JavaScript manipulation)")

