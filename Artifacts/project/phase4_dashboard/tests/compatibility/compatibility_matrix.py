"""
Compatibility matrix generator
Creates test matrix and tracks results
"""
import json
from datetime import datetime
from pathlib import Path


class CompatibilityMatrix:
    """Manages compatibility test matrix and results."""
    
    def __init__(self, matrix_file="compatibility_matrix.json"):
        self.matrix_file = Path(__file__).parent / matrix_file
        self.matrix = self._load_matrix()
    
    def _load_matrix(self):
        """Load compatibility matrix from file."""
        if self.matrix_file.exists():
            with open(self.matrix_file, 'r') as f:
                return json.load(f)
        return self._create_default_matrix()
    
    def _create_default_matrix(self):
        """Create default compatibility matrix."""
        return {
            "last_updated": datetime.now().isoformat(),
            "test_combinations": [
                {
                    "device": "Windows 10/11",
                    "resolution": "1920x1080",
                    "browser": "Chrome",
                    "version": "Latest",
                    "status": "pending",
                    "issues": [],
                    "tested_date": None,
                    "tester": None
                },
                {
                    "device": "Windows 10/11",
                    "resolution": "1920x1080",
                    "browser": "Edge",
                    "version": "Latest",
                    "status": "pending",
                    "issues": [],
                    "tested_date": None,
                    "tester": None
                },
                {
                    "device": "Windows 10/11",
                    "resolution": "1920x1080",
                    "browser": "Firefox",
                    "version": "Latest",
                    "status": "pending",
                    "issues": [],
                    "tested_date": None,
                    "tester": None
                },
                {
                    "device": "macOS",
                    "resolution": "2560x1440",
                    "browser": "Chrome",
                    "version": "Latest",
                    "status": "pending",
                    "issues": [],
                    "tested_date": None,
                    "tester": None
                },
                {
                    "device": "macOS",
                    "resolution": "2560x1440",
                    "browser": "Safari",
                    "version": "Latest",
                    "status": "pending",
                    "issues": [],
                    "tested_date": None,
                    "tester": None
                },
                {
                    "device": "macOS",
                    "resolution": "2560x1440",
                    "browser": "Firefox",
                    "version": "Latest",
                    "status": "pending",
                    "issues": [],
                    "tested_date": None,
                    "tester": None
                },
                {
                    "device": "iPad Pro",
                    "resolution": "1024x1366",
                    "browser": "Safari",
                    "version": "iOS 15+",
                    "status": "pending",
                    "issues": [],
                    "tested_date": None,
                    "tester": None
                },
                {
                    "device": "iPad",
                    "resolution": "810x1080",
                    "browser": "Safari",
                    "version": "iOS 15+",
                    "status": "pending",
                    "issues": [],
                    "tested_date": None,
                    "tester": None
                },
                {
                    "device": "Samsung Tab",
                    "resolution": "800x1280",
                    "browser": "Chrome",
                    "version": "Latest",
                    "status": "pending",
                    "issues": [],
                    "tested_date": None,
                    "tester": None
                },
                {
                    "device": "iPhone 14 Pro",
                    "resolution": "393x852",
                    "browser": "Safari",
                    "version": "iOS 15+",
                    "status": "pending",
                    "issues": [],
                    "tested_date": None,
                    "tester": None
                },
                {
                    "device": "iPhone SE",
                    "resolution": "375x667",
                    "browser": "Safari",
                    "version": "iOS 15+",
                    "status": "pending",
                    "issues": [],
                    "tested_date": None,
                    "tester": None
                },
                {
                    "device": "Samsung Galaxy",
                    "resolution": "360x800",
                    "browser": "Chrome",
                    "version": "Latest",
                    "status": "pending",
                    "issues": [],
                    "tested_date": None,
                    "tester": None
                },
                {
                    "device": "Pixel 7",
                    "resolution": "412x915",
                    "browser": "Chrome",
                    "version": "Latest",
                    "status": "pending",
                    "issues": [],
                    "tested_date": None,
                    "tester": None
                }
            ]
        }
    
    def update_result(self, device, browser, status, issues=None, tester=None):
        """Update test result for a combination."""
        for combo in self.matrix["test_combinations"]:
            if combo["device"] == device and combo["browser"] == browser:
                combo["status"] = status
                combo["issues"] = issues or []
                combo["tested_date"] = datetime.now().isoformat()
                combo["tester"] = tester
                break
        
        self.matrix["last_updated"] = datetime.now().isoformat()
        self._save_matrix()
    
    def _save_matrix(self):
        """Save compatibility matrix to file."""
        with open(self.matrix_file, 'w') as f:
            json.dump(self.matrix, f, indent=2)
    
    def get_summary(self):
        """Get summary statistics."""
        total = len(self.matrix["test_combinations"])
        passed = len([c for c in self.matrix["test_combinations"] if c["status"] == "pass"])
        failed = len([c for c in self.matrix["test_combinations"] if c["status"] == "fail"])
        issues = len([c for c in self.matrix["test_combinations"] if c["status"] == "issues"])
        pending = len([c for c in self.matrix["test_combinations"] if c["status"] == "pending"])
        
        return {
            "total": total,
            "passed": passed,
            "failed": failed,
            "issues": issues,
            "pending": pending,
            "completion_rate": ((passed + failed + issues) / total * 100) if total > 0 else 0
        }
    
    def export_report(self, output_file="compatibility_report.md"):
        """Export compatibility matrix as markdown report."""
        summary = self.get_summary()
        
        report = f"""# Compatibility Test Report

Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Summary

- **Total Combinations**: {summary['total']}
- **Passed**: {summary['passed']}
- **Failed**: {summary['failed']}
- **Issues**: {summary['issues']}
- **Pending**: {summary['pending']}
- **Completion Rate**: {summary['completion_rate']:.1f}%

## Test Matrix

| Device | Resolution | Browser | Version | Status | Issues | Tested Date | Tester |
|--------|------------|---------|---------|--------|--------|-------------|--------|
"""
        
        for combo in self.matrix["test_combinations"]:
            status_icon = {
                "pass": "✅",
                "fail": "❌",
                "issues": "⚠️",
                "pending": "⏳"
            }.get(combo["status"], "❓")
            
            issues_str = ", ".join(combo["issues"][:2]) if combo["issues"] else "-"
            if len(combo["issues"]) > 2:
                issues_str += f" (+{len(combo['issues']) - 2} more)"
            
            tested_date = combo["tested_date"][:10] if combo["tested_date"] else "-"
            tester = combo["tester"] or "-"
            
            report += f"| {combo['device']} | {combo['resolution']} | {combo['browser']} | {combo['version']} | {status_icon} {combo['status']} | {issues_str} | {tested_date} | {tester} |\n"
        
        report += "\n## Status Legend\n\n"
        report += "- ✅ **Pass**: All tests pass, no issues\n"
        report += "- ⚠️ **Issues**: Some tests fail, documented issues\n"
        report += "- ❌ **Fail**: Critical failures, not usable\n"
        report += "- ⏳ **Pending**: Not yet tested\n"
        
        # Add issues details
        report += "\n## Detailed Issues\n\n"
        has_issues = False
        for combo in self.matrix["test_combinations"]:
            if combo["issues"]:
                has_issues = True
                report += f"### {combo['device']} - {combo['browser']}\n\n"
                for issue in combo["issues"]:
                    report += f"- {issue}\n"
                report += "\n"
        
        if not has_issues:
            report += "No issues documented.\n"
        
        output_path = Path(__file__).parent / output_file
        with open(output_path, 'w') as f:
            f.write(report)
        
        return output_path

