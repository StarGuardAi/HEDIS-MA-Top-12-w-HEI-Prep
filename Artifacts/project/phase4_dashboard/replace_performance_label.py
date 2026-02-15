# -*- coding: utf-8 -*-
"""Simple script to replace 'z Performance Dashboard' with '⚡ Performance Dashboard'"""

import os
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

SEARCH = "z Performance Dashboard"
REPLACE = "⚡ Performance Dashboard"

total = 0
for file_path in FILES:
    full_path = SCRIPT_DIR / file_path
    if full_path.exists():
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            count = content.count(SEARCH)
            if count > 0:
                content = content.replace(SEARCH, REPLACE)
                with open(full_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Replaced {count} in {file_path}")
                total += count
        except Exception as e:
            print(f"Error processing {file_path}: {e}")

print(f"\nTotal replacements: {total}")

