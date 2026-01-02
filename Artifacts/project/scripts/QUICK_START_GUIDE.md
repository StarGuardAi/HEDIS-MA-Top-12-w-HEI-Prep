# Quick Start Guide - Phase 1 Database Setup

## 🚀 Three Ways to Run Phase 1 Scripts

### Option 1: Docker (Easiest - Recommended)

**Prerequisites:**
- Docker Desktop installed and running
- Python 3.8+

**Steps:**
1. Start Docker Desktop (if not running)
2. Run: `setup_with_docker.bat`
3. Wait ~15-20 minutes for all scripts to complete

**What it does:**
- Automatically starts PostgreSQL in Docker
- Runs all Phase 1 scripts (1-4)
- Validates setup
- Keeps PostgreSQL running for you to use

**To stop PostgreSQL later:**
```cmd
cd Artifacts\project\scripts
docker-compose -f docker-compose-hedis.yml down
```

---

### Option 2: Existing PostgreSQL

**Prerequisites:**
- PostgreSQL 12+ installed and running
- Database and user created

**Steps:**
1. Create database (if needed):
   ```sql
   CREATE DATABASE hedis_portfolio;
   CREATE USER hedis_api WITH PASSWORD 'hedis_password';
   GRANT ALL PRIVILEGES ON DATABASE hedis_portfolio TO hedis_api;
   ```

2. Run: `run_all_phase1.bat`

**Or set custom connection:**
```cmd
set DB_HOST=your_host
set DB_PORT=your_port
set DB_NAME=your_database
set DB_USER=your_user
set DB_PASSWORD=your_password
run_all_phase1.bat
```

---

### Option 3: Manual SQL Execution

**Prerequisites:**
- PostgreSQL installed
- psql command-line tool available

**Steps:**
```bash
# Connect to database
psql -U hedis_api -d hedis_portfolio

# Run scripts in order:
\i phase1_chat1_foundation.sql
\i phase1_chat2_velocity_tracking.sql
\i phase1_chat3_roi_analysis.sql
\i phase1_chat4_10k_scale_enhancement.sql
```

---

## 📋 Current Status

✅ **All scripts created and ready**
- Phase 1 Chat 1: Foundation
- Phase 1 Chat 2: Velocity Tracking  
- Phase 1 Chat 3: ROI Analysis
- Phase 1 Chat 4: 10K Scale Enhancement
- Validation Suite

❌ **PostgreSQL not currently available**
- Docker Desktop not running, OR
- PostgreSQL service not running

---

## 🔧 Troubleshooting

### "Docker Desktop not running"
- **Solution**: Start Docker Desktop application
- Wait for it to fully start (whale icon in system tray)
- Then run `setup_with_docker.bat` again

### "Connection refused"
- **Solution**: Start PostgreSQL service
- Windows: Services → PostgreSQL → Start
- Or use Docker option above

### "Database does not exist"
- **Solution**: Create database first (see Option 2 above)

### "Permission denied"
- **Solution**: Grant privileges to user:
  ```sql
  GRANT ALL PRIVILEGES ON DATABASE hedis_portfolio TO hedis_api;
  GRANT ALL ON SCHEMA public TO hedis_api;
  ```

---

## ✅ After Setup Completes

1. **Run Validation:**
   ```cmd
   run_validation.bat
   ```

2. **Verify Data:**
   ```sql
   SELECT COUNT(*) FROM plan_members WHERE member_id LIKE 'M%';
   -- Should return 10,000
   
   SELECT COUNT(*) FROM member_gaps WHERE member_id LIKE 'M%';
   -- Should return 12,000-16,000
   ```

3. **Check Views:**
   ```sql
   SELECT * FROM vw_revenue_at_risk LIMIT 5;
   SELECT * FROM vw_member_segmentation LIMIT 5;
   ```

---

## 📊 What You'll Have

After successful setup:
- ✅ 10,000 members with realistic demographics
- ✅ 15,000+ care gaps across 12 HEDIS measures
- ✅ Revenue at risk calculations ($1.5M-$2M)
- ✅ ROI analysis and cost metrics
- ✅ Geographic clustering (30 zip codes)
- ✅ 11 analytics views for dashboards
- ✅ Production-ready dataset

---

## 🎯 Recommended Next Steps

1. **Start Docker Desktop** (if using Docker option)
2. **Run setup script**: `setup_with_docker.bat` or `run_all_phase1.bat`
3. **Wait for completion** (~15-20 minutes)
4. **Run validation**: `run_validation.bat`
5. **Proceed to Phase 2** for operational dashboards

---

**Need Help?** Check `PHASE1_SETUP_COMPLETE.md` for detailed documentation.

