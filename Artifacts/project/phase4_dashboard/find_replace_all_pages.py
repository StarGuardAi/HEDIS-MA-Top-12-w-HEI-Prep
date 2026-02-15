"""
Find and Replace Tool for All Dashboard Pages
==============================================

This script performs find/replace operations across all page files in the dashboard.
It includes both app.py (main page) and all files in the pages/ directory.

Usage:
    python find_replace_all_pages.py
    
The script will prompt you for:
    1. Search string (what to find)
    2. Replace string (what to replace it with)
    3. Confirmation before making changes
"""

import os
import re
from pathlib import Path

# Get the directory where this script is located
SCRIPT_DIR = Path(__file__).parent

# Define all files to process
FILES_TO_PROCESS = [
    "app.py",  # Main dashboard page
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
    """
    Perform find/replace in a single file.
    
    Returns:
        tuple: (file_path, replacements_count, success)
    """
    try:
        full_path = SCRIPT_DIR / file_path
        
        if not full_path.exists():
            return (file_path, 0, False, f"File not found: {file_path}")
        
        # Read file content
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Perform replacement
        if use_regex:
            content = re.sub(search_string, replace_string, content)
        else:
            content = content.replace(search_string, replace_string)
        
        # Count replacements
        if use_regex:
            matches = len(re.findall(search_string, original_content))
        else:
            matches = original_content.count(search_string)
        
        # Write back if changed
        if content != original_content:
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return (file_path, matches, True, None)
        else:
            return (file_path, matches, False, "No changes made")
            
    except Exception as e:
        return (file_path, 0, False, str(e))


def main():
    print("=" * 70)
    print("Find & Replace Tool for HEDIS Portfolio Optimizer Pages")
    print("=" * 70)
    print(f"\nThis will process {len(FILES_TO_PROCESS)} files:")
    print(f"  - app.py (main page)")
    print(f"  - {len(FILES_TO_PROCESS) - 1} page files in pages/ directory\n")
    
    # Get search string
    search_string = input("Enter the text to FIND: ").strip()
    if not search_string:
        print("Error: Search string cannot be empty.")
        return
    
    # Get replace string
    replace_string = input("Enter the text to REPLACE it with: ").strip()
    
    # Ask about regex
    use_regex_input = input("Use regex pattern matching? (y/n, default: n): ").strip().lower()
    use_regex = use_regex_input == 'y'
    
    # Show preview
    print("\n" + "=" * 70)
    print("PREVIEW:")
    print("=" * 70)
    print(f"Search for:  {repr(search_string)}")
    print(f"Replace with: {repr(replace_string)}")
    print(f"Use regex: {use_regex}")
    print(f"Files to process: {len(FILES_TO_PROCESS)}")
    print("=" * 70)
    
    # Count matches first (dry run)
    print("\nScanning files for matches...")
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
        print("\n❌ No matches found in any files.")
        return
    
    print(f"\nFound {total_matches} total match(es) in {len(files_with_matches)} file(s):")
    for file_path, count in files_with_matches:
        print(f"  • {file_path}: {count} match(es)")
    
    # Confirm before proceeding
    print("\n" + "=" * 70)
    confirm = input("Proceed with replacement? (yes/no): ").strip().lower()
    
    if confirm not in ['yes', 'y']:
        print("Operation cancelled.")
        return
    
    # Perform replacements
    print("\n" + "=" * 70)
    print("PERFORMING REPLACEMENTS:")
    print("=" * 70)
    
    results = []
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
                print(f"  ⚠️  {file_path}: {matches} match(es) found, but {error}")
        else:
            print(f"  ⏭️  {file_path}: No matches")
        
        results.append(result)
    
    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY:")
    print("=" * 70)
    print(f"Total replacements made: {total_replacements}")
    print(f"Files modified: {successful_files}")
    print(f"Files processed: {len(FILES_TO_PROCESS)}")
    print("=" * 70)
    
    if total_replacements > 0:
        print("\n✅ Replacement complete!")
        print("\n⚠️  IMPORTANT: Review the changes and test your application.")
        print("   Consider committing changes to version control.")
    else:
        print("\n⚠️  No replacements were made.")


if __name__ == "__main__":
    main()

