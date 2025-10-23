"""
Model Evaluation for HEDIS GSD Prediction Engine

Provides comprehensive model evaluation with healthcare-specific metrics,
bias detection, and clinical validation.

HEDIS Specification: MY2023 Volume 2
Measure: HBD - Hemoglobin A1c Control for Patients with Diabetes
"""

import pandas as pd
import numpy as np
import logging
from typing import Dict, List, Optional, Tuple, Union, Any
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, roc_curve, precision_recall_curve,
    confusion_matrix, classification_report
)
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HEDISModelEvaluator:
    """
    Evaluates HEDIS GSD models with healthcare-specific metrics.
    
    Key features:
    - Clinical performance metrics
    - Bias detection across demographics
    - Temporal validation
    - Interpretability analysis
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        """
        Initialize the evaluator.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config or self._default_config()
        self.evaluation_results = {}
        
        logger.info("Initialized HEDIS model evaluator")
    
    def _default_config(self) -> Dict[str, Any]:
        """Return default configuration."""
        return {
            'threshold': 0.5,
            'demographic_groups': ['age_group', 'sex', 'race'],
            'clinical_thresholds': {
                'high_risk': 0.7,
                'medium_risk': 0.3,
                'low_risk': 0.1
            },
            'bias_metrics': ['demographic_parity', 'equalized_odds'],
            'plotting': {
                'figsize': (12, 8),
                'dpi': 100,
                'style': 'default'
            }
        }
    
    def evaluate_model(self, y_true: np.ndarray, y_pred: np.ndarray, 
                      y_proba: np.ndarray = None, X: pd.DataFrame = None) -> Dict[str, Any]:
        """
        Comprehensive model evaluation.
        
        Args:
            y_true: True labels
            y_pred: Predicted labels
            y_proba: Predicted probabilities (optional)
            X: Feature matrix for demographic analysis (optional)
            
        Returns:
            Dictionary with evaluation results
        """
        logger.info("Starting comprehensive model evaluation")
        
        results = {}
        
        # Basic metrics
        results['basic_metrics'] = self._calculate_basic_metrics(y_true, y_pred, y_proba)
        
        # Clinical metrics
        results['clinical_metrics'] = self._calculate_clinical_metrics(y_true, y_pred, y_proba)
        
        # Confusion matrix
        results['confusion_matrix'] = self._calculate_confusion_matrix(y_true, y_pred)
        
        # ROC analysis
        if y_proba is not None:
            results['roc_analysis'] = self._calculate_roc_metrics(y_true, y_proba)
        
        # Demographic bias analysis
        if X is not None:
            results['bias_analysis'] = self._analyze_demographic_bias(y_true, y_pred, y_proba, X)
        
        # Store results
        self.evaluation_results = results
        
        # Log summary (PHI-safe)
        logger.info("Model evaluation completed:")
        logger.info(f"  Accuracy: {results['basic_metrics']['accuracy']:.3f}")
        logger.info(f"  Precision: {results['basic_metrics']['precision']:.3f}")
        logger.info(f"  Recall: {results['basic_metrics']['recall']:.3f}")
        logger.info(f"  F1-Score: {results['basic_metrics']['f1']:.3f}")
        if y_proba is not None:
            logger.info(f"  AUC-ROC: {results['roc_analysis']['auc']:.3f}")
        
        return results
    
    def _calculate_basic_metrics(self, y_true: np.ndarray, y_pred: np.ndarray, 
                                y_proba: np.ndarray = None) -> Dict[str, float]:
        """Calculate basic classification metrics."""
        metrics = {
            'accuracy': accuracy_score(y_true, y_pred),
            'precision': precision_score(y_true, y_pred, zero_division=0),
            'recall': recall_score(y_true, y_pred, zero_division=0),
            'f1': f1_score(y_true, y_pred, zero_division=0),
            'specificity': self._calculate_specificity(y_true, y_pred),
            'npv': self._calculate_npv(y_true, y_pred)  # Negative Predictive Value
        }
        
        if y_proba is not None:
            metrics['auc_roc'] = roc_auc_score(y_true, y_proba)
        
        return metrics
    
    def _calculate_clinical_metrics(self, y_true: np.ndarray, y_pred: np.ndarray, 
                                   y_proba: np.ndarray = None) -> Dict[str, Any]:
        """Calculate healthcare-specific metrics."""
        tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
        
        clinical_metrics = {
            'sensitivity': tp / (tp + fn) if (tp + fn) > 0 else 0,  # Same as recall
            'specificity': tn / (tn + fp) if (tn + fp) > 0 else 0,
            'positive_predictive_value': tp / (tp + fp) if (tp + fp) > 0 else 0,  # Same as precision
            'negative_predictive_value': tn / (tn + fn) if (tn + fn) > 0 else 0,
            'false_positive_rate': fp / (fp + tn) if (fp + tn) > 0 else 0,
            'false_negative_rate': fn / (fn + tp) if (fn + tp) > 0 else 0,
            'likelihood_ratio_positive': self._calculate_lr_positive(tp, fp, fn, tn),
            'likelihood_ratio_negative': self._calculate_lr_negative(tp, fp, fn, tn)
        }
        
        # Risk stratification
        if y_proba is not None:
            clinical_metrics['risk_stratification'] = self._analyze_risk_stratification(y_true, y_proba)
        
        return clinical_metrics
    
    def _calculate_confusion_matrix(self, y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, Any]:
        """Calculate confusion matrix and related metrics."""
        cm = confusion_matrix(y_true, y_pred)
        tn, fp, fn, tp = cm.ravel()
        
        return {
            'matrix': cm,
            'true_negatives': int(tn),
            'false_positives': int(fp),
            'false_negatives': int(fn),
            'true_positives': int(tp),
            'total_samples': int(tn + fp + fn + tp)
        }
    
    def _calculate_roc_metrics(self, y_true: np.ndarray, y_proba: np.ndarray) -> Dict[str, Any]:
        """Calculate ROC curve metrics."""
        fpr, tpr, thresholds = roc_curve(y_true, y_proba)
        auc = roc_auc_score(y_true, y_proba)
        
        # Find optimal threshold (Youden's J statistic)
        j_scores = tpr - fpr
        optimal_idx = np.argmax(j_scores)
        optimal_threshold = thresholds[optimal_idx]
        
        return {
            'fpr': fpr,
            'tpr': tpr,
            'thresholds': thresholds,
            'auc': auc,
            'optimal_threshold': optimal_threshold,
            'optimal_tpr': tpr[optimal_idx],
            'optimal_fpr': fpr[optimal_idx]
        }
    
    def _analyze_demographic_bias(self, y_true: np.ndarray, y_pred: np.ndarray, 
                                y_proba: np.ndarray, X: pd.DataFrame) -> Dict[str, Any]:
        """Analyze bias across demographic groups."""
        bias_results = {}
        
        # Analyze by age groups
        if 'age_at_my_end' in X.columns:
            age_bias = self._analyze_age_bias(y_true, y_pred, y_proba, X['age_at_my_end'])
            bias_results['age_bias'] = age_bias
        
        # Analyze by sex
        if 'is_female' in X.columns:
            sex_bias = self._analyze_sex_bias(y_true, y_pred, y_proba, X['is_female'])
            bias_results['sex_bias'] = sex_bias
        
        # Analyze by race
        race_cols = [col for col in X.columns if col.startswith('is_') and 'race' in col]
        if race_cols:
            race_bias = self._analyze_race_bias(y_true, y_pred, y_proba, X[race_cols])
            bias_results['race_bias'] = race_bias
        
        return bias_results
    
    def _analyze_age_bias(self, y_true: np.ndarray, y_pred: np.ndarray, 
                         y_proba: np.ndarray, age_series: pd.Series) -> Dict[str, Any]:
        """Analyze bias by age groups."""
        # Create age groups
        age_groups = pd.cut(age_series, bins=[0, 45, 65, 100], labels=['18-44', '45-64', '65+'])
        
        age_bias = {}
        for age_group in age_groups.cat.categories:
            mask = age_groups == age_group
            if mask.sum() > 0:
                group_metrics = self._calculate_basic_metrics(
                    y_true[mask], y_pred[mask], y_proba[mask] if y_proba is not None else None
                )
                age_bias[age_group] = {
                    'sample_size': int(mask.sum()),
                    'metrics': group_metrics
                }
        
        return age_bias
    
    def _analyze_sex_bias(self, y_true: np.ndarray, y_pred: np.ndarray, 
                         y_proba: np.ndarray, sex_series: pd.Series) -> Dict[str, Any]:
        """Analyze bias by sex."""
        sex_bias = {}
        
        for sex in [0, 1]:  # 0 = male, 1 = female
            mask = sex_series == sex
            if mask.sum() > 0:
                sex_label = 'female' if sex == 1 else 'male'
                group_metrics = self._calculate_basic_metrics(
                    y_true[mask], y_pred[mask], y_proba[mask] if y_proba is not None else None
                )
                sex_bias[sex_label] = {
                    'sample_size': int(mask.sum()),
                    'metrics': group_metrics
                }
        
        return sex_bias
    
    def _analyze_race_bias(self, y_true: np.ndarray, y_pred: np.ndarray, 
                          y_proba: np.ndarray, race_df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze bias by race."""
        race_bias = {}
        
        for race_col in race_df.columns:
            mask = race_df[race_col] == 1
            if mask.sum() > 0:
                race_label = race_col.replace('is_', '').replace('_', ' ')
                group_metrics = self._calculate_basic_metrics(
                    y_true[mask], y_pred[mask], y_proba[mask] if y_proba is not None else None
                )
                race_bias[race_label] = {
                    'sample_size': int(mask.sum()),
                    'metrics': group_metrics
                }
        
        return race_bias
    
    def _analyze_risk_stratification(self, y_true: np.ndarray, y_proba: np.ndarray) -> Dict[str, Any]:
        """Analyze risk stratification performance."""
        thresholds = self.config['clinical_thresholds']
        
        risk_stratification = {}
        for risk_level, threshold in thresholds.items():
            high_risk_mask = y_proba >= threshold
            if high_risk_mask.sum() > 0:
                risk_stratification[risk_level] = {
                    'threshold': threshold,
                    'high_risk_count': int(high_risk_mask.sum()),
                    'high_risk_rate': float(high_risk_mask.mean()),
                    'precision_in_high_risk': float(y_true[high_risk_mask].mean()) if high_risk_mask.sum() > 0 else 0
                }
        
        return risk_stratification
    
    def _calculate_specificity(self, y_true: np.ndarray, y_pred: np.ndarray) -> float:
        """Calculate specificity (true negative rate)."""
        tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
        return tn / (tn + fp) if (tn + fp) > 0 else 0
    
    def _calculate_npv(self, y_true: np.ndarray, y_pred: np.ndarray) -> float:
        """Calculate negative predictive value."""
        tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
        return tn / (tn + fn) if (tn + fn) > 0 else 0
    
    def _calculate_lr_positive(self, tp: int, fp: int, fn: int, tn: int) -> float:
        """Calculate positive likelihood ratio."""
        sensitivity = tp / (tp + fn) if (tp + fn) > 0 else 0
        specificity = tn / (tn + fp) if (tn + fp) > 0 else 0
        return sensitivity / (1 - specificity) if specificity < 1 else float('inf')
    
    def _calculate_lr_negative(self, tp: int, fp: int, fn: int, tn: int) -> float:
        """Calculate negative likelihood ratio."""
        sensitivity = tp / (tp + fn) if (tp + fn) > 0 else 0
        specificity = tn / (tn + fp) if (tn + fp) > 0 else 0
        return (1 - sensitivity) / specificity if specificity > 0 else float('inf')
    
    def generate_evaluation_report(self, output_path: str = None) -> str:
        """
        Generate comprehensive evaluation report.
        
        Args:
            output_path: Path to save report (optional)
            
        Returns:
            Report text
        """
        if not self.evaluation_results:
            raise ValueError("No evaluation results available. Run evaluate_model first.")
        
        report_lines = []
        report_lines.append("HEDIS GSD Model Evaluation Report")
        report_lines.append("=" * 50)
        report_lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append("")
        
        # Basic metrics
        basic_metrics = self.evaluation_results['basic_metrics']
        report_lines.append("Basic Performance Metrics:")
        report_lines.append("-" * 30)
        for metric, value in basic_metrics.items():
            report_lines.append(f"{metric.replace('_', ' ').title()}: {value:.3f}")
        report_lines.append("")
        
        # Clinical metrics
        clinical_metrics = self.evaluation_results['clinical_metrics']
        report_lines.append("Clinical Performance Metrics:")
        report_lines.append("-" * 30)
        for metric, value in clinical_metrics.items():
            if isinstance(value, dict):
                report_lines.append(f"{metric.replace('_', ' ').title()}:")
                for sub_metric, sub_value in value.items():
                    report_lines.append(f"  {sub_metric}: {sub_value}")
            else:
                report_lines.append(f"{metric.replace('_', ' ').title()}: {value:.3f}")
        report_lines.append("")
        
        # Confusion matrix
        cm_results = self.evaluation_results['confusion_matrix']
        report_lines.append("Confusion Matrix:")
        report_lines.append("-" * 30)
        report_lines.append(f"True Negatives: {cm_results['true_negatives']}")
        report_lines.append(f"False Positives: {cm_results['false_positives']}")
        report_lines.append(f"False Negatives: {cm_results['false_negatives']}")
        report_lines.append(f"True Positives: {cm_results['true_positives']}")
        report_lines.append("")
        
        # Bias analysis
        if 'bias_analysis' in self.evaluation_results:
            bias_analysis = self.evaluation_results['bias_analysis']
            report_lines.append("Demographic Bias Analysis:")
            report_lines.append("-" * 30)
            for group_type, group_results in bias_analysis.items():
                report_lines.append(f"{group_type.replace('_', ' ').title()}:")
                for group_name, group_metrics in group_results.items():
                    report_lines.append(f"  {group_name}:")
                    report_lines.append(f"    Sample Size: {group_metrics['sample_size']}")
                    report_lines.append(f"    Accuracy: {group_metrics['metrics']['accuracy']:.3f}")
                    report_lines.append(f"    Precision: {group_metrics['metrics']['precision']:.3f}")
                    report_lines.append(f"    Recall: {group_metrics['metrics']['recall']:.3f}")
            report_lines.append("")
        
        report_text = "\n".join(report_lines)
        
        # Save report if path provided
        if output_path:
            with open(output_path, 'w') as f:
                f.write(report_text)
            logger.info(f"Evaluation report saved to {output_path}")
        
        return report_text


def evaluate_hedis_model(y_true: np.ndarray, y_pred: np.ndarray, 
                        y_proba: np.ndarray = None, X: pd.DataFrame = None,
                        config: Dict[str, Any] = None) -> HEDISModelEvaluator:
    """
    Convenience function to evaluate a HEDIS model.
    
    Args:
        y_true: True labels
        y_pred: Predicted labels
        y_proba: Predicted probabilities (optional)
        X: Feature matrix for demographic analysis (optional)
        config: Configuration dictionary
        
    Returns:
        HEDISModelEvaluator instance with results
    """
    evaluator = HEDISModelEvaluator(config)
    evaluator.evaluate_model(y_true, y_pred, y_proba, X)
    return evaluator


if __name__ == "__main__":
    # Example usage
    from sklearn.datasets import make_classification
    from sklearn.model_selection import train_test_split
    from sklearn.linear_model import LogisticRegression
    
    # Generate sample data
    X, y = make_classification(n_samples=1000, n_features=10, n_classes=2, random_state=42)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train model
    model = LogisticRegression(random_state=42)
    model.fit(X_train, y_train)
    
    # Make predictions
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]
    
    # Evaluate model
    evaluator = evaluate_hedis_model(y_test, y_pred, y_proba)
    
    # Generate report
    report = evaluator.generate_evaluation_report()
    print(report)
