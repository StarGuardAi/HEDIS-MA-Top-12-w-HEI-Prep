#!/usr/bin/env python3
"""
Phase 3 Executive Summary Generator
Generate comprehensive executive ROI report for Q4 2024
"""

import sys
import os
from datetime import datetime

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


def generate_executive_roi_report(conn, start_date='2024-10-01', end_date='2024-12-31'):
    """Generate full executive ROI report."""
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    print("=" * 100)
    print("EXECUTIVE ROI REPORT - Q4 2024")
    print("=" * 100)
    print(f"Period: {start_date} to {end_date}\n")
    
    # Check if function exists
    cur.execute("""
        SELECT EXISTS (
            SELECT FROM pg_proc p
            JOIN pg_namespace n ON p.pronamespace = n.oid
            WHERE n.nspname = 'public'
            AND p.proname = 'generate_roi_executive_report'
        );
    """)
    
    if cur.fetchone()['exists']:
        try:
            cur.execute("SELECT * FROM generate_roi_executive_report(%s, %s);", (start_date, end_date))
            results = cur.fetchall()
            if results:
                print("Report generated from function:\n")
                for row in results:
                    for key, value in row.items():
                        print(f"  {key}: {value}")
                return results
        except Exception as e:
            print(f"[WARN] Function call failed: {e}")
    
    # Generate report manually
    print("Generating comprehensive ROI report...\n")
    
    cur.execute("""
        SELECT 
            mi.measure_id,
            hm.measure_name,
            COUNT(*) FILTER (WHERE mi.status = 'completed') as successful_closures,
            COUNT(*) as total_interventions,
            SUM(mi.cost_per_intervention) FILTER (WHERE mi.status = 'completed') as total_investment,
            AVG(mi.cost_per_intervention) FILTER (WHERE mi.status = 'completed') as avg_cost_per_closure,
            CASE 
                WHEN COUNT(*) FILTER (WHERE mi.status = 'completed') > 0 
                THEN SUM(mi.cost_per_intervention) FILTER (WHERE mi.status = 'completed') / 
                     COUNT(*) FILTER (WHERE mi.status = 'completed')
                ELSE NULL
            END as cost_per_closure,
            COUNT(*) FILTER (WHERE mi.status = 'completed') * 100.0 as estimated_revenue_impact,
            CASE 
                WHEN SUM(mi.cost_per_intervention) FILTER (WHERE mi.status = 'completed') > 0 
                THEN (COUNT(*) FILTER (WHERE mi.status = 'completed') * 100.0) / 
                     SUM(mi.cost_per_intervention) FILTER (WHERE mi.status = 'completed')
                ELSE 0
            END as roi_ratio
        FROM member_interventions mi
        LEFT JOIN hedis_measures hm ON mi.measure_id = hm.measure_id
        WHERE mi.intervention_date >= %s
        AND mi.intervention_date <= %s
        GROUP BY mi.measure_id, hm.measure_name
        ORDER BY roi_ratio DESC;
    """, (start_date, end_date))
    
    results = cur.fetchall()
    
    if results:
        print("=" * 100)
        print(f"{'Measure':<10} {'Measure Name':<35} {'Closures':<12} {'Investment':<15} {'Cost/Closure':<15} {'Revenue':<15} {'ROI':<10}")
        print("=" * 100)
        
        total_closures = 0
        total_investment = 0
        total_revenue = 0
        
        for row in results:
            measure_id = (row['measure_id'] or 'N/A')[:8]
            measure_name = (row['measure_name'] or 'N/A')[:33]
            closures = int(row['successful_closures'] or 0)
            investment = float(row['total_investment'] or 0)
            cost_per_closure = float(row['cost_per_closure'] or 0)
            revenue = float(row['estimated_revenue_impact'] or 0)
            roi = float(row['roi_ratio'] or 0)
            
            total_closures += closures
            total_investment += investment
            total_revenue += revenue
            
            print(f"{measure_id:<10} {measure_name:<35} {closures:<12,} ${investment:<14,.2f} ${cost_per_closure:<14,.2f} ${revenue:<14,.2f} {roi:<9.2f}x")
        
        print("=" * 100)
        print(f"{'TOTAL':<10} {'':<35} {total_closures:<12,} ${total_investment:<14,.2f} {'':<15} ${total_revenue:<14,.2f}")
        print("=" * 100)
        
        overall_roi = (total_revenue / total_investment) if total_investment > 0 else 0
        net_benefit = total_revenue - total_investment
        
        print(f"\nPortfolio Summary:")
        print(f"  Total Successful Closures: {total_closures:,}")
        print(f"  Total Investment: ${total_investment:,.2f}")
        print(f"  Estimated Revenue Impact: ${total_revenue:,.2f}")
        print(f"  Net Benefit: ${net_benefit:,.2f}")
        print(f"  Overall ROI Ratio: {overall_roi:.2f}x")
        
        return {
            'total_closures': total_closures,
            'total_investment': total_investment,
            'total_revenue': total_revenue,
            'net_benefit': net_benefit,
            'overall_roi': overall_roi,
            'measures': results
        }
    
    return None


def show_most_expensive_measures(conn, top_n=3, start_date='2024-10-01', end_date='2024-12-31'):
    """Show most expensive measures by cost per closure."""
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    print("\n" + "=" * 100)
    print(f"MOST EXPENSIVE MEASURES (Top {top_n} by Cost per Closure)")
    print("=" * 100)
    print(f"Date Range: {start_date} to {end_date}\n")
    
    cur.execute("""
        SELECT 
            mi.measure_id,
            hm.measure_name,
            COUNT(*) FILTER (WHERE mi.status = 'completed') as successful_closures,
            SUM(mi.cost_per_intervention) FILTER (WHERE mi.status = 'completed') as total_investment,
            CASE 
                WHEN COUNT(*) FILTER (WHERE mi.status = 'completed') > 0 
                THEN SUM(mi.cost_per_intervention) FILTER (WHERE mi.status = 'completed') / 
                     COUNT(*) FILTER (WHERE mi.status = 'completed')
                ELSE NULL
            END as cost_per_closure
        FROM member_interventions mi
        LEFT JOIN hedis_measures hm ON mi.measure_id = hm.measure_id
        WHERE mi.intervention_date >= %s
        AND mi.intervention_date <= %s
        GROUP BY mi.measure_id, hm.measure_name
        HAVING COUNT(*) FILTER (WHERE mi.status = 'completed') > 0
        ORDER BY cost_per_closure DESC
        LIMIT %s;
    """, (start_date, end_date, top_n))
    
    results = cur.fetchall()
    
    if results:
        print("=" * 100)
        print(f"{'Rank':<6} {'Measure':<10} {'Measure Name':<35} {'Cost/Closure':<15} {'Total Investment':<18} {'Closures':<12}")
        print("=" * 100)
        
        for i, row in enumerate(results, 1):
            measure_id = (row['measure_id'] or 'N/A')[:8]
            measure_name = (row['measure_name'] or 'N/A')[:33]
            cost_per_closure = float(row['cost_per_closure'] or 0)
            investment = float(row['total_investment'] or 0)
            closures = int(row['successful_closures'] or 0)
            
            print(f"{i:<6} {measure_id:<10} {measure_name:<35} ${cost_per_closure:<14,.2f} ${investment:<17,.2f} {closures:<12,}")
        
        print("=" * 100)
        return results
    
    return None


def show_most_efficient_interventions(conn, top_n=3, start_date='2024-10-01', end_date='2024-12-31'):
    """Show most efficient intervention types."""
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    print("\n" + "=" * 100)
    print(f"MOST EFFICIENT INTERVENTION TYPES (Top {top_n} by Cost per Closure)")
    print("=" * 100)
    print(f"Date Range: {start_date} to {end_date}\n")
    
    cur.execute("""
        SELECT 
            ia.activity_name,
            ia.activity_type,
            COUNT(*) FILTER (WHERE mi.status = 'completed') as successful_closures,
            COUNT(*) as total_interventions,
            CASE 
                WHEN COUNT(*) FILTER (WHERE mi.status = 'completed') > 0 
                THEN AVG(mi.cost_per_intervention) FILTER (WHERE mi.status = 'completed')
                ELSE NULL
            END as cost_per_closure,
            CASE 
                WHEN COUNT(*) > 0 
                THEN COUNT(*) FILTER (WHERE mi.status = 'completed')::DECIMAL / COUNT(*) * 100
                ELSE 0
            END as success_rate
        FROM member_interventions mi
        JOIN intervention_activities ia ON mi.activity_id = ia.activity_id
        WHERE mi.intervention_date >= %s
        AND mi.intervention_date <= %s
        GROUP BY ia.activity_id, ia.activity_name, ia.activity_type
        HAVING COUNT(*) FILTER (WHERE mi.status = 'completed') > 0
        ORDER BY cost_per_closure ASC
        LIMIT %s;
    """, (start_date, end_date, top_n))
    
    results = cur.fetchall()
    
    if results:
        print("=" * 100)
        print(f"{'Rank':<6} {'Activity Name':<40} {'Type':<20} {'Cost/Closure':<15} {'Success %':<12} {'Closures':<12}")
        print("=" * 100)
        
        for i, row in enumerate(results, 1):
            activity_name = (row['activity_name'] or 'N/A')[:38]
            activity_type = (row['activity_type'] or 'N/A')[:18]
            cost_per_closure = float(row['cost_per_closure'] or 0)
            success_rate = float(row['success_rate'] or 0)
            closures = int(row['successful_closures'] or 0)
            
            print(f"{i:<6} {activity_name:<40} {activity_type:<20} ${cost_per_closure:<14,.2f} {success_rate:<11.1f}% {closures:<12,}")
        
        print("=" * 100)
        return results
    
    return None


def calculate_total_roi(conn, start_date='2024-10-01', end_date='2024-12-31'):
    """Calculate total ROI across all measures."""
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    print("\n" + "=" * 100)
    print("TOTAL ROI CALCULATION - ALL MEASURES")
    print("=" * 100)
    print(f"Date Range: {start_date} to {end_date}\n")
    
    cur.execute("""
        SELECT 
            COUNT(*) FILTER (WHERE status = 'completed') as total_closures,
            COUNT(*) as total_interventions,
            SUM(cost_per_intervention) FILTER (WHERE status = 'completed') as total_investment,
            COUNT(*) FILTER (WHERE status = 'completed') * 100.0 as estimated_revenue_impact
        FROM member_interventions
        WHERE intervention_date >= %s
        AND intervention_date <= %s;
    """, (start_date, end_date))
    
    result = cur.fetchone()
    
    if result:
        total_closures = int(result['total_closures'] or 0)
        total_interventions = int(result['total_interventions'] or 0)
        total_investment = float(result['total_investment'] or 0)
        total_revenue = float(result['estimated_revenue_impact'] or 0)
        
        roi_ratio = (total_revenue / total_investment) if total_investment > 0 else 0
        net_benefit = total_revenue - total_investment
        avg_cost_per_closure = (total_investment / total_closures) if total_closures > 0 else 0
        success_rate = (total_closures / total_interventions * 100) if total_interventions > 0 else 0
        
        print("=" * 100)
        print(f"{'Metric':<40} {'Value':<60}")
        print("=" * 100)
        print(f"{'Total Interventions':<40} {total_interventions:<60,}")
        print(f"{'Successful Closures':<40} {total_closures:<60,}")
        print(f"{'Success Rate':<40} {success_rate:<59.1f}%")
        print(f"{'Total Investment':<40} ${total_investment:<59,.2f}")
        print(f"{'Estimated Revenue Impact':<40} ${total_revenue:<59,.2f}")
        print(f"{'Net Benefit':<40} ${net_benefit:<59,.2f}")
        print(f"{'Average Cost per Closure':<40} ${avg_cost_per_closure:<59,.2f}")
        print(f"{'Overall ROI Ratio':<40} {roi_ratio:<59.2f}x")
        print("=" * 100)
        
        return {
            'total_interventions': total_interventions,
            'total_closures': total_closures,
            'total_investment': total_investment,
            'total_revenue': total_revenue,
            'net_benefit': net_benefit,
            'roi_ratio': roi_ratio,
            'avg_cost_per_closure': avg_cost_per_closure,
            'success_rate': success_rate
        }
    
    return None


def generate_one_page_summary(conn, start_date='2024-10-01', end_date='2024-12-31'):
    """Generate one-page executive summary."""
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    print("\n" + "=" * 100)
    print("=" * 100)
    print(" " * 30 + "EXECUTIVE SUMMARY - Q4 2024")
    print(" " * 25 + "HEDIS Portfolio Optimizer ROI Report")
    print("=" * 100)
    print("=" * 100)
    print()
    
    # Get total ROI metrics (without printing)
    cur.execute("""
        SELECT 
            COUNT(*) FILTER (WHERE status = 'completed') as total_closures,
            COUNT(*) as total_interventions,
            SUM(cost_per_intervention) FILTER (WHERE status = 'completed') as total_investment,
            COUNT(*) FILTER (WHERE status = 'completed') * 100.0 as estimated_revenue_impact
        FROM member_interventions
        WHERE intervention_date >= %s
        AND intervention_date <= %s;
    """, (start_date, end_date))
    
    result = cur.fetchone()
    
    if not result:
        print("[ERROR] Could not retrieve ROI data")
        return
    
    total_closures = int(result['total_closures'] or 0)
    total_interventions = int(result['total_interventions'] or 0)
    total_investment = float(result['total_investment'] or 0)
    total_revenue = float(result['estimated_revenue_impact'] or 0)
    
    roi_ratio = (total_revenue / total_investment) if total_investment > 0 else 0
    net_benefit = total_revenue - total_investment
    avg_cost_per_closure = (total_investment / total_closures) if total_closures > 0 else 0
    
    roi_data = {
        'total_interventions': total_interventions,
        'total_closures': total_closures,
        'total_investment': total_investment,
        'total_revenue': total_revenue,
        'net_benefit': net_benefit,
        'roi_ratio': roi_ratio,
        'avg_cost_per_closure': avg_cost_per_closure
    }
    
    # Get top 3 measures by ROI
    cur.execute("""
        SELECT 
            mi.measure_id,
            hm.measure_name,
            COUNT(*) FILTER (WHERE mi.status = 'completed') as closures,
            SUM(mi.cost_per_intervention) FILTER (WHERE mi.status = 'completed') as investment,
            CASE 
                WHEN SUM(mi.cost_per_intervention) FILTER (WHERE mi.status = 'completed') > 0 
                THEN (COUNT(*) FILTER (WHERE mi.status = 'completed') * 100.0) / 
                     SUM(mi.cost_per_intervention) FILTER (WHERE mi.status = 'completed')
                ELSE 0
            END as roi_ratio
        FROM member_interventions mi
        LEFT JOIN hedis_measures hm ON mi.measure_id = hm.measure_id
        WHERE mi.intervention_date >= %s AND mi.intervention_date <= %s
        GROUP BY mi.measure_id, hm.measure_name
        ORDER BY roi_ratio DESC
        LIMIT 3;
    """, (start_date, end_date))
    top_measures = cur.fetchall()
    
    # Get most efficient interventions
    cur.execute("""
        SELECT 
            ia.activity_name,
            CASE 
                WHEN COUNT(*) FILTER (WHERE mi.status = 'completed') > 0 
                THEN AVG(mi.cost_per_intervention) FILTER (WHERE mi.status = 'completed')
                ELSE NULL
            END as cost_per_closure,
            CASE 
                WHEN COUNT(*) > 0 
                THEN COUNT(*) FILTER (WHERE mi.status = 'completed')::DECIMAL / COUNT(*) * 100
                ELSE 0
            END as success_rate
        FROM member_interventions mi
        JOIN intervention_activities ia ON mi.activity_id = ia.activity_id
        WHERE mi.intervention_date >= %s AND mi.intervention_date <= %s
        GROUP BY ia.activity_id, ia.activity_name
        HAVING COUNT(*) FILTER (WHERE mi.status = 'completed') > 0
        ORDER BY cost_per_closure ASC
        LIMIT 3;
    """, (start_date, end_date))
    top_interventions = cur.fetchall()
    
    # Get budget metrics
    cur.execute("""
        SELECT 
            SUM(ba.budget_amount) as total_budget,
            COALESCE(SUM(as_spend.amount_spent), 0) as total_spent
        FROM budget_allocations ba
        LEFT JOIN actual_spending as_spend ON ba.measure_id = as_spend.measure_id
        WHERE ba.period_start >= %s AND ba.period_end <= %s;
    """, (start_date, end_date))
    budget_row = cur.fetchone()
    
    total_budget = float(budget_row['total_budget'] or 0) if budget_row else 0
    total_spent = float(budget_row['total_spent'] or 0) if budget_row else 0
    budget_utilization = (total_spent / total_budget * 100) if total_budget > 0 else 0
    
    # Count over-budget measures
    cur.execute("""
        SELECT COUNT(*) as over_budget_count
        FROM (
            SELECT 
                ba.measure_id,
                ba.budget_amount,
                COALESCE(SUM(as_spend.amount_spent), 0) as actual_spent
            FROM budget_allocations ba
            LEFT JOIN actual_spending as_spend ON ba.measure_id = as_spend.measure_id
            WHERE ba.period_start >= %s AND ba.period_end <= %s
            GROUP BY ba.measure_id, ba.budget_amount
            HAVING COALESCE(SUM(as_spend.amount_spent), 0) > ba.budget_amount
        ) over_budget;
    """, (start_date, end_date))
    over_budget_result = cur.fetchone()
    over_budget_count = int(over_budget_result['over_budget_count'] or 0) if over_budget_result else 0
    
    # Print summary
    print("PERFORMANCE HIGHLIGHTS")
    print("-" * 100)
    print(f"  Total Investment:        ${roi_data['total_investment']:,.2f}")
    print(f"  Estimated Revenue:       ${roi_data['total_revenue']:,.2f}")
    print(f"  Net Benefit:             ${roi_data['net_benefit']:,.2f}")
    print(f"  Overall ROI:             {roi_data['roi_ratio']:.2f}x")
    print(f"  Successful Closures:     {roi_data['total_closures']:,}")
    print(f"  Average Cost/Closure:    ${roi_data['avg_cost_per_closure']:,.2f}")
    print()
    
    print("TOP 3 PERFORMING MEASURES (by ROI)")
    print("-" * 100)
    for i, measure in enumerate(top_measures, 1):
        measure_id = measure['measure_id'] or 'N/A'
        measure_name = (measure['measure_name'] or 'N/A')[:50]
        roi = float(measure['roi_ratio'] or 0)
        investment = float(measure['investment'] or 0)
        closures = int(measure['closures'] or 0)
        print(f"  {i}. {measure_id} - {measure_name}")
        print(f"     ROI: {roi:.2f}x | Investment: ${investment:,.2f} | Closures: {closures:,}")
    print()
    
    print("MOST COST-EFFECTIVE INTERVENTIONS")
    print("-" * 100)
    for i, intervention in enumerate(top_interventions, 1):
        activity = (intervention['activity_name'] or 'N/A')[:50]
        cost = float(intervention['cost_per_closure'] or 0)
        success = float(intervention['success_rate'] or 0)
        print(f"  {i}. {activity}")
        print(f"     Cost: ${cost:,.2f} per closure | Success Rate: {success:.1f}%")
    print()
    
    print("BUDGET DISCIPLINE METRICS")
    print("-" * 100)
    print(f"  Total Budget:            ${total_budget:,.2f}")
    print(f"  Total Spent:             ${total_spent:,.2f}")
    print(f"  Budget Utilization:      {budget_utilization:.1f}%")
    print(f"  Measures Over Budget:   {over_budget_count} of 12")
    print()
    
    print("BUSINESS IMPACT STATEMENT")
    print("-" * 100)
    print(f"  In Q4 2024, our HEDIS Portfolio Optimizer delivered exceptional results:")
    print(f"  investing ${roi_data['total_investment']:,.0f} across 12 HEDIS measures to achieve")
    print(f"  {roi_data['total_closures']:,} successful gap closures, generating an estimated")
    print(f"  ${roi_data['total_revenue']:,.0f} in revenue impact. With a {roi_data['roi_ratio']:.2f}x ROI ratio")
    print(f"  and ${roi_data['net_benefit']:,.0f} net benefit, this demonstrates data-driven")
    print(f"  decision-making and measurable business value in healthcare analytics.")
    print()
    
    print("=" * 100)
    print("=" * 100)
    print(f"Report Generated: {datetime.now().strftime('%B %d, %Y')}")
    print("=" * 100)
    print("=" * 100)


def main():
    """Main execution function."""
    db_config = get_db_config()
    
    print("=" * 100)
    print("PHASE 3 EXECUTIVE SUMMARY GENERATOR")
    print("=" * 100)
    print(f"\nConnecting to database: {db_config['database']}")
    
    try:
        conn = psycopg2.connect(**db_config)
        print("[OK] Connected successfully!\n")
        
        # 1. Generate executive ROI report
        generate_executive_roi_report(conn, '2024-10-01', '2024-12-31')
        
        # 2. Show most expensive measures
        show_most_expensive_measures(conn, 3, '2024-10-01', '2024-12-31')
        
        # 3. Show most efficient interventions
        show_most_efficient_interventions(conn, 3, '2024-10-01', '2024-12-31')
        
        # 4. Calculate total ROI
        calculate_total_roi(conn, '2024-10-01', '2024-12-31')
        
        # 5. Generate one-page executive summary
        generate_one_page_summary(conn, '2024-10-01', '2024-12-31')
        
        print("\n[SUCCESS] Executive summary generation complete!")
        print("Ready for portfolio screenshots and recruiter presentations.")
        
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

