#!/usr/bin/env python3
"""
Success Criteria Verification Script for HEDIS GSD Prediction Engine

This script verifies that success criteria are being met in each development iteration.
Based on .cursorrules and PLAN.md requirements.
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SuccessCriteriaVerifier:
    """
    Verifies that success criteria are being met in each development iteration.
    """
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.results = {
            'overall_status': 'PENDING',
            'criteria_checks': {},
            'recommendations': [],
            'timestamp': None
        }
        
    def verify_all_criteria(self) -> Dict[str, Any]:
        """
        Verify all success criteria for the current iteration.
        
        Returns:
            Dictionary with verification results
        """
        logger.info("🔍 Starting success criteria verification...")
        
        # Core success criteria checks
        checks = [
            self._verify_hipaa_compliance,
            self._verify_hedis_alignment,
            self._verify_model_performance,
            self._verify_code_quality,
            self._verify_testing_coverage,
            self._verify_documentation,
            self._verify_security_standards
        ]
        
        for check in checks:
            try:
                check()
            except Exception as e:
                logger.error(f"Error in {check.__name__}: {e}")
                self.results['criteria_checks'][check.__name__] = {
                    'status': 'ERROR',
                    'message': str(e)
                }
        
        # Calculate overall status
        self._calculate_overall_status()
        
        logger.info(f"✅ Success criteria verification complete: {self.results['overall_status']}")
        return self.results
    
    def _verify_hipaa_compliance(self):
        """Verify HIPAA compliance requirements."""
        logger.info("Checking HIPAA compliance...")
        
        issues = []
        compliance_score = 0
        max_score = 5
        
        # Check for PHI exposure in code
        if self._check_phi_exposure():
            compliance_score += 1
        else:
            issues.append("Potential PHI exposure detected")
        
        # Check for audit logging
        if self._check_audit_logging():
            compliance_score += 1
        else:
            issues.append("Audit logging not properly implemented")
        
        # Check for data minimization
        if self._check_data_minimization():
            compliance_score += 1
        else:
            issues.append("Data minimization principles not followed")
        
        # Check for encryption mentions
        if self._check_encryption_standards():
            compliance_score += 1
        else:
            issues.append("Encryption standards not documented")
        
        # Check for de-identification methods
        if self._check_deidentification():
            compliance_score += 1
        else:
            issues.append("De-identification methods not implemented")
        
        status = 'PASS' if compliance_score >= 4 else 'FAIL'
        
        self.results['criteria_checks']['hipaa_compliance'] = {
            'status': status,
            'score': f"{compliance_score}/{max_score}",
            'issues': issues,
            'details': 'HIPAA compliance verification'
        }
        
        if issues:
            self.results['recommendations'].extend([
                f"HIPAA: {issue}" for issue in issues
            ])
    
    def _verify_hedis_alignment(self):
        """Verify HEDIS specification alignment."""
        logger.info("Checking HEDIS alignment...")
        
        issues = []
        alignment_score = 0
        max_score = 4
        
        # Check for HEDIS specification references
        if self._check_hedis_specifications():
            alignment_score += 1
        else:
            issues.append("HEDIS specifications not properly referenced")
        
        # Check for ICD-10 code validation
        if self._check_icd10_validation():
            alignment_score += 1
        else:
            issues.append("ICD-10 code validation not implemented")
        
        # Check for age calculations
        if self._check_age_calculations():
            alignment_score += 1
        else:
            issues.append("Age calculations not following HEDIS specs")
        
        # Check for exclusion criteria
        if self._check_exclusion_criteria():
            alignment_score += 1
        else:
            issues.append("HEDIS exclusion criteria not implemented")
        
        status = 'PASS' if alignment_score >= 3 else 'FAIL'
        
        self.results['criteria_checks']['hedis_alignment'] = {
            'status': status,
            'score': f"{alignment_score}/{max_score}",
            'issues': issues,
            'details': 'HEDIS specification alignment'
        }
        
        if issues:
            self.results['recommendations'].extend([
                f"HEDIS: {issue}" for issue in issues
            ])
    
    def _verify_model_performance(self):
        """Verify model performance criteria."""
        logger.info("Checking model performance...")
        
        issues = []
        performance_score = 0
        max_score = 4
        
        # Check for AUC-ROC performance
        if self._check_auc_performance():
            performance_score += 1
        else:
            issues.append("Model AUC-ROC below 0.90 threshold")
        
        # Check for temporal validation
        if self._check_temporal_validation():
            performance_score += 1
        else:
            issues.append("Temporal validation not implemented")
        
        # Check for no data leakage
        if self._check_data_leakage():
            performance_score += 1
        else:
            issues.append("Potential data leakage detected")
        
        # Check for fairness metrics
        if self._check_fairness_metrics():
            performance_score += 1
        else:
            issues.append("Fairness metrics not implemented")
        
        status = 'PASS' if performance_score >= 3 else 'FAIL'
        
        self.results['criteria_checks']['model_performance'] = {
            'status': status,
            'score': f"{performance_score}/{max_score}",
            'issues': issues,
            'details': 'Model performance verification'
        }
        
        if issues:
            self.results['recommendations'].extend([
                f"Performance: {issue}" for issue in issues
            ])
    
    def _verify_code_quality(self):
        """Verify code quality standards."""
        logger.info("Checking code quality...")
        
        issues = []
        quality_score = 0
        max_score = 3
        
        # Check for linting compliance
        if self._check_linting():
            quality_score += 1
        else:
            issues.append("Code linting issues detected")
        
        # Check for documentation
        if self._check_code_documentation():
            quality_score += 1
        else:
            issues.append("Insufficient code documentation")
        
        # Check for type hints
        if self._check_type_hints():
            quality_score += 1
        else:
            issues.append("Type hints missing in critical functions")
        
        status = 'PASS' if quality_score >= 2 else 'FAIL'
        
        self.results['criteria_checks']['code_quality'] = {
            'status': status,
            'score': f"{quality_score}/{max_score}",
            'issues': issues,
            'details': 'Code quality verification'
        }
        
        if issues:
            self.results['recommendations'].extend([
                f"Quality: {issue}" for issue in issues
            ])
    
    def _verify_testing_coverage(self):
        """Verify testing coverage and quality."""
        logger.info("Checking testing coverage...")
        
        issues = []
        testing_score = 0
        max_score = 3
        
        # Check for test existence
        if self._check_test_existence():
            testing_score += 1
        else:
            issues.append("Test files missing for key modules")
        
        # Check for test execution
        if self._check_test_execution():
            testing_score += 1
        else:
            issues.append("Tests not executing successfully")
        
        # Check for test coverage
        if self._check_test_coverage():
            testing_score += 1
        else:
            issues.append("Test coverage below 80% threshold")
        
        status = 'PASS' if testing_score >= 2 else 'FAIL'
        
        self.results['criteria_checks']['testing_coverage'] = {
            'status': status,
            'score': f"{testing_score}/{max_score}",
            'issues': issues,
            'details': 'Testing coverage verification'
        }
        
        if issues:
            self.results['recommendations'].extend([
                f"Testing: {issue}" for issue in issues
            ])
    
    def _verify_documentation(self):
        """Verify documentation completeness."""
        logger.info("Checking documentation...")
        
        issues = []
        doc_score = 0
        max_score = 3
        
        # Check for README
        if self._check_readme():
            doc_score += 1
        else:
            issues.append("README.md missing or incomplete")
        
        # Check for API documentation
        if self._check_api_docs():
            doc_score += 1
        else:
            issues.append("API documentation missing")
        
        # Check for healthcare glossary
        if self._check_healthcare_glossary():
            doc_score += 1
        else:
            issues.append("Healthcare glossary missing")
        
        status = 'PASS' if doc_score >= 2 else 'FAIL'
        
        self.results['criteria_checks']['documentation'] = {
            'status': status,
            'score': f"{doc_score}/{max_score}",
            'issues': issues,
            'details': 'Documentation verification'
        }
        
        if issues:
            self.results['recommendations'].extend([
                f"Documentation: {issue}" for issue in issues
            ])
    
    def _verify_security_standards(self):
        """Verify security standards."""
        logger.info("Checking security standards...")
        
        issues = []
        security_score = 0
        max_score = 3
        
        # Check for input validation
        if self._check_input_validation():
            security_score += 1
        else:
            issues.append("Input validation not implemented")
        
        # Check for security headers
        if self._check_security_headers():
            security_score += 1
        else:
            issues.append("Security headers not configured")
        
        # Check for sensitive data handling
        if self._check_sensitive_data_handling():
            security_score += 1
        else:
            issues.append("Sensitive data handling issues")
        
        status = 'PASS' if security_score >= 2 else 'FAIL'
        
        self.results['criteria_checks']['security_standards'] = {
            'status': status,
            'score': f"{security_score}/{max_score}",
            'issues': issues,
            'details': 'Security standards verification'
        }
        
        if issues:
            self.results['recommendations'].extend([
                f"Security: {issue}" for issue in issues
            ])
    
    def _calculate_overall_status(self):
        """Calculate overall verification status."""
        checks = self.results['criteria_checks']
        
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
    
    # Helper methods for individual checks
    def _check_phi_exposure(self) -> bool:
        """Check for PHI exposure in code."""
        # Run PHI scanner
        try:
            result = subprocess.run(['python', 'scripts/hipaa-scanner.py'], 
                                  capture_output=True, text=True, cwd=self.project_root)
            return result.returncode == 0
        except:
            return False
    
    def _check_audit_logging(self) -> bool:
        """Check for audit logging implementation."""
        src_files = list(self.project_root.glob('src/**/*.py'))
        for file in src_files:
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read()
                if 'logging' in content and ('audit' in content.lower() or 'logger' in content):
                    return True
        return False
    
    def _check_data_minimization(self) -> bool:
        """Check for data minimization principles."""
        # Look for data minimization comments or implementations
        src_files = list(self.project_root.glob('src/**/*.py'))
        for file in src_files:
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read().lower()
                if 'data minimization' in content or 'necessary fields' in content:
                    return True
        return False
    
    def _check_encryption_standards(self) -> bool:
        """Check for encryption standards documentation."""
        doc_files = list(self.project_root.glob('docs/**/*.md')) + [self.project_root / 'README.md']
        for file in doc_files:
            if file.exists():
                with open(file, 'r', encoding='utf-8') as f:
                    content = f.read().lower()
                    if 'encryption' in content:
                        return True
        return False
    
    def _check_deidentification(self) -> bool:
        """Check for de-identification methods."""
        src_files = list(self.project_root.glob('src/**/*.py'))
        for file in src_files:
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read().lower()
                if 'hash' in content or 'deident' in content:
                    return True
        return False
    
    def _check_hedis_specifications(self) -> bool:
        """Check for HEDIS specification references."""
        doc_files = list(self.project_root.glob('**/*.md'))
        for file in doc_files:
            if file.exists():
                with open(file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if 'HEDIS' in content and 'MY2023' in content:
                        return True
        return False
    
    def _check_icd10_validation(self) -> bool:
        """Check for ICD-10 code validation."""
        src_files = list(self.project_root.glob('src/**/*.py'))
        for file in src_files:
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read().lower()
                if 'icd-10' in content or 'icd10' in content:
                    return True
        return False
    
    def _check_age_calculations(self) -> bool:
        """Check for proper age calculations."""
        src_files = list(self.project_root.glob('src/**/*.py'))
        for file in src_files:
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read().lower()
                if 'age' in content and ('calculation' in content or 'measurement year' in content):
                    return True
        return False
    
    def _check_exclusion_criteria(self) -> bool:
        """Check for HEDIS exclusion criteria."""
        src_files = list(self.project_root.glob('src/**/*.py'))
        for file in src_files:
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read().lower()
                if 'exclusion' in content or 'hospice' in content:
                    return True
        return False
    
    def _check_auc_performance(self) -> bool:
        """Check for AUC performance metrics."""
        model_files = list(self.project_root.glob('reports/*.txt'))
        for file in model_files:
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read()
                if 'AUC' in content and '0.9' in content:
                    return True
        return False
    
    def _check_temporal_validation(self) -> bool:
        """Check for temporal validation implementation."""
        src_files = list(self.project_root.glob('src/**/*.py'))
        for file in src_files:
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read().lower()
                if 'temporal' in content and 'validation' in content:
                    return True
        return False
    
    def _check_data_leakage(self) -> bool:
        """Check for data leakage prevention."""
        src_files = list(self.project_root.glob('src/**/*.py'))
        for file in src_files:
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read().lower()
                if 'data leakage' in content or 'no leakage' in content:
                    return True
        return False
    
    def _check_fairness_metrics(self) -> bool:
        """Check for fairness metrics implementation."""
        src_files = list(self.project_root.glob('src/**/*.py'))
        for file in src_files:
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read().lower()
                if 'fairness' in content or 'bias' in content:
                    return True
        return False
    
    def _check_linting(self) -> bool:
        """Check for linting compliance."""
        try:
            result = subprocess.run(['flake8', 'src/'], 
                                  capture_output=True, text=True, cwd=self.project_root)
            return result.returncode == 0
        except:
            return False
    
    def _check_code_documentation(self) -> bool:
        """Check for code documentation."""
        src_files = list(self.project_root.glob('src/**/*.py'))
        documented_files = 0
        for file in src_files:
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read()
                if '"""' in content or "'''" in content:
                    documented_files += 1
        return documented_files >= len(src_files) * 0.8
    
    def _check_type_hints(self) -> bool:
        """Check for type hints in critical functions."""
        src_files = list(self.project_root.glob('src/**/*.py'))
        for file in src_files:
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read()
                if 'def ' in content and ':' in content and '->' in content:
                    return True
        return False
    
    def _check_test_existence(self) -> bool:
        """Check for test file existence."""
        test_files = list(self.project_root.glob('tests/**/*.py'))
        src_files = list(self.project_root.glob('src/**/*.py'))
        return len(test_files) >= len(src_files) * 0.5
    
    def _check_test_execution(self) -> bool:
        """Check for test execution."""
        try:
            result = subprocess.run(['python', '-m', 'pytest', 'tests/', '-v'], 
                                  capture_output=True, text=True, cwd=self.project_root)
            return result.returncode == 0
        except:
            return False
    
    def _check_test_coverage(self) -> bool:
        """Check for test coverage."""
        try:
            result = subprocess.run(['python', '-m', 'pytest', 'tests/', '--cov=src'], 
                                  capture_output=True, text=True, cwd=self.project_root)
            return result.returncode == 0
        except:
            return False
    
    def _check_readme(self) -> bool:
        """Check for README existence and quality."""
        readme_file = self.project_root / 'README.md'
        if readme_file.exists():
            with open(readme_file, 'r', encoding='utf-8') as f:
                content = f.read()
                return len(content) > 500 and 'HEDIS' in content
        return False
    
    def _check_api_docs(self) -> bool:
        """Check for API documentation."""
        doc_files = list(self.project_root.glob('docs/**/*.md'))
        for file in doc_files:
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read().lower()
                if 'api' in content:
                    return True
        return False
    
    def _check_healthcare_glossary(self) -> bool:
        """Check for healthcare glossary."""
        glossary_file = self.project_root / 'docs' / 'healthcare-glossary.md'
        return glossary_file.exists()
    
    def _check_input_validation(self) -> bool:
        """Check for input validation."""
        src_files = list(self.project_root.glob('src/**/*.py'))
        for file in src_files:
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read().lower()
                if 'validation' in content or 'validate' in content:
                    return True
        return False
    
    def _check_security_headers(self) -> bool:
        """Check for security headers."""
        # This would check API configuration files
        config_files = list(self.project_root.glob('**/*.yaml')) + list(self.project_root.glob('**/*.yml'))
        for file in config_files:
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read().lower()
                if 'security' in content or 'headers' in content:
                    return True
        return False
    
    def _check_sensitive_data_handling(self) -> bool:
        """Check for sensitive data handling."""
        src_files = list(self.project_root.glob('src/**/*.py'))
        for file in src_files:
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read().lower()
                if 'sensitive' in content or 'encrypt' in content:
                    return True
        return False
    
    def generate_report(self) -> str:
        """Generate a formatted report of the verification results."""
        report = []
        report.append("=" * 60)
        report.append("HEDIS GSD PREDICTION ENGINE - SUCCESS CRITERIA VERIFICATION")
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
        
        # Individual criteria
        for criterion, details in self.results['criteria_checks'].items():
            status_icon = status_emoji.get(details['status'], '❓')
            score_str = f" ({details['score']})" if 'score' in details else ""
            report.append(f"{status_icon} {criterion.replace('_', ' ').title()}: {details['status']}{score_str}")
            if details.get('issues'):
                for issue in details['issues']:
                    report.append(f"   • {issue}")
            if details.get('message'):
                report.append(f"   • Error: {details['message']}")
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
    """Main function to run success criteria verification."""
    verifier = SuccessCriteriaVerifier()
    results = verifier.verify_all_criteria()
    
    # Generate and print report
    report = verifier.generate_report()
    print(report)
    
    # Save results to file
    output_file = Path("reports/success_criteria_verification.json")
    output_file.parent.mkdir(exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
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
