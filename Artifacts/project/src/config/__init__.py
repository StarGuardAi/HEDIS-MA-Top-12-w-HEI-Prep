"""
Configuration Management for HEDIS GSD Prediction Engine

Handles loading and validation of configuration files with healthcare-specific
settings and environment-specific overrides.

HEDIS Specification: MY2023 Volume 2
Measure: HBD - Hemoglobin A1c Control for Patients with Diabetes
"""

import yaml
import os
import logging
from typing import Dict, Any, Optional, Union
from pathlib import Path
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HEDISConfigManager:
    """
    Manages configuration for HEDIS GSD prediction engine.
    
    Key features:
    - Environment-specific configurations
    - Configuration validation
    - Healthcare compliance settings
    - Runtime configuration updates
    """
    
    def __init__(self, config_path: str = "config.yaml", env: str = "dev"):
        """
        Initialize the configuration manager.
        
        Args:
            config_path: Path to main configuration file
            env: Environment (dev, staging, prod)
        """
        self.config_path = config_path
        self.env = env
        self.config = {}
        self.env_config = {}
        
        # Load configurations
        self._load_config()
        self._load_env_config()
        self._merge_configs()
        self._validate_config()
        
        logger.info(f"Configuration manager initialized for environment: {env}")
    
    def _load_config(self) -> None:
        """Load main configuration file."""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r') as f:
                    self.config = yaml.safe_load(f) or {}
                logger.info(f"Main configuration loaded from {self.config_path}")
            else:
                logger.warning(f"Configuration file not found: {self.config_path}")
                self.config = self._get_default_config()
        except Exception as e:
            logger.error(f"Error loading configuration: {e}")
            self.config = self._get_default_config()
    
    def _load_env_config(self) -> None:
        """Load environment-specific configuration."""
        env_config_path = f"config_{self.env}.yaml"
        
        try:
            if os.path.exists(env_config_path):
                with open(env_config_path, 'r') as f:
                    self.env_config = yaml.safe_load(f) or {}
                logger.info(f"Environment configuration loaded from {env_config_path}")
            else:
                logger.info(f"No environment-specific configuration found: {env_config_path}")
                self.env_config = {}
        except Exception as e:
            logger.error(f"Error loading environment configuration: {e}")
            self.env_config = {}
    
    def _merge_configs(self) -> None:
        """Merge main and environment configurations."""
        # Start with main config
        merged_config = self.config.copy()
        
        # Override with environment-specific settings
        self._deep_update(merged_config, self.env_config)
        
        self.config = merged_config
        logger.info("Configurations merged successfully")
    
    def _deep_update(self, base_dict: Dict[str, Any], update_dict: Dict[str, Any]) -> None:
        """Recursively update dictionary."""
        for key, value in update_dict.items():
            if key in base_dict and isinstance(base_dict[key], dict) and isinstance(value, dict):
                self._deep_update(base_dict[key], value)
            else:
                base_dict[key] = value
    
    def _validate_config(self) -> None:
        """Validate configuration settings."""
        required_sections = ['data', 'model', 'training', 'features', 'security']
        
        for section in required_sections:
            if section not in self.config:
                logger.warning(f"Missing required configuration section: {section}")
        
        # Validate data configuration
        if 'data' in self.config:
            data_config = self.config['data']
            if 'measurement_year' not in data_config:
                logger.warning("Missing measurement_year in data configuration")
            if 'raw_data_path' not in data_config:
                logger.warning("Missing raw_data_path in data configuration")
        
        # Validate model configuration
        if 'model' in self.config:
            model_config = self.config['model']
            if 'target_variable' not in model_config:
                logger.warning("Missing target_variable in model configuration")
            if 'age_range' not in model_config:
                logger.warning("Missing age_range in model configuration")
        
        # Validate security configuration
        if 'security' in self.config:
            security_config = self.config['security']
            if not security_config.get('phi_logging', True):
                logger.info("PHI logging disabled - this is correct for production")
            if not security_config.get('audit_logging', False):
                logger.warning("Audit logging disabled - consider enabling for compliance")
        
        logger.info("Configuration validation completed")
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration."""
        return {
            'data': {
                'raw_data_path': 'data/raw',
                'processed_data_path': 'data/processed',
                'measurement_year': 2008
            },
            'model': {
                'target_variable': 'poor_glycemic_control',
                'age_range': {'min': 18, 'max': 75}
            },
            'training': {
                'test_size': 0.2,
                'random_state': 42,
                'cv_folds': 5
            },
            'features': {
                'demographic_features': True,
                'comorbidity_features': True,
                'utilization_features': True,
                'diabetes_specific_features': True
            },
            'security': {
                'phi_logging': False,
                'audit_logging': True,
                'hash_identifiers': True
            },
            'logging': {
                'level': 'INFO',
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            }
        }
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value using dot notation.
        
        Args:
            key: Configuration key (e.g., 'data.measurement_year')
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        keys = key.split('.')
        value = self.config
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
    
    def set(self, key: str, value: Any) -> None:
        """
        Set configuration value using dot notation.
        
        Args:
            key: Configuration key (e.g., 'data.measurement_year')
            value: Value to set
        """
        keys = key.split('.')
        config = self.config
        
        # Navigate to the parent of the target key
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        # Set the value
        config[keys[-1]] = value
        logger.info(f"Configuration updated: {key} = {value}")
    
    def get_section(self, section: str) -> Dict[str, Any]:
        """
        Get entire configuration section.
        
        Args:
            section: Section name
            
        Returns:
            Section configuration
        """
        return self.config.get(section, {})
    
    def update_section(self, section: str, updates: Dict[str, Any]) -> None:
        """
        Update entire configuration section.
        
        Args:
            section: Section name
            updates: Updates to apply
        """
        if section not in self.config:
            self.config[section] = {}
        
        self.config[section].update(updates)
        logger.info(f"Configuration section updated: {section}")
    
    def save_config(self, output_path: str = None) -> None:
        """
        Save current configuration to file.
        
        Args:
            output_path: Output file path (optional)
        """
        if output_path is None:
            output_path = f"config_{self.env}_generated.yaml"
        
        try:
            with open(output_path, 'w') as f:
                yaml.dump(self.config, f, default_flow_style=False, indent=2)
            logger.info(f"Configuration saved to {output_path}")
        except Exception as e:
            logger.error(f"Error saving configuration: {e}")
    
    def export_json(self, output_path: str = None) -> None:
        """
        Export configuration as JSON.
        
        Args:
            output_path: Output file path (optional)
        """
        if output_path is None:
            output_path = f"config_{self.env}.json"
        
        try:
            with open(output_path, 'w') as f:
                json.dump(self.config, f, indent=2, default=str)
            logger.info(f"Configuration exported to {output_path}")
        except Exception as e:
            logger.error(f"Error exporting configuration: {e}")
    
    def get_model_config(self) -> Dict[str, Any]:
        """Get model-specific configuration."""
        return self.get_section('model')
    
    def get_training_config(self) -> Dict[str, Any]:
        """Get training-specific configuration."""
        return self.get_section('training')
    
    def get_data_config(self) -> Dict[str, Any]:
        """Get data-specific configuration."""
        return self.get_section('data')
    
    def get_security_config(self) -> Dict[str, Any]:
        """Get security-specific configuration."""
        return self.get_section('security')
    
    def get_feature_config(self) -> Dict[str, Any]:
        """Get feature engineering configuration."""
        return self.get_section('features')
    
    def get_evaluation_config(self) -> Dict[str, Any]:
        """Get evaluation configuration."""
        return self.get_section('evaluation')
    
    def get_prediction_config(self) -> Dict[str, Any]:
        """Get prediction configuration."""
        return self.get_section('prediction')
    
    def is_phi_logging_enabled(self) -> bool:
        """Check if PHI logging is enabled."""
        return self.get('security.phi_logging', False)
    
    def is_audit_logging_enabled(self) -> bool:
        """Check if audit logging is enabled."""
        return self.get('security.audit_logging', True)
    
    def get_measurement_year(self) -> int:
        """Get HEDIS measurement year."""
        return self.get('data.measurement_year', 2008)
    
    def get_target_variable(self) -> str:
        """Get target variable name."""
        return self.get('model.target_variable', 'poor_glycemic_control')
    
    def get_age_range(self) -> Dict[str, int]:
        """Get age range for HEDIS measure."""
        return self.get('model.age_range', {'min': 18, 'max': 75})


def load_config(config_path: str = "config.yaml", env: str = "dev") -> HEDISConfigManager:
    """
    Convenience function to load configuration.
    
    Args:
        config_path: Path to configuration file
        env: Environment name
        
    Returns:
        HEDISConfigManager instance
    """
    return HEDISConfigManager(config_path, env)


if __name__ == "__main__":
    # Example usage
    try:
        # Load configuration
        config_manager = load_config()
        
        # Get specific values
        measurement_year = config_manager.get_measurement_year()
        target_variable = config_manager.get_target_variable()
        age_range = config_manager.get_age_range()
        
        print(f"Configuration loaded successfully:")
        print(f"  Measurement Year: {measurement_year}")
        print(f"  Target Variable: {target_variable}")
        print(f"  Age Range: {age_range}")
        
        # Get model configuration
        model_config = config_manager.get_model_config()
        print(f"  Model Config: {model_config}")
        
        # Check security settings
        phi_logging = config_manager.is_phi_logging_enabled()
        audit_logging = config_manager.is_audit_logging_enabled()
        print(f"  PHI Logging: {phi_logging}")
        print(f"  Audit Logging: {audit_logging}")
        
    except Exception as e:
        print(f"Error loading configuration: {e}")
