"""
Find and Replace Tool - Command Line Version
=============================================

Usage:
    python find_replace_cli.py "text to find" "replacement text"
    
Example:
    python find_replace_cli.py "StarGuard AI" "StarGuard Healthcare AI"
"""

import sys
import os
import re
from pathlib import Path

# Get the directory where this script is located
SCRIPT_DIR = Path(__file__).parent

# Define all files to process
FILES_TO_PROCESS = [
    "app.py",
    "pages/1_📊_ROI_by_Measure.py",
    "pages/2_💰_Cost_Per_Closure.py",
    "pages/3_📈_Monthly_Trend.py",
    "pages/4_💵_Budget_Variance.py",
    "pages/5_🎯_Cost_Tier_Comparison.py",
    "pages/6_🤖_AI_Executive_Insights.py",
    "pages/7_📊_What-If_Scenario_Modeler.py",
    "pages/8_🎓_AI_Capabilities_Demo.py",
    "pages/8_📋_Campaign_Builder.py",
    "pages/9_🔔_Alert_Center.py",
    "pages/10_📈_Historical_Tracking.py",
    "pages/11_💰_ROI_Calculator.py",
    "pages/13_📋_Measure_Analysis.py",
    "pages/14_⭐_Star_Rating_Simulator.py",
    "pages/15_🔄_Gap_Closure_Workflow.py",
    "pages/16_🤖_ML_Gap_Closure_Predictions.py",
    "pages/17_📊_Competitive_Benchmarking.py",
    "pages/18_📋_Compliance_Reporting.py",
    "pages/18_🤖_Secure_AI_Chatbot.py",
    "pages/19_⚖️_Health_Equity_Index.py",
    "pages/z_Performance_Dashboard.py",
]


def find_replace_in_file(file_path, search_string, replace_string, use_regex=False):
    """Perform find/replace in a single file."""
    try:
        full_path = SCRIPT_DIR / file_path
        
        if not full_path.exists():
            return (file_path, 0, False, f"File not found")
        
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        if use_regex:
            content = re.sub(search_string, replace_string, content)
            matches = len(re.findall(search_string, original_content))
        else:
            content = content.replace(search_string, replace_string)
            matches = original_content.count(search_string)
        
        if content != original_content:
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return (file_path, matches, True, None)
        else:
            return (file_path, matches, False, "No changes")
            
    except Exception as e:
        return (file_path, 0, False, str(e))


def main():
    if len(sys.argv) < 3:
        print("Usage: python find_replace_cli.py \"text to find\" \"replacement text\"")
        print("\nExample:")
        print('  python find_replace_cli.py "StarGuard AI" "StarGuard Healthcare AI"')
        sys.exit(1)
    
    search_string = sys.argv[1]
    replace_string = sys.argv[2]
    use_regex = len(sys.argv) > 3 and sys.argv[3].lower() == '--regex'
    
    print("=" * 70)
    print("Find & Replace Tool - Command Line Version")
    print("=" * 70)
    print(f"Search for:  {repr(search_string)}")
    print(f"Replace with: {repr(replace_string)}")
    print(f"Use regex: {use_regex}")
    print(f"Files to process: {len(FILES_TO_PROCESS)}")
    print("=" * 70)
    
    # Count matches first
    print("\nScanning files...")
    total_matches = 0
    files_with_matches = []
    
    for file_path in FILES_TO_PROCESS:
        full_path = SCRIPT_DIR / file_path
        if full_path.exists():
            try:
                with open(full_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                if use_regex:
                    matches = len(re.findall(search_string, content))
                else:
                    matches = content.count(search_string)
                
                if matches > 0:
                    files_with_matches.append((file_path, matches))
                    total_matches += matches
            except Exception as e:
                print(f"  ⚠️  Error reading {file_path}: {e}")
    
    if total_matches == 0:
        print("\n❌ No matches found.")
        return
    
    print(f"\nFound {total_matches} match(es) in {len(files_with_matches)} file(s):")
    for file_path, count in files_with_matches:
        print(f"  • {file_path}: {count} match(es)")
    
    # Perform replacements
    print("\n" + "=" * 70)
    print("PERFORMING REPLACEMENTS:")
    print("=" * 70)
    
    total_replacements = 0
    successful_files = 0
    
    for file_path in FILES_TO_PROCESS:
        result = find_replace_in_file(file_path, search_string, replace_string, use_regex)
        file_path, matches, success, error = result
        
        if matches > 0:
            if success:
                print(f"  ✅ {file_path}: {matches} replacement(s)")
                total_replacements += matches
                successful_files += 1
            else:
                print(f"  ⚠️  {file_path}: {error}")
        else:
            print(f"  ⏭️  {file_path}: No matches")
    
    print("\n" + "=" * 70)
    print("SUMMARY:")
    print("=" * 70)
    print(f"Total replacements: {total_replacements}")
    print(f"Files modified: {successful_files}")
    print(f"Files processed: {len(FILES_TO_PROCESS)}")
    print("=" * 70)
    
    if total_replacements > 0:
        print("\n✅ Replacement complete!")
    else:
        print("\n⚠️  No replacements made.")


if __name__ == "__main__":
    main()

