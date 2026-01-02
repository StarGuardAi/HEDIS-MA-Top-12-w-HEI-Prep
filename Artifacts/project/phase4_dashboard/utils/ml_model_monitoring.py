"""
ML Model Monitoring and Drift Detection
Monitor model performance and detect data drift
"""
from typing import Dict, List, Optional
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path
import json


class ModelMonitor:
    """
    Monitor ML model performance and detect drift.
    """
    
    def __init__(self, model_path: Optional[str] = None):
        self.model_path = model_path
        self.performance_history = []
        self.prediction_history = []
        self.drift_threshold = 0.1  # 10% drift threshold
    
    def log_prediction(
        self,
        prediction: Dict,
        actual_outcome: Optional[bool] = None,
        prediction_date: Optional[datetime] = None
    ):
        """Log prediction for monitoring."""
        log_entry = {
            'prediction_date': prediction_date or datetime.now(),
            'closure_probability': prediction.get('closure_probability', 0),
            'prediction': prediction.get('prediction', 0),
            'actual_outcome': actual_outcome,
            'model_version': prediction.get('model_version', '1.0')
        }
        
        self.prediction_history.append(log_entry)
        
        # Keep only last 10000 predictions
        if len(self.prediction_history) > 10000:
            self.prediction_history = self.prediction_history[-10000:]
    
    def calculate_performance_metrics(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> Dict:
        """Calculate performance metrics for a period."""
        if not self.prediction_history:
            return {}
        
        # Filter by date range
        if start_date or end_date:
            filtered = [
                p for p in self.prediction_history
                if (not start_date or p['prediction_date'] >= start_date)
                and (not end_date or p['prediction_date'] <= end_date)
            ]
        else:
            filtered = self.prediction_history
        
        if not filtered:
            return {}
        
        # Only include predictions with actual outcomes
        with_outcomes = [p for p in filtered if p['actual_outcome'] is not None]
        
        if not with_outcomes:
            return {
                'total_predictions': len(filtered),
                'predictions_with_outcomes': 0
            }
        
        # Calculate metrics
        y_true = [p['actual_outcome'] for p in with_outcomes]
        y_pred = [p['prediction'] for p in with_outcomes]
        y_proba = [p['closure_probability'] / 100.0 for p in with_outcomes]
        
        # Accuracy
        accuracy = sum(1 for i in range(len(y_true)) if y_true[i] == y_pred[i]) / len(y_true)
        
        # Precision, Recall, F1
        tp = sum(1 for i in range(len(y_true)) if y_true[i] == 1 and y_pred[i] == 1)
        fp = sum(1 for i in range(len(y_true)) if y_true[i] == 0 and y_pred[i] == 1)
        fn = sum(1 for i in range(len(y_true)) if y_true[i] == 1 and y_pred[i] == 0)
        
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        
        # ROC AUC
        try:
            from sklearn.metrics import roc_auc_score
            roc_auc = roc_auc_score(y_true, y_proba)
        except:
            roc_auc = 0.0
        
        # Prediction distribution
        prob_buckets = {
            '0-20%': sum(1 for p in y_proba if 0 <= p < 0.2),
            '20-40%': sum(1 for p in y_proba if 0.2 <= p < 0.4),
            '40-60%': sum(1 for p in y_proba if 0.4 <= p < 0.6),
            '60-80%': sum(1 for p in y_proba if 0.6 <= p < 0.8),
            '80-100%': sum(1 for p in y_proba if 0.8 <= p <= 1.0)
        }
        
        # Success rate by bucket
        success_by_bucket = {}
        for bucket, count in prob_buckets.items():
            if count > 0:
                bucket_predictions = [
                    p for p in with_outcomes
                    if self._get_bucket(p['closure_probability'] / 100.0) == bucket
                ]
                successes = sum(1 for p in bucket_predictions if p['actual_outcome'] == 1)
                success_by_bucket[bucket] = successes / len(bucket_predictions) if bucket_predictions else 0
        
        return {
            'total_predictions': len(filtered),
            'predictions_with_outcomes': len(with_outcomes),
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1_score': f1,
            'roc_auc': roc_auc,
            'prediction_distribution': prob_buckets,
            'success_rate_by_bucket': success_by_bucket
        }
    
    def detect_drift(
        self,
        current_features: pd.DataFrame,
        reference_features: Optional[pd.DataFrame] = None
    ) -> Dict:
        """Detect data drift in features."""
        if reference_features is None:
            # Use historical data as reference
            return {'drift_detected': False, 'message': 'No reference data'}
        
        drift_results = {}
        
        # Compare feature distributions
        for col in current_features.columns:
            if col in reference_features.columns:
                current_mean = current_features[col].mean()
                reference_mean = reference_features[col].mean()
                
                if reference_mean != 0:
                    drift_pct = abs((current_mean - reference_mean) / reference_mean)
                    if drift_pct > self.drift_threshold:
                        drift_results[col] = {
                            'drift_detected': True,
                            'drift_percentage': drift_pct * 100,
                            'current_mean': current_mean,
                            'reference_mean': reference_mean
                        }
        
        return {
            'drift_detected': len(drift_results) > 0,
            'features_with_drift': drift_results,
            'total_features_checked': len(current_features.columns)
        }
    
    def _get_bucket(self, probability: float) -> str:
        """Get probability bucket."""
        if 0 <= probability < 0.2:
            return '0-20%'
        elif 0.2 <= probability < 0.4:
            return '20-40%'
        elif 0.4 <= probability < 0.6:
            return '40-60%'
        elif 0.6 <= probability < 0.8:
            return '60-80%'
        else:
            return '80-100%'
    
    def save_performance_history(self, filepath: str):
        """Save performance history to file."""
        with open(filepath, 'w') as f:
            json.dump(self.performance_history, f, default=str, indent=2)
    
    def load_performance_history(self, filepath: str):
        """Load performance history from file."""
        with open(filepath, 'r') as f:
            self.performance_history = json.load(f)

