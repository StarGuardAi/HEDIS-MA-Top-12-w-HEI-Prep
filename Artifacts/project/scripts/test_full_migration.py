#!/usr/bin/env python3
"""
Integration Test Script for Content Migration

Tests complete migration workflow with sample data.
"""

import os
import shutil
import tempfile
from pathlib import Path
import subprocess
import sys


def create_test_source(source_dir: Path):
    """Create test source directory with sample files."""
    source_dir.mkdir(parents=True, exist_ok=True)
    
    # Create sample markdown files
    test_files = {
        'README.md': """# StarGuardAI Project

Welcome to StarGuardAI - healthcare analytics platform.

Contact: info@starguardai.dev
GitHub: https://github.com/StarGuardAI/project

#healthcare #HEDIS #qualitymeasures

## Features

Our platform helps healthcare providers with patient care coordination.

Visit https://github.com/StarGuardAI/docs for more information.
""",
        'docs/overview.md': """# Overview

StarGuard AI provides healthcare analytics solutions.

## Quality Measures

We focus on HEDIS quality measures for patient populations.

Contact StarGuardAI for more information.
""",
        'docs/api.md': """# API Documentation

```python
# Example code
org = "StarGuardAI"
print(f"Working with {org}")
```

API endpoint: https://api.starguardai.dev

#healthcare #analytics
"""
    }
    
    for file_path, content in test_files.items():
        full_path = source_dir / file_path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        full_path.write_text(content, encoding='utf-8')
    
    print(f"[OK] Created test source directory: {source_dir}")
    print(f"    Files created: {len(test_files)}")


def run_migration_test(source_dir: Path, target_dir: Path, dry_run: bool = True):
    """Run migration with test data."""
    print("\n" + "="*60)
    print("RUNNING MIGRATION TEST")
    print("="*60)
    
    script_path = Path(__file__).parent.parent / 'migrate_and_cleanup.py'
    
    cmd = [
        sys.executable,
        str(script_path),
        '--source', str(source_dir),
        '--target', str(target_dir),
        '--all'
    ]
    
    if dry_run:
        cmd.append('--dry-run')
    else:
        cmd.extend(['--backup', '--change-log', str(target_dir / 'MIGRATION_CHANGELOG.md'), '--summary'])
    
    print(f"\n[INFO] Running: {' '.join(cmd)}\n")
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    print(result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)
    
    return result.returncode == 0


def verify_migration(target_dir: Path):
    """Verify migration results."""
    print("\n" + "="*60)
    print("VERIFICATION")
    print("="*60)
    
    script_path = Path(__file__).parent.parent / 'migrate_and_cleanup.py'
    
    cmd = [
        sys.executable,
        str(script_path),
        '--target', str(target_dir),
        '--verify'
    ]
    
    print(f"\n[INFO] Running: {' '.join(cmd)}\n")
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    print(result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)
    
    return result.returncode == 0


def check_files(target_dir: Path):
    """Check that expected files exist."""
    print("\n" + "="*60)
    print("FILE CHECK")
    print("="*60)
    
    expected_files = [
        'README.md',
        'docs/overview.md',
        'docs/api.md',
        'org-contact-info.md',
        'MIGRATION_CHANGELOG.md',
        'VERIFICATION_REPORT.md'
    ]
    
    missing = []
    found = []
    
    for file_path in expected_files:
        full_path = target_dir / file_path
        if full_path.exists():
            found.append(file_path)
            print(f"[OK] Found: {file_path}")
        else:
            missing.append(file_path)
            print(f"[ERROR] Missing: {file_path}")
    
    print(f"\n[STATS] Files found: {len(found)}/{len(expected_files)}")
    
    if missing:
        print(f"[WARN] Missing files: {', '.join(missing)}")
        return False
    
    return True


def check_content(target_dir: Path):
    """Check content for proper replacements."""
    print("\n" + "="*60)
    print("CONTENT CHECK")
    print("="*60)
    
    issues = []
    
    # Check README.md
    readme_path = target_dir / 'README.md'
    if readme_path.exists():
        content = readme_path.read_text(encoding='utf-8')
        
        # Check for old references
        if 'StarGuardAI' in content and 'github.com/StarGuardAI' not in content:
            issues.append("README.md still contains 'StarGuardAI' (not in URL)")
        
        if 'starguardai' in content.lower() and 'github.com' not in content.lower():
            issues.append("README.md still contains 'starguardai' reference")
        
        # Check for new references
        if 'sentinel-analytics' in content:
            print("[OK] README.md contains 'sentinel-analytics'")
        
        # Check for footers
        if 'Sentinel Analytics' in content and 'maintained by' in content:
            print("[OK] README.md has footer")
        
        # Check hashtags
        if '#healthcare' in content:
            issues.append("README.md still contains healthcare hashtag")
        elif '#lawenforcement' in content.lower() or '#intelligence' in content.lower():
            print("[OK] README.md has updated hashtags")
    
    if issues:
        print("\n[ERROR] Content issues found:")
        for issue in issues:
            print(f"   - {issue}")
        return False
    else:
        print("\n[OK] Content checks passed")
        return True


def main():
    """Run complete integration test."""
    print("="*60)
    print("FULL MIGRATION INTEGRATION TEST")
    print("="*60)
    
    # Create temporary directories
    with tempfile.TemporaryDirectory() as tmpdir:
        test_dir = Path(tmpdir) / 'migration_test'
        source_dir = test_dir / 'StarGuardAI'
        target_dir = test_dir / 'sentinel-analytics'
        
        try:
            # Step 1: Create test source
            print("\n[STEP 1] Creating test source directory...")
            create_test_source(source_dir)
            
            # Step 2: Run migration (dry run first)
            print("\n[STEP 2] Running migration (dry run)...")
            if not run_migration_test(source_dir, target_dir, dry_run=True):
                print("[ERROR] Dry run failed")
                return 1
            
            # Step 3: Run actual migration
            print("\n[STEP 3] Running actual migration...")
            if not run_migration_test(source_dir, target_dir, dry_run=False):
                print("[ERROR] Migration failed")
                return 1
            
            # Step 4: Verify migration
            print("\n[STEP 4] Verifying migration...")
            if not verify_migration(target_dir):
                print("[ERROR] Verification failed")
                return 1
            
            # Step 5: Check files
            print("\n[STEP 5] Checking files...")
            if not check_files(target_dir):
                print("[ERROR] File check failed")
                return 1
            
            # Step 6: Check content
            print("\n[STEP 6] Checking content...")
            if not check_content(target_dir):
                print("[ERROR] Content check failed")
                return 1
            
            print("\n" + "="*60)
            print("[OK] ALL TESTS PASSED")
            print("="*60)
            return 0
            
        except Exception as e:
            print(f"\n[ERROR] Test failed with exception: {e}")
            import traceback
            traceback.print_exc()
            return 1


if __name__ == '__main__':
    sys.exit(main())

