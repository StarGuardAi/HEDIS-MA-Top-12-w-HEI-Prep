#!/usr/bin/env python
"""
Update compatibility matrix with test results
"""
import sys
from tests.compatibility.compatibility_matrix import CompatibilityMatrix


def main():
    """Update compatibility matrix interactively."""
    matrix = CompatibilityMatrix()
    
    print("Compatibility Matrix Updater")
    print("=" * 60)
    print()
    
    # Show current status
    summary = matrix.get_summary()
    print(f"Current Status:")
    print(f"  Total: {summary['total']}")
    print(f"  Passed: {summary['passed']}")
    print(f"  Failed: {summary['failed']}")
    print(f"  Issues: {summary['issues']}")
    print(f"  Pending: {summary['pending']}")
    print()
    
    # List combinations
    print("Available combinations:")
    for i, combo in enumerate(matrix.matrix["test_combinations"], 1):
        status_icon = {
            "pass": "✅",
            "fail": "❌",
            "issues": "⚠️",
            "pending": "⏳"
        }.get(combo["status"], "❓")
        
        print(f"{i}. {status_icon} {combo['device']} - {combo['browser']} ({combo['resolution']})")
    
    print()
    
    if len(sys.argv) > 1:
        # Command line mode
        if sys.argv[1] == "update":
            if len(sys.argv) < 5:
                print("Usage: python update_matrix.py update <device> <browser> <status> [issues...]")
                print("Status: pass, fail, issues, pending")
                return
            
            device = sys.argv[2]
            browser = sys.argv[3]
            status = sys.argv[4]
            issues = sys.argv[5:] if len(sys.argv) > 5 else []
            
            matrix.update_result(device, browser, status, issues)
            print(f"Updated {device} - {browser} to {status}")
        elif sys.argv[1] == "report":
            report_path = matrix.export_report()
            print(f"Report generated: {report_path}")
        else:
            print("Unknown command. Use 'update' or 'report'")
    else:
        # Interactive mode
        print("Enter combination number to update (or 'q' to quit, 'r' for report):")
        choice = input("> ").strip()
        
        if choice.lower() == 'q':
            return
        elif choice.lower() == 'r':
            report_path = matrix.export_report()
            print(f"Report generated: {report_path}")
            return
        
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(matrix.matrix["test_combinations"]):
                combo = matrix.matrix["test_combinations"][idx]
                print(f"\nUpdating: {combo['device']} - {combo['browser']}")
                print("Status options: pass, fail, issues, pending")
                status = input("Status: ").strip()
                
                if status in ["pass", "fail", "issues", "pending"]:
                    issues = []
                    if status == "issues" or status == "fail":
                        print("Enter issues (one per line, empty line to finish):")
                        while True:
                            issue = input("Issue: ").strip()
                            if not issue:
                                break
                            issues.append(issue)
                    
                    tester = input("Tester name (optional): ").strip() or None
                    
                    matrix.update_result(combo["device"], combo["browser"], status, issues, tester)
                    print("Updated successfully!")
                else:
                    print("Invalid status")
            else:
                print("Invalid selection")
        except ValueError:
            print("Invalid input")


if __name__ == "__main__":
    main()

