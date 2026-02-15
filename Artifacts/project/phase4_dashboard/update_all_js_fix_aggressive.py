# -*- coding: utf-8 -*-
"""Aggressive JavaScript fix update for all pages"""

import re
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent

# SUPER AGGRESSIVE JavaScript fix
AGGRESSIVE_JS = """'use strict';

    // Ultra-aggressive fix that runs continuously
    function fixPerformanceDashboardLabel() {
        // Try ALL possible selectors
        const allSelectors = [
            '[data-testid="stSidebarNav"]',
            '[data-testid="stSidebar"] [role="navigation"]',
            '[data-testid="stSidebar"] nav',
            '[data-testid="stSidebar"] a',
            'nav a',
            '.css-1d391kg a',
            '[role="navigation"] a'
        ];
        
        let foundAny = false;
        
        for (const baseSelector of allSelectors) {
            const elements = document.querySelectorAll(baseSelector);
            elements.forEach(element => {
                const text = (element.textContent || element.innerText || '').trim();
                const lowerText = text.toLowerCase();
                
                // Check ALL possible patterns
                const patterns = [
                    /^z\s*performance\s*dashboard/i,
                    /^z_performance_dashboard/i,
                    /^z\s+performance/i,
                    /performance\s*dashboard.*^z/i
                ];
                
                let shouldFix = false;
                for (const pattern of patterns) {
                    if (pattern.test(text)) {
                        shouldFix = true;
                        break;
                    }
                }
                
                // Also check if starts with 'z' and contains 'performance'
                if (!shouldFix && lowerText.includes('performance') && (text.startsWith('z') || text.startsWith('z '))) {
                    shouldFix = true;
                }
                
                if (shouldFix) {
                    element.textContent = '⚡ Performance Dashboard';
                    element.innerText = '⚡ Performance Dashboard';
                    
                    // Fix all children
                    element.querySelectorAll('*').forEach(child => {
                        const childText = (child.textContent || child.innerText || '').trim();
                        if (childText.toLowerCase().includes('performance') && childText.startsWith('z')) {
                            child.textContent = '⚡ Performance Dashboard';
                            child.innerText = '⚡ Performance Dashboard';
                        }
                    });
                    
                    foundAny = true;
                }
            });
        }
        
        return foundAny;
    }
    
    // Run IMMEDIATELY
    fixPerformanceDashboardLabel();
    
    // Run on multiple events
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', fixPerformanceDashboardLabel);
    } else {
        fixPerformanceDashboardLabel();
    }
    
    window.addEventListener('load', fixPerformanceDashboardLabel);
    window.addEventListener('DOMContentLoaded', fixPerformanceDashboardLabel);
    
    // Run VERY frequently
    setTimeout(fixPerformanceDashboardLabel, 50);
    setTimeout(fixPerformanceDashboardLabel, 100);
    setTimeout(fixPerformanceDashboardLabel, 200);
    setTimeout(fixPerformanceDashboardLabel, 500);
    setTimeout(fixPerformanceDashboardLabel, 1000);
    setTimeout(fixPerformanceDashboardLabel, 2000);
    setTimeout(fixPerformanceDashboardLabel, 3000);
    setTimeout(fixPerformanceDashboardLabel, 5000);
    
    // MutationObserver - watch EVERYTHING
    const observer = new MutationObserver(function(mutations) {
        fixPerformanceDashboardLabel();
    });
    
    // Observe sidebar
    const sidebar = document.querySelector('[data-testid="stSidebar"]');
    if (sidebar) {
        observer.observe(sidebar, {
            childList: true,
            subtree: true,
            characterData: true,
            attributes: true,
            attributeOldValue: true
        });
    }
    
    // Observe entire document
    observer.observe(document.body, {
        childList: true,
        subtree: true,
        characterData: true
    });
    
    // Observe navigation specifically
    const nav = document.querySelector('[data-testid="stSidebarNav"]');
    if (nav) {
        observer.observe(nav, {
            childList: true,
            subtree: true,
            characterData: true
        });
    }
    
    // Continuous checking every 500ms
    setInterval(fixPerformanceDashboardLabel, 500);
    
    // Also check on any click (sidebar might update)
    document.addEventListener('click', function() {
        setTimeout(fixPerformanceDashboardLabel, 100);
    }, true);
    
    // Check on navigation
    window.addEventListener('popstate', fixPerformanceDashboardLabel);
    window.addEventListener('pushstate', fixPerformanceDashboardLabel);
    
    // Override textContent setter if possible
    const originalTextContent = Object.getOwnPropertyDescriptor(Node.prototype, 'textContent');
    if (originalTextContent && originalTextContent.set) {
        Object.defineProperty(Node.prototype, 'textContent', {
            set: function(value) {
                if (typeof value === 'string' && /^z\s*performance/i.test(value.trim())) {
                    value = '⚡ Performance Dashboard';
                }
                originalTextContent.set.call(this, value);
                setTimeout(fixPerformanceDashboardLabel, 10);
            },
            get: originalTextContent.get,
            configurable: true
        });
    }"""

FILES = [
    "app.py",
    "pages/1_📊_ROI_by_Measure.py",
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

def update_file(filepath):
    full_path = SCRIPT_DIR / filepath
    if not full_path.exists():
        return False, "Not found"
    
    try:
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if 'fixPerformanceDashboardLabel' not in content:
            return False, "No fix found"
        
        # Find and replace the JavaScript function
        # Pattern: from (function() { to })();
        pattern = r'\(function\(\) \{[^}]*?function fixPerformanceDashboardLabel\(\)[^}]*?\}[^}]*?\}\)\(\);'
        
        # More flexible pattern
        old_pattern = r'\(function\(\) \{[\s\S]*?function fixPerformanceDashboardLabel\(\)[\s\S]*?setInterval\(fixPerformanceDashboardLabel[^;]*\);[\s\S]*?\}\)\(\);'
        
        new_js_block = f"""(function() {{
{AGGRESSIVE_JS}
}})();"""
        
        if re.search(old_pattern, content):
            content = re.sub(old_pattern, new_js_block, content, flags=re.DOTALL)
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True, "Updated"
        else:
            # Try finding just the function
            func_pattern = r'function fixPerformanceDashboardLabel\(\)[\s\S]*?setInterval\(fixPerformanceDashboardLabel[^;]*\);'
            if re.search(func_pattern, content):
                # Replace function and calls
                replacement = f"""function fixPerformanceDashboardLabel() {{
        {AGGRESSIVE_JS}
    }}"""
                content = re.sub(func_pattern, replacement, content, flags=re.DOTALL)
                with open(full_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                return True, "Updated (function only)"
            return False, "Pattern not found"
            
    except Exception as e:
        return False, str(e)[:50]

if __name__ == "__main__":
    print("Updating all files with AGGRESSIVE JavaScript fix...")
    print("=" * 70)
    
    updated = 0
    for filepath in FILES:
        success, msg = update_file(filepath)
        status = "OK" if success else "SKIP"
        try:
            print(f"{status:4} {filepath}: {msg}")
        except:
            print(f"{status:4} {filepath[:50]}: {msg}")
        if success:
            updated += 1
    
    print("=" * 70)
    print(f"Updated {updated}/{len(FILES)} files")
    print("=" * 70)
    print("\nNOTE: Also updating pages 2-5 with this aggressive version...")
    
    # Also update the ones we already did
    for filepath in ["pages/2_💰_Cost_Per_Closure.py", "pages/3_📈_Monthly_Trend.py", 
                     "pages/4_💵_Budget_Variance.py", "pages/5_🎯_Cost_Tier_Comparison.py"]:
        success, msg = update_file(filepath)
        if success:
            updated += 1
            print(f"OK: {filepath}")

