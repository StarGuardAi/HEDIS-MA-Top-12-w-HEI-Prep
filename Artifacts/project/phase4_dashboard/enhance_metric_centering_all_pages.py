"""
Enhance metric centering CSS on all pages - site-wide rule
"""
import os
import sys
from pathlib import Path
import re

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

METRIC_CENTERING_CSS = '''
/* ========== RULE: CENTER ALL METRIC HEADERS OVER DATA ========== */
/* This is a site-wide standard - metric labels center over values */

/* Center the metric label text (header above the number) */
[data-testid="stMetricLabel"] {
    display: flex !important;
    justify-content: center !important;
    width: 100% !important;
    text-align: center !important;
}

[data-testid="stMetricLabel"] > div {
    width: 100% !important;
    text-align: center !important;
    margin: 0 auto !important;
}

[data-testid="stMetricLabel"] label,
[data-testid="stMetricLabel"] p,
[data-testid="stMetricLabel"] span {
    width: 100% !important;
    text-align: center !important;
    display: block !important;
}

/* Center the metric value (the big number) */
[data-testid="stMetricValue"] {
    display: flex !important;
    justify-content: center !important;
    width: 100% !important;
    text-align: center !important;
}

[data-testid="stMetricValue"] > div {
    width: 100% !important;
    text-align: center !important;
    margin: 0 auto !important;
}

/* Center the delta indicator (+$1,264,020 annually, etc.) */
[data-testid="stMetricDelta"] {
    display: flex !important;
    justify-content: center !important;
    width: 100% !important;
}

[data-testid="stMetricDelta"] > div {
    text-align: center !important;
}

/* Center the entire metric container */
[data-testid="metric-container"] {
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
    text-align: center !important;
    width: 100% !important;
}

/* Center metric containers */
div[data-testid="stMetricContainer"] {
    text-align: center !important;
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
}

/* Ensure columns containing metrics are centered */
[data-testid="column"] > div > div > div {
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
}

/* Center any custom metric-style headers (non-st.metric) */
.metric-header, .kpi-header, .summary-header {
    text-align: center !important;
    width: 100% !important;
    display: block !important;
}

/* Center st.caption used as metric labels */
[data-testid="stCaptionContainer"] {
    text-align: center !important;
    width: 100% !important;
}

[data-testid="stCaptionContainer"] p {
    text-align: center !important;
}

/* Fix for columns - ensure flex centering */
.row-widget.stHorizontalBlock > div {
    display: flex !important;
    justify-content: center !important;
}

.row-widget.stHorizontalBlock [data-testid="column"] {
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
}
'''

def check_conflicting_css(file_path):
    """Check for CSS that might override centering"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    conflicts = []
    
    # Check for left-align in metric contexts
    patterns = [
        (r'\[data-testid="stMetric.*?"\].*?text-align:\s*left', 'Left-align in metric styling'),
        (r'\[data-testid="stMetric.*?"\].*?justify-content:\s*flex-start', 'Flex-start in metric styling'),
        (r'\[data-testid="stMetric.*?"\].*?align-items:\s*flex-start', 'Flex-start alignment in metric styling'),
        (r'\.metric-header.*?text-align:\s*left', 'Left-align in custom metric headers'),
        (r'\.kpi-header.*?text-align:\s*left', 'Left-align in KPI headers'),
    ]
    
    for pattern, description in patterns:
        if re.search(pattern, content, re.DOTALL | re.IGNORECASE):
            conflicts.append(description)
    
    return conflicts

def check_custom_metrics(file_path):
    """Check for custom metric implementations"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    custom_metrics = []
    
    # Look for custom HTML metrics
    patterns = [
        (r'st\.markdown\(["\']<h[1-6]>.*?["\']', 'Custom HTML headers used as metrics'),
        (r'st\.markdown\(["\']<p\s+class=["\']big-number', 'Custom big-number paragraphs'),
        (r'st\.markdown\(["\']<div\s+class=["\']metric', 'Custom metric divs'),
        (r'compact_metric_card', 'Custom compact metric cards'),
    ]
    
    for pattern, description in patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        if matches:
            custom_metrics.append(f"{description} ({len(matches)} found)")
    
    return custom_metrics

def add_enhanced_metric_css(file_path):
    """Add enhanced metric centering CSS to a file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if already enhanced
    if 'RULE: CENTER ALL METRIC HEADERS OVER DATA' in content:
        return False, "Already enhanced"
    
    # Find where to insert (before closing </style> tag, after existing metric CSS)
    # Look for existing CENTER KPI/METRIC HEADERS section
    metric_section_pattern = r'(/\* ========== CENTER KPI/METRIC HEADERS.*?\*/)'
    
    match = re.search(metric_section_pattern, content, re.DOTALL)
    if match:
        # Insert after the existing section
        insert_pos = match.end()
        # Find the next closing brace or comment
        next_section = re.search(r'\n/\* ==========', content[insert_pos:])
        if next_section:
            insert_pos = insert_pos + next_section.start()
        
        new_content = content[:insert_pos] + '\n' + METRIC_CENTERING_CSS + '\n' + content[insert_pos:]
    else:
        # No existing section, find </style> tag
        style_close_pattern = r'(</style>)'
        match = re.search(style_close_pattern, content)
        if match:
            insert_pos = match.start()
            new_content = content[:insert_pos] + METRIC_CENTERING_CSS + '\n' + content[insert_pos:]
        else:
            return False, "Style block not found"
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    return True, "Added enhanced metric centering CSS"

def main():
    """Enhance metric centering CSS on all pages"""
    base_dir = Path(__file__).parent
    app_file = base_dir / 'app.py'
    pages_dir = base_dir / 'pages'
    
    print("Enhancing metric centering CSS (site-wide rule)...")
    print("=" * 60)
    
    files_to_update = list(pages_dir.glob('*.py'))
    
    stats = {'added': 0, 'skipped': 0, 'conflicts': 0, 'custom': 0, 'errors': 0}
    
    for file_path in files_to_update:
        if not file_path.exists():
            continue
        
        file_name = file_path.name
        
        try:
            # Check for conflicts
            conflicts = check_conflicting_css(file_path)
            if conflicts:
                print(f"[CONFLICT] {file_name} - {', '.join(conflicts)}")
                stats['conflicts'] += 1
            
            # Check for custom metrics
            custom = check_custom_metrics(file_path)
            if custom:
                print(f"[CUSTOM] {file_name} - {', '.join(custom)}")
                stats['custom'] += 1
            
            # Add CSS
            result, info = add_enhanced_metric_css(file_path)
            
            if result:
                print(f"[ADDED] {file_name} - {info}")
                stats['added'] += 1
            else:
                if "Already enhanced" in info:
                    print(f"[SKIP] {file_name} - {info}")
                else:
                    print(f"[SKIP] {file_name} - {info}")
                stats['skipped'] += 1
        except Exception as e:
            print(f"[ERROR] {file_name} - {str(e)}")
            stats['errors'] += 1
    
    print("=" * 60)
    print("[SUMMARY]")
    print(f"  Added: {stats['added']}")
    print(f"  Skipped: {stats['skipped']}")
    print(f"  Conflicts found: {stats['conflicts']}")
    print(f"  Custom metrics found: {stats['custom']}")
    print(f"  Errors: {stats['errors']}")

if __name__ == '__main__':
    main()


