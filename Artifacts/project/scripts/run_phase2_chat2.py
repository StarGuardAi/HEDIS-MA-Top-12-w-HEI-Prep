#!/usr/bin/env python3
"""
Phase 2 Chat 2: Provider Network Performance & Attribution Analytics Runner
Executes the Phase 2 Chat 2 SQL script and validates results.

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


class Phase2Chat2Runner:
    """Runner for Phase 2 Chat 2 provider network analytics."""
    
    def __init__(self, db_config: Dict[str, str]):
        """
        Initialize runner with database configuration.
        
        Args:
            db_config: Dictionary with keys: host, database, user, password, port
        """
        self.db_config = db_config
        self.conn = None
        self.script_path = Path(__file__).parent / "phase2_chat2_provider_network.sql"
    
    def connect(self) -> bool:
        """Establish database connection."""
        try:
            self.conn = psycopg2.connect(**self.db_config)
            print("[OK] Database connection established")
            return True
        except psycopg2.Error as e:
            print(f"[ERROR] Database connection failed: {e}")
            return False
    
    def check_prerequisites(self) -> bool:
        """Verify Phase 1 and Phase 2 Chat 1 are complete."""
        print("\n[CHECK] Checking prerequisites (Phase 1 Chats 1-4, Phase 2 Chat 1)...")
        
        required_tables = [
            'hedis_measures',
            'ma_plans',
            'plan_performance',
            'plan_members',
            'member_gaps',
            'member_engagement_scores',
            'zip_code_reference',
            'member_chronic_conditions'
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
            print(f"[ERROR] Missing required tables: {', '.join(missing_tables)}")
            print("  Please run Phase 1 Chats 1-4 and Phase 2 Chat 1 first!")
            return False
        
        # Check for 10K members
        with self.conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM plan_members WHERE member_id LIKE 'M%'")
            member_count = cur.fetchone()[0]
            if member_count < 1000:
                print(f"[WARNING] Only {member_count} members found. Expected ~10,000.")
                print("  Phase 1 Chat 4 should have generated 10K members.")
                response = input("  Continue anyway? (y/n): ")
                if response.lower() != 'y':
                    return False
        
        print("[OK] All required tables exist")
        print(f"[OK] Found {member_count} members")
        return True
    
    def execute_script(self) -> bool:
        """Execute the SQL script."""
        if not self.script_path.exists():
            print(f"[ERROR] Script not found: {self.script_path}")
            return False
        
        print(f"\n[INFO] Reading script: {self.script_path.name}")
        print("[INFO] This will take 4-5 minutes to complete...")
        print("   Generating 500+ providers across 18 specialties...")
        print("   Attributing 10K members to providers...")
        print("   Calculating provider performance metrics...")
        
        with open(self.script_path, 'r', encoding='utf-8') as f:
            sql_script = f.read()
        
        print("[INFO] Executing SQL script...")
        start_time = time.time()
        
        try:
            with self.conn.cursor() as cur:
                cur.execute(sql_script)
                self.conn.commit()
            
            elapsed = time.time() - start_time
            print(f"[OK] SQL script executed successfully ({elapsed:.1f} seconds)")
            return True
        except psycopg2.Error as e:
            self.conn.rollback()
            print(f"[ERROR] SQL execution failed: {e}")
            print(f"  Error detail: {e.pgcode} - {e.pgerror}")
            if hasattr(e, 'diag') and e.diag:
                context = getattr(e.diag, 'context', None)
                if context:
                    print(f"  Context: {context}")
            return False
    
    def validate_setup(self) -> Dict[str, bool]:
        """Run validation queries to verify setup."""
        print("\n[CHECK] Running validation checks...")
        results = {}
        
        validations = {
            "provider_directory": """
                SELECT COUNT(*) as count FROM provider_directory;
            """,
            "provider_performance": """
                SELECT COUNT(*) as count FROM provider_performance;
            """,
            "member_provider_attribution": """
                SELECT COUNT(*) as count FROM member_provider_attribution WHERE is_current = TRUE;
            """,
            "provider_referrals": """
                SELECT COUNT(*) as count FROM provider_referrals;
            """,
            "provider_collaboration_scores": """
                SELECT COUNT(*) as count FROM provider_collaboration_scores;
            """,
            "provider_performance_summary_view": """
                SELECT COUNT(*) as count FROM vw_provider_performance_summary;
            """,
            "provider_measure_performance_view": """
                SELECT COUNT(*) as count FROM vw_provider_measure_performance;
            """,
            "network_adequacy_view": """
                SELECT COUNT(*) as count FROM vw_network_adequacy_dashboard;
            """
        }
        
        expected = {
            "provider_directory": 500,  # 250 PCPs + 250 Specialists
            "provider_performance": None,  # Variable based on attribution
            "member_provider_attribution": 13500,  # 10K PCP + ~3.5K Specialist
            "provider_referrals": 1500,  # Sample referrals
            "provider_collaboration_scores": 500,  # One per active provider
            "provider_performance_summary_view": 500,
            "provider_measure_performance_view": None,  # Variable
            "network_adequacy_view": None  # Variable by specialty
        }
        
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            for check_name, query in validations.items():
                try:
                    cur.execute(query)
                    result = cur.fetchone()
                    count = result['count']
                    expected_count = expected[check_name]
                    
                    if expected_count is None:
                        passed = count > 0
                        status = "[OK]" if passed else "[ERROR]"
                        print(f"  {status} {check_name}: {count} (expected > 0)")
                    else:
                        # Allow some variance for random generation
                        variance = abs(count - expected_count) / expected_count if expected_count > 0 else 0
                        passed = variance < 0.15  # Allow 15% variance
                        status = "[OK]" if passed else "[WARNING]"
                        print(f"  {status} {check_name}: {count}/{expected_count}")
                        
                        if not passed:
                            print(f"    NOTE: Expected ~{expected_count}, got {count} (variance: {variance*100:.1f}%)")
                    
                    results[check_name] = passed
                except psycopg2.Error as e:
                    results[check_name] = False
                    print(f"  [ERROR] {check_name}: Query failed - {e}")
        
        return results
    
    def show_provider_summary(self):
        """Display provider directory summary."""
        print("\n[REPORT] Provider Directory Summary:")
        print("-" * 80)
        
        query = """
            SELECT 
                provider_type,
                COUNT(*) AS provider_count,
                COUNT(CASE WHEN network_status = 'Active' THEN 1 END) AS active_count,
                COUNT(CASE WHEN accepting_new_patients THEN 1 END) AS accepting_new,
                ROUND(AVG(patient_satisfaction_score), 2) AS avg_satisfaction,
                ROUND(AVG(years_in_practice), 1) AS avg_years_practice
            FROM provider_directory
            GROUP BY provider_type
            ORDER BY provider_count DESC;
        """
        
        try:
            with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query)
                rows = cur.fetchall()
                
                if not rows:
                    print("  No provider data found")
                    return
                
                # Print header
                print(f"{'Type':<15} {'Total':<10} {'Active':<10} {'Accepting':<12} {'Avg Sat':<10} {'Avg Years':<10}")
                print("-" * 80)
                
                # Print rows
                for row in rows:
                    print(f"{row['provider_type']:<15} {row['provider_count']:<10} "
                          f"{row['active_count']:<10} {row['accepting_new']:<12} "
                          f"{row['avg_satisfaction']:<10} {row['avg_years_practice']:<10}")
                
        except psycopg2.Error as e:
            print(f"  Error retrieving provider summary: {e}")
    
    def show_attribution_summary(self):
        """Display member attribution coverage."""
        print("\n[REPORT] Member Attribution Coverage:")
        print("-" * 80)
        
        query = """
            SELECT 
                'Total Members' AS metric,
                COUNT(*) AS count
            FROM plan_members
            WHERE member_id LIKE 'M%'
            UNION ALL
            SELECT 
                'Members with PCP',
                COUNT(DISTINCT member_id)
            FROM member_provider_attribution
            WHERE attribution_type = 'PCP'
              AND is_current = TRUE
            UNION ALL
            SELECT 
                'Members with Specialist',
                COUNT(DISTINCT member_id)
            FROM member_provider_attribution
            WHERE attribution_type = 'Specialist'
              AND is_current = TRUE;
        """
        
        try:
            with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query)
                rows = cur.fetchall()
                
                if not rows:
                    print("  No attribution data found")
                    return
                
                # Print header
                print(f"{'Metric':<30} {'Count':<15} {'% of Total':<15}")
                print("-" * 80)
                
                # Get total for percentage calculation
                total_members = None
                for row in rows:
                    if row['metric'] == 'Total Members':
                        total_members = row['count']
                        break
                
                # Print rows
                for row in rows:
                    pct = (row['count'] / total_members * 100) if total_members else 0
                    print(f"{row['metric']:<30} {row['count']:<15} {pct:>13.1f}%")
                
        except psycopg2.Error as e:
            print(f"  Error retrieving attribution summary: {e}")
    
    def show_performance_summary(self):
        """Display provider performance summary."""
        print("\n[REPORT] Provider Performance Summary (Top 10 Specialties):")
        print("-" * 100)
        
        query = """
            SELECT 
                specialty,
                total_providers,
                total_members_attributed,
                ROUND(members_per_provider, 1) AS members_per_provider,
                ROUND(providers_per_1000_members, 2) AS providers_per_1000,
                adequacy_rating
            FROM vw_network_adequacy_dashboard
            ORDER BY total_members_attributed DESC
            LIMIT 10;
        """
        
        try:
            with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query)
                rows = cur.fetchall()
                
                if not rows:
                    print("  No performance data found")
                    return
                
                # Print header
                print(f"{'Specialty':<25} {'Providers':<12} {'Members':<12} {'Mem/Prov':<12} {'Prov/1K':<12} {'Rating':<15}")
                print("-" * 100)
                
                # Print rows
                for row in rows:
                    providers_per_1k = row['providers_per_1000'] or 0
                    adequacy = row['adequacy_rating'] or 'N/A'
                    print(f"{row['specialty']:<25} {row['total_providers']:<12} "
                          f"{row['total_members_attributed']:<12} {row['members_per_provider'] or 0:<12} "
                          f"{providers_per_1k:<12} {adequacy:<15}")
                
        except psycopg2.Error as e:
            print(f"  Error retrieving performance summary: {e}")
    
    def show_collaboration_summary(self):
        """Display collaboration scores distribution."""
        print("\n[REPORT] Provider Collaboration Score Distribution:")
        print("-" * 80)
        
        query = """
            SELECT 
                collaboration_tier,
                COUNT(*) AS provider_count,
                ROUND(AVG(overall_collaboration_score), 1) AS avg_score,
                ROUND(AVG(gap_closure_rate_pct), 1) AS avg_closure_rate,
                ROUND(AVG(avg_days_to_close_gap), 1) AS avg_days_to_close
            FROM provider_collaboration_scores
            GROUP BY collaboration_tier
            ORDER BY 
                CASE collaboration_tier
                    WHEN 'Excellent' THEN 1
                    WHEN 'Good' THEN 2
                    WHEN 'Fair' THEN 3
                    ELSE 4
                END;
        """
        
        try:
            with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query)
                rows = cur.fetchall()
                
                if not rows:
                    print("  No collaboration data found")
                    return
                
                # Print header
                print(f"{'Tier':<15} {'Providers':<12} {'Avg Score':<12} {'Closure %':<12} {'Days':<12}")
                print("-" * 80)
                
                # Print rows
                for row in rows:
                    print(f"{row['collaboration_tier']:<15} {row['provider_count']:<12} "
                          f"{row['avg_score']:<12} {row['avg_closure_rate']:<12} "
                          f"{row['avg_days_to_close']:<12}")
                
        except psycopg2.Error as e:
            print(f"  Error retrieving collaboration summary: {e}")
    
    def close(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()
            print("\n[OK] Database connection closed")
    
    def run(self):
        """Execute full setup and validation process."""
        print("=" * 80)
        print("HEDIS STAR RATING PORTFOLIO OPTIMIZER")
        print("Phase 2 Chat 2: Provider Network Performance & Attribution Analytics")
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
                print("\n[SUCCESS] All validation checks passed!")
            else:
                print("\n[WARNING] Some validation checks had warnings. Review output above.")
            
            self.show_provider_summary()
            self.show_attribution_summary()
            self.show_performance_summary()
            self.show_collaboration_summary()
            
            print("\n" + "=" * 80)
            print("Setup complete! Next step: Phase 2 Chat 3 - Predictive Analytics & Risk Scoring")
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
    
    runner = Phase2Chat2Runner(db_config)
    success = runner.run()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

