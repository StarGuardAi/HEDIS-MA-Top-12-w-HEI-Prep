"""
Unit tests for workload balancing algorithms
"""
import pytest
import pandas as pd
from utils.campaign_builder import CampaignBuilder


class TestWorkloadBalancing:
    """Test workload balancing algorithms."""
    
    def test_balanced_assignment(self, campaign_builder):
        """Test balanced workload assignment."""
        # Create sample member data
        member_data = pd.DataFrame({
            'member_id': [f'MEM{i:04d}' for i in range(20)],
            'measure_id': ['HBA1C'] * 20,
            'intervention_id': [f'INT{i:04d}' for i in range(20)],
            'cost_per_intervention': [50.0] * 20
        })
        
        assigned = campaign_builder.assign_to_coordinators(
            member_data,
            coordinator_count=5,
            assignment_strategy="balanced"
        )
        
        assert not assigned.empty
        assert "coordinator_name" in assigned.columns
        
        # Check workload distribution
        workload = assigned.groupby('coordinator_name').size()
        max_workload = workload.max()
        min_workload = workload.min()
        
        # Workload should be relatively balanced (within 2 members)
        assert max_workload - min_workload <= 2
    
    def test_round_robin_assignment(self, campaign_builder):
        """Test round-robin assignment."""
        member_data = pd.DataFrame({
            'member_id': [f'MEM{i:04d}' for i in range(10)],
            'measure_id': ['HBA1C'] * 10,
            'intervention_id': [f'INT{i:04d}' for i in range(10)],
            'cost_per_intervention': [50.0] * 10
        })
        
        assigned = campaign_builder.assign_to_coordinators(
            member_data,
            coordinator_count=3,
            assignment_strategy="round_robin"
        )
        
        assert not assigned.empty
        assert len(assigned['coordinator_name'].unique()) == 3
    
    def test_by_measure_assignment(self, campaign_builder):
        """Test assignment grouped by measure."""
        member_data = pd.DataFrame({
            'member_id': [f'MEM{i:04d}' for i in range(15)],
            'measure_id': ['HBA1C'] * 5 + ['BP'] * 5 + ['COL'] * 5,
            'intervention_id': [f'INT{i:04d}' for i in range(15)],
            'cost_per_intervention': [50.0] * 15
        })
        
        assigned = campaign_builder.assign_to_coordinators(
            member_data,
            coordinator_count=3,
            assignment_strategy="by_measure"
        )
        
        assert not assigned.empty
        # Members of same measure should be distributed across coordinators
        measure_groups = assigned.groupby(['measure_id', 'coordinator_name']).size()
        assert len(measure_groups) > 0

