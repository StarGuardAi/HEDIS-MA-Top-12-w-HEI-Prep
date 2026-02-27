"""
ML Model for Gap Closure Prediction
XGBoost/Random Forest model training and prediction
"""
import pandas as pd
import numpy as np
import pickle
import json
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

try:
    import xgboost as xgb
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
    from sklearn.metrics import (
        accuracy_score, precision_score, recall_score, f1_score,
        roc_auc_score, confusion_matrix, classification_report
    )
    from sklearn.preprocessing import StandardScaler
    try:
        from imblearn.over_sampling import SMOTE
        SMOTE_AVAILABLE = True
    except ImportError:
        SMOTE_AVAILABLE = False
        # SMOTE is optional - model can work without it
    ML_LIBRARIES_AVAILABLE = True
except ImportError as e:
    ML_LIBRARIES_AVAILABLE = False
    SMOTE_AVAILABLE = False


class GapClosureMLModel:
    """
    Machine Learning model for predicting gap closure likelihood.
    Uses XGBoost or Random Forest with feature engineering.
    """
    
    def __init__(self, model_type: str = 'xgboost'):
        """
        Initialize ML model.
        
        Args:
            model_type: 'xgboost' or 'random_forest'
        """
        if not ML_LIBRARIES_AVAILABLE:
            raise ImportError("ML libraries not available. Install: pip install xgboost scikit-learn imbalanced-learn")
        
        self.model_type = model_type
        self.model = None
        self.scaler = StandardScaler()
        self.feature_names = []
        self.feature_importance = {}
        self.training_date = None
        self.model_version = "1.0"
        
        if model_type == 'xgboost':
            self.model = xgb.XGBClassifier(
                n_estimators=100,
                max_depth=6,
                learning_rate=0.1,
                random_state=42,
                eval_metric='logloss'
            )
        else:
            self.model = RandomForestClassifier(
                n_estimators=100,
                max_depth=10,
                random_state=42,
                class_weight='balanced'
            )
    
    def prepare_training_data(
        self,
        features_df: pd.DataFrame,
        target_series: pd.Series,
        handle_imbalance: bool = True
    ) -> Tuple[pd.DataFrame, pd.Series, pd.DataFrame, pd.Series]:
        """
        Prepare training data with train/test split and optional imbalance handling.
        
        Args:
            features_df: Feature matrix
            target_series: Target variable (1 = closed, 0 = not closed)
            handle_imbalance: Whether to use SMOTE for class imbalance
        
        Returns:
            X_train, X_test, y_train, y_test
        """
        # Train/test split
        X_train, X_test, y_train, y_test = train_test_split(
            features_df,
            target_series,
            test_size=0.2,
            random_state=42,
            stratify=target_series
        )
        
        # Handle class imbalance
        if handle_imbalance and SMOTE_AVAILABLE:
            smote = SMOTE(random_state=42)
            X_train, y_train = smote.fit_resample(X_train, y_train)
        elif handle_imbalance and not SMOTE_AVAILABLE:
            # Log warning but continue without SMOTE
            import warnings
            warnings.warn("SMOTE not available - training without class balancing")
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Convert back to DataFrame
        X_train_df = pd.DataFrame(X_train_scaled, columns=X_train.columns, index=X_train.index)
        X_test_df = pd.DataFrame(X_test_scaled, columns=X_test.columns, index=X_test.index)
        
        return X_train_df, X_test_df, y_train, y_test
    
    def train(
        self,
        features_df: pd.DataFrame,
        target_series: pd.Series,
        handle_imbalance: bool = True,
        cross_validate: bool = True
    ) -> Dict:
        """
        Train the model.
        
        Args:
            features_df: Feature matrix
            target_series: Target variable
            handle_imbalance: Handle class imbalance
            cross_validate: Perform cross-validation
        
        Returns:
            Dictionary with training metrics
        """
        # Prepare data
        X_train, X_test, y_train, y_test = self.prepare_training_data(
            features_df, target_series, handle_imbalance
        )
        
        self.feature_names = list(X_train.columns)
        
        # Train model
        self.model.fit(X_train, y_train)
        
        # Make predictions
        y_pred = self.model.predict(X_test)
        y_pred_proba = self.model.predict_proba(X_test)[:, 1]
        
        # Calculate metrics
        metrics = {
            'accuracy': accuracy_score(y_test, y_pred),
            'precision': precision_score(y_test, y_pred, zero_division=0),
            'recall': recall_score(y_test, y_pred, zero_division=0),
            'f1_score': f1_score(y_test, y_pred, zero_division=0),
            'roc_auc': roc_auc_score(y_test, y_pred_proba) if len(np.unique(y_test)) > 1 else 0.0,
            'confusion_matrix': confusion_matrix(y_test, y_pred).tolist()
        }
        
        # Cross-validation
        if cross_validate:
            cv_scores = cross_val_score(
                self.model,
                X_train,
                y_train,
                cv=StratifiedKFold(n_splits=5, shuffle=True, random_state=42),
                scoring='roc_auc'
            )
            metrics['cv_mean'] = cv_scores.mean()
            metrics['cv_std'] = cv_scores.std()
        
        # Feature importance
        if self.model_type == 'xgboost':
            importance = self.model.feature_importances_
        else:
            importance = self.model.feature_importances_
        
        self.feature_importance = dict(zip(self.feature_names, importance))
        metrics['feature_importance'] = dict(sorted(
            self.feature_importance.items(),
            key=lambda x: x[1],
            reverse=True
        )[:20])  # Top 20 features
        
        self.training_date = datetime.now()
        
        return metrics
    
    def predict(
        self,
        features: pd.Series,
        return_confidence: bool = True
    ) -> Dict:
        """
        Predict gap closure likelihood.
        
        Args:
            features: Feature vector
            return_confidence: Return confidence interval
        
        Returns:
            Dictionary with prediction and metadata
        """
        if self.model is None:
            raise ValueError("Model not trained. Call train() first.")
        
        # Check if model is trained
        if not hasattr(self.scaler, 'mean_') or self.scaler.mean_ is None:
            raise ValueError("Model not trained. Please train the model first using the 'Train Model' section.")
        
        # Ensure features match training features
        feature_df = pd.DataFrame([features])
        feature_df = feature_df.reindex(columns=self.feature_names, fill_value=0)
        
        # Scale features
        feature_scaled = self.scaler.transform(feature_df)
        
        # Predict
        probability = self.model.predict_proba(feature_scaled)[0, 1]
        prediction = 1 if probability > 0.5 else 0
        
        result = {
            'closure_probability': float(probability * 100),  # Convert to percentage
            'prediction': int(prediction),
            'model_version': self.model_version,
            'prediction_date': datetime.now().isoformat()
        }
        
        # Confidence interval (simplified - would use proper statistical methods)
        if return_confidence:
            # Bootstrap or use model uncertainty
            std_error = 0.05  # Simplified
            result['confidence_interval_lower'] = max(0, (probability - 1.96 * std_error) * 100)
            result['confidence_interval_upper'] = min(100, (probability + 1.96 * std_error) * 100)
        
        # Key influencing factors
        feature_values = feature_df.iloc[0].to_dict()
        top_features = sorted(
            self.feature_importance.items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]
        
        influencing_factors = []
        for feature_name, importance in top_features:
            value = feature_values.get(feature_name, 0)
            influencing_factors.append({
                'feature': feature_name,
                'importance': float(importance),
                'value': float(value)
            })
        
        result['influencing_factors'] = influencing_factors
        
        # Recommended intervention type
        result['recommended_intervention'] = self._recommend_intervention(features, probability)
        
        # Estimated time to close
        result['estimated_days_to_close'] = self._estimate_time_to_close(probability)
        
        return result
    
    def _recommend_intervention(self, features: pd.Series, probability: float) -> str:
        """Recommend intervention type based on features and probability."""
        if probability > 0.7:
            return "Phone"  # High probability, use direct contact
        elif features.get('prefers_sms', 0) == 1:
            return "SMS"
        elif features.get('prefers_email', 0) == 1:
            return "Email"
        else:
            return "Phone"
    
    def _estimate_time_to_close(self, probability: float) -> int:
        """Estimate days to close based on probability."""
        # Simplified model - would use regression in production
        if probability > 0.8:
            return 7
        elif probability > 0.6:
            return 14
        elif probability > 0.4:
            return 21
        else:
            return 30
    
    def save_model(self, filepath: str):
        """Save trained model to file."""
        model_data = {
            'model': self.model,
            'scaler': self.scaler,
            'feature_names': self.feature_names,
            'feature_importance': self.feature_importance,
            'training_date': self.training_date.isoformat() if self.training_date else None,
            'model_version': self.model_version,
            'model_type': self.model_type
        }
        
        with open(filepath, 'wb') as f:
            pickle.dump(model_data, f)
    
    def load_model(self, filepath: str):
        """Load trained model from file."""
        with open(filepath, 'rb') as f:
            model_data = pickle.load(f)
        
        self.model = model_data['model']
        self.scaler = model_data['scaler']
        self.feature_names = model_data['feature_names']
        self.feature_importance = model_data['feature_importance']
        self.training_date = datetime.fromisoformat(model_data['training_date']) if model_data['training_date'] else None
        self.model_version = model_data.get('model_version', '1.0')
        self.model_type = model_data.get('model_type', 'xgboost')

