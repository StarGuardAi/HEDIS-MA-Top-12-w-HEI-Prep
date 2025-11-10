# ⚡ Quick Start Testing - 5 Minutes

**For:** Recruiters, Hiring Managers, Quick Reviewers

---

## 🚀 Fastest Option: Live Demo (2 minutes)

1. **Visit:** [https://hedis-ma-top-12-w-hei-prep.streamlit.app/](https://hedis-ma-top-12-w-hei-prep.streamlit.app/)
2. **Explore:**
   - Star Rating Simulator
   - ROI Calculator
   - ML Model Explorer
   - All 10 dashboard pages

**✅ Done!** You've seen the project in action.

---

## 🧪 Run Tests Locally (5 minutes)

### Windows:
```bash
cd project
run_tests.bat
```

### Mac/Linux:
```bash
cd project
chmod +x run_tests.sh
./run_tests.sh
```

### Python (Any OS):
```bash
cd project
pip install -r requirements-full.txt
pytest tests/ -v --cov=src --cov-report=html
```

**Expected:** 200+ tests passing, 99% coverage

---

## 📊 View Test Results

After running tests, open coverage report:
- **Location:** `project/htmlcov/index.html`
- **Shows:** Code coverage, test results, line-by-line analysis

---

## 📚 More Information

- **Full Testing Guide:** [TESTING_GUIDE.md](TESTING_GUIDE.md)
- **Recruiter Guide:** [FOR_RECRUITERS.md](FOR_RECRUITERS.md)
- **Demo Script:** `python demo_showcase.py`

---

**That's it! You're ready to evaluate the project.**


