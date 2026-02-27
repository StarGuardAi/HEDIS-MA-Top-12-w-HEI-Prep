"""
SDOH & Demographic Data Loader for Health Equity Index (HEI)

This module loads and processes Social Determinants of Health (SDOH) data
and demographic information required for CMS Health Equity Index reporting.

CMS Requirement: NEW for MY2025, ENFORCED in 2027
Purpose: Measure and reduce health disparities across demographic groups

Author: Analytics Team
Date: October 23, 2025
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# CMS Race/Ethnicity Categories (Standardized)
RACE_ETHNICITY_CODES = {
    'ASIAN': ['A', 'AS', 'ASIAN'],
    'BLACK': ['B', 'BL', 'BLACK', 'AFRICAN AMERICAN', 'AA'],
    'HISPANIC': ['H', 'HI', 'HISPANIC', 'LATINO'],
    'NHPI': ['NH', 'PI', 'NATIVE HAWAIIAN', 'PACIFIC ISLANDER'],
    'WHITE': ['W', 'WH', 'WHITE', 'CAUCASIAN'],
    'OTHER': ['O', 'OT', 'OTHER', 'MULTIPLE'],
    'UNKNOWN': ['U', 'UN', 'UNKNOWN', 'DECLINED', None, '']
}

# Language Categories
LANGUAGE_CODES = {
    'ENGLISH': ['EN', 'ENG', 'ENGLISH'],
    'SPANISH': ['ES', 'ESP', 'SPANISH'],
    'CHINESE': ['ZH', 'CHI', 'CHINESE', 'MANDARIN', 'CANTONESE'],
    'VIETNAMESE': ['VI', 'VIE', 'VIETNAMESE'],
    'TAGALOG': ['TL', 'TAG', 'TAGALOG'],
    'KOREAN': ['KO', 'KOR', 'KOREAN'],
    'RUSSIAN': ['RU', 'RUS', 'RUSSIAN'],
    'ARABIC': ['AR', 'ARA', 'ARABIC'],
    'OTHER': ['OT', 'OTHER'],
    'UNKNOWN': ['UN', 'UNKNOWN', None, '']
}


class SDOHLoader:
    """
    Load and process SDOH and demographic data for Health Equity Index.
    
    Handles:
    - Race/ethnicity standardization
    - Language processing
    - SDOH factor extraction
    - Vulnerable population identification
    """
    
    def __init__(self):
        """Initialize SDOH loader"""
        logger.info("SDOH Loader initialized for Health Equity Index")
    
    def standardize_race_ethnicity(self, race_value: str) -> str:
        """
        Standardize race/ethnicity to CMS categories.
        
        Args:
            race_value: Raw race/ethnicity value
            
        Returns:
            Standardized race/ethnicity category
        """
        if pd.isna(race_value) or race_value == '':
            return 'UNKNOWN'
        
        race_upper = str(race_value).upper().strip()
        
        # Check each category
        for category, codes in RACE_ETHNICITY_CODES.items():
            if race_upper in [str(c).upper() for c in codes if c is not None]:
                return category
        
        # If no match, return UNKNOWN
        return 'UNKNOWN'
    
    def standardize_language(self, language_value: str) -> str:
        """
        Standardize language to common categories.
        
        Args:
            language_value: Raw language value
            
        Returns:
            Standardized language category
        """
        if pd.isna(language_value) or language_value == '':
            return 'UNKNOWN'
        
        lang_upper = str(language_value).upper().strip()
        
        # Check each category
        for category, codes in LANGUAGE_CODES.items():
            if lang_upper in [str(c).upper() for c in codes if c is not None]:
                return category
        
        # If no match, return OTHER
        return 'OTHER'
    
    def load_demographic_data(
        self,
        member_df: pd.DataFrame,
        member_id_col: str = 'member_id'
    ) -> pd.DataFrame:
        """
        Load and standardize demographic data.
        
        Args:
            member_df: Raw member demographic data
            member_id_col: Column name for member identifier
            
        Returns:
            DataFrame with standardized demographics
        """
        logger.info(f"Loading demographic data for {len(member_df)} members")
        
        demo_df = member_df.copy()
        
        # Standardize race/ethnicity
        if 'race' in demo_df.columns:
            demo_df['race_ethnicity_std'] = demo_df['race'].apply(self.standardize_race_ethnicity)
        elif 'ethnicity' in demo_df.columns:
            demo_df['race_ethnicity_std'] = demo_df['ethnicity'].apply(self.standardize_race_ethnicity)
        else:
            demo_df['race_ethnicity_std'] = 'UNKNOWN'
        
        # Standardize language
        if 'language' in demo_df.columns:
            demo_df['language_std'] = demo_df['language'].apply(self.standardize_language)
        else:
            demo_df['language_std'] = 'ENGLISH'  # Default assumption
        
        # Limited English Proficiency (LEP) flag
        demo_df['is_lep'] = (
            (demo_df['language_std'] != 'ENGLISH') & 
            (demo_df['language_std'] != 'UNKNOWN')
        ).astype(int)
        
        logger.info(f"Demographic data standardized: {demo_df['race_ethnicity_std'].value_counts().to_dict()}")
        
        return demo_df
    
    def load_sdoh_data(
        self,
        member_df: pd.DataFrame,
        sdoh_df: Optional[pd.DataFrame] = None,
        member_id_col: str = 'member_id'
    ) -> pd.DataFrame:
        """
        Load and process SDOH factors.
        
        Args:
            member_df: Member demographic data
            sdoh_df: SDOH data (optional, if separate)
            member_id_col: Column name for member identifier
            
        Returns:
            DataFrame with SDOH factors
        """
        logger.info("Loading SDOH data")
        
        # If SDOH data provided separately, merge it
        if sdoh_df is not None:
            result_df = member_df.merge(
                sdoh_df,
                on=member_id_col,
                how='left'
            )
        else:
            result_df = member_df.copy()
        
        # Extract SDOH factors (create if not present)
        
        # 1. Low Income Subsidy (LIS)
        if 'lis' not in result_df.columns:
            if 'subsidy' in result_df.columns:
                result_df['lis'] = result_df['subsidy'].apply(lambda x: 1 if x in ['LIS', 'LOW', 'Y', 1] else 0)
            else:
                result_df['lis'] = 0
        
        # 2. Dual Eligible (Medicare + Medicaid)
        if 'dual_eligible' not in result_df.columns:
            if 'medicaid' in result_df.columns:
                result_df['dual_eligible'] = result_df['medicaid'].apply(lambda x: 1 if x in ['Y', 'YES', 1] else 0)
            else:
                result_df['dual_eligible'] = 0
        
        # 3. Disability Status
        if 'has_disability' not in result_df.columns:
            if 'disability' in result_df.columns:
                result_df['has_disability'] = result_df['disability'].apply(lambda x: 1 if x in ['Y', 'YES', 1] else 0)
            else:
                result_df['has_disability'] = 0
        
        # 4. Area Deprivation Index (ADI) - proxy if not available
        if 'adi_percentile' not in result_df.columns:
            result_df['adi_percentile'] = 50  # Neutral default
        
        # 5. Food Insecurity
        if 'food_insecure' not in result_df.columns:
            # Proxy: LIS or dual eligible often correlates with food insecurity
            result_df['food_insecure'] = (
                (result_df['lis'] == 1) | 
                (result_df['dual_eligible'] == 1)
            ).astype(int)
        
        # 6. Housing Instability (proxy)
        if 'housing_unstable' not in result_df.columns:
            result_df['housing_unstable'] = 0  # Default
        
        # 7. Transportation Barriers (proxy)
        if 'transportation_barrier' not in result_df.columns:
            # Proxy: Rural + low income
            if 'is_rural' in result_df.columns:
                result_df['transportation_barrier'] = (
                    (result_df['is_rural'] == 1) & 
                    (result_df['lis'] == 1)
                ).astype(int)
            else:
                result_df['transportation_barrier'] = 0
        
        # Calculate SDOH risk score (0-10 scale)
        sdoh_factors = [
            'lis', 'dual_eligible', 'has_disability',
            'food_insecure', 'housing_unstable', 'transportation_barrier'
        ]
        result_df['sdoh_risk_score'] = result_df[sdoh_factors].sum(axis=1)
        
        # Categorize SDOH risk
        result_df['sdoh_risk_category'] = pd.cut(
            result_df['sdoh_risk_score'],
            bins=[-1, 0, 2, 4, 10],
            labels=['LOW', 'MODERATE', 'HIGH', 'VERY_HIGH']
        )
        
        logger.info(f"SDOH data processed: {result_df['sdoh_risk_category'].value_counts().to_dict()}")
        
        return result_df
    
    def load_geographic_data(
        self,
        member_df: pd.DataFrame,
        member_id_col: str = 'member_id'
    ) -> pd.DataFrame:
        """
        Load and process geographic data.
        
        Args:
            member_df: Member data with geographic info
            member_id_col: Column name for member identifier
            
        Returns:
            DataFrame with geographic factors
        """
        logger.info("Loading geographic data")
        
        geo_df = member_df.copy()
        
        # Rural/Urban classification
        if 'is_rural' not in geo_df.columns:
            # Proxy: ZIP code based (would need actual RUCA codes)
            geo_df['is_rural'] = 0  # Default urban
        
        # Health Professional Shortage Area (HPSA)
        if 'in_hpsa' not in geo_df.columns:
            geo_df['in_hpsa'] = 0  # Default not in HPSA
        
        # County (for regional analysis)
        if 'county' not in geo_df.columns:
            if 'zip_code' in geo_df.columns:
                # Would map ZIP to county (placeholder)
                geo_df['county'] = 'UNKNOWN'
            else:
                geo_df['county'] = 'UNKNOWN'
        
        return geo_df
    
    def identify_vulnerable_populations(
        self,
        member_df: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Identify vulnerable populations for targeted interventions.
        
        Args:
            member_df: Member data with demographics and SDOH
            
        Returns:
            DataFrame with vulnerability flags
        """
        logger.info("Identifying vulnerable populations")
        
        vuln_df = member_df.copy()
        
        # Vulnerable population flags
        
        # 1. High SDOH risk
        vuln_df['is_high_sdoh_risk'] = (
            vuln_df['sdoh_risk_score'] >= 4
        ).astype(int)
        
        # 2. Limited English Proficiency
        vuln_df['is_lep_vulnerable'] = vuln_df['is_lep']
        
        # 3. Racial/Ethnic Minority
        vuln_df['is_minority'] = (
            ~vuln_df['race_ethnicity_std'].isin(['WHITE', 'UNKNOWN'])
        ).astype(int)
        
        # 4. Dual Eligible (low income)
        vuln_df['is_low_income'] = (
            (vuln_df['lis'] == 1) | 
            (vuln_df['dual_eligible'] == 1)
        ).astype(int)
        
        # 5. Rural + Barriers
        vuln_df['is_rural_vulnerable'] = (
            (vuln_df['is_rural'] == 1) & 
            (vuln_df['transportation_barrier'] == 1)
        ).astype(int)
        
        # 6. Disability
        vuln_df['is_disability_vulnerable'] = vuln_df['has_disability']
        
        # Overall vulnerability score (0-6)
        vulnerability_flags = [
            'is_high_sdoh_risk', 'is_lep_vulnerable', 'is_minority',
            'is_low_income', 'is_rural_vulnerable', 'is_disability_vulnerable'
        ]
        vuln_df['vulnerability_score'] = vuln_df[vulnerability_flags].sum(axis=1)
        
        # Categorize vulnerability
        vuln_df['vulnerability_category'] = pd.cut(
            vuln_df['vulnerability_score'],
            bins=[-1, 0, 2, 4, 6],
            labels=['LOW', 'MODERATE', 'HIGH', 'VERY_HIGH']
        )
        
        logger.info(f"Vulnerable populations identified: {vuln_df['vulnerability_category'].value_counts().to_dict()}")
        
        return vuln_df
    
    def load_complete_hei_data(
        self,
        member_df: pd.DataFrame,
        sdoh_df: Optional[pd.DataFrame] = None,
        member_id_col: str = 'member_id'
    ) -> pd.DataFrame:
        """
        Load complete HEI dataset with all demographics, SDOH, and geographic data.
        
        Args:
            member_df: Raw member data
            sdoh_df: Optional SDOH data
            member_id_col: Column name for member identifier
            
        Returns:
            Complete DataFrame with all HEI data elements
        """
        logger.info("Loading complete HEI dataset")
        
        # Step 1: Demographic data
        result_df = self.load_demographic_data(member_df, member_id_col)
        
        # Step 2: SDOH data
        result_df = self.load_sdoh_data(result_df, sdoh_df, member_id_col)
        
        # Step 3: Geographic data
        result_df = self.load_geographic_data(result_df, member_id_col)
        
        # Step 4: Vulnerable populations
        result_df = self.identify_vulnerable_populations(result_df)
        
        logger.info(f"Complete HEI dataset loaded: {len(result_df)} members")
        
        return result_df
    
    def get_demographic_summary(self, hei_df: pd.DataFrame) -> Dict:
        """
        Generate summary statistics for demographic distribution.
        
        Args:
            hei_df: Complete HEI dataset
            
        Returns:
            Dictionary with summary statistics
        """
        summary = {
            'total_members': len(hei_df),
            'race_ethnicity_distribution': hei_df['race_ethnicity_std'].value_counts().to_dict(),
            'language_distribution': hei_df['language_std'].value_counts().to_dict(),
            'lep_members': hei_df['is_lep'].sum(),
            'lep_percentage': (hei_df['is_lep'].sum() / len(hei_df) * 100),
            'lis_members': hei_df['lis'].sum(),
            'dual_eligible_members': hei_df['dual_eligible'].sum(),
            'disability_members': hei_df['has_disability'].sum(),
            'sdoh_risk_distribution': hei_df['sdoh_risk_category'].value_counts().to_dict(),
            'vulnerability_distribution': hei_df['vulnerability_category'].value_counts().to_dict(),
            'high_vulnerability_members': hei_df[hei_df['vulnerability_score'] >= 4].shape[0],
            'high_vulnerability_percentage': (hei_df[hei_df['vulnerability_score'] >= 4].shape[0] / len(hei_df) * 100),
        }
        
        return summary

