"""
ML Model Training Script
Train and evaluate gap closure prediction model
"""
import pandas as pd
import numpy as np
from datetime import datetime
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

from utils.ml_gap_closure_model import GapClosureMLModel
from utils.ml_gap_closure_features import GapClosureFeatureEngineer


def generate_synthetic_training_data(n_samples: int = 10000) -> Tuple[pd.DataFrame, pd.Series]:
    """
    Generate synthetic training data for demonstration.
    In production, this would load from historical database.
    """
    np.random.seed(42)
    
    feature_engineer = GapClosureFeatureEngineer()
    
    features_list = []
    targets = []
    
    for i in range(n_samples):
        # Generate synthetic member data
        member_data = {
            'age': np.random.randint(45, 85),
            'gender': np.random.choice(['Male', 'Female']),
            'risk_score': np.random.uniform(0.2, 0.9),
            'chronic_conditions': np.random.choice([[], ['Diabetes'], ['Hypertension'], ['Diabetes', 'Hypertension']], p=[0.3, 0.3, 0.3, 0.1]),
            'prior_year_compliance_rate': np.random.uniform(0.5, 0.95),
            'member_since': datetime.now() - pd.Timedelta(days=np.random.randint(365, 3650)),
            'last_visit_date': datetime.now() - pd.Timedelta(days=np.random.randint(30, 365)),
            'pcp': {
                'quality_score': np.random.uniform(3.0, 5.0),
                'patient_count': np.random.randint(500, 2000)
            },
            'distance_to_facility': np.random.uniform(1.0, 30.0),
            'zip_code': f"{np.random.randint(10000, 99999)}",
            'education_level': np.random.choice(['High School', 'College', 'Graduate'])
        }
        
        gap_data = {
            'measure_id': np.random.choice(['HBA1C', 'BP', 'COL', 'MAM', 'CCS']),
            'gap_reason': np.random.choice(['Not Scheduled', 'Missed Appointment', 'Lab Pending', 'Provider Delay']),
            'deadline_date': datetime.now() + pd.Timedelta(days=np.random.randint(15, 120)),
            'assigned_coordinator': f"COORD{np.random.randint(1, 4):03d}",
            'planned_intervention_type': np.random.choice(['Phone', 'SMS', 'Email'])
        }
        
        engagement_data = {
            'portal_usage': {
                'logins_last_90_days': np.random.randint(0, 20)
            },
            'outreach_history': [
                {'responded': np.random.choice([True, False], p=[0.6, 0.4])}
                for _ in range(np.random.randint(0, 5))
            ],
            'appointment_history': [
                {'no_show': np.random.choice([True, False], p=[0.2, 0.8])}
                for _ in range(np.random.randint(0, 10))
            ],
            'preferred_contact_channel': np.random.choice(['Phone', 'SMS', 'Email']),
            'best_contact_hour': np.random.randint(8, 17)
        }
        
        operational_data = {
            'coordinators': {
                f"COORD{j:03d}": {
                    'active_gaps': np.random.randint(30, 100),
                    'closure_rate': np.random.uniform(0.6, 0.9)
                }
                for j in range(1, 4)
            }
        }
        
        # Extract features
        features = feature_engineer.create_feature_vector(
            member_id=f"MEM{i:04d}",
            gap_data=gap_data,
            member_data=member_data,
            engagement_data=engagement_data,
            operational_data=operational_data
        )
        
        features_list.append(features)
        
        # Generate target (closure outcome)
        # Higher probability of closure for:
        # - Higher prior compliance
        # - Lower no-show rate
        # - Recent visits
        # - High response rate
        base_prob = 0.5
        base_prob += (member_data['prior_year_compliance_rate'] - 0.5) * 0.3
        base_prob += (1 - len([a for a in engagement_data['appointment_history'] if a['no_show']]) / max(1, len(engagement_data['appointment_history']))) * 0.2
        
        # Add some noise
        base_prob += np.random.normal(0, 0.1)
        base_prob = max(0, min(1, base_prob))
        
        target = 1 if np.random.random() < base_prob else 0
        targets.append(target)
    
    features_df = pd.DataFrame(features_list)
    target_series = pd.Series(targets)
    
    return features_df, target_series


def train_model(
    model_type: str = 'xgboost',
    n_samples: int = 10000,
    output_path: str = 'models/gap_closure_model.pkl'
) -> Dict:
    """
    Train gap closure prediction model.
    
    Args:
        model_type: 'xgboost' or 'random_forest'
        n_samples: Number of training samples
        output_path: Path to save trained model
    
    Returns:
        Training metrics dictionary
    """
    print("Generating training data...")
    features_df, target_series = generate_synthetic_training_data(n_samples)
    
    print(f"Training data shape: {features_df.shape}")
    print(f"Target distribution: {target_series.value_counts().to_dict()}")
    
    print(f"\nTraining {model_type} model...")
    model = GapClosureMLModel(model_type=model_type)
    
    print("Training model...")
    metrics = model.train(
        features_df=features_df,
        target_series=target_series,
        handle_imbalance=True,
        cross_validate=True
    )
    
    print("\nTraining Metrics:")
    print(f"  Accuracy: {metrics['accuracy']:.3f}")
    print(f"  Precision: {metrics['precision']:.3f}")
    print(f"  Recall: {metrics['recall']:.3f}")
    print(f"  F1 Score: {metrics['f1_score']:.3f}")
    print(f"  ROC AUC: {metrics['roc_auc']:.3f}")
    if 'cv_mean' in metrics:
        print(f"  CV Mean: {metrics['cv_mean']:.3f} ± {metrics['cv_std']:.3f}")
    
    print("\nTop 10 Features:")
    for feature, importance in list(metrics['feature_importance'].items())[:10]:
        print(f"  {feature}: {importance:.4f}")
    
    # Save model
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    model.save_model(output_path)
    print(f"\nModel saved to: {output_path}")
    
    return metrics


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Train gap closure prediction model")
    parser.add_argument("--model-type", choices=['xgboost', 'random_forest'], default='xgboost')
    parser.add_argument("--n-samples", type=int, default=10000)
    parser.add_argument("--output", default='models/gap_closure_model.pkl')
    
    args = parser.parse_args()
    
    train_model(
        model_type=args.model_type,
        n_samples=args.n_samples,
        output_path=args.output
    )

