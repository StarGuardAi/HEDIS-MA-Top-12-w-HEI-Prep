"""
Quick Database Query Tool
Run common analytics queries on the HEDIS Portfolio database
"""
import psycopg2
import pandas as pd
from typing import Optional

def get_connection():
    """Get database connection."""
    return psycopg2.connect(
        host='localhost',
        database='hedis_portfolio',
        user='hedis_api',
        password='hedis_password'
    )

def query_to_dataframe(query: str) -> pd.DataFrame:
    """Execute query and return as DataFrame."""
    conn = get_connection()
    try:
        df = pd.read_sql(query, conn)
        return df
    finally:
        conn.close()

def get_revenue_at_risk(plan_id: Optional[str] = None) -> pd.DataFrame:
    """Get revenue at risk data."""
    query = "SELECT * FROM vw_revenue_at_risk"
    if plan_id:
        query += f" WHERE plan_id = '{plan_id}'"
    query += " ORDER BY revenue_at_risk DESC"
    return query_to_dataframe(query)

def get_cost_per_closure(plan_id: Optional[str] = None) -> pd.DataFrame:
    """Get cost per closure data."""
    query = "SELECT * FROM vw_cost_per_closure"
    if plan_id:
        query += f" WHERE plan_id = '{plan_id}'"
    query += " ORDER BY cost_per_gap_closed"
    return query_to_dataframe(query)

def get_velocity_metrics(plan_id: Optional[str] = None) -> pd.DataFrame:
    """Get velocity metrics."""
    query = "SELECT * FROM vw_current_velocity"
    if plan_id:
        query += f" WHERE plan_id = '{plan_id}'"
    return query_to_dataframe(query)

def get_member_segmentation(plan_id: Optional[str] = None) -> pd.DataFrame:
    """Get member segmentation data."""
    query = "SELECT * FROM vw_member_segmentation"
    if plan_id:
        query += f" WHERE plan_id = '{plan_id}'"
    query += " ORDER BY member_count DESC"
    return query_to_dataframe(query)

def get_portfolio_roi(plan_id: Optional[str] = None) -> pd.DataFrame:
    """Get portfolio ROI data."""
    query = "SELECT * FROM vw_portfolio_roi"
    if plan_id:
        query += f" WHERE plan_id = '{plan_id}'"
    query += " ORDER BY projected_roi_ratio DESC"
    return query_to_dataframe(query)

def print_summary():
    """Print database summary."""
    conn = get_connection()
    cur = conn.cursor()
    
    print("\n" + "=" * 80)
    print("HEDIS PORTFOLIO DATABASE - QUICK SUMMARY")
    print("=" * 80)
    
    # Member counts
    cur.execute("SELECT COUNT(*) FROM plan_members WHERE member_id LIKE 'M%'")
    members = cur.fetchone()[0]
    print(f"\nMembers: {members:,}")
    
    # Gap counts
    cur.execute("SELECT COUNT(*) FROM member_gaps WHERE member_id LIKE 'M%'")
    gaps = cur.fetchone()[0]
    print(f"Care Gaps: {gaps:,}")
    
    # Plans
    cur.execute("SELECT COUNT(*) FROM ma_plans")
    plans = cur.fetchone()[0]
    print(f"MA Plans: {plans}")
    
    # Measures
    cur.execute("SELECT COUNT(*) FROM hedis_measures")
    measures = cur.fetchone()[0]
    print(f"HEDIS Measures: {measures}")
    
    # Revenue at Risk
    cur.execute("SELECT COUNT(*) FROM vw_revenue_at_risk")
    rar_records = cur.fetchone()[0]
    print(f"Revenue at Risk Records: {rar_records}")
    
    # Total Revenue at Risk
    cur.execute("SELECT SUM(revenue_at_risk) FROM vw_revenue_at_risk")
    total_rar = cur.fetchone()[0]
    if total_rar:
        print(f"Total Revenue at Risk: ${total_rar:,.0f}")
    
    print("\n" + "=" * 80)
    
    conn.close()

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "summary":
            print_summary()
        elif command == "revenue":
            plan_id = sys.argv[2] if len(sys.argv) > 2 else None
            df = get_revenue_at_risk(plan_id)
            print("\nRevenue at Risk:")
            print(df.to_string(index=False))
        elif command == "cost":
            plan_id = sys.argv[2] if len(sys.argv) > 2 else None
            df = get_cost_per_closure(plan_id)
            print("\nCost per Closure:")
            print(df.to_string(index=False))
        elif command == "velocity":
            plan_id = sys.argv[2] if len(sys.argv) > 2 else None
            df = get_velocity_metrics(plan_id)
            print("\nVelocity Metrics:")
            print(df.to_string(index=False))
        elif command == "segmentation":
            plan_id = sys.argv[2] if len(sys.argv) > 2 else None
            df = get_member_segmentation(plan_id)
            print("\nMember Segmentation:")
            print(df.to_string(index=False))
        elif command == "roi":
            plan_id = sys.argv[2] if len(sys.argv) > 2 else None
            df = get_portfolio_roi(plan_id)
            print("\nPortfolio ROI:")
            print(df.to_string(index=False))
        else:
            print(f"Unknown command: {command}")
            print("\nAvailable commands:")
            print("  summary       - Database summary")
            print("  revenue       - Revenue at risk data")
            print("  cost          - Cost per closure data")
            print("  velocity      - Velocity metrics")
            print("  segmentation  - Member segmentation")
            print("  roi           - Portfolio ROI")
    else:
        print_summary()
        print("\nUsage: python quick_query.py <command> [plan_id]")
        print("\nExamples:")
        print("  python quick_query.py summary")
        print("  python quick_query.py revenue")
        print("  python quick_query.py revenue H1234-001")
        print("  python quick_query.py cost")
        print("  python quick_query.py velocity H5678-002")

