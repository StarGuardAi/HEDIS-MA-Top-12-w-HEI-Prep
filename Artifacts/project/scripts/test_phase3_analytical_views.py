#!/usr/bin/env python3
"""
Test Phase 3 Analytical Views
Test all analytical views with formatted output for demos
"""

import sys
import os

try:
    import psycopg2
    from psycopg2.extras import RealDictCursor
except ImportError:
    print("ERROR: psycopg2 not installed. Install with: pip install psycopg2-binary")
    sys.exit(1)


def get_db_config():
    """Get database configuration from environment or defaults."""
    return {
        "host": os.getenv("DB_HOST", "localhost"),
        "database": os.getenv("DB_NAME", "hedis_portfolio"),
        "user": os.getenv("DB_USER", "hedis_api"),
        "password": os.getenv("DB_PASSWORD", "hedis_password"),
        "port": os.getenv("DB_PORT", "5432")
    }


def check_view_exists(conn, view_name):
    """Check if a view exists."""
    cur = conn.cursor()
    cur.execute("""
        SELECT EXISTS (
            SELECT FROM information_schema.views
            WHERE table_schema = 'public'
            AND table_name = %s
        );
    """, (view_name,))
    return cur.fetchone()[0]


def test_roi_summary_dashboard(conn):
    """Test v_roi_summary_dashboard view."""
    print("=" * 100)
    print("VIEW 1: v_roi_summary_dashboard")
    print("=" * 100)
    print("All 12 Measures Sorted by ROI Ratio (Descending)\n")
    
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    if check_view_exists(conn, 'v_roi_summary_dashboard'):
        try:
            cur.execute("""
                SELECT * FROM v_roi_summary_dashboard
                ORDER BY roi_ratio DESC NULLS LAST;
            """)
            results = cur.fetchall()
        except Exception as e:
            print(f"[ERROR] View query failed: {e}")
            return None
    else:
        print("[WARN] View v_roi_summary_dashboard does not exist.")
        print("Calculating from data...\n")
        
        # Manual calculation
        cur.execute("""
            SELECT 
                mi.measure_id,
                hm.measure_name,
                COUNT(*) FILTER (WHERE mi.status = 'completed') as successful_closures,
                SUM(mi.cost_per_intervention) FILTER (WHERE mi.status = 'completed') as total_investment,
                COUNT(*) FILTER (WHERE mi.status = 'completed') * 100.0 as estimated_revenue_impact,
                CASE 
                    WHEN SUM(mi.cost_per_intervention) FILTER (WHERE mi.status = 'completed') > 0 
                    THEN (COUNT(*) FILTER (WHERE mi.status = 'completed') * 100.0) / 
                         SUM(mi.cost_per_intervention) FILTER (WHERE mi.status = 'completed')
                    ELSE 0
                END as roi_ratio
            FROM member_interventions mi
            LEFT JOIN hedis_measures hm ON mi.measure_id = hm.measure_id
            WHERE mi.intervention_date >= '2024-10-01'
            AND mi.intervention_date <= '2024-12-31'
            GROUP BY mi.measure_id, hm.measure_name
            ORDER BY roi_ratio DESC;
        """)
        results = cur.fetchall()
    
    if results:
        print("=" * 100)
        print(f"{'Rank':<6} {'Measure':<10} {'Measure Name':<35} {'ROI Ratio':<12} {'Investment':<15} {'Revenue':<15} {'Closures':<12}")
        print("=" * 100)
        
        for i, row in enumerate(results, 1):
            measure_id = (row.get('measure_id') or 'N/A')[:8]
            measure_name = (row.get('measure_name') or row.get('measure_name') or 'N/A')[:33]
            roi_ratio = float(row.get('roi_ratio') or row.get('roi_ratio') or 0)
            investment = float(row.get('total_investment') or row.get('investment') or 0)
            revenue = float(row.get('estimated_revenue_impact') or row.get('revenue_impact') or row.get('revenue') or 0)
            closures = int(row.get('successful_closures') or row.get('closures') or 0)
            
            print(f"{i:<6} {measure_id:<10} {measure_name:<35} {roi_ratio:<11.2f}x ${investment:<14,.2f} ${revenue:<14,.2f} {closures:<12,}")
        
        print("=" * 100)
        return results
    else:
        print("[WARN] No data returned from view")
        return None


def test_budget_variance_analysis(conn):
    """Test v_budget_variance_analysis view."""
    print("\n" + "=" * 100)
    print("VIEW 2: v_budget_variance_analysis")
    print("=" * 100)
    print("Budget Variance Analysis for Q4 2024\n")
    
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    if check_view_exists(conn, 'v_budget_variance_analysis'):
        try:
            cur.execute("""
                SELECT * FROM v_budget_variance_analysis
                WHERE period_start >= '2024-10-01' AND period_end <= '2024-12-31'
                ORDER BY variance_pct DESC;
            """)
            results = cur.fetchall()
        except Exception as e:
            print(f"[ERROR] View query failed: {e}")
            return None
    else:
        print("[WARN] View v_budget_variance_analysis does not exist.")
        print("Calculating from data...\n")
        
        # Manual calculation
        cur.execute("""
            SELECT 
                ba.measure_id,
                hm.measure_name,
                ba.budget_amount,
                COALESCE(SUM(as_spend.amount_spent), 0) as actual_spent,
                ba.budget_amount - COALESCE(SUM(as_spend.amount_spent), 0) as variance_amount,
                CASE 
                    WHEN ba.budget_amount > 0 
                    THEN ((COALESCE(SUM(as_spend.amount_spent), 0) - ba.budget_amount) / ba.budget_amount * 100)
                    ELSE 0
                END as variance_pct,
                CASE 
                    WHEN COALESCE(SUM(as_spend.amount_spent), 0) > ba.budget_amount THEN 'Over Budget'
                    WHEN COALESCE(SUM(as_spend.amount_spent), 0) < ba.budget_amount THEN 'Under Budget'
                    ELSE 'On Budget'
                END as status
            FROM budget_allocations ba
            LEFT JOIN hedis_measures hm ON ba.measure_id = hm.measure_id
            LEFT JOIN actual_spending as_spend ON ba.measure_id = as_spend.measure_id
            WHERE ba.period_start >= '2024-10-01' 
            AND ba.period_end <= '2024-12-31'
            GROUP BY ba.measure_id, hm.measure_name, ba.budget_amount
            ORDER BY variance_pct DESC;
        """)
        results = cur.fetchall()
    
    if results:
        print("=" * 100)
        print(f"{'Measure':<10} {'Measure Name':<35} {'Budget':<15} {'Actual':<15} {'Variance':<15} {'Variance %':<12} {'Status':<15}")
        print("=" * 100)
        
        for row in results:
            measure_id = (row.get('measure_id') or 'N/A')[:8]
            measure_name = (row.get('measure_name') or 'N/A')[:33]
            budget = float(row.get('budget_amount') or row.get('budget') or 0)
            actual = float(row.get('actual_spent') or row.get('actual') or 0)
            variance = float(row.get('variance_amount') or row.get('variance') or 0)
            variance_pct = float(row.get('variance_pct') or 0)
            status = row.get('status') or 'N/A'
            
            variance_str = f"${variance:,.2f}" if variance != 0 else "$0.00"
            variance_pct_str = f"{variance_pct:+.1f}%" if variance_pct != 0 else "0.0%"
            
            print(f"{measure_id:<10} {measure_name:<35} ${budget:<14,.2f} ${actual:<14,.2f} {variance_str:<15} {variance_pct_str:<12} {status:<15}")
        
        print("=" * 100)
        return results
    else:
        print("[WARN] No data returned from view")
        return None


def test_top_cost_effective_interventions(conn, top_n=10):
    """Test v_top_cost_effective_interventions view."""
    print("\n" + "=" * 100)
    print(f"VIEW 3: v_top_cost_effective_interventions")
    print("=" * 100)
    print(f"Top {top_n} Most Efficient Intervention Types\n")
    
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    if check_view_exists(conn, 'v_top_cost_effective_interventions'):
        try:
            cur.execute(f"""
                SELECT * FROM v_top_cost_effective_interventions
                LIMIT {top_n};
            """)
            results = cur.fetchall()
        except Exception as e:
            print(f"[ERROR] View query failed: {e}")
            return None
    else:
        print("[WARN] View v_top_cost_effective_interventions does not exist.")
        print("Calculating from data...\n")
        
        # Manual calculation
        cur.execute(f"""
            SELECT 
                ia.activity_name,
                ia.activity_type,
                COUNT(*) FILTER (WHERE mi.status = 'completed') as successful_closures,
                COUNT(*) as total_interventions,
                AVG(mi.cost_per_intervention) FILTER (WHERE mi.status = 'completed') as avg_cost,
                CASE 
                    WHEN COUNT(*) FILTER (WHERE mi.status = 'completed') > 0 
                    THEN COUNT(*) FILTER (WHERE mi.status = 'completed')::DECIMAL / COUNT(*) * 100
                    ELSE 0
                END as success_rate,
                CASE 
                    WHEN COUNT(*) FILTER (WHERE mi.status = 'completed') > 0 
                    THEN AVG(mi.cost_per_intervention) FILTER (WHERE mi.status = 'completed')
                    ELSE NULL
                END as cost_per_closure
            FROM member_interventions mi
            JOIN intervention_activities ia ON mi.activity_id = ia.activity_id
            WHERE mi.intervention_date >= '2024-10-01'
            AND mi.intervention_date <= '2024-12-31'
            GROUP BY ia.activity_id, ia.activity_name, ia.activity_type
            HAVING COUNT(*) FILTER (WHERE mi.status = 'completed') > 0
            ORDER BY success_rate DESC, cost_per_closure ASC
            LIMIT {top_n};
        """)
        results = cur.fetchall()
    
    if results:
        print("=" * 100)
        print(f"{'Rank':<6} {'Activity Name':<40} {'Type':<20} {'Closures':<12} {'Total':<12} {'Success %':<12} {'Avg Cost':<12}")
        print("=" * 100)
        
        for i, row in enumerate(results, 1):
            activity_name = (row.get('activity_name') or 'N/A')[:38]
            activity_type = (row.get('activity_type') or 'N/A')[:18]
            closures = int(row.get('successful_closures') or row.get('closures') or 0)
            total = int(row.get('total_interventions') or row.get('total') or 0)
            success_rate = float(row.get('success_rate') or 0)
            avg_cost = float(row.get('avg_cost') or row.get('cost_per_closure') or 0)
            
            print(f"{i:<6} {activity_name:<40} {activity_type:<20} {closures:<12,} {total:<12,} {success_rate:<11.1f}% ${avg_cost:<11,.2f}")
        
        print("=" * 100)
        return results
    else:
        print("[WARN] No data returned from view")
        return None


def test_cost_per_closure_by_activity(conn, measure_id='BPD'):
    """Test v_cost_per_closure_by_activity view for specific measure."""
    print("\n" + "=" * 100)
    print(f"VIEW 4: v_cost_per_closure_by_activity")
    print("=" * 100)
    print(f"Cost per Closure by Activity Type for {measure_id} Measure\n")
    
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    if check_view_exists(conn, 'v_cost_per_closure_by_activity'):
        try:
            cur.execute("""
                SELECT * FROM v_cost_per_closure_by_activity
                WHERE measure_id = %s
                ORDER BY cost_per_closure ASC;
            """, (measure_id,))
            results = cur.fetchall()
        except Exception as e:
            print(f"[ERROR] View query failed: {e}")
            return None
    else:
        print("[WARN] View v_cost_per_closure_by_activity does not exist.")
        print("Calculating from data...\n")
        
        # Manual calculation
        cur.execute("""
            SELECT 
                ia.activity_name,
                ia.activity_type,
                COUNT(*) FILTER (WHERE mi.status = 'completed') as successful_closures,
                COUNT(*) as total_interventions,
                AVG(mi.cost_per_intervention) FILTER (WHERE mi.status = 'completed') as cost_per_closure,
                SUM(mi.cost_per_intervention) FILTER (WHERE mi.status = 'completed') as total_cost,
                CASE 
                    WHEN COUNT(*) > 0 
                    THEN COUNT(*) FILTER (WHERE mi.status = 'completed')::DECIMAL / COUNT(*) * 100
                    ELSE 0
                END as success_rate
            FROM member_interventions mi
            JOIN intervention_activities ia ON mi.activity_id = ia.activity_id
            WHERE mi.measure_id = %s
            AND mi.intervention_date >= '2024-10-01'
            AND mi.intervention_date <= '2024-12-31'
            GROUP BY ia.activity_id, ia.activity_name, ia.activity_type
            HAVING COUNT(*) FILTER (WHERE mi.status = 'completed') > 0
            ORDER BY cost_per_closure ASC;
        """, (measure_id,))
        results = cur.fetchall()
    
    if results:
        print("=" * 100)
        print(f"{'Activity Name':<45} {'Type':<20} {'Closures':<12} {'Total':<12} {'Cost/Closure':<15} {'Total Cost':<15} {'Success %':<12}")
        print("=" * 100)
        
        for row in results:
            activity_name = (row.get('activity_name') or 'N/A')[:43]
            activity_type = (row.get('activity_type') or 'N/A')[:18]
            closures = int(row.get('successful_closures') or row.get('closures') or 0)
            total = int(row.get('total_interventions') or row.get('total') or 0)
            cost_per_closure = float(row.get('cost_per_closure') or 0)
            total_cost = float(row.get('total_cost') or 0)
            success_rate = float(row.get('success_rate') or 0)
            
            print(f"{activity_name:<45} {activity_type:<20} {closures:<12,} {total:<12,} ${cost_per_closure:<14,.2f} ${total_cost:<14,.2f} {success_rate:<11.1f}%")
        
        print("=" * 100)
        return results
    else:
        print("[WARN] No data returned from view")
        return None


def test_cost_tier_effectiveness(conn):
    """Test v_cost_tier_effectiveness view."""
    print("\n" + "=" * 100)
    print("VIEW 5: v_cost_tier_effectiveness")
    print("=" * 100)
    print("Low-Touch vs Medium-Touch vs High-Touch Intervention Comparison\n")
    
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    if check_view_exists(conn, 'v_cost_tier_effectiveness'):
        try:
            cur.execute("""
                SELECT * FROM v_cost_tier_effectiveness
                ORDER BY avg_cost ASC;
            """)
            results = cur.fetchall()
        except Exception as e:
            print(f"[ERROR] View query failed: {e}")
            return None
    else:
        print("[WARN] View v_cost_tier_effectiveness does not exist.")
        print("Calculating from data...\n")
        
        # Manual calculation - categorize by cost using subquery
        cur.execute("""
            WITH intervention_stats AS (
                SELECT 
                    mi.activity_id,
                    AVG(mi.cost_per_intervention) FILTER (WHERE mi.status = 'completed') as avg_cost
                FROM member_interventions mi
                WHERE mi.intervention_date >= '2024-10-01'
                AND mi.intervention_date <= '2024-12-31'
                GROUP BY mi.activity_id
            ),
            tiered_interventions AS (
                SELECT 
                    mi.*,
                    CASE 
                        WHEN is_stats.avg_cost < 30 THEN 'Low-Touch'
                        WHEN is_stats.avg_cost < 100 THEN 'Medium-Touch'
                        ELSE 'High-Touch'
                    END as cost_tier
                FROM member_interventions mi
                JOIN intervention_stats is_stats ON mi.activity_id = is_stats.activity_id
                WHERE mi.intervention_date >= '2024-10-01'
                AND mi.intervention_date <= '2024-12-31'
            )
            SELECT 
                cost_tier,
                COUNT(*) FILTER (WHERE status = 'completed') as successful_closures,
                COUNT(*) as total_interventions,
                AVG(cost_per_intervention) FILTER (WHERE status = 'completed') as avg_cost,
                SUM(cost_per_intervention) FILTER (WHERE status = 'completed') as total_cost,
                CASE 
                    WHEN COUNT(*) > 0 
                    THEN COUNT(*) FILTER (WHERE status = 'completed')::DECIMAL / COUNT(*) * 100
                    ELSE 0
                END as success_rate,
                CASE 
                    WHEN COUNT(*) FILTER (WHERE status = 'completed') > 0 
                    THEN SUM(cost_per_intervention) FILTER (WHERE status = 'completed') / 
                         COUNT(*) FILTER (WHERE status = 'completed')
                    ELSE NULL
                END as cost_per_closure
            FROM tiered_interventions
            GROUP BY cost_tier
            ORDER BY avg_cost ASC;
        """)
        results = cur.fetchall()
    
    if results:
        print("=" * 100)
        print(f"{'Cost Tier':<15} {'Closures':<12} {'Total':<12} {'Avg Cost':<15} {'Total Cost':<15} {'Success %':<12} {'Cost/Closure':<15}")
        print("=" * 100)
        
        for row in results:
            tier = (row.get('cost_tier') or row.get('tier') or 'N/A')[:13]
            closures = int(row.get('successful_closures') or row.get('closures') or 0)
            total = int(row.get('total_interventions') or row.get('total') or 0)
            avg_cost = float(row.get('avg_cost') or 0)
            total_cost = float(row.get('total_cost') or 0)
            success_rate = float(row.get('success_rate') or 0)
            cost_per_closure = float(row.get('cost_per_closure') or 0)
            
            print(f"{tier:<15} {closures:<12,} {total:<12,} ${avg_cost:<14,.2f} ${total_cost:<14,.2f} {success_rate:<11.1f}% ${cost_per_closure:<14,.2f}")
        
        print("=" * 100)
        
        # Summary comparison
        if len(results) >= 2:
            print("\nTier Comparison Summary:")
            low_touch = next((r for r in results if 'Low' in str(r.get('cost_tier', ''))), None)
            medium_touch = next((r for r in results if 'Medium' in str(r.get('cost_tier', ''))), None)
            high_touch = next((r for r in results if 'High' in str(r.get('cost_tier', ''))), None)
            
            if low_touch and high_touch:
                low_cost = float(low_touch.get('cost_per_closure') or 0)
                high_cost = float(high_touch.get('cost_per_closure') or 0)
                low_success = float(low_touch.get('success_rate') or 0)
                high_success = float(high_touch.get('success_rate') or 0)
                
                print(f"  Low-Touch: ${low_cost:,.2f} per closure, {low_success:.1f}% success rate")
                print(f"  High-Touch: ${high_cost:,.2f} per closure, {high_success:.1f}% success rate")
                if high_cost > 0:
                    print(f"  Cost Difference: {((high_cost - low_cost) / low_cost * 100):.1f}% higher for high-touch")
                if low_success > 0:
                    print(f"  Success Rate Difference: {((high_success - low_success) / low_success * 100):.1f}% higher for high-touch")
        
        return results
    else:
        print("[WARN] No data returned from view")
        return None


def main():
    """Main execution function."""
    db_config = get_db_config()
    
    print("=" * 100)
    print("PHASE 3 ANALYTICAL VIEWS TEST")
    print("=" * 100)
    print(f"\nConnecting to database: {db_config['database']}")
    
    try:
        conn = psycopg2.connect(**db_config)
        print("[OK] Connected successfully!\n")
        
        # Test all views
        test_roi_summary_dashboard(conn)
        test_budget_variance_analysis(conn)
        test_top_cost_effective_interventions(conn, 10)
        test_cost_per_closure_by_activity(conn, 'BPD')
        test_cost_tier_effectiveness(conn)
        
        print("\n" + "=" * 100)
        print("[SUCCESS] All analytical view tests completed!")
        print("=" * 100)
        
        conn.close()
        return True
        
    except psycopg2.OperationalError as e:
        print(f"[ERROR] Connection failed: {e}")
        return False
    except Exception as e:
        print(f"[ERROR] {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

