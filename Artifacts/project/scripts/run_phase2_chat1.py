#!/usr/bin/env python3
"""
Phase 2 Chat 1: Member Engagement & Outreach Effectiveness Tracking Runner
Executes the Phase 2 Chat 1 SQL script and validates results.

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


class Phase2Chat1Runner:
    """Runner for Phase 2 Chat 1 member engagement tracking."""
    
    def __init__(self, db_config: Dict[str, str]):
        """
        Initialize runner with database configuration.
        
        Args:
            db_config: Dictionary with keys: host, database, user, password, port
        """
        self.db_config = db_config
        self.conn = None
        self.script_path = Path(__file__).parent / "phase2_chat1_member_engagement.sql"
    
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
        """Verify Phase 1 Chats 1-4 are complete."""
        print("\n[CHECK] Checking prerequisites (Phase 1 Chats 1-4)...")
        
        required_tables = [
            'hedis_measures',
            'ma_plans',
            'plan_performance',
            'plan_members',
            'member_gaps'
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
            print("  Please run Phase 1 Chats 1-4 first!")
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
        print("[INFO] This will take 3-4 minutes to complete...")
        print("   Generating engagement scores for 10K members...")
        print("   Creating outreach campaigns and contact records...")
        
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
            "engagement_scores": """
                SELECT COUNT(*) as count FROM member_engagement_scores;
            """,
            "contact_preferences": """
                SELECT COUNT(*) as count FROM member_contact_preferences;
            """,
            "outreach_campaigns": """
                SELECT COUNT(*) as count FROM outreach_campaigns;
            """,
            "outreach_contacts": """
                SELECT COUNT(*) as count FROM member_outreach_contacts;
            """,
            "engagement_summary_view": """
                SELECT COUNT(*) as count FROM vw_member_engagement_summary;
            """,
            "campaign_performance_view": """
                SELECT COUNT(*) as count FROM vw_campaign_performance;
            """,
            "contact_method_view": """
                SELECT COUNT(*) as count FROM vw_contact_method_effectiveness;
            """,
            "barrier_analysis_view": """
                SELECT COUNT(*) as count FROM vw_barrier_analysis;
            """
        }
        
        expected = {
            "engagement_scores": 10000,  # One per member
            "contact_preferences": 8000,  # 80% of members
            "outreach_campaigns": 12,  # One per measure
            "outreach_contacts": None,  # Variable, just check > 0
            "engagement_summary_view": 10000,
            "campaign_performance_view": 12,
            "contact_method_view": None,  # Variable
            "barrier_analysis_view": None  # Variable
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
                        passed = count == expected_count
                        status = "[OK]" if passed else "[ERROR]"
                        print(f"  {status} {check_name}: {count}/{expected_count}")
                        
                        if not passed:
                            print(f"    WARNING: Expected {expected_count}, got {count}")
                    
                    results[check_name] = passed
                except psycopg2.Error as e:
                    results[check_name] = False
                    print(f"  [ERROR] {check_name}: Query failed - {e}")
        
        return results
    
    def show_engagement_summary(self):
        """Display engagement score distribution."""
        print("\n[REPORT] Engagement Score Distribution:")
        print("-" * 80)
        
        query = """
            SELECT 
                engagement_tier,
                COUNT(*) AS member_count,
                ROUND(COUNT(*)::DECIMAL / 10000 * 100, 1) AS pct_of_total,
                ROUND(AVG(overall_engagement_score), 1) AS avg_score,
                ROUND(MIN(overall_engagement_score), 1) AS min_score,
                ROUND(MAX(overall_engagement_score), 1) AS max_score
            FROM member_engagement_scores
            GROUP BY engagement_tier
            ORDER BY 
                CASE engagement_tier
                    WHEN 'High' THEN 1
                    WHEN 'Medium' THEN 2
                    WHEN 'Low' THEN 3
                    ELSE 4
                END;
        """
        
        try:
            with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query)
                rows = cur.fetchall()
                
                if not rows:
                    print("  No engagement data found")
                    return
                
                # Print header
                print(f"{'Tier':<15} {'Members':<12} {'% of Total':<12} {'Avg Score':<12} {'Min':<8} {'Max':<8}")
                print("-" * 80)
                
                # Print rows
                for row in rows:
                    print(f"{row['engagement_tier']:<15} {row['member_count']:<12} "
                          f"{row['pct_of_total']:<12} {row['avg_score']:<12} "
                          f"{row['min_score']:<8} {row['max_score']:<8}")
                
        except psycopg2.Error as e:
            print(f"  Error retrieving engagement summary: {e}")
    
    def show_campaign_summary(self):
        """Display top campaign performance."""
        print("\n[REPORT] Top 5 Campaign Performance:")
        print("-" * 100)
        
        query = """
            SELECT 
                campaign_name,
                target_member_count,
                members_contacted,
                successful_contacts,
                gaps_closed,
                ROUND(contact_rate_pct, 1) AS contact_rate,
                ROUND(success_rate_pct, 1) AS success_rate,
                ROUND(closure_rate_pct, 1) AS closure_rate
            FROM vw_campaign_performance
            ORDER BY gaps_closed DESC
            LIMIT 5;
        """
        
        try:
            with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query)
                rows = cur.fetchall()
                
                if not rows:
                    print("  No campaign data found")
                    return
                
                # Print header
                print(f"{'Campaign':<40} {'Target':<8} {'Contacted':<10} {'Success':<8} {'Closed':<8} {'Rates':<20}")
                print("-" * 100)
                
                # Print rows
                for row in rows:
                    campaign_short = row['campaign_name'][:38]
                    rates = f"{row['contact_rate']}%/{row['success_rate']}%/{row['closure_rate']}%"
                    print(f"{campaign_short:<40} {row['target_member_count']:<8} "
                          f"{row['members_contacted']:<10} {row['successful_contacts']:<8} "
                          f"{row['gaps_closed']:<8} {rates:<20}")
                
        except psycopg2.Error as e:
            print(f"  Error retrieving campaign summary: {e}")
    
    def show_contact_methods(self):
        """Display contact method effectiveness."""
        print("\n[REPORT] Contact Method Effectiveness:")
        print("-" * 80)
        
        query = """
            SELECT 
                contact_method,
                total_attempts,
                successful_attempts,
                success_rate_pct,
                ROUND(avg_duration_minutes, 1) AS avg_duration,
                gaps_closed_within_30_days
            FROM vw_contact_method_effectiveness
            ORDER BY success_rate_pct DESC;
        """
        
        try:
            with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query)
                rows = cur.fetchall()
                
                if not rows:
                    print("  No contact method data found")
                    return
                
                # Print header
                print(f"{'Method':<15} {'Attempts':<10} {'Success':<10} {'Rate %':<10} {'Avg Min':<10} {'Closures':<10}")
                print("-" * 80)
                
                # Print rows
                for row in rows:
                    print(f"{row['contact_method']:<15} {row['total_attempts']:<10} "
                          f"{row['successful_attempts']:<10} {row['success_rate_pct']:<10} "
                          f"{row['avg_duration'] or 'N/A':<10} {row['gaps_closed_within_30_days']:<10}")
                
        except psycopg2.Error as e:
            print(f"  Error retrieving contact methods: {e}")
    
    def close(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()
            print("\n[OK] Database connection closed")
    
    def run(self):
        """Execute full setup and validation process."""
        print("=" * 80)
        print("HEDIS STAR RATING PORTFOLIO OPTIMIZER")
        print("Phase 2 Chat 1: Member Engagement & Outreach Effectiveness Tracking")
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
                print("\n[WARNING] Some validation checks failed. Review output above.")
            
            self.show_engagement_summary()
            self.show_campaign_summary()
            self.show_contact_methods()
            
            print("\n" + "=" * 80)
            print("Setup complete! Next step: Phase 2 Chat 2 - Provider Network Performance")
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
    
    runner = Phase2Chat1Runner(db_config)
    success = runner.run()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

