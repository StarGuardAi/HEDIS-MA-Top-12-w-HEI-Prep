"""
Add JavaScript metric centering to all pages
"""
import os
import sys
from pathlib import Path
import re

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

JS_METRIC_CENTERING = '''
    // ====================================================================
    // FORCE CENTER ALL METRIC LABELS AND VALUES
    // ====================================================================
    function forceCenterMetrics() {
        // Find all metric containers
        const metricContainers = document.querySelectorAll('[data-testid="stMetricContainer"]');
        
        metricContainers.forEach(container => {
            // Force center alignment on container
            container.style.textAlign = 'center';
            container.style.display = 'flex';
            container.style.flexDirection = 'column';
            container.style.alignItems = 'center';
            container.style.justifyContent = 'center';
            
            // Find and center label
            const label = container.querySelector('[data-testid="stMetricLabel"]');
            if (label) {
                label.style.textAlign = 'center';
                label.style.width = '100%';
                label.style.display = 'block';
                label.style.marginLeft = 'auto';
                label.style.marginRight = 'auto';
                
                // Center all children
                const labelChildren = label.querySelectorAll('*');
                labelChildren.forEach(child => {
                    child.style.textAlign = 'center';
                    child.style.marginLeft = 'auto';
                    child.style.marginRight = 'auto';
                });
            }
            
            // Find and center value
            const value = container.querySelector('[data-testid="stMetricValue"]');
            if (value) {
                value.style.textAlign = 'center';
                value.style.width = '100%';
                value.style.display = 'block';
                value.style.marginLeft = 'auto';
                value.style.marginRight = 'auto';
                
                // Center all children
                const valueChildren = value.querySelectorAll('*');
                valueChildren.forEach(child => {
                    child.style.textAlign = 'center';
                    child.style.marginLeft = 'auto';
                    child.style.marginRight = 'auto';
                });
            }
            
            // Find and center delta
            const delta = container.querySelector('[data-testid="stMetricDelta"]');
            if (delta) {
                delta.style.textAlign = 'center';
                delta.style.width = '100%';
                delta.style.display = 'block';
                delta.style.marginLeft = 'auto';
                delta.style.marginRight = 'auto';
                
                // Center all children
                const deltaChildren = delta.querySelectorAll('*');
                deltaChildren.forEach(child => {
                    child.style.textAlign = 'center';
                    child.style.marginLeft = 'auto';
                    child.style.marginRight = 'auto';
                });
            }
        });
    }
    
    // Run immediately and on delays
    forceCenterMetrics();
    setTimeout(forceCenterMetrics, 100);
    setTimeout(forceCenterMetrics, 500);
    setTimeout(forceCenterMetrics, 1000);
    setTimeout(forceCenterMetrics, 2000);
    
    // Watch for new metrics being added
    const metricObserver = new MutationObserver(function() {
        forceCenterMetrics();
    });
    
    metricObserver.observe(document.body, {
        childList: true,
        subtree: true
    });
'''

def add_js_metric_centering(file_path):
    """Add JavaScript metric centering to a file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if already added
    if 'FORCE CENTER ALL METRIC LABELS AND VALUES' in content:
        return False, "Already added"
    
    # Find the closing </script> tag in the JavaScript section
    # Look for the Performance Dashboard emoji fix script
    script_pattern = r'(setTimeout\(fixPerformanceDashboardLabel, 2000\);)\s*(</script>)'
    
    match = re.search(script_pattern, content, re.DOTALL)
    if match:
        # Insert before </script>
        insert_pos = match.end(1)
        new_content = content[:insert_pos] + JS_METRIC_CENTERING + '\n' + content[insert_pos:]
    else:
        # Try to find any </script> tag
        script_close_pattern = r'(</script>)'
        match = re.search(script_close_pattern, content)
        if match:
            insert_pos = match.start()
            new_content = content[:insert_pos] + JS_METRIC_CENTERING + '\n' + content[insert_pos:]
        else:
            return False, "Script tag not found"
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    return True, "Added JavaScript metric centering"

def main():
    """Add JavaScript metric centering to all pages"""
    base_dir = Path(__file__).parent
    app_file = base_dir / 'app.py'
    pages_dir = base_dir / 'pages'
    
    print("Adding JavaScript metric centering...")
    print("=" * 60)
    
    files_to_update = [app_file] + list(pages_dir.glob('*.py'))
    
    stats = {'added': 0, 'skipped': 0, 'errors': 0}
    
    for file_path in files_to_update:
        if not file_path.exists():
            continue
        
        file_name = file_path.name
        
        try:
            result, info = add_js_metric_centering(file_path)
            
            if result:
                print(f"[ADDED] {file_name} - {info}")
                stats['added'] += 1
            else:
                if "Already added" in info:
                    print(f"[SKIP] {file_name} - {info}")
                else:
                    print(f"[SKIP] {file_name} - {info}")
                stats['skipped'] += 1
        except Exception as e:
            print(f"[ERROR] {file_name} - {str(e)}")
            stats['errors'] += 1
    
    print("=" * 60)
    print(f"[SUMMARY] Added: {stats['added']}, Skipped: {stats['skipped']}, Errors: {stats['errors']}")

if __name__ == '__main__':
    main()


