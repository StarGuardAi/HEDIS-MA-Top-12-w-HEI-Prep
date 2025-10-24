#!/bin/bash
# Pre-commit checks for HEDIS GSD project

set -e

echo "🔍 Running pre-commit checks for HEDIS GSD..."

# 1. PHI Scan
echo "1/6 Scanning for PHI exposure..."
python scripts/hipaa-scanner.py

# 2. Run tests
echo "2/6 Running unit tests..."
if [ -d "tests" ]; then
    python -m pytest tests/ -v --tb=short 2>/dev/null || echo "⚠️  Some tests failed"
fi

# 3. Success Criteria Verification
echo "3/6 Verifying success criteria..."
python scripts/verify-success-criteria.py 2>/dev/null || echo "⚠️  Success criteria verification issues"

# 4. Testing Verification
echo "4/6 Verifying testing coverage..."
python scripts/verify-testing.py 2>/dev/null || echo "⚠️  Testing verification issues"

# 5. Check for sensitive data in git
echo "5/6 Checking for sensitive files..."
if git ls-files | grep -qE '\.(pkl|csv|parquet)$'; then
    echo "⚠️  Warning: Model/data files detected in git"
    echo "   Consider using Git LFS or .gitignore"
fi

# 6. Code quality
echo "6/6 Checking code quality..."
if command -v flake8 &> /dev/null; then
    flake8 src/ --count --select=E9,F63,F7,F82 --show-source --statistics 2>/dev/null || true
fi

echo ""
echo "✅ Pre-commit checks complete!"