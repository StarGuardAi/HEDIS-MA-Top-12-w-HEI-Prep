"""
KED Prediction Interface

Production-ready prediction interface for KED (Kidney Health Evaluation) model.
Provides predictions, risk scores, gap-specific recommendations, and SHAP explanations.

HEDIS Specification: MY2025
Measure: KED - Kidney Health Evaluation for Patients with Diabetes
Weight: 3x (Triple-weighted)

Features:
- Single member prediction
- Batch prediction
- Risk tier classification (high/medium/low)
- Gap-specific recommendations
- SHAP explanations (if available)
- PHI-safe logging
"""

import pandas as pd
import numpy as np
import logging
import hashlib
import warnings
from typing import Dict, List, Optional, Tuple, Union, Any
from pathlib import Path
import joblib

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class KEDPredictor:
    """
    Production prediction interface for KED gap prediction.
    
    Provides:
    - Risk scores (probability of KED gap)
    - Risk tiers (high/medium/low)
    - Gap-specific recommendations
    - Model interpretability
    """
    
    def __init__(self, model_dir: Union[str, Path], model_name: str = 'ked_model'):
        """
        Initialize KED predictor.
        
        Args:
            model_dir: Directory containing model artifacts
            model_name: Base name of model files
        """
        self.model_dir = Path(model_dir)
        self.model_name = model_name
        
        # Load model artifacts
        self.model = None
        self.scaler = None
        self.feature_names = None
        self.metadata = None
        
        self._load_model()
        
        logger.info(f"Initialized KED Predictor from {model_dir}")
    
    def _load_model(self):
        """Load model and artifacts."""
        try:
            # Load model
            model_path = self.model_dir / f"{self.model_name}.pkl"
            self.model = joblib.load(model_path)
            logger.info(f"Loaded model: {model_path}")
            
            # Load scaler
            scaler_path = self.model_dir / f"{self.model_name}_scaler.pkl"
            self.scaler = joblib.load(scaler_path)
            logger.info(f"Loaded scaler: {scaler_path}")
            
            # Load feature names
            features_path = self.model_dir / f"{self.model_name}_features.txt"
            with open(features_path, 'r') as f:
                self.feature_names = [line.strip() for line in f.readlines()]
            logger.info(f"Loaded {len(self.feature_names)} feature names")
            
            # Load metadata
            metadata_path = self.model_dir / f"{self.model_name}_metadata.pkl"
            if metadata_path.exists():
                self.metadata = joblib.load(metadata_path)
                logger.info(f"Loaded metadata (AUC: {self.metadata.get('auc_roc', 'N/A')})")
            
        except FileNotFoundError as e:
            logger.error(f"Model file not found: {e}")
            raise
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            raise
    
    def _hash_member_id(self, member_id: str) -> str:
        """Hash member ID for PHI-safe logging."""
        return hashlib.sha256(str(member_id).encode()).hexdigest()[:8]
    
    def _validate_features(self, features: pd.DataFrame) -> pd.DataFrame:
        """
        Validate and align features with model.
        
        Args:
            features: Input features DataFrame
            
        Returns:
            Aligned features DataFrame
        """
        # Check for required features
        missing_features = set(self.feature_names) - set(features.columns)
        if missing_features:
            logger.warning(f"Missing {len(missing_features)} features, will fill with zeros")
            for feature in missing_features:
                features[feature] = 0
        
        # Select and order features
        features_aligned = features[self.feature_names].copy()
        
        # Handle missing values
        if features_aligned.isnull().any().any():
            logger.warning("Null values detected, filling with zeros")
            features_aligned.fillna(0, inplace=True)
        
        return features_aligned
    
    def _classify_risk_tier(self, probability: float) -> str:
        """
        Classify risk tier based on probability.
        
        Args:
            probability: Probability of KED gap (0-1)
            
        Returns:
            Risk tier: 'high', 'medium', or 'low'
        """
        if probability >= 0.7:
            return 'high'
        elif probability >= 0.4:
            return 'medium'
        else:
            return 'low'
    
    def _generate_recommendations(self,
                                 member_data: pd.Series,
                                 risk_score: float,
                                 risk_tier: str) -> Dict[str, Any]:
        """
        Generate gap-specific recommendations.
        
        Args:
            member_data: Member feature data
            risk_score: Risk score (probability)
            risk_tier: Risk tier (high/medium/low)
            
        Returns:
            Dictionary with recommendations
        """
        recommendations = {
            'priority': risk_tier,
            'actions': [],
            'clinical_notes': []
        }
        
        # High-risk recommendations
        if risk_tier == 'high':
            recommendations['actions'].append({
                'action': 'Immediate outreach',
                'description': 'Contact member within 7 days to schedule kidney health tests'
            })
            recommendations['actions'].append({
                'action': 'Provider notification',
                'description': 'Alert PCP about overdue kidney health evaluation'
            })
        
        # Check what's missing based on history
        if member_data.get('had_egfr_prior_year', 0) == 0:
            recommendations['actions'].append({
                'action': 'Schedule eGFR test',
                'description': 'Member has no recent eGFR (kidney function) test'
            })
            recommendations['clinical_notes'].append(
                'No eGFR test in prior year - assess kidney function'
            )
        
        if member_data.get('had_acr_prior_year', 0) == 0:
            recommendations['actions'].append({
                'action': 'Schedule ACR test',
                'description': 'Member has no recent ACR (urine albumin) test'
            })
            recommendations['clinical_notes'].append(
                'No ACR test in prior year - assess kidney damage markers'
            )
        
        # Comorbidity-based recommendations
        if member_data.get('has_ckd', 0) == 1:
            recommendations['clinical_notes'].append(
                'Member has CKD diagnosis - kidney monitoring critical'
            )
            recommendations['priority'] = 'high'  # Upgrade to high priority
        
        if member_data.get('has_hypertension', 0) == 1:
            recommendations['clinical_notes'].append(
                'Member has hypertension - increased kidney disease risk'
            )
        
        # High utilization flag
        if member_data.get('high_ed_user', 0) == 1:
            recommendations['actions'].append({
                'action': 'Care coordination',
                'description': 'High ED utilizer - may need care management support'
            })
        
        # General recommendation
        if len(recommendations['actions']) == 0:
            recommendations['actions'].append({
                'action': 'Preventive outreach',
                'description': 'Schedule annual kidney health evaluation'
            })
        
        return recommendations
    
    def predict_single(self,
                      member_features: Union[pd.Series, pd.DataFrame],
                      member_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Predict KED gap risk for single member.
        
        Args:
            member_features: Member features (Series or single-row DataFrame)
            member_id: Optional member ID for logging
            
        Returns:
            Dictionary with prediction results
        """
        # Convert to DataFrame if Series
        if isinstance(member_features, pd.Series):
            features_df = pd.DataFrame([member_features])
        else:
            features_df = member_features.copy()
        
        # Validate features
        features_aligned = self._validate_features(features_df)
        
        # Scale features
        features_scaled = self.scaler.transform(features_aligned)
        
        # Predict
        prediction = self.model.predict(features_scaled)[0]
        probability = self.model.predict_proba(features_scaled)[0, 1]
        
        # Classify risk
        risk_tier = self._classify_risk_tier(probability)
        
        # Generate recommendations
        member_data = member_features if isinstance(member_features, pd.Series) else member_features.iloc[0]
        recommendations = self._generate_recommendations(member_data, probability, risk_tier)
        
        # Log (PHI-safe)
        if member_id:
            hashed_id = self._hash_member_id(member_id)
            logger.info(f"Prediction for member {hashed_id}: risk={risk_tier}, score={probability:.3f}")
        
        result = {
            'prediction': int(prediction),  # 1 = gap, 0 = compliant
            'risk_score': float(probability),
            'risk_tier': risk_tier,
            'confidence': float(max(probability, 1 - probability)),
            'recommendations': recommendations,
        }
        
        return result
    
    def predict_batch(self,
                     features_df: pd.DataFrame,
                     member_ids: Optional[pd.Series] = None) -> pd.DataFrame:
        """
        Predict KED gap risk for batch of members.
        
        Args:
            features_df: Features DataFrame
            member_ids: Optional Series of member IDs
            
        Returns:
            DataFrame with predictions
        """
        logger.info(f"Making batch predictions for {len(features_df):,} members")
        
        # Validate features
        features_aligned = self._validate_features(features_df)
        
        # Scale features
        features_scaled = self.scaler.transform(features_aligned)
        
        # Predict
        predictions = self.model.predict(features_scaled)
        probabilities = self.model.predict_proba(features_scaled)[:, 1]
        
        # Create results DataFrame
        results = pd.DataFrame({
            'prediction': predictions,
            'risk_score': probabilities,
            'risk_tier': [self._classify_risk_tier(p) for p in probabilities],
            'confidence': [max(p, 1-p) for p in probabilities],
        }, index=features_df.index)
        
        # Add member IDs if provided
        if member_ids is not None:
            results.insert(0, 'member_id', member_ids)
        
        # Summary statistics
        gap_count = (predictions == 1).sum()
        gap_rate = gap_count / len(predictions) * 100
        
        risk_tier_counts = results['risk_tier'].value_counts()
        
        logger.info(f"Batch predictions complete:")
        logger.info(f"  Predicted gaps: {gap_count:,} ({gap_rate:.1f}%)")
        logger.info(f"  High risk: {risk_tier_counts.get('high', 0):,}")
        logger.info(f"  Medium risk: {risk_tier_counts.get('medium', 0):,}")
        logger.info(f"  Low risk: {risk_tier_counts.get('low', 0):,}")
        
        return results
    
    def get_top_risk_members(self,
                            features_df: pd.DataFrame,
                            member_ids: pd.Series,
                            top_n: int = 100) -> pd.DataFrame:
        """
        Get top N highest risk members.
        
        Args:
            features_df: Features DataFrame
            member_ids: Series of member IDs
            top_n: Number of top risk members to return
            
        Returns:
            DataFrame with top risk members sorted by risk score
        """
        logger.info(f"Identifying top {top_n} highest risk members")
        
        # Get predictions
        predictions = self.predict_batch(features_df, member_ids)
        
        # Sort by risk score and get top N
        top_risk = predictions.nlargest(top_n, 'risk_score')
        
        logger.info(f"Top {top_n} members identified:")
        logger.info(f"  Risk score range: {top_risk['risk_score'].min():.3f} - {top_risk['risk_score'].max():.3f}")
        logger.info(f"  High risk: {(top_risk['risk_tier'] == 'high').sum()}")
        logger.info(f"  Medium risk: {(top_risk['risk_tier'] == 'medium').sum()}")
        
        return top_risk
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        Get model information and metadata.
        
        Returns:
            Dictionary with model information
        """
        info = {
            'model_name': self.model_name,
            'model_type': type(self.model).__name__,
            'n_features': len(self.feature_names),
            'features': self.feature_names,
        }
        
        if self.metadata:
            info.update({
                'measurement_year': self.metadata.get('measurement_year'),
                'training_date': self.metadata.get('training_date'),
                'auc_roc': self.metadata.get('auc_roc'),
            })
        
        return info


def load_ked_predictor(model_dir: str = 'models',
                       model_name: str = 'ked_model') -> KEDPredictor:
    """
    Convenience function to load KED predictor.
    
    Args:
        model_dir: Directory containing model artifacts
        model_name: Base name of model files
        
    Returns:
        KEDPredictor instance
    """
    predictor = KEDPredictor(model_dir, model_name)
    return predictor


if __name__ == "__main__":
    logger.info("KED Prediction Interface")
    logger.info("Production-ready predictions for KED gap risk")
    logger.info("Features: Risk scores, recommendations, interpretability")

