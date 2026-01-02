"""
Historical Performance Tracking
Tracks HEDIS measure performance over time with forecasting
"""
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

from utils.database import execute_query
from utils.queries import get_roi_by_measure_query


class HistoricalTracker:
    """
    Tracks historical performance of HEDIS measures with forecasting.
    """
    
    def __init__(self):
        self.forecast_method = "prophet"  # or "arima"
    
    def get_monthly_trends(
        self,
        measure_id: Optional[str] = None,
        start_date: str = None,
        end_date: str = None
    ) -> pd.DataFrame:
        """
        Get monthly trend data for measures.
        
        Returns:
            DataFrame with monthly performance metrics
        """
        if start_date is None:
            start_date = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")
        if end_date is None:
            end_date = datetime.now().strftime("%Y-%m-%d")
        
        query = f"""
            SELECT 
                strftime('%Y-%m', mi.intervention_date) as month,
                date(mi.intervention_date, 'start of month') as month_start,
                mi.measure_id,
                hm.measure_name,
                COUNT(*) as total_interventions,
                SUM(CASE WHEN mi.status = 'completed' THEN 1 ELSE 0 END) as successful_closures,
                ROUND(
                    CAST(SUM(CASE WHEN mi.status = 'completed' THEN 1 ELSE 0 END) AS REAL) * 100.0 / 
                    NULLIF(COUNT(*), 0),
                    1
                ) as success_rate,
                ROUND(SUM(CASE WHEN mi.status = 'completed' THEN mi.cost_per_intervention ELSE 0 END), 2) as total_cost,
                SUM(CASE WHEN mi.status = 'completed' THEN 1 ELSE 0 END) * 100.0 as revenue
            FROM member_interventions mi
            LEFT JOIN hedis_measures hm ON mi.measure_id = hm.measure_id
            WHERE mi.intervention_date >= '{start_date}'
            AND mi.intervention_date <= '{end_date}'
        """
        
        if measure_id:
            query += f" AND mi.measure_id = '{measure_id}'"
        
        query += """
            GROUP BY strftime('%Y-%m', mi.intervention_date), date(mi.intervention_date, 'start of month'), 
                     mi.measure_id, hm.measure_name
            ORDER BY month_start ASC, mi.measure_id
        """
        
        return execute_query(query)
    
    def get_year_over_year_comparison(
        self,
        measure_id: Optional[str] = None,
        current_year: int = None
    ) -> pd.DataFrame:
        """
        Get year-over-year comparison data.
        
        Returns:
            DataFrame with YoY comparison metrics
        """
        if current_year is None:
            current_year = datetime.now().year
        
        current_start = f"{current_year}-01-01"
        current_end = datetime.now().strftime("%Y-%m-%d")
        
        previous_year = current_year - 1
        previous_start = f"{previous_year}-01-01"
        previous_end = f"{previous_year}-12-31"
        
        # Get current year data
        current_query = f"""
            SELECT 
                mi.measure_id,
                hm.measure_name,
                COUNT(*) as total_interventions,
                SUM(CASE WHEN mi.status = 'completed' THEN 1 ELSE 0 END) as successful_closures,
                ROUND(
                    CAST(SUM(CASE WHEN mi.status = 'completed' THEN 1 ELSE 0 END) AS REAL) * 100.0 / 
                    NULLIF(COUNT(*), 0),
                    1
                ) as success_rate,
                SUM(CASE WHEN mi.status = 'completed' THEN 1 ELSE 0 END) * 100.0 as revenue
            FROM member_interventions mi
            LEFT JOIN hedis_measures hm ON mi.measure_id = hm.measure_id
            WHERE mi.intervention_date >= '{current_start}'
            AND mi.intervention_date <= '{current_end}'
        """
        
        if measure_id:
            current_query += f" AND mi.measure_id = '{measure_id}'"
        
        current_query += " GROUP BY mi.measure_id, hm.measure_name"
        
        current_data = execute_query(current_query)
        current_data['period'] = f"{current_year} YTD"
        
        # Get previous year data
        previous_query = f"""
            SELECT 
                mi.measure_id,
                hm.measure_name,
                COUNT(*) as total_interventions,
                SUM(CASE WHEN mi.status = 'completed' THEN 1 ELSE 0 END) as successful_closures,
                ROUND(
                    CAST(SUM(CASE WHEN mi.status = 'completed' THEN 1 ELSE 0 END) AS REAL) * 100.0 / 
                    NULLIF(COUNT(*), 0),
                    1
                ) as success_rate,
                SUM(CASE WHEN mi.status = 'completed' THEN 1 ELSE 0 END) * 100.0 as revenue
            FROM member_interventions mi
            LEFT JOIN hedis_measures hm ON mi.measure_id = hm.measure_id
            WHERE mi.intervention_date >= '{previous_start}'
            AND mi.intervention_date <= '{previous_end}'
        """
        
        if measure_id:
            previous_query += f" AND mi.measure_id = '{measure_id}'"
        
        previous_query += " GROUP BY mi.measure_id, hm.measure_name"
        
        previous_data = execute_query(previous_query)
        previous_data['period'] = f"{previous_year} Full Year"
        
        # Combine and calculate changes
        if not current_data.empty and not previous_data.empty:
            combined = pd.concat([current_data, previous_data], ignore_index=True)
            
            # Calculate YoY changes
            yoy_data = []
            for measure_id in combined['measure_id'].unique():
                current_row = current_data[current_data['measure_id'] == measure_id]
                previous_row = previous_data[previous_data['measure_id'] == measure_id]
                
                if not current_row.empty and not previous_row.empty:
                    curr = current_row.iloc[0]
                    prev = previous_row.iloc[0]
                    
                    success_rate_change = curr['success_rate'] - prev['success_rate']
                    revenue_change = curr['revenue'] - prev['revenue']
                    revenue_change_pct = ((curr['revenue'] - prev['revenue']) / prev['revenue'] * 100) if prev['revenue'] > 0 else 0
                    
                    yoy_data.append({
                        'measure_id': measure_id,
                        'measure_name': curr['measure_name'],
                        'current_success_rate': curr['success_rate'],
                        'previous_success_rate': prev['success_rate'],
                        'success_rate_change': success_rate_change,
                        'current_revenue': curr['revenue'],
                        'previous_revenue': prev['revenue'],
                        'revenue_change': revenue_change,
                        'revenue_change_pct': revenue_change_pct,
                        'current_interventions': curr['total_interventions'],
                        'previous_interventions': prev['total_interventions']
                    })
            
            return pd.DataFrame(yoy_data)
        
        return pd.DataFrame()
    
    def detect_seasonal_patterns(
        self,
        measure_id: Optional[str] = None,
        start_date: str = None,
        end_date: str = None
    ) -> Dict:
        """
        Detect seasonal patterns in performance.
        
        Returns:
            Dictionary with seasonal pattern information
        """
        trends = self.get_monthly_trends(measure_id, start_date, end_date)
        
        if trends.empty:
            return {
                "has_seasonality": False,
                "peak_month": None,
                "low_month": None,
                "seasonal_variance": 0
            }
        
        # Group by month (1-12) to find patterns
        trends['month_num'] = pd.to_datetime(trends['month']).dt.month
        monthly_avg = trends.groupby('month_num')['success_rate'].mean()
        
        if len(monthly_avg) >= 3:  # Need at least 3 months of data
            peak_month = monthly_avg.idxmax()
            low_month = monthly_avg.idxmin()
            variance = monthly_avg.std()
            
            # Determine if there's significant seasonality (variance > 5%)
            has_seasonality = variance > 5.0
            
            month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                          'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            
            return {
                "has_seasonality": has_seasonality,
                "peak_month": month_names[peak_month - 1] if peak_month else None,
                "low_month": month_names[low_month - 1] if low_month else None,
                "seasonal_variance": float(variance),
                "monthly_averages": monthly_avg.to_dict()
            }
        
        return {
            "has_seasonality": False,
            "peak_month": None,
            "low_month": None,
            "seasonal_variance": 0
        }
    
    def forecast_next_quarter(
        self,
        measure_id: Optional[str] = None,
        method: str = "prophet"
    ) -> pd.DataFrame:
        """
        Forecast next quarter performance.
        
        Uses simple linear trend if Prophet/ARIMA not available.
        
        Returns:
            DataFrame with forecasted metrics
        """
        # Get historical data
        start_date = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")
        end_date = datetime.now().strftime("%Y-%m-%d")
        
        trends = self.get_monthly_trends(measure_id, start_date, end_date)
        
        if trends.empty:
            return pd.DataFrame()
        
        # Simple forecasting using linear trend
        # Group by month and calculate trend
        trends['month_start'] = pd.to_datetime(trends['month_start'])
        trends = trends.sort_values('month_start')
        
        # Calculate forecast for next 3 months
        last_month = trends['month_start'].max()
        forecast_months = []
        
        for i in range(1, 4):  # Next 3 months
            forecast_date = last_month + pd.DateOffset(months=i)
            forecast_months.append(forecast_date)
        
        # Simple linear trend forecast
        if len(trends) >= 3:
            # Calculate average growth rate
            recent_trends = trends.tail(6)  # Last 6 months
            if len(recent_trends) >= 2:
                success_rate_trend = recent_trends['success_rate'].values
                intervention_trend = recent_trends['total_interventions'].values
                
                # Linear regression for trend
                x = np.arange(len(success_rate_trend))
                success_rate_slope = np.polyfit(x, success_rate_trend, 1)[0] if len(success_rate_trend) > 1 else 0
                intervention_slope = np.polyfit(x, intervention_trend, 1)[0] if len(intervention_trend) > 1 else 0
                
                # Forecast
                forecasts = []
                last_success_rate = success_rate_trend[-1]
                last_interventions = intervention_trend[-1]
                
                for i, forecast_date in enumerate(forecast_months):
                    forecast_success_rate = last_success_rate + (success_rate_slope * (i + 1))
                    forecast_interventions = max(0, last_interventions + (intervention_slope * (i + 1)))
                    forecast_closures = int(forecast_interventions * (forecast_success_rate / 100))
                    forecast_revenue = forecast_closures * 100.0
                    
                    forecasts.append({
                        'month': forecast_date.strftime('%Y-%m'),
                        'month_start': forecast_date.strftime('%Y-%m-%d'),
                        'measure_id': trends['measure_id'].iloc[0] if not trends.empty else measure_id,
                        'measure_name': trends['measure_name'].iloc[0] if not trends.empty else 'Unknown',
                        'forecasted_interventions': int(forecast_interventions),
                        'forecasted_success_rate': float(forecast_success_rate),
                        'forecasted_closures': forecast_closures,
                        'forecasted_revenue': float(forecast_revenue),
                        'is_forecast': True
                    })
                
                return pd.DataFrame(forecasts)
        
        return pd.DataFrame()
    
    def calculate_status(
        self,
        measure_id: str,
        target_success_rate: float = 85.0,
        lookback_months: int = 3
    ) -> Dict:
        """
        Calculate 'On Track' vs 'At Risk' status.
        
        Returns:
            Dictionary with status information
        """
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=lookback_months * 30)).strftime("%Y-%m-%d")
        
        # Try getting trends - if empty, try wider date range
        trends = self.get_monthly_trends(measure_id, start_date, end_date)
        
        # If no data in recent period, try last 6 months
        if trends.empty:
            start_date = (datetime.now() - timedelta(days=180)).strftime("%Y-%m-%d")
            trends = self.get_monthly_trends(measure_id, start_date, end_date)
        
        # If still empty, try last year
        if trends.empty:
            start_date = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")
            trends = self.get_monthly_trends(measure_id, start_date, end_date)
        
        if trends.empty:
            return {
                "status": "unknown",
                "current_rate": 0.0,
                "target_rate": target_success_rate,
                "variance": -target_success_rate,
                "trend": "stable"
            }
        
        # Calculate recent average - use available data
        # If we have less data than requested, use what we have
        num_months = min(lookback_months, len(trends))
        has_actual_data = False
        total_interventions = 0
        
        if num_months > 0:
            recent_trends = trends.tail(num_months)
            # Check if we have actual intervention data
            total_interventions = 0
            total_completed = 0
            
            if 'total_interventions' in recent_trends.columns:
                total_interventions = int(recent_trends['total_interventions'].sum())
            
            if 'successful_closures' in recent_trends.columns:
                total_completed = int(recent_trends['successful_closures'].sum())
            
            # We need at least some completed interventions to have performance data
            has_actual_data = total_interventions > 0 and total_completed > 0
            
            # Handle NaN values in success_rate
            success_rates = recent_trends['success_rate'].dropna()
            if len(success_rates) > 0:
                avg_success_rate = float(success_rates.mean())
                # Even if we have a rate, if no interventions completed, we don't have real data
                if total_completed == 0:
                    has_actual_data = False
                    avg_success_rate = 0.0
            else:
                avg_success_rate = 0.0
                has_actual_data = False
        else:
            avg_success_rate = 0.0
            recent_trends = pd.DataFrame()
            has_actual_data = False
            total_interventions = 0
            total_completed = 0
        
        # If no completed interventions exist, return unknown status
        # (We can't assess performance without any completed work)
        if not has_actual_data or total_completed == 0:
            return {
                "status": "unknown",
                "current_rate": 0.0,
                "target_rate": target_success_rate,
                "variance": -target_success_rate,
                "trend": "stable",
                "has_data": False
            }
        
        # Determine trend (only if we have data)
        if len(recent_trends) >= 2:
            rates = recent_trends['success_rate'].dropna().values
            if len(rates) >= 2:
                trend_slope = (rates[-1] - rates[0]) / len(rates) if len(rates) > 1 else 0
                trend = "improving" if trend_slope > 0.5 else ("declining" if trend_slope < -0.5 else "stable")
            else:
                trend = "stable"
        else:
            trend = "stable"
        
        # Determine status based on actual performance
        variance = avg_success_rate - target_success_rate
        
        if avg_success_rate >= target_success_rate:
            status = "on_track"
        elif avg_success_rate >= target_success_rate * 0.9:
            status = "at_risk"
        else:
            status = "critical"
        
        return {
            "status": status,
            "current_rate": float(avg_success_rate),
            "target_rate": target_success_rate,
            "variance": float(variance),
            "trend": trend,
            "months_analyzed": len(recent_trends),
            "has_data": True
        }
    
    def get_all_measures_status(
        self,
        target_success_rate: float = 85.0
    ) -> pd.DataFrame:
        """
        Get status for all measures.
        
        Returns:
            DataFrame with status for each measure
        """
        # Get all measures
        measures_query = """
            SELECT DISTINCT mi.measure_id, hm.measure_name
            FROM member_interventions mi
            LEFT JOIN hedis_measures hm ON mi.measure_id = hm.measure_id
            ORDER BY hm.measure_name
        """
        
        measures = execute_query(measures_query)
        
        if measures.empty:
            return pd.DataFrame()
        
        status_data = []
        for _, row in measures.iterrows():
            measure_id = row['measure_id']
            measure_name = row['measure_name']
            
            status = self.calculate_status(measure_id, target_success_rate)
            
            status_data.append({
                'measure_id': measure_id,
                'measure_name': measure_name,
                'status': status['status'],
                'current_rate': status['current_rate'],
                'target_rate': status['target_rate'],
                'variance': status['variance'],
                'trend': status['trend']
            })
        
        return pd.DataFrame(status_data)

