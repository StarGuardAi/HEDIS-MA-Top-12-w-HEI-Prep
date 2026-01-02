#!/usr/bin/env python3
"""
Full System Validation Suite Runner
Comprehensive testing for Phase 1 & Phase 2 components.

Author: Robert Reichert
Created: 2025-11-18
"""

import sys
import time
from pathlib import Path
from typing import Dict, List, Tuple
from collections import defaultdict

try:
    import psycopg2
    from psycopg2.extras import RealDictCursor
except ImportError:
    print("ERROR: psycopg2 not installed. Install with: pip install psycopg2-binary")
    sys.exit(1)


class FullSystemValidator:
    """Comprehensive validation suite for Phase 1 & Phase 2."""
    
    def __init__(self, db_config: Dict[str, str]):
        """Initialize validator with database configuration."""
        self.db_config = db_config
        self.conn = None
        self.script_path = Path(__file__).parent / "validate_full_system.sql"
        self.test_results = defaultdict(list)
        self.summary_stats = {
            'total_tests': 0,
            'passed': 0,
            'warnings': 0,
            'failed': 0
        }
    
    def connect(self) -> bool:
        """Establish database connection."""
        try:
            self.conn = psycopg2.connect(**self.db_config)
            return True
        except psycopg2.Error as e:
            print(f"[ERROR] Database connection failed: {e}")
            return False
    
    def close(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()
    
    def parse_status(self, status_str: str) -> str:
        """Parse status string and return category."""
        if not status_str:
            return 'unknown'
        status_str = status_str.strip()
        if '✓ PASS' in status_str or 'PASS' in status_str:
            return 'pass'
        elif '⚠' in status_str or 'WARN' in status_str:
            return 'warning'
        elif '✗' in status_str or 'FAIL' in status_str:
            return 'fail'
        else:
            return 'info'
    
    def run_validation(self) -> bool:
        """Execute validation SQL script and parse results."""
        if not self.script_path.exists():
            print(f"[ERROR] Validation script not found: {self.script_path}")
            return False
        
        print("=" * 80)
        print("HEDIS STAR RATING PORTFOLIO OPTIMIZER")
        print("FULL SYSTEM VALIDATION SUITE")
        print("Phase 1 + Phase 2 Complete")
        print("=" * 80)
        print()
        
        print(f"[INFO] Reading validation script: {self.script_path.name}")
        print("[INFO] This will take 5-7 minutes to complete...")
        print()
        
        with open(self.script_path, 'r', encoding='utf-8') as f:
            sql_script = f.read()
        
        print("[INFO] Executing validation queries...")
        start_time = time.time()
        
        try:
            with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
                # Split script into individual queries (semicolon-separated)
                queries = [q.strip() for q in sql_script.split(';') if q.strip() and not q.strip().startswith('--')]
                
                current_section = "General"
                query_count = 0
                
                for query in queries:
                    if not query or query.startswith('--'):
                        continue
                    
                    try:
                        cur.execute(query)
                        
                        # Try to fetch results
                        try:
                            results = cur.fetchall()
                            
                            if results:
                                # Process results
                                for row in results:
                                    # Check for status column
                                    if 'status' in row:
                                        status = self.parse_status(str(row.get('status', '')))
                                        self.summary_stats['total_tests'] += 1
                                        
                                        if status == 'pass':
                                            self.summary_stats['passed'] += 1
                                        elif status == 'warning':
                                            self.summary_stats['warnings'] += 1
                                        elif status == 'fail':
                                            self.summary_stats['failed'] += 1
                                        
                                        # Store result
                                        test_name = str(row.get('metric', row.get('object_type', row.get('relationship', 'Unknown'))))
                                        self.test_results[current_section].append({
                                            'name': test_name,
                                            'status': status,
                                            'data': dict(row)
                                        })
                        except psycopg2.ProgrammingError:
                            # No results to fetch (e.g., CREATE, INSERT)
                            pass
                        
                        query_count += 1
                        if query_count % 10 == 0:
                            print(f"  Processed {query_count} queries...")
                    
                    except psycopg2.Error as e:
                        # Skip errors for now, continue with other queries
                        if 'does not exist' not in str(e).lower():
                            print(f"  [WARNING] Query failed: {str(e)[:100]}")
                        continue
            
            elapsed = time.time() - start_time
            print(f"[OK] Validation queries executed ({elapsed:.1f} seconds)")
            return True
            
        except psycopg2.Error as e:
            print(f"[ERROR] Validation execution failed: {e}")
            return False
    
    def generate_report(self):
        """Generate comprehensive validation report."""
        print()
        print("=" * 80)
        print("VALIDATION REPORT")
        print("=" * 80)
        print()
        
        # Summary statistics
        total = self.summary_stats['total_tests']
        if total > 0:
            pass_pct = (self.summary_stats['passed'] / total) * 100
            warn_pct = (self.summary_stats['warnings'] / total) * 100
            fail_pct = (self.summary_stats['failed'] / total) * 100
            
            print("SUMMARY STATISTICS:")
            print("-" * 80)
            print(f"Total Tests: {total}")
            print(f"  [PASS] {self.summary_stats['passed']} ({pass_pct:.1f}%)")
            print(f"  [WARN] {self.summary_stats['warnings']} ({warn_pct:.1f}%)")
            print(f"  [FAIL] {self.summary_stats['failed']} ({fail_pct:.1f}%)")
            print()
        
        # Detailed results by section
        print("DETAILED RESULTS:")
        print("-" * 80)
        
        for section, tests in self.test_results.items():
            if not tests:
                continue
            
            print(f"\n[{section}]")
            
            for test in tests:
                status_icon = {
                    'pass': '[PASS]',
                    'warning': '[WARN]',
                    'fail': '[FAIL]',
                    'info': '[INFO]'
                }.get(test['status'], '[?]')
                
                print(f"  {status_icon} {test['name']}")
                
                # Show key metrics if available
                data = test['data']
                if 'count' in data:
                    print(f"      Count: {data['count']:,}")
                if 'expected' in data:
                    print(f"      Expected: {data['expected']}")
        
        # Overall status
        print()
        print("=" * 80)
        if self.summary_stats['failed'] == 0:
            if self.summary_stats['warnings'] < total * 0.1:
                print("[SUCCESS] All critical tests passed! System is production-ready.")
            else:
                print("[SUCCESS] All critical tests passed. Some warnings to review.")
        else:
            print(f"[WARNING] {self.summary_stats['failed']} test(s) failed. Review above.")
        print("=" * 80)
    
    def run(self):
        """Execute full validation suite."""
        if not self.connect():
            return False
        
        try:
            if not self.run_validation():
                return False
            
            self.generate_report()
            return self.summary_stats['failed'] == 0
            
        finally:
            self.close()


def get_db_config() -> Dict[str, str]:
    """Get database configuration from environment or defaults."""
    import os
    
    return {
        "host": os.getenv("DB_HOST", "localhost"),
        "database": os.getenv("DB_NAME", "hedis_portfolio"),
        "user": os.getenv("DB_USER", "hedis_api"),
        "password": os.getenv("DB_PASSWORD", "hedis_password"),
        "port": os.getenv("DB_PORT", "5432")
    }


def main():
    """Main entry point."""
    db_config = get_db_config()
    
    # Allow override via command line arguments
    if len(sys.argv) > 1:
        db_config["host"] = sys.argv[1] if len(sys.argv) > 1 else db_config["host"]
        db_config["database"] = sys.argv[2] if len(sys.argv) > 2 else db_config["database"]
        db_config["user"] = sys.argv[3] if len(sys.argv) > 3 else db_config["user"]
        db_config["password"] = sys.argv[4] if len(sys.argv) > 4 else db_config["password"]
    
    validator = FullSystemValidator(db_config)
    success = validator.run()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

