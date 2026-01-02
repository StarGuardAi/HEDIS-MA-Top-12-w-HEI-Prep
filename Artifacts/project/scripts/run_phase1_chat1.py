#!/usr/bin/env python3
"""
Phase 1 Chat 1: Database Setup Runner
Executes the revenue calculator foundation SQL script and validates results.

Author: Robert Reichert
Created: 2025-11-18
"""

import sys
from pathlib import Path
from typing import Dict, List, Optional

try:
    import psycopg2
    from psycopg2.extras import RealDictCursor
except ImportError:
    print("ERROR: psycopg2 not installed. Install with: pip install psycopg2-binary")
    sys.exit(1)


class Phase1Chat1Runner:
    """Runner for Phase 1 Chat 1 database setup."""
    
    def __init__(self, db_config: Dict[str, str]):
        """
        Initialize runner with database configuration.
        
        Args:
            db_config: Dictionary with keys: host, database, user, password, port
        """
        self.db_config = db_config
        self.conn = None
        self.script_path = Path(__file__).parent / "phase1_chat1_revenue_calculator_foundation.sql"
    
    def connect(self) -> bool:
        """Establish database connection."""
        try:
            self.conn = psycopg2.connect(**self.db_config)
            print("✓ Database connection established")
            return True
        except psycopg2.Error as e:
            print(f"✗ Database connection failed: {e}")
            return False
    
    def execute_script(self) -> bool:
        """Execute the SQL script."""
        if not self.script_path.exists():
            print(f"✗ Script not found: {self.script_path}")
            return False
        
        print(f"\n📄 Reading script: {self.script_path.name}")
        with open(self.script_path, 'r', encoding='utf-8') as f:
            sql_script = f.read()
        
        # Split by semicolons but preserve function/view definitions
        # Simple approach: execute as single transaction
        print("⚙️  Executing SQL script...")
        try:
            with self.conn.cursor() as cur:
                cur.execute(sql_script)
                self.conn.commit()
            print("✓ SQL script executed successfully")
            return True
        except psycopg2.Error as e:
            self.conn.rollback()
            print(f"✗ SQL execution failed: {e}")
            print(f"  Error detail: {e.pgcode} - {e.pgerror}")
            return False
    
    def validate_setup(self) -> Dict[str, bool]:
        """Run validation queries to verify setup."""
        print("\n🔍 Running validation checks...")
        results = {}
        
        validations = {
            "measures_count": """
                SELECT COUNT(*) as count FROM hedis_measures;
            """,
            "thresholds_count": """
                SELECT COUNT(*) as count FROM star_thresholds WHERE measurement_year = 2024;
            """,
            "plans_count": """
                SELECT COUNT(*) as count FROM ma_plans;
            """,
            "performance_count": """
                SELECT COUNT(*) as count FROM plan_performance WHERE measurement_year = 2024;
            """,
            "revenue_view": """
                SELECT COUNT(*) as count FROM vw_revenue_at_risk WHERE measurement_year = 2024;
            """
        }
        
        expected = {
            "measures_count": 12,
            "thresholds_count": 84,  # 12 measures × 7 thresholds
            "plans_count": 3,
            "performance_count": 36,  # 12 measures × 3 plans
            "revenue_view": 36  # All measures have gaps
        }
        
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            for check_name, query in validations.items():
                try:
                    cur.execute(query)
                    result = cur.fetchone()
                    count = result['count']
                    expected_count = expected[check_name]
                    passed = count == expected_count
                    results[check_name] = passed
                    
                    status = "✓" if passed else "✗"
                    print(f"  {status} {check_name}: {count}/{expected_count}")
                    
                    if not passed:
                        print(f"    WARNING: Expected {expected_count}, got {count}")
                except psycopg2.Error as e:
                    results[check_name] = False
                    print(f"  ✗ {check_name}: Query failed - {e}")
        
        return results
    
    def show_revenue_summary(self):
        """Display revenue at risk summary."""
        print("\n💰 Revenue at Risk Summary:")
        print("-" * 80)
        
        query = """
            SELECT 
                plan_id,
                plan_name,
                COUNT(DISTINCT measure_id) AS measures_at_risk,
                SUM(members_needed) AS total_gaps,
                ROUND(SUM(revenue_at_risk)::numeric, 2) AS total_revenue_at_risk,
                ROUND(SUM(weighted_revenue_impact)::numeric, 2) AS weighted_total
            FROM vw_revenue_at_risk
            WHERE measurement_year = 2024
            GROUP BY plan_id, plan_name
            ORDER BY total_revenue_at_risk DESC;
        """
        
        try:
            with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query)
                rows = cur.fetchall()
                
                if not rows:
                    print("  No revenue at risk data found")
                    return
                
                # Print header
                print(f"{'Plan ID':<12} {'Plan Name':<30} {'Measures':<10} {'Gaps':<10} {'Revenue ($)':<15} {'Weighted ($)':<15}")
                print("-" * 80)
                
                # Print rows
                total_revenue = 0
                total_gaps = 0
                for row in rows:
                    print(f"{row['plan_id']:<12} {row['plan_name']:<30} {row['measures_at_risk']:<10} "
                          f"{row['total_gaps']:<10} ${row['total_revenue_at_risk']:>13,.2f} ${row['weighted_total']:>13,.2f}")
                    total_revenue += float(row['total_revenue_at_risk'])
                    total_gaps += row['total_gaps']
                
                print("-" * 80)
                print(f"{'PORTFOLIO TOTAL':<42} {total_gaps:<10} ${total_revenue:>13,.2f}")
                
        except psycopg2.Error as e:
            print(f"  Error retrieving revenue summary: {e}")
    
    def close(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()
            print("\n✓ Database connection closed")
    
    def run(self):
        """Execute full setup and validation process."""
        print("=" * 80)
        print("HEDIS STAR RATING PORTFOLIO OPTIMIZER")
        print("Phase 1 Chat 1: Revenue at Risk Calculator Foundation")
        print("=" * 80)
        
        if not self.connect():
            return False
        
        try:
            if not self.execute_script():
                return False
            
            results = self.validate_setup()
            all_passed = all(results.values())
            
            if all_passed:
                print("\n✅ All validation checks passed!")
            else:
                print("\n⚠️  Some validation checks failed. Review output above.")
            
            self.show_revenue_summary()
            
            print("\n" + "=" * 80)
            print("Setup complete! Next step: Phase 1 Chat 2 - Gap Closure Velocity")
            print("=" * 80)
            
            return all_passed
            
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
    
    runner = Phase1Chat1Runner(db_config)
    success = runner.run()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

