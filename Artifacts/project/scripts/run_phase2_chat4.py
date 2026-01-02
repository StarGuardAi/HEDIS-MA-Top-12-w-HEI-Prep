#!/usr/bin/env python3
"""
Phase 2 Chat 4: Operational Dashboards & Executive KPIs Runner
Executes the Phase 2 Chat 4 SQL script and validates results.

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


class Phase2Chat4Runner:
    """Runner for Phase 2 Chat 4 operational dashboards."""
    
    def __init__(self, db_config: Dict[str, str]):
        """
        Initialize runner with database configuration.
        
        Args:
            db_config: Dictionary with keys: host, database, user, password, port
        """
        self.db_config = db_config
        self.conn = None
        self.script_path = Path(__file__).parent / "phase2_chat4_operational_dashboards.sql"
    
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
        """Verify Phase 1 and Phase 2 Chats 1-3 are complete."""
        print("\n[CHECK] Checking prerequisites (Phase 1 Chats 1-4, Phase 2 Chats 1-3)...")
        
        required_tables = [
            'hedis_measures',
            'ma_plans',
            'plan_performance',
            'plan_members',
            'member_gaps',
            'member_engagement_scores',
            'member_provider_attribution',
            'provider_performance',
            'gap_closure_propensity',
            'member_risk_stratification',
            'intervention_priority_queue'
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
            print("  Please run Phase 1 Chats 1-4 and Phase 2 Chats 1-3 first!")
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
        print("   Creating dashboard infrastructure...")
        print("   Generating 12 executive dashboard views...")
        print("   Populating KPI snapshots and team metrics...")
        
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
            "daily_kpi_snapshots": """
                SELECT COUNT(*) as count FROM daily_kpi_snapshots;
            """,
            "team_performance_metrics": """
                SELECT COUNT(*) as count FROM team_performance_metrics;
            """,
            "executive_summary_view": """
                SELECT COUNT(*) as count FROM vw_executive_summary;
            """,
            "plan_comparison_view": """
                SELECT COUNT(*) as count FROM vw_plan_comparison;
            """,
            "measure_performance_view": """
                SELECT COUNT(*) as count FROM vw_measure_performance_dashboard;
            """,
            "operations_dashboard_view": """
                SELECT COUNT(*) as count FROM vw_operations_dashboard;
            """,
            "team_scorecard_view": """
                SELECT COUNT(*) as count FROM vw_team_scorecard;
            """,
            "data_export_view": """
                SELECT COUNT(*) as count FROM vw_data_export_master;
            """
        }
        
        expected = {
            "daily_kpi_snapshots": 270,  # 90 days * 3 plans
            "team_performance_metrics": 300,  # 10 members * 30 days
            "executive_summary_view": 1,
            "plan_comparison_view": 3,  # 3 plans
            "measure_performance_view": 12,  # 12 measures
            "operations_dashboard_view": 1,
            "team_scorecard_view": 10,  # 10 team members
            "data_export_view": 10000  # 10K members
        }
        
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            for check_name, query in validations.items():
                try:
                    cur.execute(query)
                    result = cur.fetchone()
                    count = result['count']
                    expected_count = expected[check_name]
                    
                    # Allow some variance for random generation
                    variance = abs(count - expected_count) / expected_count if expected_count > 0 else 0
                    passed = variance < 0.20  # Allow 20% variance
                    status = "[OK]" if passed else "[WARNING]"
                    print(f"  {status} {check_name}: {count:,}/{expected_count:,}")
                    
                    if not passed:
                        print(f"    NOTE: Expected ~{expected_count:,}, got {count:,} (variance: {variance*100:.1f}%)")
                    
                    results[check_name] = passed
                except psycopg2.Error as e:
                    results[check_name] = False
                    print(f"  [ERROR] {check_name}: Query failed - {e}")
        
        return results
    
    def show_executive_summary(self):
        """Display executive summary."""
        print("\n[REPORT] Executive Summary Dashboard:")
        print("-" * 100)
        
        query = "SELECT * FROM vw_executive_summary;"
        
        try:
            with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query)
                row = cur.fetchone()
                
                if not row:
                    print("  No executive summary data found")
                    return
                
                print(f"Total Members: {row['total_members'] or 0:,}")
                print(f"Engagement Rate: {row['engagement_rate_pct'] or 0}%")
                print(f"High Risk Members: {row['high_risk_members'] or 0:,} ({row['high_risk_rate_pct'] or 0}%)")
                print(f"Total Gaps: {row['total_gaps'] or 0:,}")
                print(f"Open Gaps: {row['open_gaps'] or 0:,}")
                print(f"Gaps Closed YTD: {row['gaps_closed_ytd'] or 0:,} ({row['ytd_closure_rate_pct'] or 0}%)")
                print(f"Revenue at Risk: ${row['revenue_at_risk'] or 0:,.0f}")
                print(f"Intervention Cost YTD: ${row['intervention_cost_ytd'] or 0:,.0f}")
                print(f"Cost per Closure: ${row['cost_per_closure'] or 0:.2f}")
                print(f"Projected ROI: {row['projected_roi'] or 0:.2f}x")
                
        except psycopg2.Error as e:
            print(f"  Error retrieving executive summary: {e}")
    
    def show_plan_comparison(self):
        """Display plan comparison."""
        print("\n[REPORT] Plan Comparison:")
        print("-" * 100)
        
        query = """
            SELECT 
                plan_id,
                plan_name,
                active_members,
                ROUND(avg_engagement_score, 1) AS engagement,
                open_gaps,
                ROUND(closure_rate_pct, 1) AS closure_rate,
                ROUND(revenue_at_risk/1000, 0) AS revenue_at_risk_k
            FROM vw_plan_comparison
            ORDER BY plan_id;
        """
        
        try:
            with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query)
                rows = cur.fetchall()
                
                if not rows:
                    print("  No plan comparison data found")
                    return
                
                # Print header
                print(f"{'Plan':<15} {'Members':<12} {'Engage':<10} {'Open Gaps':<12} {'Closure %':<12} {'Rev Risk ($K)':<15}")
                print("-" * 100)
                
                # Print rows
                for row in rows:
                    engagement = row['engagement'] or 0
                    open_gaps = row['open_gaps'] or 0
                    closure_rate = row['closure_rate'] or 0
                    revenue_k = row['revenue_at_risk_k'] or 0
                    print(f"{row['plan_id']:<15} {row['active_members'] or 0:<12} {engagement:<10} "
                          f"{open_gaps:<12} {closure_rate:<12} {revenue_k:<15}")
                
        except psycopg2.Error as e:
            print(f"  Error retrieving plan comparison: {e}")
    
    def show_top_measures(self):
        """Display top measures by revenue impact."""
        print("\n[REPORT] Top 5 Measures by Revenue Impact:")
        print("-" * 100)
        
        query = """
            SELECT 
                measure_id,
                measure_name,
                ROUND(avg_performance_rate, 1) AS performance,
                total_open_gaps,
                ROUND(closure_rate_pct, 1) AS closure_rate,
                ROUND(revenue_at_risk/1000, 0) AS revenue_at_risk_k
            FROM vw_measure_performance_dashboard
            ORDER BY revenue_at_risk DESC
            LIMIT 5;
        """
        
        try:
            with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query)
                rows = cur.fetchall()
                
                if not rows:
                    print("  No measure data found")
                    return
                
                # Print header
                print(f"{'Measure':<15} {'Name':<40} {'Perf %':<10} {'Open Gaps':<12} {'Closure %':<12} {'Rev ($K)':<12}")
                print("-" * 100)
                
                # Print rows
                for row in rows:
                    name_short = (row['measure_name'] or '')[:38]
                    performance = row['performance'] or 0
                    open_gaps = row['total_open_gaps'] or 0
                    closure_rate = row['closure_rate'] or 0
                    revenue_k = row['revenue_at_risk_k'] or 0
                    print(f"{row['measure_id']:<15} {name_short:<40} {performance:<10} "
                          f"{open_gaps:<12} {closure_rate:<12} {revenue_k:<12}")
                
        except psycopg2.Error as e:
            print(f"  Error retrieving top measures: {e}")
    
    def show_team_performance(self):
        """Display top team members."""
        print("\n[REPORT] Top 5 Team Members by Productivity:")
        print("-" * 100)
        
        query = """
            SELECT 
                team_member,
                team_role,
                total_gaps_closed,
                ROUND(avg_gap_closure_rate, 1) AS closure_rate,
                ROUND(avg_productivity_score, 1) AS productivity,
                most_common_tier
            FROM vw_team_scorecard
            ORDER BY avg_productivity_score DESC
            LIMIT 5;
        """
        
        try:
            with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query)
                rows = cur.fetchall()
                
                if not rows:
                    print("  No team performance data found")
                    return
                
                # Print header
                print(f"{'Team Member':<25} {'Role':<20} {'Gaps Closed':<15} {'Closure %':<12} {'Productivity':<12} {'Tier':<15}")
                print("-" * 100)
                
                # Print rows
                for row in rows:
                    gaps_closed = row['total_gaps_closed'] or 0
                    closure_rate = row['closure_rate'] or 0
                    productivity = row['productivity'] or 0
                    tier = row['most_common_tier'] or 'N/A'
                    print(f"{row['team_member']:<25} {row['team_role']:<20} {gaps_closed:<15} "
                          f"{closure_rate:<12} {productivity:<12} {tier:<15}")
                
        except psycopg2.Error as e:
            print(f"  Error retrieving team performance: {e}")
    
    def close(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()
            print("\n[OK] Database connection closed")
    
    def run(self):
        """Execute full setup and validation process."""
        print("=" * 80)
        print("HEDIS STAR RATING PORTFOLIO OPTIMIZER")
        print("Phase 2 Chat 4: Operational Dashboards & Executive KPIs")
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
            
            self.show_executive_summary()
            self.show_plan_comparison()
            self.show_top_measures()
            self.show_team_performance()
            
            print("\n" + "=" * 80)
            print("PHASE 2 COMPLETE! All operational dashboards deployed.")
            print("=" * 80)
            print("\nTotal Phase 2 Deliverables:")
            print("  - Chat 1: Member Engagement & Outreach")
            print("  - Chat 2: Provider Network Performance")
            print("  - Chat 3: Predictive Analytics & Risk Scoring")
            print("  - Chat 4: Operational Dashboards & Executive KPIs")
            print("\nYou now have a complete, production-ready HEDIS analytics platform!")
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
    
    runner = Phase2Chat4Runner(db_config)
    success = runner.run()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

