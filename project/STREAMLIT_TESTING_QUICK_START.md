# Streamlit App Testing - Quick Start Guide

**HEDIS Portfolio Optimizer Dashboard**  
**Author:** Robert Reichert  
**Date:** October 24, 2025

---

## 🚀 Get Started in 3 Steps

### Option 1: Use the Automated Test Launcher (Easiest)

```bash
# Windows
test_streamlit.bat

# This will show you a menu with options for:
# 1. Manual testing (launches app)
# 2. Automated tests
# 3. Coverage reports
# 4. Specific test classes
# 5. Debug mode
```

### Option 2: Manual Testing (Immediate)

```bash
# Start the app
streamlit run streamlit_app.py

# Open browser to: http://localhost:8501
# Follow the manual testing checklist below
```

### Option 3: Automated Testing (Recommended)

```bash
# Run all tests
pytest tests/test_streamlit_app.py -v

# Run with coverage
pytest tests/test_streamlit_app.py --cov=streamlit_app --cov-report=html
```

---

## ✅ Quick Manual Testing Checklist (5 Minutes)

### 1. App Load Test (30 seconds)
- [ ] Run `streamlit run streamlit_app.py`
- [ ] App loads at http://localhost:8501
- [ ] No errors in terminal
- [ ] Sidebar visible with logo
- [ ] Contact info shows in sidebar

### 2. Navigation Test (1 minute)
- [ ] Click sidebar dropdown (page selector)
- [ ] Select 3 different pages
- [ ] Each page loads without errors
- [ ] Content changes when switching pages

### 3. Interactive Widgets Test (2 minutes)

**Sliders:**
- [ ] Find a page with sliders (ROI Calculator, Portfolio Simulator)
- [ ] Move one slider left/right
- [ ] Charts/numbers update automatically
- [ ] No lag or freezing

**Radio Buttons:**
- [ ] Find radio buttons (Scenario selection, Simulation mode)
- [ ] Click different options
- [ ] Content updates based on selection

**Dropdowns:**
- [ ] Try the model selection dropdown
- [ ] Select different models
- [ ] Performance metrics update

### 4. Chart Interaction Test (1 minute)
- [ ] Navigate to a page with charts
- [ ] Hover over chart (tooltip appears)
- [ ] Try zoom/pan on Plotly charts
- [ ] Click camera icon to download PNG

### 5. Responsive Test (30 seconds)
- [ ] Press F12 (open DevTools)
- [ ] Click device toggle (Ctrl+Shift+M)
- [ ] Select "iPhone SE" or "iPad"
- [ ] Verify layout adjusts
- [ ] Sidebar collapses on mobile

---

## 🤖 Automated Testing Results

### Test Suite Overview

The automated test suite checks:

| Test Class | What It Tests | # Tests |
|-----------|---------------|---------|
| `TestAppInitialization` | App loads, sidebar exists | 4 |
| `TestNavigation` | Page switching works | 3 |
| `TestInteractiveWidgets` | Sliders, radios, selectboxes | 6 |
| `TestEdgeCases` | Min/max values, rapid switching | 3 |
| `TestDataVisualization` | Charts render | 1 |
| `TestContactInformation` | Contact info present | 1 |
| `TestPerformance` | Load time < 10s | 1 |
| **TOTAL** | | **19 tests** |

### Expected Output (All Pass ✅)

```
====================== test session starts ======================
tests/test_streamlit_app.py::TestAppInitialization::test_app_loads_without_errors PASSED
tests/test_streamlit_app.py::TestAppInitialization::test_app_has_title PASSED
tests/test_streamlit_app.py::TestAppInitialization::test_sidebar_exists PASSED
tests/test_streamlit_app.py::TestAppInitialization::test_sidebar_has_navigation PASSED
tests/test_streamlit_app.py::TestNavigation::test_page_selector_exists PASSED
tests/test_streamlit_app.py::TestNavigation::test_multiple_pages_available PASSED
tests/test_streamlit_app.py::TestNavigation::test_page_navigation_no_errors PASSED
tests/test_streamlit_app.py::TestInteractiveWidgets::test_sliders_exist PASSED
tests/test_streamlit_app.py::TestInteractiveWidgets::test_slider_min_value_works PASSED
tests/test_streamlit_app.py::TestInteractiveWidgets::test_slider_max_value_works PASSED
tests/test_streamlit_app.py::TestInteractiveWidgets::test_radio_buttons_exist PASSED
tests/test_streamlit_app.py::TestInteractiveWidgets::test_radio_button_selection PASSED
tests/test_streamlit_app.py::TestInteractiveWidgets::test_selectbox_beyond_navigation PASSED
tests/test_streamlit_app.py::TestEdgeCases::test_all_sliders_at_minimum PASSED
tests/test_streamlit_app.py::TestEdgeCases::test_all_sliders_at_maximum PASSED
tests/test_streamlit_app.py::TestEdgeCases::test_rapid_page_switching PASSED
tests/test_streamlit_app.py::TestDataVisualization::test_charts_exist PASSED
tests/test_streamlit_app.py::TestContactInformation::test_sidebar_has_contact_info PASSED
tests/test_streamlit_app.py::TestPerformance::test_app_loads_quickly PASSED

====================== 19 passed in 45.23s ======================
```

---

## 🐛 Common Issues & Quick Fixes

### Issue: `ModuleNotFoundError: No module named 'streamlit'`
**Fix:**
```bash
pip install streamlit pytest
```

### Issue: `FileNotFoundError: streamlit_app.py not found`
**Fix:**
```bash
# Make sure you're in project root
cd C:\Users\reich\Projects\HEDIS-MA-Top-12-w-HEI-Prep
pytest tests/test_streamlit_app.py -v
```

### Issue: Tests timeout or hang
**Fix:**
```bash
# The app might be large; increase timeout
pytest tests/test_streamlit_app.py -v --timeout=120
```

### Issue: Port 8501 already in use
**Fix:**
```bash
# Find and kill process using port 8501
netstat -ano | findstr :8501
taskkill /PID <PID> /F

# Or use different port
streamlit run streamlit_app.py --server.port 8502
```

---

## 📊 Test Coverage

### Check What's Tested

```bash
# Generate coverage report
pytest tests/test_streamlit_app.py --cov=streamlit_app --cov-report=html

# Open in browser
start htmlcov\index.html
```

**Target Coverage:** >80% of interactive components

---

## 🎯 What to Test Based on Changes

### If You Modified Sliders:
```bash
pytest tests/test_streamlit_app.py::TestInteractiveWidgets::test_slider_min_value_works -v
pytest tests/test_streamlit_app.py::TestInteractiveWidgets::test_slider_max_value_works -v
pytest tests/test_streamlit_app.py::TestEdgeCases -v
```

### If You Added New Pages:
```bash
pytest tests/test_streamlit_app.py::TestNavigation -v
```

### If You Modified Charts:
```bash
pytest tests/test_streamlit_app.py::TestDataVisualization -v
```

### If You Changed Layout:
```bash
pytest tests/test_streamlit_app.py::TestAppInitialization -v
```

---

## 📚 Full Documentation

For comprehensive testing guide including:
- Selenium/Playwright browser automation
- Performance testing
- Cross-browser testing
- CI/CD integration

**Read:** `docs/STREAMLIT_TESTING_GUIDE.md`

---

## 🔄 Continuous Testing Workflow

### During Development:
```bash
# Terminal 1: Run app
streamlit run streamlit_app.py

# Terminal 2: Watch tests (re-run on file changes)
pytest-watch tests/test_streamlit_app.py
```

### Before Committing:
```bash
# Run full test suite
pytest tests/test_streamlit_app.py -v

# Check coverage
pytest tests/test_streamlit_app.py --cov=streamlit_app --cov-report=term

# If all pass, commit!
git add tests/test_streamlit_app.py
git commit -m "Add Streamlit interactivity tests"
```

---

## ✅ Testing Checklist for Portfolio Review

Before showcasing to recruiters/hiring managers:

- [ ] All automated tests pass (19/19)
- [ ] Manual testing checklist complete
- [ ] App loads in < 5 seconds
- [ ] No console errors (F12 → Console)
- [ ] Works on Chrome, Firefox, Edge
- [ ] Mobile responsive (test in DevTools)
- [ ] All links work (GitHub, LinkedIn, Portfolio)
- [ ] Charts interactive (hover, zoom work)
- [ ] Contact info visible and correct

---

## 🚀 Next Steps

1. **Run the test launcher:** `test_streamlit.bat`
2. **Try manual testing** (5 minutes)
3. **Run automated tests** (1 minute)
4. **Review coverage report** (optional)
5. **Fix any failures** (if needed)

---

## 📞 Need Help?

**Documentation:**
- Quick Start: This file
- Comprehensive Guide: `docs/STREAMLIT_TESTING_GUIDE.md`
- Streamlit Docs: https://docs.streamlit.io/library/api-reference/app-testing

**Contact:**
- Robert Reichert
- reichert99@gmail.com
- GitHub: github.com/bobareichert

---

**Last Updated:** October 24, 2025  
**App Version:** HEDIS Portfolio Optimizer v1.0  
**Test Coverage:** 19 tests covering initialization, navigation, widgets, edge cases, and performance

