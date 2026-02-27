"""
Unit Tests for HEDIS GSD Models Module

Tests model training, prediction, evaluation, and serialization functions
with healthcare compliance validation.
"""

import unittest
import pandas as pd
import numpy as np
from datetime import datetime
import tempfile
import os
from pathlib import Path
import joblib

# Import modules to test
from src.models.trainer import HEDISModelTrainer, train_hedis_gsd_models
from src.models.predictor import HEDISModelPredictor, create_predictor
from src.models.evaluator import HEDISModelEvaluator, evaluate_hedis_model
from src.models.serializer import HEDISModelSerializer, save_hedis_model, load_hedis_model


class TestHEDISModelTrainer(unittest.TestCase):
    """Test cases for HEDIS model trainer."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.trainer = HEDISModelTrainer()
        
        # Create sample feature data
        np.random.seed(42)
        self.sample_features = pd.DataFrame({
            'age_at_my_end': np.random.randint(18, 76, 100),
            'is_female': np.random.choice([0, 1], 100),
            'is_white': np.random.choice([0, 1], 100),
            'has_diabetes_comprehensive': np.random.choice([0, 1], 100),
            'has_ckd': np.random.choice([0, 1], 100),
            'has_cvd': np.random.choice([0, 1], 100),
            'inpatient_claim_count': np.random.randint(0, 10, 100),
            'outpatient_claim_count': np.random.randint(0, 20, 100)
        })
        
        # Create synthetic target
        self.sample_target = np.random.choice([0, 1], 100, p=[0.7, 0.3])
    
    def test_prepare_training_data(self):
        """Test training data preparation."""
        X, y = self.trainer.prepare_training_data(self.sample_features, 'poor_glycemic_control')
        
        self.assertEqual(X.shape[0], 100)
        self.assertEqual(len(y), 100)
        self.assertIn('age_at_my_end', X.columns)
        self.assertNotIn('DESYNPUF_ID', X.columns)
    
    def test_split_data_temporal(self):
        """Test temporal data splitting."""
        X, y = self.trainer.prepare_training_data(self.sample_features)
        X_train, X_test, y_train, y_test = self.trainer.split_data_temporal(X, y)
        
        self.assertGreater(len(X_train), 0)
        self.assertGreater(len(X_test), 0)
        self.assertEqual(len(X_train) + len(X_test), len(X))
    
    def test_scale_features(self):
        """Test feature scaling."""
        X, y = self.trainer.prepare_training_data(self.sample_features)
        X_train, X_test, y_train, y_test = self.trainer.split_data_temporal(X, y)
        
        X_train_scaled, X_test_scaled = self.trainer.scale_features(X_train, X_test)
        
        self.assertEqual(X_train_scaled.shape, X_train.shape)
        self.assertEqual(X_test_scaled.shape, X_test.shape)
    
    def test_train_logistic_regression(self):
        """Test logistic regression training."""
        X, y = self.trainer.prepare_training_data(self.sample_features)
        X_train, X_test, y_train, y_test = self.trainer.split_data_temporal(X, y)
        X_train_scaled, X_test_scaled = self.trainer.scale_features(X_train, X_test)
        
        results = self.trainer.train_logistic_regression(X_train_scaled, y_train)
        
        self.assertIn('model', results)
        self.assertIn('cv_scores', results)
        self.assertIn('cv_mean', results)
        self.assertIsNotNone(results['model'])
    
    def test_train_random_forest(self):
        """Test random forest training."""
        X, y = self.trainer.prepare_training_data(self.sample_features)
        X_train, X_test, y_train, y_test = self.trainer.split_data_temporal(X, y)
        
        results = self.trainer.train_random_forest(X_train, y_train)
        
        self.assertIn('model', results)
        self.assertIn('cv_scores', results)
        self.assertIn('feature_importance', results)
        self.assertIsNotNone(results['model'])
    
    def test_train_all_models(self):
        """Test training all models."""
        results = self.trainer.train_all_models(self.sample_features)
        
        self.assertIn('logistic_regression', results)
        self.assertIn('random_forest', results)
        self.assertIsNotNone(self.trainer.models['logistic_regression'])
        self.assertIsNotNone(self.trainer.models['random_forest'])
    
    def test_get_feature_importance(self):
        """Test feature importance extraction."""
        # Train a model first
        self.trainer.train_all_models(self.sample_features)
        
        importance_df = self.trainer.get_feature_importance('random_forest')
        
        self.assertIn('feature', importance_df.columns)
        self.assertIn('importance', importance_df.columns)
        self.assertGreater(len(importance_df), 0)
    
    def test_save_models(self):
        """Test model saving."""
        # Train models first
        self.trainer.train_all_models(self.sample_features)
        
        with tempfile.TemporaryDirectory() as temp_dir:
            self.trainer.save_models(temp_dir)
            
            # Check files were created
            self.assertTrue(os.path.exists(os.path.join(temp_dir, "scaler.pkl")))
            self.assertTrue(os.path.exists(os.path.join(temp_dir, "logistic_regression_model.pkl")))
            self.assertTrue(os.path.exists(os.path.join(temp_dir, "random_forest_model.pkl")))
            self.assertTrue(os.path.exists(os.path.join(temp_dir, "training_results.pkl")))


class TestHEDISModelPredictor(unittest.TestCase):
    """Test cases for HEDIS model predictor."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        
        # Create and save a simple model for testing
        from sklearn.linear_model import LogisticRegression
        from sklearn.preprocessing import StandardScaler
        
        # Create sample data
        np.random.seed(42)
        X = np.random.randn(100, 5)
        y = np.random.choice([0, 1], 100)
        
        # Train model and scaler
        self.scaler = StandardScaler()
        X_scaled = self.scaler.fit_transform(X)
        
        self.model = LogisticRegression(random_state=42)
        self.model.fit(X_scaled, y)
        
        # Save model and scaler
        joblib.dump(self.model, os.path.join(self.temp_dir, "logistic_regression_model.pkl"))
        joblib.dump(self.scaler, os.path.join(self.temp_dir, "scaler.pkl"))
        
        # Save training results
        training_results = {
            'logistic_regression': {
                'model': self.model,
                'cv_mean': 0.85,
                'cv_std': 0.05,
                'training_time': datetime.now()
            }
        }
        joblib.dump(training_results, os.path.join(self.temp_dir, "training_results.pkl"))
    
    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_load_model(self):
        """Test model loading."""
        predictor = HEDISModelPredictor(self.temp_dir, "logistic_regression")
        
        self.assertIsNotNone(predictor.model)
        self.assertIsNotNone(predictor.scaler)
        self.assertEqual(predictor.model_name, "logistic_regression")
    
    def test_predict_proba(self):
        """Test probability prediction."""
        predictor = HEDISModelPredictor(self.temp_dir, "logistic_regression")
        
        # Create test data
        X_test = np.random.randn(10, 5)
        probabilities = predictor.predict_proba(X_test)
        
        self.assertEqual(probabilities.shape[0], 10)
        self.assertEqual(probabilities.shape[1], 2)
        self.assertTrue(np.all(probabilities >= 0))
        self.assertTrue(np.all(probabilities <= 1))
    
    def test_predict(self):
        """Test class prediction."""
        predictor = HEDISModelPredictor(self.temp_dir, "logistic_regression")
        
        # Create test data
        X_test = np.random.randn(10, 5)
        predictions = predictor.predict(X_test)
        
        self.assertEqual(len(predictions), 10)
        self.assertTrue(np.all(np.isin(predictions, [0, 1])))
    
    def test_predict_single(self):
        """Test single member prediction."""
        predictor = HEDISModelPredictor(self.temp_dir, "logistic_regression")
        
        member_features = {
            'age_at_my_end': 65,
            'is_female': 1,
            'is_white': 1,
            'has_diabetes_comprehensive': 1,
            'has_ckd': 0
        }
        
        result = predictor.predict_single(member_features)
        
        self.assertIn('prediction', result)
        self.assertIn('risk_score', result)
        self.assertIn('risk_level', result)
        self.assertIn('confidence', result)
        self.assertIn('model_name', result)
    
    def test_predict_batch(self):
        """Test batch prediction."""
        predictor = HEDISModelPredictor(self.temp_dir, "logistic_regression")
        
        # Create test DataFrame
        X_test = pd.DataFrame({
            'age_at_my_end': [65, 45, 55],
            'is_female': [1, 0, 1],
            'is_white': [1, 1, 0],
            'has_diabetes_comprehensive': [1, 0, 1],
            'has_ckd': [0, 0, 1]
        })
        
        results_df = predictor.predict_batch(X_test)
        
        self.assertEqual(len(results_df), 3)
        self.assertIn('prediction', results_df.columns)
        self.assertIn('risk_score', results_df.columns)
        self.assertIn('risk_level', results_df.columns)
    
    def test_get_model_info(self):
        """Test model information retrieval."""
        predictor = HEDISModelPredictor(self.temp_dir, "logistic_regression")
        
        model_info = predictor.get_model_info()
        
        self.assertIn('model_name', model_info)
        self.assertIn('model_type', model_info)
        self.assertIn('has_scaler', model_info)
        self.assertEqual(model_info['model_name'], "logistic_regression")


class TestHEDISModelEvaluator(unittest.TestCase):
    """Test cases for HEDIS model evaluator."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.evaluator = HEDISModelEvaluator()
        
        # Create sample data
        np.random.seed(42)
        self.y_true = np.random.choice([0, 1], 100, p=[0.7, 0.3])
        self.y_pred = np.random.choice([0, 1], 100, p=[0.7, 0.3])
        self.y_proba = np.random.rand(100)
        
        # Create sample features for bias analysis
        self.X = pd.DataFrame({
            'age_at_my_end': np.random.randint(18, 76, 100),
            'is_female': np.random.choice([0, 1], 100),
            'is_white': np.random.choice([0, 1], 100),
            'is_black': np.random.choice([0, 1], 100)
        })
    
    def test_calculate_basic_metrics(self):
        """Test basic metrics calculation."""
        metrics = self.evaluator._calculate_basic_metrics(self.y_true, self.y_pred, self.y_proba)
        
        self.assertIn('accuracy', metrics)
        self.assertIn('precision', metrics)
        self.assertIn('recall', metrics)
        self.assertIn('f1', metrics)
        self.assertIn('specificity', metrics)
        self.assertIn('npv', metrics)
        self.assertIn('auc_roc', metrics)
    
    def test_calculate_clinical_metrics(self):
        """Test clinical metrics calculation."""
        metrics = self.evaluator._calculate_clinical_metrics(self.y_true, self.y_pred, self.y_proba)
        
        self.assertIn('sensitivity', metrics)
        self.assertIn('specificity', metrics)
        self.assertIn('positive_predictive_value', metrics)
        self.assertIn('negative_predictive_value', metrics)
        self.assertIn('false_positive_rate', metrics)
        self.assertIn('false_negative_rate', metrics)
    
    def test_calculate_confusion_matrix(self):
        """Test confusion matrix calculation."""
        cm_results = self.evaluator._calculate_confusion_matrix(self.y_true, self.y_pred)
        
        self.assertIn('matrix', cm_results)
        self.assertIn('true_negatives', cm_results)
        self.assertIn('false_positives', cm_results)
        self.assertIn('false_negatives', cm_results)
        self.assertIn('true_positives', cm_results)
    
    def test_calculate_roc_metrics(self):
        """Test ROC metrics calculation."""
        roc_results = self.evaluator._calculate_roc_metrics(self.y_true, self.y_proba)
        
        self.assertIn('fpr', roc_results)
        self.assertIn('tpr', roc_results)
        self.assertIn('thresholds', roc_results)
        self.assertIn('auc', roc_results)
        self.assertIn('optimal_threshold', roc_results)
    
    def test_analyze_demographic_bias(self):
        """Test demographic bias analysis."""
        bias_results = self.evaluator._analyze_demographic_bias(self.y_true, self.y_pred, self.y_proba, self.X)
        
        self.assertIn('age_bias', bias_results)
        self.assertIn('sex_bias', bias_results)
        self.assertIn('race_bias', bias_results)
    
    def test_evaluate_model(self):
        """Test comprehensive model evaluation."""
        results = self.evaluator.evaluate_model(self.y_true, self.y_pred, self.y_proba, self.X)
        
        self.assertIn('basic_metrics', results)
        self.assertIn('clinical_metrics', results)
        self.assertIn('confusion_matrix', results)
        self.assertIn('roc_analysis', results)
        self.assertIn('bias_analysis', results)
    
    def test_generate_evaluation_report(self):
        """Test evaluation report generation."""
        # Run evaluation first
        self.evaluator.evaluate_model(self.y_true, self.y_pred, self.y_proba, self.X)
        
        report = self.evaluator.generate_evaluation_report()
        
        self.assertIsInstance(report, str)
        self.assertIn("HEDIS GSD Model Evaluation Report", report)
        self.assertIn("Basic Performance Metrics", report)
        self.assertIn("Clinical Performance Metrics", report)


class TestHEDISModelSerializer(unittest.TestCase):
    """Test cases for HEDIS model serializer."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.serializer = HEDISModelSerializer(self.temp_dir)
        
        # Create sample model and scaler
        from sklearn.linear_model import LogisticRegression
        from sklearn.preprocessing import StandardScaler
        
        self.model = LogisticRegression(random_state=42)
        self.scaler = StandardScaler()
        
        # Create sample data for fitting
        np.random.seed(42)
        X = np.random.randn(100, 5)
        y = np.random.choice([0, 1], 100)
        
        self.scaler.fit(X)
        self.model.fit(self.scaler.transform(X), y)
    
    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_save_model(self):
        """Test model saving."""
        metadata = {
            'description': 'Test model',
            'performance': {'auc': 0.85}
        }
        
        model_dir = self.serializer.save_model(
            self.model, 
            'test_model', 
            self.scaler, 
            metadata
        )
        
        self.assertTrue(os.path.exists(model_dir))
        self.assertTrue(os.path.exists(os.path.join(model_dir, 'test_model_model.pkl')))
        self.assertTrue(os.path.exists(os.path.join(model_dir, 'scaler.pkl')))
        self.assertTrue(os.path.exists(os.path.join(model_dir, 'metadata.json')))
        self.assertTrue(os.path.exists(os.path.join(model_dir, 'checksums.json')))
    
    def test_load_model(self):
        """Test model loading."""
        # Save model first
        model_dir = self.serializer.save_model(self.model, 'test_model', self.scaler)
        
        # Load model
        loaded_data = self.serializer.load_model('test_model')
        
        self.assertIn('model', loaded_data)
        self.assertIn('scaler', loaded_data)
        self.assertIn('metadata', loaded_data)
        self.assertIsNotNone(loaded_data['model'])
        self.assertIsNotNone(loaded_data['scaler'])
    
    def test_list_models(self):
        """Test model listing."""
        # Save a model first
        self.serializer.save_model(self.model, 'test_model', self.scaler)
        
        models = self.serializer.list_models()
        
        self.assertIn('test_model', models)
        self.assertGreater(len(models['test_model']), 0)
    
    def test_get_latest_model(self):
        """Test getting latest model."""
        # Save a model first
        self.serializer.save_model(self.model, 'test_model', self.scaler)
        
        latest_data = self.serializer.get_latest_model('test_model')
        
        self.assertIn('model', latest_data)
        self.assertIn('scaler', latest_data)
        self.assertIsNotNone(latest_data['model'])
    
    def test_delete_model(self):
        """Test model deletion."""
        # Save a model first
        model_dir = self.serializer.save_model(self.model, 'test_model', self.scaler)
        
        # Delete model
        success = self.serializer.delete_model('test_model', 'latest')
        
        self.assertTrue(success)
        self.assertFalse(os.path.exists(model_dir))


if __name__ == '__main__':
    # Run all tests
    unittest.main(verbosity=2)
