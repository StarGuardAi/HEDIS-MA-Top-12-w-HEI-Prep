#!/usr/bin/env python3
"""
HIPAA PHI Scanner for HEDIS GSD Project
Scans code for potential PHI exposure before commits
"""
import re
import sys
from pathlib import Path

PHI_PATTERNS = {
    'member_id': r'\b(member_id|patient_id|subscriber_id)\s*[=:]\s*["\']?\d+["\']?',
    'ssn': r'\b\d{3}-\d{2}-\d{4}\b',
    'dob': r'\b(dob|date_of_birth|birth_date)\s*[=:]\s*["\']?\d{1,2}[/-]\d{1,2}[/-]\d{2,4}',
    'name': r'\b(first_name|last_name|patient_name)\s*[=:]\s*["\'][A-Z][a-z]+',
}

def scan_file(filepath):
    """Scan a file for PHI patterns"""
    violations = []
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.split('\n')
            
            for pattern_name, pattern in PHI_PATTERNS.items():
                for match in re.finditer(pattern, content, re.IGNORECASE):
                    line_num = content[:match.start()].count('\n') + 1
                    
                    # Skip if in comments explaining the pattern
                    line_content = lines[line_num - 1].strip()
                    if line_content.startswith('#') or line_content.startswith('"""'):
                        continue
                    
                    violations.append({
                        'file': str(filepath),
                        'line': line_num,
                        'type': pattern_name,
                        'text': line_content
                    })
    except Exception as e:
        print(f"Error scanning {filepath}: {e}")
    
    return violations

def scan_project():
    """Scan all Python files in project"""
    project_root = Path.cwd()
    all_violations = []
    
    # Scan Python files
    for py_file in project_root.rglob('*.py'):
        # Skip virtual env and cache
        if any(p in py_file.parts for p in ['venv', '.venv', '__pycache__', 'site-packages']):
            continue
        
        violations = scan_file(py_file)
        all_violations.extend(violations)
    
    return all_violations

if __name__ == '__main__':
    print("🔍 Scanning for PHI exposure...")
    violations = scan_project()
    
    if violations:
        print(f"\n⚠️  Found {len(violations)} potential PHI exposures:\n")
        for v in violations:
            print(f"  {v['file']}:{v['line']} - {v['type']}")
            print(f"    → {v['text']}\n")
        sys.exit(1)
    else:
        print("✅ No obvious PHI patterns detected")
        sys.exit(0)