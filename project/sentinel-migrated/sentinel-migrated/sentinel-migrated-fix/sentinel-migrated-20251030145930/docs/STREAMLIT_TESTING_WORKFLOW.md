# Streamlit Testing Workflow - Visual Guide

**Criminal Intelligence Database Portfolio Optimizer**  
**Author:** Robert Reichert  
**Date:** October 24, 2025

---

## 🎯 Testing Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    START TESTING                            │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
        ┌─────────────────────┐
        │  Run Test Launcher  │
        │  test_streamlit.bat │
        └─────────┬───────────┘
                  │
                  ▼
        ┌─────────────────────┐
        │   Choose Option:    │
        ├─────────────────────┤
        │ 1. Manual Testing   │───┐
        │ 2. Automated Tests  │───┼───┐
        │ 3. Coverage Report  │───┼───┼───┐
        │ 4. Specific Tests   │───┼───┼───┼───┐
        │ 5. Debug Mode       │───┼───┼───┼───┼───┐
        └─────────────────────┘   │   │   │   │   │
                                  │   │   │   │   │
┌─────────────────────────────────┘   │   │   │   │
│ MANUAL TESTING (Option 1)           │   │   │   │
│                                     │   │   │   │
│ 1. App launches at localhost:8501   │   │   │   │
│                                     │   │   │   │
│ 2. Follow 5-Minute Checklist:       │   │   │   │
│    ├─ App Load (30s)                │   │   │   │
│    ├─ Navigation (1min)             │   │   │   │
│    ├─ Widgets (2min)                │   │   │   │
│    ├─ Charts (1min)                 │   │   │   │
│    └─ Responsive (30s)              │   │   │   │
│                                     │   │   │   │
│ 3. Visual Inspection:               │   │   │   │
│    ├─ Move sliders                  │   │   │   │
│    ├─ Click radio buttons           │   │   │   │
│    ├─ Switch pages                  │   │   │   │
│    ├─ Hover over charts             │   │   │   │
│    └─ Test mobile view (F12)        │   │   │   │
│                                     │   │   │   │
└─────────────────┬───────────────────┘   │   │   │
                  │                       │   │   │
                  ▼                       │   │   │
        ┌─────────────────┐               │   │   │
        │ PASS or FAIL?   │               │   │   │
        └─────┬───────┬───┘               │   │   │
              │       │                   │   │   │
         PASS │       │ FAIL              │   │   │
              │       │                   │   │   │
              │       └──────────┐        │   │   │
              │                  │        │   │   │
              │                  ▼        │   │   │
              │         ┌────────────────┐│   │   │
              │         │ Fix Issues     ││   │   │
              │         │ Re-test        ││   │   │
              │         └────────┬───────┘│   │   │
              │                  │        │   │   │
              │                  └────────┘   │   │
              │                               │   │
              └───────────────┐               │   │
                              │               │   │
┌─────────────────────────────┴───────────────┘   │
│ AUTOMATED TESTING (Option 2)                    │
│                                                 │
│ pytest tests/test_streamlit_app.py -v          │
│                                                 │
│ Test Execution Flow:                           │
│ ┌─────────────────────────────────────────┐    │
│ │ 1. TestAppInitialization (4 tests)      │    │
│ │    ├─ test_app_loads_without_errors     │    │
│ │    ├─ test_app_has_title                │    │
│ │    ├─ test_sidebar_exists               │    │
│ │    └─ test_sidebar_has_navigation       │    │
│ └─────────────────────────────────────────┘    │
│                    ▼                            │
│ ┌─────────────────────────────────────────┐    │
│ │ 2. TestNavigation (3 tests)             │    │
│ │    ├─ test_page_selector_exists         │    │
│ │    ├─ test_multiple_pages_available     │    │
│ │    └─ test_page_navigation_no_errors    │    │
│ └─────────────────────────────────────────┘    │
│                    ▼                            │
│ ┌─────────────────────────────────────────┐    │
│ │ 3. TestInteractiveWidgets (6 tests)     │    │
│ │    ├─ test_sliders_exist                │    │
│ │    ├─ test_slider_min_value_works       │    │
│ │    ├─ test_slider_max_value_works       │    │
│ │    ├─ test_radio_buttons_exist          │    │
│ │    ├─ test_radio_button_selection       │    │
│ │    └─ test_selectbox_beyond_navigation  │    │
│ └─────────────────────────────────────────┘    │
│                    ▼                            │
│ ┌─────────────────────────────────────────┐    │
│ │ 4. TestEdgeCases (3 tests)              │    │
│ │    ├─ test_all_sliders_at_minimum       │    │
│ │    ├─ test_all_sliders_at_maximum       │    │
│ │    └─ test_rapid_page_switching         │    │
│ └─────────────────────────────────────────┘    │
│                    ▼                            │
│ ┌─────────────────────────────────────────┐    │
│ │ 5. TestDataVisualization (1 test)       │    │
│ │    └─ test_charts_exist                 │    │
│ └─────────────────────────────────────────┘    │
│                    ▼                            │
│ ┌─────────────────────────────────────────┐    │
│ │ 6. TestContactInformation (1 test)      │    │
│ │    └─ test_sidebar_has_contact_info     │    │
│ └─────────────────────────────────────────┘    │
│                    ▼                            │
│ ┌─────────────────────────────────────────┐    │
│ │ 7. TestPerformance (1 test)             │    │
│ │    └─ test_app_loads_quickly            │    │
│ └─────────────────────────────────────────┘    │
│                    ▼                            │
│         ┌─────────────────┐                     │
│         │ 19 PASSED ✅    │                     │
│         └─────────────────┘                     │
│                                                 │
└─────────────────────┬───────────────────────────┘
                      │                     
┌─────────────────────┴───────────────────────────┐
│ COVERAGE REPORT (Option 3)                      │
│                                                 │
│ pytest --cov=streamlit_app --cov-report=html   │
│                                                 │
│ Generated Report:                               │
│ ┌─────────────────────────────────────────┐    │
│ │ htmlcov/index.html                       │    │
│ │                                          │    │
│ │ Coverage Summary:                        │    │
│ │ ├─ Interactive widgets: 100%             │    │
│ │ ├─ Navigation: 100%                      │    │
│ │ ├─ Page rendering: 100%                  │    │
│ │ └─ Overall: TBD                          │    │
│ └─────────────────────────────────────────┘    │
│                                                 │
│ Visual Coverage Map:                            │
│ ┌─────────────────────────────────────────┐    │
│ │ streamlit_app.py                         │    │
│ │                                          │    │
│ │ Line 1-100:    ██████████ 100% ✅       │    │
│ │ Line 101-200:  ████████░░  80% ⚠️        │    │
│ │ Line 201-300:  ██████████ 100% ✅       │    │
│ │ ...                                      │    │
│ └─────────────────────────────────────────┘    │
│                                                 │
└─────────────────────────────────────────────────┘
                      │
                      ▼
        ┌─────────────────────┐
        │  ALL TESTS PASS?    │
        └─────┬───────┬───────┘
              │       │
         YES  │       │ NO
              │       │
              │       └──────────┐
              │                  │
              │                  ▼
              │         ┌────────────────┐
              │         │ Debug & Fix:   │
              │         │                │
              │         │ 1. Check logs  │
              │         │ 2. Re-run test │
              │         │ 3. Fix code    │
              │         └────────┬───────┘
              │                  │
              │                  └────────┐
              │                           │
              ▼                           │
    ┌─────────────────┐                  │
    │ READY TO COMMIT │◄─────────────────┘
    └─────────┬───────┘
              │
              ▼
    ┌─────────────────┐
    │  git add tests/ │
    │  git commit     │
    └─────────┬───────┘
              │
              ▼
    ┌─────────────────┐
    │   DEPLOY TO:    │
    ├─────────────────┤
    │ • GitHub        │
    │ • Streamlit.io  │
    │ • Portfolio     │
    └─────────────────┘
```

---

## 🔄 Continuous Testing Loop

```
┌──────────────────────────────────────────────────────┐
│                  DEVELOPMENT CYCLE                   │
└───────────────────────┬──────────────────────────────┘
                        │
                        ▼
        ┌───────────────────────────┐
        │   Make Code Changes       │
        │   (streamlit_app.py)      │
        └───────────┬───────────────┘
                    │
                    ▼
        ┌───────────────────────────┐
        │   Run Tests               │
        │   (pytest or manual)      │
        └───────────┬───────────────┘
                    │
                    ├─ PASS → Continue
                    │
                    └─ FAIL → Fix
                        │
                        └──────┐
                               │
        ┌──────────────────────┴────┐
        │   Fix Issues              │
        └──────────┬────────────────┘
                   │
                   └─────┐
                         │
                         ▼
        ┌────────────────────────────┐
        │   Re-run Tests             │
        └───────────┬────────────────┘
                    │
                    ▼ (Loop until all pass)
        ┌───────────────────────────┐
        │   All Tests Pass ✅       │
        └───────────┬───────────────┘
                    │
                    ▼
        ┌───────────────────────────┐
        │   Review Coverage         │
        │   (Aim for >80%)          │
        └───────────┬───────────────┘
                    │
                    ▼
        ┌───────────────────────────┐
        │   Commit Changes          │
        └───────────┬───────────────┘
                    │
                    ▼
        ┌───────────────────────────┐
        │   Push to GitHub          │
        └───────────┬───────────────┘
                    │
                    ▼
        ┌───────────────────────────┐
        │   Deploy (if ready)       │
        └───────────────────────────┘
```

---

## 📊 Test Decision Tree

```
                    START
                      │
                      ▼
            ┌─────────────────┐
            │ What do you     │
            │ want to test?   │
            └─────┬───────────┘
                  │
    ┌─────────────┼─────────────┐
    │             │             │
    ▼             ▼             ▼
┌───────┐    ┌────────┐    ┌────────┐
│ Quick │    │ Full   │    │Specific│
│ Check │    │ Suite  │    │Feature │
└───┬───┘    └───┬────┘    └───┬────┘
    │            │             │
    ▼            ▼             ▼
Manual      Automated      Targeted
Testing     All Tests      Tests
    │            │             │
    │            │             │
    ▼            ▼             ▼
┌───────┐    ┌────────┐    ┌────────┐
│Option │    │Option  │    │Option  │
│  1    │    │  2     │    │  4     │
│ (5min)│    │(1min)  │    │(30sec) │
└───────┘    └────────┘    └────────┘
```

---

## 🎯 Widget Testing Flow

```
SLIDER TESTING
├── Navigate to page with sliders
│   └── Example: ROI Calculator
│
├── Test Scenario 1: Minimum Value
│   ├── Move slider to left (minimum)
│   ├── Verify: value displays correctly
│   ├── Verify: charts update
│   └── Verify: calculations adjust
│
├── Test Scenario 2: Maximum Value
│   ├── Move slider to right (maximum)
│   ├── Verify: value displays correctly
│   ├── Verify: charts update
│   └── Verify: calculations adjust
│
├── Test Scenario 3: Mid-range Value
│   ├── Set slider to middle
│   ├── Verify: smooth movement
│   └── Verify: responsive updates
│
└── Test Scenario 4: Keyboard Control
    ├── Tab to slider
    ├── Use arrow keys to adjust
    └── Verify: accessible interaction

RADIO BUTTON TESTING
├── Navigate to page with radio buttons
│   └── Example: Scenario Selection
│
├── Test Scenario 1: Initial State
│   └── Verify: one option pre-selected
│
├── Test Scenario 2: Selection Change
│   ├── Click different option
│   ├── Verify: previous option deselected
│   ├── Verify: new option selected
│   └── Verify: content updates
│
└── Test Scenario 3: All Options
    ├── Click each radio option
    └── Verify: each triggers correct content

SELECTBOX TESTING
├── Navigate to page with selectboxes
│   └── Example: Model Performance
│
├── Test Scenario 1: Dropdown Opens
│   ├── Click selectbox
│   └── Verify: options list appears
│
├── Test Scenario 2: Option Selection
│   ├── Select each option
│   ├── Verify: display updates
│   └── Verify: related content changes
│
└── Test Scenario 3: Keyboard Navigation
    ├── Tab to selectbox
    ├── Press arrow keys
    ├── Press Enter to select
    └── Verify: selection works
```

---

## 📱 Responsive Testing Flow

```
DESKTOP (1920x1080)
├── Full layout visible
├── Sidebar expanded
├── Charts full width
└── No horizontal scroll

        ↓ Resize ↓

TABLET (768x1024)
├── Sidebar collapsible
├── Charts adjust width
├── Touch interactions
└── Vertical scroll only

        ↓ Resize ↓

MOBILE (375x667)
├── Hamburger menu
├── Sidebar hidden by default
├── Charts stack vertically
├── Touch-optimized controls
└── No horizontal scroll

TEST PROCESS:
1. Press F12 (DevTools)
2. Click device toggle (Ctrl+Shift+M)
3. Select device preset
4. Verify layout
5. Test interactions
```

---

## 🔍 Debugging Flow

```
                TEST FAILS
                    │
                    ▼
        ┌───────────────────────┐
        │ Check Error Message   │
        └───────────┬───────────┘
                    │
    ┌───────────────┼───────────────┐
    │               │               │
    ▼               ▼               ▼
App Crash      Widget Error    Data Error
    │               │               │
    │               │               │
    ▼               ▼               ▼
Check          Check           Check
Console        Element         Data
Logs           Selector        Loading
    │               │               │
    │               │               │
    ▼               ▼               ▼
Fix Bug        Update Test     Fix Data
    │               │               │
    │               │               │
    └───────────────┴───────────────┘
                    │
                    ▼
        ┌───────────────────────┐
        │    Re-run Tests       │
        └───────────┬───────────┘
                    │
                    ├─ PASS → Done ✅
                    │
                    └─ FAIL → Debug again
```

---

## ⚡ Quick Command Reference

```
┌─────────────────────────────────────────────────────────┐
│                   COMMAND QUICK GUIDE                   │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  MANUAL TESTING                                         │
│  streamlit run streamlit_app.py                         │
│                                                         │
│  AUTOMATED TESTING                                      │
│  pytest tests/test_streamlit_app.py -v                  │
│                                                         │
│  COVERAGE REPORT                                        │
│  pytest tests/test_streamlit_app.py --cov=streamlit_app│
│                                                         │
│  SPECIFIC TEST CLASS                                    │
│  pytest tests/test_streamlit_app.py::TestNavigation    │
│                                                         │
│  DEBUG MODE                                             │
│  streamlit run streamlit_app.py --logger.level=debug   │
│                                                         │
│  DIFFERENT PORT                                         │
│  streamlit run streamlit_app.py --server.port 8502     │
│                                                         │
│  TEST LAUNCHER                                          │
│  test_streamlit.bat                                     │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 📚 Documentation Map

```
Testing Documentation
│
├── STREAMLIT_TESTING_SETUP_COMPLETE.md
│   └── Overview of all testing resources
│
├── STREAMLIT_TESTING_QUICK_START.md
│   ├── 3-step quick start
│   ├── 5-minute manual checklist
│   └── Common issues & fixes
│
├── docs/STREAMLIT_TESTING_GUIDE.md
│   ├── Comprehensive manual testing
│   ├── AppTest framework details
│   ├── Selenium/Playwright setup
│   ├── Performance testing
│   ├── Cross-browser testing
│   └── CI/CD integration
│
├── docs/STREAMLIT_TESTING_WORKFLOW.md (THIS FILE)
│   └── Visual workflow diagrams
│
└── tests/test_streamlit_app.py
    └── Actual test implementation
```

---

## ✅ Success Criteria Checklist

```
PRE-DEPLOYMENT CHECKLIST
│
├── Technical Validation
│   ├── [ ] 19/19 automated tests pass
│   ├── [ ] No console errors
│   ├── [ ] Load time < 5 seconds
│   ├── [ ] Coverage > 80%
│   └── [ ] All widgets functional
│
├── Cross-Platform Testing
│   ├── [ ] Chrome (latest)
│   ├── [ ] Firefox (latest)
│   ├── [ ] Edge (latest)
│   ├── [ ] Mobile Chrome
│   └── [ ] Mobile Safari
│
├── Responsive Design
│   ├── [ ] Desktop (1920x1080)
│   ├── [ ] Tablet (768x1024)
│   └── [ ] Mobile (375x667)
│
├── Content Verification
│   ├── [ ] Contact info correct
│   ├── [ ] All links work
│   ├── [ ] Charts interactive
│   ├── [ ] Data displays correctly
│   └── [ ] No placeholder content
│
└── User Experience
    ├── [ ] Smooth navigation
    ├── [ ] Instant widget updates
    ├── [ ] No lag or freezing
    ├── [ ] Tooltips functional
    └── [ ] Downloads work
```

---

**Last Updated:** October 24, 2025  
**Testing Framework:** Streamlit AppTest + pytest  
**Test Coverage:** 19 tests, all interactive components



---
*This file is maintained by Sentinel Analytics. For inquiries, contact reichert.sentinel.ai@gmail.com.*
