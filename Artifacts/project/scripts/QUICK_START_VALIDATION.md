# Quick Start - Full System Validation

## Run Validation via psql Command Line

### Option 1: Direct Command (Output to File)
```bash
psql -U your_username -d hedis_portfolio -f validate_full_system.sql > validation_report.txt
```

**With specific credentials:**
```bash
psql -h localhost -p 5432 -U hedis_api -d hedis_portfolio -f validate_full_system.sql > validation_report.txt
```

### Option 2: Interactive psql Mode
```bash
# Connect to database
psql -U your_username -d hedis_portfolio

# Then run:
\i validate_full_system.sql
```

### Option 3: Windows Batch Script
```batch
cd Artifacts\project\scripts
run_validation_psql.bat
```

### Option 4: PowerShell Script
```powershell
cd Artifacts\project\scripts
.\run_validation_psql.ps1
```

## Environment Variables (Optional)

Set these before running if not using defaults:
```bash
set DB_HOST=localhost
set DB_NAME=hedis_portfolio
set DB_USER=hedis_api
set DB_PASSWORD=hedis_password
set DB_PORT=5432
```

## View Results

After running, check the output:
- **Command line**: Results displayed in terminal
- **Redirected output**: Check `validation_report.txt`
- **Interactive mode**: Results displayed in psql session

## Expected Runtime

5-7 minutes for complete validation suite

## What You'll See

- Section headers with test names
- Status indicators: ✓ PASS, ⚠ WARN, ✗ FAIL
- Summary statistics
- Key performance indicators
- Final system status

## Troubleshooting

**Connection refused?**
- Check PostgreSQL is running
- Verify host/port settings

**Permission denied?**
- Check database user has SELECT permissions
- Verify database name is correct

**File not found?**
- Ensure you're in the `Artifacts\project\scripts` directory
- Or use full path: `-f C:\full\path\to\validate_full_system.sql`

