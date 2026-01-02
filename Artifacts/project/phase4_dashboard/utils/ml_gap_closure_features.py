"""
ML Feature Engineering for Gap Closure Prediction
Extracts and engineers features for gap closure likelihood prediction
"""
from typing import Dict, List, Optional
import pandas as pd
import numpy as np
from datetime import datetime, timedelta


class GapClosureFeatureEngineer:
    """
    Feature engineering for gap closure prediction.
    Extracts features from member, clinical, engagement, and operational data.
    """
    
    def __init__(self):
        self.feature_names = []
    
    def extract_member_characteristics(
        self,
        member_id: str,
        member_data: Dict
    ) -> Dict:
        """
        Extract member characteristic features.
        
        Features:
        - Age, gender, risk score
        - Chronic conditions count
        - Prior year compliance
        - Member tenure
        - Socioeconomic factors
        """
        features = {}
        
        # Demographics
        features['age'] = member_data.get('age', 65)
        features['age_group'] = self._get_age_group(features['age'])
        features['gender_male'] = 1 if member_data.get('gender') == 'Male' else 0
        features['gender_female'] = 1 if member_data.get('gender') == 'Female' else 0
        
        # Risk score
        features['risk_score'] = member_data.get('risk_score', 0.5)
        features['risk_score_high'] = 1 if features['risk_score'] > 0.7 else 0
        features['risk_score_medium'] = 1 if 0.3 <= features['risk_score'] <= 0.7 else 0
        features['risk_score_low'] = 1 if features['risk_score'] < 0.3 else 0
        
        # Chronic conditions
        chronic_conditions = member_data.get('chronic_conditions', [])
        features['chronic_conditions_count'] = len(chronic_conditions)
        features['has_diabetes'] = 1 if 'Diabetes' in chronic_conditions else 0
        features['has_hypertension'] = 1 if 'Hypertension' in chronic_conditions else 0
        features['has_copd'] = 1 if 'COPD' in chronic_conditions else 0
        
        # Prior year compliance
        features['prior_year_compliance'] = member_data.get('prior_year_compliance_rate', 0.75)
        features['prior_year_compliance_high'] = 1 if features['prior_year_compliance'] > 0.8 else 0
        
        # Member tenure (years)
        member_since = member_data.get('member_since', datetime.now() - timedelta(days=365))
        if isinstance(member_since, str):
            member_since = datetime.fromisoformat(member_since)
        features['member_tenure_years'] = (datetime.now() - member_since).days / 365.0
        features['member_tenure_new'] = 1 if features['member_tenure_years'] < 1 else 0
        
        # Socioeconomic factors
        zip_code = member_data.get('zip_code', '00000')
        features['zip_code_prefix'] = int(zip_code[:3]) if zip_code else 0
        features['education_level'] = member_data.get('education_level', 'Unknown')
        features['education_high_school'] = 1 if features['education_level'] == 'High School' else 0
        features['education_college'] = 1 if features['education_level'] == 'College' else 0
        
        return features
    
    def extract_clinical_factors(
        self,
        gap_data: Dict,
        member_data: Dict
    ) -> Dict:
        """
        Extract clinical factor features.
        
        Features:
        - Measure type
        - Gap severity
        - Time since last visit
        - PCP characteristics
        - Distance to facilities
        """
        features = {}
        
        # Measure type
        measure_id = gap_data.get('measure_id', '')
        features['measure_type_preventive'] = 1 if measure_id in ['COL', 'MAM', 'CCS'] else 0
        features['measure_type_chronic'] = 1 if measure_id in ['HBA1C', 'BP'] else 0
        features['measure_type_outcome'] = 1 if measure_id in ['HBA1C', 'BP'] else 0
        
        # Gap severity
        gap_reason = gap_data.get('gap_reason', '')
        features['gap_severity_low'] = 1 if gap_reason == 'Lab Pending' else 0
        features['gap_severity_medium'] = 1 if gap_reason == 'Not Scheduled' else 0
        features['gap_severity_high'] = 1 if gap_reason in ['Missed Appointment', 'Provider Delay'] else 0
        
        # Time since last visit
        last_visit = member_data.get('last_visit_date')
        if last_visit:
            if isinstance(last_visit, str):
                last_visit = datetime.fromisoformat(last_visit)
            days_since_visit = (datetime.now() - last_visit).days
        else:
            days_since_visit = 365
        features['days_since_last_visit'] = days_since_visit
        features['recent_visit'] = 1 if days_since_visit < 90 else 0
        
        # PCP characteristics
        pcp_data = member_data.get('pcp', {})
        features['pcp_quality_score'] = pcp_data.get('quality_score', 3.5)
        features['pcp_high_quality'] = 1 if features['pcp_quality_score'] > 4.0 else 0
        features['pcp_patient_count'] = pcp_data.get('patient_count', 1000)
        
        # Distance to facilities
        features['distance_to_facility_miles'] = member_data.get('distance_to_facility', 10.0)
        features['distance_close'] = 1 if features['distance_to_facility_miles'] < 5 else 0
        features['distance_far'] = 1 if features['distance_to_facility_miles'] > 20 else 0
        
        return features
    
    def extract_engagement_factors(
        self,
        member_id: str,
        engagement_data: Dict
    ) -> Dict:
        """
        Extract engagement factor features.
        
        Features:
        - Portal usage frequency
        - Response rate to outreach
        - Appointment no-show history
        - Preferred contact channel
        - Best contact time
        """
        features = {}
        
        # Portal usage
        portal_usage = engagement_data.get('portal_usage', {})
        features['portal_logins_last_90_days'] = portal_usage.get('logins_last_90_days', 0)
        features['portal_active_user'] = 1 if features['portal_logins_last_90_days'] > 5 else 0
        
        # Response rate
        outreach_history = engagement_data.get('outreach_history', [])
        total_outreach = len(outreach_history)
        responded = sum(1 for o in outreach_history if o.get('responded', False))
        features['outreach_response_rate'] = responded / total_outreach if total_outreach > 0 else 0.5
        features['high_response_rate'] = 1 if features['outreach_response_rate'] > 0.7 else 0
        
        # No-show history
        appointment_history = engagement_data.get('appointment_history', [])
        total_appointments = len(appointment_history)
        no_shows = sum(1 for a in appointment_history if a.get('no_show', False))
        features['no_show_rate'] = no_shows / total_appointments if total_appointments > 0 else 0.1
        features['low_no_show_rate'] = 1 if features['no_show_rate'] < 0.2 else 0
        
        # Preferred contact channel
        preferred_channel = engagement_data.get('preferred_contact_channel', 'Phone')
        features['prefers_phone'] = 1 if preferred_channel == 'Phone' else 0
        features['prefers_sms'] = 1 if preferred_channel == 'SMS' else 0
        features['prefers_email'] = 1 if preferred_channel == 'Email' else 0
        
        # Best contact time
        best_contact_hour = engagement_data.get('best_contact_hour', 10)
        features['best_contact_hour'] = best_contact_hour
        features['best_contact_morning'] = 1 if 8 <= best_contact_hour < 12 else 0
        features['best_contact_afternoon'] = 1 if 12 <= best_contact_hour < 17 else 0
        
        return features
    
    def extract_operational_factors(
        self,
        gap_data: Dict,
        operational_data: Dict
    ) -> Dict:
        """
        Extract operational factor features.
        
        Features:
        - Coordinator workload
        - Intervention type
        - Season/time of year
        - Days until deadline
        """
        features = {}
        
        # Coordinator workload
        coordinator_id = gap_data.get('assigned_coordinator', '')
        coordinator_data = operational_data.get('coordinators', {}).get(coordinator_id, {})
        features['coordinator_active_gaps'] = coordinator_data.get('active_gaps', 50)
        features['coordinator_workload_high'] = 1 if features['coordinator_active_gaps'] > 75 else 0
        features['coordinator_closure_rate'] = coordinator_data.get('closure_rate', 0.75)
        features['coordinator_high_performer'] = 1 if features['coordinator_closure_rate'] > 0.85 else 0
        
        # Intervention type
        intervention_type = gap_data.get('planned_intervention_type', 'Phone')
        features['intervention_phone'] = 1 if intervention_type == 'Phone' else 0
        features['intervention_sms'] = 1 if intervention_type == 'SMS' else 0
        features['intervention_email'] = 1 if intervention_type == 'Email' else 0
        
        # Season/time of year
        current_month = datetime.now().month
        features['month'] = current_month
        features['season_spring'] = 1 if 3 <= current_month <= 5 else 0
        features['season_summer'] = 1 if 6 <= current_month <= 8 else 0
        features['season_fall'] = 1 if 9 <= current_month <= 11 else 0
        features['season_winter'] = 1 if current_month in [12, 1, 2] else 0
        
        # Days until deadline
        deadline_date = gap_data.get('deadline_date')
        if isinstance(deadline_date, str):
            deadline_date = datetime.fromisoformat(deadline_date)
        days_until = (deadline_date - datetime.now()).days
        features['days_until_deadline'] = days_until
        features['deadline_urgent'] = 1 if days_until < 30 else 0
        features['deadline_critical'] = 1 if days_until < 15 else 0
        
        return features
    
    def create_feature_vector(
        self,
        member_id: str,
        gap_data: Dict,
        member_data: Dict,
        engagement_data: Dict,
        operational_data: Dict
    ) -> pd.Series:
        """
        Create complete feature vector for prediction.
        
        Returns:
            pandas Series with all features
        """
        features = {}
        
        # Extract all feature groups
        features.update(self.extract_member_characteristics(member_id, member_data))
        features.update(self.extract_clinical_factors(gap_data, member_data))
        features.update(self.extract_engagement_factors(member_id, engagement_data))
        features.update(self.extract_operational_factors(gap_data, operational_data))
        
        return pd.Series(features)
    
    def _get_age_group(self, age: float) -> str:
        """Get age group category."""
        if age < 50:
            return '18-49'
        elif age < 65:
            return '50-64'
        elif age < 75:
            return '65-74'
        else:
            return '75+'

