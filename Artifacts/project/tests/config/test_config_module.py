"""
Unit Tests for HEDIS GSD Configuration Module

Tests configuration loading, validation, and management functions
with healthcare compliance validation.
"""

import unittest
import tempfile
import os
import yaml
from pathlib import Path

# Import modules to test
from src.config import HEDISConfigManager, load_config


class TestHEDISConfigManager(unittest.TestCase):
    """Test cases for HEDIS configuration manager."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        
        # Create sample config file
        self.config_content = {
            'data': {
                'raw_data_path': 'data/raw',
                'measurement_year': 2008
            },
            'model': {
                'target_variable': 'poor_glycemic_control',
                'age_range': {'min': 18, 'max': 75}
            },
            'training': {
                'test_size': 0.2,
                'random_state': 42
            },
            'security': {
                'phi_logging': False,
                'audit_logging': True
            }
        }
        
        self.config_path = os.path.join(self.temp_dir, 'test_config.yaml')
        with open(self.config_path, 'w') as f:
            yaml.dump(self.config_content, f)
    
    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_config_loading(self):
        """Test configuration loading."""
        config_manager = HEDISConfigManager(self.config_path, 'dev')
        
        self.assertIsNotNone(config_manager.config)
        self.assertIn('data', config_manager.config)
        self.assertIn('model', config_manager.config)
    
    def test_get_config_value(self):
        """Test getting configuration values."""
        config_manager = HEDISConfigManager(self.config_path, 'dev')
        
        # Test simple key
        measurement_year = config_manager.get('data.measurement_year')
        self.assertEqual(measurement_year, 2008)
        
        # Test nested key
        age_min = config_manager.get('model.age_range.min')
        self.assertEqual(age_min, 18)
        
        # Test default value
        missing_value = config_manager.get('missing.key', 'default')
        self.assertEqual(missing_value, 'default')
    
    def test_set_config_value(self):
        """Test setting configuration values."""
        config_manager = HEDISConfigManager(self.config_path, 'dev')
        
        # Set a new value
        config_manager.set('new.key', 'new_value')
        self.assertEqual(config_manager.get('new.key'), 'new_value')
        
        # Update existing value
        config_manager.set('data.measurement_year', 2009)
        self.assertEqual(config_manager.get('data.measurement_year'), 2009)
    
    def test_get_section(self):
        """Test getting configuration sections."""
        config_manager = HEDISConfigManager(self.config_path, 'dev')
        
        data_section = config_manager.get_section('data')
        self.assertIn('raw_data_path', data_section)
        self.assertIn('measurement_year', data_section)
        
        model_section = config_manager.get_section('model')
        self.assertIn('target_variable', model_section)
        self.assertIn('age_range', model_section)
    
    def test_update_section(self):
        """Test updating configuration sections."""
        config_manager = HEDISConfigManager(self.config_path, 'dev')
        
        updates = {
            'new_param': 'new_value',
            'measurement_year': 2010
        }
        
        config_manager.update_section('data', updates)
        
        self.assertEqual(config_manager.get('data.new_param'), 'new_value')
        self.assertEqual(config_manager.get('data.measurement_year'), 2010)
    
    def test_save_config(self):
        """Test saving configuration."""
        config_manager = HEDISConfigManager(self.config_path, 'dev')
        
        # Modify config
        config_manager.set('data.measurement_year', 2011)
        
        # Save to new file
        output_path = os.path.join(self.temp_dir, 'saved_config.yaml')
        config_manager.save_config(output_path)
        
        # Verify file was created
        self.assertTrue(os.path.exists(output_path))
        
        # Verify content
        with open(output_path, 'r') as f:
            saved_config = yaml.safe_load(f)
        
        self.assertEqual(saved_config['data']['measurement_year'], 2011)
    
    def test_export_json(self):
        """Test exporting configuration as JSON."""
        config_manager = HEDISConfigManager(self.config_path, 'dev')
        
        # Export to JSON
        output_path = os.path.join(self.temp_dir, 'config.json')
        config_manager.export_json(output_path)
        
        # Verify file was created
        self.assertTrue(os.path.exists(output_path))
    
    def test_get_model_config(self):
        """Test getting model configuration."""
        config_manager = HEDISConfigManager(self.config_path, 'dev')
        
        model_config = config_manager.get_model_config()
        
        self.assertIn('target_variable', model_config)
        self.assertIn('age_range', model_config)
        self.assertEqual(model_config['target_variable'], 'poor_glycemic_control')
    
    def test_get_training_config(self):
        """Test getting training configuration."""
        config_manager = HEDISConfigManager(self.config_path, 'dev')
        
        training_config = config_manager.get_training_config()
        
        self.assertIn('test_size', training_config)
        self.assertIn('random_state', training_config)
        self.assertEqual(training_config['test_size'], 0.2)
    
    def test_get_data_config(self):
        """Test getting data configuration."""
        config_manager = HEDISConfigManager(self.config_path, 'dev')
        
        data_config = config_manager.get_data_config()
        
        self.assertIn('raw_data_path', data_config)
        self.assertIn('measurement_year', data_config)
        self.assertEqual(data_config['measurement_year'], 2008)
    
    def test_get_security_config(self):
        """Test getting security configuration."""
        config_manager = HEDISConfigManager(self.config_path, 'dev')
        
        security_config = config_manager.get_security_config()
        
        self.assertIn('phi_logging', security_config)
        self.assertIn('audit_logging', security_config)
        self.assertFalse(security_config['phi_logging'])
        self.assertTrue(security_config['audit_logging'])
    
    def test_is_phi_logging_enabled(self):
        """Test PHI logging check."""
        config_manager = HEDISConfigManager(self.config_path, 'dev')
        
        phi_logging = config_manager.is_phi_logging_enabled()
        self.assertFalse(phi_logging)
    
    def test_is_audit_logging_enabled(self):
        """Test audit logging check."""
        config_manager = HEDISConfigManager(self.config_path, 'dev')
        
        audit_logging = config_manager.is_audit_logging_enabled()
        self.assertTrue(audit_logging)
    
    def test_get_measurement_year(self):
        """Test getting measurement year."""
        config_manager = HEDISConfigManager(self.config_path, 'dev')
        
        measurement_year = config_manager.get_measurement_year()
        self.assertEqual(measurement_year, 2008)
    
    def test_get_target_variable(self):
        """Test getting target variable."""
        config_manager = HEDISConfigManager(self.config_path, 'dev')
        
        target_variable = config_manager.get_target_variable()
        self.assertEqual(target_variable, 'poor_glycemic_control')
    
    def test_get_age_range(self):
        """Test getting age range."""
        config_manager = HEDISConfigManager(self.config_path, 'dev')
        
        age_range = config_manager.get_age_range()
        self.assertEqual(age_range['min'], 18)
        self.assertEqual(age_range['max'], 75)
    
    def test_environment_config_override(self):
        """Test environment-specific configuration override."""
        # Create environment-specific config
        env_config_content = {
            'data': {
                'measurement_year': 2009  # Override
            },
            'training': {
                'test_size': 0.3  # Override
            },
            'development': {
                'debug_mode': True  # New section
            }
        }
        
        env_config_path = os.path.join(self.temp_dir, 'config_dev.yaml')
        with open(env_config_path, 'w') as f:
            yaml.dump(env_config_content, f)
        
        # Load config with environment override
        config_manager = HEDISConfigManager(self.config_path, 'dev')
        
        # Check overrides
        self.assertEqual(config_manager.get('data.measurement_year'), 2009)
        self.assertEqual(config_manager.get('training.test_size'), 0.3)
        self.assertTrue(config_manager.get('development.debug_mode'))
        
        # Check original values are preserved
        self.assertEqual(config_manager.get('model.target_variable'), 'poor_glycemic_control')
    
    def test_config_validation(self):
        """Test configuration validation."""
        # Create config with missing required sections
        incomplete_config = {
            'data': {
                'raw_data_path': 'data/raw'
                # Missing measurement_year
            }
            # Missing other required sections
        }
        
        incomplete_config_path = os.path.join(self.temp_dir, 'incomplete_config.yaml')
        with open(incomplete_config_path, 'w') as f:
            yaml.dump(incomplete_config, f)
        
        # Should not raise exception but log warnings
        config_manager = HEDISConfigManager(incomplete_config_path, 'dev')
        self.assertIsNotNone(config_manager.config)


class TestConfigConvenienceFunctions(unittest.TestCase):
    """Test cases for configuration convenience functions."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        
        # Create sample config file
        self.config_content = {
            'data': {
                'raw_data_path': 'data/raw',
                'measurement_year': 2008
            },
            'model': {
                'target_variable': 'poor_glycemic_control'
            }
        }
        
        self.config_path = os.path.join(self.temp_dir, 'test_config.yaml')
        with open(self.config_path, 'w') as f:
            yaml.dump(self.config_content, f)
    
    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_load_config_convenience_function(self):
        """Test load_config convenience function."""
        config_manager = load_config(self.config_path, 'dev')
        
        self.assertIsInstance(config_manager, HEDISConfigManager)
        self.assertEqual(config_manager.get('data.measurement_year'), 2008)
        self.assertEqual(config_manager.get('model.target_variable'), 'poor_glycemic_control')


if __name__ == '__main__':
    # Run all tests
    unittest.main(verbosity=2)
