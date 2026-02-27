# Full System Validation Suite

Comprehensive testing suite for Phase 1 & Phase 2 of the HEDIS Star Rating Portfolio Optimizer.

## Quick Start

### Option 1: Using psql (Recommended)

The validation script is designed to run with `psql` command-line tool, which supports `\echo` commands for formatted output.

#### Windows (Batch Script)
```batch
cd Artifacts\project\scripts
run_validation_psql.bat
```

#### Windows (PowerShell)
```powershell
cd Artifacts\project\scripts
.\run_validation_psql.ps1
```

#### Manual psql Command
```bash
# Set environment variables (optional, defaults provided)
set DB_HOST=localhost
set DB_NAME=hedis_portfolio
set DB_USER=hedis_api
set DB_PASSWORD=hedis_password
set DB_PORT=5432

# Run validation
psql -h %DB_HOST% -p %DB_PORT% -U %DB_USER% -d %DB_NAME% -f validate_full_system.sql > validation_report.txt
```

#### Interactive psql Mode
```bash
psql -U your_username -d hedis_portfolio
\i validate_full_system.sql
```

### Option 2: Using Python Runner

The Python runner (`run_full_validation.py`) works but will skip `\echo` commands (psql-only). It provides a structured report.

```bash
python Artifacts\project\scripts\run_full_validation.py
```

## What Gets Validated

### Section 1: System Health Check
- Database object inventory (tables, views, functions, indexes)
- Table sizes and row counts
- Expected data volumes

### Section 2: Phase 1 Foundation
- HEDIS measures catalog completeness
- Plan configuration
- Plan performance coverage
- Member demographics quality
- Chronic condition assignment
- Revenue at risk calculations

### Section 3: Phase 2 Operations
- Member engagement scores
- Provider network coverage
- Member-provider attribution
- Provider performance metrics
- Predictive models operational status
- Early warning system

### Section 4: Data Quality
- Referential integrity checks
- Critical field completeness
- Data range validation

### Section 5: Business Logic
- Revenue calculation accuracy
- Gap closure propensity logic
- Risk stratification alignment

### Section 6: Dashboard Functionality
- All dashboard views operational
- Executive summary completeness
- Real-time operations dashboard

### Section 7: Export Readiness
- Master data export view
- Export column completeness

### Section 8: Final Summary
- Overall system status
- Key performance indicators

## Expected Results

### Pass Criteria
- **Critical Tests**: 95%+ should PASS
- **Warning Items**: Acceptable if <10% of total tests
- **Performance**: Dashboard queries <2 seconds

### Key Metrics Validated
- 10,000 member records
- 12,000-18,000 care gaps
- 500+ active providers
- 10,000 engagement scores
- 10,000 risk stratifications
- 8,000+ propensity scores
- 10,000 cost predictions
- 8,000+ priority queue items

## Output

### psql Output
When run via psql, the script produces formatted output with:
- Section headers
- Test names with ▶ indicators
- Status indicators (✓ PASS, ⚠ WARN, ✗ FAIL)
- Final summary with KPIs

### Report File
Output is saved to `validation_report.txt` in the scripts directory.

## Troubleshooting

### Connection Issues
- Verify database credentials in environment variables
- Check PostgreSQL service is running
- Ensure database exists and user has access

### Missing Tables/Views
- Run Phase 1 scripts first (Chats 1-4)
- Run Phase 2 scripts (Chats 1-4)
- Check prerequisites are met

### Unicode Errors (Windows)
- Use psql directly (batch/PowerShell scripts handle this)
- Or set console encoding: `chcp 65001`

## Next Steps

### If All Tests Pass
1. **Generate portfolio summary** - Get comprehensive statistics
2. **Build Streamlit dashboard** - Create web visualization
3. **Export one-pager** - Quick summary for sharing

### If Issues Found
1. Review any ✗ FAIL items
2. Check ⚠ WARN items for significance
3. Reply "Fix [specific issue]" for targeted help

## Files

- `validate_full_system.sql` - Main validation SQL script (psql-compatible)
- `run_validation_psql.bat` - Windows batch script runner
- `run_validation_psql.ps1` - PowerShell script runner
- `run_full_validation.py` - Python runner (limited \echo support)
- `validation_report.txt` - Generated validation report

## Notes

- The SQL script uses psql meta-commands (`\echo`) for formatted output
- These commands only work in psql, not in direct SQL execution
- For best results, use the batch/PowerShell scripts or psql directly
- Runtime: 5-7 minutes for full validation suite
