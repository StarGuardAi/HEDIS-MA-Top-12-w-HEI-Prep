# 🌟 StarGuard AI - HEDIS Portfolio Optimizer

> AI-powered decision platform for Medicare Advantage Star Ratings optimization

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.30+-red.svg)](https://streamlit.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🎯 Overview

StarGuard AI helps healthcare managers optimize HEDIS measure performance and Medicare Advantage Star Ratings through predictive analytics and AI-powered insights.

**Key Features:**
- 🤖 AI-powered gap closure predictions (93% recall)
- 💰 Real-time ROI calculations ($935K+ annual value)
- ⭐ Star Rating impact modeling
- 📊 Interactive scenario planning
- 📱 Mobile-responsive design

## 🚀 Quick Start

```bash
# Clone repository
git clone https://github.com/yourusername/hedis-portfolio-optimizer.git
cd hedis-portfolio-optimizer

# Install dependencies
pip install -r requirements.txt

# Run application
streamlit run app_new.py
```

## 📁 Project Structure

```
hedis-portfolio-optimizer/
├── app_new.py              # Main entry point (new architecture)
├── app.py                  # Legacy entry point (backward compatible)
├── config/                 # Configuration
│   ├── __init__.py
│   └── settings.py         # APP_CONFIG, DATA_CONFIG, etc.
├── src/                    # Source code
│   ├── data/              # Data loading & processing
│   │   ├── __init__.py
│   │   └── loaders.py     # Data loading functions
│   ├── models/            # Business logic & ML models
│   │   ├── __init__.py
│   │   └── calculator.py  # ROI, Star Rating calculators
│   ├── ui/                # UI components & pages
│   │   ├── __init__.py
│   │   ├── layout.py      # Page setup & header
│   │   ├── components/     # Reusable components
│   │   │   ├── __init__.py
│   │   │   └── metrics.py # Metric cards
│   │   └── pages/         # Page modules
│   │       ├── __init__.py
│   │       ├── dashboard.py
│   │       ├── measures.py
│   │       ├── members.py
│   │       └── analytics.py
│   └── utils/             # Utilities
│       ├── __init__.py
│       ├── state.py       # Session state management
│       └── cache.py       # Caching utilities
├── tests/                 # Test suite
│   ├── conftest.py        # Pytest fixtures
│   └── test_calculators.py
├── utils/                 # Legacy utilities (backward compatible)
├── pages/                 # Legacy pages (backward compatible)
└── docs/                  # Documentation
```

## 🏗️ Architecture

### Clean Separation of Concerns

- **`config/`**: Application configuration and constants
- **`src/data/`**: Data loading with caching
- **`src/models/`**: Business logic and calculations
- **`src/ui/`**: Presentation layer (pages and components)
- **`src/utils/`**: Shared utilities

### Key Principles

1. **Separation of Concerns**: Business logic separated from UI
2. **Reusability**: Components and utilities are reusable
3. **Testability**: All business logic is easily testable
4. **Maintainability**: Clear structure, easy to navigate
5. **Type Safety**: Comprehensive type hints throughout

## 📖 Usage Examples

### Loading Data

```python
from src.data.loaders import load_member_data, load_measures_data

# Load member data
members_df = load_member_data(
    date_range=('2024-01-01', '2024-12-31'),
    measures=['HbA1c_Testing', 'BP_Control']
)

# Load measures data
measures_df = load_measures_data()
```

### Business Calculations

```python
from src.models.calculator import ROICalculator, StarRatingCalculator

# Calculate ROI
calculator = ROICalculator()
roi_result = calculator.calculate_intervention_roi(
    members_df,
    intervention_cost_per_member=50
)

# Calculate Star Rating impact
impact = StarRatingCalculator.calculate_measure_impact(
    current_rate=85.0,
    predicted_rate=90.0,
    measure_weight=3.0
)
```

### UI Components

```python
from src.ui.components.metrics import render_kpi_summary

render_kpi_summary(
    roi_percentage=498,
    star_rating=4.5,
    member_count=10000,
    compliance_rate=85
)
```

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_calculators.py
```

## 🔧 Configuration

All configuration is centralized in `config/settings.py`:

- `APP_CONFIG`: Application settings (title, icon, layout)
- `DATA_CONFIG`: Data settings (cache TTL, max rows)
- `MODEL_CONFIG`: Model settings (thresholds, confidence)
- `UI_CONFIG`: UI settings (colors, chart heights)
- `HEDIS_MEASURES`: HEDIS measure definitions

## 📚 Documentation

- **Architecture**: See `ARCHITECTURE.md` for detailed architecture documentation
- **Migration**: See `MIGRATION_GUIDE.md` for migrating from old structure
- **Quick Reference**: See `QUICK_REFERENCE.md` for common patterns

## 🚦 Migration from Legacy Structure

The new architecture (`app_new.py`) works alongside the existing structure:

1. **Gradual Migration**: Migrate pages one at a time
2. **Backward Compatible**: Old `app.py` still works
3. **Shared Utilities**: Both use same `utils/` directory

To switch to new architecture:
```bash
# Rename old app.py
mv app.py app_legacy.py

# Use new app
mv app_new.py app.py

# Run
streamlit run app.py
```

## 🤝 Contributing

1. Follow the architecture patterns in `src/`
2. Add tests for new business logic
3. Update documentation
4. Use type hints throughout

## 📄 License

MIT License - see LICENSE file for details

## 👤 Author

**Robert Reichert**
- 📧 Email: reichert.starguardai@gmail.com
- 🔗 LinkedIn: [sentinel-analytics](https://www.linkedin.com/in/sentinel-analytics/)
- 💻 GitHub: [HEDIS-MA-Top-12-w-HEI-Prep](https://github.com/StarGuardAi/HEDIS-MA-Top-12-w-HEI-Prep/blob/main/README.md)
- 🎨 Portfolio: [Canva Portfolio](https://www.canva.com/design/DAG2WzhiLwM/N_iXUe3eEKL3dzQ2M_0PgQ/edit)

---

**Built with ❤️ for healthcare innovation**

