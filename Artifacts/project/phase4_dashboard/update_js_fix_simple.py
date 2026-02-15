# -*- coding: utf-8 -*-
import re
import sys
from pathlib import Path

# Set UTF-8 encoding for output
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

SCRIPT_DIR = Path(__file__).parent

# Improved JavaScript code (single line pattern for matching)
OLD_PATTERN = r"function fixPerformanceDashboardLabel\(\) \{[^}]+\}[^}]*if \(document\.readyState === 'loading'\)[^}]+setInterval\(fixPerformanceDashboardLabel, 3000\);"

NEW_JS_FUNCTION = """'use strict';
    
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
            
            const shouldReplace = (
                /^z\\s+performance\\s+dashboard/i.test(fullText) ||
                /^z_performance_dashboard/i.test(fullText) ||
                (lowerText.includes('performance dashboard') && (fullText.startsWith('z') || fullText.startsWith('z ')))
            );
            
            if (shouldReplace) {
                link.textContent = '⚡ Performance Dashboard';
                link.innerText = '⚡ Performance Dashboard';
                
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
    window.addEventListener('load', fixPerformanceDashboardLabel);"""

FILES = [
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
            return False, "No fix found"
        
        # Pattern to match the old function and its calls
        old_pattern = r"(function fixPerformanceDashboardLabel\(\) \{.*?setInterval\(fixPerformanceDashboardLabel, 3000\);)"
        
        if re.search(old_pattern, content, re.DOTALL):
            # Replace the old function with new one
            new_content = re.sub(
                r"\(function\(\) \{",
                "(function() {\n    " + NEW_JS_FUNCTION,
                content,
                count=1
            )
            
            # More targeted replacement
            old_func_pattern = r"function fixPerformanceDashboardLabel\(\) \{.*?\n    \}"
            if re.search(old_func_pattern, content, re.DOTALL):
                # Replace just the function body
                content = re.sub(
                    old_func_pattern,
                    "function fixPerformanceDashboardLabel() {\n        " + NEW_JS_FUNCTION.replace("\n    ", "\n        "),
                    content,
                    flags=re.DOTALL
                )
            else:
                # Full replacement approach
                old_block = r"(\(function\(\) \{)[\s\S]*?(function fixPerformanceDashboardLabel\(\) \{)[\s\S]*?(setInterval\(fixPerformanceDashboardLabel, 3000\);[\s\S]*?\}\);[\s\S]*?</script>)"
                replacement = r"\1\n    " + NEW_JS_FUNCTION + "\n})();\n</script>"
                content = re.sub(old_block, replacement, content, flags=re.DOTALL)
            
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True, "Updated"
        else:
            return False, "Pattern mismatch"
            
    except Exception as e:
        return False, str(e)[:50]

print("Updating JavaScript fixes...")
updated = 0
for filepath in FILES:
    success, msg = update_file(filepath)
    if success:
        updated += 1
        print(f"OK: {filepath}")
    else:
        print(f"SKIP: {filepath} - {msg}")

print(f"\nUpdated {updated}/{len(FILES)} files")

