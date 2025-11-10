#!/bin/bash
# Quick test runner for HEDIS Project (Mac/Linux)
# Author: Robert Reichert

echo "======================================================================"
echo "  HEDIS Project - Quick Test Runner"
echo "======================================================================"
echo ""

# Check if pytest is available
if ! python -m pytest --version > /dev/null 2>&1; then
    echo "ERROR: pytest not found!"
    echo "Please install dependencies: pip install -r requirements-full.txt"
    exit 1
fi

echo "Running comprehensive test suite..."
echo "Expected time: 2-5 minutes"
echo ""

# Run tests with coverage
python -m pytest tests/ -v --cov=src --cov-report=html --cov-report=term

if [ $? -eq 0 ]; then
    echo ""
    echo "======================================================================"
    echo "  All tests passed! Project is production-ready."
    echo "======================================================================"
    echo ""
    echo "Coverage report generated in: htmlcov/index.html"
    echo "Open it in your browser to see detailed coverage."
    echo ""
else
    echo ""
    echo "======================================================================"
    echo "  Some tests failed. Check output above for details."
    echo "======================================================================"
    exit 1
fi


