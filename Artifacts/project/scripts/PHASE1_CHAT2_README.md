# Phase 1 Chat 2: Gap Closure Velocity Tracking & Trend Analysis

## Overview

This SQL script builds on Phase 1 Chat 1 to add gap closure velocity tracking, trend analysis, and predictive analytics. It creates:

- **1,000 Demo Members** across 3 MA plans
- **Member-Level Gaps** with historical tracking
- **Closure Activity Tracking** with timestamps
- **Velocity Metrics** (monthly periods Jan-Oct 2024)
- **3 Analysis Views** for velocity dashboards
- **Velocity Calculation Function** for custom period analysis

## Prerequisites

**⚠️ IMPORTANT: Phase 1 Chat 1 must be completed first!**

The script requires:
- All Phase 1 Chat 1 tables (hedis_measures, ma_plans, plan_performance, etc.)
- Database connection with appropriate permissions

## Quick Start

### Option 1: Windows Batch File (Easiest)
```cmd
cd Artifacts\project\scripts
run_phase1_chat2.bat
```

### Option 2: Python Script
```bash
cd Artifacts/project/scripts
python run_phase1_chat2.py
```

### Option 3: Direct SQL (psql)
```bash
psql -U hedis_api -d hedis_portfolio -f scripts/phase1_chat2_velocity_tracking.sql
```

## Expected Runtime

- **Full script execution**: 2-3 minutes
- **Member generation**: ~15 seconds
- **Gap data creation**: ~30 seconds
- **Activity tracking**: ~10 seconds
- **Velocity metrics**: ~45 seconds
- **View creation**: ~5 seconds

## What Gets Created

### Demo Data
- **1,000 Members**: 500 (H1234-001), 300 (H5678-002), 200 (H9012-003)
- **Member Gaps**: For 5 key measures (GSD, KED, EED, BPD, CBP)
- **Closure Activities**: Timestamped activities for closed gaps
- **Velocity Metrics**: Monthly snapshots (Jan-Oct 2024)

### Database Objects
- **1 Table**: `gap_velocity_metrics` (aggregate velocity tracking)
- **1 Function**: `calculate_gap_velocity()` (custom period analysis)
- **3 Views**:
  - `vw_current_velocity` - Current velocity dashboard
  - `vw_velocity_trends` - Month-over-month trends
  - `vw_velocity_performance` - Performance rankings

## Expected Results

### Velocity Metrics
- **Closure Rates**: 8-15% monthly (varies by plan/measure)
- **Average Days to Close**: 
  - GSD/KED: 60-75 days (administrative data)
  - EED: 90-120 days (requires appointments)
  - BPD/CBP: 70-90 days (medical records)
- **Weekly Velocity**: 2-10 gaps per week (varies by plan)

### Performance Patterns
- **H9012-003** (High-Performer): Highest velocity scores
- **H1234-001** (Struggling): Lower velocity but improving trends
- **H5678-002** (Stable): Consistent moderate velocity

## Key Test Queries

### Current Velocity Dashboard
```sql
SELECT 
    plan_id,
    plan_name,
    measure_id,
    measure_name,
    gaps_open_end AS current_gaps,
    gaps_per_week,
    closure_rate_pct,
    velocity_rating,
    closure_status
FROM vw_current_velocity
ORDER BY plan_id, measure_id;
```

### Velocity Trends
```sql
SELECT 
    plan_id,
    measure_id,
    TO_CHAR(current_period, 'YYYY-MM') AS period,
    ROUND(current_velocity, 2) AS current_vel,
    ROUND(prior_velocity, 2) AS prior_vel,
    trend_direction
FROM vw_velocity_trends
WHERE current_period >= DATE '2024-08-01'
ORDER BY plan_id, measure_id, current_period;
```

### Performance Rankings
```sql
SELECT 
    plan_name,
    measure_name,
    ROUND(velocity_score, 2) AS weekly_velocity,
    ROUND(closure_rate_pct, 2) AS closure_rate,
    performance_tier
FROM vw_velocity_performance
ORDER BY measure_id, velocity_rank;
```

## Validation Checklist

The runner automatically checks:
- ✅ 1,000 members created
- ✅ Member gaps exist for key measures
- ✅ Closure activities tracked
- ✅ Velocity metrics calculated
- ✅ 3 velocity views created

## Troubleshooting

### Error: "relation does not exist"
- **Cause**: Phase 1 Chat 1 not completed
- **Solution**: Run `phase1_chat1_revenue_calculator_foundation.sql` first

### Error: "duplicate key value"
- **Cause**: Script already partially executed
- **Solution**: Drop and recreate tables, or use `TRUNCATE` for demo data tables

### Slow Performance
- **Cause**: Large data generation
- **Solution**: Normal for first run; subsequent runs are faster

### No Velocity Data
- **Cause**: No gaps closed in demo period
- **Solution**: Check `member_gaps` table for closed gaps with `gap_closed_date` set

## Database Schema Additions

### New Table: `gap_velocity_metrics`
Tracks velocity metrics by plan/measure/period:
- Snapshot metrics (gaps open/closed)
- Velocity calculations (closure rate, days to close, weekly velocity)
- Projections (projected closure date, on-track status)

### New Function: `calculate_gap_velocity()`
Calculates velocity for custom date ranges:
```sql
SELECT * FROM calculate_gap_velocity(
    'H1234-001',  -- plan_id
    'GSD',        -- measure_id
    2024,         -- measurement_year
    DATE '2024-09-01',  -- period_start
    DATE '2024-09-30'   -- period_end
);
```

## Key Insights

### Closure Patterns
- **Administrative Measures** (GSD, KED): Faster closure (60-75 days)
- **Hybrid Measures** (EED): Slower closure (90-120 days) - requires appointments
- **Outcome Measures** (BPD, CBP): Moderate closure (70-90 days)

### Seasonal Trends
- **Q1**: Higher velocity (new year engagement)
- **Summer**: Dip in velocity (vacation season)
- **Q4**: Acceleration (year-end push)

### Performance Tiers
- **Excellent**: ≥10 gaps/week
- **Good**: 5-10 gaps/week
- **Fair**: 2-5 gaps/week
- **Needs Improvement**: <2 gaps/week

## Next Steps

After successful execution:

1. ✅ Review velocity dashboard (`vw_current_velocity`)
2. ✅ Analyze trends (`vw_velocity_trends`)
3. ✅ Identify top/bottom performers (`vw_velocity_performance`)
4. ✅ Proceed to **Phase 1 Chat 3** for ROI Analysis & Cost-per-Closure tracking

## Support

For issues or questions:
- Verify Phase 1 Chat 1 is complete
- Check database logs for detailed error messages
- Review validation checklist output

---

**Author**: Robert Reichert  
**Created**: 2025-11-18  
**Version**: Phase 1 Chat 2  
**Prerequisites**: Phase 1 Chat 1

