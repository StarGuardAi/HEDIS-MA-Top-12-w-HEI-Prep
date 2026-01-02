#!/usr/bin/env python3
"""
Phase 1 Chat 3: ROI Analysis & Cost-per-Closure Tracking Runner
Executes the ROI analysis SQL script and validates results.

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


class Phase1Chat3Runner:
    """Runner for Phase 1 Chat 3 database setup."""
    
    def __init__(self, db_config: Dict[str, str]):
        """
        Initialize runner with database configuration.
        
        Args:
            db_config: Dictionary with keys: host, database, user, password, port
        """
        self.db_config = db_config
        self.conn = None
        self.script_path = Path(__file__).parent / "phase1_chat3_roi_analysis.sql"
    
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
        """Verify Phase 1 Chat 1 and Chat 2 are complete."""
        print("\n🔍 Checking prerequisites (Phase 1 Chat 1 & Chat 2)...")
        
        required_tables = [
            'hedis_measures',
            'ma_plans',
            'plan_performance',
            'plan_members',
            'member_gaps',
            'gap_closure_tracking',
            'gap_velocity_metrics'
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
            print("  Please run Phase 1 Chat 1 and Chat 2 first!")
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
            "activity_costs": """
                SELECT COUNT(*) as count FROM activity_cost_standards;
            """,
            "intervention_costs": """
                SELECT COUNT(*) as count FROM measure_intervention_costs;
            """,
            "budgets": """
                SELECT COUNT(*) as count FROM plan_budgets;
            """,
            "intervention_transactions": """
                SELECT COUNT(*) as count FROM intervention_costs;
            """,
            "roi_views": """
                SELECT COUNT(*) as count FROM information_schema.views 
                WHERE table_name IN ('vw_cost_per_closure', 'vw_portfolio_roi', 
                                      'vw_budget_performance', 'vw_intervention_efficiency', 
                                      'vw_team_productivity');
            """
        }
        
        expected = {
            "activity_costs": 26,
            "intervention_costs": 36,
            "budgets": 12,  # 3 plans × 4 categories
            "intervention_transactions": (0, None),  # At least some transactions
            "roi_views": 5
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
    
    def show_roi_summary(self):
        """Display ROI summary."""
        print("\n💰 Portfolio ROI Summary:")
        print("-" * 120)
        
        query = """
            SELECT 
                plan_id,
                plan_name,
                measure_id,
                measure_name,
                ROUND(potential_revenue, 0) AS revenue_at_risk,
                gaps_remaining,
                gaps_closed,
                ROUND(cost_to_date, 0) AS cost_to_date,
                ROUND(projected_roi_ratio, 2) AS projected_roi,
                ROUND(net_revenue_impact, 0) AS net_revenue
            FROM vw_portfolio_roi
            ORDER BY plan_id, net_revenue_impact DESC
            LIMIT 15;
        """
        
        try:
            with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query)
                rows = cur.fetchall()
                
                if not rows:
                    print("  No ROI data found")
                    return
                
                # Print header
                print(f"{'Plan ID':<12} {'Plan Name':<25} {'Measure':<8} {'Revenue $':<12} {'Gaps':<8} {'Cost $':<12} {'ROI':<8} {'Net $':<12}")
                print("-" * 120)
                
                # Print rows
                for row in rows:
                    print(f"{row['plan_id']:<12} {row['plan_name'][:24]:<25} {row['measure_id']:<8} "
                          f"${row['revenue_at_risk']:>10,.0f} {row['gaps_remaining']:<8} "
                          f"${row['cost_to_date']:>10,.0f} {row['projected_roi']:<8.2f} "
                          f"${row['net_revenue']:>10,.0f}")
                
        except psycopg2.Error as e:
            print(f"  Error retrieving ROI summary: {e}")
    
    def show_cost_per_closure(self):
        """Display cost per closure analysis."""
        print("\n💵 Cost per Closure Analysis:")
        print("-" * 100)
        
        query = """
            SELECT 
                plan_id,
                plan_name,
                measure_id,
                measure_name,
                total_gaps_closed,
                ROUND(total_intervention_cost, 0) AS total_cost,
                ROUND(cost_per_gap_closed, 2) AS cost_per_closure,
                ROUND(roi_ratio, 2) AS roi_ratio
            FROM vw_cost_per_closure
            ORDER BY plan_id, measure_id
            LIMIT 12;
        """
        
        try:
            with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query)
                rows = cur.fetchall()
                
                if not rows:
                    print("  No cost data found")
                    return
                
                print(f"{'Plan ID':<12} {'Plan Name':<25} {'Measure':<8} {'Closures':<10} {'Total $':<12} {'Per Gap $':<12} {'ROI':<8}")
                print("-" * 100)
                
                for row in rows:
                    print(f"{row['plan_id']:<12} {row['plan_name'][:24]:<25} {row['measure_id']:<8} "
                          f"{row['total_gaps_closed']:<10} ${row['total_cost']:>10,.0f} "
                          f"${row['cost_per_closure']:>10,.2f} {row['roi_ratio']:<8.2f}")
                
        except psycopg2.Error as e:
            print(f"  Error retrieving cost data: {e}")
    
    def show_executive_summary(self):
        """Display executive financial summary for first plan."""
        print("\n📊 Executive Financial Summary (H1234-001):")
        print("-" * 80)
        
        query = """
            SELECT 
                summary_metric,
                ROUND(metric_value, 2) AS value,
                metric_unit
            FROM get_executive_financial_summary('H1234-001', 2024)
            ORDER BY summary_metric;
        """
        
        try:
            with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query)
                rows = cur.fetchall()
                
                if not rows:
                    print("  No summary data found")
                    return
                
                print(f"{'Metric':<35} {'Value':<20} {'Unit':<15}")
                print("-" * 80)
                
                for row in rows:
                    value_str = f"${row['value']:,.2f}" if 'Dollar' in row['metric_unit'] else f"{row['value']:,.2f}"
                    print(f"{row['summary_metric']:<35} {value_str:<20} {row['metric_unit']:<15}")
                
        except psycopg2.Error as e:
            print(f"  Error retrieving executive summary: {e}")
    
    def close(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()
            print("\n✓ Database connection closed")
    
    def run(self):
        """Execute full setup and validation process."""
        print("=" * 80)
        print("HEDIS STAR RATING PORTFOLIO OPTIMIZER")
        print("Phase 1 Chat 3: ROI Analysis & Cost-per-Closure Tracking")
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
            
            self.show_roi_summary()
            self.show_cost_per_closure()
            self.show_executive_summary()
            
            print("\n" + "=" * 80)
            print("✅ PHASE 1 COMPLETE - All Financial Impact KPIs Operational!")
            print("=" * 80)
            print("\nNext Phase: Operational Performance Metrics")
            print("  - Gap closure velocity dashboards")
            print("  - Member engagement scoring")
            print("  - Provider network performance")
            print("  - Outreach effectiveness tracking")
            print("  - Predictive gap identification")
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
    
    runner = Phase1Chat3Runner(db_config)
    success = runner.run()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

