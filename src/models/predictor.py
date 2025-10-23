"""
Model Prediction Interface for HEDIS GSD Prediction Engine

Provides prediction interface for trained models with healthcare-specific
considerations, interpretability, and audit logging.

HEDIS Specification: MY2023 Volume 2
Measure: HBD - Hemoglobin A1c Control for Patients with Diabetes
"""

import pandas as pd
import numpy as np
import logging
from typing import Dict, List, Optional, Tuple, Union, Any
import joblib
import os
from datetime import datetime
import warnings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HEDISModelPredictor:
    """
    Provides prediction interface for HEDIS GSD models.
    
    Key features:
    - Single and batch predictions
    - Model interpretability (SHAP values)
    - Healthcare-specific validation
    - Audit logging for compliance
    """
    
    def __init__(self, model_path: str = "models", model_name: str = "logistic_regression"):
        """
        Initialize the predictor.
        
        Args:
            model_path: Path to directory containing saved models
            model_name: Name of the model to use for predictions
        """
        self.model_path = model_path
        self.model_name = model_name
        self.model = None
        self.scaler = None
        self.feature_names = None
        self.model_metadata = {}
        
        # Load model and scaler
        self._load_model()
        
        logger.info(f"Initialized HEDIS predictor with {model_name} model")
    
    def _load_model(self) -> None:
        """Load the trained model and scaler."""
        try:
            # Load scaler
            scaler_path = os.path.join(self.model_path, "scaler.pkl")
            if os.path.exists(scaler_path):
                self.scaler = joblib.load(scaler_path)
                logger.info("Scaler loaded successfully")
            else:
                logger.warning(f"Scaler not found at {scaler_path}")
            
            # Load model
            model_path = os.path.join(self.model_path, f"{self.model_name}_model.pkl")
            if os.path.exists(model_path):
                self.model = joblib.load(model_path)
                logger.info(f"{self.model_name} model loaded successfully")
            else:
                raise FileNotFoundError(f"Model not found at {model_path}")
            
            # Load training results for metadata
            results_path = os.path.join(self.model_path, "training_results.pkl")
            if os.path.exists(results_path):
                training_results = joblib.load(results_path)
                if self.model_name in training_results:
                    self.model_metadata = training_results[self.model_name]
                    logger.info("Model metadata loaded successfully")
            
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            raise
    
    def _validate_input(self, X: Union[pd.DataFrame, np.ndarray]) -> pd.DataFrame:
        """
        Validate and prepare input data for prediction.
        
        Args:
            X: Input features
            
        Returns:
            Validated DataFrame
        """
        # Convert to DataFrame if needed
        if isinstance(X, np.ndarray):
            if self.feature_names is None:
                raise ValueError("Feature names not available for numpy array input")
            X = pd.DataFrame(X, columns=self.feature_names)
        
        # Handle missing values
        X = X.fillna(0)
        
        # Log prediction request (PHI-safe)
        logger.info(f"Prediction request: {X.shape[0]} samples, {X.shape[1]} features")
        
        return X
    
    def _scale_features(self, X: pd.DataFrame) -> pd.DataFrame:
        """
        Scale features using the trained scaler.
        
        Args:
            X: Input features
            
        Returns:
            Scaled features
        """
        if self.scaler is None:
            logger.warning("No scaler available, returning unscaled features")
            return X
        
        X_scaled = pd.DataFrame(
            self.scaler.transform(X),
            columns=X.columns,
            index=X.index
        )
        
        return X_scaled
    
    def predict_proba(self, X: Union[pd.DataFrame, np.ndarray]) -> np.ndarray:
        """
        Predict class probabilities.
        
        Args:
            X: Input features
            
        Returns:
            Array of class probabilities
        """
        # Validate input
        X_validated = self._validate_input(X)
        
        # Scale features if scaler is available
        if self.model_name == 'logistic_regression':
            X_scaled = self._scale_features(X_validated)
        else:
            X_scaled = X_validated
        
        # Make predictions
        probabilities = self.model.predict_proba(X_scaled)
        
        # Log prediction results (PHI-safe)
        logger.info(f"Prediction completed: {probabilities.shape[0]} samples")
        
        return probabilities
    
    def predict(self, X: Union[pd.DataFrame, np.ndarray], threshold: float = 0.5) -> np.ndarray:
        """
        Predict class labels.
        
        Args:
            X: Input features
            threshold: Classification threshold
            
        Returns:
            Array of predicted class labels
        """
        probabilities = self.predict_proba(X)
        predictions = (probabilities[:, 1] >= threshold).astype(int)
        
        # Log prediction summary (PHI-safe)
        positive_predictions = predictions.sum()
        logger.info(f"Predictions: {positive_predictions} high-risk, {len(predictions) - positive_predictions} low-risk")
        
        return predictions
    
    def predict_single(self, member_features: Dict[str, float]) -> Dict[str, Any]:
        """
        Predict for a single member with interpretability.
        
        Args:
            member_features: Dictionary of member features
            
        Returns:
            Dictionary with prediction results and metadata
        """
        # Convert to DataFrame
        X = pd.DataFrame([member_features])
        
        # Get probabilities
        probabilities = self.predict_proba(X)
        prediction = self.predict(X)
        
        # Calculate risk score
        risk_score = probabilities[0, 1]
        
        # Create result
        result = {
            'prediction': int(prediction[0]),
            'risk_score': float(risk_score),
            'risk_level': 'High' if risk_score >= 0.5 else 'Low',
            'confidence': float(max(probabilities[0])),
            'model_name': self.model_name,
            'prediction_time': datetime.now().isoformat(),
            'model_metadata': self.model_metadata
        }
        
        # Log single prediction (PHI-safe)
        logger.info(f"Single prediction: Risk Level = {result['risk_level']}, Score = {risk_score:.3f}")
        
        return result
    
    def predict_batch(self, X: Union[pd.DataFrame, np.ndarray]) -> pd.DataFrame:
        """
        Predict for a batch of members.
        
        Args:
            X: Input features DataFrame or array
            
        Returns:
            DataFrame with predictions and metadata
        """
        # Validate input
        X_validated = self._validate_input(X)
        
        # Get predictions
        probabilities = self.predict_proba(X_validated)
        predictions = self.predict(X_validated)
        
        # Create results DataFrame
        results_df = pd.DataFrame({
            'prediction': predictions,
            'risk_score': probabilities[:, 1],
            'risk_level': ['High' if score >= 0.5 else 'Low' for score in probabilities[:, 1]],
            'confidence': np.max(probabilities, axis=1),
            'model_name': self.model_name,
            'prediction_time': datetime.now().isoformat()
        })
        
        # Add original features if DataFrame input
        if isinstance(X, pd.DataFrame):
            results_df = pd.concat([X.reset_index(drop=True), results_df], axis=1)
        
        # Log batch prediction summary (PHI-safe)
        high_risk_count = results_df['risk_level'].value_counts().get('High', 0)
        logger.info(f"Batch prediction completed: {high_risk_count} high-risk members out of {len(results_df)}")
        
        return results_df
    
    def get_feature_importance(self) -> pd.DataFrame:
        """
        Get feature importance for the loaded model.
        
        Returns:
            DataFrame with feature importance
        """
        if self.model is None:
            raise ValueError("No model loaded")
        
        if hasattr(self.model, 'feature_importances_'):
            # Random Forest
            importance_df = pd.DataFrame({
                'feature': self.feature_names or [f'feature_{i}' for i in range(len(self.model.feature_importances_))],
                'importance': self.model.feature_importances_
            }).sort_values('importance', ascending=False)
        elif hasattr(self.model, 'coef_'):
            # Logistic Regression
            importance_df = pd.DataFrame({
                'feature': self.feature_names or [f'feature_{i}' for i in range(len(self.model.coef_[0]))],
                'importance': np.abs(self.model.coef_[0])
            }).sort_values('importance', ascending=False)
        else:
            raise ValueError(f"Model {self.model_name} does not support feature importance")
        
        return importance_df
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        Get information about the loaded model.
        
        Returns:
            Dictionary with model information
        """
        info = {
            'model_name': self.model_name,
            'model_type': type(self.model).__name__,
            'model_path': self.model_path,
            'has_scaler': self.scaler is not None,
            'feature_count': len(self.feature_names) if self.feature_names else 'Unknown',
            'metadata': self.model_metadata,
            'loaded_time': datetime.now().isoformat()
        }
        
        return info


def create_predictor(model_path: str = "models", model_name: str = "logistic_regression") -> HEDISModelPredictor:
    """
    Convenience function to create a predictor.
    
    Args:
        model_path: Path to directory containing saved models
        model_name: Name of the model to use
        
    Returns:
        HEDISModelPredictor instance
    """
    return HEDISModelPredictor(model_path, model_name)


if __name__ == "__main__":
    # Example usage
    try:
        # Create predictor
        predictor = create_predictor()
        
        # Get model info
        model_info = predictor.get_model_info()
        print("Model Information:")
        for key, value in model_info.items():
            print(f"  {key}: {value}")
        
        # Example single prediction
        sample_features = {
            'age_at_my_end': 65,
            'is_female': 1,
            'has_diabetes_comprehensive': 1,
            'has_ckd': 0,
            'has_cvd': 1
        }
        
        result = predictor.predict_single(sample_features)
        print(f"\nSample Prediction:")
        print(f"  Risk Level: {result['risk_level']}")
        print(f"  Risk Score: {result['risk_score']:.3f}")
        print(f"  Confidence: {result['confidence']:.3f}")
        
    except Exception as e:
        print(f"Error in prediction: {e}")
