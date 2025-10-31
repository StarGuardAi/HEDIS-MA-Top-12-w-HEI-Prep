"""
KED End-to-End Integration Test

Tests complete KED pipeline from data loading through prediction.

Pipeline:
1. Load member demographics, claims, labs
2. Calculate KED measure (denominator, numerator, gaps)
3. Create diabetes features
4. Train KED prediction model
5. Make predictions
6. Validate results

HEDIS Specification: MY2025
Measure: KED - Kidney Health Evaluation
"""

import unittest
import pandas as pd
import numpy as np
from datetime import datetime
import sys
from pathlib import Path
import tempfile
import shutil

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Import all components
from src.measures.ked import KEDMeasure, calculate_ked_measure
from src.data.features.diabetes_features import (
    DiabetesFeatureEngineer,
    create_diabetes_features
)
from src.models.ked_trainer import KEDModelTrainer, train_ked_model
from src.models.ked_predictor import KEDPredictor, load_ked_predictor
from tests.fixtures.synthetic_ked_data import get_synthetic_ked_test_data


class TestKEDEndToEnd(unittest.TestCase):
    """Test complete KED pipeline end-to-end."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test fixtures once for all tests."""
        cls.measurement_year = 2025
        
        # Create temporary directory for model artifacts
        cls.temp_dir = tempfile.mkdtemp()
        
        # Load synthetic test data
        cls.member_df, cls.claims_df, cls.labs_df = get_synthetic_ked_test_data(
            cls.measurement_year
        )
        
        print(f"\n{'='*80}")
        print("KED END-TO-END INTEGRATION TEST")
        print(f"{'='*80}")
        print(f"Test data loaded:")
        print(f"  Members: {len(cls.member_df)}")
        print(f"  Claims: {len(cls.claims_df)}")
        print(f"  Labs: {len(cls.labs_df)}")
    
    @classmethod
    def tearDownClass(cls):
        """Clean up temporary directory."""
        shutil.rmtree(cls.temp_dir)
    
    def test_01_ked_measure_calculation(self):
        """Test Step 1: Calculate KED measure."""
        print(f"\n{'='*80}")
        print("STEP 1: KED Measure Calculation")
        print(f"{'='*80}")
        
        # Calculate KED measure
        results = calculate_ked_measure(
            self.member_df.copy(),
            self.claims_df.copy(),
            self.labs_df.copy(),
            measurement_year=self.measurement_year
        )
        
        # Validate results
        self.assertIsInstance(results, dict)
        self.assertEqual(results['measure_code'], 'KED')
        self.assertEqual(results['measurement_year'], 2025)
        self.assertEqual(results['weight'], 3.0)
        self.assertTrue(results['new_2025'])
        
        # Check denominator and numerator
        self.assertGreater(results['denominator'], 0)
        self.assertGreaterEqual(results['denominator'], results['numerator'])
        
        # Check gap analysis
        self.assertIn('gaps', results)
        self.assertIn('total_gaps', results['gaps'])
        
        print(f"✓ KED measure calculated successfully")
        print(f"  Denominator: {results['denominator']}")
        print(f"  Numerator: {results['numerator']}")
        print(f"  Rate: {results['rate']:.1f}%")
        print(f"  Gaps: {results['gaps']['total_gaps']}")
        
        # Store for next tests
        self.__class__.ked_results = results
    
    def test_02_diabetes_feature_engineering(self):
        """Test Step 2: Create diabetes features."""
        print(f"\n{'='*80}")
        print("STEP 2: Diabetes Feature Engineering")
        print(f"{'='*80}")
        
        # Create features
        features_df = create_diabetes_features(
            self.member_df.copy(),
            self.claims_df.copy(),
            self.labs_df.copy(),
            measurement_year=self.measurement_year
        )
        
        # Validate features
        self.assertIsInstance(features_df, pd.DataFrame)
        self.assertEqual(len(features_df), len(self.member_df))
        
        # Check key features exist
        key_features = [
            'age_at_my_end',
            'diabetes_type1', 'diabetes_type2',
            'has_ckd', 'has_cvd',
            'had_hba1c_prior_year', 'had_egfr_prior_year',
            'ed_visits', 'inpatient_admits'
        ]
        for feature in key_features:
            self.assertIn(feature, features_df.columns)
        
        # Check for nulls in key features
        self.assertFalse(features_df['age_at_my_end'].isnull().any())
        
        feature_count = len([col for col in features_df.columns if col != 'member_id'])
        print(f"✓ Features created successfully")
        print(f"  Total features: {feature_count}")
        print(f"  Total members: {len(features_df)}")
        
        # Store for next tests
        self.__class__.features_df = features_df
    
    def test_03_model_training(self):
        """Test Step 3: Train KED prediction model."""
        print(f"\n{'='*80}")
        print("STEP 3: KED Model Training")
        print(f"{'='*80}")
        
        # Get member results from KED calculation
        member_results = self.ked_results['member_results']
        
        # Train model
        trainer = KEDModelTrainer(
            measurement_year=self.measurement_year,
            model_type='logistic'  # Use logistic for fast testing
        )
        
        # Create target variable
        y = trainer.create_target_variable(member_results)
        
        # Prepare features
        X, y = trainer.prepare_features(self.features_df.copy(), y)
        
        # Train/test split
        X_train, X_test, y_train, y_test = trainer.temporal_train_test_split(X, y, test_size=0.3)
        
        # Train model
        trainer.train_model(X_train, y_train)
        
        # Evaluate
        eval_results = trainer.evaluate_model(X_test, y_test)
        
        # Validate results
        self.assertIsNotNone(trainer.model)
        self.assertIn('auc_roc', eval_results)
        self.assertIn('accuracy', eval_results)
        self.assertIn('precision', eval_results)
        self.assertIn('recall', eval_results)
        
        # Model should have reasonable performance (small test set)
        self.assertGreater(eval_results['auc_roc'], 0.5)
        
        print(f"✓ Model trained successfully")
        print(f"  AUC-ROC: {eval_results['auc_roc']:.4f}")
        print(f"  Accuracy: {eval_results['accuracy']:.4f}")
        print(f"  Precision: {eval_results['precision']:.4f}")
        print(f"  Recall: {eval_results['recall']:.4f}")
        
        # Save model
        saved_files = trainer.save_model(self.temp_dir, model_name='ked_test_model')
        
        self.assertIn('model', saved_files)
        self.assertIn('scaler', saved_files)
        self.assertIn('features', saved_files)
        self.assertIn('metadata', saved_files)
        
        print(f"✓ Model saved to {self.temp_dir}")
        
        # Store for next tests
        self.__class__.trainer = trainer
        self.__class__.eval_results = eval_results
        self.__class__.X_test = X_test
        self.__class__.y_test = y_test
    
    def test_04_model_prediction_single(self):
        """Test Step 4a: Single member prediction."""
        print(f"\n{'='*80}")
        print("STEP 4a: Single Member Prediction")
        print(f"{'='*80}")
        
        # Load predictor
        predictor = load_ked_predictor(self.temp_dir, model_name='ked_test_model')
        
        # Get a single member
        member_features = self.features_df.iloc[0]
        member_id = self.member_df.iloc[0]['member_id']
        
        # Make prediction
        prediction = predictor.predict_single(member_features, member_id=member_id)
        
        # Validate prediction
        self.assertIsInstance(prediction, dict)
        self.assertIn('prediction', prediction)
        self.assertIn('risk_score', prediction)
        self.assertIn('risk_tier', prediction)
        self.assertIn('recommendations', prediction)
        
        # Risk score should be between 0 and 1
        self.assertGreaterEqual(prediction['risk_score'], 0.0)
        self.assertLessEqual(prediction['risk_score'], 1.0)
        
        # Risk tier should be valid
        self.assertIn(prediction['risk_tier'], ['high', 'medium', 'low'])
        
        print(f"✓ Single prediction successful")
        print(f"  Member: {member_id}")
        print(f"  Risk Score: {prediction['risk_score']:.3f}")
        print(f"  Risk Tier: {prediction['risk_tier']}")
        print(f"  Recommendations: {len(prediction['recommendations']['actions'])} actions")
    
    def test_05_model_prediction_batch(self):
        """Test Step 4b: Batch prediction."""
        print(f"\n{'='*80}")
        print("STEP 4b: Batch Prediction")
        print(f"{'='*80}")
        
        # Load predictor
        predictor = load_ked_predictor(self.temp_dir, model_name='ked_test_model')
        
        # Make batch predictions
        predictions = predictor.predict_batch(
            self.features_df.copy(),
            member_ids=self.member_df['member_id']
        )
        
        # Validate predictions
        self.assertIsInstance(predictions, pd.DataFrame)
        self.assertEqual(len(predictions), len(self.features_df))
        
        required_cols = ['member_id', 'prediction', 'risk_score', 'risk_tier', 'confidence']
        for col in required_cols:
            self.assertIn(col, predictions.columns)
        
        # All risk scores should be valid
        self.assertTrue((predictions['risk_score'] >= 0).all())
        self.assertTrue((predictions['risk_score'] <= 1).all())
        
        # Count risk tiers
        risk_tier_counts = predictions['risk_tier'].value_counts()
        
        print(f"✓ Batch predictions successful")
        print(f"  Total predictions: {len(predictions)}")
        print(f"  High risk: {risk_tier_counts.get('high', 0)}")
        print(f"  Medium risk: {risk_tier_counts.get('medium', 0)}")
        print(f"  Low risk: {risk_tier_counts.get('low', 0)}")
        
        # Store for next test
        self.__class__.batch_predictions = predictions
    
    def test_06_top_risk_identification(self):
        """Test Step 5: Identify top risk members."""
        print(f"\n{'='*80}")
        print("STEP 5: Top Risk Member Identification")
        print(f"{'='*80}")
        
        # Load predictor
        predictor = load_ked_predictor(self.temp_dir, model_name='ked_test_model')
        
        # Get top 3 risk members (small test set)
        top_n = min(3, len(self.features_df))
        top_risk = predictor.get_top_risk_members(
            self.features_df.copy(),
            self.member_df['member_id'],
            top_n=top_n
        )
        
        # Validate
        self.assertEqual(len(top_risk), top_n)
        
        # Should be sorted by risk score descending
        risk_scores = top_risk['risk_score'].tolist()
        self.assertEqual(risk_scores, sorted(risk_scores, reverse=True))
        
        print(f"✓ Top risk members identified")
        print(f"  Top {top_n} members:")
        for idx, row in top_risk.iterrows():
            print(f"    {row['member_id']}: {row['risk_score']:.3f} ({row['risk_tier']})")
    
    def test_07_model_info(self):
        """Test Step 6: Get model information."""
        print(f"\n{'='*80}")
        print("STEP 6: Model Information")
        print(f"{'='*80}")
        
        # Load predictor
        predictor = load_ked_predictor(self.temp_dir, model_name='ked_test_model')
        
        # Get model info
        model_info = predictor.get_model_info()
        
        # Validate
        self.assertIsInstance(model_info, dict)
        self.assertIn('model_name', model_info)
        self.assertIn('model_type', model_info)
        self.assertIn('n_features', model_info)
        self.assertIn('measurement_year', model_info)
        
        print(f"✓ Model information retrieved")
        print(f"  Model: {model_info['model_name']}")
        print(f"  Type: {model_info['model_type']}")
        print(f"  Features: {model_info['n_features']}")
        print(f"  Measurement Year: {model_info['measurement_year']}")
        if 'auc_roc' in model_info and model_info['auc_roc']:
            print(f"  AUC-ROC: {model_info['auc_roc']:.4f}")
    
    def test_08_end_to_end_validation(self):
        """Test Step 7: Validate complete pipeline."""
        print(f"\n{'='*80}")
        print("STEP 7: End-to-End Pipeline Validation")
        print(f"{'='*80}")
        
        # All previous tests must have passed
        self.assertIsNotNone(self.ked_results)
        self.assertIsNotNone(self.features_df)
        self.assertIsNotNone(self.trainer)
        self.assertIsNotNone(self.batch_predictions)
        
        # Validate pipeline consistency
        # Number of predictions should match number of members
        self.assertEqual(len(self.batch_predictions), len(self.member_df))
        
        # All members in denominator should have predictions
        member_results = self.ked_results['member_results']
        denominator_members = member_results[member_results['in_denominator_final']]
        
        # Get predictions for denominator members
        denominator_predictions = self.batch_predictions[
            self.batch_predictions['member_id'].isin(denominator_members['member_id'])
        ]
        
        self.assertEqual(len(denominator_predictions), len(denominator_members))
        
        print(f"✓ End-to-end pipeline validated")
        print(f"  Pipeline steps: 7")
        print(f"  Tests passed: 8")
        print(f"  Members processed: {len(self.member_df)}")
        print(f"  Features created: {len(self.features_df.columns) - 1}")
        print(f"  Predictions made: {len(self.batch_predictions)}")
        print(f"  Model AUC: {self.eval_results['auc_roc']:.4f}")
        
        print(f"\n{'='*80}")
        print("KED END-TO-END INTEGRATION TEST: ✅ PASSED")
        print(f"{'='*80}\n")


if __name__ == '__main__':
    unittest.main(verbosity=2)

