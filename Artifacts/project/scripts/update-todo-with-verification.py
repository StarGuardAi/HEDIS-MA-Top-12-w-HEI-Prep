#!/usr/bin/env python3
"""
Update Todo with Verification Results

This script updates the tasks/todo.md file with verification results from each iteration.
"""

import os
import sys
import json
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TodoUpdater:
    """
    Updates todo.md with verification results.
    """
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.todo_file = self.project_root / 'tasks' / 'todo.md'
        
    def update_with_verification_results(self, verification_results: Dict[str, Any]):
        """
        Update todo.md with verification results.
        
        Args:
            verification_results: Results from iteration verification
        """
        logger.info("Updating todo.md with verification results...")
        
        # Read current todo.md
        if self.todo_file.exists():
            with open(self.todo_file, 'r') as f:
                current_content = f.read()
        else:
            current_content = "# HEDIS GSD Prediction Engine - Current Tasks\n\n"
        
        # Generate verification section
        verification_section = self._generate_verification_section(verification_results)
        
        # Update content
        updated_content = self._update_todo_content(current_content, verification_section)
        
        # Write updated content
        with open(self.todo_file, 'w') as f:
            f.write(updated_content)
        
        logger.info(f"Todo updated with verification results: {self.todo_file}")
    
    def _generate_verification_section(self, results: Dict[str, Any]) -> str:
        """Generate verification section for todo.md."""
        section = []
        section.append("## 🔍 Verification Results")
        section.append("")
        section.append(f"**Iteration ID:** {results.get('iteration_id', 'Unknown')}")
        section.append(f"**Timestamp:** {results.get('timestamp', 'Unknown')}")
        section.append(f"**Overall Status:** {results.get('overall_status', 'Unknown')}")
        section.append(f"**Approval Status:** {results.get('approval_status', 'Unknown')}")
        section.append("")
        
        # Success criteria results
        success_criteria = results.get('success_criteria', {})
        section.append("### Success Criteria Verification")
        section.append(f"- **Status:** {success_criteria.get('overall_status', 'Unknown')}")
        
        criteria_checks = success_criteria.get('criteria_checks', {})
        for criterion, details in criteria_checks.items():
            status_icon = '✅' if details['status'] == 'PASS' else '❌'
            section.append(f"- {status_icon} **{criterion.replace('_', ' ').title()}:** {details['status']} ({details['score']})")
        
        section.append("")
        
        # Testing verification results
        testing_verification = results.get('testing_verification', {})
        section.append("### Testing Verification")
        section.append(f"- **Status:** {testing_verification.get('overall_status', 'Unknown')}")
        
        test_checks = testing_verification.get('test_checks', {})
        for test_type, details in test_checks.items():
            status_icon = '✅' if details['status'] == 'PASS' else '❌'
            section.append(f"- {status_icon} **{test_type.replace('_', ' ').title()}:** {details['status']} ({details['score']})")
        
        section.append("")
        
        # Coverage summary
        if testing_verification.get('coverage_analysis'):
            coverage = testing_verification['coverage_analysis']
            section.append("### Test Coverage Summary")
            section.append(f"- **Total Coverage:** {coverage.get('total_coverage', 0):.1f}%")
            section.append(f"- **Line Coverage:** {coverage.get('line_coverage', 0)}%")
            section.append(f"- **Files Covered:** {coverage.get('files_covered', 0)}")
            section.append("")
        
        # Test quality metrics
        if testing_verification.get('test_quality_metrics'):
            metrics = testing_verification['test_quality_metrics']
            section.append("### Test Quality Metrics")
            section.append(f"- **Total Tests:** {metrics.get('total_tests', 0)}")
            section.append(f"- **Pass Rate:** {metrics.get('pass_rate', 0):.1%}")
            section.append("")
        
        # Recommendations
        recommendations = results.get('recommendations', [])
        if recommendations:
            section.append("### Recommendations")
            for rec in recommendations:
                section.append(f"- {rec}")
            section.append("")
        
        # Next steps
        section.append("### Next Steps")
        overall_status = results.get('overall_status', 'Unknown')
        if overall_status == 'APPROVED':
            section.append("- ✅ Iteration approved - proceed to next development phase")
            section.append("- 📋 Update project documentation")
            section.append("- 🚀 Begin next iteration planning")
        elif overall_status == 'CONDITIONAL_APPROVAL':
            section.append("- ⚠️ Address warning conditions")
            section.append("- 🔄 Re-run verification")
            section.append("- ✅ Proceed once warnings resolved")
        else:
            section.append("- ❌ Fix critical issues identified")
            section.append("- 🔄 Re-run verification")
            section.append("- 📋 Update development plan if needed")
        
        section.append("")
        section.append("---")
        section.append("")
        
        return "\n".join(section)
    
    def _update_todo_content(self, current_content: str, verification_section: str) -> str:
        """Update todo.md content with verification results."""
        lines = current_content.split('\n')
        
        # Find where to insert verification section
        insert_index = len(lines)
        
        # Look for existing verification section
        for i, line in enumerate(lines):
            if line.startswith("## 🔍 Verification Results"):
                # Remove existing verification section
                j = i
                while j < len(lines) and not (lines[j].startswith("## ") and j > i):
                    j += 1
                lines = lines[:i] + lines[j:]
                insert_index = i
                break
        
        # Insert new verification section
        lines.insert(insert_index, verification_section)
        
        return '\n'.join(lines)


def main():
    """Main function to update todo with verification results."""
    if len(sys.argv) < 2:
        print("Usage: python update-todo-with-verification.py <verification_results_file>")
        sys.exit(1)
    
    results_file = Path(sys.argv[1])
    if not results_file.exists():
        print(f"Error: Results file not found: {results_file}")
        sys.exit(1)
    
    # Load verification results
    with open(results_file, 'r') as f:
        verification_results = json.load(f)
    
    # Update todo.md
    updater = TodoUpdater()
    updater.update_with_verification_results(verification_results)
    
    print("✅ Todo updated with verification results")


if __name__ == "__main__":
    main()
