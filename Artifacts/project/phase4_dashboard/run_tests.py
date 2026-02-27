#!/usr/bin/env python
"""
Test runner script for HEDIS Portfolio Optimizer
Provides convenient commands for running different test suites
"""
import sys
import subprocess
import argparse


def run_command(cmd):
    """Run a command and return exit code."""
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd)
    return result.returncode


def main():
    parser = argparse.ArgumentParser(description="Run HEDIS Portfolio Optimizer tests")
    parser.add_argument(
        "test_type",
        choices=["all", "unit", "integration", "ui", "performance", "validation", "accessibility", "coverage"],
        help="Type of tests to run"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Verbose output"
    )
    parser.add_argument(
        "--no-cov",
        action="store_true",
        help="Skip coverage reporting"
    )
    
    args = parser.parse_args()
    
    base_cmd = ["pytest"]
    
    if args.verbose:
        base_cmd.append("-v")
    
    if not args.no_cov and args.test_type in ["all", "coverage"]:
        base_cmd.extend([
            "--cov=utils",
            "--cov=pages",
            "--cov-report=html",
            "--cov-report=term-missing",
            "--cov-fail-under=80"
        ])
    
    if args.test_type == "all":
        cmd = base_cmd + ["tests/"]
    elif args.test_type == "coverage":
        cmd = base_cmd + [
            "--cov=utils",
            "--cov=pages",
            "--cov-report=html",
            "--cov-report=term-missing",
            "--cov-fail-under=80",
            "tests/"
        ]
    else:
        cmd = base_cmd + ["-m", args.test_type, "tests/"]
    
    exit_code = run_command(cmd)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()

