# What-If Scenario Modeler Guide

## Overview

The What-If Scenario Modeler allows healthcare managers to model different budget and FTE (Full-Time Equivalent) allocations to predict ROI impact before making decisions.

## Features

- ✅ **Budget Adjustment**: Slider from $50K to $500K
- ✅ **FTE Assignment**: Adjust care coordinators from 1-10
- ✅ **Real-Time Predictions**: See ROI impact instantly as you adjust inputs
- ✅ **3-Scenario Comparison**: Compare up to 3 scenarios side-by-side
- ✅ **Pareto Frontier**: Visualize optimal trade-offs between ROI and volume
- ✅ **Export Reports**: Download scenarios as CSV, Excel, or text reports
- ✅ **Mobile Version**: Simplified single scenario view with touch-friendly sliders

## How It Works

### Scenario Calculation

The modeler uses historical data from your HEDIS portfolio to predict outcomes:

1. **Capacity Calculation**: Each FTE can handle ~200 interventions per quarter
2. **Budget Constraint**: Total interventions limited by budget / average cost per intervention
3. **Capacity Constraint**: Total interventions limited by FTE capacity
4. **Actual Interventions**: Minimum of budget-constrained and capacity-constrained
5. **Success Rate**: Based on historical data, adjusted by strategy
6. **Revenue**: $100 per successful closure (standard HEDIS revenue)
7. **ROI**: Calculated as revenue / cost

### Strategies

- **Balanced**: Standard allocation across measures
- **High ROI Focus**: Prioritizes high-ROI measures (15% success rate boost)
- **High Volume Focus**: Maximizes intervention volume (5% success rate reduction)

## Desktop Version

### Using the Scenario Modeler

1. **Set Baseline Period**: Select date range for historical data
2. **Configure Scenarios**: Set up to 3 scenarios with:
   - Budget allocation ($50K - $500K)
   - FTE count (1-10)
   - Strategy (Balanced, High ROI, High Volume)
3. **View Results**: See predicted outcomes including:
   - Predicted interventions
   - Predicted closures
   - Predicted revenue
   - ROI ratio
   - Net benefit
   - Success rate
4. **Compare Scenarios**: Side-by-side comparison table
5. **Analyze Trade-offs**: Pareto frontier chart shows optimal configurations
6. **Export Reports**: Download detailed scenario analysis

### Key Metrics Explained

- **Predicted Interventions**: Number of interventions possible given budget and FTE constraints
- **Predicted Closures**: Expected successful closures based on historical success rate
- **Predicted Revenue**: Closures × $100 per closure
- **ROI Ratio**: Revenue / Cost (higher is better)
- **Net Benefit**: Revenue - Cost (profit)
- **Constraint**: Whether budget or capacity is limiting factor

### Pareto Frontier

The Pareto frontier shows optimal trade-offs between:
- **X-axis**: ROI Ratio (efficiency)
- **Y-axis**: Predicted Closures (volume)

Points on the frontier represent non-dominated solutions - you can't improve one metric without worsening the other.

## Mobile Version

### Simplified Interface

1. **Set Baseline Period**: Quick date selection
2. **Adjust Sliders**:
   - Budget slider ($50K - $500K)
   - FTE slider (1-10)
   - Strategy dropdown
3. **View Results**: Real-time updates as you adjust
4. **Export**: Download single scenario report

### Mobile Features

- Touch-friendly sliders
- Large, readable metrics
- Simplified visualization
- Single scenario focus
- Quick export options

## Export Options

### CSV Export
- Full scenario data in spreadsheet format
- Includes all calculated metrics
- Compatible with Excel, Google Sheets

### Excel Export
- Multi-sheet workbook
- Scenario comparison sheet
- Summary sheet with best scenarios
- Requires `openpyxl` package

### Text Report
- Human-readable format
- Scenario configuration
- Predicted outcomes
- Recommendations
- Suitable for email or documentation

## Best Practices

### Scenario Planning

1. **Start with Baseline**: Use current budget/FTE as Scenario 1
2. **Model Optimistic**: Create Scenario 2 with increased resources
3. **Model Conservative**: Create Scenario 3 with reduced resources
4. **Compare Trade-offs**: Use Pareto frontier to find optimal balance

### Interpreting Results

- **Budget Constrained**: Increase budget to maximize capacity
- **Capacity Constrained**: Add FTE to fully utilize budget
- **Low ROI**: Focus on higher-ROI measures or adjust strategy
- **High Utilization**: System is operating efficiently

### Decision Making

- **Maximize ROI**: Choose scenario with highest ROI ratio
- **Maximize Volume**: Choose scenario with most closures
- **Maximize Net Benefit**: Choose scenario with highest profit
- **Balance Approach**: Use Pareto frontier to find sweet spot

## Troubleshooting

### "No baseline data loaded"
- Check date range includes data
- Verify database connection
- Ensure Phase 3 data is loaded

### "Excel export not working"
- Install openpyxl: `pip install openpyxl`
- Check file permissions
- Try CSV export as alternative

### "Predictions seem unrealistic"
- Verify baseline period has sufficient data
- Check that historical success rates are reasonable
- Adjust strategy if needed

### "Mobile view not updating"
- Refresh the page
- Check that sliders are moving
- Verify baseline data is loaded

## Technical Details

### Capacity Assumptions

- **Interventions per FTE per Quarter**: 200
- Based on industry standard: 3-4 interventions per day per FTE
- Adjustable in `scenario_modeler.py` if needed

### Revenue Assumptions

- **Revenue per Closure**: $100
- Standard HEDIS measure revenue
- Based on Star Ratings impact

### Success Rate Adjustments

- **Balanced**: No adjustment (uses historical average)
- **High ROI**: +15% success rate (focus on proven measures)
- **High Volume**: -5% success rate (broader reach, lower precision)

## Advanced Usage

### Custom Scenarios

Modify `scenario_modeler.py` to:
- Adjust capacity assumptions
- Change revenue per closure
- Modify strategy multipliers
- Add custom constraints

### API Integration

The `ScenarioModeler` class can be used programmatically:

```python
from utils.scenario_modeler import ScenarioModeler

modeler = ScenarioModeler("2024-10-01", "2024-12-31")
scenario = modeler.calculate_scenario(budget=250000, fte_count=5, strategy="balanced")
print(scenario)
```

## Support

For questions or issues:
- 📧 **Email**: reichert.starguardai@gmail.com
- 🔗 **LinkedIn**: [sentinel-analytics](https://www.linkedin.com/in/sentinel-analytics/)
- 💻 **GitHub**: [HEDIS-MA-Top-12-w-HEI-Prep](https://github.com/StarGuardAi/HEDIS-MA-Top-12-w-HEI-Prep/blob/main/README.md)
- 🎨 **Portfolio**: [Canva Portfolio](https://www.canva.com/design/DAG2WzhiLwM/N_iXUe3eEKL3dzQ2M_0PgQ/edit)

---

**What-If Scenario Modeler** | Part of HEDIS Portfolio Optimizer | Built for Healthcare Managers

