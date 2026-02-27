#!/usr/bin/env python
"""
Compatibility test runner
Runs automated compatibility tests and generates report
"""
import sys
import subprocess
from pathlib import Path
from tests.compatibility.compatibility_matrix import CompatibilityMatrix


def run_playwright_tests():
    """Run Playwright compatibility tests."""
    print("Running Playwright compatibility tests...")
    
    cmd = [
        "pytest",
        "tests/compatibility/",
        "-m", "compatibility",
        "-v",
        "--browser=all"
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    print(result.stdout)
    if result.stderr:
        print("Errors:", result.stderr)
    
    return result.returncode == 0


def generate_report():
    """Generate compatibility test report."""
    print("Generating compatibility report...")
    
    matrix = CompatibilityMatrix()
    report_path = matrix.export_report()
    
    print(f"Report generated: {report_path}")
    
    summary = matrix.get_summary()
    print(f"\nSummary:")
    print(f"  Total: {summary['total']}")
    print(f"  Passed: {summary['passed']}")
    print(f"  Failed: {summary['failed']}")
    print(f"  Issues: {summary['issues']}")
    print(f"  Pending: {summary['pending']}")
    print(f"  Completion: {summary['completion_rate']:.1f}%")


def main():
    """Main test runner."""
    print("=" * 60)
    print("HEDIS Portfolio Optimizer - Compatibility Testing")
    print("=" * 60)
    print()
    
    # Check if Streamlit app is running
    print("Note: Ensure Streamlit app is running on http://localhost:8501")
    print()
    
    # Run automated tests
    if "--skip-automated" not in sys.argv:
        success = run_playwright_tests()
        if not success:
            print("Warning: Some automated tests failed")
    else:
        print("Skipping automated tests (--skip-automated flag)")
    
    # Generate report
    generate_report()
    
    print()
    print("=" * 60)
    print("Compatibility testing complete!")
    print("=" * 60)
    print()
    print("Next steps:")
    print("1. Review compatibility_report.md")
    print("2. Complete manual testing checklist")
    print("3. Update compatibility matrix with results")
    print("4. Address any critical issues found")


if __name__ == "__main__":
    main()

