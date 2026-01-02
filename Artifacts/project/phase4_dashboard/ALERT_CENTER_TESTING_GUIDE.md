# 🔔 Alert Center - Testing Guide

## How the Alert Center Works

The Alert Center generates intelligent alerts by analyzing your HEDIS portfolio data. It checks for:

1. **Star Rating Risks** - Measures trending below threshold (default: 85%)
2. **Opportunities** - High-value members identified (default: $10,000+)
3. **Deadlines** - Interventions due within timeframe (default: 30 days)
4. **Performance Anomalies** - Significant changes in closure rates (default: 15% change)

## How to Test

### Step 1: Check Database Data
The Alert Center needs data in your database to generate alerts. Verify:

1. **Navigate to any page with data** (like Portfolio Overview)
2. **Check if you have intervention data** in the database
3. **Verify date ranges** - alerts use last 90 days by default

### Step 2: Generate Alerts

1. **Go to Alert Center**: http://localhost:8501/Alert_Center
2. **Click "🔄 Generate Alerts"** button
3. **Wait for processing** - it will show "Analyzing portfolio..."
4. **Check results** - should show "Generated X alerts" message

### Step 3: Understand Results

**If you see "Generated 0 alerts":**

This is **NORMAL** if:
- ✅ No measures are below the star rating threshold
- ✅ No high-value opportunities meet the criteria
- ✅ No deadlines within the timeframe
- ✅ No performance anomalies detected

**To get alerts, you need:**

1. **Star Rating Risks**:
   - Measures with success rate < threshold (default 85%)
   - At least 10 interventions in the period

2. **Opportunities**:
   - Pending/scheduled interventions
   - Potential revenue >= $10,000 (default)
   - Within date range

3. **Deadlines**:
   - Interventions due within 30 days (default)
   - Status = 'pending' or 'scheduled'
   - At least 10 interventions

4. **Performance Anomalies**:
   - Closure rate change >= 15% (default)
   - Comparing current vs previous period

### Step 4: Adjust Thresholds (Optional)

To generate more alerts, adjust thresholds in the sidebar:

1. **Open "⚙️ Alert Configuration"** expander
2. **Lower thresholds** to be more sensitive:
   - Star Rating Threshold: Try 90% (more alerts)
   - Opportunity Value: Try $5,000 (more alerts)
   - Deadline Days: Try 60 days (more alerts)
   - Anomaly Threshold: Try 5% (more alerts)
3. **Click "💾 Save Configuration"**
4. **Click "🔄 Generate Alerts"** again

## Testing Checklist

- [ ] Alert Center page loads without errors
- [ ] "Generate Alerts" button works
- [ ] No error messages appear
- [ ] Statistics show correctly (even if 0)
- [ ] Filters work (Type, Priority, Unread Only)
- [ ] Mark All Read button works
- [ ] Clear All button works
- [ ] Alert cards display properly (if alerts exist)

## Expected Behavior

### With No Data
- Shows "Generated 0 alerts"
- Shows "No alerts generated yet" message
- Statistics all show 0
- This is **normal and expected** with no matching data

### With Data
- Shows number of alerts generated
- Displays alert cards with priority colors
- Shows statistics breakdown
- Allows filtering and management

## Troubleshooting

### If "Generate Alerts" button doesn't work:
1. Check browser console for errors
2. Verify database connection (check other pages)
3. Look for error messages on the page

### If you want to test with alerts:
1. Use the Scenario Modeler to create test scenarios
2. Lower all thresholds in configuration
3. Ensure you have intervention data in the database

### If alerts don't appear:
1. Check if alert types are enabled (checkboxes in sidebar)
2. Verify database has data for the date range
3. Try adjusting thresholds to be more sensitive
4. Check that interventions have status 'pending' or 'scheduled'

## Is the Page Working?

**YES** - The page is working correctly if:
- ✅ Page loads without errors
- ✅ "Generate Alerts" button responds
- ✅ Shows "Generated X alerts" message (even if X=0)
- ✅ No error messages appear
- ✅ Statistics display (even if all zeros)

**"0 alerts" is normal** - It means no conditions were met that require alerts. This is actually a **good sign** - it means your portfolio is performing well!

## Next Steps

If you want to see alerts in action:
1. Create test scenarios with lower performance
2. Add test interventions with future due dates
3. Lower alert thresholds
4. Generate alerts again

The Alert Center is **working correctly** - it's just waiting for conditions that require alerts!









