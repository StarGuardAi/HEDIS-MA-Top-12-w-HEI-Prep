# Competitive Benchmarking Analysis Guide

## Overview

The Competitive Benchmarking module provides comprehensive performance comparison against multiple data sources:

- **CMS Star Ratings** - Public Medicare Advantage star rating data
- **HEDIS Benchmarks** - National percentile rankings (10th, 25th, 50th, 75th, 90th, 95th)
- **Regional Performance** - State-level and market-specific comparisons
- **NQF Standards** - National Quality Forum target rates
- **Similar Plans** - Size and model-type comparisons

## Features

### 1. National Comparison

Compare your plan's performance against national percentiles:

- **Percentile Rankings**: See where you rank for each measure
- **Gap Analysis**: Calculate distance to 90th percentile
- **Benchmark Bands**: Visual representation of performance tiers
- **Performance Distribution**: See your position in the market curve

**Key Metrics:**
- Current rate vs national percentiles
- Percentile ranking (10th, 25th, 50th, 75th, 90th, 95th)
- Gap to top performers
- Above/below median status

### 2. Regional Comparison

Compare against state and regional benchmarks:

- **State-Level Analysis**: Compare to your state's average
- **Market Position**: Identify regional leadership opportunities
- **Geographic Insights**: Understand regional variations

**Key Metrics:**
- Plan rate vs regional average
- Percent difference from regional
- Measures above/below regional
- Top/bottom performers in region

### 3. Similar Plans Comparison

Compare against plans with similar characteristics:

- **Size-Based**: Compare to similar-sized plans
- **Model-Type**: Compare HMO vs PPO vs other models
- **Market Segment**: Compare within your market segment

**Key Metrics:**
- Plan rate vs similar size plans
- Plan rate vs similar type plans
- Average benchmark comparison
- Competitive positioning

### 4. Year-over-Year Analysis

Track performance trends over time:

- **Improvement Tracking**: Identify improving measures
- **Decline Detection**: Flag declining performance
- **Trend Analysis**: Understand trajectory

**Key Metrics:**
- Current vs previous year rates
- Absolute and percent change
- Improving vs declining measures
- Net change across all measures

## Visualizations

### Radar Charts

Multi-measure comparison showing:
- Your plan's performance across all measures
- Benchmark performance (national, regional, or similar plans)
- Visual gap identification

**Use Cases:**
- Quick overview of overall performance
- Identify measure clusters
- Compare across different benchmark types

### Benchmark Bands

Visual representation of percentile tiers:
- Color-coded bands for each percentile
- Your plan's position marked
- Easy identification of performance tier

**Use Cases:**
- Detailed measure analysis
- Understanding performance distribution
- Setting improvement targets

### Performance Distribution Curves

Market distribution visualization:
- Normal distribution of plan performance
- Your plan's position on the curve
- Percentile markers (50th, 75th, 90th)

**Use Cases:**
- Understanding market dynamics
- Identifying competitive position
- Setting realistic targets

### Market Share vs Quality Scatter

Positioning in the market landscape:
- Market share on x-axis
- Quality score on y-axis
- Your plan highlighted

**Use Cases:**
- Strategic positioning
- Competitive analysis
- Market opportunity identification

## Insights Generation

The system automatically generates actionable insights:

### Insight Types

1. **National Ranking Insights**
   - "You rank 45th percentile nationally on HbA1c"
   - Identifies measures below median
   - Calculates gap to top performers

2. **Regional Leadership**
   - "You lead your region in Breast Cancer Screening"
   - Highlights competitive advantages
   - Identifies areas of strength

3. **Improvement Opportunities**
   - "Improving BP Control by 3% would move you to top quartile"
   - Quantifies improvement needed
   - Sets clear targets

4. **Declining Performance Alerts**
   - "HbA1c Testing declined by 2.5% year-over-year"
   - Flags concerning trends
   - Requires investigation

### Insight Severity Levels

- **High**: Critical issues requiring immediate attention
- **Medium**: Important opportunities for improvement
- **Low**: Positive findings or minor opportunities

## Desktop Version

### Navigation

Access via: **📊 Competitive Benchmarking** page

### Layout

1. **Summary Overview**
   - Key metrics at a glance
   - Average national percentile
   - Measures above regional
   - Improving measures count
   - Bottom quartile alerts

2. **Key Insights Section**
   - Top 5 actionable insights
   - Severity indicators
   - Expandable details

3. **Comparison Tabs**
   - National Comparison
   - Regional Comparison
   - Similar Plans
   - Year-over-Year

4. **Visualizations**
   - Radar charts
   - Benchmark bands
   - Distribution curves
   - Market share scatter

5. **Export Options**
   - National rankings CSV
   - Regional comparison CSV
   - YoY trends CSV

### Usage Workflow

1. **Review Summary**: Check overall performance
2. **Read Insights**: Understand key findings
3. **Explore Comparisons**: Dive into specific comparisons
4. **Analyze Visualizations**: Identify patterns
5. **Export Data**: Download for further analysis

## Mobile Version

### Simplified Interface

Optimized for mobile devices with:

- **Quick Overview Cards**: Key metrics at a glance
- **Top 3 Insights**: Most important findings
- **Simplified Charts**: Touch-optimized visualizations
- **Top/Bottom Lists**: Quick performance highlights

### Mobile Features

1. **National Tab**
   - Top 5 and Bottom 5 measures
   - Simplified radar chart
   - Percentile rankings

2. **Regional Tab**
   - Top 3 and Bottom 3 vs regional
   - Regional comparison summary

3. **YoY Tab**
   - Top 3 improvements
   - Top 3 declines
   - Simple bar chart

## Data Sources

### CMS Star Ratings

- Public Medicare Advantage data
- Updated annually
- Includes all MA plans
- Star rating methodology

### HEDIS Benchmarks

- National percentile data
- Updated quarterly
- Includes all reporting plans
- Measure-specific benchmarks

### Regional Data

- State-level aggregations
- Market-specific data
- Geographic variations
- Updated quarterly

### NQF Standards

- National Quality Forum targets
- Evidence-based standards
- Measure-specific goals
- Updated annually

## Implementation

### Core Module

```python
from utils.competitive_benchmarking import CompetitiveBenchmarking
from utils.database import get_db_connection

# Initialize
db = get_db_connection()
benchmarking = CompetitiveBenchmarking(db_connection=db)

# Get national ranking
ranking = benchmarking.get_national_ranking('HbA1c Testing')
print(f"Percentile: {ranking['percentile']}th")
print(f"Gap to 90th: {ranking['gap_to_90th']:.1f}%")

# Get regional comparison
regional = benchmarking.get_regional_comparison('CA')
print(f"Measures above regional: {regional['measures_above']}")

# Get YoY trends
yoy = benchmarking.get_year_over_year()
print(f"Improving measures: {yoy['improving_measures']}")

# Generate insights
insights = benchmarking.generate_insights()
for insight in insights:
    print(f"{insight['message']}: {insight['action']}")
```

### Visualizations

```python
# Radar chart
radar_fig = benchmarking.create_radar_chart(comparison_type='national')
st.plotly_chart(radar_fig)

# Benchmark bands
bands_fig = benchmarking.create_benchmark_bands_chart('HbA1c Testing')
st.plotly_chart(bands_fig)

# Performance distribution
dist_fig = benchmarking.create_performance_distribution('HbA1c Testing')
st.plotly_chart(dist_fig)

# Market share scatter
market_fig = benchmarking.create_market_share_scatter()
st.plotly_chart(market_fig)
```

## Best Practices

### 1. Regular Monitoring

- Review benchmarks monthly
- Track YoY trends quarterly
- Update targets annually

### 2. Prioritization

- Focus on bottom quartile measures
- Target high-impact improvements
- Maintain regional leadership

### 3. Action Planning

- Use insights to set priorities
- Calculate improvement targets
- Track progress against benchmarks

### 4. Communication

- Share insights with stakeholders
- Use visualizations in presentations
- Export data for detailed analysis

## Troubleshooting

### Data Not Loading

- Check database connection
- Verify benchmark data availability
- Review data source configuration

### Rankings Seem Incorrect

- Verify current plan data
- Check benchmark data freshness
- Review calculation methodology

### Visualizations Not Displaying

- Check Plotly installation
- Verify data format
- Review browser compatibility

## Advanced Usage

### Custom Benchmarks

```python
# Add custom benchmark data
custom_benchmarks = {
    'national': {
        '90th': {'HbA1c Testing': 85.0},
        # ... other percentiles
    }
}
benchmarking.benchmark_data.update(custom_benchmarks)
```

### Filtered Comparisons

```python
# Compare specific measures
selected_measures = ['HbA1c Testing', 'Blood Pressure Control']
filtered_rankings = [
    benchmarking.get_national_ranking(m) 
    for m in selected_measures
]
```

### Trend Analysis

```python
# Multi-year trend
years = [2022, 2023, 2024]
trends = {}
for year in years:
    # Load data for year
    yoy = benchmarking.get_year_over_year()
    trends[year] = yoy['net_change']
```

## Integration Ideas

### Dashboard Widgets

- Add benchmark summary to main dashboard
- Include top insights in executive summary
- Show YoY trends in measure pages

### Automated Reports

- Weekly benchmark updates
- Monthly regional comparisons
- Quarterly national rankings

### Alerts

- Notify when dropping below percentile thresholds
- Alert on declining YoY trends
- Flag regional position changes

## Support

For questions or issues:
- 📧 **Email**: reichert.starguardai@gmail.com
- 🔗 **LinkedIn**: [sentinel-analytics](https://www.linkedin.com/in/sentinel-analytics/)
- 💻 **GitHub**: [HEDIS-MA-Top-12-w-HEI-Prep](https://github.com/StarGuardAi/HEDIS-MA-Top-12-w-HEI-Prep/blob/main/README.md)
- 🎨 **Portfolio**: [Canva Portfolio](https://www.canva.com/design/DAG2WzhiLwM/N_iXUe3eEKL3dzQ2M_0PgQ/edit)

---

**Competitive Benchmarking** | Comprehensive performance comparison | Data-driven insights

