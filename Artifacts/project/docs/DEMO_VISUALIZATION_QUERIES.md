# Phase 3 Demo Visualization Queries

Export-ready SQL queries for creating visualizations in Excel, Tableau, or other tools.

---

## QUERY 1: ROI BY MEASURE (Bar Chart)

**Purpose:** Compare ROI performance across all 12 HEDIS measures  
**Visualization:** Horizontal or vertical bar chart  
**Sort:** ROI ratio descending (best performers first)

### SQL Query:
```sql
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
```

### Sample Results:
| measure_code | measure_name | total_investment | revenue_impact | roi_ratio | successful_closures | total_interventions |
|--------------|--------------|------------------|----------------|-----------|---------------------|---------------------|
| BPD | Blood Pressure Control for Patients with Diabetes | 18776.00 | 25900.0 | 1.38 | 259 | 596 |
| SUPD | Follow-Up After Emergency Dept Visit | 16570.00 | 22700.0 | 1.37 | 227 | 541 |
| BCS | Breast Cancer Screening | 13300.00 | 17900.0 | 1.35 | 179 | 452 |

**Export File:** `exports/roi_by_measure.csv`

---

## QUERY 2: COST PER CLOSURE BY ACTIVITY (Scatter Plot)

**Purpose:** Identify most cost-effective intervention types  
**Visualization:** Scatter plot with bubble size = usage frequency  
**X-Axis:** Average cost  
**Y-Axis:** Success rate  
**Bubble Size:** Times used  
**Filter:** Only activities with 10+ uses

### SQL Query:
```sql
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
```

### Sample Results:
| activity_name | avg_cost | success_rate | times_used | successful_closures | cost_per_closure |
|---------------|----------|--------------|------------|---------------------|------------------|
| Automated Reminder System | 6.00 | 44.4 | 453 | 201 | 6.00 |
| Member Portal Notification | 12.00 | 48.5 | 427 | 207 | 12.00 |
| Text Message | 30.00 | 40.6 | 433 | 176 | 30.00 |

**Export File:** `exports/cost_per_closure_by_activity.csv`

---

## QUERY 3: MONTHLY INTERVENTION TREND (Line Chart)

**Purpose:** Track intervention volume and success over time  
**Visualization:** Multi-line chart showing trends  
**X-Axis:** Month  
**Y-Axis:** Counts and rates  
**Lines:** Total interventions, successful closures, success rate

### SQL Query:
```sql
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
```

### Sample Results:
| month | month_start | total_interventions | successful_closures | avg_cost | success_rate | total_investment |
|-------|-------------|---------------------|---------------------|----------|--------------|------------------|
| 2024-10 | 2024-10-01 | 2350 | 1008 | 78.57 | 42.9 | 79003.00 |
| 2024-11 | 2024-11-01 | 2260 | 962 | 77.51 | 42.6 | 76383.00 |
| 2024-12 | 2024-12-01 | 2322 | 968 | 77.78 | 41.7 | 72333.00 |

**Export File:** `exports/monthly_intervention_trend.csv`

---

## QUERY 4: BUDGET VARIANCE BY MEASURE (Variance Chart)

**Purpose:** Identify measures over/under budget  
**Visualization:** Variance chart (waterfall or bar chart with variance indicators)  
**Sort:** By absolute variance percentage (largest variances first)

### SQL Query:
```sql
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
```

### Sample Results:
| measure_code | measure_name | budget_allocated | actual_spent | variance | variance_pct | budget_status |
|--------------|--------------|------------------|--------------|----------|--------------|---------------|
| CBP | Controlling High Blood Pressure | 30000.00 | 48388.00 | 18388.00 | 61.3 | Over Budget |
| BCS | Breast Cancer Screening | 60000.00 | 35641.00 | -24359.00 | -40.6 | Under Budget |
| PDC-STA | Statin Therapy | 40000.00 | 49797.00 | 9797.00 | 24.5 | Over Budget |

**Export File:** `exports/budget_variance_by_measure.csv`

---

## QUERY 5: COST TIER COMPARISON (Grouped Bar Chart)

**Purpose:** Compare low/medium/high touch intervention effectiveness  
**Visualization:** Grouped bar chart  
**Groups:** Low Touch, Medium Touch, High Touch  
**Metrics:** Average cost, success rate, intervention count

### SQL Query:
```sql
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
```

### Sample Results:
| cost_tier | avg_cost | success_rate | interventions_count | successful_closures | total_investment | cost_per_closure |
|-----------|----------|--------------|---------------------|---------------------|------------------|------------------|
| Low Touch | 8.91 | 46.4 | 880 | 408 | 3690.00 | 9.04 |
| Medium Touch | 39.55 | 41.4 | 2581 | 1068 | 42313.00 | 39.62 |
| High Touch | 124.03 | 42.1 | 3471 | 1462 | 181716.00 | 124.29 |

**Export File:** `exports/cost_tier_comparison.csv`

---

## How to Use

### Option 1: Run Python Export Script
```bash
python scripts/export_demo_data.py
```
This will:
- Execute all 5 queries
- Display results in formatted tables
- Export CSV files to `Artifacts/project/exports/`

### Option 2: Run SQL Queries Directly
```bash
psql -U hedis_api -d hedis_portfolio -f scripts/phase3_demo_queries.sql
```

### Option 3: Copy Individual Queries
Copy any query from `scripts/phase3_demo_queries.sql` and run in your SQL client.

---

## Export Files Location

All CSV files are saved to: `Artifacts/project/exports/`

1. `roi_by_measure.csv` - ROI performance by measure
2. `cost_per_closure_by_activity.csv` - Activity effectiveness scatter plot data
3. `monthly_intervention_trend.csv` - Time series trend data
4. `budget_variance_by_measure.csv` - Budget variance analysis
5. `cost_tier_comparison.csv` - Low/medium/high touch comparison

---

## Visualization Recommendations

### Excel
- **Bar Charts:** Query 1, Query 5
- **Scatter Plot:** Query 2 (use bubble chart)
- **Line Chart:** Query 3
- **Waterfall Chart:** Query 4

### Tableau
- All queries work well with Tableau's drag-and-drop interface
- Use calculated fields for additional metrics
- Create dashboards combining multiple visualizations

### Power BI
- Import CSV files as data sources
- Create relationships between measures and activities
- Use DAX for additional calculations

---

**Last Updated:** November 19, 2025  
**Data Period:** Q4 2024 (October 1 - December 31, 2024)

