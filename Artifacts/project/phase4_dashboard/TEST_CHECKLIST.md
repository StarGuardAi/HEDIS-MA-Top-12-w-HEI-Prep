# Test Checklist

Quick reference checklist for running and verifying tests.

## Pre-Test Setup

- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Install Playwright: `playwright install chromium`
- [ ] Verify database connection (if needed)
- [ ] Start Streamlit app (for UI tests): `streamlit run app.py`

## Running Tests

### Quick Test Run
- [ ] Run all tests: `pytest`
- [ ] Check exit code is 0 (all tests passed)
- [ ] Review any warnings or skipped tests

### Coverage Check
- [ ] Run with coverage: `pytest --cov=utils --cov=pages --cov-report=html`
- [ ] Open coverage report: `htmlcov/index.html`
- [ ] Verify coverage >80%
- [ ] Review uncovered code

### Category Tests
- [ ] Unit tests: `pytest -m unit`
- [ ] Integration tests: `pytest -m integration`
- [ ] Performance tests: `pytest -m performance`
- [ ] Validation tests: `pytest -m validation`
- [ ] UI tests: `pytest -m ui` (requires app running)
- [ ] Accessibility tests: `pytest -m accessibility`

## Test Categories Verification

### Unit Tests
- [ ] Data loading functions tested
- [ ] Calculation accuracy verified
- [ ] Filter logic tested
- [ ] Data transformations tested
- [ ] Workload balancing tested
- [ ] Forecasting tested
- [ ] Alert generation tested

### Integration Tests
- [ ] Scenario workflow tested
- [ ] Campaign workflow tested
- [ ] ROI workflow tested
- [ ] Alert workflow tested
- [ ] Data pipeline tested
- [ ] State management tested

### Performance Tests
- [ ] Load time benchmarks met
- [ ] Stress tests passed
- [ ] Large dataset handling verified

### Validation Tests
- [ ] Missing data handling tested
- [ ] Null value handling tested
- [ ] Date validation tested
- [ ] Boundary conditions tested

### UI Tests
- [ ] Responsive breakpoints tested
- [ ] Button interactions tested
- [ ] Chart rendering tested

### Accessibility Tests
- [ ] Keyboard navigation tested
- [ ] Screen reader compatibility tested
- [ ] Color contrast verified
- [ ] Touch target sizes verified

## Post-Test Verification

- [ ] All tests pass
- [ ] Coverage >80%
- [ ] No critical warnings
- [ ] Test artifacts cleaned up
- [ ] Documentation updated if needed

## Troubleshooting

### Tests Failing
- [ ] Check database connection
- [ ] Verify test data exists
- [ ] Check dependencies installed
- [ ] Review error messages

### Coverage Low
- [ ] Review coverage report
- [ ] Add tests for uncovered code
- [ ] Focus on critical paths

### UI Tests Failing
- [ ] Ensure Streamlit app is running
- [ ] Check Playwright installation
- [ ] Verify browser access

## Support

For questions or issues:
- 📧 **Email**: reichert.starguardai@gmail.com
- 🔗 **LinkedIn**: [sentinel-analytics](https://www.linkedin.com/in/sentinel-analytics/)
- 💻 **GitHub**: [HEDIS-MA-Top-12-w-HEI-Prep](https://github.com/StarGuardAi/HEDIS-MA-Top-12-w-HEI-Prep/blob/main/README.md)
- 🎨 **Portfolio**: [Canva Portfolio](https://www.canva.com/design/DAG2WzhiLwM/N_iXUe3eEKL3dzQ2M_0PgQ/edit)

---

**Test Checklist** | Use before committing code | Ensure quality

