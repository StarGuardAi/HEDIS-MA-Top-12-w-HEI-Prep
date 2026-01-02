# Campaign Builder Guide

## Overview

The Campaign Builder allows healthcare managers to create and manage HEDIS intervention campaigns by selecting members, calculating metrics, automatically assigning care coordinators, and tracking progress.

## Features

- ✅ **Multi-Select Members**: Select members from filtered table
- ✅ **Campaign Metrics**: Calculate total value, predicted success rate, required FTEs
- ✅ **Workload Balancing**: Automatic assignment to care coordinators with balanced workloads
- ✅ **CRM Export**: Generate CSV files for CRM import
- ✅ **Call Lists**: Printable call lists (all or by coordinator)
- ✅ **Progress Dashboard**: Track campaign progress with visualizations
- ✅ **Mobile View**: View-only campaign status on mobile devices

## Desktop Version

### Building a Campaign

#### Step 1: Select Members

1. **Filter Members**:
   - Filter by measure (optional)
   - Select statuses (pending, scheduled, in_progress)
   - Set days ahead for intervention date range

2. **Select Members**:
   - Use "Select All" checkbox for bulk selection
   - Or use multi-select dropdown for individual selection
   - Selected members appear in campaign

#### Step 2: Campaign Metrics

Automatically calculated metrics:
- **Total Members**: Number of unique members selected
- **Total Value**: Predicted revenue potential
- **Predicted Success Rate**: Based on historical data
- **Predicted Closures**: Expected successful closures
- **Required FTE**: Number of coordinators needed
- **Total Cost**: Sum of intervention costs
- **Predicted Revenue**: Closures × $100 per closure
- **Net Benefit**: Revenue - Cost

#### Step 3: Configure Campaign

1. **Campaign Name**: Descriptive name for the campaign
2. **Number of Coordinators**: Adjust based on required FTE
3. **Assignment Strategy**:
   - **Balanced Workload**: Distributes members evenly
   - **Round Robin**: Simple sequential assignment
   - **Group by Measure**: Keeps measures together
4. **Target Completion Date**: When campaign should be completed

#### Step 4: Create Campaign

- Click "Create Campaign" to generate
- Campaign is created with coordinator assignments
- Ready for export and tracking

### Viewing Campaigns

Access all campaigns from the "View Campaigns" tab:

- **Campaign List**: All active campaigns
- **Campaign Details**: Metrics and status
- **Export Options**:
  - **CRM CSV**: Full member data for CRM import
  - **Call List**: Printable list for all coordinators
  - **Coordinator Call List**: Filter by specific coordinator

### Campaign Dashboard

View overall campaign statistics and progress:

- **Overall Statistics**: Total campaigns, members, value, FTEs
- **Campaign Progress**: Bar chart showing completion percentage
- **Coordinator Workload**: Distribution of members across coordinators
- **Workload Summary**: Table with member counts per coordinator

## Mobile Version

### View-Only Campaign Status

Mobile version provides read-only access to campaign information:

1. **Select Campaign**: Choose from active campaigns
2. **View Overview**: Key metrics (members, closures, value, FTE)
3. **Track Progress**: Progress bar and completion statistics
4. **Coordinator Workload**: Chart and table showing assignments
5. **Campaign Details**: Full campaign information
6. **Summary Statistics**: Additional metrics and ROI

**Note**: Campaign creation and exports are available in desktop version only.

## Assignment Strategies

### Balanced Workload (Recommended)

- Distributes members evenly across coordinators
- Minimizes workload variance
- Keeps related interventions together when possible
- Best for most scenarios

### Round Robin

- Simple sequential assignment
- Predictable distribution
- Good for uniform workloads

### Group by Measure

- Keeps all members for a measure with same coordinator
- Better for measure-specific expertise
- May create workload imbalance

## Export Formats

### CRM CSV Export

Format includes:
- Member ID
- Member Name
- Phone
- Email
- Measure
- Intervention Date
- Coordinator
- Status
- Priority

Ready for import into most CRM systems.

### Call List Export

Format includes:
- Member ID
- Member Name
- Phone
- Measure
- Intervention Date
- Status
- Notes (empty column for manual notes)

Suitable for printing or digital use.

## Metrics Explained

### Total Value
Predicted revenue potential = Predicted Closures × $100

### Predicted Success Rate
Based on historical success rate for similar interventions and measures.

### Required FTE
Calculated as: Total Interventions ÷ 50 (interventions per FTE per month)

### Predicted Closures
Total Interventions × (Predicted Success Rate / 100)

### Net Benefit
Predicted Revenue - Total Cost

## Best Practices

### Campaign Planning

1. **Start Small**: Test with smaller campaigns first
2. **Filter Effectively**: Use measure and status filters to focus
3. **Review Metrics**: Check predicted success rate before creating
4. **Balance Workload**: Use balanced assignment for fairness
5. **Set Realistic Targets**: Consider coordinator capacity

### Coordinator Assignment

1. **Match Capacity**: Ensure coordinator count matches required FTE
2. **Consider Expertise**: Use "Group by Measure" if coordinators specialize
3. **Monitor Workload**: Check dashboard for balance
4. **Adjust as Needed**: Reassign if workload becomes imbalanced

### Progress Tracking

1. **Regular Updates**: Update progress regularly
2. **Monitor Dashboard**: Watch for bottlenecks
3. **Export Regularly**: Keep call lists current
4. **Track Completion**: Use progress metrics to adjust strategy

## Troubleshooting

### "No members found"
- Check date range includes future dates
- Verify status filter includes pending/scheduled
- Ensure measure filter isn't too restrictive

### "Assignment seems unbalanced"
- Try "Balanced Workload" strategy
- Adjust coordinator count
- Check if measures are evenly distributed

### "Export not working"
- Verify campaign has member data
- Check browser download settings
- Try different export format

### "Mobile view not updating"
- Refresh the page
- Verify campaign exists
- Check campaign status

## Technical Details

### Capacity Assumptions

- **Interventions per FTE per Month**: 50
- Based on: ~2-3 interventions per day per FTE
- Adjustable in `campaign_builder.py` if needed

### Revenue Assumptions

- **Revenue per Closure**: $100
- Standard HEDIS measure revenue
- Based on Star Ratings impact

### Success Rate Calculation

Uses historical success rate from:
- Same measure types
- Similar intervention dates
- Overall portfolio average

## Advanced Usage

### Programmatic Access

The `CampaignBuilder` class can be used programmatically:

```python
from utils.campaign_builder import CampaignBuilder

builder = CampaignBuilder()

# Get available members
members = builder.get_available_members(
    measure_id="HBA1C",
    status_filter=["pending", "scheduled"]
)

# Calculate metrics
metrics = builder.calculate_campaign_metrics(member_ids)

# Create campaign
campaign = builder.create_campaign(
    name="Q1 HbA1c Campaign",
    member_ids=member_ids,
    coordinator_count=5
)
```

### Custom Assignment

Modify `campaign_builder.py` to:
- Adjust capacity assumptions
- Change assignment algorithms
- Add custom assignment rules
- Integrate with external systems

## Support

For questions or issues:
- 📧 **Email**: reichert.starguardai@gmail.com
- 🔗 **LinkedIn**: [sentinel-analytics](https://www.linkedin.com/in/sentinel-analytics/)
- 💻 **GitHub**: [HEDIS-MA-Top-12-w-HEI-Prep](https://github.com/StarGuardAi/HEDIS-MA-Top-12-w-HEI-Prep/blob/main/README.md)
- 🎨 **Portfolio**: [Canva Portfolio](https://www.canva.com/design/DAG2WzhiLwM/N_iXUe3eEKL3dzQ2M_0PgQ/edit)

---

**Campaign Builder** | Part of HEDIS Portfolio Optimizer | Built for Healthcare Managers

