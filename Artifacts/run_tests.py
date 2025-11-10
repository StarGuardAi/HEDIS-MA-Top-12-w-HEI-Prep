#!/usr/bin/env python3
"""
Quick test runner for HEDIS Project
Provides easy testing for recruiters and hiring managers

Author: Robert Reichert
Usage: python run_tests.py
"""

import sys
import subprocess
from pathlib import Path

def print_header(text):
    """Print formatted header"""
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70 + "\n")

def run_command(cmd, description):
    """Run a command and return success status"""
    print(f"▶ {description}...")
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent / "project"
        )
        if result.returncode == 0:
            print(f"✅ {description} - SUCCESS\n")
            return True
        else:
            print(f"❌ {description} - FAILED")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Main test runner"""
    print_header("HEDIS Project - Quick Test Runner")
    
    print("This script will run comprehensive tests to verify project quality.")
    print("Expected time: 2-5 minutes\n")
    
    # Check if we're in the right directory
    project_dir = Path(__file__).parent / "project"
    if not project_dir.exists():
        print("❌ Error: 'project' directory not found!")
        print("   Please run this script from the repository root.")
        sys.exit(1)
    
    # Check if pytest is installed
    print("Checking dependencies...")
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "--version"],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        print("❌ pytest not found. Installing dependencies...")
        print("   Run: pip install -r project/requirements-full.txt")
        sys.exit(1)
    
    print("✅ Dependencies OK\n")
    
    # Test categories
    test_categories = [
        ("pytest tests/api/ -v", "API Tests"),
        ("pytest tests/models/ -v", "ML Model Tests"),
        ("pytest tests/measures/ -v", "HEDIS Measure Tests"),
        ("pytest tests/data/ -v", "Data Processing Tests"),
        ("pytest tests/integration/ -v", "Integration Tests"),
    ]
    
    results = []
    
    # Run each test category
    for cmd, description in test_categories:
        success = run_command(cmd, description)
        results.append((description, success))
    
    # Run full test suite with coverage
    print_header("Running Full Test Suite with Coverage")
    success = run_command(
        "pytest tests/ -v --cov=src --cov-report=html --cov-report=term",
        "Full Test Suite with Coverage"
    )
    results.append(("Full Test Suite", success))
    
    # Summary
    print_header("Test Summary")
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for description, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {description}")
    
    print(f"\n{'='*70}")
    print(f"  Results: {passed}/{total} test categories passed")
    print(f"{'='*70}\n")
    
    if passed == total:
        print("🎉 All tests passed! Project is production-ready.")
        print("\n📊 Coverage report generated in: project/htmlcov/index.html")
        print("   Open it in your browser to see detailed coverage.")
    else:
        print("⚠️  Some tests failed. Check output above for details.")
        sys.exit(1)

if __name__ == "__main__":
    main()


