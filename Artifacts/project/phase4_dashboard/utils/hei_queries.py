"""
HEI (Health Equity Index) Database Queries
Query utilities for health equity and disparity analysis
"""
from datetime import datetime, timedelta
from typing import Optional


def get_hei_demographic_data_query(
    start_date: str = "2024-01-01",
    end_date: str = "2024-12-31",
    measure_ids: Optional[list] = None
) -> str:
    """
    Query to get demographic breakdown by measure for HEI analysis.
    
    Returns completion rates by measure, race, age_group, and gender.
    """
    measure_filter = ""
    if measure_ids:
        measure_list = "', '".join(measure_ids)
        measure_filter = f"AND mi.measure_id IN ('{measure_list}')"
    
    # Note: This assumes demographic columns exist in member_interventions or a members table
    # Adjust based on actual schema
    return f"""
        SELECT 
            hm.measure_name,
            COALESCE(m.race, 'Unknown') as race,
            CASE 
                WHEN m.date_of_birth IS NOT NULL 
                THEN CASE
                    WHEN DATE_PART('year', AGE(m.date_of_birth)) BETWEEN 18 AND 44 THEN '18-44'
                    WHEN DATE_PART('year', AGE(m.date_of_birth)) BETWEEN 45 AND 64 THEN '45-64'
                    WHEN DATE_PART('year', AGE(m.date_of_birth)) BETWEEN 65 AND 74 THEN '65-74'
                    ELSE '75+'
                END
                ELSE 'Unknown'
            END as age_group,
            COALESCE(m.gender, 'Unknown') as gender,
            COUNT(DISTINCT mi.member_id) as member_count,
            COUNT(DISTINCT CASE WHEN mi.status = 'completed' THEN mi.member_id END) as completed_count
        FROM member_interventions mi
        LEFT JOIN hedis_measures hm ON mi.measure_id = hm.measure_id
        LEFT JOIN members m ON mi.member_id = m.member_id
        WHERE mi.intervention_date >= '{start_date}'
          AND mi.intervention_date <= '{end_date}'
          {measure_filter}
        GROUP BY hm.measure_name, m.race, age_group, m.gender
        ORDER BY hm.measure_name, m.race, age_group, m.gender;
    """


def get_hei_demographic_data_sqlite_query(
    start_date: str = "2024-01-01",
    end_date: str = "2024-12-31",
    measure_ids: Optional[list] = None
) -> str:
    """
    SQLite-compatible version of HEI demographic data query.
    """
    measure_filter = ""
    if measure_ids:
        measure_list = "', '".join(measure_ids)
        measure_filter = f"AND mi.measure_id IN ('{measure_list}')"
    
    return f"""
        SELECT 
            hm.measure_name,
            COALESCE(m.race, 'Unknown') as race,
            CASE 
                WHEN m.date_of_birth IS NOT NULL 
                THEN CASE
                    WHEN (strftime('%Y', 'now') - strftime('%Y', m.date_of_birth)) BETWEEN 18 AND 44 THEN '18-44'
                    WHEN (strftime('%Y', 'now') - strftime('%Y', m.date_of_birth)) BETWEEN 45 AND 64 THEN '45-64'
                    WHEN (strftime('%Y', 'now') - strftime('%Y', m.date_of_birth)) BETWEEN 65 AND 74 THEN '65-74'
                    ELSE '75+'
                END
                ELSE 'Unknown'
            END as age_group,
            COALESCE(m.gender, 'Unknown') as gender,
            COUNT(DISTINCT mi.member_id) as member_count,
            COUNT(DISTINCT CASE WHEN mi.status = 'completed' THEN mi.member_id END) as completed_count
        FROM member_interventions mi
        LEFT JOIN hedis_measures hm ON mi.measure_id = hm.measure_id
        LEFT JOIN members m ON mi.member_id = m.member_id
        WHERE mi.intervention_date >= '{start_date}'
          AND mi.intervention_date <= '{end_date}'
          {measure_filter}
        GROUP BY hm.measure_name, m.race, age_group, m.gender
        ORDER BY hm.measure_name, m.race, age_group, m.gender;
    """


def get_measure_equity_summary_query(
    start_date: str = "2024-01-01",
    end_date: str = "2024-12-31"
) -> str:
    """
    Query to get equity summary by measure (overall rates and demographic breakdowns).
    """
    return f"""
        SELECT 
            hm.measure_name,
            COUNT(DISTINCT mi.member_id) as total_members,
            COUNT(DISTINCT CASE WHEN mi.status = 'completed' THEN mi.member_id END) as completed_members,
            ROUND(
                CAST(COUNT(DISTINCT CASE WHEN mi.status = 'completed' THEN mi.member_id END) AS FLOAT) * 100.0 / 
                NULLIF(COUNT(DISTINCT mi.member_id), 0),
                2
            ) as overall_rate
        FROM member_interventions mi
        LEFT JOIN hedis_measures hm ON mi.measure_id = hm.measure_id
        WHERE mi.intervention_date >= '{start_date}'
          AND mi.intervention_date <= '{end_date}'
        GROUP BY hm.measure_name
        ORDER BY hm.measure_name;
    """


def get_available_measures_query() -> str:
    """Get list of available measures from database."""
    return """
        SELECT DISTINCT 
            measure_id,
            measure_name
        FROM hedis_measures
        ORDER BY measure_name;
    """


def get_historical_hei_trend_query(
    months: int = 24
) -> str:
    """
    Query to get historical HEI trend over time.
    Returns monthly aggregate data for trend analysis.
    """
    # Calculate start date
    start_date = datetime.now().replace(day=1) - timedelta(days=30 * months)
    
    return f"""
        SELECT 
            DATE_TRUNC('month', mi.intervention_date) as month,
            COUNT(DISTINCT mi.member_id) as total_members,
            COUNT(DISTINCT CASE WHEN mi.status = 'completed' THEN mi.member_id END) as completed_members
        FROM member_interventions mi
        WHERE mi.intervention_date >= '{start_date.strftime('%Y-%m-%d')}'
        GROUP BY DATE_TRUNC('month', mi.intervention_date)
        ORDER BY month ASC;
    """


def get_historical_hei_trend_sqlite_query(
    months: int = 24
) -> str:
    """
    SQLite-compatible version of historical HEI trend query.
    """
    start_date = datetime.now().replace(day=1) - timedelta(days=30 * months)
    
    return f"""
        SELECT 
            date(mi.intervention_date, 'start of month') as month,
            COUNT(DISTINCT mi.member_id) as total_members,
            COUNT(DISTINCT CASE WHEN mi.status = 'completed' THEN mi.member_id END) as completed_members
        FROM member_interventions mi
        WHERE mi.intervention_date >= '{start_date.strftime('%Y-%m-%d')}'
        GROUP BY date(mi.intervention_date, 'start of month')
        ORDER BY month ASC;
    """

