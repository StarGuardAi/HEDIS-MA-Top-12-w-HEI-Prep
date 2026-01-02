# Phase 1 Chat 1 - Quick Start Guide

## Files Created

✅ **phase1_chat1_revenue_calculator_foundation.sql** - Main SQL script (all database setup)  
✅ **run_phase1_chat1.py** - Python runner with validation  
✅ **run_phase1_chat1.bat** - Windows batch file for easy execution  
✅ **PHASE1_CHAT1_README.md** - Comprehensive documentation  

## Quick Execution (3 Options)

### Option 1: Windows Batch File (Easiest)
```cmd
cd Artifacts\project\scripts
run_phase1_chat1.bat
```

### Option 2: Python Script
```bash
cd Artifacts/project/scripts
python run_phase1_chat1.py
```

### Option 3: Direct SQL (psql)
```bash
psql -U hedis_api -d hedis_portfolio -f scripts/phase1_chat1_revenue_calculator_foundation.sql
```

## What Gets Created

### Database Objects
- **7 Tables**: hedis_measures, star_thresholds, ma_plans, plan_performance, plan_members, member_gaps, gap_closure_tracking
- **1 View**: vw_revenue_at_risk (portfolio-level analysis)
- **1 Function**: calculate_revenue_impact() (plan/measure revenue calculation)

### Demo Data
- **12 HEDIS Measures** with revenue weights
- **84 Star Thresholds** (7 levels × 12 measures)
- **3 MA Plans** (struggling, stable, high-performer)
- **36 Performance Records** (12 measures × 3 plans)

## Expected Output

After successful execution, you should see:

```
✓ Database connection established
✓ SQL script executed successfully
✓ All validation checks passed

💰 Revenue at Risk Summary:
Plan ID       Plan Name                      Measures   Gaps       Revenue ($)    Weighted ($)
H1234-001     HealthFirst Advantage Plus    12         19,557     $1,200,000     $3,600,000
H5678-002     WellCare Premier               12         3,291      $380,000      $950,000
H9012-003     Summit Elite Medicare          12         2,257      $180,000      $450,000
PORTFOLIO TOTAL                                        25,105     $1,760,000
```

## Validation Checklist

The runner automatically checks:
- ✅ 12 measures loaded
- ✅ 84 thresholds loaded (7 per measure)
- ✅ 3 plans created
- ✅ 36 performance records
- ✅ Revenue view operational

## Troubleshooting

**Connection Error?**
- Verify PostgreSQL is running
- Check database credentials in `run_phase1_chat1.py` or set environment variables

**Permission Error?**
- Ensure user has CREATE privileges
- Run: `GRANT ALL ON SCHEMA public TO hedis_api;`

**Script Not Found?**
- Ensure you're in the correct directory
- Check file path: `Artifacts/project/scripts/phase1_chat1_revenue_calculator_foundation.sql`

## Next Steps

Once Phase 1 Chat 1 is complete:
1. ✅ Verify revenue calculations match expected values
2. ✅ Review the `vw_revenue_at_risk` view
3. ✅ Proceed to **Phase 1 Chat 2** for Gap Closure Velocity tracking

## Database Configuration

Default settings (can be overridden via environment variables):
- **Host**: localhost
- **Database**: hedis_portfolio
- **User**: hedis_api
- **Password**: hedis_password
- **Port**: 5432

To customize, set environment variables:
```bash
export DB_HOST=your_host
export DB_NAME=your_database
export DB_USER=your_user
export DB_PASSWORD=your_password
```

Or edit `run_phase1_chat1.py` directly.

---

**Ready to run?** Execute `run_phase1_chat1.bat` (Windows) or `python run_phase1_chat1.py` (Linux/Mac)

