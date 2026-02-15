"""
Center all summary data headers and notes on all pages
Match the home page example styling
"""
import os
import sys
from pathlib import Path
import re

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

CENTER_SUMMARY_CSS = '''
/* ========== CENTER SUMMARY HEADERS AND NOTES ========== */

/* Center summary section headers */
h2:contains("Summary"),
h2:contains("Overview"),
h2:contains("Performance"),
h2:contains("Metrics"),
h2:contains("Analysis"),
h3:contains("Summary"),
h3:contains("Overview"),
h3:contains("Performance"),
h3:contains("Metrics"),
h3:contains("Analysis"),
h3:contains("Portfolio"),
h3:contains("ROI"),
h3:contains("Budget"),
h3:contains("Cost"),
h3:contains("Trend"),
h3:contains("Variance"),
h3:contains("Comparison"),
h3:contains("Insights"),
h3:contains("Scenario"),
h3:contains("Tracking"),
h3:contains("Calculator"),
h3:contains("Measure"),
h3:contains("Rating"),
h3:contains("Workflow"),
h3:contains("Predictions"),
h3:contains("Benchmarking"),
h3:contains("Reporting"),
h3:contains("Equity"),
h3:contains("Dashboard"),
h3:contains("Executive"),
h3:contains("Key"),
h3:contains("AI"),
h3:contains("Capabilities"),
h3:contains("Campaign"),
h3:contains("Alert"),
h3:contains("Compliance"),
h3:contains("Chatbot") {
    text-align: center !important;
}

/* Center all h2 and h3 headers that are section headers */
h2, h3 {
    text-align: center !important;
}

/* Center captions and notes */
.stCaption,
[data-testid="stCaption"],
.stMarkdown:has-text("📊"),
.stMarkdown:has-text("💰"),
.stMarkdown:has-text("📈"),
.stMarkdown:has-text("💵"),
.stMarkdown:has-text("🎯"),
.stMarkdown:has-text("🤖"),
.stMarkdown:has-text("📋"),
.stMarkdown:has-text("⭐"),
.stMarkdown:has-text("🔄"),
.stMarkdown:has-text("📊"),
.stMarkdown:has-text("⚖️"),
.stMarkdown:has-text("⚡") {
    text-align: center !important;
}

/* Center markdown headers that are summary sections */
.stMarkdown h2,
.stMarkdown h3 {
    text-align: center !important;
}

/* Center section dividers text */
hr + h2,
hr + h3,
.stMarkdown:has(hr) + h2,
.stMarkdown:has(hr) + h3 {
    text-align: center !important;
}

/* Center notes/details below metrics */
[data-testid="stMetricContainer"] + .stMarkdown,
[data-testid="stMetricContainer"] ~ .stMarkdown,
[data-testid="stMetricValue"] + *,
.stMetric + .stMarkdown {
    text-align: center !important;
}

/* Center all markdown content that follows metrics */
div[data-testid="stVerticalBlock"]:has([data-testid="stMetricContainer"]) + .stMarkdown,
div[data-testid="stVerticalBlock"]:has([data-testid="stMetricContainer"]) ~ .stMarkdown {
    text-align: center !important;
}

/* Center summary statistics headers */
h2:has-text("Summary"),
h3:has-text("Summary"),
h2:has-text("Statistics"),
h3:has-text("Statistics"),
h2:has-text("Overview"),
h3:has-text("Overview") {
    text-align: center !important;
}

/* Center headers that come after dividers (section headers) */
.stMarkdown:has-text("---") + h2,
.stMarkdown:has-text("---") + h3,
hr + h2,
hr + h3 {
    text-align: center !important;
}
'''

def add_center_summary_styling(file_path):
    """Add center-align CSS for summary headers and notes"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if already added
    if 'CENTER SUMMARY HEADERS AND NOTES' in content:
        return False, "Already added"
    
    # Find where to insert (before closing </style> tag)
    style_close_pattern = r'(</style>)'
    
    match = re.search(style_close_pattern, content)
    if match:
        insert_pos = match.start()
        # Insert before </style>
        new_content = content[:insert_pos] + CENTER_SUMMARY_CSS + '\n' + content[insert_pos:]
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True, "Added center-align CSS for summary headers/notes"
    
    return False, "Style block not found"

def main():
    """Add center-align styling for summary headers and notes to all pages"""
    base_dir = Path(__file__).parent
    app_file = base_dir / 'app.py'
    pages_dir = base_dir / 'pages'
    
    print("Adding center-align styling for summary headers and notes...")
    print("=" * 60)
    
    files_to_update = [app_file] + list(pages_dir.glob('*.py'))
    
    stats = {'added': 0, 'skipped': 0, 'errors': 0}
    
    for file_path in files_to_update:
        if not file_path.exists():
            continue
        
        file_name = file_path.name
        
        result, info = add_center_summary_styling(file_path)
        
        if result is True:
            print(f"[ADDED] {file_name} - {info}")
            stats['added'] += 1
        elif result is False:
            if "Already added" in info:
                print(f"[SKIP] {file_name} - {info}")
                stats['skipped'] += 1
            else:
                print(f"[SKIP] {file_name} - {info}")
                stats['skipped'] += 1
        else:
            print(f"[ERROR] {file_name} - {info}")
            stats['errors'] += 1
    
    print("=" * 60)
    print("[SUMMARY]")
    print(f"  Added: {stats['added']}")
    print(f"  Skipped: {stats['skipped']}")
    print(f"  Errors: {stats['errors']}")

if __name__ == '__main__':
    main()


