#!/usr/bin/env python3
"""
Phase 1 Complete Setup Runner
Executes all Phase 1 scripts in sequence (Chats 1-4) plus validation.

Author: Robert Reichert
Created: 2025-11-18
"""

import sys
import subprocess
import time
from pathlib import Path
from typing import Dict, List

try:
    import psycopg2
    from psycopg2.extras import RealDictCursor
except ImportError:
    print("ERROR: psycopg2 not installed. Install with: pip install psycopg2-binary")
    sys.exit(1)


class Phase1MasterRunner:
    """Master runner for all Phase 1 scripts."""
    
    def __init__(self, db_config: Dict[str, str]):
        """Initialize with database configuration."""
        self.db_config = db_config
        self.conn = None
        self.scripts_dir = Path(__file__).parent
        self.scripts = [
            ("Phase 1 Chat 1: Foundation", "phase1_chat1_foundation.sql", 30),
            ("Phase 1 Chat 2: Velocity Tracking", "phase1_chat2_velocity_tracking.sql", 180),
            ("Phase 1 Chat 3: ROI Analysis", "phase1_chat3_roi_analysis.sql", 180),
            ("Phase 1 Chat 4: 10K Scale Enhancement", "phase1_chat4_10k_scale_enhancement.sql", 420),
        ]
    
    def connect(self) -> bool:
        """Establish database connection."""
        try:
            self.conn = psycopg2.connect(**self.db_config)
            print("[OK] Database connection established")
            return True
        except psycopg2.Error as e:
            print(f"X Database connection failed: {e}")
            print("\nPlease ensure:")
            print("  1. PostgreSQL is installed and running")
            print("  2. Database 'hedis_portfolio' exists")
            print("  3. User 'hedis_api' has appropriate permissions")
            return False
    
    def execute_sql_file(self, script_path: Path) -> bool:
        """Execute SQL file using psycopg2."""
        if not script_path.exists():
            print(f"X Script not found: {script_path}")
            return False
        
        print(f"   Reading: {script_path.name}")
        with open(script_path, 'r', encoding='utf-8') as f:
            sql_content = f.read()
        
        try:
            with self.conn.cursor() as cur:
                cur.execute(sql_content)
                self.conn.commit()
            return True
        except psycopg2.Error as e:
            self.conn.rollback()
            print(f"X SQL execution failed: {e}")
            if hasattr(e, 'pgcode'):
                print(f"   Error code: {e.pgcode}")
            if hasattr(e, 'pgerror'):
                print(f"   Details: {e.pgerror}")
            return False
    
    def run_script(self, name: str, filename: str, estimated_seconds: int) -> bool:
        """Run a single Phase 1 script."""
        script_path = self.scripts_dir / filename
        
        print(f"\n{'='*80}")
        print(f"{name}")
        print(f"{'='*80}")
        print(f"Estimated time: {estimated_seconds // 60} minutes {estimated_seconds % 60} seconds")
        
        if not script_path.exists():
            print(f"X Script file not found: {filename}")
            return False
        
        start_time = time.time()
        success = self.execute_sql_file(script_path)
        elapsed = time.time() - start_time
        
        if success:
            print(f"[OK] Completed in {elapsed:.1f} seconds")
            return True
        else:
            print(f"[FAIL] Failed after {elapsed:.1f} seconds")
            return False
    
    def validate_setup(self) -> bool:
        """Quick validation that setup completed."""
        print(f"\n{'='*80}")
        print("Quick Validation Check")
        print(f"{'='*80}")
        
        checks = {
            "HEDIS Measures": "SELECT COUNT(*) FROM hedis_measures;",
            "Star Thresholds": "SELECT COUNT(*) FROM star_thresholds WHERE measurement_year = 2024;",
            "MA Plans": "SELECT COUNT(*) FROM ma_plans;",
            "Plan Performance": "SELECT COUNT(*) FROM plan_performance WHERE measurement_year = 2024;",
            "Members (10K)": "SELECT COUNT(*) FROM plan_members WHERE member_id LIKE 'M%';",
            "Member Gaps": "SELECT COUNT(*) FROM member_gaps WHERE member_id LIKE 'M%';",
        }
        
        all_passed = True
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            for check_name, query in checks.items():
                try:
                    cur.execute(query)
                    result = cur.fetchone()
                    # RealDictCursor returns dict, get first value
                    count = list(result.values())[0] if result else 0
                    status = "[OK]" if count > 0 else "[FAIL]"
                    print(f"  {status} {check_name}: {count:,}")
                    if count == 0 and check_name in ["HEDIS Measures", "MA Plans"]:
                        all_passed = False
                except (psycopg2.Error, TypeError, IndexError) as e:
                    print(f"  [FAIL] {check_name}: Query failed - {e}")
                    all_passed = False
        
        return all_passed
    
    def close(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()
    
    def run(self):
        """Execute all Phase 1 scripts in sequence."""
        print("=" * 80)
        print("HEDIS STAR RATING PORTFOLIO OPTIMIZER")
        print("Phase 1 Complete Setup - All Scripts")
        print("=" * 80)
        
        if not self.connect():
            return False
        
        total_start = time.time()
        
        try:
            for name, filename, est_seconds in self.scripts:
                if not self.run_script(name, filename, est_seconds):
                    print(f"\n[FAIL] Setup failed at {name}")
                    print("  Please fix errors above before continuing")
                    return False
                
                # Brief pause between scripts
                time.sleep(2)
            
            # Final validation
            if self.validate_setup():
                total_elapsed = time.time() - total_start
                print(f"\n{'='*80}")
                print("[SUCCESS] PHASE 1 COMPLETE!")
                print(f"{'='*80}")
                print(f"Total execution time: {total_elapsed // 60:.0f} minutes {total_elapsed % 60:.0f} seconds")
                print("\nNext steps:")
                print("  1. Run validation suite: python run_validation.py")
                print("  2. Review data quality reports")
                print("  3. Proceed to Phase 2 for operational dashboards")
                print("=" * 80)
                return True
            else:
                print("\n⚠️  Setup completed but validation found issues")
                print("  Review validation results above")
                return False
                
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
    import os
    
    db_config = get_db_config()
    
    # Allow override via command line arguments
    if len(sys.argv) > 1:
        db_config["host"] = sys.argv[1] if len(sys.argv) > 1 else db_config["host"]
        db_config["database"] = sys.argv[2] if len(sys.argv) > 2 else db_config["database"]
        db_config["user"] = sys.argv[3] if len(sys.argv) > 3 else db_config["user"]
        db_config["password"] = sys.argv[4] if len(sys.argv) > 4 else db_config["password"]
    
    runner = Phase1MasterRunner(db_config)
    success = runner.run()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

