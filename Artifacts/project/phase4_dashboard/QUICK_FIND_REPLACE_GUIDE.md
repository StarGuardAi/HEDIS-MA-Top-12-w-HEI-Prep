# Quick Guide: Global Find/Replace Across All Pages

## Method 1: Python Script (Recommended) ⭐

**Step-by-step:**

1. **Navigate to the folder:**
   ```
   C:\Users\reich\Projects\HEDIS-MA-Top-12-w-HEI-Prep\Artifacts\project\phase4_dashboard
   ```

2. **Double-click:** `FIND_REPLACE_ALL_PAGES.bat`

3. **Follow the prompts:**
   - Enter text to FIND: `[your search text]`
   - Enter text to REPLACE: `[your replacement text]`
   - Use regex? (y/n): `n` (unless you need regex patterns)
   - Review the preview
   - Type `yes` to confirm

**Example:**
```
Enter the text to FIND: StarGuard AI
Enter the text to REPLACE it with: StarGuard Healthcare AI
Use regex pattern matching? (y/n, default: n): n
```

---

## Method 2: VS Code (If Already Open)

**Step-by-step:**

1. **Open Find/Replace:** Press `Ctrl+Shift+H`

2. **Enter search text** in the first box

3. **Enter replacement text** in the second box

4. **Set files to include:** Click the folder icon, then enter:
   ```
   app.py, pages/*.py
   ```

5. **Review matches** (optional): Click each match to see context

6. **Replace All:** Click the "Replace All" button (or use `Ctrl+Alt+Enter`)

---

## What Gets Updated?

The script processes **22 files total:**
- ✅ `app.py` (main dashboard page)
- ✅ All 21 files in `pages/` directory

---

## Safety Features

- ✅ Shows preview before making changes
- ✅ Counts matches in each file
- ✅ Requires confirmation before replacing
- ✅ Reports results after completion

---

## Common Use Cases

### Update Branding
```
FIND:  StarGuard AI
REPLACE: StarGuard Healthcare AI
```

### Update Footer Text
```
FIND:  © 2024-2026 Robert Reichert
REPLACE: © 2024-2027 Robert Reichert
```

### Update Colors
```
FIND:  #4A3D6F
REPLACE: #5A4D7F
```

### Update URLs
```
FIND:  https://old-url.com
REPLACE: https://new-url.com
```

---

## Troubleshooting

**Script won't run?**
- Make sure Python is installed: `python --version`
- Run directly: `python find_replace_all_pages.py`

**No matches found?**
- Check spelling/case sensitivity
- Try partial matches
- Use regex for patterns: `y` when prompted

**Want to undo changes?**
- Use version control (git) to revert
- Or run find/replace again with reversed values

---

## Files Processed

1. app.py
2. pages/1_📊_ROI_by_Measure.py
3. pages/2_💰_Cost_Per_Closure.py
4. pages/3_📈_Monthly_Trend.py
5. pages/4_💵_Budget_Variance.py
6. pages/5_🎯_Cost_Tier_Comparison.py
7. pages/6_🤖_AI_Executive_Insights.py
8. pages/7_📊_What-If_Scenario_Modeler.py
9. pages/8_🎓_AI_Capabilities_Demo.py
10. pages/8_📋_Campaign_Builder.py
11. pages/9_🔔_Alert_Center.py
12. pages/10_📈_Historical_Tracking.py
13. pages/11_💰_ROI_Calculator.py
14. pages/13_📋_Measure_Analysis.py
15. pages/14_⭐_Star_Rating_Simulator.py
16. pages/15_🔄_Gap_Closure_Workflow.py
17. pages/16_🤖_ML_Gap_Closure_Predictions.py
18. pages/17_📊_Competitive_Benchmarking.py
19. pages/18_📋_Compliance_Reporting.py
20. pages/18_🤖_Secure_AI_Chatbot.py
21. pages/19_⚖️_Health_Equity_Index.py
22. pages/z_Performance_Dashboard.py

