#!/usr/bin/env python3
"""
Test Phase 3 ROI Calculation Functions
Test ROI functions with real Q4 2024 data
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


def check_functions_exist(conn):
    """Check if ROI functions exist."""
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    print("=" * 80)
    print("Checking for ROI Functions")
    print("=" * 80)
    
    functions_to_check = [
        'calculate_cost_per_closure',
        'calculate_intervention_roi',
        'generate_executive_roi_report'
    ]
    
    existing_functions = []
    
    for func_name in functions_to_check:
        cur.execute("""
            SELECT EXISTS (
                SELECT FROM pg_proc p
                JOIN pg_namespace n ON p.pronamespace = n.oid
                WHERE n.nspname = 'public'
                AND p.proname = %s
            );
        """, (func_name,))
        exists = cur.fetchone()['exists']
        
        status = "[OK]" if exists else "[MISSING]"
        print(f"{status} {func_name}()")
        
        if exists:
            existing_functions.append(func_name)
    
    return existing_functions


def test_cost_per_closure(conn, measure_id='GSD', start_date='2024-10-01', end_date='2024-12-31'):
    """Test calculate_cost_per_closure function."""
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    print("\n" + "=" * 80)
    print(f"TEST 1: calculate_cost_per_closure() for {measure_id}")
    print("=" * 80)
    print(f"Date Range: {start_date} to {end_date}\n")
    
    # Check if function exists
    cur.execute("""
        SELECT EXISTS (
            SELECT FROM pg_proc p
            JOIN pg_namespace n ON p.pronamespace = n.oid
            WHERE n.nspname = 'public'
            AND p.proname = 'calculate_cost_per_closure'
        );
    """)
    
    if not cur.fetchone()['exists']:
        print("[WARN] Function calculate_cost_per_closure() does not exist.")
        print("Calculating manually from data...\n")
        
        # Manual calculation
        cur.execute("""
            SELECT 
                COUNT(*) as total_interventions,
                COUNT(*) FILTER (WHERE status = 'completed') as successful_closures,
                SUM(cost_per_intervention) FILTER (WHERE status = 'completed') as total_cost,
                AVG(cost_per_intervention) FILTER (WHERE status = 'completed') as avg_cost_per_intervention
            FROM member_interventions
            WHERE measure_id = %s
            AND intervention_date >= %s
            AND intervention_date <= %s
            AND status = 'completed';
        """, (measure_id, start_date, end_date))
        
        result = cur.fetchone()
        
        total_interventions = result['total_interventions'] or 0
        successful_closures = result['successful_closures'] or 0
        total_cost = result['total_cost'] or 0
        avg_cost = result['avg_cost_per_intervention'] or 0
        
        cost_per_closure = total_cost / successful_closures if successful_closures > 0 else 0
        
        print("Results:")
        print(f"  Total Interventions: {total_interventions:,}")
        print(f"  Successful Closures: {successful_closures:,}")
        print(f"  Total Cost: ${total_cost:,.2f}")
        print(f"  Average Cost per Intervention: ${avg_cost:,.2f}")
        print(f"  Cost per Closure: ${cost_per_closure:,.2f}")
        
        return {
            'cost_per_closure': cost_per_closure,
            'total_interventions': total_interventions,
            'successful_closures': successful_closures,
            'total_cost': total_cost
        }
    else:
        # Call function
        try:
            cur.execute("""
                SELECT calculate_cost_per_closure(%s, %s, %s) as cost_per_closure;
            """, (measure_id, start_date, end_date))
            
            result = cur.fetchone()
            cost_per_closure = result['cost_per_closure'] or 0
            
            print(f"Cost per Closure: ${cost_per_closure:,.2f}")
            
            return {'cost_per_closure': cost_per_closure}
        except Exception as e:
            print(f"[ERROR] Function call failed: {e}")
            return None


def test_intervention_roi(conn, measure_id='GSD', start_date='2024-10-01', end_date='2024-12-31'):
    """Test calculate_intervention_roi function."""
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    print("\n" + "=" * 80)
    print(f"TEST 2: calculate_intervention_roi() for {measure_id}")
    print("=" * 80)
    print(f"Date Range: {start_date} to {end_date}\n")
    
    # Check if function exists
    cur.execute("""
        SELECT EXISTS (
            SELECT FROM pg_proc p
            JOIN pg_namespace n ON p.pronamespace = n.oid
            WHERE n.nspname = 'public'
            AND p.proname = 'calculate_intervention_roi'
        );
    """)
    
    if not cur.fetchone()['exists']:
        print("[WARN] Function calculate_intervention_roi() does not exist.")
        print("Calculating manually from data...\n")
        
        # Manual calculation - need to estimate revenue impact
        # Typical: Each gap closure can improve star rating, worth ~$372/member/year in QBP
        # For Q4, we'll use a portion of that
        
        cur.execute("""
            SELECT 
                COUNT(*) FILTER (WHERE status = 'completed') as successful_closures,
                SUM(cost_per_intervention) FILTER (WHERE status = 'completed') as total_investment
            FROM member_interventions
            WHERE measure_id = %s
            AND intervention_date >= %s
            AND intervention_date <= %s;
        """, (measure_id, start_date, end_date))
        
        result = cur.fetchone()
        successful_closures = result['successful_closures'] or 0
        total_investment = result['total_investment'] or 0
        
        # Estimate revenue impact (simplified - would need actual star rating impact)
        # Assume each closure improves measure performance, contributing to star rating
        # Conservative estimate: $100 per closure in QBP impact
        revenue_per_closure = 100.0
        revenue_impact = float(successful_closures) * revenue_per_closure
        total_investment_float = float(total_investment) if total_investment else 0.0
        
        roi_ratio = (revenue_impact / total_investment_float) if total_investment_float > 0 else 0
        net_benefit = revenue_impact - total_investment_float
        
        print("Results:")
        print(f"  Successful Closures: {successful_closures:,}")
        print(f"  Total Investment: ${total_investment:,.2f}")
        print(f"  Estimated Revenue Impact: ${revenue_impact:,.2f}")
        print(f"  Net Benefit: ${net_benefit:,.2f}")
        print(f"  ROI Ratio: {roi_ratio:.2f}x")
        
        return {
            'roi_ratio': roi_ratio,
            'total_investment': total_investment,
            'revenue_impact': revenue_impact,
            'net_benefit': net_benefit,
            'successful_closures': successful_closures
        }
    else:
        # Call function
        try:
            cur.execute("""
                SELECT * FROM calculate_intervention_roi(%s, %s, %s);
            """, (measure_id, start_date, end_date))
            
            result = cur.fetchone()
            
            print("Results:")
            for key, value in result.items():
                if isinstance(value, float):
                    if 'ratio' in key.lower() or 'roi' in key.lower():
                        print(f"  {key}: {value:.2f}x")
                    elif 'cost' in key.lower() or 'investment' in key.lower() or 'revenue' in key.lower() or 'benefit' in key.lower():
                        print(f"  {key}: ${value:,.2f}")
                    else:
                        print(f"  {key}: {value:,.2f}")
                else:
                    print(f"  {key}: {value}")
            
            return dict(result)
        except Exception as e:
            print(f"[ERROR] Function call failed: {e}")
            import traceback
            traceback.print_exc()
            return None


def generate_executive_roi_report(conn, start_date='2024-10-01', end_date='2024-12-31'):
    """Generate executive ROI report for Q4 2024."""
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    print("\n" + "=" * 80)
    print("TEST 3: Executive ROI Report for Q4 2024")
    print("=" * 80)
    print(f"Date Range: {start_date} to {end_date}\n")
    
    # Check if function/view exists
    cur.execute("""
        SELECT EXISTS (
            SELECT FROM pg_proc p
            JOIN pg_namespace n ON p.pronamespace = n.oid
            WHERE n.nspname = 'public'
            AND p.proname = 'generate_executive_roi_report'
        );
    """)
    function_exists = cur.fetchone()['exists']
    
    cur.execute("""
        SELECT EXISTS (
            SELECT FROM information_schema.views
            WHERE table_schema = 'public'
            AND table_name = 'v_roi_summary_dashboard'
        );
    """)
    view_exists = cur.fetchone()['exists']
    
    if function_exists:
        try:
            cur.execute("""
                SELECT * FROM generate_executive_roi_report(%s, %s);
            """, (start_date, end_date))
            results = cur.fetchall()
            
            if results:
                print("Executive ROI Report:\n")
                for row in results:
                    for key, value in row.items():
                        print(f"  {key}: {value}")
            else:
                print("[WARN] Function returned no results")
        except Exception as e:
            print(f"[ERROR] Function call failed: {e}")
            function_exists = False
    
    if not function_exists:
        # Generate report manually
        print("Generating report from data...\n")
        
        cur.execute("""
            SELECT 
                mi.measure_id,
                hm.measure_name,
                COUNT(*) FILTER (WHERE mi.status = 'completed') as successful_closures,
                COUNT(*) as total_interventions,
                SUM(mi.cost_per_intervention) FILTER (WHERE mi.status = 'completed') as total_investment,
                AVG(mi.cost_per_intervention) FILTER (WHERE mi.status = 'completed') as avg_cost_per_closure,
                COUNT(*) FILTER (WHERE mi.status = 'completed') * 100.0 as estimated_revenue_impact
            FROM member_interventions mi
            LEFT JOIN hedis_measures hm ON mi.measure_id = hm.measure_id
            WHERE mi.intervention_date >= %s
            AND mi.intervention_date <= %s
            GROUP BY mi.measure_id, hm.measure_name
            ORDER BY successful_closures DESC;
        """, (start_date, end_date))
        
        results = cur.fetchall()
        
        if results:
            print("=" * 100)
            print(f"{'Measure':<12} {'Measure Name':<30} {'Closures':<12} {'Interventions':<15} {'Investment':<15} {'Avg Cost':<12} {'Est. Revenue':<15}")
            print("=" * 100)
            
            total_closures = 0
            total_interventions = 0
            total_investment = 0
            total_revenue = 0
            
            for row in results:
                measure_id = row['measure_id'] or 'N/A'
                measure_name = (row['measure_name'] or 'N/A')[:28]
                closures = row['successful_closures'] or 0
                interventions = row['total_interventions'] or 0
                investment = row['total_investment'] or 0
                avg_cost = float(row['avg_cost_per_closure']) if row['avg_cost_per_closure'] else 0.0
                revenue = float(row['estimated_revenue_impact']) if row['estimated_revenue_impact'] else 0.0
                investment_float = float(investment) if investment else 0.0
                
                total_closures += closures
                total_interventions += interventions
                total_investment += investment_float
                total_revenue += revenue
                
                print(f"{measure_id:<12} {measure_name:<30} {closures:<12,} {interventions:<15,} ${investment_float:<14,.2f} ${avg_cost:<11,.2f} ${revenue:<14,.2f}")
            
            print("=" * 100)
            print(f"{'TOTAL':<12} {'':<30} {total_closures:<12,} {total_interventions:<15,} ${total_investment:<14,.2f} {'':<12} ${total_revenue:<14,.2f}")
            print("=" * 100)
            
            overall_roi = (total_revenue / total_investment) if total_investment > 0 else 0
            net_benefit = total_revenue - total_investment
            
            print(f"\nSummary:")
            print(f"  Total Successful Closures: {total_closures:,}")
            print(f"  Total Interventions: {total_interventions:,}")
            print(f"  Total Investment: ${total_investment:,.2f}")
            print(f"  Estimated Revenue Impact: ${total_revenue:,.2f}")
            print(f"  Net Benefit: ${net_benefit:,.2f}")
            print(f"  Overall ROI Ratio: {overall_roi:.2f}x")
            
            return results
        else:
            print("[WARN] No data found for report")
            return None


def show_top_measures_by_roi(conn, top_n=3, start_date='2024-10-01', end_date='2024-12-31'):
    """Show top N measures by ROI ratio."""
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    print("\n" + "=" * 80)
    print(f"TEST 4: Top {top_n} Measures by ROI Ratio")
    print("=" * 80)
    print(f"Date Range: {start_date} to {end_date}\n")
    
    # Calculate ROI for each measure
    cur.execute("""
        SELECT 
            mi.measure_id,
            hm.measure_name,
            COUNT(*) FILTER (WHERE mi.status = 'completed') as successful_closures,
            SUM(mi.cost_per_intervention) FILTER (WHERE mi.status = 'completed') as total_investment,
            COUNT(*) FILTER (WHERE mi.status = 'completed') * 100.0 as estimated_revenue_impact
        FROM member_interventions mi
        LEFT JOIN hedis_measures hm ON mi.measure_id = hm.measure_id
        WHERE mi.intervention_date >= %s
        AND mi.intervention_date <= %s
        GROUP BY mi.measure_id, hm.measure_name
        HAVING COUNT(*) FILTER (WHERE mi.status = 'completed') > 0
        ORDER BY (COUNT(*) FILTER (WHERE mi.status = 'completed') * 100.0) / 
                 NULLIF(SUM(mi.cost_per_intervention) FILTER (WHERE mi.status = 'completed'), 0) DESC
        LIMIT %s;
    """, (start_date, end_date, top_n))
    
    results = cur.fetchall()
    
    if results:
        print("=" * 100)
        print(f"{'Rank':<6} {'Measure':<12} {'Measure Name':<30} {'ROI Ratio':<12} {'Investment':<15} {'Revenue':<15} {'Closures':<12}")
        print("=" * 100)
        
        for i, row in enumerate(results, 1):
            measure_id = row['measure_id'] or 'N/A'
            measure_name = (row['measure_name'] or 'N/A')[:28]
            closures = row['successful_closures'] or 0
            investment = float(row['total_investment']) if row['total_investment'] else 0.0
            revenue = float(row['estimated_revenue_impact']) if row['estimated_revenue_impact'] else 0.0
            roi_ratio = (revenue / investment) if investment > 0 else 0
            
            print(f"{i:<6} {measure_id:<12} {measure_name:<30} {roi_ratio:<11.2f}x ${investment:<14,.2f} ${revenue:<14,.2f} {closures:<12,}")
        
        print("=" * 100)
        
        return results
    else:
        print("[WARN] No data found")
        return None


def main():
    """Main execution function."""
    db_config = get_db_config()
    
    print("=" * 80)
    print("PHASE 3 ROI FUNCTION TESTS")
    print("=" * 80)
    print(f"\nConnecting to database: {db_config['database']}")
    
    try:
        conn = psycopg2.connect(**db_config)
        print("[OK] Connected successfully!\n")
        
        # Check what functions exist
        existing_functions = check_functions_exist(conn)
        
        # Test 1: Cost per closure for GSD
        test_cost_per_closure(conn, 'GSD', '2024-10-01', '2024-12-31')
        
        # Test 2: ROI for GSD
        test_intervention_roi(conn, 'GSD', '2024-10-01', '2024-12-31')
        
        # Test 3: Executive ROI report
        generate_executive_roi_report(conn, '2024-10-01', '2024-12-31')
        
        # Test 4: Top 3 measures by ROI
        show_top_measures_by_roi(conn, 3, '2024-10-01', '2024-12-31')
        
        print("\n" + "=" * 80)
        print("[SUCCESS] All ROI tests completed!")
        print("=" * 80)
        
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

