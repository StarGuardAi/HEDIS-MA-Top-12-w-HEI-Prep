# 📋 PHASE C: TESTING & QA STRATEGY

**Date:** October 26, 2025  
**Status:** Strategy document for test fixes and quality assurance  
**Goal:** Fix failing tests, add integration tests, achieve 95%+ coverage

---

## 🎯 **PHASE C OBJECTIVES**

### C1: Fix 43 Failing Measure Tests
**Current Status:** 43 of 132 tests failing (67% pass rate)  
**Target:** 100% pass rate  
**Estimated Time:** 3-4 hours

### C2: Add Integration Tests  
**Current Status:** Limited integration test coverage  
**Target:** Full API workflow integration tests  
**Estimated Time:** 1-2 hours

### C3: Achieve 95%+ Test Coverage
**Current Status:** Coverage not measured  
**Target:** 95%+ code coverage  
**Estimated Time:** 1-2 hours

---

## 📊 **CURRENT TEST STATUS**

### Test Results Summary
```
Total Tests: 132
Passing: 89 (67%)
Failing: 43 (33%)
```

### Likely Failure Reasons
1. **Test signature mismatches** - Function parameters changed but tests not updated
2. **Missing test data** - Data loaders need updated test fixtures
3. **API endpoint changes** - New HEI endpoints not in old tests
4. **Import errors** - Refactored code, imports need updating

---

## 🔧 **C1: FIXING FAILING TESTS**

### Strategy

**Step 1: Run tests and categorize failures**
```bash
pytest tests/ -v --tb=short > test_failures.txt
```

**Step 2: Group failures by type**
- Import errors (quick fix)
- Signature mismatches (parameter updates)
- Missing fixtures (data setup)
- Logic errors (actual bugs)

**Step 3: Fix by priority**
1. Import errors (5-10 min)
2. Signature mismatches (1-2 hours)
3. Missing fixtures (30-60 min)
4. Logic errors (1-2 hours)

### Expected Test File Updates

**Measure Tests** (11 files):
- `tests/measures/test_gsd.py`
- `tests/measures/test_ked.py`
- `tests/measures/test_eed.py`
- `tests/measures/test_cbp.py`
- `tests/measures/test_pdc_dr.py`
- `tests/measures/test_pdc_rasa.py`
- `tests/measures/test_pdc_sta.py`
- `tests/measures/test_bpd.py`
- `tests/measures/test_supd.py`
- `tests/measures/test_bcs.py`
- `tests/measures/test_col.py`

**HEI Tests** (1 file):
- `tests/utils/test_hei_calculator.py` ← Already passing!

**API Tests** (3-4 files):
- `tests/api/test_equity_endpoints.py` ← New endpoints
- `tests/api/test_prediction_endpoints.py`
- `tests/api/test_portfolio_endpoints.py`

### Quick Fix Template

For signature mismatches:
```python
# OLD (failing)
def test_calculate_gsd(calculator):
    result = calculator.calculate_gsd(member_id, claims_df)
    
# NEW (fixed)
def test_calculate_gsd(calculator):
    result = calculator.calculate_gsd(
        member_id=member_id,
        claims_df=claims_df,
        labs_df=labs_df,  # New required parameter
        measurement_year=2025
    )
```

---

## 🧪 **C2: INTEGRATION TESTS**

### Coverage Needed

**API Workflow Tests:**
1. **Prediction Workflow**
   - Request prediction → Get result → Verify format
   - Test all 12 measure prediction endpoints

2. **Portfolio Workflow**
   - Request portfolio analysis → Get optimization → Verify recommendations

3. **HEI Workflow** (NEW)
   - Request equity analysis → Get disparities → Get interventions
   - Test all 4 new HEI endpoints

4. **Analytics Workflow**
   - Request performance metrics → Get trends → Verify calculations

### Integration Test Template

```python
# tests/integration/test_api_workflows.py

import pytest
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_gsd_prediction_workflow():
    """Test complete GSD prediction workflow"""
    # Step 1: Request prediction
    response = client.post("/api/v1/predict/gsd", json={
        "member_id": "M12345",
        "claims_data": [...],
        "labs_data": [...]
    })
    assert response.status_code == 200
    
    # Step 2: Verify prediction structure
    data = response.json()
    assert "prediction" in data
    assert "risk_score" in data
    assert "confidence" in data
    
    # Step 3: Verify prediction values
    assert 0 <= data["risk_score"] <= 1
    assert data["prediction"] in ["low_risk", "high_risk"]

def test_hei_equity_analysis_workflow():
    """Test complete HEI equity analysis workflow"""
    # Step 1: Analyze equity
    response = client.post("/api/v1/equity/analyze", json={
        "measure_results": [...],
        "hei_data": [...]
    })
    assert response.status_code == 200
    
    # Step 2: Get equity score
    score_response = client.post("/api/v1/equity/score", json={...})
    assert score_response.status_code == 200
    
    # Step 3: Get interventions
    interventions = client.post("/api/v1/equity/interventions", json={...})
    assert interventions.status_code == 200
```

---

## 📈 **C3: TEST COVERAGE**

### Coverage Tools Setup

```bash
# Install coverage
pip install pytest-cov

# Run tests with coverage
pytest tests/ --cov=src --cov-report=html --cov-report=term

# View coverage report
open htmlcov/index.html
```

### Coverage Targets by Module

| Module | Current | Target | Priority |
|--------|---------|--------|----------|
| `src/measures/` | Unknown | 95%+ | HIGH |
| `src/api/` | Unknown | 90%+ | HIGH |
| `src/utils/hei_calculator.py` | ~90% | 95%+ | MEDIUM |
| `src/data/` | Unknown | 85%+ | MEDIUM |
| `src/models/` | Unknown | 90%+ | HIGH |

### Coverage Improvement Strategy

1. **Identify uncovered lines**
   ```bash
   pytest --cov=src --cov-report=term-missing
   ```

2. **Add tests for uncovered code**
   - Focus on critical paths first
   - Error handling branches
   - Edge cases

3. **Achieve 95%+ overall**
   - Measures: 95%+
   - API: 90%+
   - Utils: 95%+
   - Data: 85%+

---

## 🚀 **EXECUTION PLAN**

### Phase C Timeline

**Day 1 (4-6 hours):**
1. Run full test suite, categorize failures (30 min)
2. Fix import errors (30 min)
3. Fix signature mismatches (2 hours)
4. Fix missing fixtures (1 hour)
5. Fix logic errors (1-2 hours)

**Day 2 (2-3 hours):**
6. Add integration tests (1-2 hours)
7. Measure and improve coverage (1 hour)
8. Final test run, verify 100% pass (30 min)

### Success Criteria

✅ **C1:** All 132 tests passing (100%)  
✅ **C2:** Integration tests for all API workflows  
✅ **C3:** 95%+ code coverage  
✅ **Documentation:** Test results documented

---

## 📝 **TESTING BEST PRACTICES**

### For This Project

1. **Use Fixtures**
   - Create reusable test data in `tests/conftest.py`
   - Parameterize tests for multiple scenarios

2. **Mock External Dependencies**
   - Mock database calls
   - Mock API calls to external services
   - Use in-memory data for tests

3. **Test Edge Cases**
   - Null/None values
   - Empty datasets
   - Invalid inputs
   - Boundary conditions

4. **Healthcare-Specific Tests**
   - Verify Criminal Intelligence Database spec compliance
   - Test age calculations (off-by-one errors common)
   - Test date logic (measurement year boundaries)
   - Test exclusion criteria

---

## 🎯 **PHASE C DELIVERABLES**

1. ✅ **All Tests Passing** - 132/132 tests (100%)
2. ✅ **Integration Test Suite** - API workflow tests
3. ✅ **Coverage Report** - 95%+ overall coverage
4. ✅ **Test Documentation** - Results and strategy documented

---

## 💡 **RECOMMENDATIONS**

### Immediate Actions

1. **Run pytest with verbose output** to see all failures
2. **Group failures by type** for efficient fixing
3. **Fix import errors first** (quick wins)
4. **Update test fixtures** for new measure logic
5. **Add integration tests** for HEI endpoints

### Long-Term

1. **CI/CD Integration** - Auto-run tests on every commit
2. **Pre-commit Hooks** - Run tests before allowing commits
3. **Coverage Monitoring** - Track coverage over time
4. **Automated Test Generation** - Use tools like Hypothesis for property-based testing

---

**Status:** ✅ **Strategy Complete - Ready for Implementation**  
**Next:** Run tests, fix failures, add integration tests, measure coverage

**Last Updated:** October 26, 2025



---
*This file is maintained by Sentinel Analytics. For inquiries, contact reichert.sentinel.ai@gmail.com.*
