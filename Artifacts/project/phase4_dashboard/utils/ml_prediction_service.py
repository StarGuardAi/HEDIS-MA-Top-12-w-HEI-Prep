"""
ML Prediction Service
Real-time and batch prediction API
"""
from typing import Dict, List, Optional
import pandas as pd
from datetime import datetime
from pathlib import Path

from utils.ml_gap_closure_features import GapClosureFeatureEngineer
from utils.ml_gap_closure_model import GapClosureMLModel
from utils.ml_model_monitoring import ModelMonitor


class GapClosurePredictionService:
    """
    Prediction service for gap closure likelihood.
    Handles both real-time and batch predictions.
    """
    
    def __init__(self, model_path: Optional[str] = None):
        try:
            self.feature_engineer = GapClosureFeatureEngineer()
            self.model = GapClosureMLModel()
            self.monitor = ModelMonitor()
            
            # Load model if path provided
            if model_path and Path(model_path).exists():
                self.model.load_model(model_path)
            else:
                # Use default model (would be trained separately)
                self._initialize_default_model()
        except ImportError as e:
            # Re-raise ImportError so calling code can handle it
            raise
        except Exception as e:
            # For other errors, set model to None and continue
            self.model = None
            self.feature_engineer = None
            self.monitor = None
    
    def _initialize_default_model(self):
        """Initialize with default/placeholder model."""
        # In production, this would load a pre-trained model
        # For now, model can work without a pre-trained model file
        pass
    
    def predict_single(
        self,
        member_id: str,
        gap_data: Dict,
        member_data: Dict,
        engagement_data: Dict,
        operational_data: Dict
    ) -> Dict:
        """
        Real-time prediction for a single gap.
        
        Args:
            member_id: Member identifier
            gap_data: Gap information
            member_data: Member characteristics
            engagement_data: Engagement history
            operational_data: Operational factors
        
        Returns:
            Prediction dictionary with probability and recommendations
        """
        # Extract features
        features = self.feature_engineer.create_feature_vector(
            member_id=member_id,
            gap_data=gap_data,
            member_data=member_data,
            engagement_data=engagement_data,
            operational_data=operational_data
        )
        
        # Make prediction
        prediction = self.model.predict(features, return_confidence=True)
        
        # Log for monitoring
        self.monitor.log_prediction(prediction)
        
        return prediction
    
    def predict_batch(
        self,
        gaps: List[Dict],
        member_data_dict: Dict[str, Dict],
        engagement_data_dict: Dict[str, Dict],
        operational_data: Dict
    ) -> List[Dict]:
        """
        Batch prediction for multiple gaps.
        
        Args:
            gaps: List of gap dictionaries
            member_data_dict: Dictionary mapping member_id to member data
            engagement_data_dict: Dictionary mapping member_id to engagement data
            operational_data: Operational factors
        
        Returns:
            List of prediction dictionaries
        """
        predictions = []
        
        for gap in gaps:
            member_id = gap.get('member_id')
            member_data = member_data_dict.get(member_id, {})
            engagement_data = engagement_data_dict.get(member_id, {})
            
            prediction = self.predict_single(
                member_id=member_id,
                gap_data=gap,
                member_data=member_data,
                engagement_data=engagement_data,
                operational_data=operational_data
            )
            
            prediction['gap_id'] = gap.get('gap_id')
            prediction['member_id'] = member_id
            predictions.append(prediction)
        
        return predictions
    
    def get_model_performance(self, days: int = 30) -> Dict:
        """Get model performance metrics."""
        start_date = datetime.now() - pd.Timedelta(days=days)
        return self.monitor.calculate_performance_metrics(start_date=start_date)
    
    def check_drift(self, current_features: pd.DataFrame) -> Dict:
        """Check for data drift."""
        return self.monitor.detect_drift(current_features)

