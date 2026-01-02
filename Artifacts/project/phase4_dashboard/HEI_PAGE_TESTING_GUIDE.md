# HEI Page Testing Guide

## 🔄 Streamlit Restart vs. Refresh

### **Recommended: Restart Streamlit** ⚠️

Since we created:
- ✅ New page file (`19_⚖️_Health_Equity_Index.py`)
- ✅ New utility file (`utils/hei_queries.py`)
- ✅ New imports

**You should restart Streamlit** to ensure everything loads correctly.

---

## 🚀 Step-by-Step Testing Instructions

### Step 1: Restart Streamlit

1. **Stop the current Streamlit server**:
   - Press `Ctrl+C` in the terminal where Streamlit is running
   - Or close the terminal window

2. **Navigate to the dashboard directory**:
   ```bash
   cd C:\Users\reich\Projects\HEDIS-MA-Top-12-w-HEI-Prep\Artifacts\project\phase4_dashboard
   ```

3. **Start Streamlit again**:
   ```bash
   streamlit run app.py
   ```

### Step 2: Navigate to HEI Page

1. Open your browser to the Streamlit app (usually `http://localhost:8501`)
2. Look in the sidebar for: **"⚖️ Health Equity Index"**
3. Click on it to load the page

---

## ✅ Testing Checklist

### 1. Page Loads Correctly
- [ ] Page appears in sidebar navigation
- [ ] Page title shows "⚖️ Health Equity Index (HEI) Analyzer"
- [ ] No error messages in the page
- [ ] No errors in the Streamlit terminal/console

### 2. Visualizations Render
- [ ] **Overview Dashboard Tab**: 
  - HEI Score gauge displays
  - Key metrics (4 cards) show values
  - Disparity heatmap chart appears
  - Equity trend chart displays
  - Measure equity table shows data

- [ ] **Demographic Deep Dive Tab**:
  - Measure selector dropdown works
  - Demographic breakdown charts render
  - Worst/Best performing groups show data

- [ ] **Intervention Planner Tab**:
  - Scenario modeling controls appear
  - Projections calculate correctly

- [ ] **Predictive Analytics Tab**:
  - Forecast chart displays
  - Recommendations appear

- [ ] **Reports & Downloads Tab**:
  - Export buttons appear
  - Data preview tables show

### 3. Database Connection (Optional)

**If you have a database configured:**

- [ ] Check sidebar for "✅ Database Connected" message
- [ ] Toggle "Use Database Data" checkbox
- [ ] Page attempts to load from database
- [ ] If database fails, shows warning and uses synthetic data

**If no database:**

- [ ] "Use Database Data" checkbox works but uses synthetic data
- [ ] No errors occur
- [ ] Synthetic data displays correctly

### 4. Filters and Controls

- [ ] **Date Range**: Select different dates → Data updates
- [ ] **Demographic Focus**: Switch Race/Age/Gender → Charts update
- [ ] **Measure Filter**: Select/deselect measures → Data filters
- [ ] **Scenario Sliders**:
  - Disparity Reduction slider → Updates projections
  - Intervention Budget slider → Updates financial impact
  - Timeline slider → Updates projections
  - Reward Factor slider → Updates revenue projections

### 5. Interactive Features

- [ ] Click on charts → Tooltips work
- [ ] Hover over data points → Information displays
- [ ] Zoom/pan charts (if available)
- [ ] Select measure in dropdown → Details update

### 6. Data Exports

- [ ] Click "Download Measure Equity Metrics (CSV)"
- [ ] Download button appears
- [ ] CSV file downloads successfully
- [ ] Open CSV → Data is correct format
- [ ] Click "Download Detailed Demographic Data (CSV)"
- [ ] Second CSV downloads successfully

### 7. Error Handling

- [ ] Toggle database on/off → No crashes
- [ ] Change filters rapidly → No errors
- [ ] Select all/no measures → Handles gracefully
- [ ] View with no data → Shows informative message

---

## 🐛 Troubleshooting

### Page Doesn't Appear in Sidebar

**Problem**: HEI page not showing in navigation

**Solutions**:
1. Ensure file is named correctly: `19_⚖️_Health_Equity_Index.py`
2. Check file is in `pages/` directory
3. Restart Streamlit completely
4. Check for import errors in terminal

### Import Errors

**Problem**: Error about `utils.hei_queries` not found

**Solutions**:
1. Verify `utils/hei_queries.py` exists
2. Check file has no syntax errors
3. Restart Streamlit
4. Check terminal for specific error message

### Charts Not Rendering

**Problem**: Blank charts or errors

**Solutions**:
1. Check browser console for JavaScript errors
2. Verify Plotly is installed: `pip install plotly`
3. Check if data is loading (look at table views)
4. Refresh the page

### Database Connection Issues

**Problem**: Database errors when toggling "Use Database Data"

**Solutions**:
1. This is expected if database isn't configured
2. Page should show warning and use synthetic data
3. If crashes, check `utils/database.py` connection
4. Uncheck "Use Database Data" to use synthetic data only

---

## 📝 Expected Behavior

### With Synthetic Data (Default)
- ✅ All visualizations work
- ✅ All filters work
- ✅ All exports work
- ✅ No errors
- ✅ Fast loading

### With Database (If Configured)
- ✅ Loads real data from database
- ✅ Falls back to synthetic if database fails
- ✅ Shows status indicator
- ✅ No crashes

---

## 🎯 Quick Test (2 Minutes)

If you're in a hurry, just verify:

1. ✅ Page appears in sidebar
2. ✅ Page loads without errors
3. ✅ HEI Score gauge displays
4. ✅ At least one chart renders
5. ✅ One slider works

If all 5 pass, the page is working! You can do detailed testing later.

---

## 📊 Performance Expectations

- **Page Load**: < 3 seconds
- **Chart Rendering**: < 1 second per chart
- **Filter Updates**: < 2 seconds
- **CSV Export**: < 1 second

If significantly slower, check:
- Data size (synthetic data should be fast)
- Browser performance
- Network issues

---

## 💡 Tips

1. **Start Simple**: Test Overview Dashboard tab first
2. **Use Synthetic Data First**: Easier to test without database
3. **Check Terminal**: Errors often show in Streamlit terminal
4. **Browser Console**: Press F12 to see JavaScript errors
5. **Clear Cache**: If issues persist, Streamlit menu → "Clear cache"

---

## ✅ Success Criteria

The page is working correctly if:

- ✅ All 5 tabs load without errors
- ✅ All visualizations render
- ✅ At least 3 charts display data
- ✅ Filters update the display
- ✅ CSV exports work
- ✅ No crashes or error messages

---

**Next Steps After Testing**:
- Report any issues found
- Request specific enhancements
- Optimize performance if needed
- Add more features from the plan

---

**Date**: 2024-12-19  
**Status**: Ready for Testing









