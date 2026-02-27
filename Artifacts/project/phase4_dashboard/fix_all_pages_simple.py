# -*- coding: utf-8 -*-
import re
import sys
from pathlib import Path

# Fix encoding for Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

SCRIPT_DIR = Path(__file__).parent

# Read the improved JS from page 2
template_file = SCRIPT_DIR / "pages" / "2_💰_Cost_Per_Closure.py"
if template_file.exists():
    with open(template_file, 'r', encoding='utf-8') as f:
        template_content = f.read()
    
    # Extract the improved JS block
    match = re.search(r'# Fix sidebar label.*?</script>"""', template_content, re.DOTALL)
    if match:
        IMPROVED_JS_BLOCK = match.group(0)
    else:
        IMPROVED_JS_BLOCK = None
else:
    IMPROVED_JS_BLOCK = None

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
            return False, "No JS fix found"
        
        if IMPROVED_JS_BLOCK:
            # Replace old JS block with improved one
            pattern = r'# Fix sidebar label: Replace.*?</script>"""'
            if re.search(pattern, content, re.DOTALL):
                content = re.sub(pattern, IMPROVED_JS_BLOCK, content, flags=re.DOTALL)
                with open(full_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                return True, "Updated"
        
        return False, "Pattern not found"
    except Exception as e:
        return False, str(e)[:30]

print("Updating files...")
updated = 0
for filepath in FILES:
    success, msg = update_file(filepath)
    if success:
        updated += 1
        print(f"OK: {filepath}")
    else:
        print(f"SKIP: {filepath} - {msg}")

print(f"\nUpdated {updated}/{len(FILES)} files")

