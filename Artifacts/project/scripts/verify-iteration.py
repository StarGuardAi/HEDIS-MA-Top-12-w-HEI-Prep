#!/usr/bin/env python3
"""
Iteration Verification Script for HEDIS GSD Prediction Engine

This script runs both success criteria and testing verification for each development iteration,
providing approval and reworking recommendations.
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple, Any
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class IterationVerifier:
    """
    Verifies both success criteria and testing for each development iteration.
    """
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.results = {
            'iteration_id': f"iteration_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'timestamp': datetime.now().isoformat(),
            'overall_status': 'PENDING',
            'success_criteria': {},
            'testing_verification': {},
            'approval_status': 'PENDING',
            'rework_required': [],
            'recommendations': []
        }
        
    def verify_iteration(self) -> Dict[str, Any]:
        """
        Verify the current development iteration.
        
        Returns:
            Dictionary with complete verification results
        """
        logger.info("🚀 Starting iteration verification...")
        
        # Run success criteria verification
        logger.info("1/2 Running success criteria verification...")
        success_results = self._run_success_criteria_verification()
        self.results['success_criteria'] = success_results
        
        # Run testing verification
        logger.info("2/2 Running testing verification...")
        testing_results = self._run_testing_verification()
        self.results['testing_verification'] = testing_results
        
        # Determine overall status and approval
        self._determine_approval_status()
        
        # Generate recommendations
        self._generate_recommendations()
        
        logger.info(f"✅ Iteration verification complete: {self.results['overall_status']}")
        return self.results
    
    def _run_success_criteria_verification(self) -> Dict[str, Any]:
        """Run success criteria verification."""
        try:
            result = subprocess.run([
                'python', 'scripts/verify-success-criteria.py'
            ], capture_output=True, text=True, cwd=self.project_root)
            
            if result.returncode == 0:
                # Load results from file
                results_file = self.project_root / 'reports' / 'success_criteria_verification.json'
                if results_file.exists():
                    with open(results_file, 'r') as f:
                        return json.load(f)
                else:
                    return {'status': 'ERROR', 'message': 'Results file not found'}
            else:
                return {
                    'status': 'ERROR',
                    'message': f'Verification failed: {result.stderr}',
                    'returncode': result.returncode
                }
                
        except Exception as e:
            return {
                'status': 'ERROR',
                'message': f'Verification error: {str(e)}'
            }
    
    def _run_testing_verification(self) -> Dict[str, Any]:
        """Run testing verification."""
        try:
            result = subprocess.run([
                'python', 'scripts/verify-testing.py'
            ], capture_output=True, text=True, cwd=self.project_root)
            
            if result.returncode == 0:
                # Load results from file
                results_file = self.project_root / 'reports' / 'testing_verification.json'
                if results_file.exists():
                    with open(results_file, 'r') as f:
                        return json.load(f)
                else:
                    return {'status': 'ERROR', 'message': 'Results file not found'}
            else:
                return {
                    'status': 'ERROR',
                    'message': f'Verification failed: {result.stderr}',
                    'returncode': result.returncode
                }
                
        except Exception as e:
            return {
                'status': 'ERROR',
                'message': f'Verification error: {str(e)}'
            }
    
    def _determine_approval_status(self):
        """Determine approval status based on verification results."""
        success_status = self.results['success_criteria'].get('overall_status', 'ERROR')
        testing_status = self.results['testing_verification'].get('overall_status', 'ERROR')
        
        # Determine overall status
        if success_status == 'PASS' and testing_status == 'PASS':
            self.results['overall_status'] = 'APPROVED'
            self.results['approval_status'] = 'APPROVED'
        elif success_status == 'WARNING' or testing_status == 'WARNING':
            self.results['overall_status'] = 'CONDITIONAL_APPROVAL'
            self.results['approval_status'] = 'CONDITIONAL'
        else:
            self.results['overall_status'] = 'REWORK_REQUIRED'
            self.results['approval_status'] = 'REWORK'
    
    def _generate_recommendations(self):
        """Generate recommendations for approval or rework."""
        recommendations = []
        
        # Success criteria recommendations
        success_recs = self.results['success_criteria'].get('recommendations', [])
        if success_recs:
            recommendations.extend([f"Success Criteria: {rec}" for rec in success_recs])
        
        # Testing recommendations
        testing_recs = self.results['testing_verification'].get('recommendations', [])
        if testing_recs:
            recommendations.extend([f"Testing: {rec}" for rec in testing_recs])
        
        # Overall recommendations based on status
        if self.results['overall_status'] == 'APPROVED':
            recommendations.append("✅ Iteration APPROVED - Ready for next phase")
        elif self.results['overall_status'] == 'CONDITIONAL_APPROVAL':
            recommendations.append("⚠️ Iteration CONDITIONALLY APPROVED - Address warnings before proceeding")
        else:
            recommendations.append("❌ Iteration REQUIRES REWORK - Fix critical issues before proceeding")
        
        self.results['recommendations'] = recommendations
    
    def generate_approval_report(self) -> str:
        """Generate a comprehensive approval report."""
        report = []
        report.append("=" * 80)
        report.append("HEDIS GSD PREDICTION ENGINE - ITERATION APPROVAL REPORT")
        report.append("=" * 80)
        report.append(f"Iteration ID: {self.results['iteration_id']}")
        report.append(f"Timestamp: {self.results['timestamp']}")
        report.append("")
        
        # Overall status
        status_emoji = {
            'APPROVED': '✅',
            'CONDITIONAL_APPROVAL': '⚠️',
            'REWORK_REQUIRED': '❌',
            'ERROR': '💥'
        }
        
        report.append(f"Overall Status: {status_emoji.get(self.results['overall_status'], '❓')} {self.results['overall_status']}")
        report.append(f"Approval Status: {self.results['approval_status']}")
        report.append("")
        
        # Success criteria summary
        success_criteria = self.results['success_criteria']
        report.append("📋 SUCCESS CRITERIA VERIFICATION:")
        report.append(f"   Status: {success_criteria.get('overall_status', 'UNKNOWN')}")
        
        criteria_checks = success_criteria.get('criteria_checks', {})
        for criterion, details in criteria_checks.items():
            status_icon = '✅' if details['status'] == 'PASS' else '❌'
            report.append(f"   {status_icon} {criterion.replace('_', ' ').title()}: {details['status']} ({details['score']})")
        
        report.append("")
        
        # Testing verification summary
        testing_verification = self.results['testing_verification']
        report.append("🧪 TESTING VERIFICATION:")
        report.append(f"   Status: {testing_verification.get('overall_status', 'UNKNOWN')}")
        
        test_checks = testing_verification.get('test_checks', {})
        for test_type, details in test_checks.items():
            status_icon = '✅' if details['status'] == 'PASS' else '❌'
            report.append(f"   {status_icon} {test_type.replace('_', ' ').title()}: {details['status']} ({details['score']})")
        
        report.append("")
        
        # Coverage summary
        if testing_verification.get('coverage_analysis'):
            coverage = testing_verification['coverage_analysis']
            report.append("📊 COVERAGE SUMMARY:")
            report.append(f"   Total Coverage: {coverage.get('total_coverage', 0):.1f}%")
            report.append(f"   Line Coverage: {coverage.get('line_coverage', 0)}%")
            report.append(f"   Files Covered: {coverage.get('files_covered', 0)}")
            report.append("")
        
        # Test quality metrics
        if testing_verification.get('test_quality_metrics'):
            metrics = testing_verification['test_quality_metrics']
            report.append("📈 TEST QUALITY METRICS:")
            report.append(f"   Total Tests: {metrics.get('total_tests', 0)}")
            report.append(f"   Pass Rate: {metrics.get('pass_rate', 0):.1%}")
            report.append("")
        
        # Recommendations
        if self.results['recommendations']:
            report.append("🔧 RECOMMENDATIONS:")
            for rec in self.results['recommendations']:
                report.append(f"   • {rec}")
            report.append("")
        
        # Next steps
        report.append("📝 NEXT STEPS:")
        if self.results['overall_status'] == 'APPROVED':
            report.append("   1. ✅ Iteration approved - proceed to next development phase")
            report.append("   2. 📋 Update project documentation")
            report.append("   3. 🚀 Begin next iteration planning")
        elif self.results['overall_status'] == 'CONDITIONAL_APPROVAL':
            report.append("   1. ⚠️ Address warning conditions")
            report.append("   2. 🔄 Re-run verification")
            report.append("   3. ✅ Proceed once warnings resolved")
        else:
            report.append("   1. ❌ Fix critical issues identified")
            report.append("   2. 🔄 Re-run verification")
            report.append("   3. 📋 Update development plan if needed")
        
        report.append("")
        report.append("=" * 80)
        
        return "\n".join(report)
    
    def save_results(self):
        """Save verification results to file."""
        output_file = self.project_root / 'reports' / f"iteration_verification_{self.results['iteration_id']}.json"
        output_file.parent.mkdir(exist_ok=True)
        
        with open(output_file, 'w') as f:
            json.dump(self.results, f, indent=2, default=str)
        
        logger.info(f"Results saved to: {output_file}")
        return output_file


def main():
    """Main function to run iteration verification."""
    verifier = IterationVerifier()
    results = verifier.verify_iteration()
    
    # Generate and print approval report
    report = verifier.generate_approval_report()
    print(report)
    
    # Save results
    output_file = verifier.save_results()
    
    print(f"\n📄 Detailed results saved to: {output_file}")
    
    # Exit with appropriate code
    if results['overall_status'] == 'APPROVED':
        print("\n🎉 ITERATION APPROVED - Ready to proceed!")
        sys.exit(0)
    elif results['overall_status'] == 'CONDITIONAL_APPROVAL':
        print("\n⚠️ ITERATION CONDITIONALLY APPROVED - Address warnings")
        sys.exit(1)
    else:
        print("\n❌ ITERATION REQUIRES REWORK - Fix issues before proceeding")
        sys.exit(2)


if __name__ == "__main__":
    main()
