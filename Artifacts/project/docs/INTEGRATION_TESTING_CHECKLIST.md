# Integration Testing Checklist

## Quick Verification Commands

Run these commands to verify installation:

```bash
# 1. Check all files created
cd Artifacts/project
dir services\context_engineering
dir services\agentic_rag
dir phase4_dashboard\components
dir phase4_dashboard\pages\8_*
dir docs\CONTEXT_ENGINEERING_AGENTIC_RAG.md

# 2. Test imports
python -c "from services.context_engineering import HierarchicalContextBuilder; print('✅ Context engineering imported')"
python -c "from services.agentic_rag import AgenticPlanner, ToolExecutor; print('✅ Agentic RAG imported')"
cd phase4_dashboard
python -c "from components.visualization_components import render_efficiency_gauge; print('✅ Components imported')"

# 3. Test context builder
cd ..
python -c "from services.context_engineering import HierarchicalContextBuilder; builder = HierarchicalContextBuilder(); context = builder.build_context('Calculate ROI for diabetes'); assert 'metadata' in context; assert 'efficiency_score' in context['metadata']; print(f'✅ Context builder works: {context[\"metadata\"][\"efficiency_score\"]}% efficiency')"

# 4. Test planner
python -c "from services.agentic_rag import AgenticPlanner; planner = AgenticPlanner(); plan = planner.create_plan('Find gaps and calculate ROI'); assert 'steps' in plan; assert 'estimated_time' in plan; print(f'✅ Planner works: {len(plan[\"steps\"])} steps, {plan[\"estimated_time\"]}s')"
```

## Manual Testing Checklist

### Test 1: Enhanced Secure AI Chatbot

**Location:** Pages > Secure AI Chatbot

- [ ] Navigate to "Secure AI Chatbot" page
- [ ] Page loads without errors
- [ ] AI Mode selector appears in sidebar
- [ ] Three options visible: "Basic RAG", "Context-Aware RAG", "Full Agentic RAG"
- [ ] Select "Context-Aware RAG" mode
- [ ] Visualization checkboxes appear in sidebar:
  - [ ] "Show Context Analysis"
  - [ ] "Show Planning Steps"
  - [ ] "Show Validation"
  - [ ] "Show Performance Metrics"
- [ ] Enable "Show Context Analysis"
- [ ] Enter query: "Calculate ROI for HbA1c testing"
- [ ] Click "🔍 Ask" button
- [ ] Context building spinner appears
- [ ] Context layers display correctly (3 columns)
- [ ] Efficiency gauge chart renders
- [ ] Response generates successfully
- [ ] No console errors in browser

**Expected Results:**
- Context analysis shows Layer 1, Layer 2, Layer 3 status
- Efficiency gauge displays score (0-100)
- Query processes and returns response

---

### Test 2: AI Capabilities Demo

**Location:** Pages > AI Capabilities Demo

- [ ] Navigate to "AI Capabilities Demo" page
- [ ] Page loads without errors
- [ ] All 4 tabs are visible:
  - [ ] "📊 Architecture Overview"
  - [ ] "🧠 Context Engineering"
  - [ ] "🤖 Agentic RAG"
  - [ ] "🎮 Live Demo"

**Tab 1: Architecture Overview**
- [ ] Comparison cards display (Traditional RAG vs StarGuard AI)
- [ ] Flow diagrams render correctly
- [ ] Performance comparison charts display
- [ ] Key innovation callout box visible

**Tab 2: Context Engineering**
- [ ] Problem statement displays
- [ ] 3-layer context explanation visible
- [ ] Layer expanders work (click to expand/collapse)
- [ ] Live Context Analyzer section visible
- [ ] Select sample query from dropdown
- [ ] Click "🔍 Analyze Context" button
- [ ] Context analysis results display
- [ ] Efficiency gauge chart renders
- [ ] Performance impact table shows

**Tab 3: Agentic RAG**
- [ ] Query example text area visible
- [ ] Click "🤖 Generate Execution Plan" button
- [ ] Execution plan generates successfully
- [ ] Plan summary metrics display (steps, time, cost, confidence)
- [ ] Execution steps expanders work
- [ ] Dependency diagram renders
- [ ] Self-correction section displays

**Tab 4: Live Demo**
- [ ] Complexity selector works (Simple/Medium/Complex)
- [ ] Pre-built queries dropdown populates
- [ ] Select "Complex" query
- [ ] Click "▶️ Execute Query" button
- [ ] Progress bar animates through 4 phases
- [ ] Status text updates correctly
- [ ] Context layers expander shows results
- [ ] Execution plan expander shows steps
- [ ] Execution log expander shows results
- [ ] Final results display
- [ ] Performance comparison table shows
- [ ] Download button generates JSON file

**Expected Results:**
- All tabs render without errors
- Charts display correctly
- Interactive elements work
- No JavaScript errors in console

---

### Test 3: Enhanced ROI Calculator

**Location:** Pages > ROI Calculator

- [ ] Navigate to "ROI Calculator" page
- [ ] Page loads without errors
- [ ] Scroll to bottom of page
- [ ] "Interactive ROI Calculator: Your Organization" section visible
- [ ] Organization profile inputs visible:
  - [ ] Health Plan Name text input
  - [ ] Members Covered slider (10K-500K)
  - [ ] Queries per Day slider (10-5K)
  - [ ] Data Analysts slider (1-50)
  - [ ] Analyst Hourly Rate slider ($40-$150)
  - [ ] Current AI Spend number input
- [ ] Adjust sliders to custom values
- [ ] Click "📊 Calculate My ROI" button
- [ ] Big total value displays with gradient background
- [ ] Year 1 ROI and Ongoing ROI metrics show
- [ ] Cost savings breakdown table displays
- [ ] Bar chart renders (Annual Value by Category)
- [ ] 5-year financial projection table displays
- [ ] 5-year projection chart renders (bar + line)
- [ ] Executive summary box displays
- [ ] Next Steps section shows three buttons:
  - [ ] "📧 Email This Report"
  - [ ] "📊 Download Full Report (JSON)"
  - [ ] "📅 Schedule Demo"
- [ ] Click download button
- [ ] JSON file downloads successfully
- [ ] Verify JSON contains all expected fields

**Expected Results:**
- All inputs work correctly
- Calculations are accurate
- Charts render properly
- JSON download works
- No calculation errors

---

### Test 4: Performance Testing

- [ ] Open browser developer tools (F12)
- [ ] Navigate to Console tab
- [ ] Visit "Secure AI Chatbot" page
- [ ] Check for JavaScript errors (should be none)
- [ ] Check page load time (should be < 3 seconds)
- [ ] Visit "AI Capabilities Demo" page
- [ ] Check page load time (should be < 3 seconds)
- [ ] Navigate between tabs quickly
- [ ] Verify no lag or stuttering
- [ ] Check browser memory usage (should be < 500MB)
- [ ] Run multiple queries in chatbot
- [ ] Verify performance doesn't degrade

**Expected Results:**
- No console errors
- Pages load quickly
- Smooth interactions
- Reasonable memory usage

---

### Test 5: Integration Testing

- [ ] All existing pages still work:
  - [ ] Home page
  - [ ] ROI by Measure
  - [ ] Cost Per Closure
  - [ ] Monthly Trend
  - [ ] Budget Variance
  - [ ] Other existing pages
- [ ] Navigation sidebar works correctly
- [ ] New pages appear in navigation
- [ ] No duplicate functionality
- [ ] Styling is consistent across all pages
- [ ] Footer displays on all pages
- [ ] Header displays on all pages

**Mobile Responsiveness:**
- [ ] Open on mobile device or resize browser
- [ ] "Secure AI Chatbot" page responsive
- [ ] "AI Capabilities Demo" page responsive
- [ ] "ROI Calculator" page responsive
- [ ] Charts resize correctly
- [ ] Text is readable
- [ ] Buttons are clickable

**Expected Results:**
- No broken functionality
- Consistent styling
- Mobile-friendly layouts

---

## Common Issues & Fixes

### Issue 1: ModuleNotFoundError: No module named 'services'

**Symptoms:**
```
ModuleNotFoundError: No module named 'services'
```

**Fix:**
Add project root to Python path in page files:
```python
import sys
import os
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
```

---

### Issue 2: AttributeError with ContextLayer

**Symptoms:**
```
AttributeError: 'ContextLayer' object has no attribute 'data'
```

**Fix:**
Check dataclass definitions in `services/context_engineering/context_builder.py`. Ensure ContextLayer dataclass is properly defined:
```python
@dataclass
class ContextLayer:
    name: str
    data: Dict[str, Any]
    size_bytes: int
    last_updated: datetime
    ttl_seconds: int
    relevance_score: float
```

---

### Issue 3: Charts not rendering

**Symptoms:**
- Charts show as blank spaces
- JavaScript errors in console

**Fix:**
```bash
pip install plotly --upgrade
```

Restart Streamlit after upgrading.

---

### Issue 4: Slow performance

**Symptoms:**
- Queries take > 10 seconds
- Page loads slowly

**Fix:**
1. Check cache is working:
```python
builder = HierarchicalContextBuilder()
stats = builder.get_cache_stats()
print(f"Cache hits: {stats['hits']}, misses: {stats['misses']}")
```

2. Verify cache TTLs are appropriate
3. Check for unnecessary database queries
4. Monitor memory usage

---

### Issue 5: Import errors in components

**Symptoms:**
```
ImportError: cannot import name 'render_efficiency_gauge'
```

**Fix:**
1. Verify `phase4_dashboard/components/__init__.py` exports functions correctly
2. Check import path:
```python
from components.visualization_components import render_efficiency_gauge
```
Or:
```python
from components import render_efficiency_gauge
```

---

### Issue 6: Streamlit page not appearing in navigation

**Symptoms:**
- New page doesn't show in sidebar
- Page loads but isn't listed

**Fix:**
1. Verify file naming: `pages/8_🎓_AI_Capabilities_Demo.py`
2. Check file is in `phase4_dashboard/pages/` directory
3. Restart Streamlit server
4. Clear browser cache

---

### Issue 7: Execution plan not generating

**Symptoms:**
- "Generate Execution Plan" button does nothing
- Error message appears

**Fix:**
1. Check AgenticPlanner is imported correctly
2. Verify query is not empty
3. Check browser console for JavaScript errors
4. Verify context is being passed to planner:
```python
plan = planner.create_plan(query, context)  # Not just query
```

---

## Verification Script

Create a test script to run all verifications:

```python
# test_integration.py
import sys
import os

def test_imports():
    """Test all imports work"""
    try:
        from services.context_engineering import HierarchicalContextBuilder
        from services.agentic_rag import AgenticPlanner, ToolExecutor
        sys.path.insert(0, 'phase4_dashboard')
        from components.visualization_components import render_efficiency_gauge
        print("✅ All imports successful")
        return True
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def test_context_builder():
    """Test context builder works"""
    try:
        from services.context_engineering import HierarchicalContextBuilder
        builder = HierarchicalContextBuilder()
        context = builder.build_context("Test query")
        assert 'metadata' in context
        assert 'efficiency_score' in context['metadata']
        print(f"✅ Context builder works: {context['metadata']['efficiency_score']}% efficiency")
        return True
    except Exception as e:
        print(f"❌ Context builder error: {e}")
        return False

def test_planner():
    """Test planner works"""
    try:
        from services.agentic_rag import AgenticPlanner
        planner = AgenticPlanner()
        plan = planner.create_plan("Test query")
        assert 'steps' in plan
        assert 'estimated_time' in plan
        print(f"✅ Planner works: {len(plan['steps'])} steps, {plan['estimated_time']}s")
        return True
    except Exception as e:
        print(f"❌ Planner error: {e}")
        return False

def test_visualization_components():
    """Test visualization components work"""
    try:
        sys.path.insert(0, 'phase4_dashboard')
        from components.visualization_components import render_efficiency_gauge
        fig = render_efficiency_gauge(75)
        assert fig is not None
        print("✅ Visualization components work")
        return True
    except Exception as e:
        print(f"❌ Visualization components error: {e}")
        return False

if __name__ == "__main__":
    print("Running integration tests...")
    results = [
        test_imports(),
        test_context_builder(),
        test_planner(),
        test_visualization_components()
    ]
    
    if all(results):
        print("\n✅ ALL TESTS PASSED - Ready for demo!")
    else:
        print("\n❌ SOME TESTS FAILED - Review errors above")
```

Run with:
```bash
cd Artifacts/project
python test_integration.py
```

---

## Final Checklist

Before declaring ready for demo:

- [ ] All verification commands pass
- [ ] All manual tests pass
- [ ] No console errors
- [ ] Performance is acceptable
- [ ] Mobile responsive
- [ ] Documentation is complete
- [ ] Code is clean (no linter errors)
- [ ] All files committed to version control

---

## Success Criteria

✅ **ALL TESTS PASSED?**
- [ ] Yes → Ready for demo!
- [ ] No → Review error logs, check troubleshooting section above

---

## Quick Reference

**Key Files:**
- `services/context_engineering/context_builder.py` - Context builder implementation
- `services/agentic_rag/planner.py` - Planning agent
- `services/agentic_rag/executor.py` - Tool executor
- `phase4_dashboard/components/visualization_components.py` - UI components
- `phase4_dashboard/pages/18_🤖_Secure_AI_Chatbot.py` - Enhanced chatbot
- `phase4_dashboard/pages/8_🎓_AI_Capabilities_Demo.py` - Demo page
- `phase4_dashboard/pages/11_💰_ROI_Calculator.py` - Enhanced ROI calculator
- `docs/CONTEXT_ENGINEERING_AGENTIC_RAG.md` - Documentation

**Key Commands:**
```bash
# Start Streamlit
cd phase4_dashboard
streamlit run app.py

# Run integration tests
cd Artifacts/project
python test_integration.py

# Check imports
python -c "from services.context_engineering import HierarchicalContextBuilder; print('OK')"
```

---

**Last Updated:** [Current Date]
**Version:** 1.0



