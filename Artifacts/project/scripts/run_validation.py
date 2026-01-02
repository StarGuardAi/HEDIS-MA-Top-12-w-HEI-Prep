#!/usr/bin/env python3
"""
10K Dataset Validation Suite Runner
Executes comprehensive validation tests and generates summary report.

Author: Robert Reichert
Created: 2025-11-18
"""

import sys
import subprocess
from pathlib import Path
from typing import Dict, Optional

try:
    import psycopg2
    from psycopg2.extras import RealDictCursor
except ImportError:
    print("ERROR: psycopg2 not installed. Install with: pip install psycopg2-binary")
    sys.exit(1)


class ValidationRunner:
    """Runner for 10K dataset validation suite."""
    
    def __init__(self, db_config: Dict[str, str]):
        """
        Initialize runner with database configuration.
        
        Args:
            db_config: Dictionary with keys: host, database, user, password, port
        """
        self.db_config = db_config
        self.conn = None
        self.script_path = Path(__file__).parent / "validate_10k_dataset.sql"
    
    def connect(self) -> bool:
        """Establish database connection."""
        try:
            self.conn = psycopg2.connect(**self.db_config)
            print("[OK] Database connection established")
            return True
        except psycopg2.Error as e:
            print(f"[FAIL] Database connection failed: {e}")
            return False
    
    def check_prerequisites(self) -> bool:
        """Verify 10K dataset exists."""
        print("\n[CHECK] Checking prerequisites...")
        
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT COUNT(*) FROM plan_members WHERE member_id LIKE 'M%';
            """)
            member_count = cur.fetchone()[0]
            
            if member_count < 9000:
                print(f"[FAIL] Only {member_count:,} members found. Expected 10,000.")
                print("  Please run Phase 1 Chat 4 first!")
                return False
            
            print(f"[OK] Found {member_count:,} members")
            return True
    
    def run_validation(self) -> bool:
        """Execute validation SQL script using psql."""
        import os
        
        if not self.script_path.exists():
            print(f"[FAIL] Validation script not found: {self.script_path}")
            return False
        
        print(f"\n[RUN] Running validation suite: {self.script_path.name}")
        print("   This will take 2-3 minutes...")
        print("   Generating 25 comprehensive validation reports...\n")
        
        # Build psql command
        psql_cmd = [
            "psql",
            "-h", self.db_config["host"],
            "-d", self.db_config["database"],
            "-U", self.db_config["user"],
            "-f", str(self.script_path),
            "-o", str(self.script_path.parent / "validation_report.txt")
        ]
        
        # Set password via environment variable
        env = dict(os.environ)
        env["PGPASSWORD"] = self.db_config["password"]
        
        try:
            result = subprocess.run(
                psql_cmd,
                env=env,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            if result.returncode == 0:
                print("[SUCCESS] Validation suite completed successfully")
                print(f"  Full report saved to: validation_report.txt")
                return True
            else:
                print(f"[FAIL] Validation failed with return code {result.returncode}")
                if result.stderr:
                    print(f"  Error: {result.stderr[:500]}")
                return False
                
        except subprocess.TimeoutExpired:
            print("[FAIL] Validation timed out after 5 minutes")
            return False
        except FileNotFoundError:
            print("[FAIL] psql command not found. Please install PostgreSQL client tools.")
            print("  Alternative: Run validation script directly in psql or pgAdmin")
            return False
    
    def quick_summary(self):
        """Generate quick validation summary."""
        print("\n[SUMMARY] Quick Validation Summary:")
        print("-" * 80)
        
        queries = {
            "Members": "SELECT COUNT(*) FROM plan_members WHERE member_id LIKE 'M%';",
            "Gaps": "SELECT COUNT(*) FROM member_gaps WHERE member_id LIKE 'M%';",
            "Conditions": "SELECT COUNT(*) FROM member_chronic_conditions;",
            "Zip Codes": "SELECT COUNT(DISTINCT zip_code) FROM plan_members WHERE member_id LIKE 'M%';",
            "Views": "SELECT COUNT(*) FROM pg_views WHERE schemaname = 'public' AND viewname LIKE 'vw_%';"
        }
        
        try:
            with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
                for metric, query in queries.items():
                    cur.execute(query)
                    result = cur.fetchone()
                    count = list(result.values())[0] if result else 0
                    print(f"  {metric:<15}: {count:,}")
                
        except psycopg2.Error as e:
            print(f"  Error generating summary: {e}")
    
    def close(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()
    
    def run(self):
        """Execute full validation process."""
        import os
        
        print("=" * 80)
        print("HEDIS STAR RATING PORTFOLIO OPTIMIZER")
        print("10K Dataset Validation Suite")
        print("=" * 80)
        
        if not self.connect():
            return False
        
        try:
            if not self.check_prerequisites():
                return False
            
            self.quick_summary()
            
            print("\n" + "=" * 80)
            print("Running comprehensive validation suite...")
            print("=" * 80)
            
            if not self.run_validation():
                return False
            
            print("\n" + "=" * 80)
            print("[SUCCESS] VALIDATION COMPLETE!")
            print("=" * 80)
            print("\nReview validation_report.txt for detailed results.")
            print("\nResults Interpretation:")
            print("  [PASS]  - Metric within acceptable range, production-ready")
            print("  [WARN]  - Metric outside ideal range but acceptable for demo")
            print("  [FAIL]  - Issue requires attention")
            print("=" * 80)
            
            return True
            
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
    
    runner = ValidationRunner(db_config)
    success = runner.run()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

