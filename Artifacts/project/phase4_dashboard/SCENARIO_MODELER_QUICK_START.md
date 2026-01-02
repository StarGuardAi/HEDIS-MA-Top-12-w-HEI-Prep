# What-If Scenario Modeler - Quick Start

## 🚀 Get Started in 2 Steps

### 1. Run the Dashboard
```bash
streamlit run app.py
```

### 2. Navigate to Scenario Modeler
Click **"📊 What-If Scenario Modeler"** in the sidebar

## 📊 Desktop Version

### Quick Usage

1. **Set Baseline Period**: Choose date range for historical data
2. **Configure 3 Scenarios**:
   - Adjust budget slider ($50K - $500K)
   - Adjust FTE slider (1-10)
   - Select strategy (Balanced, High ROI, High Volume)
3. **View Results**: See real-time predictions as you adjust
4. **Compare**: Side-by-side comparison table
5. **Analyze**: Pareto frontier shows optimal trade-offs
6. **Export**: Download CSV, Excel, or text report

### Key Features

- ✅ **Real-Time Updates**: Calculations update automatically as you move sliders
- ✅ **3-Scenario Comparison**: Compare different resource allocations
- ✅ **Pareto Frontier**: Visualize optimal ROI vs volume trade-offs
- ✅ **Export Reports**: Multiple export formats available

## 📱 Mobile Version

### Quick Usage

1. **Set Baseline Period**: Quick date selection
2. **Adjust Sliders**:
   - Budget: $50K - $500K
   - FTE: 1-10 coordinators
   - Strategy: Balanced/High ROI/High Volume
3. **View Results**: Real-time metric updates
4. **Export**: Download single scenario report

### Mobile Features

- Touch-friendly sliders
- Large, readable metrics
- Simplified single scenario view
- Quick export options

## 💡 Example Scenarios

### Scenario 1: Current State
- Budget: $200K
- FTE: 4
- Strategy: Balanced

### Scenario 2: Optimistic
- Budget: $350K
- FTE: 7
- Strategy: High ROI Focus

### Scenario 3: Conservative
- Budget: $150K
- FTE: 3
- Strategy: Balanced

## 📈 Understanding Results

- **Predicted Closures**: Expected successful HEDIS closures
- **ROI Ratio**: Revenue / Cost (higher is better)
- **Net Benefit**: Revenue - Cost (profit)
- **Constraint**: Budget or Capacity limiting factor

## 🎯 Best Practices

1. **Start with Current State**: Model your current budget/FTE as baseline
2. **Model Alternatives**: Create optimistic and conservative scenarios
3. **Use Pareto Frontier**: Find optimal balance between ROI and volume
4. **Export Reports**: Share scenarios with stakeholders

## 🔧 Troubleshooting

**"No baseline data"**
- Check date range includes data
- Verify database connection

**"Excel export not working"**
- Install: `pip install openpyxl`
- Use CSV export as alternative

**"Predictions seem off"**
- Verify baseline period has sufficient data
- Check historical success rates

## 📚 More Information

See `SCENARIO_MODELER_GUIDE.md` for:
- Detailed feature explanations
- Technical assumptions
- Advanced usage
- API integration

---

**Ready to model scenarios?** Open the dashboard and navigate to the Scenario Modeler page!

