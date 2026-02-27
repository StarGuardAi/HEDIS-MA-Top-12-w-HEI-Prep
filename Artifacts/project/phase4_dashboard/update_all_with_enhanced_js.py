# -*- coding: utf-8 -*-
"""Update all pages with enhanced JavaScript that ensures ⚡ Performance Dashboard"""

import re
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent

# Enhanced JavaScript that ensures "⚡ Performance Dashboard" is ALWAYS shown
ENHANCED_JS = '''# Fix sidebar label: Ensure "⚡ Performance Dashboard" is always shown
st.markdown("""
<script>
(function() {
    'use strict';
    
    function fixPerformanceDashboardLabel() {
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
            
            // Check if it's Performance Dashboard - ensure it ALWAYS shows "⚡ Performance Dashboard"
            const shouldReplace = (
                /performance\s*dashboard/i.test(fullText) &&
                !/^⚡\s*performance\s*dashboard/i.test(fullText)
            );
            
            if (shouldReplace || lowerText.includes('performance dashboard')) {
                link.textContent = '⚡ Performance Dashboard';
                link.innerText = '⚡ Performance Dashboard';
                
                link.querySelectorAll('span, div, p').forEach(child => {
                    const childText = (child.textContent || child.innerText || '').trim();
                    if (childText.toLowerCase().includes('performance dashboard')) {
                        child.textContent = '⚡ Performance Dashboard';
                        child.innerText = '⚡ Performance Dashboard';
                    }
                });
                found = true;
            }
        });
        
        return found;
    }
    
    fixPerformanceDashboardLabel();
    setTimeout(fixPerformanceDashboardLabel, 100);
    setTimeout(fixPerformanceDashboardLabel, 500);
    setTimeout(fixPerformanceDashboardLabel, 1000);
    setTimeout(fixPerformanceDashboardLabel, 2000);
    setTimeout(fixPerformanceDashboardLabel, 3000);
    
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
    
    const sidebar = document.querySelector('[data-testid="stSidebar"]');
    if (sidebar) {
        observer.observe(sidebar, { childList: true, subtree: true, characterData: true });
    }
    observer.observe(document.body, { childList: true, subtree: true });
    
    setInterval(fixPerformanceDashboardLabel, 2000);
    
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', fixPerformanceDashboardLabel);
    }
    window.addEventListener('load', fixPerformanceDashboardLabel);
})();
</script>
""", unsafe_allow_html=True)'''

FILES = [
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
    "app.py",
    "pages/1_📊_ROI_by_Measure.py",
]

def update_file(filepath):
    full_path = SCRIPT_DIR / filepath
    if not full_path.exists():
        return False, "Not found"
    
    try:
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if 'fixPerformanceDashboardLabel' not in content:
            return False, "No JS found"
        
        # Replace the JavaScript block
        pattern = r'# Fix sidebar label: Replace.*?</script>""", unsafe_allow_html=True\)'
        if re.search(pattern, content, re.DOTALL):
            content = re.sub(pattern, ENHANCED_JS, content, flags=re.DOTALL)
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True, "Updated"
        return False, "Pattern not found"
    except Exception as e:
        return False, str(e)[:30]

if __name__ == "__main__":
    print("Updating all pages with enhanced JavaScript...")
    updated = 0
    for filepath in FILES:
        success, msg = update_file(filepath)
        if success:
            updated += 1
            print(f"OK: {filepath}")
        else:
            print(f"SKIP: {filepath}")
    print(f"\nUpdated {updated}/{len(FILES)} files")

