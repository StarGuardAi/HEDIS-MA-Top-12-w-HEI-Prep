"""
Portfolio Service

Business logic for portfolio-level operations and aggregations.
"""
from typing import Dict, Any
import pandas as pd

from src.data.loaders import load_portfolio_summary, load_measures_data
from src.services.member_service import MemberService
from src.services.roi_service import ROIService
from src.services.star_rating_service import StarRatingService
from infrastructure.cache import cached


class PortfolioService:
    """Service for portfolio-level business logic"""
    
    def __init__(self):
        self.member_service = MemberService()
        self.roi_service = ROIService()
        self.star_rating_service = StarRatingService()
    
    @cached(prefix="portfolio_summary", ttl=3600)
    def get_portfolio_summary(self) -> pd.DataFrame:
        """
        Get portfolio-level summary data
        
        Returns:
            DataFrame with portfolio summary
        """
        return load_portfolio_summary()
    
    def get_portfolio_kpis(self) -> Dict[str, Any]:
        """
        Get key portfolio KPIs
        
        Returns:
            Dictionary with KPI values
        """
        # Get member statistics
        member_stats = self.member_service.get_member_statistics()
        
        # Get ROI summary
        roi_summary = self.roi_service.get_roi_summary()
        
        # Get star rating summary
        rating_summary = self.star_rating_service.get_rating_summary()
        
        # Get measures summary
        measures_df = load_measures_data()
        avg_compliance = measures_df['current_rate'].mean() if not measures_df.empty and 'current_rate' in measures_df.columns else 0.0
        
        return {
            'roi_percentage': roi_summary.get('roi_percentage', 0),
            'star_rating': rating_summary.get('overall_rating', 4.0),
            'member_count': member_stats.get('total_members', 0),
            'compliance_rate': avg_compliance,
            'total_value': member_stats.get('total_value', 0.0),
            'open_gaps': member_stats.get('open_gaps', 0)
        }
    
    def get_portfolio_overview(self) -> Dict[str, Any]:
        """
        Get comprehensive portfolio overview
        
        Returns:
            Dictionary with portfolio overview data
        """
        kpis = self.get_portfolio_kpis()
        measures_df = load_measures_data()
        
        return {
            'kpis': kpis,
            'total_measures': len(measures_df) if not measures_df.empty else 0,
            'measures_data': measures_df.to_dict('records') if not measures_df.empty else []
        }

