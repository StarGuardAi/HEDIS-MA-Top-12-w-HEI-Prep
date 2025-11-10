"""
Interactive Plan Size Calculator
Generates custom financial projections for any Medicare Advantage plan size

Usage:
    python scripts/plan_size_calculator.py --members 150000
    python scripts/plan_size_calculator.py --members 75000 --output custom_plan.csv

Author: Analytics Team
Date: October 24, 2025
"""

import argparse
import pandas as pd
import numpy as np

def calculate_financials(members):
    """
    Calculate 5-year financial projections for a given plan size.
    
    Args:
        members (int): Number of MA members in the plan
        
    Returns:
        dict: Complete financial model with yearly breakdowns
    """
    
    # Scaling factors (based on empirical data from multi-size model)
    base_members = 100000
    scale_factor = members / base_members
    
    # Development costs (fixed regardless of size)
    dev_costs = 50000
    
    # Implementation costs (scales with members, but with economies of scale)
    impl_base = 970000
    impl_factor = scale_factor ** 0.85  # Sublinear scaling
    impl_costs_total = impl_base * impl_factor
    
    # Maintenance costs (scales with members)
    maint_base = 1260000
    maint_factor = scale_factor ** 0.9  # Slight economies of scale
    maint_costs_total = maint_base * maint_factor
    
    # Year-by-year breakdown
    impl_y1 = impl_costs_total * 0.31  # 31% Year 1
    impl_y2 = impl_costs_total * 0.23  # 23% Year 2
    impl_y3_5 = impl_costs_total * 0.15  # 15% Years 3-5
    
    maint_y1 = maint_costs_total * 0.17  # 17% Year 1
    maint_y2_3 = maint_costs_total * 0.24  # 24% Years 2-3
    maint_y4_5 = maint_costs_total * 0.17  # 17% Years 4-5
    
    # Revenue calculations (scales linearly with members)
    # Tier 1: Diabetes portfolio
    tier1_base = 6220000  # Base case (100K)
    tier1_total = tier1_base * scale_factor
    tier1_y1 = tier1_total * 0.11  # 11% Year 1
    tier1_y2 = tier1_total * 0.19  # 19% Year 2
    tier1_y3 = tier1_total * 0.23  # 23% Year 3
    tier1_y4 = tier1_total * 0.23  # 23% Year 4
    tier1_y5 = tier1_total * 0.24  # 24% Year 5
    
    # Tier 2: Cardiovascular portfolio
    tier2_base = 3240000
    tier2_total = tier2_base * scale_factor
    tier2_y1 = tier2_total * 0.11
    tier2_y2 = tier2_total * 0.19
    tier2_y3 = tier2_total * 0.22
    tier2_y4 = tier2_total * 0.23
    tier2_y5 = tier2_total * 0.24
    
    # Tier 3: Cancer screening
    tier3_base = 1580000
    tier3_total = tier3_base * scale_factor
    tier3_y1 = tier3_total * 0.11
    tier3_y2 = tier3_total * 0.19
    tier3_y3 = tier3_total * 0.22
    tier3_y4 = tier3_total * 0.23
    tier3_y5 = tier3_total * 0.24
    
    # HEI Protection (sublinear scaling due to risk pooling)
    hei_base = 65800000
    hei_factor = scale_factor ** 0.7  # Stronger economies of scale
    hei_total = hei_base * hei_factor
    hei_y1 = hei_total * 0.08
    hei_y2 = hei_total * 0.15
    hei_y3 = hei_total * 0.21
    hei_y4 = hei_total * 0.26
    hei_y5 = hei_total * 0.30
    
    # Build year-by-year model
    model = {
        'Year 1': {
            'Development': dev_costs,
            'Implementation': impl_y1,
            'Maintenance': maint_y1,
            'Total Costs': dev_costs + impl_y1 + maint_y1,
            'Tier 1 Revenue': tier1_y1,
            'Tier 2 Revenue': tier2_y1,
            'Tier 3 Revenue': tier3_y1,
            'HEI Protection': hei_y1,
            'Total Revenue': tier1_y1 + tier2_y1 + tier3_y1 + hei_y1,
            'Net Benefit': (tier1_y1 + tier2_y1 + tier3_y1 + hei_y1) - (dev_costs + impl_y1 + maint_y1)
        },
        'Year 2': {
            'Development': 0,
            'Implementation': impl_y2,
            'Maintenance': maint_y2_3,
            'Total Costs': impl_y2 + maint_y2_3,
            'Tier 1 Revenue': tier1_y2,
            'Tier 2 Revenue': tier2_y2,
            'Tier 3 Revenue': tier3_y2,
            'HEI Protection': hei_y2,
            'Total Revenue': tier1_y2 + tier2_y2 + tier3_y2 + hei_y2,
            'Net Benefit': (tier1_y2 + tier2_y2 + tier3_y2 + hei_y2) - (impl_y2 + maint_y2_3)
        },
        'Year 3': {
            'Development': 0,
            'Implementation': impl_y3_5,
            'Maintenance': maint_y2_3,
            'Total Costs': impl_y3_5 + maint_y2_3,
            'Tier 1 Revenue': tier1_y3,
            'Tier 2 Revenue': tier2_y3,
            'Tier 3 Revenue': tier3_y3,
            'HEI Protection': hei_y3,
            'Total Revenue': tier1_y3 + tier2_y3 + tier3_y3 + hei_y3,
            'Net Benefit': (tier1_y3 + tier2_y3 + tier3_y3 + hei_y3) - (impl_y3_5 + maint_y2_3)
        },
        'Year 4': {
            'Development': 0,
            'Implementation': impl_y3_5,
            'Maintenance': maint_y4_5,
            'Total Costs': impl_y3_5 + maint_y4_5,
            'Tier 1 Revenue': tier1_y4,
            'Tier 2 Revenue': tier2_y4,
            'Tier 3 Revenue': tier3_y4,
            'HEI Protection': hei_y4,
            'Total Revenue': tier1_y4 + tier2_y4 + tier3_y4 + hei_y4,
            'Net Benefit': (tier1_y4 + tier2_y4 + tier3_y4 + hei_y4) - (impl_y3_5 + maint_y4_5)
        },
        'Year 5': {
            'Development': 0,
            'Implementation': impl_y3_5,
            'Maintenance': maint_y4_5,
            'Total Costs': impl_y3_5 + maint_y4_5,
            'Tier 1 Revenue': tier1_y5,
            'Tier 2 Revenue': tier2_y5,
            'Tier 3 Revenue': tier3_y5,
            'HEI Protection': hei_y5,
            'Total Revenue': tier1_y5 + tier2_y5 + tier3_y5 + hei_y5,
            'Net Benefit': (tier1_y5 + tier2_y5 + tier3_y5 + hei_y5) - (impl_y3_5 + maint_y4_5)
        }
    }
    
    # Calculate totals
    total_costs = sum(year['Total Costs'] for year in model.values())
    total_revenue = sum(year['Total Revenue'] for year in model.values())
    total_net = sum(year['Net Benefit'] for year in model.values())
    roi = (total_net / total_costs) * 100 if total_costs > 0 else 0
    
    # Add summary
    model['5-Year Total'] = {
        'Development': dev_costs,
        'Implementation': impl_costs_total,
        'Maintenance': maint_costs_total,
        'Total Costs': total_costs,
        'Tier 1 Revenue': tier1_total,
        'Tier 2 Revenue': tier2_total,
        'Tier 3 Revenue': tier3_total,
        'HEI Protection': hei_total,
        'Total Revenue': total_revenue,
        'Net Benefit': total_net
    }
    
    # Add cumulative metrics
    cumulative_net = 0
    for year in ['Year 1', 'Year 2', 'Year 3', 'Year 4', 'Year 5']:
        cumulative_net += model[year]['Net Benefit']
        model[year]['Cumulative Net'] = cumulative_net
    
    # Add metadata
    model['Metadata'] = {
        'Plan Members': members,
        'ROI': roi,
        'Payback Period': 'Immediate (Year 1)' if model['Year 1']['Net Benefit'] > 0 else 'N/A',
        'Annual Value at Maturity': model['Year 5']['Total Revenue'],
        'Per-Member Annual Value': model['Year 5']['Total Revenue'] / members if members > 0 else 0,
        'Per-Member Annual Cost': model['Year 5']['Total Costs'] / members if members > 0 else 0
    }
    
    return model

def format_currency(value):
    """Format value as currency."""
    if value >= 1000000:
        return f"${value/1000000:.2f}M"
    elif value >= 1000:
        return f"${value/1000:.1f}K"
    else:
        return f"${value:.0f}"

def print_summary(model, members):
    """Print executive summary to console."""
    print("\n" + "=" * 80)
    print(f"FINANCIAL PROJECTION - {members:,} MEMBER MA PLAN")
    print("=" * 80)
    print(f"\nPlan Size: {members:,} members")
    print(f"Projection Period: 5 years (2025-2029)")
    print("\n" + "-" * 80)
    print("5-YEAR SUMMARY")
    print("-" * 80)
    
    total = model['5-Year Total']
    meta = model['Metadata']
    
    print(f"\nTotal Investment:     {format_currency(total['Total Costs'])}")
    print(f"  - Development:      {format_currency(total['Development'])}")
    print(f"  - Implementation:   {format_currency(total['Implementation'])}")
    print(f"  - Maintenance:      {format_currency(total['Maintenance'])}")
    
    print(f"\nTotal Returns:        {format_currency(total['Total Revenue'])}")
    print(f"  - Tier 1 (Diabetes):{format_currency(total['Tier 1 Revenue'])}")
    print(f"  - Tier 2 (Cardio):  {format_currency(total['Tier 2 Revenue'])}")
    print(f"  - Tier 3 (Cancer):  {format_currency(total['Tier 3 Revenue'])}")
    print(f"  - HEI Protection:   {format_currency(total['HEI Protection'])}")
    
    print(f"\n{'='*30}")
    print(f"NET BENEFIT:          {format_currency(total['Net Benefit'])}")
    print(f"ROI:                  {meta['ROI']:.0f}%")
    print(f"Payback Period:       {meta['Payback Period']}")
    print(f"{'='*30}")
    
    print(f"\nPer-Member Economics:")
    print(f"  - Annual Value:     {format_currency(meta['Per-Member Annual Value'])}/member")
    print(f"  - Annual Cost:      {format_currency(meta['Per-Member Annual Cost'])}/member")
    print(f"  - Net Benefit:      {format_currency(meta['Per-Member Annual Value'] - meta['Per-Member Annual Cost'])}/member")
    
    print("\n" + "-" * 80)
    print("YEAR-BY-YEAR BREAKDOWN")
    print("-" * 80)
    print(f"\n{'Year':<10} {'Costs':<15} {'Revenue':<15} {'Net Benefit':<15} {'Cumulative':<15}")
    print("-" * 80)
    
    for year in ['Year 1', 'Year 2', 'Year 3', 'Year 4', 'Year 5']:
        y = model[year]
        print(f"{year:<10} {format_currency(y['Total Costs']):<15} "
              f"{format_currency(y['Total Revenue']):<15} "
              f"{format_currency(y['Net Benefit']):<15} "
              f"{format_currency(y['Cumulative Net']):<15}")
    
    print("\n" + "=" * 80)

def save_to_csv(model, members, output_file):
    """Save model to CSV file."""
    
    # Create DataFrame
    rows = []
    
    # Header
    rows.append(['HEDIS Star Rating Portfolio - Financial Projection'])
    rows.append([f'Plan Size: {members:,} Members'])
    rows.append([f'Projection Period: 5 Years (2025-2029)'])
    rows.append([])
    
    # Costs section
    rows.append(['INVESTMENT (COSTS)', 'Year 1', 'Year 2', 'Year 3', 'Year 4', 'Year 5', '5-Year Total'])
    rows.append(['Development', 
                 model['Year 1']['Development'],
                 model['Year 2']['Development'],
                 model['Year 3']['Development'],
                 model['Year 4']['Development'],
                 model['Year 5']['Development'],
                 model['5-Year Total']['Development']])
    rows.append(['Implementation',
                 model['Year 1']['Implementation'],
                 model['Year 2']['Implementation'],
                 model['Year 3']['Implementation'],
                 model['Year 4']['Implementation'],
                 model['Year 5']['Implementation'],
                 model['5-Year Total']['Implementation']])
    rows.append(['Maintenance',
                 model['Year 1']['Maintenance'],
                 model['Year 2']['Maintenance'],
                 model['Year 3']['Maintenance'],
                 model['Year 4']['Maintenance'],
                 model['Year 5']['Maintenance'],
                 model['5-Year Total']['Maintenance']])
    rows.append(['TOTAL COSTS',
                 model['Year 1']['Total Costs'],
                 model['Year 2']['Total Costs'],
                 model['Year 3']['Total Costs'],
                 model['Year 4']['Total Costs'],
                 model['Year 5']['Total Costs'],
                 model['5-Year Total']['Total Costs']])
    rows.append([])
    
    # Revenue section
    rows.append(['RETURNS (REVENUE)', 'Year 1', 'Year 2', 'Year 3', 'Year 4', 'Year 5', '5-Year Total'])
    rows.append(['Tier 1 - Diabetes Portfolio',
                 model['Year 1']['Tier 1 Revenue'],
                 model['Year 2']['Tier 1 Revenue'],
                 model['Year 3']['Tier 1 Revenue'],
                 model['Year 4']['Tier 1 Revenue'],
                 model['Year 5']['Tier 1 Revenue'],
                 model['5-Year Total']['Tier 1 Revenue']])
    rows.append(['Tier 2 - Cardiovascular Portfolio',
                 model['Year 1']['Tier 2 Revenue'],
                 model['Year 2']['Tier 2 Revenue'],
                 model['Year 3']['Tier 2 Revenue'],
                 model['Year 4']['Tier 2 Revenue'],
                 model['Year 5']['Tier 2 Revenue'],
                 model['5-Year Total']['Tier 2 Revenue']])
    rows.append(['Tier 3 - Cancer Screening',
                 model['Year 1']['Tier 3 Revenue'],
                 model['Year 2']['Tier 3 Revenue'],
                 model['Year 3']['Tier 3 Revenue'],
                 model['Year 4']['Tier 3 Revenue'],
                 model['Year 5']['Tier 3 Revenue'],
                 model['5-Year Total']['Tier 3 Revenue']])
    rows.append(['HEI Protection (2027 Mandate)',
                 model['Year 1']['HEI Protection'],
                 model['Year 2']['HEI Protection'],
                 model['Year 3']['HEI Protection'],
                 model['Year 4']['HEI Protection'],
                 model['Year 5']['HEI Protection'],
                 model['5-Year Total']['HEI Protection']])
    rows.append(['TOTAL REVENUE',
                 model['Year 1']['Total Revenue'],
                 model['Year 2']['Total Revenue'],
                 model['Year 3']['Total Revenue'],
                 model['Year 4']['Total Revenue'],
                 model['Year 5']['Total Revenue'],
                 model['5-Year Total']['Total Revenue']])
    rows.append([])
    
    # Net benefit
    rows.append(['NET BENEFIT', 'Year 1', 'Year 2', 'Year 3', 'Year 4', 'Year 5', '5-Year Total'])
    rows.append(['Annual Net Benefit',
                 model['Year 1']['Net Benefit'],
                 model['Year 2']['Net Benefit'],
                 model['Year 3']['Net Benefit'],
                 model['Year 4']['Net Benefit'],
                 model['Year 5']['Net Benefit'],
                 model['5-Year Total']['Net Benefit']])
    rows.append(['Cumulative Net Benefit',
                 model['Year 1']['Cumulative Net'],
                 model['Year 2']['Cumulative Net'],
                 model['Year 3']['Cumulative Net'],
                 model['Year 4']['Cumulative Net'],
                 model['Year 5']['Cumulative Net'],
                 model['5-Year Total']['Net Benefit']])
    rows.append([])
    
    # Metrics
    meta = model['Metadata']
    rows.append(['KEY METRICS', 'Value'])
    rows.append(['ROI (%)', f"{meta['ROI']:.0f}%"])
    rows.append(['Payback Period', meta['Payback Period']])
    rows.append(['Annual Value at Maturity', meta['Annual Value at Maturity']])
    rows.append(['Per-Member Annual Value', f"${meta['Per-Member Annual Value']:.2f}"])
    rows.append(['Per-Member Annual Cost', f"${meta['Per-Member Annual Cost']:.2f}"])
    
    df = pd.DataFrame(rows)
    df.to_csv(output_file, index=False, header=False)
    print(f"\n[OK] Financial model saved to: {output_file}")

def main():
    parser = argparse.ArgumentParser(description='Calculate HEDIS Portfolio financials for any plan size')
    parser.add_argument('--members', type=int, required=True, help='Number of MA members in the plan')
    parser.add_argument('--output', type=str, default=None, help='Output CSV file (optional)')
    
    args = parser.parse_args()
    
    # Validate input
    if args.members < 1000:
        print("[ERROR] Plan size must be at least 1,000 members")
        return
    
    if args.members > 5000000:
        print("[WARNING] Plan size exceeds typical MA plan. Projections may be less accurate.")
    
    # Calculate financials
    model = calculate_financials(args.members)
    
    # Print summary
    print_summary(model, args.members)
    
    # Save to CSV if requested
    if args.output:
        save_to_csv(model, args.members, args.output)
    else:
        # Default output filename
        default_output = f'reports/financial_projection_{args.members}_members.csv'
        save_to_csv(model, args.members, default_output)

if __name__ == '__main__':
    main()

