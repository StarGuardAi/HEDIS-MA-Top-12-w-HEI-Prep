"""
Batch Update Script for Standardized Sidebars
This script helps identify and update sidebar code patterns across all pages.
Run this to see which pages need updates.
"""
import os
import re
from pathlib import Path

PAGES_DIR = Path(__file__).parent / "pages"

# Pattern to find sidebar code blocks
SIDEBAR_PATTERN = r"with st\.sidebar:.*?st\.markdown\(.*?Mobile Optimized.*?\)"

# Pages that need sidebar updates
PAGES_TO_UPDATE = [
    "8_📋_Campaign_Builder.py",
    "9_🔔_Alert_Center.py",
    "10_📈_Historical_Tracking.py",
    "11_💰_ROI_Calculator.py",
    "13_📋_Measure_Analysis.py",
    "14_⭐_Star_Rating_Simulator.py",
    "15_🔄_Gap_Closure_Workflow.py",
    "16_🤖_ML_Gap_Closure_Predictions.py",
    "17_📊_Competitive_Benchmarking.py",
    "18_📋_Compliance_Reporting.py",
    "19_⚖️_Health_Equity_Index.py",
    "Performance_Dashboard.py",
]

# Key mappings for each page
PAGE_KEYS = {
    "8_📋_Campaign_Builder.py": "campaign_builder",
    "9_🔔_Alert_Center.py": "alert_center",
    "10_📈_Historical_Tracking.py": "historical_tracking",
    "11_💰_ROI_Calculator.py": "roi_calculator",
    "13_📋_Measure_Analysis.py": "measure_analysis",
    "14_⭐_Star_Rating_Simulator.py": "star_rating",
    "15_🔄_Gap_Closure_Workflow.py": "gap_closure",
    "16_🤖_ML_Gap_Closure_Predictions.py": "ml_predictions",
    "17_📊_Competitive_Benchmarking.py": "competitive_benchmarking",
    "18_📋_Compliance_Reporting.py": "compliance_reporting",
    "19_⚖️_Health_Equity_Index.py": "health_equity",
    "Performance_Dashboard.py": "performance_dashboard",
}

def generate_sidebar_replacement(page_key: str) -> str:
    """Generate standardized sidebar code for a page."""
    return f'''# Apply sidebar styling FIRST (purple gradient matching StarGuard AI header)
apply_sidebar_styling()

# Standardized sidebar with CTA for recruiters/hiring managers
from utils.standard_sidebar import render_standard_sidebar, get_sidebar_date_range, get_sidebar_membership_size

render_standard_sidebar(
    membership_slider_key="membership_slider_{page_key}",
    start_date_key="sidebar_start_date_{page_key}",
    end_date_key="sidebar_end_date_{page_key}"
)

# Get values from sidebar
membership_size = get_sidebar_membership_size()
start_date, end_date = get_sidebar_date_range()'''

def check_page_needs_update(page_path: Path) -> bool:
    """Check if a page needs sidebar update."""
    try:
        content = page_path.read_text(encoding='utf-8')
        # Check if it already uses standardized sidebar
        if "render_standard_sidebar" in content:
            return False
        # Check if it has old sidebar pattern
        if "with st.sidebar:" in content and "Mobile Optimized" in content:
            return True
        return False
    except Exception as e:
        print(f"Error reading {page_path}: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("Batch Sidebar Update Checker")
    print("=" * 60)
    print()
    
    for page_file in PAGES_TO_UPDATE:
        page_path = PAGES_DIR / page_file
        if page_path.exists():
            needs_update = check_page_needs_update(page_path)
            status = "✅ NEEDS UPDATE" if needs_update else "✓ Already updated"
            print(f"{page_file}: {status}")
        else:
            print(f"{page_file}: ❌ FILE NOT FOUND")
    
    print()
    print("=" * 60)
    print("To update a page, replace the sidebar section with:")
    print("=" * 60)
    print(generate_sidebar_replacement("example_key"))

