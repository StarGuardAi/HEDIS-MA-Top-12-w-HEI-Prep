#!/usr/bin/env python3
"""
Export Phase 3 Demo Visualization Data
Runs all demo queries and exports to CSV files
"""

import sys
import os
import csv
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


def format_table(headers, rows, title=""):
    """Format query results as a clean table."""
    if not rows:
        return f"\n{title}\nNo data found.\n"
    
    # Calculate column widths
    col_widths = [len(str(h)) for h in headers]
    for row in rows:
        for i, val in enumerate(row.values()):
            if i < len(col_widths):
                col_widths[i] = max(col_widths[i], len(str(val)) if val is not None else 4)
    
    # Build table
    lines = []
    if title:
        lines.append(f"\n{'=' * 100}")
        lines.append(title)
        lines.append('=' * 100)
    
    # Header
    header_row = " | ".join(str(h).ljust(col_widths[i]) for i, h in enumerate(headers))
    lines.append(header_row)
    lines.append("-" * len(header_row))
    
    # Data rows
    for row in rows:
        data_row = " | ".join(
            str(row[h]) if row[h] is not None else "NULL"
            for h in headers
        )
        lines.append(data_row)
    
    lines.append("")
    return "\n".join(lines)


def export_to_csv(data, filename, headers):
    """Export data to CSV file."""
    output_dir = os.path.join(os.path.dirname(__file__), "..", "exports")
    os.makedirs(output_dir, exist_ok=True)
    
    filepath = os.path.join(output_dir, filename)
    
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        for row in data:
            writer.writerow({h: row[h] if row[h] is not None else '' for h in headers})
    
    return filepath


def run_query(cur, query, title, csv_filename, headers):
    """Run a query and display/export results."""
    try:
        cur.execute(query)
        rows = cur.fetchall()
        
        if rows:
            # Display table
            print(format_table(headers, rows, title))
            
            # Export to CSV
            filepath = export_to_csv(rows, csv_filename, headers)
            print(f"[OK] Exported to: {filepath}\n")
            
            return rows
        else:
            print(f"\n{title}\nNo data found.\n")
            return []
            
    except Exception as e:
        print(f"\n{title}\nERROR: {e}\n")
        return []


def main():
    """Main execution."""
    db_config = get_db_config()
    
    print("=" * 100)
    print("PHASE 3 DEMO VISUALIZATION DATA EXPORT")
    print("=" * 100)
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    try:
        conn = psycopg2.connect(**db_config)
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        # Query 1: ROI by Measure
        query1 = """
            SELECT 
                mi.measure_id as measure_code,
                hm.measure_name,
                ROUND(SUM(mi.cost_per_intervention) FILTER (WHERE mi.status = 'completed'), 2) as total_investment,
                COUNT(*) FILTER (WHERE mi.status = 'completed') * 100.0 as revenue_impact,
                CASE 
                    WHEN SUM(mi.cost_per_intervention) FILTER (WHERE mi.status = 'completed') > 0 
                    THEN ROUND((COUNT(*) FILTER (WHERE mi.status = 'completed') * 100.0) / 
                               SUM(mi.cost_per_intervention) FILTER (WHERE mi.status = 'completed'), 2)
                    ELSE 0
                END as roi_ratio,
                COUNT(*) FILTER (WHERE mi.status = 'completed') as successful_closures,
                COUNT(*) as total_interventions
            FROM member_interventions mi
            LEFT JOIN hedis_measures hm ON mi.measure_id = hm.measure_id
            WHERE mi.intervention_date >= '2024-10-01'
            AND mi.intervention_date <= '2024-12-31'
            GROUP BY mi.measure_id, hm.measure_name
            ORDER BY roi_ratio DESC;
        """
        run_query(
            cur, query1,
            "QUERY 1: ROI BY MEASURE (Bar Chart)",
            "roi_by_measure.csv",
            ['measure_code', 'measure_name', 'total_investment', 'revenue_impact', 'roi_ratio', 'successful_closures', 'total_interventions']
        )
        
        # Query 2: Cost per Closure by Activity
        query2 = """
            SELECT 
                ia.activity_name,
                ROUND(AVG(mi.cost_per_intervention) FILTER (WHERE mi.status = 'completed'), 2) as avg_cost,
                ROUND(COUNT(*) FILTER (WHERE mi.status = 'completed')::DECIMAL / COUNT(*) * 100, 1) as success_rate,
                COUNT(*) as times_used,
                COUNT(*) FILTER (WHERE mi.status = 'completed') as successful_closures,
                ROUND(SUM(mi.cost_per_intervention) FILTER (WHERE mi.status = 'completed') / 
                      NULLIF(COUNT(*) FILTER (WHERE mi.status = 'completed'), 0), 2) as cost_per_closure
            FROM member_interventions mi
            INNER JOIN intervention_activities ia ON mi.activity_id = ia.activity_id
            WHERE mi.intervention_date >= '2024-10-01'
            AND mi.intervention_date <= '2024-12-31'
            GROUP BY ia.activity_id, ia.activity_name
            HAVING COUNT(*) >= 10
            ORDER BY avg_cost ASC;
        """
        run_query(
            cur, query2,
            "QUERY 2: COST PER CLOSURE BY ACTIVITY (Scatter Plot)",
            "cost_per_closure_by_activity.csv",
            ['activity_name', 'avg_cost', 'success_rate', 'times_used', 'successful_closures', 'cost_per_closure']
        )
        
        # Query 3: Monthly Intervention Trend
        query3 = """
            SELECT 
                TO_CHAR(mi.intervention_date, 'YYYY-MM') as month,
                DATE_TRUNC('month', mi.intervention_date)::DATE as month_start,
                COUNT(*) as total_interventions,
                COUNT(*) FILTER (WHERE mi.status = 'completed') as successful_closures,
                ROUND(AVG(mi.cost_per_intervention), 2) as avg_cost,
                ROUND(COUNT(*) FILTER (WHERE mi.status = 'completed')::DECIMAL / COUNT(*) * 100, 1) as success_rate,
                ROUND(SUM(mi.cost_per_intervention) FILTER (WHERE mi.status = 'completed'), 2) as total_investment
            FROM member_interventions mi
            WHERE mi.intervention_date >= '2024-10-01'
            AND mi.intervention_date <= '2024-12-31'
            GROUP BY DATE_TRUNC('month', mi.intervention_date), TO_CHAR(mi.intervention_date, 'YYYY-MM')
            ORDER BY month_start ASC;
        """
        run_query(
            cur, query3,
            "QUERY 3: MONTHLY INTERVENTION TREND (Line Chart)",
            "monthly_intervention_trend.csv",
            ['month', 'month_start', 'total_interventions', 'successful_closures', 'avg_cost', 'success_rate', 'total_investment']
        )
        
        # Query 4: Budget Variance by Measure
        query4 = """
            SELECT 
                measure_code,
                measure_name,
                budget_allocated,
                actual_spent,
                variance,
                variance_pct,
                budget_status
            FROM (
                SELECT 
                    ba.measure_id as measure_code,
                    hm.measure_name,
                    ba.budget_amount as budget_allocated,
                    COALESCE(SUM(as_spend.amount_spent), 0) as actual_spent,
                    COALESCE(SUM(as_spend.amount_spent), 0) - ba.budget_amount as variance,
                    ROUND(((COALESCE(SUM(as_spend.amount_spent), 0) - ba.budget_amount) / NULLIF(ba.budget_amount, 0)) * 100, 1) as variance_pct,
                    CASE 
                        WHEN COALESCE(SUM(as_spend.amount_spent), 0) > ba.budget_amount THEN 'Over Budget'
                        WHEN COALESCE(SUM(as_spend.amount_spent), 0) < ba.budget_amount THEN 'Under Budget'
                        ELSE 'On Budget'
                    END as budget_status
                FROM budget_allocations ba
                LEFT JOIN hedis_measures hm ON ba.measure_id = hm.measure_id
                LEFT JOIN actual_spending as_spend ON ba.measure_id = as_spend.measure_id
                    AND as_spend.spending_date >= ba.period_start
                    AND as_spend.spending_date <= ba.period_end
                WHERE ba.period_start >= '2024-10-01' 
                AND ba.period_end <= '2024-12-31'
                GROUP BY ba.measure_id, hm.measure_name, ba.budget_amount, ba.period_start, ba.period_end
            ) subquery
            ORDER BY ABS(variance_pct) DESC;
        """
        run_query(
            cur, query4,
            "QUERY 4: BUDGET VARIANCE BY MEASURE (Variance Chart)",
            "budget_variance_by_measure.csv",
            ['measure_code', 'measure_name', 'budget_allocated', 'actual_spent', 'variance', 'variance_pct', 'budget_status']
        )
        
        # Query 5: Cost Tier Comparison
        query5 = """
            WITH intervention_tiers AS (
                SELECT 
                    mi.*,
                    ia.activity_name,
                    CASE 
                        WHEN mi.cost_per_intervention <= 25 THEN 'Low Touch'
                        WHEN mi.cost_per_intervention <= 75 THEN 'Medium Touch'
                        ELSE 'High Touch'
                    END as cost_tier
                FROM member_interventions mi
                INNER JOIN intervention_activities ia ON mi.activity_id = ia.activity_id
                WHERE mi.intervention_date >= '2024-10-01'
                AND mi.intervention_date <= '2024-12-31'
            )
            SELECT 
                cost_tier,
                ROUND(AVG(cost_per_intervention), 2) as avg_cost,
                ROUND(COUNT(*) FILTER (WHERE status = 'completed')::DECIMAL / COUNT(*) * 100, 1) as success_rate,
                COUNT(*) as interventions_count,
                COUNT(*) FILTER (WHERE status = 'completed') as successful_closures,
                ROUND(SUM(cost_per_intervention) FILTER (WHERE status = 'completed'), 2) as total_investment,
                ROUND(SUM(cost_per_intervention) FILTER (WHERE status = 'completed') / 
                      NULLIF(COUNT(*) FILTER (WHERE status = 'completed'), 0), 2) as cost_per_closure
            FROM intervention_tiers
            GROUP BY cost_tier
            ORDER BY 
                CASE cost_tier
                    WHEN 'Low Touch' THEN 1
                    WHEN 'Medium Touch' THEN 2
                    WHEN 'High Touch' THEN 3
                END;
        """
        run_query(
            cur, query5,
            "QUERY 5: COST TIER COMPARISON (Grouped Bar Chart)",
            "cost_tier_comparison.csv",
            ['cost_tier', 'avg_cost', 'success_rate', 'interventions_count', 'successful_closures', 'total_investment', 'cost_per_closure']
        )
        
        print("=" * 100)
        print("EXPORT COMPLETE")
        print("=" * 100)
        print("\nAll CSV files exported to: Artifacts/project/exports/")
        print("\nFiles created:")
        print("  1. roi_by_measure.csv")
        print("  2. cost_per_closure_by_activity.csv")
        print("  3. monthly_intervention_trend.csv")
        print("  4. budget_variance_by_measure.csv")
        print("  5. cost_tier_comparison.csv")
        print("\nSQL queries saved to: Artifacts/project/scripts/phase3_demo_queries.sql")
        
        conn.close()
        
    except psycopg2.OperationalError as e:
        print(f"[ERROR] Connection failed: {e}")
        return False
    except Exception as e:
        print(f"[ERROR] {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    main()

