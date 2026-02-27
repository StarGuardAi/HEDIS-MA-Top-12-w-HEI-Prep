# -*- coding: utf-8 -*-
"""Add Performance Dashboard label fix JavaScript to all pages"""

import re
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent

FILES = [
    "app.py",
    "pages/1_📊_ROI_by_Measure.py",
    "pages/2_💰_Cost_Per_Closure.py",
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

# JavaScript code to add
JS_FIX = """
    // Fix sidebar label: Replace "z Performance Dashboard" with "⚡ Performance Dashboard"
    function fixPerformanceDashboardLabel() {
        const sidebarNav = document.querySelector('[data-testid="stSidebarNav"]');
        if (sidebarNav) {
            const links = sidebarNav.querySelectorAll('a');
            links.forEach(link => {
                const text = link.textContent.trim();
                // Handle various formats: "z Performance Dashboard", "z_Performance_Dashboard", etc.
                if (text === 'z Performance Dashboard' || 
                    text === '⚡ Performance Dashboard' || 
                    text.includes('z Performance Dashboard') ||
                    text.includes('⚡ Performance Dashboard') ||
                    text === 'z_Performance_Dashboard' ||
                    text.includes('z_Performance_Dashboard') ||
                    (text.includes('Performance Dashboard') && text.startsWith('z'))) {
                    link.textContent = '⚡ Performance Dashboard';
                    // Also update any child elements
                    const spans = link.querySelectorAll('span');
                    spans.forEach(span => {
                        const spanText = span.textContent.trim();
                        if (spanText.includes('z Performance Dashboard') || 
                            spanText.includes('z_Performance_Dashboard') ||
                            spanText.includes('⚡ Performance Dashboard')) {
                            span.textContent = '⚡ Performance Dashboard';
                        }
                    });
                }
            });
        }
    }
    
    // Run on page load and after delays
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', fixPerformanceDashboardLabel);
    } else {
        fixPerformanceDashboardLabel();
    }
    setTimeout(fixPerformanceDashboardLabel, 500);
    setTimeout(fixPerformanceDashboardLabel, 1000);
    setTimeout(fixPerformanceDashboardLabel, 2000);
    // Also run periodically to catch dynamically loaded navigation
    setInterval(fixPerformanceDashboardLabel, 3000);
"""

def add_js_fix_to_file(file_path):
    """Add JavaScript fix to a file if it doesn't already have it."""
    full_path = SCRIPT_DIR / file_path
    
    if not full_path.exists():
        return (False, f"File not found: {file_path}")
    
    try:
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if fix already exists
        if 'fixPerformanceDashboardLabel' in content:
            # Check if it's the updated version
            if "text === 'z Performance Dashboard'" in content:
                return (False, "Already has updated fix")
            else:
                # Has old version, need to update
                # Remove old version first
                old_pattern = r'// Fix sidebar label:.*?setInterval\(fixPerformanceDashboardLabel[^;]*\);'
                content = re.sub(old_pattern, JS_FIX.strip(), content, flags=re.DOTALL)
                if 'fixPerformanceDashboardLabel' not in content:
                    # Pattern didn't match, try different approach
                    return (False, "Could not update existing fix")
        
        # Find where to insert - look for existing script tags
        script_pattern = r'(</script>\s*""",\s*unsafe_allow_html=True)'
        matches = list(re.finditer(script_pattern, content))
        
        if matches:
            # Insert before the last </script> tag
            insert_pos = matches[-1].start()
            # Check if we're inside a script tag
            before_insert = content[:insert_pos]
            if '<script>' in before_insert or 'st.markdown("""<script>' in before_insert:
                # Insert before closing script tag
                content = content[:insert_pos] + JS_FIX + "\n" + content[insert_pos:]
            else:
                # Need to add script wrapper
                script_wrapper = '<script>\n' + JS_FIX + '\n</script>\n"""'
                content = content[:insert_pos] + script_wrapper + content[insert_pos:]
        else:
            # No existing script tag, add one at the end
            # Look for the end of the file or a good insertion point
            # Try to find a place after imports and config
            end_marker = 'st.markdown("""'
            if end_marker in content:
                # Add before the last st.markdown if it exists
                last_markdown = content.rfind(end_marker)
                if last_markdown > len(content) * 0.7:  # Near end of file
                    script_block = f'''
st.markdown("""
<script>
{JS_FIX}
</script>
""", unsafe_allow_html=True)
'''
                    content = content[:last_markdown] + script_block + "\n" + content[last_markdown:]
                else:
                    # Add at end
                    script_block = f'''
st.markdown("""
<script>
{JS_FIX}
</script>
""", unsafe_allow_html=True)
'''
                    content = content.rstrip() + "\n" + script_block
            else:
                # Add at end
                script_block = f'''
st.markdown("""
<script>
{JS_FIX}
</script>
""", unsafe_allow_html=True)
'''
                content = content.rstrip() + "\n" + script_block
        
        # Write back
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return (True, "Added/Updated")
        
    except Exception as e:
        return (False, str(e))

def main():
    print("=" * 70)
    print("Adding Performance Dashboard Label Fix to All Pages")
    print("=" * 70)
    
    results = []
    for file_path in FILES:
        success, message = add_js_fix_to_file(file_path)
        status = "✅" if success else "⏭️"
        print(f"{status} {file_path}: {message}")
        results.append((file_path, success, message))
    
    print("\n" + "=" * 70)
    print("SUMMARY:")
    print("=" * 70)
    successful = sum(1 for _, s, _ in results if s)
    print(f"Files processed: {len(FILES)}")
    print(f"Successfully updated: {successful}")
    print(f"Already had fix/Skipped: {len(FILES) - successful}")
    print("=" * 70)

if __name__ == "__main__":
    main()

