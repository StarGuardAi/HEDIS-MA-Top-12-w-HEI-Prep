# Phase 1 Chat 1: Revenue at Risk Calculator Foundation

## Overview

This SQL script establishes the foundational database schema and demo data for the HEDIS Star Rating Portfolio Optimizer. It creates:

- **12 Critical HEDIS Measures** with Star Rating thresholds
- **3 Demo MA Plans** representing different performance scenarios
- **Revenue Calculation Functions** for portfolio-level analysis
- **Test Queries** for validation

## Prerequisites

- PostgreSQL 12+ (or SQL Server with minor syntax adjustments)
- Database initialized (run `init_database.sql` first if needed)
- Appropriate database permissions (CREATE TABLE, INSERT, CREATE FUNCTION, CREATE VIEW)

## Quick Start

### Option 1: Using psql Command Line

```bash
# Connect to your database
psql -U hedis_api -d hedis_portfolio -f scripts/phase1_chat1_revenue_calculator_foundation.sql
```

### Option 2: Using pgAdmin or DBeaver

1. Open the SQL script in your database client
2. Connect to the `hedis_portfolio` database
3. Execute the entire script (or run sections sequentially)

### Option 3: Using Python (psycopg2)

```python
import psycopg2
from pathlib import Path

# Connect to database
conn = psycopg2.connect(
    host="localhost",
    database="hedis_portfolio",
    user="hedis_api",
    password="hedis_password"
)

# Read and execute script
script_path = Path("scripts/phase1_chat1_revenue_calculator_foundation.sql")
with open(script_path, 'r') as f:
    sql_script = f.read()

with conn.cursor() as cur:
    cur.execute(sql_script)
    conn.commit()

conn.close()
print("Phase 1 Chat 1 setup complete!")
```

## Expected Runtime

- **Full script execution**: 2-3 minutes
- **Schema creation**: ~10 seconds
- **Data insertion**: ~30 seconds
- **Function/view creation**: ~5 seconds

## Validation

After running the script, execute the test queries (Section 8) to verify:

1. ✅ All 12 HEDIS measures loaded
2. ✅ Star thresholds complete (7 levels per measure = 84 threshold records)
3. ✅ 3 demo plans created
4. ✅ 36 performance records (12 measures × 3 plans)
5. ✅ Revenue calculation function operational
6. ✅ View returning revenue at risk data

## Expected Results

### Revenue at Risk Summary

| Plan ID | Plan Name | Revenue at Risk | Total Gaps |
|---------|-----------|----------------|------------|
| H1234-001 | HealthFirst Advantage Plus | ~$1.2M | 19,557 |
| H5678-002 | WellCare Premier | ~$380K | 3,291 |
| H9012-003 | Summit Elite Medicare | ~$180K | 2,257 |
| **Portfolio Total** | | **~$1.76M** | **25,105** |

### Key Test Queries

Run these queries to verify setup:

```sql
-- Test 1: Measure Catalog
SELECT measure_id, measure_name, domain, star_weight, revenue_per_point
FROM hedis_measures
ORDER BY domain, measure_id;

-- Test 5: Revenue at Risk Summary (Most Important)
SELECT 
    plan_id,
    plan_name,
    COUNT(DISTINCT measure_id) AS measures_at_risk,
    SUM(members_needed) AS total_gaps,
    SUM(revenue_at_risk) AS total_revenue_at_risk
FROM vw_revenue_at_risk
WHERE measurement_year = 2024
GROUP BY plan_id, plan_name
ORDER BY total_revenue_at_risk DESC;
```

## Database Schema

### Core Tables

1. **hedis_measures** - Catalog of 12 HEDIS measures
2. **star_thresholds** - Star rating cut points by measure
3. **ma_plans** - Medicare Advantage plan information
4. **plan_performance** - Performance data by plan/measure
5. **plan_members** - Member demographics (structure only, no demo data)
6. **member_gaps** - Member-level care gaps (structure only, no demo data)
7. **gap_closure_tracking** - Gap closure activity (structure only, no demo data)

### Views & Functions

- **vw_revenue_at_risk** - Portfolio-level revenue analysis view
- **calculate_revenue_impact()** - Function to calculate revenue impact for specific plan/measure

## Troubleshooting

### Error: "relation already exists"
- The script includes `DROP TABLE IF EXISTS` statements
- If errors persist, manually drop objects or use `CASCADE`

### Error: "permission denied"
- Ensure database user has CREATE privileges
- Grant necessary permissions: `GRANT ALL ON SCHEMA public TO hedis_api;`

### Error: "syntax error near..."
- Verify PostgreSQL version (12+ recommended)
- For SQL Server, adjust SERIAL to IDENTITY, TIMESTAMP to DATETIME2

### No data in views
- Check that `plan_performance` has records
- Verify `current_star_rating < target_star_rating` (view only shows gaps)

## Next Steps

After successful execution:

1. ✅ Verify all test queries return expected results
2. ✅ Review revenue at risk calculations
3. ✅ Proceed to **Phase 1 Chat 2** for Gap Closure Velocity tracking

## Support

For issues or questions:
- Review the validation checklist in the SQL script
- Check database logs for detailed error messages
- Verify all prerequisites are met

---

**Author**: Robert Reichert  
**Created**: 2025-11-18  
**Version**: Phase 1 Chat 1

