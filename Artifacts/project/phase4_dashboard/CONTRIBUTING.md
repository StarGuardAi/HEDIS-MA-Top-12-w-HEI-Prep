# Contributing to HEDIS Portfolio Optimizer

Thank you for your interest in contributing to this project! This document outlines the development practices and standards we follow to maintain production-grade code quality and HIPAA compliance.

---

## 📋 Code of Conduct

### Our Standards

We are committed to maintaining a professional, respectful, and inclusive environment. As contributors, we:

- **Respect all team members** and their contributions
- **Prioritize security and compliance** in all code changes
- **Maintain professional communication** in all interactions
- **Follow healthcare data privacy standards** rigorously

### Healthcare Data Responsibility

This project demonstrates architecture for handling protected health information (PHI). All contributors must:

- ✅ Never commit PHI or sensitive data to the repository
- ✅ Follow HIPAA compliance best practices
- ✅ Report security concerns immediately
- ✅ Understand the implications of healthcare data handling

**Security and compliance are not optional—they are fundamental requirements.**

---

## 🚀 Development Setup

### Prerequisites

- **Python 3.9+** (3.11+ recommended)
- **PostgreSQL 12+** (for database development)
- **Git** (for version control)
- **8GB+ RAM** (for local AI components)

### Initial Setup

```bash
# 1. Fork and clone the repository
git clone https://github.com/yourusername/hedis-portfolio-optimizer.git
cd hedis-portfolio-optimizer

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# 4. Install development dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Development tools

# 5. Set up pre-commit hooks
pre-commit install

# 6. Configure environment variables
cp .env.example .env
# Edit .env with your local database credentials (NEVER commit .env)
```

### Development Database

```bash
# Create local development database
createdb hedis_portfolio_dev

# Run migrations
python scripts/initialize_database.py --env dev

# Load sample data (de-identified only)
python scripts/load_sample_data.py --env dev
```

### Verify Setup

```bash
# Run tests to verify setup
pytest tests/

# Check code formatting
black --check .
flake8 .

# Start development server
streamlit run app.py
```

---

## 📝 Code Standards

### Python Style Guide

We follow **PEP 8** with the following specific requirements:

#### Code Formatting

- **Line length:** Maximum 100 characters (88 for Black compatibility)
- **Indentation:** 4 spaces (no tabs)
- **Quotes:** Double quotes for strings (Black default)
- **Imports:** Sorted and grouped (isort)

```python
# ✅ GOOD
from typing import List, Optional
import pandas as pd
from utils.database import execute_query

# ❌ BAD
import pandas as pd
from utils.database import execute_query
from typing import List, Optional
```

#### Type Hints

**All functions must include type hints:**

```python
# ✅ GOOD
def calculate_roi(
    intervention_cost: float,
    quality_bonus: float,
    member_count: int
) -> float:
    """Calculate ROI ratio for interventions."""
    return (quality_bonus * member_count) / intervention_cost

# ❌ BAD
def calculate_roi(intervention_cost, quality_bonus, member_count):
    return (quality_bonus * member_count) / intervention_cost
```

#### Docstrings

**All functions, classes, and modules must have docstrings:**

```python
def get_available_members(
    measure_id: Optional[str] = None,
    status_filter: List[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
) -> pd.DataFrame:
    """
    Get list of members available for campaign selection.
    
    Args:
        measure_id: Filter by specific HEDIS measure ID
        status_filter: List of intervention statuses to include
        start_date: Filter by intervention date start (YYYY-MM-DD)
        end_date: Filter by intervention date end (YYYY-MM-DD)
    
    Returns:
        DataFrame with member information including:
        - member_id
        - measure_id
        - intervention_date
        - status
        - cost_per_intervention
    
    Raises:
        DatabaseError: If query execution fails
        ValueError: If date format is invalid
    
    Example:
        >>> members = get_available_members(
        ...     measure_id="CDC",
        ...     status_filter=["pending", "scheduled"],
        ...     start_date="2024-01-01",
        ...     end_date="2024-12-31"
        ... )
        >>> len(members)
        150
    """
    # Implementation...
```

### Code Quality Tools

We use automated tools to maintain code quality:

```bash
# Format code
black .

# Sort imports
isort .

# Lint code
flake8 .

# Type checking
mypy .

# Run all checks
pre-commit run --all-files
```

### File Organization

```
project/
├── app.py                 # Main Streamlit application
├── pages/                 # Streamlit page modules
├── utils/                 # Utility modules
│   ├── database.py        # Database operations
│   ├── queries.py         # SQL queries
│   └── ...
├── src/                   # Source code modules
│   ├── services/          # Business logic services
│   └── ...
├── tests/                 # Test files
│   ├── unit/              # Unit tests
│   ├── integration/       # Integration tests
│   └── ...
├── scripts/               # Utility scripts
└── docs/                  # Documentation
```

---

## 🔒 Security Requirements

### Critical Security Rules

**These rules are non-negotiable and will result in immediate rejection of contributions if violated:**

#### 1. No PHI in Commits

**NEVER commit:**
- ❌ Protected Health Information (PHI)
- ❌ Real patient data
- ❌ Member IDs from production systems
- ❌ Any personally identifiable information (PII)

**ALWAYS use:**
- ✅ De-identified sample data
- ✅ Synthetic test data
- ✅ Anonymized identifiers (e.g., "MEMBER_001")
- ✅ Data generators for testing

```python
# ✅ GOOD - De-identified data
member_id = "DEMO_MEMBER_001"
member_name = "Test Member"

# ❌ BAD - Real PHI
member_id = "123456789"  # Real member ID
member_name = "John Doe"  # Real name
```

#### 2. Secrets Management

**NEVER commit:**
- ❌ Database passwords
- ❌ API keys
- ❌ Connection strings with credentials
- ❌ Environment variables with secrets

**ALWAYS use:**
- ✅ `.env` file (in `.gitignore`)
- ✅ Environment variables
- ✅ Secret management services (for production)
- ✅ `.env.example` for documentation

```python
# ✅ GOOD
import os
from dotenv import load_dotenv

load_dotenv()
db_password = os.getenv("DB_PASSWORD")

# ❌ BAD
db_password = "my_secret_password"  # Hardcoded secret
```

#### 3. SQL Injection Prevention

**ALWAYS use parameterized queries:**

```python
# ✅ GOOD - Parameterized query
query = "SELECT * FROM members WHERE measure_id = %s"
execute_query(query, (measure_id,))

# ❌ BAD - String formatting (SQL injection risk)
query = f"SELECT * FROM members WHERE measure_id = '{measure_id}'"
execute_query(query)
```

#### 4. External API Restrictions

**This project maintains zero external API exposure:**

- ❌ No calls to external APIs with PHI
- ❌ No cloud-based AI services
- ✅ All AI processing must be on-premises
- ✅ Use local LLMs (Ollama) only

### Security Checklist

Before submitting a PR, verify:

- [ ] No PHI or PII in code or commits
- [ ] No hardcoded secrets or credentials
- [ ] All database queries use parameterization
- [ ] No external API calls with sensitive data
- [ ] Environment variables used for configuration
- [ ] `.env` file in `.gitignore`
- [ ] Security-sensitive code reviewed

---

## 🧪 Testing Guidelines

### Test Structure

```
tests/
├── unit/                  # Unit tests (fast, isolated)
│   ├── test_database.py
│   ├── test_queries.py
│   └── ...
├── integration/           # Integration tests (database, services)
│   ├── test_data_pipeline.py
│   └── ...
└── fixtures/              # Test data and fixtures
    ├── sample_data.json
    └── ...
```

### Writing Tests

**All new features must include tests:**

```python
# tests/unit/test_roi_calculator.py
import pytest
from utils.roi_calculator import calculate_roi_ratio

def test_calculate_roi_ratio_positive():
    """Test ROI calculation with positive return."""
    intervention_cost = 10000.0
    quality_bonus = 50000.0
    member_count = 1000
    
    roi = calculate_roi_ratio(
        intervention_cost=intervention_cost,
        quality_bonus=quality_bonus,
        member_count=member_count
    )
    
    assert roi == pytest.approx(5.0, rel=0.01)
    assert roi > 1.0  # Positive ROI

def test_calculate_roi_ratio_zero_cost():
    """Test ROI calculation with zero cost (edge case)."""
    with pytest.raises(ValueError, match="Intervention cost must be positive"):
        calculate_roi_ratio(
            intervention_cost=0.0,
            quality_bonus=50000.0,
            member_count=1000
        )
```

### Test Requirements

- **Unit tests:** Minimum 80% code coverage
- **Integration tests:** For database operations and data pipelines
- **Edge cases:** Test error conditions and boundary values
- **Data validation:** Test with de-identified sample data only

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/unit/test_roi_calculator.py

# Run with verbose output
pytest -v

# Run only fast tests
pytest -m "not slow"
```

### Data Validation Tests

**Always validate data before processing:**

```python
def test_validate_member_data():
    """Test member data validation."""
    # Valid data
    valid_data = {
        "member_id": "DEMO_001",
        "measure_id": "CDC",
        "intervention_date": "2024-01-15",
        "status": "completed"
    }
    assert validate_member_data(valid_data) is True
    
    # Invalid data - missing required field
    invalid_data = {
        "member_id": "DEMO_001",
        # Missing measure_id
    }
    assert validate_member_data(invalid_data) is False
```

---

## 🔄 Pull Request Process

### Before Submitting

1. **Update documentation** for any new features
2. **Add tests** for new functionality
3. **Run all tests** and ensure they pass
4. **Check code formatting** (`black .`, `isort .`)
5. **Run linters** (`flake8 .`, `mypy .`)
6. **Verify security** (no PHI, no secrets)
7. **Update CHANGELOG.md** (if applicable)

### PR Title Format

```
[Type] Brief description

Examples:
[Feature] Add campaign builder coordinator assignment
[Fix] Resolve NoneType error in alert system
[Docs] Update installation instructions
[Security] Add parameterized query validation
```

### PR Description Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Security improvement
- [ ] Performance optimization

## Security Considerations
- [ ] No PHI or PII in changes
- [ ] No hardcoded secrets
- [ ] Parameterized queries used
- [ ] No external API calls with sensitive data

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] All tests passing
- [ ] Test coverage maintained/improved

## Checklist
- [ ] Code follows PEP 8 style guide
- [ ] Type hints added to all functions
- [ ] Docstrings added/updated
- [ ] Documentation updated
- [ ] CHANGELOG.md updated (if applicable)
```

### Review Process

1. **Automated checks** run on all PRs (CI/CD)
2. **Code review** by maintainers
3. **Security review** for compliance-sensitive changes
4. **Testing verification** (all tests must pass)
5. **Documentation review** (if applicable)

### After Approval

- Maintainers will merge the PR
- Your contribution will be credited in the project
- Thank you for contributing! 🎉

---

## 🏥 Healthcare Compliance Notes

### HIPAA Considerations for Contributors

This project demonstrates architecture for healthcare data processing. Contributors must understand:

#### Protected Health Information (PHI)

**PHI includes:**
- Names, addresses, phone numbers
- Medical record numbers
- Health plan beneficiary numbers
- Dates (birth, admission, discharge, death)
- Any unique identifier that could identify an individual

**In this project:**
- ✅ We use **de-identified data only**
- ✅ Sample data uses synthetic identifiers
- ✅ No real member information is processed
- ✅ All test data is anonymized

#### Compliance Requirements

**For production deployment:**
- Full HIPAA compliance audit required
- Business Associate Agreements (BAAs) if using vendors
- Access controls and audit logging
- Encryption at rest and in transit
- Incident response procedures

**For development:**
- Use only de-identified sample data
- Never commit PHI to version control
- Follow security best practices
- Understand data privacy implications

#### Data Handling Best Practices

1. **Minimize data collection:** Only collect necessary data
2. **De-identify early:** Remove PHI as soon as possible
3. **Access controls:** Limit who can access sensitive data
4. **Audit trails:** Log all data access
5. **Encryption:** Encrypt data at rest and in transit

### Compliance Checklist for Contributors

Before contributing code that handles data:

- [ ] Understand what constitutes PHI
- [ ] Verify no PHI in test data or code
- [ ] Use de-identified data only
- [ ] Follow data minimization principles
- [ ] Implement appropriate access controls
- [ ] Add audit logging where needed
- [ ] Document compliance considerations

---

## 📚 Additional Resources

### Development Resources

- [Python PEP 8 Style Guide](https://peps.python.org/pep-0008/)
- [Type Hints Documentation](https://docs.python.org/3/library/typing.html)
- [pytest Documentation](https://docs.pytest.org/)
- [Black Code Formatter](https://black.readthedocs.io/)

### Healthcare Compliance Resources

- [HIPAA Compliance Guide](https://www.hhs.gov/hipaa/index.html)
- [De-identification Standards](https://www.hhs.gov/hipaa/for-professionals/privacy/special-topics/de-identification/index.html)
- [Healthcare Data Security Best Practices](https://www.hhs.gov/hipaa/for-professionals/security/index.html)

### Project-Specific Documentation

- [Architecture Documentation](COMPLIANCE_ARCHITECTURE.md)
- [Database Schema](docs/database_schema.md)
- [API Documentation](docs/api.md)
- [Security Guidelines](docs/security.md)

---

## ❓ Questions?

If you have questions about:

- **Development setup:** Check the [README.md](README.md) or open an issue
- **Security concerns:** Contact maintainers privately (do not post in public issues)
- **HIPAA compliance:** Review [COMPLIANCE_ARCHITECTURE.md](COMPLIANCE_ARCHITECTURE.md)
- **Code standards:** Refer to this document or ask in discussions

**We're here to help!** Don't hesitate to ask questions or seek clarification.

---

## 🙏 Thank You

Thank you for contributing to this project! Your efforts help demonstrate production-grade healthcare AI architecture that maintains security and compliance standards.

**Together, we're building healthcare AI that works within regulatory constraints, not against them.**

---

<div align="center">

**Built with 🔒 security-first practices | 🏥 Healthcare AI that maintains compliance**

</div>










