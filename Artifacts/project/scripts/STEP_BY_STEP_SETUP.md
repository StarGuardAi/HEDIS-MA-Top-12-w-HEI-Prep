# Step-by-Step Phase 1 Setup Guide

## 🎯 Goal
Set up the HEDIS Portfolio Optimizer database with 10,000 members and complete analytics.

---

## STEP 1: Check Prerequisites

### 1.1 Verify Python is Installed
```cmd
python --version
```
**Expected:** Python 3.8 or higher  
**If error:** Install Python from python.org

### 1.2 Verify psycopg2 is Installed
```cmd
python -c "import psycopg2; print('psycopg2 installed')"
```
**Expected:** "psycopg2 installed"  
**If error:** Run `pip install psycopg2-binary`

### 1.3 Check Current Directory
```cmd
cd
```
**Expected:** Should be in project root  
**If not:** Navigate to: `C:\Users\reich\Projects\HEDIS-MA-Top-12-w-HEI-Prep`

---

## STEP 2: Choose Your PostgreSQL Option

### Option A: Docker Desktop (Easiest - Recommended)
**Go to STEP 3A**

### Option B: Existing PostgreSQL Installation
**Go to STEP 3B**

---

## STEP 3A: Docker Desktop Setup (Option A)

### 3A.1 Open Docker Desktop
1. Press `Windows Key`
2. Type "Docker Desktop"
3. Click "Docker Desktop" application
4. **Wait 1-2 minutes** for Docker to fully start

### 3A.2 Verify Docker is Running
```cmd
docker ps
```
**Expected:** No errors (may show empty list or running containers)  
**If error:** Docker Desktop is not running - wait longer or restart Docker Desktop

### 3A.3 Navigate to Scripts Directory
```cmd
cd Artifacts\project\scripts
```

### 3A.4 Run Docker Setup
```cmd
python setup_with_docker.py
```
**OR use batch file:**
```cmd
setup_with_docker.bat
```

**What this does:**
- Starts PostgreSQL in Docker container
- Creates database `hedis_portfolio`
- Creates user `hedis_api`
- Runs all Phase 1 scripts automatically

**Expected output:**
```
Starting Docker containers...
[OK] PostgreSQL container started
[OK] Database connection established
[OK] Phase 1 Chat 1: Foundation - Completed
[OK] Phase 1 Chat 2: Velocity Tracking - Completed
[OK] Phase 1 Chat 3: ROI Analysis - Completed
[OK] Phase 1 Chat 4: 10K Scale Enhancement - Completed
[SUCCESS] PHASE 1 COMPLETE!
```

**Time:** 15-20 minutes

### 3A.5 Skip to STEP 4 (Validation)

---

## STEP 3B: Existing PostgreSQL Setup (Option B)

### 3B.1 Check if PostgreSQL Service is Running
```cmd
Get-Service | Where-Object {$_.Name -like "*postgres*"}
```
**Expected:** Service exists and Status = "Running"  
**If not running:** Continue to 3B.2  
**If not found:** Install PostgreSQL from postgresql.org

### 3B.2 Start PostgreSQL Service (if needed)
1. Press `Windows Key + R`
2. Type `services.msc` and press Enter
3. Find service named "postgresql-x64-XX" or "PostgreSQL"
4. Right-click → **Start**
5. Wait 30 seconds

### 3B.3 Create Database and User
```cmd
psql -U postgres
```
**If prompted for password:** Enter your PostgreSQL admin password

**Then run these SQL commands:**
```sql
CREATE DATABASE hedis_portfolio;
CREATE USER hedis_api WITH PASSWORD 'hedis_password';
GRANT ALL PRIVILEGES ON DATABASE hedis_portfolio TO hedis_api;
\q
```

**Alternative (if psql not in PATH):**
- Use pgAdmin GUI
- Connect as postgres user
- Right-click Databases → Create → Database
- Name: `hedis_portfolio`
- Then create user `hedis_api` with password `hedis_password`

### 3B.4 Test Database Connection
```cmd
python -c "import psycopg2; conn = psycopg2.connect(host='localhost', database='hedis_portfolio', user='hedis_api', password='hedis_password'); print('Connected!')"
```
**Expected:** "Connected!"  
**If error:** Check database name, user, password, and service status

### 3B.5 Navigate to Scripts Directory
```cmd
cd Artifacts\project\scripts
```

### 3B.6 Run Phase 1 Setup
```cmd
python run_all_phase1.py
```
**OR use batch file:**
```cmd
run_all_phase1.bat
```

**What this does:**
- Connects to existing PostgreSQL database
- Creates all tables and schema
- Loads 12 HEDIS measures
- Generates 10,000 members
- Creates 15,000+ care gaps
- Builds all analytics views

**Expected output:**
```
[OK] Database connection established
[OK] Phase 1 Chat 1: Foundation - Completed
[OK] Phase 1 Chat 2: Velocity Tracking - Completed
[OK] Phase 1 Chat 3: ROI Analysis - Completed
[OK] Phase 1 Chat 4: 10K Scale Enhancement - Completed
[SUCCESS] PHASE 1 COMPLETE!
```

**Time:** 15-20 minutes

---

## STEP 4: Validate the Setup

### 4.1 Run Validation Script
```cmd
cd Artifacts\project\scripts
python run_validation.py
```
**OR use batch file:**
```cmd
run_validation.bat
```

**Expected output:**
```
Running validation tests...
[OK] Test 1: Member Count - PASSED
[OK] Test 2: Gap Distribution - PASSED
[OK] Test 3: Revenue Calculations - PASSED
...
[SUCCESS] All validation tests passed!
```

**Time:** 2-3 minutes

### 4.2 Check Validation Results
The script will show:
- ✅ 10,000 members created
- ✅ 15,000+ gaps distributed
- ✅ All measures loaded
- ✅ Revenue calculations working
- ✅ Velocity metrics populated

---

## STEP 5: Verify Database Contents

### 5.1 Connect to Database
```cmd
psql -U hedis_api -d hedis_portfolio
```
**Password:** `hedis_password`

### 5.2 Run Quick Verification Queries

**Check member count:**
```sql
SELECT COUNT(*) FROM plan_members;
```
**Expected:** ~10,000

**Check gap count:**
```sql
SELECT COUNT(*) FROM member_gaps;
```
**Expected:** ~15,000+

**Check measures:**
```sql
SELECT COUNT(*) FROM hedis_measures;
```
**Expected:** 12

**Check plans:**
```sql
SELECT plan_id, plan_name, total_enrollment FROM ma_plans;
```
**Expected:** 3 plans

**Exit:**
```sql
\q
```

---

## STEP 6: Test Analytics Views

### 6.1 Test Revenue at Risk View
```cmd
psql -U hedis_api -d hedis_portfolio -c "SELECT plan_id, COUNT(*) as measures_at_risk, SUM(revenue_at_risk) as total_revenue FROM vw_revenue_at_risk GROUP BY plan_id;"
```

### 6.2 Test Velocity Metrics
```cmd
psql -U hedis_api -d hedis_portfolio -c "SELECT plan_id, measure_id, velocity_score FROM vw_current_velocity LIMIT 10;"
```

### 6.3 Test ROI Analysis
```cmd
psql -U hedis_api -d hedis_portfolio -c "SELECT plan_id, measure_id, cost_per_gap_closed, roi_ratio FROM vw_cost_per_closure LIMIT 10;"
```

---

## STEP 7: Troubleshooting

### Problem: "Connection refused"
**Solution:**
- Docker Desktop not running → Start Docker Desktop
- PostgreSQL service not running → Start service in Services
- Wrong port → Check if PostgreSQL is on port 5432

### Problem: "Database does not exist"
**Solution:**
- Run STEP 3B.3 to create database
- Or use Docker setup (STEP 3A) which creates it automatically

### Problem: "Permission denied"
**Solution:**
- Check user has privileges: `GRANT ALL PRIVILEGES ON DATABASE hedis_portfolio TO hedis_api;`
- Or use Docker setup which handles permissions automatically

### Problem: "Script fails at Chat 2/3/4"
**Solution:**
- Ensure previous chats completed successfully
- Check database connection is still active
- Review error messages for specific table/view issues

### Problem: "Validation fails"
**Solution:**
- Ensure all Phase 1 scripts completed
- Check member and gap counts are reasonable
- Review validation output for specific failures

---

## STEP 8: Success Indicators

### ✅ You're Done When:

1. **All Phase 1 scripts completed** without errors
2. **Validation passes** all tests
3. **Database contains:**
   - 12 HEDIS measures
   - 3 MA plans
   - ~10,000 members
   - ~15,000+ care gaps
   - All analytics views created

4. **You can query:**
   - `vw_revenue_at_risk`
   - `vw_current_velocity`
   - `vw_cost_per_closure`
   - `vw_portfolio_roi`

---

## 📋 Quick Reference Commands

### Start Everything (Docker)
```cmd
cd Artifacts\project\scripts
setup_with_docker.bat
```

### Start Everything (Existing PostgreSQL)
```cmd
cd Artifacts\project\scripts
run_all_phase1.bat
```

### Validate Setup
```cmd
cd Artifacts\project\scripts
run_validation.bat
```

### Connect to Database
```cmd
psql -U hedis_api -d hedis_portfolio
```

### Check Docker Status
```cmd
docker ps
```

### Check PostgreSQL Service
```cmd
Get-Service | Where-Object {$_.Name -like "*postgres*"}
```

---

## ⏱️ Estimated Timeline

- **Step 1 (Prerequisites):** 2 minutes
- **Step 2 (Choose Option):** 1 minute
- **Step 3A (Docker Setup):** 20 minutes
- **Step 3B (PostgreSQL Setup):** 25 minutes
- **Step 4 (Validation):** 3 minutes
- **Step 5-6 (Verification):** 5 minutes

**Total Time:** ~30-35 minutes

---

## 🎉 Next Steps After Phase 1

Once Phase 1 is complete, you can:
1. **Integrate with Streamlit** dashboard
2. **Build Phase 2** operational metrics
3. **Query the database** for analytics
4. **Export data** for reporting

See `NEXT_STEPS_GUIDE.md` for details.

---

## 📞 Still Need Help?

Check these files:
- `STATUS_AND_ACTION_REQUIRED.md` - Current status
- `MASTER_SETUP_GUIDE.md` - Comprehensive guide
- `QUICK_START_GUIDE.md` - Quick reference

**Ready to start? Begin with STEP 1!** 🚀

