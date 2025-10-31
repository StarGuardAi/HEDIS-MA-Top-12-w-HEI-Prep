"""
Portfolio Reporter for HEDIS Measures

This module generates comprehensive reports for the HEDIS portfolio including
executive summaries, detailed measure reports, member-level priorities, and
financial projections.

Export formats:
- JSON (for APIs and data exchange)
- CSV (for Excel import)
- Markdown (for documentation)
- Text (for simple viewing)

HEDIS Specification: MY2025 Volume 2
"""

import pandas as pd
import numpy as np
import json
from typing import Dict, List, Optional
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PortfolioReporter:
    """
    Generate comprehensive reports for HEDIS portfolio management.
    
    Report types:
    - Executive summary
    - Detailed measure reports
    - Member-level priority lists
    - Financial projections
    - Intervention recommendations
    """
    
    def __init__(self, measurement_year: int = 2023):
        """
        Initialize portfolio reporter.
        
        Args:
            measurement_year: Measurement year for reports
        """
        self.measurement_year = measurement_year
        self.report_date = datetime.now().strftime("%Y-%m-%d")
        logger.info("Portfolio reporter initialized for MY%d", measurement_year)
    
    def generate_executive_summary(
        self,
        portfolio_summary: Dict,
        star_scenarios: Dict,
        optimization_results: Dict
    ) -> str:
        """
        Generate executive summary report.
        
        Args:
            portfolio_summary: From portfolio_calculator
            star_scenarios: From star_rating_simulator
            optimization_results: From cross_measure_optimizer
            
        Returns:
            Formatted executive summary (markdown)
        """
        report = []
        report.append("# HEDIS Portfolio Executive Summary")
        report.append(f"\n**Measurement Year:** {self.measurement_year}")
        report.append(f"**Report Date:** {self.report_date}")
        report.append(f"**Portfolio:** {portfolio_summary.get('portfolio_name', 'Tier 1 Diabetes')}")
        report.append("\n---\n")
        
        # Portfolio Overview
        report.append("## Portfolio Overview\n")
        report.append(f"- **Total Measures:** {portfolio_summary.get('total_measures', 5)}")
        report.append(f"- **Total Members:** {portfolio_summary.get('total_members', 0):,}")
        report.append(f"- **Members with Gaps:** {portfolio_summary.get('members_with_gaps', 0):,}")
        report.append(f"- **Gap Rate:** {portfolio_summary.get('gap_rate', 0)}%")
        report.append(f"- **Multi-Measure Gaps:** {portfolio_summary.get('members_multi_gaps', 0):,}")
        report.append("")
        
        # Star Rating
        star_current = portfolio_summary.get('star_rating', {})
        report.append("## Star Rating Performance\n")
        report.append(f"- **Current Rating:** {star_current.get('current_stars', 0)} stars")
        report.append(f"- **Weighted Compliance:** {star_current.get('current_weighted_rate', 0)}%")
        
        # Potential improvements
        with_50 = star_current.get('with_50pct_closure', {})
        with_100 = star_current.get('with_100pct_closure', {})
        report.append(f"- **With 50% Gap Closure:** {with_50.get('stars', 0)} stars (+{with_50.get('star_improvement', 0)})")
        report.append(f"- **With 100% Gap Closure:** {with_100.get('stars', 0)} stars (+{with_100.get('star_improvement', 0)})")
        report.append("")
        
        # Financial Impact
        value = portfolio_summary.get('value', {})
        report.append("## Financial Impact\n")
        report.append(f"- **Total Portfolio Value:** {value.get('total_portfolio_value', '$0')}")
        report.append(f"- **Current Value (at risk):** {value.get('current_value', '$0')}")
        report.append(f"- **Opportunity Value:** {value.get('opportunity_value', '$0')}")
        report.append(f"- **Opportunity %:** {value.get('opportunity_pct', 0)}%")
        report.append("")
        
        # Intervention Strategy
        report.append("## Recommended Intervention Strategy\n")
        report.append(f"- **Priority Members:** {optimization_results.get('total_members', 0):,}")
        report.append(f"- **Total Interventions:** {optimization_results.get('total_interventions', 0):,}")
        report.append(f"- **Estimated Cost:** {optimization_results.get('total_cost', '$0')}")
        report.append(f"- **Expected Value:** {optimization_results.get('expected_value', '$0')}")
        report.append(f"- **Expected ROI:** {optimization_results.get('expected_roi', 0)}x")
        report.append("")
        
        # Key Priorities
        report.append("## Key Priorities\n")
        segments = portfolio_summary.get('segments', {})
        report.append(f"1. **High-Value Members:** {segments.get('high_value', 0):,} (triple-weighted measures)")
        report.append(f"2. **NEW 2025 Priority:** {segments.get('new_2025_priority', 0):,} (KED, BPD)")
        report.append(f"3. **Multi-Measure Opportunities:** {segments.get('multi_measure', 0):,} (efficiency gains)")
        report.append("")
        
        # Recommendations
        report.append("## Executive Recommendations\n")
        report.append("1. **Focus on triple-weighted measures** (GSD, KED) for maximum Star Rating impact")
        report.append("2. **Prioritize NEW 2025 measures** (KED, BPD) to launch strong")
        report.append("3. **Target multi-measure members** for intervention bundling (20-40% cost savings)")
        report.append("4. **Implement systematic outreach** to close identified gaps")
        report.append("5. **Monitor progress monthly** and adjust strategy as needed")
        report.append("")
        
        return "\n".join(report)
    
    def generate_measure_report(
        self,
        measure_code: str,
        measure_summary: Dict
    ) -> str:
        """
        Generate detailed report for a single measure.
        
        Args:
            measure_code: Measure code (e.g., "GSD", "KED")
            measure_summary: Measure summary from measure calculation
            
        Returns:
            Formatted measure report (markdown)
        """
        report = []
        report.append(f"# {measure_code}: {measure_summary.get('measure_name', '')}\n")
        report.append(f"**Measurement Year:** {self.measurement_year}")
        report.append(f"**Report Date:** {self.report_date}")
        report.append("\n---\n")
        
        # Performance Summary
        report.append("## Performance Summary\n")
        report.append(f"- **Denominator:** {measure_summary.get('denominator', 0):,} members")
        report.append(f"- **Exclusions:** {measure_summary.get('exclusions', 0):,} members")
        report.append(f"- **Eligible Population:** {measure_summary.get('eligible_population', 0):,} members")
        report.append(f"- **Numerator (Compliant):** {measure_summary.get('numerator', 0):,} members")
        report.append(f"- **Gaps:** {measure_summary.get('gaps', 0):,} members")
        report.append(f"- **Compliance Rate:** {measure_summary.get('compliance_rate', 0)}%")
        report.append(f"- **Gap Rate:** {measure_summary.get('gap_rate', 0)}%")
        report.append("")
        
        # HEDIS Specification
        report.append("## HEDIS Specification\n")
        report.append(f"- **Measure Code:** {measure_code}")
        report.append(f"- **HEDIS Spec:** {measure_summary.get('measurement_year', 'MY2025')} Volume 2")
        if measure_summary.get('new_2025_measure'):
            report.append("- **Status:** NEW 2025 MEASURE ⭐")
        report.append("")
        
        # Gap Analysis
        report.append("## Gap Analysis\n")
        eligible = measure_summary.get('eligible_population', 0)
        gaps = measure_summary.get('gaps', 0)
        if eligible > 0:
            gap_pct = (gaps / eligible * 100)
            report.append(f"- **Total Gaps:** {gaps:,} ({gap_pct:.1f}% of eligible)")
            
            # Estimate closure potential
            potential_10 = int(gaps * 0.10)
            potential_25 = int(gaps * 0.25)
            potential_50 = int(gaps * 0.50)
            
            report.append(f"- **With 10% Closure:** {potential_10:,} gaps closed")
            report.append(f"- **With 25% Closure:** {potential_25:,} gaps closed")
            report.append(f"- **With 50% Closure:** {potential_50:,} gaps closed")
        report.append("")
        
        # Recommendations
        report.append("## Intervention Recommendations\n")
        
        if measure_code == "GSD":
            report.append("- Schedule HbA1c tests for gap members")
            report.append("- Bundle with KED for efficiency (combined lab order)")
            report.append("- Target members with poor diabetes control")
        elif measure_code == "KED":
            report.append("- Order eGFR + ACR tests for gap members")
            report.append("- Bundle with GSD for efficiency (combined lab order)")
            report.append("- Focus on members with CKD risk factors")
        elif measure_code == "EED":
            report.append("- Schedule eye exams with ophthalmologists")
            report.append("- Send reminder letters for overdue exams")
            report.append("- Target members with retinopathy history")
        elif measure_code == "PDC-DR":
            report.append("- Pharmacist consultation for medication adherence")
            report.append("- Address barriers to medication access")
            report.append("- Implement medication synchronization programs")
        elif measure_code == "BPD":
            report.append("- BP monitoring and medication review")
            report.append("- Hypertension education and lifestyle counseling")
            report.append("- Home BP monitoring for uncontrolled members")
        
        report.append("")
        
        return "\n".join(report)
    
    def generate_member_priority_report(
        self,
        priority_list: pd.DataFrame,
        top_n: int = 100
    ) -> str:
        """
        Generate member-level priority report.
        
        Args:
            priority_list: Priority list from cross_measure_optimizer
            top_n: Number of top members to include (default: 100)
            
        Returns:
            Formatted member priority report (markdown)
        """
        report = []
        report.append(f"# Member Priority List (Top {top_n})\n")
        report.append(f"**Measurement Year:** {self.measurement_year}")
        report.append(f"**Report Date:** {self.report_date}")
        report.append("\n---\n")
        
        # Summary statistics
        report.append("## Summary\n")
        report.append(f"- **Total Priority Members:** {len(priority_list):,}")
        report.append(f"- **Showing Top:** {min(top_n, len(priority_list)):,}")
        report.append(f"- **Total Gaps:** {priority_list['total_gaps'].sum():,.0f}")
        report.append(f"- **Total Est. Cost:** ${priority_list['total_cost'].sum():,.0f}")
        report.append(f"- **Total Est. Value:** ${priority_list['expected_value_min'].sum():,.0f}-${priority_list['expected_value_max'].sum():,.0f}")
        report.append("")
        
        # Priority breakdown
        report.append("## Priority Breakdown\n")
        if 'intervention_priority' in priority_list.columns:
            priority_counts = priority_list['intervention_priority'].value_counts()
            for priority, count in priority_counts.items():
                report.append(f"- **{priority}:** {count:,} members")
        report.append("")
        
        # Top members table
        report.append("## Top Members\n")
        report.append("| Rank | Member ID | Age | Gaps | Priority | ROI | Recommended Actions |")
        report.append("|------|-----------|-----|------|----------|-----|---------------------|")
        
        top_members = priority_list.head(top_n)
        for rank, (_, member) in enumerate(top_members.iterrows(), 1):
            member_id = str(member.get('member_id', 'N/A'))[:8] + "..."  # Truncate for display
            age = int(member.get('age', 0))
            gaps = int(member.get('total_gaps', 0))
            priority = round(member.get('priority_score', 0), 1)
            roi = round(member.get('expected_roi_avg', 0), 2)
            actions = member.get('recommended_actions', 'N/A')[:50] + "..."  # Truncate
            
            report.append(f"| {rank} | {member_id} | {age} | {gaps} | {priority} | {roi}x | {actions} |")
        
        report.append("")
        
        return "\n".join(report)
    
    def export_to_json(
        self,
        data: Dict,
        filename: str
    ) -> None:
        """
        Export data to JSON file.
        
        Args:
            data: Dictionary to export
            filename: Output filename
        """
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2, default=str)
        
        logger.info("Exported to JSON: %s", filename)
    
    def export_to_csv(
        self,
        df: pd.DataFrame,
        filename: str
    ) -> None:
        """
        Export DataFrame to CSV file.
        
        Args:
            df: DataFrame to export
            filename: Output filename
        """
        df.to_csv(filename, index=False)
        logger.info("Exported to CSV: %s", filename)
    
    def generate_complete_portfolio_report(
        self,
        portfolio_summary: Dict,
        star_scenarios: Dict,
        optimization_results: Dict,
        priority_list: pd.DataFrame,
        output_dir: str = "reports"
    ) -> Dict[str, str]:
        """
        Generate complete portfolio report package.
        
        Args:
            portfolio_summary: From portfolio_calculator
            star_scenarios: From star_rating_simulator
            optimization_results: From cross_measure_optimizer
            priority_list: Priority list DataFrame
            output_dir: Output directory for reports
            
        Returns:
            Dictionary of generated report filenames
        """
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        reports = {}
        
        # Executive summary
        exec_summary = self.generate_executive_summary(
            portfolio_summary,
            star_scenarios,
            optimization_results
        )
        exec_filename = f"{output_dir}/executive_summary_{self.report_date}.md"
        with open(exec_filename, 'w') as f:
            f.write(exec_summary)
        reports["executive_summary"] = exec_filename
        
        # Measure reports
        measures = portfolio_summary.get('measures', {})
        for measure_code, measure_summary in measures.items():
            measure_report = self.generate_measure_report(measure_code, measure_summary)
            measure_filename = f"{output_dir}/measure_{measure_code}_{self.report_date}.md"
            with open(measure_filename, 'w') as f:
                f.write(measure_report)
            reports[f"measure_{measure_code}"] = measure_filename
        
        # Member priority list
        priority_report = self.generate_member_priority_report(priority_list, top_n=100)
        priority_filename = f"{output_dir}/priority_list_{self.report_date}.md"
        with open(priority_filename, 'w') as f:
            f.write(priority_report)
        reports["priority_list"] = priority_filename
        
        # Export data files
        json_filename = f"{output_dir}/portfolio_data_{self.report_date}.json"
        self.export_to_json(portfolio_summary, json_filename)
        reports["portfolio_json"] = json_filename
        
        csv_filename = f"{output_dir}/priority_members_{self.report_date}.csv"
        self.export_to_csv(priority_list.head(500), csv_filename)
        reports["priority_csv"] = csv_filename
        
        logger.info("Generated complete portfolio report package: %d files", len(reports))
        
        return reports

