# Comprehensive ROI Calculator Guide

## Overview

The Comprehensive ROI Calculator provides detailed financial analysis for HEDIS intervention programs, including quality bonus impact, Star Rating financial implications, intervention costs, and net ROI calculations with confidence intervals.

## Features

- ✅ **Quality Bonus Calculation**: Impact of Star Rating improvements on quality bonuses
- ✅ **Star Rating Financial Impact**: $X per member per rating point
- ✅ **Detailed Cost Breakdown**: Staff time, outreach, lab costs
- ✅ **Net ROI Calculation**: Revenue + Quality Bonus - Total Costs
- ✅ **Confidence Intervals**: 95% CI for success rates and ROI
- ✅ **Sensitivity Analysis**: What-if scenarios for different success rates
- ✅ **CFO Report Export**: Financial justification reports (Text and Excel)
- ✅ **Mobile Summary Cards**: Quick ROI overview on mobile

## Desktop Version

### Configuration

**Quality Bonus Settings**:
- Quality Bonus per Member per Star: Default $50
- Members per Measure: Default 1,000
- Revenue per Closure: Default $100

**Cost Settings**:
- Staff Cost per Hour: Default $75
- Outreach Cost per Member: Default $15
- Lab Cost per Test: Default $25

**Statistical Settings**:
- Confidence Level: Default 95% (80-99% range)

### ROI Calculation

**Revenue Components**:
1. **Revenue from Closures**: Successful closures × $100 per closure
2. **Quality Bonus Impact**: Star Rating × Members × Bonus per Star

**Cost Components**:
1. **Staff Costs**: Interventions × 0.5 hours × $75/hour
2. **Outreach Costs**: Interventions × $15 per member
3. **Lab Costs**: (Interventions × 0.5) × $25 per test
4. **Intervention Costs**: Actual intervention costs from database

**Net ROI**:
- Total Benefit = Revenue + Quality Bonus
- Net ROI = Total Benefit - Total Costs
- ROI Ratio = Total Benefit / Total Costs

### Confidence Intervals

**Success Rate CI**:
- Uses Wilson score interval (binomial distribution)
- 95% confidence level (configurable)
- Accounts for sample size

**ROI CI**:
- Derived from success rate CI
- Estimates revenue range based on success rate range
- Calculates net ROI range

### Sensitivity Analysis

**What-If Scenarios**:
- Adjust success rate to see impact
- Example: "If closure rate is 85% instead of 93%..."
- Compare multiple scenarios side-by-side
- Visual comparison charts

**Scenario Types**:
- Lower success rate (pessimistic)
- Current success rate (baseline)
- Higher success rate (optimistic)

### CFO Report Export

**Report Contents**:
- Executive summary
- Portfolio overview
- Measure-by-measure ROI analysis
- Cost breakdowns
- Key assumptions
- Recommendations

**Export Formats**:
- **Text Report**: Human-readable format
- **Excel Report**: Multi-sheet workbook with:
  - ROI Summary
  - Cost Breakdown
  - Detailed metrics

## Mobile Version

### Quick ROI Summary Cards

**Features**:
- Simplified configuration
- Single measure analysis
- Key metrics display
- Cost breakdown table
- Simple visualization
- Confidence intervals

**Metrics Shown**:
- Success Rate with CI
- Star Rating
- Revenue
- Quality Bonus
- Net ROI with CI
- ROI Ratio

## Calculations Explained

### Star Rating Estimation

Simplified model:
- 95%+ success rate = 5 stars
- 90-94% = 4 stars
- 85-89% = 3 stars
- <85% = 2 stars

### Quality Bonus

Formula:
```
Quality Bonus = Star Rating × Members per Measure × Bonus per Star
```

Example:
- 4 stars × 1,000 members × $50 = $200,000

### Cost Breakdown

**Staff Costs**:
```
Staff Cost = Total Interventions × 0.5 hours × $75/hour
```

**Outreach Costs**:
```
Outreach Cost = Total Interventions × $15
```

**Lab Costs**:
```
Lab Cost = (Total Interventions × 0.5) × $25
```

**Total Costs**:
```
Total Costs = Staff + Outreach + Lab + Intervention Costs
```

### Net ROI

```
Total Benefit = Revenue from Closures + Quality Bonus
Net ROI = Total Benefit - Total Costs
ROI Ratio = Total Benefit / Total Costs
```

## Best Practices

### Configuration

1. **Adjust for Your Organization**: Update cost assumptions to match your rates
2. **Set Realistic Bonuses**: Base quality bonus on actual CMS rates
3. **Review Regularly**: Update assumptions quarterly
4. **Document Changes**: Keep track of assumption changes

### Analysis

1. **Review Confidence Intervals**: Understand uncertainty in estimates
2. **Use Sensitivity Analysis**: Test different scenarios
3. **Compare Measures**: Identify high-ROI opportunities
4. **Track Over Time**: Monitor ROI trends

### Reporting

1. **Export Regularly**: Generate CFO reports quarterly
2. **Include Assumptions**: Always document assumptions
3. **Highlight Key Findings**: Emphasize important metrics
4. **Provide Context**: Explain methodology

## Troubleshooting

### "ROI seems too high/low"
- Check cost assumptions match reality
- Verify quality bonus rates
- Review success rate calculations
- Check date range includes complete data

### "Confidence intervals too wide"
- Need more interventions for narrower CI
- Check data quality
- Review success rate variability

### "Star Rating seems wrong"
- Verify success rate calculation
- Check Star Rating estimation model
- Adjust thresholds if needed

### "Export not working"
- Check openpyxl installed for Excel export
- Verify file permissions
- Try text export as alternative

## Technical Details

### Confidence Interval Method

Uses Wilson score interval for binomial proportion:
- More accurate than normal approximation
- Works well for small samples
- Accounts for sample size

### Cost Assumptions

Default assumptions based on industry standards:
- Staff: $75/hour (care coordinator)
- Outreach: $15/member (phone, mail, digital)
- Labs: $25/test (average lab cost)

Adjust based on your organization's actual costs.

### Quality Bonus Rates

Default: $50 per member per star rating point
- Based on CMS quality bonus structure
- Varies by plan size and region
- Update to match your contract terms

## Advanced Usage

### Custom Calculations

```python
from utils.roi_calculator import ROICalculator

calculator = ROICalculator()

# Custom configuration
config = {
    "quality_bonus_per_member_per_star": 60.0,
    "members_per_measure": 1500,
    "revenue_per_closure": 120.0,
    "confidence_level": 0.99
}

# Calculate ROI
roi = calculator.calculate_measure_roi(
    measure_id="HBA1C",
    start_date="2024-01-01",
    end_date="2024-12-31",
    config=config
)

# Sensitivity analysis
scenarios = [
    {"name": "Pessimistic", "success_rate": 80},
    {"name": "Optimistic", "success_rate": 95}
]
sensitivity = calculator.sensitivity_analysis(roi, scenarios)
```

### Integration Ideas

- **Automated Reports**: Generate CFO reports monthly
- **Dashboard Widgets**: Display key ROI metrics
- **Alert Integration**: Trigger alerts for negative ROI
- **API Endpoints**: Expose ROI calculations via API
- **Historical Tracking**: Track ROI trends over time

## Support

For questions or issues:
- 📧 **Email**: reichert.starguardai@gmail.com
- 🔗 **LinkedIn**: [sentinel-analytics](https://www.linkedin.com/in/sentinel-analytics/)
- 💻 **GitHub**: [HEDIS-MA-Top-12-w-HEI-Prep](https://github.com/StarGuardAi/HEDIS-MA-Top-12-w-HEI-Prep/blob/main/README.md)
- 🎨 **Portfolio**: [Canva Portfolio](https://www.canva.com/design/DAG2WzhiLwM/N_iXUe3eEKL3dzQ2M_0PgQ/edit)

---

**Comprehensive ROI Calculator** | Part of HEDIS Portfolio Optimizer | Financial Justification for Interventions

