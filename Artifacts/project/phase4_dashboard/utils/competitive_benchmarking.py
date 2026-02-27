"""
Competitive Benchmarking Analysis Module

Provides comprehensive benchmarking against:
- CMS Star Ratings public data
- HEDIS benchmarks by percentile
- Regional performance data
- National Quality Forum (NQF) standards
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots


class CompetitiveBenchmarking:
    """Competitive benchmarking analysis engine"""
    
    def __init__(self, db_connection=None):
        """Initialize benchmarking engine"""
        self.db = db_connection
        self.benchmark_data = self._load_benchmark_data()
        self.plan_data = self._load_plan_data()
        
    def _load_benchmark_data(self) -> Dict:
        """Load benchmark data from various sources"""
        # In production, this would load from actual CMS/NQF APIs
        # For demo, using synthetic benchmark data
        
        measures = [
            'HbA1c Testing', 'Blood Pressure Control', 'Breast Cancer Screening',
            'Colorectal Cancer Screening', 'Statin Therapy', 'Eye Exam',
            'Nephropathy Screening', 'Flu Vaccination', 'Pneumonia Vaccination',
            'Depression Screening', 'Falls Risk Assessment', 'Medication Review'
        ]
        
        # National benchmarks (percentiles)
        national_benchmarks = {
            '10th': {m: np.random.uniform(20, 40) for m in measures},
            '25th': {m: np.random.uniform(35, 50) for m in measures},
            '50th': {m: np.random.uniform(50, 65) for m in measures},
            '75th': {m: np.random.uniform(65, 80) for m in measures},
            '90th': {m: np.random.uniform(75, 90) for m in measures},
            '95th': {m: np.random.uniform(85, 95) for m in measures}
        }
        
        # Regional benchmarks (by state)
        regional_benchmarks = {}
        states = ['CA', 'TX', 'FL', 'NY', 'PA', 'IL', 'OH', 'GA', 'NC', 'MI']
        for state in states:
            regional_benchmarks[state] = {
                m: np.random.uniform(40, 85) for m in measures
            }
        
        # Similar plan benchmarks (by size and type)
        similar_plan_benchmarks = {
            'size_small': {m: np.random.uniform(45, 70) for m in measures},
            'size_medium': {m: np.random.uniform(50, 75) for m in measures},
            'size_large': {m: np.random.uniform(55, 80) for m in measures},
            'type_hmo': {m: np.random.uniform(50, 75) for m in measures},
            'type_ppo': {m: np.random.uniform(45, 70) for m in measures}
        }
        
        # NQF standards (target rates)
        nqf_standards = {
            m: np.random.uniform(70, 90) for m in measures
        }
        
        return {
            'national': national_benchmarks,
            'regional': regional_benchmarks,
            'similar_plans': similar_plan_benchmarks,
            'nqf_standards': nqf_standards,
            'measures': measures
        }
    
    def _load_plan_data(self) -> Dict:
        """Load current plan performance data"""
        # In production, this would query the database
        # For demo, using synthetic data
        
        measures = self.benchmark_data['measures']
        
        # Current year data
        current_data = {
            m: np.random.uniform(40, 75) for m in measures
        }
        
        # Previous year data (for YoY comparison)
        previous_data = {
            m: max(0, current_data[m] - np.random.uniform(-5, 10))
            for m in measures
        }
        
        # Plan metadata
        plan_metadata = {
            'name': 'Demo Medicare Advantage Plan',
            'state': 'CA',
            'size': 'medium',
            'type': 'HMO',
            'member_count': 50000,
            'current_year': 2024,
            'previous_year': 2023
        }
        
        return {
            'current': current_data,
            'previous': previous_data,
            'metadata': plan_metadata
        }
    
    def get_national_ranking(self, measure: str) -> Dict:
        """Get plan's national percentile ranking for a measure"""
        current_rate = self.plan_data['current'][measure]
        benchmarks = self.benchmark_data['national']
        
        # Determine percentile
        percentile = 50  # Default to median
        if current_rate >= benchmarks['90th'][measure]:
            percentile = 90
        elif current_rate >= benchmarks['75th'][measure]:
            percentile = 75
        elif current_rate >= benchmarks['50th'][measure]:
            percentile = 50
        elif current_rate >= benchmarks['25th'][measure]:
            percentile = 25
        else:
            percentile = 10
        
        gap_to_90th = benchmarks['90th'][measure] - current_rate
        
        return {
            'measure': measure,
            'current_rate': current_rate,
            'percentile': percentile,
            '90th_percentile': benchmarks['90th'][measure],
            'gap_to_90th': gap_to_90th,
            'above_benchmark': current_rate >= benchmarks['50th'][measure]
        }
    
    def get_regional_comparison(self, state: Optional[str] = None) -> Dict:
        """Compare plan to regional benchmarks"""
        if state is None:
            state = self.plan_data['metadata']['state']
        
        regional_rates = self.benchmark_data['regional'][state]
        current_rates = self.plan_data['current']
        
        comparisons = {}
        for measure in self.benchmark_data['measures']:
            plan_rate = current_rates[measure]
            regional_rate = regional_rates[measure]
            
            comparisons[measure] = {
                'plan_rate': plan_rate,
                'regional_rate': regional_rate,
                'difference': plan_rate - regional_rate,
                'above_regional': plan_rate > regional_rate,
                'percent_difference': ((plan_rate - regional_rate) / regional_rate * 100) if regional_rate > 0 else 0
            }
        
        return {
            'state': state,
            'comparisons': comparisons,
            'measures_above': sum(1 for c in comparisons.values() if c['above_regional']),
            'measures_below': sum(1 for c in comparisons.values() if not c['above_regional'])
        }
    
    def get_similar_plan_comparison(self) -> Dict:
        """Compare plan to similar plans (size and type)"""
        plan_metadata = self.plan_data['metadata']
        size_key = f"size_{plan_metadata['size']}"
        type_key = f"type_{plan_metadata['type'].lower()}"
        
        size_benchmarks = self.benchmark_data['similar_plans'][size_key]
        type_benchmarks = self.benchmark_data['similar_plans'][type_key]
        current_rates = self.plan_data['current']
        
        comparisons = {}
        for measure in self.benchmark_data['measures']:
            plan_rate = current_rates[measure]
            size_rate = size_benchmarks[measure]
            type_rate = type_benchmarks[measure]
            
            comparisons[measure] = {
                'plan_rate': plan_rate,
                'size_benchmark': size_rate,
                'type_benchmark': type_rate,
                'above_size': plan_rate > size_rate,
                'above_type': plan_rate > type_rate,
                'avg_benchmark': (size_rate + type_rate) / 2,
                'vs_avg': plan_rate - ((size_rate + type_rate) / 2)
            }
        
        return {
            'size': plan_metadata['size'],
            'type': plan_metadata['type'],
            'comparisons': comparisons
        }
    
    def get_year_over_year(self) -> Dict:
        """Get year-over-year comparison"""
        current = self.plan_data['current']
        previous = self.plan_data['previous']
        
        changes = {}
        for measure in self.benchmark_data['measures']:
            current_rate = current[measure]
            previous_rate = previous[measure]
            change = current_rate - previous_rate
            percent_change = (change / previous_rate * 100) if previous_rate > 0 else 0
            
            changes[measure] = {
                'current': current_rate,
                'previous': previous_rate,
                'change': change,
                'percent_change': percent_change,
                'improving': change > 0,
                'declining': change < 0
            }
        
        improving_count = sum(1 for c in changes.values() if c['improving'])
        declining_count = sum(1 for c in changes.values() if c['declining'])
        
        return {
            'changes': changes,
            'improving_measures': improving_count,
            'declining_measures': declining_count,
            'net_change': sum(c['change'] for c in changes.values()) / len(changes)
        }
    
    def generate_insights(self) -> List[Dict]:
        """Generate actionable insights from benchmarking data"""
        insights = []
        
        # National ranking insights
        for measure in self.benchmark_data['measures']:
            ranking = self.get_national_ranking(measure)
            if ranking['percentile'] < 50:
                insights.append({
                    'type': 'national_ranking',
                    'severity': 'high' if ranking['percentile'] < 25 else 'medium',
                    'measure': measure,
                    'message': f"You rank in the {ranking['percentile']}th percentile nationally on {measure}",
                    'action': f"Improving by {ranking['gap_to_90th']:.1f}% would reach 90th percentile"
                })
        
        # Regional leadership insights
        regional = self.get_regional_comparison()
        top_measures = sorted(
            [(m, c['difference']) for m, c in regional['comparisons'].items()],
            key=lambda x: x[1],
            reverse=True
        )[:3]
        
        for measure, diff in top_measures:
            if diff > 5:
                insights.append({
                    'type': 'regional_leadership',
                    'severity': 'low',
                    'measure': measure,
                    'message': f"You lead your region in {measure}",
                    'action': 'Maintain this competitive advantage'
                })
        
        # Improvement opportunity insights
        yoy = self.get_year_over_year()
        declining = [(m, c) for m, c in yoy['changes'].items() if c['declining']]
        declining.sort(key=lambda x: abs(x[1]['change']), reverse=True)
        
        for measure, change_data in declining[:3]:
            insights.append({
                'type': 'declining_performance',
                'severity': 'high',
                'measure': measure,
                'message': f"{measure} declined by {abs(change_data['change']):.1f}% year-over-year",
                'action': 'Investigate root cause and implement corrective actions'
            })
        
        # Top quartile opportunity insights
        for measure in self.benchmark_data['measures']:
            ranking = self.get_national_ranking(measure)
            if ranking['percentile'] < 75 and ranking['gap_to_90th'] < 10:
                insights.append({
                    'type': 'improvement_opportunity',
                    'severity': 'medium',
                    'measure': measure,
                    'message': f"Improving {measure} by {ranking['gap_to_90th']:.1f}% would move you to top quartile",
                    'action': f"Target improvement: {ranking['gap_to_90th']:.1f} percentage points"
                })
        
        return sorted(insights, key=lambda x: {'high': 3, 'medium': 2, 'low': 1}[x['severity']], reverse=True)
    
    def create_radar_chart(self, comparison_type: str = 'national') -> go.Figure:
        """Create radar chart comparing plan to benchmarks"""
        measures = self.benchmark_data['measures']
        plan_rates = [self.plan_data['current'][m] for m in measures]
        
        if comparison_type == 'national':
            benchmark_rates = [self.benchmark_data['national']['75th'][m] for m in measures]
            benchmark_label = '75th Percentile'
        elif comparison_type == 'regional':
            state = self.plan_data['metadata']['state']
            benchmark_rates = [self.benchmark_data['regional'][state][m] for m in measures]
            benchmark_label = f'{state} Regional Average'
        else:
            plan_metadata = self.plan_data['metadata']
            size_key = f"size_{plan_metadata['size']}"
            benchmark_rates = [self.benchmark_data['similar_plans'][size_key][m] for m in measures]
            benchmark_label = f'Similar {plan_metadata["size"].title()} Plans'
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=plan_rates + [plan_rates[0]],  # Close the loop
            theta=measures + [measures[0]],
            fill='toself',
            name='Your Plan',
            line_color='#1f77b4'
        ))
        
        fig.add_trace(go.Scatterpolar(
            r=benchmark_rates + [benchmark_rates[0]],
            theta=measures + [measures[0]],
            fill='toself',
            name=benchmark_label,
            line_color='#ff7f0e'
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )),
            showlegend=True,
            title=f'Performance Comparison: {comparison_type.title()}',
            height=600
        )
        
        return fig
    
    def create_benchmark_bands_chart(self, measure: str) -> go.Figure:
        """Create benchmark bands visualization for a measure"""
        ranking = self.get_national_ranking(measure)
        benchmarks = self.benchmark_data['national']
        
        percentiles = ['10th', '25th', '50th', '75th', '90th', '95th']
        values = [benchmarks[p][measure] for p in percentiles]
        labels = [p.replace('th', '') for p in percentiles]
        
        fig = go.Figure()
        
        # Add benchmark bands
        colors = ['#d62728', '#ff7f0e', '#ffbb78', '#2ca02c', '#1f77b4', '#9467bd']
        for i, (label, value, color) in enumerate(zip(labels, values, colors)):
            fig.add_trace(go.Bar(
                x=[label],
                y=[value],
                name=label,
                marker_color=color,
                showlegend=False
            ))
        
        # Add plan performance line
        fig.add_trace(go.Scatter(
            x=labels,
            y=[ranking['current_rate']] * len(labels),
            mode='lines+markers',
            name='Your Plan',
            line=dict(color='black', width=3),
            marker=dict(size=10)
        ))
        
        fig.update_layout(
            title=f'{measure} - Benchmark Comparison',
            xaxis_title='Percentile',
            yaxis_title='Rate (%)',
            height=400,
            hovermode='x unified'
        )
        
        return fig
    
    def create_performance_distribution(self, measure: str) -> go.Figure:
        """Create performance distribution curve"""
        # Simulate distribution of plan performance
        mean = self.benchmark_data['national']['50th'][measure]
        std = (self.benchmark_data['national']['90th'][measure] - 
               self.benchmark_data['national']['10th'][measure]) / 3
        
        x = np.linspace(0, 100, 1000)
        y = np.exp(-0.5 * ((x - mean) / std) ** 2) / (std * np.sqrt(2 * np.pi))
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=x,
            y=y,
            mode='lines',
            name='Market Distribution',
            fill='tozeroy',
            line_color='#1f77b4'
        ))
        
        # Mark plan position
        plan_rate = self.plan_data['current'][measure]
        plan_y = np.exp(-0.5 * ((plan_rate - mean) / std) ** 2) / (std * np.sqrt(2 * np.pi))
        
        fig.add_trace(go.Scatter(
            x=[plan_rate],
            y=[plan_y],
            mode='markers',
            name='Your Plan',
            marker=dict(size=15, color='red', symbol='diamond')
        ))
        
        # Add percentile markers
        benchmarks = self.benchmark_data['national']
        for percentile, value in [('50th', benchmarks['50th'][measure]),
                                   ('75th', benchmarks['75th'][measure]),
                                   ('90th', benchmarks['90th'][measure])]:
            y_val = np.exp(-0.5 * ((value - mean) / std) ** 2) / (std * np.sqrt(2 * np.pi))
            fig.add_trace(go.Scatter(
                x=[value],
                y=[y_val],
                mode='markers',
                name=f'{percentile} Percentile',
                marker=dict(size=10, color='orange', symbol='triangle-up'),
                showlegend=True
            ))
        
        fig.update_layout(
            title=f'{measure} - Performance Distribution',
            xaxis_title='Rate (%)',
            yaxis_title='Density',
            height=400
        )
        
        return fig
    
    def create_market_share_scatter(self) -> go.Figure:
        """Create market share vs quality scatter plot"""
        # Simulate market data
        np.random.seed(42)
        n_plans = 50
        market_share = np.random.uniform(1, 20, n_plans)
        quality_score = np.random.uniform(40, 90, n_plans)
        
        # Calculate plan's position
        plan_metadata = self.plan_data['metadata']
        plan_share = 5.0  # Example
        avg_rate = np.mean(list(self.plan_data['current'].values()))
        plan_quality = avg_rate
        
        fig = go.Figure()
        
        # Other plans
        fig.add_trace(go.Scatter(
            x=market_share,
            y=quality_score,
            mode='markers',
            name='Other Plans',
            marker=dict(size=10, color='lightblue', opacity=0.6)
        ))
        
        # Your plan
        fig.add_trace(go.Scatter(
            x=[plan_share],
            y=[plan_quality],
            mode='markers',
            name='Your Plan',
            marker=dict(size=20, color='red', symbol='star')
        ))
        
        fig.update_layout(
            title='Market Share vs Quality Score',
            xaxis_title='Market Share (%)',
            yaxis_title='Quality Score (%)',
            height=500
        )
        
        return fig
    
    def get_summary_statistics(self) -> Dict:
        """Get overall summary statistics"""
        rankings = [self.get_national_ranking(m) for m in self.benchmark_data['measures']]
        avg_percentile = np.mean([r['percentile'] for r in rankings])
        
        regional = self.get_regional_comparison()
        measures_above_regional = regional['measures_above']
        
        yoy = self.get_year_over_year()
        improving_measures = yoy['improving_measures']
        
        return {
            'avg_national_percentile': avg_percentile,
            'measures_above_regional': measures_above_regional,
            'total_measures': len(self.benchmark_data['measures']),
            'improving_measures': improving_measures,
            'top_quartile_measures': sum(1 for r in rankings if r['percentile'] >= 75),
            'bottom_quartile_measures': sum(1 for r in rankings if r['percentile'] < 25)
        }

