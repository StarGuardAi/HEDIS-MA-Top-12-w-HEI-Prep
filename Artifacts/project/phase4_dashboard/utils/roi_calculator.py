"""
Comprehensive ROI Calculator
Calculates quality bonus impact, Star Rating financial impact, and net ROI
"""
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from scipy import stats

from utils.database import execute_query
from utils.queries import get_roi_by_measure_query, get_portfolio_summary_query


class ROICalculator:
    """
    Comprehensive ROI calculator for HEDIS measures.
    Calculates quality bonuses, Star Rating impact, and net ROI.
    """
    
    def __init__(self):
        # Default assumptions (can be configured)
        self.defaults = {
            "quality_bonus_per_member_per_star": 50.0,  # $50 per member per star rating point
            "members_per_measure": 1000,  # Average members per measure
            "revenue_per_closure": 100.0,  # $100 per successful closure
            "staff_cost_per_hour": 75.0,  # $75 per hour for care coordinator
            "outreach_cost_per_member": 15.0,  # $15 per member outreach
            "lab_cost_per_test": 25.0,  # $25 per lab test
            "confidence_level": 0.95  # 95% confidence interval
        }
    
    def calculate_measure_roi(
        self,
        measure_id: str,
        start_date: str = None,
        end_date: str = None,
        config: Dict = None
    ) -> Dict:
        """
        Calculate comprehensive ROI for a specific measure.
        
        Returns:
            Dictionary with detailed ROI calculations
        """
        if config is None:
            config = self.defaults.copy()
        
        if start_date is None:
            start_date = (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d")
        if end_date is None:
            end_date = datetime.now().strftime("%Y-%m-%d")
        
        # Get measure performance data
        query = get_roi_by_measure_query(start_date, end_date)
        measure_data = execute_query(query)
        
        if measure_data.empty:
            return self._empty_roi_result(measure_id)
        
        # Filter for specific measure
        measure_row = measure_data[measure_data['measure_code'] == measure_id]
        if measure_row.empty:
            return self._empty_roi_result(measure_id)
        
        measure_row = measure_row.iloc[0]
        measure_name = measure_row.get('measure_name', 'Unknown')
        
        # Get detailed intervention data
        intervention_query = f"""
            SELECT 
                COUNT(*) as total_interventions,
                SUM(CASE WHEN mi.status = 'completed' THEN 1 ELSE 0 END) as successful_closures,
                SUM(mi.cost_per_intervention) as total_cost,
                AVG(mi.cost_per_intervention) as avg_cost,
                SUM(CASE WHEN mi.status = 'completed' THEN mi.cost_per_intervention ELSE 0 END) as completed_cost
            FROM member_interventions mi
            WHERE mi.measure_id = '{measure_id}'
            AND mi.intervention_date >= '{start_date}'
            AND mi.intervention_date <= '{end_date}'
        """
        
        intervention_data = execute_query(intervention_query)
        
        if intervention_data.empty:
            return self._empty_roi_result(measure_id)
        
        int_row = intervention_data.iloc[0]
        
        total_interventions = int(int_row.get('total_interventions', 0))
        successful_closures = int(int_row.get('successful_closures', 0))
        total_cost = float(int_row.get('total_cost', 0))
        avg_cost = float(int_row.get('avg_cost', 0))
        completed_cost = float(int_row.get('completed_cost', 0))
        
        # Calculate success rate
        success_rate = (successful_closures / total_interventions * 100) if total_interventions > 0 else 0
        
        # Revenue calculations
        revenue_per_closure = config.get('revenue_per_closure', 100.0)
        total_revenue = successful_closures * revenue_per_closure
        
        # Quality bonus calculation
        # Assumes each star rating point improvement = $X per member
        # Simplified: success rate improvement translates to star rating improvement
        quality_bonus_per_star = config.get('quality_bonus_per_member_per_star', 50.0)
        members_per_measure = config.get('members_per_measure', 1000)
        
        # Estimate star rating impact (simplified model)
        # Higher success rate = higher star rating
        # Assume 85% = 3 stars, 90% = 4 stars, 95% = 5 stars
        if success_rate >= 95:
            star_rating = 5
        elif success_rate >= 90:
            star_rating = 4
        elif success_rate >= 85:
            star_rating = 3
        else:
            star_rating = 2
        
        # Quality bonus = star rating × members × bonus per star
        quality_bonus = star_rating * members_per_measure * quality_bonus_per_star
        
        # Cost breakdown
        # Estimate costs: staff time, outreach, labs
        staff_hours_per_intervention = 0.5  # 30 minutes per intervention
        staff_cost = total_interventions * staff_hours_per_intervention * config.get('staff_cost_per_hour', 75.0)
        
        outreach_cost = total_interventions * config.get('outreach_cost_per_member', 15.0)
        
        # Assume 50% of interventions require lab tests
        lab_tests = int(total_interventions * 0.5)
        lab_cost = lab_tests * config.get('lab_cost_per_test', 25.0)
        
        total_intervention_cost = staff_cost + outreach_cost + lab_cost
        
        # Total costs
        total_costs = total_intervention_cost + completed_cost
        
        # Net ROI
        total_benefit = total_revenue + quality_bonus
        net_roi = total_benefit - total_costs
        roi_ratio = (total_benefit / total_costs) if total_costs > 0 else 0
        
        # Calculate confidence intervals
        confidence_level = config.get('confidence_level', 0.95)
        ci_lower, ci_upper = self._calculate_confidence_interval(
            successful_closures,
            total_interventions,
            confidence_level
        )
        
        # Confidence intervals for ROI
        # Use success rate CI to estimate revenue CI
        revenue_ci_lower = int(total_interventions * (ci_lower / 100) * revenue_per_closure)
        revenue_ci_upper = int(total_interventions * (ci_upper / 100) * revenue_per_closure)
        
        net_roi_ci_lower = revenue_ci_lower + quality_bonus - total_costs
        net_roi_ci_upper = revenue_ci_upper + quality_bonus - total_costs
        
        return {
            "measure_id": measure_id,
            "measure_name": measure_name,
            "period_start": start_date,
            "period_end": end_date,
            "total_interventions": total_interventions,
            "successful_closures": successful_closures,
            "success_rate": success_rate,
            "success_rate_ci_lower": ci_lower,
            "success_rate_ci_upper": ci_upper,
            "total_revenue": total_revenue,
            "revenue_ci_lower": revenue_ci_lower,
            "revenue_ci_upper": revenue_ci_upper,
            "quality_bonus": quality_bonus,
            "star_rating": star_rating,
            "cost_breakdown": {
                "staff_cost": staff_cost,
                "outreach_cost": outreach_cost,
                "lab_cost": lab_cost,
                "intervention_cost": completed_cost,
                "total_cost": total_costs
            },
            "total_costs": total_costs,
            "total_benefit": total_benefit,
            "net_roi": net_roi,
            "net_roi_ci_lower": net_roi_ci_lower,
            "net_roi_ci_upper": net_roi_ci_upper,
            "roi_ratio": roi_ratio,
            "payback_period_months": (total_costs / (total_benefit / 3)) if total_benefit > 0 else None
        }
    
    def _calculate_confidence_interval(
        self,
        successes: int,
        total: int,
        confidence_level: float = 0.95
    ) -> Tuple[float, float]:
        """
        Calculate confidence interval for success rate using binomial distribution.
        """
        if total == 0:
            return (0.0, 0.0)
        
        p = successes / total
        z = stats.norm.ppf((1 + confidence_level) / 2)
        
        # Wilson score interval
        denominator = 1 + (z**2 / total)
        centre_adjusted_probability = (p + (z**2 / (2 * total))) / denominator
        adjusted_standard_deviation = np.sqrt((p * (1 - p) + z**2 / (4 * total)) / total) / denominator
        
        lower_bound = (centre_adjusted_probability - z * adjusted_standard_deviation) * 100
        upper_bound = (centre_adjusted_probability + z * adjusted_standard_deviation) * 100
        
        return (max(0, lower_bound), min(100, upper_bound))
    
    def _empty_roi_result(self, measure_id: str) -> Dict:
        """Return empty ROI result structure."""
        return {
            "measure_id": measure_id,
            "measure_name": "Unknown",
            "total_interventions": 0,
            "successful_closures": 0,
            "success_rate": 0,
            "total_revenue": 0,
            "quality_bonus": 0,
            "total_costs": 0,
            "net_roi": 0,
            "roi_ratio": 0
        }
    
    def generate_sample_roi_results(self, config: Dict = None) -> List[Dict]:
        """
        Generate sample ROI results for demonstration when database is empty.
        
        Args:
            config: Configuration dictionary with default values
            
        Returns:
            List of sample ROI result dictionaries
        """
        if config is None:
            config = self.defaults.copy()
        
        np.random.seed(42)  # Reproducible
        
        sample_measures = [
            {"id": "CDC", "name": "HbA1c Testing (CDC)"},
            {"id": "CBP", "name": "Blood Pressure Control (CBP)"},
            {"id": "COL", "name": "Colorectal Cancer Screening (COL)"},
            {"id": "BCS", "name": "Breast Cancer Screening (BCS)"},
            {"id": "EED", "name": "Diabetes Eye Exam (EED)"}
        ]
        
        sample_results = []
        
        for measure in sample_measures:
            # Generate realistic sample data
            total_interventions = np.random.randint(800, 1500)
            success_rate = np.random.uniform(85, 95)
            successful_closures = int(total_interventions * (success_rate / 100))
            
            # Revenue
            revenue_per_closure = config.get('revenue_per_closure', 100.0)
            total_revenue = successful_closures * revenue_per_closure
            
            # Star rating (based on success rate)
            if success_rate >= 95:
                star_rating = 5
            elif success_rate >= 90:
                star_rating = 4
            elif success_rate >= 85:
                star_rating = 3
            else:
                star_rating = 2
            
            # Quality bonus
            quality_bonus_per_star = config.get('quality_bonus_per_member_per_star', 50.0)
            members_per_measure = config.get('members_per_measure', 1000)
            quality_bonus = star_rating * members_per_measure * quality_bonus_per_star
            
            # Costs
            staff_hours_per_intervention = 0.5
            staff_cost = total_interventions * staff_hours_per_intervention * config.get('staff_cost_per_hour', 75.0)
            outreach_cost = total_interventions * config.get('outreach_cost_per_member', 15.0)
            lab_tests = int(total_interventions * 0.5)
            lab_cost = lab_tests * config.get('lab_cost_per_test', 25.0)
            intervention_cost = np.random.uniform(5000, 15000)
            
            total_costs = staff_cost + outreach_cost + lab_cost + intervention_cost
            
            # Net ROI
            total_benefit = total_revenue + quality_bonus
            net_roi = total_benefit - total_costs
            roi_ratio = (total_benefit / total_costs) if total_costs > 0 else 0
            
            # Confidence intervals
            confidence_level = config.get('confidence_level', 0.95)
            ci_lower, ci_upper = self._calculate_confidence_interval(
                successful_closures,
                total_interventions,
                confidence_level
            )
            
            revenue_ci_lower = int(total_interventions * (ci_lower / 100) * revenue_per_closure)
            revenue_ci_upper = int(total_interventions * (ci_upper / 100) * revenue_per_closure)
            net_roi_ci_lower = revenue_ci_lower + quality_bonus - total_costs
            net_roi_ci_upper = revenue_ci_upper + quality_bonus - total_costs
            
            sample_results.append({
                "measure_id": measure["id"],
                "measure_name": measure["name"],
                "period_start": (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d"),
                "period_end": datetime.now().strftime("%Y-%m-%d"),
                "total_interventions": total_interventions,
                "successful_closures": successful_closures,
                "success_rate": success_rate,
                "success_rate_ci_lower": ci_lower,
                "success_rate_ci_upper": ci_upper,
                "total_revenue": total_revenue,
                "revenue_ci_lower": revenue_ci_lower,
                "revenue_ci_upper": revenue_ci_upper,
                "quality_bonus": quality_bonus,
                "star_rating": star_rating,
                "cost_breakdown": {
                    "staff_cost": staff_cost,
                    "outreach_cost": outreach_cost,
                    "lab_cost": lab_cost,
                    "intervention_cost": intervention_cost,
                    "total_cost": total_costs
                },
                "total_costs": total_costs,
                "total_benefit": total_benefit,
                "net_roi": net_roi,
                "net_roi_ci_lower": net_roi_ci_lower,
                "net_roi_ci_upper": net_roi_ci_upper,
                "roi_ratio": roi_ratio,
                "payback_period_months": (total_costs / (total_benefit / 3)) if total_benefit > 0 else None
            })
        
        return sample_results
    
    def sensitivity_analysis(
        self,
        base_roi: Dict,
        scenarios: List[Dict]
    ) -> pd.DataFrame:
        """
        Perform sensitivity analysis with what-if scenarios.
        
        Args:
            base_roi: Base ROI calculation result
            scenarios: List of scenario dictionaries with parameter changes
        
        Returns:
            DataFrame with scenario results
        """
        results = []
        
        for scenario in scenarios:
            # Clone base ROI
            scenario_roi = base_roi.copy()
            
            # Apply scenario changes
            if 'success_rate' in scenario:
                new_rate = scenario['success_rate']
                scenario_roi['success_rate'] = new_rate
                
                # Recalculate based on new rate
                total_interventions = scenario_roi['total_interventions']
                new_closures = int(total_interventions * (new_rate / 100))
                scenario_roi['successful_closures'] = new_closures
                
                # Recalculate revenue
                revenue_per_closure = 100.0  # Default
                scenario_roi['total_revenue'] = new_closures * revenue_per_closure
                
                # Recalculate quality bonus (if star rating changes)
                if new_rate >= 95:
                    new_star = 5
                elif new_rate >= 90:
                    new_star = 4
                elif new_rate >= 85:
                    new_star = 3
                else:
                    new_star = 2
                
                scenario_roi['star_rating'] = new_star
                quality_bonus_per_star = 50.0
                members_per_measure = 1000
                scenario_roi['quality_bonus'] = new_star * members_per_measure * quality_bonus_per_star
                
                # Recalculate net ROI
                scenario_roi['total_benefit'] = scenario_roi['total_revenue'] + scenario_roi['quality_bonus']
                scenario_roi['net_roi'] = scenario_roi['total_benefit'] - scenario_roi['total_costs']
                scenario_roi['roi_ratio'] = (scenario_roi['total_benefit'] / scenario_roi['total_costs']) if scenario_roi['total_costs'] > 0 else 0
            
            if 'cost_multiplier' in scenario:
                # Adjust costs
                multiplier = scenario['cost_multiplier']
                scenario_roi['total_costs'] = scenario_roi['total_costs'] * multiplier
                scenario_roi['net_roi'] = scenario_roi['total_benefit'] - scenario_roi['total_costs']
                scenario_roi['roi_ratio'] = (scenario_roi['total_benefit'] / scenario_roi['total_costs']) if scenario_roi['total_costs'] > 0 else 0
            
            results.append({
                'scenario_name': scenario.get('name', 'Scenario'),
                'success_rate': scenario_roi['success_rate'],
                'total_revenue': scenario_roi['total_revenue'],
                'quality_bonus': scenario_roi['quality_bonus'],
                'total_costs': scenario_roi['total_costs'],
                'net_roi': scenario_roi['net_roi'],
                'roi_ratio': scenario_roi['roi_ratio'],
                'change_from_base': scenario_roi['net_roi'] - base_roi['net_roi']
            })
        
        return pd.DataFrame(results)
    
    def generate_cfo_report(
        self,
        roi_results: List[Dict],
        portfolio_summary: Dict = None
    ) -> str:
        """
        Generate financial justification report for CFO.
        
        Returns:
            Formatted report text
        """
        report_date = datetime.now().strftime("%Y-%m-%d")
        
        report = f"""
HEDIS PORTFOLIO ROI ANALYSIS - FINANCIAL JUSTIFICATION REPORT
Generated: {report_date}
Prepared for: Chief Financial Officer

================================================================================
EXECUTIVE SUMMARY
================================================================================

This report provides comprehensive ROI analysis for HEDIS intervention programs,
including quality bonus impact, Star Rating financial implications, and net ROI
calculations with confidence intervals.

"""
        
        if portfolio_summary:
            # Helper function to safely get values, handling None
            def safe_get(key, default=0):
                value = portfolio_summary.get(key, default)
                return value if value is not None else default
            
            report += f"""
PORTFOLIO OVERVIEW
------------------
Total Interventions: {safe_get('total_interventions', 0):,}
Successful Closures: {safe_get('total_closures', 0):,}
Overall Success Rate: {safe_get('overall_success_rate', 0):.1f}%
Total Investment: ${safe_get('total_investment', 0):,.2f}
Total Revenue Impact: ${safe_get('revenue_impact', 0):,.2f}
Net Benefit: ${safe_get('net_benefit', 0):,.2f}
ROI Ratio: {safe_get('roi_ratio', 0):.2f}

"""
        
        report += """
================================================================================
MEASURE-BY-MEASURE ROI ANALYSIS
================================================================================

"""
        
        total_portfolio_revenue = 0
        total_portfolio_bonus = 0
        total_portfolio_costs = 0
        total_portfolio_roi = 0
        
        for roi in roi_results:
            measure_name = roi.get('measure_name', 'Unknown')
            success_rate = roi.get('success_rate', 0)
            total_revenue = roi.get('total_revenue', 0)
            quality_bonus = roi.get('quality_bonus', 0)
            total_costs = roi.get('total_costs', 0)
            net_roi = roi.get('net_roi', 0)
            roi_ratio = roi.get('roi_ratio', 0)
            star_rating = roi.get('star_rating', 0)
            
            total_portfolio_revenue += total_revenue
            total_portfolio_bonus += quality_bonus
            total_portfolio_costs += total_costs
            total_portfolio_roi += net_roi
            
            report += f"""
{measure_name}
  Success Rate: {success_rate:.1f}%
  Star Rating Impact: {star_rating} stars
  Revenue from Closures: ${total_revenue:,.2f}
  Quality Bonus Impact: ${quality_bonus:,.2f}
  Total Costs: ${total_costs:,.2f}
  Net ROI: ${net_roi:,.2f}
  ROI Ratio: {roi_ratio:.2f}
  
  Cost Breakdown:
    - Staff Costs: ${roi.get('cost_breakdown', {}).get('staff_cost', 0):,.2f}
    - Outreach Costs: ${roi.get('cost_breakdown', {}).get('outreach_cost', 0):,.2f}
    - Lab Costs: ${roi.get('cost_breakdown', {}).get('lab_cost', 0):,.2f}
    - Intervention Costs: ${roi.get('cost_breakdown', {}).get('intervention_cost', 0):,.2f}

"""
        
        report += f"""
================================================================================
PORTFOLIO SUMMARY
================================================================================

Total Revenue (Closures): ${total_portfolio_revenue:,.2f}
Total Quality Bonus Impact: ${total_portfolio_bonus:,.2f}
Total Intervention Costs: ${total_portfolio_costs:,.2f}
Total Net ROI: ${total_portfolio_roi:,.2f}

Portfolio ROI Ratio: {((total_portfolio_revenue + total_portfolio_bonus) / total_portfolio_costs if total_portfolio_costs > 0 else 0):.2f}

"""
        
        report += """
================================================================================
KEY ASSUMPTIONS
================================================================================

- Revenue per Closure: $100 (standard HEDIS measure revenue)
- Quality Bonus: $50 per member per star rating point
- Staff Cost: $75 per hour (care coordinator)
- Outreach Cost: $15 per member
- Lab Test Cost: $25 per test
- Confidence Intervals: 95% confidence level

"""
        
        report += """
================================================================================
RECOMMENDATIONS
================================================================================

Based on this analysis:

1. Continue investment in high-ROI measures
2. Optimize costs for measures with lower ROI
3. Focus on improving success rates for at-risk measures
4. Monitor quality bonus impact as Star Ratings are updated
5. Review cost structure quarterly to maintain profitability

"""
        
        report += f"""
================================================================================
Report End
Generated: {report_date}
================================================================================
"""
        
        return report

