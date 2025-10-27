"""
Validate Tier 2 Cardiovascular Features

This script creates synthetic test data and validates that all 35+ features
are correctly generated with expected values.

Author: Analytics Team
Date: October 25, 2025
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.data.features.cardiovascular_features import (
    create_cardiovascular_features,
    validate_cardiovascular_features,
    get_cbp_features,
    get_supd_features,
    get_pdc_rasa_features,
    get_pdc_sta_features
)


def create_synthetic_test_data(n_members=1000):
    """Create synthetic test data for feature validation"""
    
    np.random.seed(42)
    member_ids = range(1, n_members + 1)
    
    # Create synthetic claims data
    claims_data = []
    for member_id in member_ids:
        # Random diagnoses
        diagnoses = np.random.choice(
            ['I10', 'E11.9', 'I50.9', 'I21.9', 'I63.9', 'N18.3', 'I20.0'],
            size=np.random.randint(1, 5),
            replace=True
        )
        
        for dx in diagnoses:
            claims_data.append({
                'member_id': member_id,
                'diagnosis_code': dx,
                'procedure_code': '99213',
                'service_date': (datetime(2025, 1, 1) + timedelta(days=np.random.randint(0, 365))).strftime('%Y-%m-%d'),
                'claim_type': np.random.choice(['outpatient', 'inpatient', 'emergency'], p=[0.8, 0.1, 0.1]),
                'provider_specialty': np.random.choice(['primary_care', 'cardiology', 'nephrology'], p=[0.6, 0.3, 0.1])
            })
    
    claims_df = pd.DataFrame(claims_data)
    
    # Create synthetic pharmacy data
    pharmacy_data = []
    for member_id in member_ids:
        if np.random.random() > 0.3:  # 70% have pharmacy data
            medications = np.random.choice(
                ['lisinopril 10mg', 'atorvastatin 40mg', 'metoprolol 50mg', 
                 'losartan 50mg', 'amlodipine 5mg'],
                size=np.random.randint(1, 4),
                replace=False
            )
            
            for med in medications:
                pharmacy_data.append({
                    'member_id': member_id,
                    'medication_name': med,
                    'fill_date': (datetime(2025, 1, 1) + timedelta(days=np.random.randint(0, 365))).strftime('%Y-%m-%d'),
                    'days_supply': 30
                })
    
    pharmacy_df = pd.DataFrame(pharmacy_data) if pharmacy_data else pd.DataFrame()
    
    # Create synthetic vitals data
    vitals_data = []
    for member_id in member_ids:
        if np.random.random() > 0.4:  # 60% have vitals data
            for _ in range(np.random.randint(1, 4)):
                vitals_data.append({
                    'member_id': member_id,
                    'reading_date': (datetime(2025, 1, 1) + timedelta(days=np.random.randint(0, 365))).strftime('%Y-%m-%d'),
                    'systolic_bp': np.random.randint(110, 180),
                    'diastolic_bp': np.random.randint(70, 110)
                })
    
    vitals_df = pd.DataFrame(vitals_data) if vitals_data else pd.DataFrame()
    
    return claims_df, pharmacy_df, vitals_df


def validate_feature_counts(features_df):
    """Validate that all expected features are present"""
    
    expected_features = [
        # HTN features (10)
        'has_htn_diagnosis', 'htn_diagnosis_count', 'years_since_first_htn',
        'has_htn_ckd_complication', 'has_htn_cvd_complication', 'has_stroke_history',
        'bp_med_fills_count', 'bp_med_adherence_90d', 'bp_med_classes_count',
        'most_recent_systolic', 'most_recent_diastolic', 'avg_systolic_bp_year',
        'avg_diastolic_bp_year', 'uncontrolled_bp_episodes', 'htn_ed_visits',
        'htn_hospitalizations',
        
        # CVD features (10)
        'has_mi_history', 'has_stroke_history', 'has_pci_history', 'has_cabg_history',
        'has_ascvd', 'years_since_ascvd', 'has_chf', 'chf_visits_count',
        'has_angina', 'has_pad', 'has_carotid_disease', 'cvd_procedures_count',
        'has_cardiac_rehab', 'cardiology_visits_count', 'cvd_ed_visits',
        'cvd_hospitalizations',
        
        # Medication features (10)
        'has_statin_rx', 'statin_fills_count', 'has_high_potency_statin',
        'has_ace_arb_rx', 'ace_arb_fills_count', 'total_bp_medications',
        'cvd_med_adherence_estimate', 'statin_switches', 'total_med_switches',
        'polypharmacy_count', 'has_polypharmacy', 'recent_med_changes',
        'avg_refill_gap_days',
        
        # Diabetes features (5+)
        'has_diabetes', 'diabetes_diagnosis_count', 'years_since_diabetes',
        'has_diabetic_cvd', 'has_diabetic_ckd', 'has_ckd',
        'in_tier1_population'
    ]
    
    missing_features = [f for f in expected_features if f not in features_df.columns]
    extra_features = [f for f in features_df.columns if f not in expected_features + ['member_id_hash']]
    
    return missing_features, extra_features


def validate_feature_values(features_df):
    """Validate feature value ranges and types"""
    
    issues = []
    
    # Check binary features
    binary_features = [
        'has_htn_diagnosis', 'has_mi_history', 'has_stroke_history',
        'has_ascvd', 'has_diabetes', 'has_ckd', 'in_tier1_population'
    ]
    
    for feature in binary_features:
        if feature in features_df.columns:
            unique_values = features_df[feature].unique()
            if not all(v in [0, 1] for v in unique_values):
                issues.append(f"{feature}: Contains values other than 0/1: {unique_values}")
    
    # Check count features (should be non-negative)
    count_features = [
        'htn_diagnosis_count', 'diabetes_diagnosis_count', 'bp_med_fills_count',
        'statin_fills_count', 'cardiology_visits_count'
    ]
    
    for feature in count_features:
        if feature in features_df.columns:
            if features_df[feature].min() < 0:
                issues.append(f"{feature}: Contains negative values")
    
    # Check percentage/ratio features (0-1)
    ratio_features = ['bp_med_adherence_90d', 'cvd_med_adherence_estimate']
    
    for feature in ratio_features:
        if feature in features_df.columns:
            if features_df[feature].min() < 0 or features_df[feature].max() > 1:
                issues.append(f"{feature}: Values outside 0-1 range")
    
    # Check BP values (should be in reasonable range)
    if 'most_recent_systolic' in features_df.columns:
        systolic_values = features_df[features_df['most_recent_systolic'] > 0]['most_recent_systolic']
        if len(systolic_values) > 0:
            if systolic_values.min() < 70 or systolic_values.max() > 250:
                issues.append(f"Systolic BP values out of reasonable range: {systolic_values.min()}-{systolic_values.max()}")
    
    return issues


def main():
    """Run feature validation"""
    
    print("=" * 80)
    print("TIER 2 CARDIOVASCULAR FEATURES VALIDATION")
    print("=" * 80)
    print()
    
    # Create synthetic test data
    print("Step 1: Creating synthetic test data...")
    claims_df, pharmacy_df, vitals_df = create_synthetic_test_data(n_members=1000)
    print(f"✅ Created data for 1,000 members")
    print(f"   - Claims records: {len(claims_df):,}")
    print(f"   - Pharmacy records: {len(pharmacy_df):,}")
    print(f"   - Vitals records: {len(vitals_df):,}")
    print()
    
    # Generate features
    print("Step 2: Generating cardiovascular features...")
    features_df = create_cardiovascular_features(
        claims_df=claims_df,
        pharmacy_df=pharmacy_df if not pharmacy_df.empty else None,
        vitals_df=vitals_df if not vitals_df.empty else None,
        measurement_year=2025
    )
    print(f"✅ Generated features for {len(features_df)} members")
    print(f"   - Total features: {len(features_df.columns) - 1}")  # Exclude member_id_hash
    print()
    
    # Validate feature completeness
    print("Step 3: Validating feature completeness...")
    missing_features, extra_features = validate_feature_counts(features_df)
    
    if missing_features:
        print(f"❌ Missing features ({len(missing_features)}):")
        for f in missing_features:
            print(f"   - {f}")
    else:
        print(f"✅ All expected features present (35+ features)")
    
    if extra_features:
        print(f"ℹ️  Extra features ({len(extra_features)}):")
        for f in extra_features[:5]:  # Show first 5
            print(f"   - {f}")
    print()
    
    # Validate feature values
    print("Step 4: Validating feature values...")
    value_issues = validate_feature_values(features_df)
    
    if value_issues:
        print(f"❌ Value validation issues ({len(value_issues)}):")
        for issue in value_issues:
            print(f"   - {issue}")
    else:
        print(f"✅ All feature values within expected ranges")
    print()
    
    # Run built-in validation
    print("Step 5: Running built-in validation...")
    validation_results = validate_cardiovascular_features(features_df)
    
    print("Validation Results:")
    print(f"   - Total members: {validation_results['total_members']}")
    print(f"   - Members with HTN: {validation_results['has_htn_diagnosis']}")
    print(f"   - Members with ASCVD: {validation_results['has_ascvd']}")
    print(f"   - Members with diabetes: {validation_results['has_diabetes']}")
    print(f"   - HTN + Diabetes overlap: {validation_results['htn_diabetes_overlap']}")
    print(f"   - ASCVD + Diabetes overlap: {validation_results['ascvd_diabetes_overlap']}")
    print()
    
    # Test measure-specific feature subsets
    print("Step 6: Testing measure-specific feature subsets...")
    
    cbp_features = get_cbp_features(features_df)
    print(f"✅ CBP features: {len(cbp_features.columns)} columns")
    
    supd_features = get_supd_features(features_df)
    print(f"✅ SUPD features: {len(supd_features.columns)} columns")
    
    pdc_rasa_features = get_pdc_rasa_features(features_df)
    print(f"✅ PDC-RASA features: {len(pdc_rasa_features.columns)} columns")
    
    pdc_sta_features = get_pdc_sta_features(features_df)
    print(f"✅ PDC-STA features: {len(pdc_sta_features.columns)} columns")
    print()
    
    # Summary
    print("=" * 80)
    print("VALIDATION SUMMARY")
    print("=" * 80)
    
    total_issues = len(missing_features) + len(value_issues)
    
    if total_issues == 0:
        print("✅ ALL VALIDATIONS PASSED")
        print()
        print("Tier 2 cardiovascular features are ready for:")
        print("   - CBP (Controlling High Blood Pressure)")
        print("   - SUPD (Statin Therapy for Diabetes)")
        print("   - PDC-RASA (Medication Adherence - Hypertension)")
        print("   - PDC-STA (Medication Adherence - Cholesterol)")
        print()
        print("Next Step: Proceed to Phase 2.2 (CBP Implementation)")
        return 0
    else:
        print(f"❌ VALIDATION FAILED: {total_issues} issues found")
        print()
        print("Please review and fix the issues above before proceeding.")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)

