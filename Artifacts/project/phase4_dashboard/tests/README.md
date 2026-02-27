# HEDIS Portfolio Optimizer - Test Suite

Comprehensive testing strategy with >80% code coverage.

## Test Structure

```
tests/
├── unit/              # Unit tests for individual functions
│   ├── test_data_loading.py
│   ├── test_calculations.py
│   ├── test_filters.py
│   └── test_data_transformations.py
├── integration/       # Integration tests for workflows
│   ├── test_workflows.py
│   └── test_data_pipeline.py
├── performance/       # Performance and stress tests
│   └── test_load_times.py
├── validation/        # Data validation and edge cases
│   └── test_edge_cases.py
├── ui/               # UI tests with Playwright
│   └── test_responsive.py
├── accessibility/    # Accessibility tests
│   └── test_a11y.py
├── conftest.py       # Pytest fixtures
└── conftest_ui.py    # UI test fixtures
```

## Running Tests

### All Tests
```bash
pytest
```

### By Category
```bash
# Unit tests only
pytest -m unit

# Integration tests
pytest -m integration

# UI tests
pytest -m ui

# Performance tests
pytest -m performance

# Accessibility tests
pytest -m accessibility
```

### With Coverage
```bash
pytest --cov=utils --cov=pages --cov-report=html
```

### Specific Test File
```bash
pytest tests/unit/test_calculations.py
```

## Test Categories

### Unit Tests
- **Data Loading**: Test query generation and data retrieval
- **Calculations**: Test ROI, scenario, and metric calculations
- **Filters**: Test filtering logic
- **Transformations**: Test data transformation functions

### Integration Tests
- **Workflows**: End-to-end workflow testing
- **Data Pipeline**: Load → Transform → Display pipeline
- **State Management**: Test session state handling

### Performance Tests
- **Load Times**: Benchmark calculation speeds
- **Stress Tests**: Test with 10K+ rows
- **Memory Usage**: Monitor memory consumption

### UI Tests
- **Responsive Design**: Test breakpoints (375px, 768px, 1920px)
- **Button Interactions**: Test click handlers
- **Form Submissions**: Test form validation
- **Chart Rendering**: Test Plotly chart display

### Data Validation
- **Missing Data**: Test handling of null/empty data
- **Edge Cases**: Test boundary conditions
- **Date Validation**: Test date range handling
- **Calculation Boundaries**: Test extreme values

### Accessibility Tests
- **Screen Reader**: Test ARIA labels and alt text
- **Keyboard Navigation**: Test tab order and focus
- **Color Contrast**: Test WCAG AA compliance
- **Touch Targets**: Test minimum 44px size

## Coverage Goals

- **Target**: >80% code coverage
- **Critical Paths**: 100% coverage
- **Utilities**: >90% coverage
- **Pages**: >70% coverage

## Prerequisites

### Required Packages
```bash
pip install pytest pytest-cov pytest-playwright playwright
```

### Playwright Setup
```bash
playwright install chromium
```

## Continuous Integration

Tests should run:
- On every commit
- Before merging PRs
- On scheduled basis (nightly)

## Test Data

- Uses temporary SQLite database for testing
- Creates sample data in fixtures
- Cleans up after tests

## Writing New Tests

1. **Unit Tests**: Test individual functions in isolation
2. **Integration Tests**: Test complete workflows
3. **UI Tests**: Test user interactions
4. **Performance Tests**: Benchmark critical paths

### Example Unit Test
```python
def test_calculation_accuracy(roi_calculator):
    """Test ROI calculation accuracy."""
    roi = roi_calculator.calculate_measure_roi("HBA1C")
    assert roi["net_roi"] >= 0
    assert "roi_ratio" in roi
```

### Example Integration Test
```python
def test_campaign_workflow(campaign_builder):
    """Test complete campaign workflow."""
    members = campaign_builder.get_available_members()
    metrics = campaign_builder.calculate_campaign_metrics(member_ids)
    campaign = campaign_builder.create_campaign(name, member_ids)
    assert campaign is not None
```

## Troubleshooting

### Tests Failing
- Check database connection
- Verify test data exists
- Check dependencies installed
- Review error messages

### Coverage Low
- Add tests for uncovered code
- Review coverage report
- Focus on critical paths

### UI Tests Failing
- Ensure Streamlit app is running
- Check Playwright is installed
- Verify browser can access app

## Support

For questions or issues:
- 📧 **Email**: reichert.starguardai@gmail.com
- 🔗 **LinkedIn**: [sentinel-analytics](https://www.linkedin.com/in/sentinel-analytics/)
- 💻 **GitHub**: [HEDIS-MA-Top-12-w-HEI-Prep](https://github.com/StarGuardAi/HEDIS-MA-Top-12-w-HEI-Prep/blob/main/README.md)
- 🎨 **Portfolio**: [Canva Portfolio](https://www.canva.com/design/DAG2WzhiLwM/N_iXUe3eEKL3dzQ2M_0PgQ/edit)

---

**Test Suite** | Part of HEDIS Portfolio Optimizer | Comprehensive Quality Assurance

