"""
Campaign Builder Engine
Handles member selection, metrics calculation, and care coordinator assignment
"""
from typing import Dict, List, Optional, Tuple
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import uuid

from utils.database import execute_query


class CampaignBuilder:
    """
    Builds and manages HEDIS intervention campaigns.
    Handles member selection, metrics calculation, and workload balancing.
    """
    
    def __init__(self):
        self.campaigns = {}  # Store campaigns in memory (could use database)
    
    def get_available_members(
        self,
        measure_id: Optional[str] = None,
        status_filter: List[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> pd.DataFrame:
        """
        Get list of members available for campaign selection.
        
        Args:
            measure_id: Filter by specific measure
            status_filter: List of statuses to include (e.g., ['pending', 'scheduled'])
            start_date: Filter by intervention date start
            end_date: Filter by intervention date end
        
        Returns:
            DataFrame with member information
        """
        if status_filter is None:
            status_filter = ['pending', 'scheduled']
        
        # Build status filter
        status_list = "','".join(status_filter)
        base_query = f"""
            SELECT DISTINCT
                mi.member_id,
                mi.intervention_id,
                mi.measure_id,
                hm.measure_name,
                mi.intervention_date,
                mi.status,
                mi.cost_per_intervention,
                CASE 
                    WHEN mi.status = 'completed' THEN 1 
                    ELSE 0 
                END as historical_success,
                'Member ' || mi.member_id as member_name,
                '' as member_phone,
                '' as member_email
            FROM member_interventions mi
            LEFT JOIN hedis_measures hm ON mi.measure_id = hm.measure_id
            WHERE mi.status IN ('{status_list}')
        """
        
        params = []
        
        if measure_id:
            base_query += f" AND mi.measure_id = '{measure_id}'"
        
        # Make date filters optional - only apply if provided
        # If no dates provided, show all matching status records
        if start_date and start_date.strip():
            base_query += f" AND mi.intervention_date >= '{start_date}'"
        
        if end_date and end_date.strip():
            base_query += f" AND mi.intervention_date <= '{end_date}'"
        
        base_query += " ORDER BY mi.intervention_date ASC, mi.member_id"
        
        return execute_query(base_query)
    
    def calculate_campaign_metrics(
        self,
        member_ids: List[str],
        intervention_ids: Optional[List[str]] = None
    ) -> Dict:
        """
        Calculate campaign metrics for selected members.
        
        Args:
            member_ids: List of member IDs
            intervention_ids: Optional list of specific intervention IDs
        
        Returns:
            Dictionary with campaign metrics
        """
        if not member_ids:
            return {
                "total_members": 0,
                "total_value": 0,
                "predicted_success_rate": 0,
                "predicted_closures": 0,
                "predicted_revenue": 0,
                "total_cost": 0,
                "predicted_net_benefit": 0,
                "required_fte": 0,
                "avg_cost_per_member": 0
            }
        
        # Get member data
        member_list = "','".join(member_ids)
        query = f"""
            SELECT 
                mi.member_id,
                mi.intervention_id,
                mi.cost_per_intervention,
                mi.measure_id,
                hm.measure_name,
                CASE WHEN mi.status = 'completed' THEN 1 ELSE 0 END as historical_success
            FROM member_interventions mi
            LEFT JOIN hedis_measures hm ON mi.measure_id = hm.measure_id
            WHERE mi.member_id IN ('{member_list}')
        """
        
        if intervention_ids:
            intervention_list = "','".join(intervention_ids)
            query += f" AND mi.intervention_id IN ('{intervention_list}')"
        
        member_data = execute_query(query)
        
        if member_data.empty:
            return {
                "total_members": 0,
                "total_value": 0,
                "predicted_success_rate": 0,
                "predicted_closures": 0,
                "predicted_revenue": 0,
                "total_cost": 0,
                "predicted_net_benefit": 0,
                "required_fte": 0,
                "avg_cost_per_member": 0
            }
        
        # Calculate metrics
        total_members = member_data['member_id'].nunique()
        total_interventions = len(member_data)
        total_cost = float(member_data['cost_per_intervention'].sum())
        avg_cost_per_member = total_cost / total_members if total_members > 0 else 0
        
        # Calculate predicted success rate from historical data
        # Get overall success rate from similar interventions
        member_list = "','".join(member_ids)
        historical_query = f"""
            SELECT 
                AVG(CASE WHEN status = 'completed' THEN 1.0 ELSE 0.0 END) * 100 as avg_success_rate
            FROM member_interventions
            WHERE measure_id IN (
                SELECT DISTINCT measure_id 
                FROM member_interventions 
                WHERE member_id IN ('{member_list}')
            )
        """
        
        historical_data = execute_query(historical_query)
        predicted_success_rate = float(historical_data.iloc[0]['avg_success_rate']) if not historical_data.empty else 75.0
        
        # Revenue calculation: $100 per successful closure
        revenue_per_closure = 100.0
        predicted_closures = int(total_interventions * (predicted_success_rate / 100))
        predicted_revenue = predicted_closures * revenue_per_closure
        predicted_net_benefit = predicted_revenue - total_cost
        
        # Calculate required FTE
        # Assumption: Each FTE can handle ~200 interventions per quarter
        # For campaign, assume 30-day timeline
        interventions_per_fte_per_month = 50  # ~2-3 per day
        required_fte = max(1, np.ceil(total_interventions / interventions_per_fte_per_month))
        
        # Total value (revenue potential)
        total_value = predicted_revenue
        
        return {
            "total_members": int(total_members),
            "total_interventions": int(total_interventions),
            "total_value": float(total_value),
            "predicted_success_rate": float(predicted_success_rate),
            "predicted_closures": int(predicted_closures),
            "predicted_revenue": float(predicted_revenue),
            "total_cost": float(total_cost),
            "predicted_net_benefit": float(predicted_net_benefit),
            "required_fte": int(required_fte),
            "avg_cost_per_member": float(avg_cost_per_member),
            "revenue_per_closure": float(revenue_per_closure)
        }
    
    def assign_to_coordinators(
        self,
        member_data: pd.DataFrame,
        coordinator_count: int,
        assignment_strategy: str = "balanced"
    ) -> pd.DataFrame:
        """
        Assign members to care coordinators with workload balancing.
        
        Args:
            member_data: DataFrame with member/intervention data
            coordinator_count: Number of care coordinators
            assignment_strategy: "balanced", "round_robin", or "by_measure"
        
        Returns:
            DataFrame with coordinator assignments
        """
        if member_data.empty or coordinator_count < 1:
            return pd.DataFrame()
        
        # Create coordinator IDs
        coordinators = [f"Coordinator {i+1}" for i in range(coordinator_count)]
        
        # Reset index for easier manipulation
        member_data = member_data.copy().reset_index(drop=True)
        
        if assignment_strategy == "round_robin":
            # Simple round-robin assignment
            member_data['coordinator'] = member_data.index % coordinator_count
            member_data['coordinator_name'] = member_data['coordinator'].apply(
                lambda x: coordinators[x]
            )
        
        elif assignment_strategy == "by_measure":
            # Group by measure, then distribute
            member_data = member_data.sort_values('measure_id')
            member_data['coordinator'] = member_data.groupby('measure_id').cumcount() % coordinator_count
            member_data['coordinator_name'] = member_data['coordinator'].apply(
                lambda x: coordinators[x]
            )
        
        else:  # balanced
            # Balance workload by intervention count
            # Sort by measure to keep related interventions together
            member_data = member_data.sort_values(['measure_id', 'member_id'])
            
            # Calculate target workload per coordinator
            total_interventions = len(member_data)
            target_per_coordinator = total_interventions / coordinator_count
            
            # Assign to balance workload
            coordinator_workloads = [0] * coordinator_count
            assignments = []
            
            for idx, row in member_data.iterrows():
                # Find coordinator with least current workload
                min_coordinator = min(range(coordinator_count), key=lambda i: coordinator_workloads[i])
                assignments.append(min_coordinator)
                coordinator_workloads[min_coordinator] += 1
            
            member_data['coordinator'] = assignments
            member_data['coordinator_name'] = member_data['coordinator'].apply(
                lambda x: coordinators[x]
            )
        
        return member_data
    
    def create_campaign(
        self,
        name: str,
        member_ids: List[str],
        intervention_ids: Optional[List[str]] = None,
        coordinator_count: int = 5,
        assignment_strategy: str = "balanced",
        target_date: Optional[str] = None
    ) -> Dict:
        """
        Create a new campaign.
        
        Returns:
            Campaign dictionary with ID and details
        """
        campaign_id = str(uuid.uuid4())[:8]
        
        # Get member data
        member_list = "','".join(member_ids)
        query = f"""
            SELECT 
                mi.member_id,
                mi.intervention_id,
                mi.measure_id,
                hm.measure_name,
                mi.intervention_date,
                mi.status,
                mi.cost_per_intervention,
                'Member ' || mi.member_id as member_name,
                '' as member_phone,
                '' as member_email
            FROM member_interventions mi
            LEFT JOIN hedis_measures hm ON mi.measure_id = hm.measure_id
            WHERE mi.member_id IN ('{member_list}')
        """
        
        if intervention_ids:
            intervention_list = "','".join(intervention_ids)
            query += f" AND mi.intervention_id IN ('{intervention_list}')"
        
        member_data = execute_query(query)
        
        # Calculate metrics
        metrics = self.calculate_campaign_metrics(member_ids, intervention_ids)
        
        # Assign to coordinators
        assigned_data = self.assign_to_coordinators(
            member_data,
            coordinator_count,
            assignment_strategy
        )
        
        # Create campaign
        campaign = {
            "campaign_id": campaign_id,
            "name": name,
            "created_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "target_date": target_date or (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d"),
            "member_ids": member_ids,
            "intervention_ids": intervention_ids or [],
            "coordinator_count": coordinator_count,
            "assignment_strategy": assignment_strategy,
            "metrics": metrics,
            "member_data": assigned_data,
            "status": "active"
        }
        
        # Store campaign
        self.campaigns[campaign_id] = campaign
        
        return campaign
    
    def get_campaign(self, campaign_id: str) -> Optional[Dict]:
        """Get campaign by ID."""
        return self.campaigns.get(campaign_id)
    
    def get_all_campaigns(self) -> List[Dict]:
        """Get all campaigns."""
        return list(self.campaigns.values())
    
    def update_campaign_progress(
        self,
        campaign_id: str,
        completed_interventions: List[str]
    ) -> Dict:
        """
        Update campaign progress with completed interventions.
        
        Returns:
            Updated campaign with progress metrics
        """
        campaign = self.get_campaign(campaign_id)
        if not campaign:
            return None
        
        member_data = campaign['member_data'].copy()
        
        # Mark completed interventions
        if 'completed' not in member_data.columns:
            member_data['completed'] = False
        
        member_data.loc[member_data['intervention_id'].isin(completed_interventions), 'completed'] = True
        
        # Calculate progress
        total = len(member_data)
        completed = member_data['completed'].sum()
        progress_pct = (completed / total * 100) if total > 0 else 0
        
        # Update campaign
        campaign['member_data'] = member_data
        campaign['progress'] = {
            "total": int(total),
            "completed": int(completed),
            "remaining": int(total - completed),
            "progress_pct": float(progress_pct)
        }
        
        return campaign
    
    def export_crm_csv(self, campaign_id: str) -> str:
        """
        Generate CSV export for CRM import.
        
        Returns:
            CSV string
        """
        campaign = self.get_campaign(campaign_id)
        if not campaign:
            return ""
        
        member_data = campaign['member_data'].copy()
        
        # Format for CRM import
        crm_data = pd.DataFrame({
            "Member ID": member_data['member_id'],
            "Member Name": member_data.get('member_name', ''),
            "Phone": member_data.get('member_phone', ''),
            "Email": member_data.get('member_email', ''),
            "Measure": member_data.get('measure_name', ''),
            "Intervention Date": member_data.get('intervention_date', ''),
            "Coordinator": member_data.get('coordinator_name', ''),
            "Status": member_data.get('status', 'pending'),
            "Priority": "High"  # Could be calculated based on metrics
        })
        
        return crm_data.to_csv(index=False)
    
    def generate_call_list(self, campaign_id: str, coordinator_name: Optional[str] = None) -> pd.DataFrame:
        """
        Generate printable call list for campaign.
        
        Args:
            campaign_id: Campaign ID
            coordinator_name: Optional filter by coordinator
        
        Returns:
            DataFrame formatted for printing
        """
        campaign = self.get_campaign(campaign_id)
        if not campaign:
            return pd.DataFrame()
        
        member_data = campaign['member_data'].copy()
        
        if coordinator_name:
            member_data = member_data[member_data['coordinator_name'] == coordinator_name]
        
        # Format for call list
        call_list = pd.DataFrame({
            "Member ID": member_data['member_id'],
            "Member Name": member_data.get('member_name', ''),
            "Phone": member_data.get('member_phone', ''),
            "Measure": member_data.get('measure_name', ''),
            "Intervention Date": pd.to_datetime(member_data.get('intervention_date', '')).dt.strftime('%Y-%m-%d'),
            "Status": member_data.get('status', 'pending'),
            "Notes": ""  # Empty column for notes
        })
        
        return call_list.sort_values(['Measure', 'Member ID'])

