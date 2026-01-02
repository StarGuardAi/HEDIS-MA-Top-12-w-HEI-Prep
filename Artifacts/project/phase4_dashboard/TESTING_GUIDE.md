# Testing Strategy Guide

## Overview

Comprehensive testing strategy for HEDIS Portfolio Optimizer with >80% code coverage across unit, integration, UI, performance, validation, and accessibility tests.

## Test Categories

### 1. Unit Tests

**Purpose**: Test individual functions in isolation

**Coverage**:
- Data loading functions
- Calculation accuracy (ROI, predictions, metrics)
- Filter logic
- Data transformations

**Location**: `tests/unit/`

**Example**:
```python
def test_roi_calculation_accuracy(roi_calculator):
    """Test ROI calculation returns correct values."""
    roi = roi_calculator.calculate_measure_roi("HBA1C")
    assert roi["net_roi"] == roi["total_benefit"] - roi["total_costs"]
```

### 2. Integration Tests

**Purpose**: Test end-to-end workflows

**Coverage**:
- Complete workflow execution
- Data pipeline: load → transform → display
- Navigation flows
- State management

**Location**: `tests/integration/`

**Example**:
```python
def test_campaign_workflow_complete(campaign_builder):
    """Test complete campaign building workflow."""
    members = campaign_builder.get_available_members()
    metrics = campaign_builder.calculate_campaign_metrics(member_ids)
    campaign = campaign_builder.create_campaign(name, member_ids)
    assert campaign is not None
```

### 3. UI Tests

**Purpose**: Test user interface and interactions

**Coverage**:
- Responsive breakpoints (375px, 768px, 1920px)
- Button interactions
- Form submissions
- Chart rendering

**Framework**: Playwright

**Location**: `tests/ui/`

**Example**:
```python
def test_responsive_breakpoints(page: Page, width, height):
    """Test layout at different screen sizes."""
    page.set_viewport_size({"width": width, "height": height})
    page.goto("http://localhost:8501")
    # Verify layout is correct
```

### 4. Performance Tests

**Purpose**: Benchmark performance and stress testing

**Coverage**:
- Load time benchmarks (target: <3s desktop, <2s mobile)
- Stress test with 10K+ rows
- Memory usage monitoring
- Caching effectiveness

**Location**: `tests/performance/`

**Example**:
```python
@pytest.mark.performance
def test_scenario_calculation_speed(scenario_modeler):
    """Test scenario calculation completes in < 1 second."""
    start_time = time.time()
    scenario = scenario_modeler.calculate_scenario(250000, 5)
    elapsed = time.time() - start_time
    assert elapsed < 1.0
```

### 5. Data Validation Tests

**Purpose**: Test edge cases and data handling

**Coverage**:
- Missing data handling
- Edge cases (0 members, null values)
- Date range validation
- Calculation boundaries

**Location**: `tests/validation/`

**Example**:
```python
def test_campaign_with_empty_member_list(campaign_builder):
    """Test campaign handles empty member list."""
    metrics = campaign_builder.calculate_campaign_metrics([])
    assert metrics["total_members"] == 0
```

### 6. Accessibility Tests

**Purpose**: Ensure WCAG AA compliance

**Coverage**:
- Screen reader compatibility
- Keyboard navigation
- Color contrast ratios
- Touch target sizes (44px minimum)

**Location**: `tests/accessibility/`

**Example**:
```python
@pytest.mark.accessibility
def test_keyboard_navigation(page: Page):
    """Test keyboard navigation works."""
    page.goto("http://localhost:8501")
    page.keyboard.press("Tab")
    focused = page.evaluate("document.activeElement")
    assert focused is not None
```

## Running Tests

### Install Dependencies
```bash
pip install -r requirements.txt
playwright install chromium
```

### Run All Tests
```bash
pytest
```

### Run by Category
```bash
# Unit tests
pytest -m unit

# Integration tests
pytest -m integration

# UI tests (requires Streamlit running)
pytest -m ui

# Performance tests
pytest -m performance

# Accessibility tests
pytest -m accessibility
```

### Run with Coverage
```bash
pytest --cov=utils --cov=pages --cov-report=html
```

Coverage report will be in `htmlcov/index.html`

## Coverage Goals

- **Overall**: >80% code coverage
- **Critical Functions**: 100% coverage
- **Utilities**: >90% coverage
- **Pages**: >70% coverage

## Test Fixtures

### Database Fixture
Creates temporary SQLite database with test data:
```python
@pytest.fixture
def temp_db():
    """Create temporary database for testing."""
    # Creates test database
    # Yields path
    # Cleans up after test
```

### Component Fixtures
Pre-configured instances:
- `scenario_modeler`: ScenarioModeler instance
- `campaign_builder`: CampaignBuilder instance
- `roi_calculator`: ROICalculator instance
- `historical_tracker`: HistoricalTracker instance
- `alert_system`: AlertSystem instance

## Performance Benchmarks

### Load Time Targets
- **Desktop**: <3 seconds for page load
- **Mobile**: <2 seconds for page load
- **Calculations**: <1 second for scenario/ROI calculations
- **Data Loading**: <2 seconds for query execution

### Stress Test Targets
- **10K Members**: Handle in <5 seconds
- **100 Scenarios**: Calculate in <10 seconds
- **Large Queries**: Execute without timeout

## Best Practices

### Writing Tests
1. **Test One Thing**: Each test should verify one behavior
2. **Use Descriptive Names**: Test names should describe what they test
3. **Arrange-Act-Assert**: Structure tests clearly
4. **Use Fixtures**: Reuse test data and setup
5. **Test Edge Cases**: Include boundary conditions

### Maintaining Tests
1. **Keep Tests Fast**: Unit tests should be <1 second
2. **Isolate Tests**: Tests should not depend on each other
3. **Clean Up**: Use fixtures for setup/teardown
4. **Update Tests**: Keep tests in sync with code changes
5. **Review Coverage**: Ensure critical paths are covered

## Continuous Integration

### Pre-commit Checks
- Run unit tests
- Check code coverage
- Lint code

### CI Pipeline
1. Install dependencies
2. Run all tests
3. Generate coverage report
4. Check coverage threshold (>80%)
5. Run UI tests (if applicable)

## Troubleshooting

### Tests Failing
- **Database Issues**: Check database connection and test data
- **Import Errors**: Verify PYTHONPATH includes project root
- **Missing Dependencies**: Install all requirements
- **Timing Issues**: Add appropriate waits for async operations

### Coverage Low
- **Review Report**: Check `htmlcov/index.html`
- **Add Tests**: Focus on uncovered critical paths
- **Exclude Non-Critical**: Mark non-testable code appropriately

### UI Tests Failing
- **App Not Running**: Start Streamlit app before UI tests
- **Browser Issues**: Verify Playwright is installed correctly
- **Timing**: Add appropriate waits for page loads

## Test Data

### Temporary Database
- Created per test session
- Populated with sample data
- Automatically cleaned up

### Sample Data Includes
- Member interventions
- HEDIS measures
- Intervention activities
- Budget allocations

## Markers

Use pytest markers to categorize tests:
- `@pytest.mark.unit`: Unit tests
- `@pytest.mark.integration`: Integration tests
- `@pytest.mark.ui`: UI tests
- `@pytest.mark.performance`: Performance tests
- `@pytest.mark.stress`: Stress tests
- `@pytest.mark.accessibility`: Accessibility tests
- `@pytest.mark.slow`: Slow running tests

## Example Test Structure

```python
import pytest
from utils.roi_calculator import ROICalculator

class TestROICalculations:
    """Test ROI calculation accuracy."""
    
    def test_basic_roi_calculation(self, roi_calculator):
        """Test basic ROI calculation."""
        roi = roi_calculator.calculate_measure_roi("HBA1C")
        assert roi is not None
        assert "net_roi" in roi
    
    def test_roi_with_custom_config(self, roi_calculator):
        """Test ROI with custom configuration."""
        config = {"revenue_per_closure": 120.0}
        roi = roi_calculator.calculate_measure_roi("HBA1C", config=config)
        assert roi["total_revenue"] > 0
```

## Support

For testing questions:
- Review test examples in `tests/` directory
- Check pytest documentation
- Review coverage reports
- Consult team for test patterns

## Support

For questions or issues:
- 📧 **Email**: reichert.starguardai@gmail.com
- 🔗 **LinkedIn**: [sentinel-analytics](https://www.linkedin.com/in/sentinel-analytics/)
- 💻 **GitHub**: [HEDIS-MA-Top-12-w-HEI-Prep](https://github.com/StarGuardAi/HEDIS-MA-Top-12-w-HEI-Prep/blob/main/README.md)
- 🎨 **Portfolio**: [Canva Portfolio](https://www.canva.com/design/DAG2WzhiLwM/N_iXUe3eEKL3dzQ2M_0PgQ/edit)

---

**Testing Strategy** | Part of HEDIS Portfolio Optimizer | Comprehensive Quality Assurance

