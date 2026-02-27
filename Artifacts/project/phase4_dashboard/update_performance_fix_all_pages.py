# -*- coding: utf-8 -*-
"""Update all pages with improved Performance Dashboard JavaScript fix"""

import re
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent

FILES = [
    "app.py",
    "pages/1_📊_ROI_by_Measure.py",
    "pages/3_📈_Monthly_Trend.py",
    "pages/4_💵_Budget_Variance.py",
    "pages/5_🎯_Cost_Tier_Comparison.py",
    "pages/6_🤖_AI_Executive_Insights.py",
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
]

# Old JavaScript pattern (flexible matching)
OLD_JS_PATTERN = r'# Fix sidebar label: Replace.*?</script>"""'

# New improved JavaScript
NEW_JS = '''# Fix sidebar label: Replace "z Performance Dashboard" with "⚡ Performance Dashboard"
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

def update_file(file_path):
    """Update JavaScript fix in a file."""
    full_path = SCRIPT_DIR / file_path
    
    if not full_path.exists():
        return (False, "File not found")
    
    try:
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if old pattern exists
        if 'fixPerformanceDashboardLabel' not in content:
            return (False, "No fix found")
        
        # Replace the old JavaScript block with new one
        # Match from "# Fix sidebar label" to closing script tag
        pattern = r'(# Fix sidebar label: Replace.*?<script>.*?</script>""", unsafe_allow_html=True)'
        
        if re.search(pattern, content, re.DOTALL):
            content = re.sub(pattern, NEW_JS, content, flags=re.DOTALL)
            
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return (True, "Updated")
        else:
            return (False, "Pattern not found")
            
    except Exception as e:
        return (False, str(e))

def main():
    print("Updating Performance Dashboard JavaScript fix in all pages...")
    print("=" * 70)
    
    results = []
    for file_path in FILES:
        success, message = update_file(file_path)
        status = "OK" if success else "SKIP"
        print(f"{status:4} {file_path}: {message}")
        results.append((file_path, success, message))
    
    print("=" * 70)
    successful = sum(1 for _, s, _ in results if s)
    print(f"Updated: {successful}/{len(FILES)} files")
    print("=" * 70)

if __name__ == "__main__":
    main()

