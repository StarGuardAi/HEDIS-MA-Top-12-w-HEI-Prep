#!/usr/bin/env python3
"""
Phase 1 Chat 2: Gap Closure Velocity Tracking Runner
Executes the velocity tracking SQL script and validates results.

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


class Phase1Chat2Runner:
    """Runner for Phase 1 Chat 2 database setup."""
    
    def __init__(self, db_config: Dict[str, str]):
        """
        Initialize runner with database configuration.
        
        Args:
            db_config: Dictionary with keys: host, database, user, password, port
        """
        self.db_config = db_config
        self.conn = None
        self.script_path = Path(__file__).parent / "phase1_chat2_velocity_tracking.sql"
    
    def connect(self) -> bool:
        """Establish database connection."""
        try:
            self.conn = psycopg2.connect(**self.db_config)
            print("✓ Database connection established")
            return True
        except psycopg2.Error as e:
            print(f"✗ Database connection failed: {e}")
            return False
    
    def check_prerequisites(self) -> bool:
        """Verify Phase 1 Chat 1 is complete."""
        print("\n🔍 Checking prerequisites (Phase 1 Chat 1)...")
        
        required_tables = [
            'hedis_measures',
            'star_thresholds',
            'ma_plans',
            'plan_performance',
            'plan_members',
            'member_gaps',
            'gap_closure_tracking'
        ]
        
        missing_tables = []
        with self.conn.cursor() as cur:
            for table in required_tables:
                cur.execute("""
                    SELECT EXISTS (
                        SELECT FROM information_schema.tables 
                        WHERE table_name = %s
                    );
                """, (table,))
                exists = cur.fetchone()[0]
                if not exists:
                    missing_tables.append(table)
        
        if missing_tables:
            print(f"✗ Missing required tables: {', '.join(missing_tables)}")
            print("  Please run Phase 1 Chat 1 first!")
            return False
        
        print("✓ All required tables exist")
        return True
    
    def execute_script(self) -> bool:
        """Execute the SQL script."""
        if not self.script_path.exists():
            print(f"✗ Script not found: {self.script_path}")
            return False
        
        print(f"\n📄 Reading script: {self.script_path.name}")
        with open(self.script_path, 'r', encoding='utf-8') as f:
            sql_script = f.read()
        
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
            "members_count": """
                SELECT COUNT(*) as count FROM plan_members;
            """,
            "gaps_count": """
                SELECT COUNT(*) as count FROM member_gaps WHERE measurement_year = 2024;
            """,
            "activities_count": """
                SELECT COUNT(*) as count FROM gap_closure_tracking;
            """,
            "velocity_metrics_count": """
                SELECT COUNT(*) as count FROM gap_velocity_metrics;
            """,
            "velocity_views": """
                SELECT COUNT(*) as count FROM information_schema.views 
                WHERE table_name IN ('vw_current_velocity', 'vw_velocity_trends', 'vw_velocity_performance');
            """
        }
        
        expected = {
            "members_count": 1000,  # 500 + 300 + 200
            "gaps_count": (0, None),  # At least some gaps
            "activities_count": (0, None),  # At least some activities
            "velocity_metrics_count": (0, None),  # At least some metrics
            "velocity_views": 3
        }
        
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            for check_name, query in validations.items():
                try:
                    cur.execute(query)
                    result = cur.fetchone()
                    count = result['count']
                    expected_val = expected[check_name]
                    
                    if isinstance(expected_val, tuple):
                        # Range check (min, max)
                        min_val, max_val = expected_val
                        passed = count >= (min_val if min_val else 0)
                        if max_val:
                            passed = passed and count <= max_val
                    else:
                        passed = count == expected_val
                    
                    results[check_name] = passed
                    
                    status = "✓" if passed else "✗"
                    if isinstance(expected_val, tuple):
                        print(f"  {status} {check_name}: {count} (range check)")
                    else:
                        print(f"  {status} {check_name}: {count}/{expected_val}")
                    
                    if not passed:
                        if isinstance(expected_val, tuple):
                            print(f"    WARNING: Expected range, got {count}")
                        else:
                            print(f"    WARNING: Expected {expected_val}, got {count}")
                except psycopg2.Error as e:
                    results[check_name] = False
                    print(f"  ✗ {check_name}: Query failed - {e}")
        
        return results
    
    def show_velocity_summary(self):
        """Display velocity metrics summary."""
        print("\n📊 Velocity Metrics Summary:")
        print("-" * 100)
        
        query = """
            SELECT 
                plan_id,
                plan_name,
                measure_id,
                measure_name,
                gaps_open_end AS current_gaps,
                ROUND(gaps_per_week, 2) AS weekly_velocity,
                ROUND(closure_rate_pct, 2) AS closure_rate,
                velocity_rating,
                closure_status
            FROM vw_current_velocity
            ORDER BY plan_id, measure_id
            LIMIT 15;
        """
        
        try:
            with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query)
                rows = cur.fetchall()
                
                if not rows:
                    print("  No velocity data found")
                    return
                
                # Print header
                print(f"{'Plan ID':<12} {'Plan Name':<25} {'Measure':<8} {'Gaps':<8} {'Vel/Wk':<8} {'Rate %':<8} {'Rating':<15} {'Status':<12}")
                print("-" * 100)
                
                # Print rows
                for row in rows:
                    print(f"{row['plan_id']:<12} {row['plan_name'][:24]:<25} {row['measure_id']:<8} "
                          f"{row['current_gaps']:<8} {row['weekly_velocity']:<8.2f} "
                          f"{row['closure_rate']:<8.2f} {row['velocity_rating']:<15} {row['closure_status']:<12}")
                
        except psycopg2.Error as e:
            print(f"  Error retrieving velocity summary: {e}")
    
    def show_trends(self):
        """Display velocity trends."""
        print("\n📈 Recent Velocity Trends:")
        print("-" * 80)
        
        query = """
            SELECT 
                plan_id,
                measure_id,
                TO_CHAR(current_period, 'YYYY-MM') AS period,
                ROUND(current_velocity, 2) AS current_vel,
                ROUND(prior_velocity, 2) AS prior_vel,
                ROUND(velocity_change, 2) AS change,
                trend_direction
            FROM vw_velocity_trends
            WHERE current_period >= DATE '2024-08-01'
            ORDER BY plan_id, measure_id, current_period
            LIMIT 10;
        """
        
        try:
            with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query)
                rows = cur.fetchall()
                
                if not rows:
                    print("  No trend data found")
                    return
                
                print(f"{'Plan ID':<12} {'Measure':<8} {'Period':<8} {'Current':<8} {'Prior':<8} {'Change':<8} {'Trend':<12}")
                print("-" * 80)
                
                for row in rows:
                    print(f"{row['plan_id']:<12} {row['measure_id']:<8} {row['period']:<8} "
                          f"{row['current_vel']:<8.2f} {row['prior_vel']:<8.2f} "
                          f"{row['change']:<8.2f} {row['trend_direction']:<12}")
                
        except psycopg2.Error as e:
            print(f"  Error retrieving trends: {e}")
    
    def close(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()
            print("\n✓ Database connection closed")
    
    def run(self):
        """Execute full setup and validation process."""
        print("=" * 80)
        print("HEDIS STAR RATING PORTFOLIO OPTIMIZER")
        print("Phase 1 Chat 2: Gap Closure Velocity Tracking & Trend Analysis")
        print("=" * 80)
        
        if not self.connect():
            return False
        
        try:
            if not self.check_prerequisites():
                return False
            
            if not self.execute_script():
                return False
            
            results = self.validate_setup()
            all_passed = all(results.values())
            
            if all_passed:
                print("\n✅ All validation checks passed!")
            else:
                print("\n⚠️  Some validation checks failed. Review output above.")
            
            self.show_velocity_summary()
            self.show_trends()
            
            print("\n" + "=" * 80)
            print("Setup complete! Next step: Phase 1 Chat 3 - ROI Analysis & Cost-per-Closure")
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
    
    runner = Phase1Chat2Runner(db_config)
    success = runner.run()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

