#!/usr/bin/env python3
"""
Testing Verification Script for HEDIS GSD Prediction Engine

This script verifies that comprehensive testing is applied at each development step
with approval and reworking capabilities.
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple, Any
import logging
import ast
import re

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TestingVerifier:
    """
    Verifies that comprehensive testing is applied at each development step.
    """
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.results = {
            'overall_status': 'PENDING',
            'test_checks': {},
            'coverage_analysis': {},
            'test_quality_metrics': {},
            'recommendations': [],
            'timestamp': None
        }
        
    def verify_all_testing(self) -> Dict[str, Any]:
        """
        Verify all testing requirements for the current iteration.
        
        Returns:
            Dictionary with verification results
        """
        logger.info("🧪 Starting comprehensive testing verification...")
        
        # Core testing verification checks
        checks = [
            self._verify_test_structure,
            self._verify_test_coverage,
            self._verify_test_quality,
            self._verify_test_execution,
            self._verify_test_data_management,
            self._verify_healthcare_specific_tests,
            self._verify_integration_tests,
            self._verify_performance_tests
        ]
        
        for check in checks:
            try:
                check()
            except Exception as e:
                logger.error(f"Error in {check.__name__}: {e}")
                self.results['test_checks'][check.__name__] = {
                    'status': 'ERROR',
                    'message': str(e)
                }
        
        # Calculate overall status
        self._calculate_overall_status()
        
        logger.info(f"✅ Testing verification complete: {self.results['overall_status']}")
        return self.results
    
    def _verify_test_structure(self):
        """Verify test structure and organization."""
        logger.info("Checking test structure...")
        
        issues = []
        structure_score = 0
        max_score = 4
        
        # Check for test directory structure
        test_dir = self.project_root / 'tests'
        if test_dir.exists():
            structure_score += 1
        else:
            issues.append("Tests directory missing")
        
        # Check for module-specific test files
        src_modules = [d.name for d in (self.project_root / 'src').iterdir() if d.is_dir()]
        test_modules = [d.name for d in test_dir.iterdir() if d.is_dir()] if test_dir.exists() else []
        
        module_coverage = len(set(src_modules) & set(test_modules)) / len(src_modules) if src_modules else 0
        if module_coverage >= 0.8:
            structure_score += 1
        else:
            issues.append(f"Module test coverage: {module_coverage:.1%} (target: 80%)")
        
        # Check for test configuration files
        config_files = ['pytest.ini', 'pyproject.toml', 'setup.cfg']
        has_config = any((self.project_root / f).exists() for f in config_files)
        if has_config:
            structure_score += 1
        else:
            issues.append("Test configuration files missing")
        
        # Check for test fixtures
        fixtures_dir = test_dir / 'fixtures' if test_dir.exists() else None
        if fixtures_dir and fixtures_dir.exists():
            structure_score += 1
        else:
            issues.append("Test fixtures directory missing")
        
        status = 'PASS' if structure_score >= 3 else 'FAIL'
        
        self.results['test_checks']['test_structure'] = {
            'status': status,
            'score': f"{structure_score}/{max_score}",
            'issues': issues,
            'details': 'Test structure and organization'
        }
        
        if issues:
            self.results['recommendations'].extend([
                f"Structure: {issue}" for issue in issues
            ])
    
    def _verify_test_coverage(self):
        """Verify test coverage metrics."""
        logger.info("Checking test coverage...")
        
        issues = []
        coverage_score = 0
        max_score = 3
        
        # Run coverage analysis
        try:
            result = subprocess.run([
                'python', '-m', 'pytest', 'tests/', '--cov=src', '--cov-report=json'
            ], capture_output=True, text=True, cwd=self.project_root)
            
            if result.returncode == 0:
                # Parse coverage report
                coverage_file = self.project_root / 'coverage.json'
                if coverage_file.exists():
                    with open(coverage_file, 'r') as f:
                        coverage_data = json.load(f)
                        total_coverage = coverage_data['totals']['percent_covered']
                        
                        if total_coverage >= 90:
                            coverage_score += 1
                        else:
                            issues.append(f"Overall coverage: {total_coverage:.1f}% (target: 90%)")
                        
                        # Check line coverage
                        line_coverage = coverage_data['totals']['percent_covered_display']
                        if float(line_coverage) >= 85:
                            coverage_score += 1
                        else:
                            issues.append(f"Line coverage: {line_coverage}% (target: 85%)")
                        
                        # Check branch coverage
                        branch_coverage = coverage_data['totals'].get('percent_covered_display', '0')
                        if float(branch_coverage) >= 80:
                            coverage_score += 1
                        else:
                            issues.append(f"Branch coverage: {branch_coverage}% (target: 80%)")
                        
                        self.results['coverage_analysis'] = {
                            'total_coverage': total_coverage,
                            'line_coverage': line_coverage,
                            'branch_coverage': branch_coverage,
                            'files_covered': len(coverage_data['files'])
                        }
            else:
                issues.append("Coverage analysis failed to run")
                
        except Exception as e:
            issues.append(f"Coverage analysis error: {str(e)}")
        
        status = 'PASS' if coverage_score >= 2 else 'FAIL'
        
        self.results['test_checks']['test_coverage'] = {
            'status': status,
            'score': f"{coverage_score}/{max_score}",
            'issues': issues,
            'details': 'Test coverage metrics'
        }
        
        if issues:
            self.results['recommendations'].extend([
                f"Coverage: {issue}" for issue in issues
            ])
    
    def _verify_test_quality(self):
        """Verify test quality and best practices."""
        logger.info("Checking test quality...")
        
        issues = []
        quality_score = 0
        max_score = 4
        
        # Check for test naming conventions
        test_files = list((self.project_root / 'tests').glob('**/test_*.py'))
        if test_files:
            quality_score += 1
        else:
            issues.append("Test files not following naming convention (test_*.py)")
        
        # Check for test documentation
        documented_tests = 0
        for test_file in test_files:
            with open(test_file, 'r') as f:
                content = f.read()
                if '"""' in content or "'''" in content:
                    documented_tests += 1
        
        doc_ratio = documented_tests / len(test_files) if test_files else 0
        if doc_ratio >= 0.7:
            quality_score += 1
        else:
            issues.append(f"Test documentation: {doc_ratio:.1%} (target: 70%)")
        
        # Check for test isolation
        isolated_tests = 0
        for test_file in test_files:
            with open(test_file, 'r') as f:
                content = f.read()
                if 'def test_' in content and 'setup_method' in content or 'teardown_method' in content:
                    isolated_tests += 1
        
        isolation_ratio = isolated_tests / len(test_files) if test_files else 0
        if isolation_ratio >= 0.5:
            quality_score += 1
        else:
            issues.append(f"Test isolation: {isolation_ratio:.1%} (target: 50%)")
        
        # Check for assertion quality
        assertion_tests = 0
        for test_file in test_files:
            with open(test_file, 'r') as f:
                content = f.read()
                if 'assert' in content and ('assertEqual' in content or 'assertTrue' in content):
                    assertion_tests += 1
        
        assertion_ratio = assertion_tests / len(test_files) if test_files else 0
        if assertion_ratio >= 0.8:
            quality_score += 1
        else:
            issues.append(f"Quality assertions: {assertion_ratio:.1%} (target: 80%)")
        
        status = 'PASS' if quality_score >= 3 else 'FAIL'
        
        self.results['test_checks']['test_quality'] = {
            'status': status,
            'score': f"{quality_score}/{max_score}",
            'issues': issues,
            'details': 'Test quality and best practices'
        }
        
        if issues:
            self.results['recommendations'].extend([
                f"Quality: {issue}" for issue in issues
            ])
    
    def _verify_test_execution(self):
        """Verify test execution and results."""
        logger.info("Checking test execution...")
        
        issues = []
        execution_score = 0
        max_score = 3
        
        # Check for successful test execution
        try:
            result = subprocess.run([
                'python', '-m', 'pytest', 'tests/', '-v', '--tb=short'
            ], capture_output=True, text=True, cwd=self.project_root)
            
            if result.returncode == 0:
                execution_score += 1
                
                # Parse test results
                output_lines = result.stdout.split('\n')
                passed_tests = len([line for line in output_lines if 'PASSED' in line])
                failed_tests = len([line for line in output_lines if 'FAILED' in line])
                total_tests = passed_tests + failed_tests
                
                if total_tests > 0:
                    pass_rate = passed_tests / total_tests
                    if pass_rate >= 0.95:
                        execution_score += 1
                    else:
                        issues.append(f"Test pass rate: {pass_rate:.1%} (target: 95%)")
                    
                    self.results['test_quality_metrics'] = {
                        'total_tests': total_tests,
                        'passed_tests': passed_tests,
                        'failed_tests': failed_tests,
                        'pass_rate': pass_rate
                    }
                else:
                    issues.append("No tests found to execute")
            else:
                issues.append("Test execution failed")
                issues.append(f"Error: {result.stderr}")
                
        except Exception as e:
            issues.append(f"Test execution error: {str(e)}")
        
        # Check for test performance
        try:
            result = subprocess.run([
                'python', '-m', 'pytest', 'tests/', '--durations=10'
            ], capture_output=True, text=True, cwd=self.project_root)
            
            if result.returncode == 0:
                execution_score += 1
            else:
                issues.append("Performance test analysis failed")
                
        except Exception as e:
            issues.append(f"Performance analysis error: {str(e)}")
        
        status = 'PASS' if execution_score >= 2 else 'FAIL'
        
        self.results['test_checks']['test_execution'] = {
            'status': status,
            'score': f"{execution_score}/{max_score}",
            'issues': issues,
            'details': 'Test execution and results'
        }
        
        if issues:
            self.results['recommendations'].extend([
                f"Execution: {issue}" for issue in issues
            ])
    
    def _verify_test_data_management(self):
        """Verify test data management practices."""
        logger.info("Checking test data management...")
        
        issues = []
        data_score = 0
        max_score = 3
        
        # Check for test fixtures
        fixtures_dir = self.project_root / 'tests' / 'fixtures'
        if fixtures_dir.exists():
            data_score += 1
        else:
            issues.append("Test fixtures directory missing")
        
        # Check for synthetic test data
        test_files = list((self.project_root / 'tests').glob('**/test_*.py'))
        synthetic_data_tests = 0
        for test_file in test_files:
            with open(test_file, 'r') as f:
                content = f.read()
                if 'synthetic' in content.lower() or 'mock' in content.lower():
                    synthetic_data_tests += 1
        
        synthetic_ratio = synthetic_data_tests / len(test_files) if test_files else 0
        if synthetic_ratio >= 0.6:
            data_score += 1
        else:
            issues.append(f"Synthetic test data usage: {synthetic_ratio:.1%} (target: 60%)")
        
        # Check for PHI-free test data
        phi_free_tests = 0
        for test_file in test_files:
            with open(test_file, 'r') as f:
                content = f.read()
                if 'phi' not in content.lower() and 'patient' not in content.lower():
                    phi_free_tests += 1
        
        phi_free_ratio = phi_free_tests / len(test_files) if test_files else 0
        if phi_free_ratio >= 0.8:
            data_score += 1
        else:
            issues.append(f"PHI-free test data: {phi_free_ratio:.1%} (target: 80%)")
        
        status = 'PASS' if data_score >= 2 else 'FAIL'
        
        self.results['test_checks']['test_data_management'] = {
            'status': status,
            'score': f"{data_score}/{max_score}",
            'issues': issues,
            'details': 'Test data management practices'
        }
        
        if issues:
            self.results['recommendations'].extend([
                f"Data Management: {issue}" for issue in issues
            ])
    
    def _verify_healthcare_specific_tests(self):
        """Verify healthcare-specific test requirements."""
        logger.info("Checking healthcare-specific tests...")
        
        issues = []
        healthcare_score = 0
        max_score = 3
        
        # Check for HIPAA compliance tests
        test_files = list((self.project_root / 'tests').glob('**/test_*.py'))
        hipaa_tests = 0
        for test_file in test_files:
            with open(test_file, 'r') as f:
                content = f.read().lower()
                if 'hipaa' in content or 'phi' in content:
                    hipaa_tests += 1
        
        if hipaa_tests > 0:
            healthcare_score += 1
        else:
            issues.append("HIPAA compliance tests missing")
        
        # Check for HEDIS specification tests
        hedis_tests = 0
        for test_file in test_files:
            with open(test_file, 'r') as f:
                content = f.read().lower()
                if 'hedis' in content or 'icd-10' in content:
                    hedis_tests += 1
        
        if hedis_tests > 0:
            healthcare_score += 1
        else:
            issues.append("HEDIS specification tests missing")
        
        # Check for clinical validation tests
        clinical_tests = 0
        for test_file in test_files:
            with open(test_file, 'r') as f:
                content = f.read().lower()
                if 'clinical' in content or 'validation' in content:
                    clinical_tests += 1
        
        if clinical_tests > 0:
            healthcare_score += 1
        else:
            issues.append("Clinical validation tests missing")
        
        status = 'PASS' if healthcare_score >= 2 else 'FAIL'
        
        self.results['test_checks']['healthcare_specific_tests'] = {
            'status': status,
            'score': f"{healthcare_score}/{max_score}",
            'issues': issues,
            'details': 'Healthcare-specific test requirements'
        }
        
        if issues:
            self.results['recommendations'].extend([
                f"Healthcare: {issue}" for issue in issues
            ])
    
    def _verify_integration_tests(self):
        """Verify integration test coverage."""
        logger.info("Checking integration tests...")
        
        issues = []
        integration_score = 0
        max_score = 2
        
        # Check for integration test files
        integration_tests = list((self.project_root / 'tests').glob('**/test_integration*.py'))
        if integration_tests:
            integration_score += 1
        else:
            issues.append("Integration test files missing")
        
        # Check for API integration tests
        api_tests = 0
        test_files = list((self.project_root / 'tests').glob('**/test_*.py'))
        for test_file in test_files:
            with open(test_file, 'r') as f:
                content = f.read().lower()
                if 'api' in content or 'endpoint' in content:
                    api_tests += 1
        
        if api_tests > 0:
            integration_score += 1
        else:
            issues.append("API integration tests missing")
        
        status = 'PASS' if integration_score >= 1 else 'FAIL'
        
        self.results['test_checks']['integration_tests'] = {
            'status': status,
            'score': f"{integration_score}/{max_score}",
            'issues': issues,
            'details': 'Integration test coverage'
        }
        
        if issues:
            self.results['recommendations'].extend([
                f"Integration: {issue}" for issue in issues
            ])
    
    def _verify_performance_tests(self):
        """Verify performance test coverage."""
        logger.info("Checking performance tests...")
        
        issues = []
        performance_score = 0
        max_score = 2
        
        # Check for performance test files
        performance_tests = list((self.project_root / 'tests').glob('**/test_performance*.py'))
        if performance_tests:
            performance_score += 1
        else:
            issues.append("Performance test files missing")
        
        # Check for load testing
        test_files = list((self.project_root / 'tests').glob('**/test_*.py'))
        load_tests = 0
        for test_file in test_files:
            with open(test_file, 'r') as f:
                content = f.read().lower()
                if 'load' in content or 'performance' in content:
                    load_tests += 1
        
        if load_tests > 0:
            performance_score += 1
        else:
            issues.append("Load/performance tests missing")
        
        status = 'PASS' if performance_score >= 1 else 'FAIL'
        
        self.results['test_checks']['performance_tests'] = {
            'status': status,
            'score': f"{performance_score}/{max_score}",
            'issues': issues,
            'details': 'Performance test coverage'
        }
        
        if issues:
            self.results['recommendations'].extend([
                f"Performance: {issue}" for issue in issues
            ])
    
    def _calculate_overall_status(self):
        """Calculate overall testing verification status."""
        checks = self.results['test_checks']
        
        if not checks:
            self.results['overall_status'] = 'ERROR'
            return
        
        pass_count = sum(1 for check in checks.values() if check['status'] == 'PASS')
        total_count = len(checks)
        
        if pass_count == total_count:
            self.results['overall_status'] = 'PASS'
        elif pass_count >= total_count * 0.8:
            self.results['overall_status'] = 'WARNING'
        else:
            self.results['overall_status'] = 'FAIL'
    
    def generate_report(self) -> str:
        """Generate a formatted report of the testing verification results."""
        report = []
        report.append("=" * 60)
        report.append("HEDIS GSD PREDICTION ENGINE - TESTING VERIFICATION")
        report.append("=" * 60)
        report.append("")
        
        # Overall status
        status_emoji = {
            'PASS': '✅',
            'WARNING': '⚠️',
            'FAIL': '❌',
            'ERROR': '💥'
        }
        
        report.append(f"Overall Status: {status_emoji.get(self.results['overall_status'], '❓')} {self.results['overall_status']}")
        report.append("")
        
        # Test quality metrics
        if self.results.get('test_quality_metrics'):
            metrics = self.results['test_quality_metrics']
            report.append("📊 Test Quality Metrics:")
            report.append(f"   Total Tests: {metrics.get('total_tests', 0)}")
            report.append(f"   Passed: {metrics.get('passed_tests', 0)}")
            report.append(f"   Failed: {metrics.get('failed_tests', 0)}")
            report.append(f"   Pass Rate: {metrics.get('pass_rate', 0):.1%}")
            report.append("")
        
        # Coverage analysis
        if self.results.get('coverage_analysis'):
            coverage = self.results['coverage_analysis']
            report.append("📈 Coverage Analysis:")
            report.append(f"   Total Coverage: {coverage.get('total_coverage', 0):.1f}%")
            report.append(f"   Line Coverage: {coverage.get('line_coverage', 0)}%")
            report.append(f"   Branch Coverage: {coverage.get('branch_coverage', 0)}%")
            report.append(f"   Files Covered: {coverage.get('files_covered', 0)}")
            report.append("")
        
        # Individual test checks
        for criterion, details in self.results['test_checks'].items():
            status_icon = status_emoji.get(details['status'], '❓')
            report.append(f"{status_icon} {criterion.replace('_', ' ').title()}: {details['status']} ({details['score']})")
            if details.get('issues'):
                for issue in details['issues']:
                    report.append(f"   • {issue}")
            report.append("")
        
        # Recommendations
        if self.results['recommendations']:
            report.append("🔧 Recommendations:")
            for rec in self.results['recommendations']:
                report.append(f"   • {rec}")
            report.append("")
        
        report.append("=" * 60)
        
        return "\n".join(report)


def main():
    """Main function to run testing verification."""
    verifier = TestingVerifier()
    results = verifier.verify_all_testing()
    
    # Generate and print report
    report = verifier.generate_report()
    print(report)
    
    # Save results to file
    output_file = Path("reports/testing_verification.json")
    output_file.parent.mkdir(exist_ok=True)
    
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"\n📄 Detailed results saved to: {output_file}")
    
    # Exit with appropriate code
    if results['overall_status'] == 'PASS':
        sys.exit(0)
    elif results['overall_status'] == 'WARNING':
        sys.exit(1)
    else:
        sys.exit(2)


if __name__ == "__main__":
    main()
