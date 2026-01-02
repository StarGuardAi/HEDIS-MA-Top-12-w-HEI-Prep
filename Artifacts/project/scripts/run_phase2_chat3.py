#!/usr/bin/env python3
"""
Phase 2 Chat 3: Predictive Analytics & Risk Scoring Engine Runner
Executes the Phase 2 Chat 3 SQL script and validates results.

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


class Phase2Chat3Runner:
    """Runner for Phase 2 Chat 3 predictive analytics."""
    
    def __init__(self, db_config: Dict[str, str]):
        """
        Initialize runner with database configuration.
        
        Args:
            db_config: Dictionary with keys: host, database, user, password, port
        """
        self.db_config = db_config
        self.conn = None
        self.script_path = Path(__file__).parent / "phase2_chat3_predictive_analytics.sql"
    
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
        """Verify Phase 1 and Phase 2 Chats 1-2 are complete."""
        print("\n[CHECK] Checking prerequisites (Phase 1 Chats 1-4, Phase 2 Chats 1-2)...")
        
        required_tables = [
            'hedis_measures',
            'ma_plans',
            'plan_performance',
            'plan_members',
            'member_gaps',
            'member_engagement_scores',
            'member_provider_attribution',
            'provider_performance',
            'member_outreach_contacts'
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
            print("  Please run Phase 1 Chats 1-4 and Phase 2 Chats 1-2 first!")
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
        print("   Calculating gap closure propensity scores...")
        print("   Generating member risk stratification...")
        print("   Creating cost predictions...")
        print("   Building intervention priority queue...")
        
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
            "gap_closure_propensity": """
                SELECT COUNT(*) as count FROM gap_closure_propensity;
            """,
            "member_risk_stratification": """
                SELECT COUNT(*) as count FROM member_risk_stratification;
            """,
            "member_cost_predictions": """
                SELECT COUNT(*) as count FROM member_cost_predictions;
            """,
            "early_warning_alerts": """
                SELECT COUNT(*) as count FROM early_warning_alerts;
            """,
            "intervention_priority_queue": """
                SELECT COUNT(*) as count FROM intervention_priority_queue;
            """,
            "high_value_targets_view": """
                SELECT COUNT(*) as count FROM vw_high_value_targets;
            """,
            "risk_dashboard_view": """
                SELECT COUNT(*) as count FROM vw_risk_dashboard;
            """,
            "alert_dashboard_view": """
                SELECT COUNT(*) as count FROM vw_alert_dashboard;
            """
        }
        
        expected = {
            "gap_closure_propensity": None,  # Variable based on open gaps
            "member_risk_stratification": 10000,  # One per member
            "member_cost_predictions": 10000,  # One per member
            "early_warning_alerts": None,  # Variable
            "intervention_priority_queue": None,  # Variable based on open gaps
            "high_value_targets_view": None,  # Variable
            "risk_dashboard_view": None,  # Variable by plan/tier
            "alert_dashboard_view": None  # Variable
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
                        print(f"  {status} {check_name}: {count:,} (expected > 0)")
                    else:
                        # Allow some variance for random generation
                        variance = abs(count - expected_count) / expected_count if expected_count > 0 else 0
                        passed = variance < 0.15  # Allow 15% variance
                        status = "[OK]" if passed else "[WARNING]"
                        print(f"  {status} {check_name}: {count:,}/{expected_count:,}")
                        
                        if not passed:
                            print(f"    NOTE: Expected ~{expected_count:,}, got {count:,} (variance: {variance*100:.1f}%)")
                    
                    results[check_name] = passed
                except psycopg2.Error as e:
                    results[check_name] = False
                    print(f"  [ERROR] {check_name}: Query failed - {e}")
        
        return results
    
    def show_propensity_summary(self):
        """Display gap closure propensity distribution."""
        print("\n[REPORT] Gap Closure Propensity Distribution:")
        print("-" * 80)
        
        query = """
            SELECT 
                closure_likelihood,
                COUNT(*) AS gap_count,
                ROUND(AVG(closure_propensity_score), 1) AS avg_score,
                ROUND(AVG(predicted_days_to_close), 1) AS avg_days,
                ROUND(AVG(predicted_cost_to_close), 2) AS avg_cost
            FROM gap_closure_propensity
            GROUP BY closure_likelihood
            ORDER BY 
                CASE closure_likelihood
                    WHEN 'Very High' THEN 1
                    WHEN 'High' THEN 2
                    WHEN 'Medium' THEN 3
                    WHEN 'Low' THEN 4
                    ELSE 5
                END;
        """
        
        try:
            with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query)
                rows = cur.fetchall()
                
                if not rows:
                    print("  No propensity data found")
                    return
                
                # Print header
                print(f"{'Likelihood':<15} {'Gaps':<12} {'Avg Score':<12} {'Avg Days':<12} {'Avg Cost':<12}")
                print("-" * 80)
                
                # Print rows
                for row in rows:
                    print(f"{row['closure_likelihood']:<15} {row['gap_count']:<12} "
                          f"{row['avg_score']:<12} {row['avg_days']:<12} ${row['avg_cost']:<11}")
                
        except psycopg2.Error as e:
            print(f"  Error retrieving propensity summary: {e}")
    
    def show_risk_summary(self):
        """Display risk stratification summary."""
        print("\n[REPORT] Member Risk Stratification Summary:")
        print("-" * 100)
        
        query = """
            SELECT 
                risk_tier,
                COUNT(*) AS member_count,
                ROUND(COUNT(*)::DECIMAL / 10000 * 100, 1) AS pct_of_total,
                ROUND(AVG(overall_risk_score), 1) AS avg_risk_score,
                COUNT(CASE WHEN care_management_needed THEN 1 END) AS care_mgmt_needed,
                COUNT(CASE WHEN disengagement_risk THEN 1 END) AS disengagement_risk
            FROM member_risk_stratification
            GROUP BY risk_tier
            ORDER BY 
                CASE risk_tier
                    WHEN 'Critical' THEN 1
                    WHEN 'High' THEN 2
                    WHEN 'Medium' THEN 3
                    ELSE 4
                END;
        """
        
        try:
            with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query)
                rows = cur.fetchall()
                
                if not rows:
                    print("  No risk data found")
                    return
                
                # Print header
                print(f"{'Tier':<15} {'Members':<12} {'% Total':<12} {'Avg Risk':<12} {'Care Mgmt':<12} {'Disengage':<12}")
                print("-" * 100)
                
                # Print rows
                for row in rows:
                    print(f"{row['risk_tier']:<15} {row['member_count']:<12} "
                          f"{row['pct_of_total']:<12} {row['avg_risk_score']:<12} "
                          f"{row['care_mgmt_needed']:<12} {row['disengagement_risk']:<12}")
                
        except psycopg2.Error as e:
            print(f"  Error retrieving risk summary: {e}")
    
    def show_cost_summary(self):
        """Display cost predictions summary."""
        print("\n[REPORT] Cost Predictions by Risk Category:")
        print("-" * 100)
        
        query = """
            SELECT 
                cost_risk_category,
                COUNT(*) AS member_count,
                ROUND(AVG(predicted_total_cost), 0) AS avg_predicted_cost,
                ROUND(AVG(estimated_avoidable_cost), 0) AS avg_avoidable_cost,
                ROUND(AVG(intervention_roi), 2) AS avg_roi
            FROM member_cost_predictions
            GROUP BY cost_risk_category
            ORDER BY 
                CASE cost_risk_category
                    WHEN 'Very High' THEN 1
                    WHEN 'High' THEN 2
                    WHEN 'Medium' THEN 3
                    ELSE 4
                END;
        """
        
        try:
            with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query)
                rows = cur.fetchall()
                
                if not rows:
                    print("  No cost data found")
                    return
                
                # Print header
                print(f"{'Category':<15} {'Members':<12} {'Avg Cost':<15} {'Avoidable':<15} {'Avg ROI':<12}")
                print("-" * 100)
                
                # Print rows
                for row in rows:
                    print(f"{row['cost_risk_category']:<15} {row['member_count']:<12} "
                          f"${row['avg_predicted_cost']:<14} ${row['avg_avoidable_cost']:<14} "
                          f"{row['avg_roi']:<12}")
                
        except psycopg2.Error as e:
            print(f"  Error retrieving cost summary: {e}")
    
    def show_priority_queue_summary(self):
        """Display intervention priority queue summary."""
        print("\n[REPORT] Intervention Priority Queue Summary:")
        print("-" * 100)
        
        query = """
            SELECT 
                priority_tier,
                COUNT(*) AS intervention_count,
                ROUND(AVG(priority_score), 1) AS avg_priority_score,
                ROUND(AVG(estimated_cost), 2) AS avg_cost,
                ROUND(AVG(estimated_roi), 2) AS avg_roi,
                COUNT(CASE WHEN status = 'Queued' THEN 1 END) AS queued_count
            FROM intervention_priority_queue
            GROUP BY priority_tier
            ORDER BY 
                CASE priority_tier
                    WHEN 'Urgent' THEN 1
                    WHEN 'High' THEN 2
                    WHEN 'Medium' THEN 3
                    ELSE 4
                END;
        """
        
        try:
            with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query)
                rows = cur.fetchall()
                
                if not rows:
                    print("  No priority queue data found")
                    return
                
                # Print header
                print(f"{'Tier':<15} {'Count':<12} {'Avg Priority':<15} {'Avg Cost':<12} {'Avg ROI':<12} {'Queued':<12}")
                print("-" * 100)
                
                # Print rows
                for row in rows:
                    print(f"{row['priority_tier']:<15} {row['intervention_count']:<12} "
                          f"{row['avg_priority_score']:<15} ${row['avg_cost']:<11} "
                          f"{row['avg_roi']:<12} {row['queued_count']:<12}")
                
        except psycopg2.Error as e:
            print(f"  Error retrieving priority queue summary: {e}")
    
    def show_alerts_summary(self):
        """Display early warning alerts summary."""
        print("\n[REPORT] Early Warning Alerts Summary:")
        print("-" * 100)
        
        query = """
            SELECT 
                alert_type,
                alert_severity,
                COUNT(*) AS total_alerts,
                COUNT(CASE WHEN alert_status = 'Active' THEN 1 END) AS active_alerts,
                COUNT(DISTINCT member_id) AS unique_members
            FROM early_warning_alerts
            GROUP BY alert_type, alert_severity
            ORDER BY 
                CASE alert_severity
                    WHEN 'Critical' THEN 1
                    WHEN 'High' THEN 2
                    WHEN 'Medium' THEN 3
                    ELSE 4
                END,
                total_alerts DESC
            LIMIT 10;
        """
        
        try:
            with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query)
                rows = cur.fetchall()
                
                if not rows:
                    print("  No alert data found")
                    return
                
                # Print header
                print(f"{'Type':<25} {'Severity':<12} {'Total':<12} {'Active':<12} {'Members':<12}")
                print("-" * 100)
                
                # Print rows
                for row in rows:
                    print(f"{row['alert_type']:<25} {row['alert_severity']:<12} "
                          f"{row['total_alerts']:<12} {row['active_alerts']:<12} "
                          f"{row['unique_members']:<12}")
                
        except psycopg2.Error as e:
            print(f"  Error retrieving alerts summary: {e}")
    
    def close(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()
            print("\n[OK] Database connection closed")
    
    def run(self):
        """Execute full setup and validation process."""
        print("=" * 80)
        print("HEDIS STAR RATING PORTFOLIO OPTIMIZER")
        print("Phase 2 Chat 3: Predictive Analytics & Risk Scoring Engine")
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
            
            self.show_propensity_summary()
            self.show_risk_summary()
            self.show_cost_summary()
            self.show_priority_queue_summary()
            self.show_alerts_summary()
            
            print("\n" + "=" * 80)
            print("Setup complete! Next step: Phase 2 Chat 4 - Operational Dashboards & Executive KPIs")
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
    
    runner = Phase2Chat3Runner(db_config)
    success = runner.run()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

