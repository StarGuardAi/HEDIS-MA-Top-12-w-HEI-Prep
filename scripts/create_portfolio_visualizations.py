"""
Portfolio Visualization Generator
Creates professional charts for LinkedIn and presentations

Charts Generated:
1. 5-Year ROI Projection
2. Portfolio Value Breakdown (12 measures)
3. Plan Size Comparison
4. Development Efficiency
5. Star Rating Impact

Author: Analytics Team
Date: October 24, 2025
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from matplotlib.patches import Rectangle
import seaborn as sns

# Set professional style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# Create output directory
import os
output_dir = 'visualizations/portfolio'
os.makedirs(output_dir, exist_ok=True)

print("Creating Portfolio Visualizations...")
print("=" * 60)

# ============================================================================
# CHART 1: 5-Year ROI Projection
# ============================================================================
print("\n1. Creating 5-Year ROI Projection Chart...")

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

# Data
years = ['Year 1', 'Year 2', 'Year 3', 'Year 4', 'Year 5']
investment = [-0.75, -0.65, -0.60, -0.50, -0.50]  # in millions
returns = [2.5, 13.0, 20.0, 25.0, 27.0]  # in millions
net_benefit = [1.75, 12.35, 19.4, 24.5, 26.5]  # in millions
cumulative = [1.75, 14.1, 33.5, 58.0, 84.5]  # in millions

x = np.arange(len(years))
width = 0.35

# Left chart: Annual Investment vs Returns
bars1 = ax1.bar(x - width/2, investment, width, label='Investment', color='#E74C3C', alpha=0.8)
bars2 = ax1.bar(x + width/2, returns, width, label='Returns', color='#27AE60', alpha=0.8)

ax1.set_xlabel('Year', fontsize=12, fontweight='bold')
ax1.set_ylabel('Amount ($ Millions)', fontsize=12, fontweight='bold')
ax1.set_title('Annual Investment vs. Returns\n5-Year Projection', fontsize=14, fontweight='bold', pad=20)
ax1.set_xticks(x)
ax1.set_xticklabels(years)
ax1.legend(fontsize=11)
ax1.grid(axis='y', alpha=0.3)
ax1.axhline(y=0, color='black', linewidth=0.8)

# Add value labels
for bar in bars1:
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., height - 0.1,
            f'${abs(height):.2f}M', ha='center', va='top', fontweight='bold', fontsize=9)
for bar in bars2:
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., height + 0.3,
            f'${height:.1f}M', ha='center', va='bottom', fontweight='bold', fontsize=9)

# Right chart: Cumulative Net Benefit
line = ax2.plot(years, cumulative, marker='o', linewidth=3, markersize=10, 
                color='#3498DB', label='Cumulative Net Benefit')
ax2.fill_between(range(len(years)), cumulative, alpha=0.3, color='#3498DB')

ax2.set_xlabel('Year', fontsize=12, fontweight='bold')
ax2.set_ylabel('Cumulative Net Benefit ($ Millions)', fontsize=12, fontweight='bold')
ax2.set_title('Cumulative Net Benefit Growth\n5-Year Total: $84.5M', 
              fontsize=14, fontweight='bold', pad=20)
ax2.grid(alpha=0.3)

# Add value labels on points
for i, (year, value) in enumerate(zip(years, cumulative)):
    ax2.annotate(f'${value:.1f}M', 
                xy=(i, value), 
                xytext=(0, 10),
                textcoords='offset points',
                ha='center',
                fontweight='bold',
                fontsize=10,
                bbox=dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.8))

# Add ROI text
fig.text(0.5, 0.02, 'ROI: 2,817% (28x return) | Payback: Immediate', 
         ha='center', fontsize=13, fontweight='bold', 
         bbox=dict(boxstyle='round,pad=0.8', facecolor='#F39C12', alpha=0.8))

plt.tight_layout(rect=[0, 0.05, 1, 1])
plt.savefig(f'{output_dir}/1_five_year_roi.png', dpi=300, bbox_inches='tight')
print(f"   [OK] Saved: {output_dir}/1_five_year_roi.png")
plt.close()

# ============================================================================
# CHART 2: Portfolio Value Breakdown (12 Measures)
# ============================================================================
print("\n2. Creating Portfolio Value Breakdown Chart...")

fig, ax = plt.subplots(figsize=(14, 10))

# Data for all 12 measures
measures = [
    'GSD\n(Glycemic Status)', 'KED\n(Kidney Health)', 'EED\n(Eye Exam)',
    'PDC-DR\n(Diabetes Meds)', 'BPD\n(BP Control)',
    'CBP\n(BP Control)', 'SUPD\n(Statin)', 
    'PDC-RASA\n(HTN Meds)', 'PDC-STA\n(Cholesterol)',
    'BCS\n(Breast Cancer)', 'COL\n(Colorectal)',
    'HEI\n(Health Equity)'
]

value_min = [360, 360, 120, 120, 120, 300, 120, 100, 100, 150, 150, 10000]  # in thousands
value_max = [615, 615, 205, 205, 205, 450, 180, 150, 150, 225, 225, 20000]  # in thousands

tiers = ['Tier 1\nDiabetes'] * 5 + ['Tier 2\nCardiovascular'] * 4 + ['Tier 3\nCancer'] * 2 + ['Tier 4\nEquity']
colors_map = {
    'Tier 1\nDiabetes': '#E74C3C',
    'Tier 2\nCardiovascular': '#3498DB', 
    'Tier 3\nCancer': '#9B59B6',
    'Tier 4\nEquity': '#F39C12'
}
colors = [colors_map[t] for t in tiers]

y_pos = np.arange(len(measures))

# Create horizontal bars
bars = ax.barh(y_pos, value_max, color=colors, alpha=0.7, edgecolor='black', linewidth=1.5)

# Add value labels
for i, (vmin, vmax) in enumerate(zip(value_min, value_max)):
    if vmax >= 1000:  # HEI
        ax.text(vmax + 500, i, f'${vmin/1000:.0f}M-${vmax/1000:.0f}M', 
                va='center', fontweight='bold', fontsize=10)
    else:
        ax.text(vmax + 15, i, f'${vmin}K-${vmax}K', 
                va='center', fontweight='bold', fontsize=10)

# Add measure annotations
new_2025 = [1, 4]  # KED, BPD
new_2027 = [11]  # HEI
triple_weighted = [0, 1, 5]  # GSD, KED, CBP

for i in new_2025:
    ax.text(10, i, '* NEW 2025', va='center', ha='left', 
            fontweight='bold', fontsize=8, color='white',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='green', alpha=0.8))

for i in new_2027:
    ax.text(500, i, '** NEW 2027', va='center', ha='left',
            fontweight='bold', fontsize=8, color='white',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='darkgreen', alpha=0.8))

for i in triple_weighted:
    if i < 11:  # Not HEI
        ax.text(value_max[i] - 40, i, '3x', va='center', ha='center',
                fontweight='bold', fontsize=10, color='white',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='red', alpha=0.9))

ax.set_yticks(y_pos)
ax.set_yticklabels(measures, fontsize=10, fontweight='bold')
ax.set_xlabel('Annual Value (100K Member Plan)', fontsize=12, fontweight='bold')
ax.set_title('Complete Portfolio Value Breakdown\n12 HEDIS Measures Across 4 Tiers', 
             fontsize=15, fontweight='bold', pad=20)
ax.grid(axis='x', alpha=0.3)

# Add tier labels and totals
tier_totals = {
    'Tier 1\nDiabetes': '$1.2M-$1.4M',
    'Tier 2\nCardiovascular': '$620K-$930K',
    'Tier 3\nCancer': '$300K-$450K',
    'Tier 4\nEquity': '$10M-$20M'
}

# Legend
legend_elements = [mpatches.Patch(facecolor=colors_map[tier], 
                                  label=f'{tier.replace(chr(10), " ")}: {tier_totals[tier]}',
                                  alpha=0.7, edgecolor='black')
                  for tier in colors_map.keys()]
ax.legend(handles=legend_elements, loc='lower right', fontsize=11, framealpha=0.9)

# Add total
fig.text(0.5, 0.02, 'Total Portfolio Value: $13M-$27M/year (includes $10M-$20M HEI protection)', 
         ha='center', fontsize=13, fontweight='bold',
         bbox=dict(boxstyle='round,pad=0.8', facecolor='#27AE60', alpha=0.8))

plt.tight_layout(rect=[0, 0.05, 1, 1])
plt.savefig(f'{output_dir}/2_portfolio_value_breakdown.png', dpi=300, bbox_inches='tight')
print(f"   [OK] Saved: {output_dir}/2_portfolio_value_breakdown.png")
plt.close()

# ============================================================================
# CHART 3: Plan Size Comparison
# ============================================================================
print("\n3. Creating Plan Size Comparison Chart...")

fig, ax = plt.subplots(figsize=(14, 8))

# Data for different plan sizes
plan_sizes = ['25K', '50K', '100K\n(Base)', '250K', '500K', '1M']
sizes_numeric = [25, 50, 100, 250, 500, 1000]  # in thousands

# Scale values (linear for gap closure, sublinear for HEI)
gap_closure_min = [0.53, 1.06, 2.12, 5.3, 10.6, 21.2]  # in millions
gap_closure_max = [0.69, 1.39, 2.78, 6.95, 13.9, 27.8]  # in millions
hei_protection_min = [2.5, 5, 10, 20, 35, 60]  # in millions (sublinear scale)
hei_protection_max = [5, 10, 20, 35, 60, 100]  # in millions

total_min = [a + b for a, b in zip(gap_closure_min, hei_protection_min)]
total_max = [a + b for a, b in zip(gap_closure_max, hei_protection_max)]

x = np.arange(len(plan_sizes))
width = 0.35

# Stacked bars
bars1 = ax.bar(x, gap_closure_max, width, label='Gap Closure Revenue', 
               color='#3498DB', alpha=0.8)
bars2 = ax.bar(x, hei_protection_max, width, bottom=gap_closure_max,
               label='HEI Protection', color='#F39C12', alpha=0.8)

ax.set_xlabel('Plan Size (Members)', fontsize=12, fontweight='bold')
ax.set_ylabel('Annual Value ($ Millions)', fontsize=12, fontweight='bold')
ax.set_title('Portfolio Value by Plan Size\nScalable Economics Across All Plan Sizes', 
             fontsize=15, fontweight='bold', pad=20)
ax.set_xticks(x)
ax.set_xticklabels(plan_sizes, fontsize=11, fontweight='bold')
ax.legend(fontsize=12, loc='upper left')
ax.grid(axis='y', alpha=0.3)

# Add total value labels
for i, (total_min_val, total_max_val) in enumerate(zip(total_min, total_max)):
    total_height = total_max_val
    ax.text(i, total_height + 2, f'${total_min_val:.1f}M-\n${total_max_val:.1f}M',
            ha='center', va='bottom', fontweight='bold', fontsize=10,
            bbox=dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.8))

# Add highlight for base case
ax.axvspan(1.7, 2.3, alpha=0.2, color='green')
ax.text(2, ax.get_ylim()[1] * 0.95, '← Base Case\n(100K Members)',
        ha='center', fontsize=11, fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.5', facecolor='lightgreen', alpha=0.7))

# Add ROI note
fig.text(0.5, 0.02, 'ROI remains consistently 2,500-3,000% across all plan sizes', 
         ha='center', fontsize=12, fontweight='bold',
         bbox=dict(boxstyle='round,pad=0.8', facecolor='#27AE60', alpha=0.8))

plt.tight_layout(rect=[0, 0.05, 1, 1])
plt.savefig(f'{output_dir}/3_plan_size_comparison.png', dpi=300, bbox_inches='tight')
print(f"   [OK] Saved: {output_dir}/3_plan_size_comparison.png")
plt.close()

# ============================================================================
# CHART 4: Development Efficiency
# ============================================================================
print("\n4. Creating Development Efficiency Chart...")

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

# Left: Time comparison
methods = ['Traditional\nApproach', 'Our Pattern-\nBased Approach']
time_hours = [4380, 27]  # 6 months = 4,380 hours (182.5 days * 24 hours) vs 27 hours
time_labels = ['6-12 months\n(~4,380 hrs)', '27 hours\n(1.5 days)']

bars = ax1.barh(methods, time_hours, color=['#E74C3C', '#27AE60'], alpha=0.8)

ax1.set_xlabel('Development Time (Hours, log scale)', fontsize=12, fontweight='bold')
ax1.set_title('Development Time Comparison\n99.4% Time Reduction', 
              fontsize=14, fontweight='bold', pad=20)
ax1.set_xscale('log')
ax1.grid(axis='x', alpha=0.3)

# Add value labels
for bar, label in zip(bars, time_labels):
    width = bar.get_width()
    ax1.text(width * 1.5, bar.get_y() + bar.get_height()/2,
            label, ha='left', va='center', fontweight='bold', fontsize=12,
            bbox=dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.8))

# Right: Cost comparison
methods_cost = ['Traditional\nApproach', 'Our Pattern-\nBased Approach']
costs = [1500, 50]  # in thousands
cost_labels = ['$1M-$2M\n(typical)', '$50K\n(equivalent)']

bars = ax2.barh(methods_cost, costs, color=['#E74C3C', '#27AE60'], alpha=0.8)

ax2.set_xlabel('Development Cost ($K, log scale)', fontsize=12, fontweight='bold')
ax2.set_title('Development Cost Comparison\n95-98% Cost Reduction', 
              fontsize=14, fontweight='bold', pad=20)
ax2.set_xscale('log')
ax2.grid(axis='x', alpha=0.3)

# Add value labels
for bar, label in zip(bars, cost_labels):
    width = bar.get_width()
    ax2.text(width * 1.5, bar.get_y() + bar.get_height()/2,
            label, ha='left', va='center', fontweight='bold', fontsize=12,
            bbox=dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.8))

# Add summary
fig.text(0.5, 0.02, 'Pattern-Based Development: 162x faster, 30x cheaper, same enterprise quality', 
         ha='center', fontsize=13, fontweight='bold',
         bbox=dict(boxstyle='round,pad=0.8', facecolor='#F39C12', alpha=0.8))

plt.tight_layout(rect=[0, 0.05, 1, 1])
plt.savefig(f'{output_dir}/4_development_efficiency.png', dpi=300, bbox_inches='tight')
print(f"   [OK] Saved: {output_dir}/4_development_efficiency.png")
plt.close()

# ============================================================================
# CHART 5: Star Rating Impact
# ============================================================================
print("\n5. Creating Star Rating Impact Chart...")

fig, ax = plt.subplots(figsize=(14, 8))

# Data
scenarios = ['Current\nState', 'Year 1\n(30% gaps\nclosed)', 'Year 2\n(50% gaps\nclosed)', 
             'Year 3\n(70% gaps\nclosed)', 'Target\nState\n(Optimal)']
star_ratings = [3.5, 3.75, 4.25, 4.5, 5.0]
bonus_payments = [30, 36, 48, 54, 60]  # in millions
portfolio_contribution = [0, 1.75, 12.35, 19.4, 27]  # in millions (from our portfolio)

x = np.arange(len(scenarios))
width = 0.4

# Create grouped bars
bars1 = ax.bar(x - width/2, star_ratings, width, label='Star Rating', 
               color='#F39C12', alpha=0.8)
ax2 = ax.twinx()
bars2 = ax2.bar(x + width/2, bonus_payments, width, label='CMS Bonus Payment',
                color='#27AE60', alpha=0.8)

# Add labels on bars
for bar in bars1:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height + 0.05,
            f'{height:.2f} STARS', ha='center', va='bottom', 
            fontweight='bold', fontsize=11)

for bar, contrib in zip(bars2, portfolio_contribution):
    height = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2., height + 1,
             f'${height}M', ha='center', va='bottom',
             fontweight='bold', fontsize=11,
             bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))
    if contrib > 0:
        ax2.text(bar.get_x() + bar.get_width()/2., height/2,
                f'Portfolio:\n+${contrib:.1f}M', ha='center', va='center',
                fontweight='bold', fontsize=9, color='white')

ax.set_xlabel('Scenario', fontsize=12, fontweight='bold')
ax.set_ylabel('Star Rating', fontsize=12, fontweight='bold', color='#F39C12')
ax2.set_ylabel('Annual CMS Bonus Payment ($ Millions)', fontsize=12, fontweight='bold', color='#27AE60')
ax.set_title('Star Rating Impact & CMS Bonus Growth\nPortfolio-Driven Improvement Trajectory',
             fontsize=15, fontweight='bold', pad=20)

ax.set_xticks(x)
ax.set_xticklabels(scenarios, fontsize=10, fontweight='bold')
ax.set_ylim(3, 5.5)
ax2.set_ylim(25, 65)

ax.tick_params(axis='y', labelcolor='#F39C12')
ax2.tick_params(axis='y', labelcolor='#27AE60')

ax.grid(axis='y', alpha=0.3)

# Add legend
lines1, labels1 = ax.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=11)

# Add impact arrow
ax.annotate('', xy=(4, 5.0), xytext=(0, 3.5),
            arrowprops=dict(arrowstyle='->', lw=3, color='red', alpha=0.5))
ax.text(2, 4.5, 'Portfolio Impact:\n+1.5 Stars\n+$30M/year',
        ha='center', fontsize=12, fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.8', facecolor='yellow', alpha=0.7))

plt.tight_layout()
plt.savefig(f'{output_dir}/5_star_rating_impact.png', dpi=300, bbox_inches='tight')
print(f"   [OK] Saved: {output_dir}/5_star_rating_impact.png")
plt.close()

# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "=" * 60)
print("[OK] ALL 5 VISUALIZATIONS CREATED SUCCESSFULLY!")
print("=" * 60)
print(f"\nFiles saved in: {output_dir}/")
print("\nGenerated Charts:")
print("  1. 1_five_year_roi.png - 5-Year ROI & Cumulative Net Benefit")
print("  2. 2_portfolio_value_breakdown.png - 12 Measures Across 4 Tiers")
print("  3. 3_plan_size_comparison.png - Scalable Value by Plan Size")
print("  4. 4_development_efficiency.png - Time & Cost Savings")
print("  5. 5_star_rating_impact.png - Star Rating Growth Trajectory")
print("\nReady for:")
print("  [OK] LinkedIn carousel post")
print("  [OK] Executive presentations")
print("  [OK] GitHub repository showcase")
print("  [OK] Portfolio demonstrations")
print("\n" + "=" * 60)

