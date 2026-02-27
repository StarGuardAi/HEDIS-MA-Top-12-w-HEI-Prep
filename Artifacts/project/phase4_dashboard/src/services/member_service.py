"""
Member Service

Business logic for member-related operations.
"""
from typing import List, Optional, Dict, Any
import pandas as pd
from datetime import datetime

from domain.entities import Member
from src.data.loaders import load_member_data
from infrastructure.database import get_db_manager
from infrastructure.cache import cached


class MemberService:
    """Service for member-related business logic"""
    
    def __init__(self):
        self.db_manager = get_db_manager()
    
    @cached(prefix="members", ttl=3600)
    def get_all_members(
        self,
        date_range: Optional[tuple] = None,
        measures: Optional[List[str]] = None
    ) -> pd.DataFrame:
        """
        Get all members with optional filtering
        
        Args:
            date_range: Optional tuple of (start_date, end_date)
            measures: Optional list of measure names to filter
        
        Returns:
            DataFrame with member data
        """
        return load_member_data(date_range=date_range, measures=measures)
    
    def get_member_by_id(self, member_id: str) -> Optional[Member]:
        """
        Get a specific member by ID
        
        Args:
            member_id: Member identifier
        
        Returns:
            Member entity or None if not found
        """
        df = load_member_data()
        member_data = df[df['member_id'] == member_id]
        
        if member_data.empty:
            return None
        
        row = member_data.iloc[0]
        # Convert to Member entity
        # This is a simplified version - in production, would map from database
        return None  # Placeholder - would create Member from row data
    
    def get_high_priority_members(
        self,
        min_priority: float = 0.7,
        measures: Optional[List[str]] = None
    ) -> pd.DataFrame:
        """
        Get members with high priority scores
        
        Args:
            min_priority: Minimum priority score
            measures: Optional measure filter
        
        Returns:
            DataFrame of high-priority members
        """
        df = load_member_data(measures=measures)
        
        if 'predicted_closure_probability' in df.columns:
            return df[df['predicted_closure_probability'] >= min_priority]
        
        return df
    
    def get_member_statistics(self) -> Dict[str, Any]:
        """
        Get aggregate member statistics
        
        Returns:
            Dictionary with statistics
        """
        df = load_member_data()
        
        if df.empty:
            return {
                'total_members': 0,
                'open_gaps': 0,
                'avg_closure_probability': 0.0,
                'total_value': 0.0
            }
        
        stats = {
            'total_members': len(df),
            'open_gaps': len(df[df.get('gap_status', '') == 'Open']) if 'gap_status' in df.columns else 0,
            'avg_closure_probability': df['predicted_closure_probability'].mean() if 'predicted_closure_probability' in df.columns else 0.0,
            'total_value': df['financial_value'].sum() if 'financial_value' in df.columns else 0.0
        }
        
        return stats

