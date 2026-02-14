# StarGuard AI Mobile Companion App

Medicare Advantage analytics platform for portfolio/consulting launch.

**Target Completion:** 6 weeks (February–March 2026)  
**Owner:** Robert Reichert  
**Version:** 1.0

## Setup

```bash
# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate   # Windows
# source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt
```

## Run

```bash
# From starguard-mobile directory (with venv activated):
shiny run app.app --port 8000

# Or use the run script:
shiny run run:app --port 8000
```

## Project Structure

```
starguard-mobile/
├── app/
│   ├── __init__.py
│   ├── app.py
│   ├── pages/
│   ├── components/
│   ├── utils/
│   ├── assets/
│   └── data/
├── tests/
├── docs/
├── requirements.txt
└── README.md
```
