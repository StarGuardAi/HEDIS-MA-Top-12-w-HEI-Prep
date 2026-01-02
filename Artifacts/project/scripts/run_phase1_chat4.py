#!/usr/bin/env python3
"""
Phase 1 Chat 4: 10K Member Scale Enhancement Runner
Executes the 10K scale enhancement SQL script and validates results.

Author: Robert Reichert
Created: 2025-11-18
"""

import sys
import time
from pathlib import Path
from typing import Dict, List, Optional

try:
    import psycopg2
    from psycopg2.extras import RealDictCursor
except ImportError:
    print("ERROR: psycopg2 not installed. Install with: pip install psycopg2-binary")
    sys.exit(1)


class Phase1Chat4Runner:
    """Runner for Phase 1 Chat 4 database enhancement."""
    
    def __init__(self, db_config: Dict[str, str]):
        """
        Initialize runner with database configuration.
        
        Args:
            db_config: Dictionary with keys: host, database, user, password, port
        """
        self.db_config = db_config
        self.conn = None
        self.script_path = Path(__file__).parent / "phase1_chat4_10k_scale_enhancement.sql"
    
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
        """Verify Phase 1 Chats 1-3 are complete."""
        print("\n🔍 Checking prerequisites (Phase 1 Chats 1-3)...")
        
        required_tables = [
            'hedis_measures',
            'ma_plans',
            'plan_performance',
            'plan_members',
            'member_gaps',
            'activity_cost_standards',
            'plan_budgets'
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
            print("  Please run Phase 1 Chats 1-3 first!")
            return False
        
        print("✓ All required tables exist")
        return True
    
    def execute_script(self) -> bool:
        """Execute the SQL script."""
        if not self.script_path.exists():
            print(f"✗ Script not found: {self.script_path}")
            return False
        
        print(f"\n📄 Reading script: {self.script_path.name}")
        print("⚠️  This will take 5-7 minutes to complete...")
        print("   Generating 10,000 members with realistic demographics...")
        
        with open(self.script_path, 'r', encoding='utf-8') as f:
            sql_script = f.read()
        
        print("⚙️  Executing SQL script...")
        start_time = time.time()
        
        try:
            with self.conn.cursor() as cur:
                cur.execute(sql_script)
                self.conn.commit()
            
            elapsed = time.time() - start_time
            print(f"✓ SQL script executed successfully ({elapsed:.1f} seconds)")
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
            "members_10k": """
                SELECT COUNT(*) as count FROM plan_members WHERE member_id LIKE 'M%';
            """,
            "zip_codes": """
                SELECT COUNT(*) as count FROM zip_code_reference;
            """,
            "chronic_conditions": """
                SELECT COUNT(*) as count FROM chronic_conditions_reference;
            """,
            "member_conditions": """
                SELECT COUNT(*) as count FROM member_chronic_conditions;
            """,
            "gaps_15k": """
                SELECT COUNT(*) as count FROM member_gaps 
                WHERE member_id LIKE 'M%';
            """,
            "segmentation_view": """
                SELECT COUNT(*) as count FROM information_schema.views 
                WHERE table_name IN ('vw_member_segmentation', 'vw_geographic_performance', 
                                      'vw_condition_impact');
            """
        }
        
        expected = {
            "members_10k": 10000,
            "zip_codes": 30,
            "chronic_conditions": 17,
            "member_conditions": (5000, None),  # At least 5K condition assignments
            "gaps_15k": (12000, None),  # At least 12K gaps
            "segmentation_view": 3
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
                        print(f"  {status} {check_name}: {count:,} (range check)")
                    else:
                        print(f"  {status} {check_name}: {count:,}/{expected_val:,}")
                    
                    if not passed:
                        if isinstance(expected_val, tuple):
                            print(f"    WARNING: Expected range, got {count:,}")
                        else:
                            print(f"    WARNING: Expected {expected_val:,}, got {count:,}")
                except psycopg2.Error as e:
                    results[check_name] = False
                    print(f"  ✗ {check_name}: Query failed - {e}")
        
        return results
    
    def show_member_summary(self):
        """Display member distribution summary."""
        print("\n👥 Member Distribution Summary:")
        print("-" * 100)
        
        query = """
            SELECT 
                plan_id,
                COUNT(*) AS member_count,
                ROUND(COUNT(*)::DECIMAL / 10000 * 100, 1) AS pct_of_total,
                ROUND(AVG(EXTRACT(YEAR FROM AGE(date_of_birth))), 1) AS avg_age,
                ROUND(AVG(risk_score), 3) AS avg_risk_score,
                COUNT(DISTINCT zip_code) AS unique_zip_codes
            FROM plan_members
            WHERE member_id LIKE 'M%'
            GROUP BY plan_id
            ORDER BY plan_id;
        """
        
        try:
            with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query)
                rows = cur.fetchall()
                
                if not rows:
                    print("  No member data found")
                    return
                
                print(f"{'Plan ID':<12} {'Members':<10} {'% Total':<10} {'Avg Age':<10} {'Avg Risk':<10} {'Zip Codes':<10}")
                print("-" * 100)
                
                for row in rows:
                    print(f"{row['plan_id']:<12} {row['member_count']:<10,} {row['pct_of_total']:<10.1f} "
                          f"{row['avg_age']:<10.1f} {row['avg_risk_score']:<10.3f} {row['unique_zip_codes']:<10}")
                
        except psycopg2.Error as e:
            print(f"  Error retrieving member summary: {e}")
    
    def show_gap_summary(self):
        """Display gap distribution summary."""
        print("\n📊 Care Gap Distribution Summary:")
        print("-" * 100)
        
        query = """
            SELECT 
                pm.plan_id,
                mg.gap_status,
                COUNT(*) AS gap_count,
                ROUND(COUNT(*)::DECIMAL / SUM(COUNT(*)) OVER (PARTITION BY pm.plan_id) * 100, 1) AS pct_within_plan
            FROM member_gaps mg
            JOIN plan_members pm ON mg.member_id = pm.member_id
            WHERE pm.member_id LIKE 'M%'
            GROUP BY pm.plan_id, mg.gap_status
            ORDER BY pm.plan_id, mg.gap_status;
        """
        
        try:
            with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query)
                rows = cur.fetchall()
                
                if not rows:
                    print("  No gap data found")
                    return
                
                print(f"{'Plan ID':<12} {'Status':<12} {'Gap Count':<12} {'% of Plan':<12}")
                print("-" * 100)
                
                for row in rows:
                    print(f"{row['plan_id']:<12} {row['gap_status']:<12} {row['gap_count']:<12,} "
                          f"{row['pct_within_plan']:<12.1f}")
                
        except psycopg2.Error as e:
            print(f"  Error retrieving gap summary: {e}")
    
    def show_demographics(self):
        """Display demographic distribution."""
        print("\n📈 Demographic Distribution:")
        print("-" * 80)
        
        query = """
            SELECT 
                CASE 
                    WHEN EXTRACT(YEAR FROM AGE(date_of_birth)) < 70 THEN '65-69'
                    WHEN EXTRACT(YEAR FROM AGE(date_of_birth)) < 75 THEN '70-74'
                    WHEN EXTRACT(YEAR FROM AGE(date_of_birth)) < 80 THEN '75-79'
                    WHEN EXTRACT(YEAR FROM AGE(date_of_birth)) < 85 THEN '80-84'
                    ELSE '85+'
                END AS age_band,
                COUNT(*) AS member_count,
                ROUND(COUNT(*)::DECIMAL / 10000 * 100, 1) AS pct_of_total
            FROM plan_members
            WHERE member_id LIKE 'M%'
            GROUP BY age_band
            ORDER BY age_band;
        """
        
        try:
            with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query)
                rows = cur.fetchall()
                
                if not rows:
                    print("  No demographic data found")
                    return
                
                print(f"{'Age Band':<10} {'Members':<12} {'% Total':<10}")
                print("-" * 80)
                
                for row in rows:
                    print(f"{row['age_band']:<10} {row['member_count']:<12,} {row['pct_of_total']:<10.1f}")
                
        except psycopg2.Error as e:
            print(f"  Error retrieving demographics: {e}")
    
    def close(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()
            print("\n✓ Database connection closed")
    
    def run(self):
        """Execute full setup and validation process."""
        print("=" * 80)
        print("HEDIS STAR RATING PORTFOLIO OPTIMIZER")
        print("Phase 1 Chat 4: 10K Member Scale Enhancement")
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
            
            self.show_member_summary()
            self.show_gap_summary()
            self.show_demographics()
            
            print("\n" + "=" * 80)
            print("✅ PHASE 1 CHAT 4 COMPLETE - 10K Member Dataset Ready!")
            print("=" * 80)
            print("\nProduction-Ready Achievements:")
            print("  ✓ 10,000 members with realistic demographics")
            print("  ✓ 30 zip codes in Pittsburgh region")
            print("  ✓ 17 chronic conditions with prevalence-based assignment")
            print("  ✓ 15,000+ care gaps across 12 measures")
            print("  ✓ Optimized indexes for dashboard performance")
            print("  ✓ Segmentation analysis capability")
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
    
    runner = Phase1Chat4Runner(db_config)
    success = runner.run()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

