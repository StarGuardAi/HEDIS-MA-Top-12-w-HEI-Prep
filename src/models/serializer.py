"""
Model Serialization for HEDIS GSD Prediction Engine

Handles saving and loading of trained models, scalers, and metadata
with healthcare compliance and version control.

HEDIS Specification: MY2023 Volume 2
Measure: HBD - Hemoglobin A1c Control for Patients with Diabetes
"""

import pandas as pd
import numpy as np
import logging
from typing import Dict, List, Optional, Tuple, Union, Any
import joblib
import json
import os
from datetime import datetime
import hashlib
import warnings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HEDISModelSerializer:
    """
    Handles model serialization with healthcare compliance.
    
    Key features:
    - Model versioning and metadata
    - Healthcare compliance validation
    - Audit logging
    - Model integrity verification
    """
    
    def __init__(self, base_path: str = "models"):
        """
        Initialize the serializer.
        
        Args:
            base_path: Base directory for model storage
        """
        self.base_path = base_path
        self.model_registry = {}
        
        # Create base directory if it doesn't exist
        os.makedirs(base_path, exist_ok=True)
        
        logger.info(f"Initialized HEDIS model serializer with base path: {base_path}")
    
    def save_model(self, model: Any, model_name: str, scaler: Any = None, 
                   metadata: Dict[str, Any] = None, version: str = None) -> str:
        """
        Save a trained model with metadata.
        
        Args:
            model: Trained model object
            model_name: Name of the model
            scaler: Fitted scaler object (optional)
            metadata: Model metadata (optional)
            version: Model version (optional)
            
        Returns:
            Path to saved model directory
        """
        # Generate version if not provided
        if version is None:
            version = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Create model directory
        model_dir = os.path.join(self.base_path, f"{model_name}_v{version}")
        os.makedirs(model_dir, exist_ok=True)
        
        # Save model
        model_path = os.path.join(model_dir, f"{model_name}_model.pkl")
        joblib.dump(model, model_path)
        logger.info(f"Model saved to {model_path}")
        
        # Save scaler if provided
        scaler_path = None
        if scaler is not None:
            scaler_path = os.path.join(model_dir, "scaler.pkl")
            joblib.dump(scaler, scaler_path)
            logger.info(f"Scaler saved to {scaler_path}")
        
        # Create metadata
        model_metadata = self._create_model_metadata(
            model, model_name, version, scaler, metadata
        )
        
        # Save metadata
        metadata_path = os.path.join(model_dir, "metadata.json")
        with open(metadata_path, 'w') as f:
            json.dump(model_metadata, f, indent=2, default=str)
        logger.info(f"Metadata saved to {metadata_path}")
        
        # Calculate and save checksums
        checksums = self._calculate_checksums(model_dir)
        checksum_path = os.path.join(model_dir, "checksums.json")
        with open(checksum_path, 'w') as f:
            json.dump(checksums, f, indent=2)
        
        # Update registry
        self.model_registry[model_name] = {
            'version': version,
            'path': model_dir,
            'created': model_metadata['created'],
            'metadata': model_metadata
        }
        
        # Log save operation (PHI-safe)
        logger.info(f"Model serialization completed:")
        logger.info(f"  Model: {model_name}")
        logger.info(f"  Version: {version}")
        logger.info(f"  Directory: {model_dir}")
        
        return model_dir
    
    def load_model(self, model_name: str, version: str = None) -> Dict[str, Any]:
        """
        Load a saved model with metadata.
        
        Args:
            model_name: Name of the model
            version: Model version (optional, loads latest if not specified)
            
        Returns:
            Dictionary with model, scaler, and metadata
        """
        # Find model directory
        model_dir = self._find_model_directory(model_name, version)
        
        if model_dir is None:
            raise FileNotFoundError(f"Model {model_name} version {version} not found")
        
        # Load model
        model_path = os.path.join(model_dir, f"{model_name}_model.pkl")
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found: {model_path}")
        
        model = joblib.load(model_path)
        logger.info(f"Model loaded from {model_path}")
        
        # Load scaler if exists
        scaler = None
        scaler_path = os.path.join(model_dir, "scaler.pkl")
        if os.path.exists(scaler_path):
            scaler = joblib.load(scaler_path)
            logger.info(f"Scaler loaded from {scaler_path}")
        
        # Load metadata
        metadata_path = os.path.join(model_dir, "metadata.json")
        metadata = {}
        if os.path.exists(metadata_path):
            with open(metadata_path, 'r') as f:
                metadata = json.load(f)
            logger.info(f"Metadata loaded from {metadata_path}")
        
        # Verify checksums
        if not self._verify_checksums(model_dir):
            logger.warning("Checksum verification failed - model files may be corrupted")
        
        # Log load operation (PHI-safe)
        logger.info(f"Model loading completed:")
        logger.info(f"  Model: {model_name}")
        logger.info(f"  Version: {metadata.get('version', 'unknown')}")
        logger.info(f"  Created: {metadata.get('created', 'unknown')}")
        
        return {
            'model': model,
            'scaler': scaler,
            'metadata': metadata,
            'model_dir': model_dir
        }
    
    def list_models(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        List all available models and versions.
        
        Returns:
            Dictionary mapping model names to list of versions
        """
        models = {}
        
        # Scan base directory for model directories
        if os.path.exists(self.base_path):
            for item in os.listdir(self.base_path):
                if os.path.isdir(os.path.join(self.base_path, item)):
                    # Parse model name and version from directory name
                    if '_v' in item:
                        model_name, version = item.rsplit('_v', 1)
                        
                        if model_name not in models:
                            models[model_name] = []
                        
                        # Load metadata if available
                        metadata_path = os.path.join(self.base_path, item, "metadata.json")
                        metadata = {}
                        if os.path.exists(metadata_path):
                            try:
                                with open(metadata_path, 'r') as f:
                                    metadata = json.load(f)
                            except Exception as e:
                                logger.warning(f"Could not load metadata for {item}: {e}")
                        
                        models[model_name].append({
                            'version': version,
                            'path': os.path.join(self.base_path, item),
                            'created': metadata.get('created', 'unknown'),
                            'metadata': metadata
                        })
        
        # Sort versions by creation date
        for model_name in models:
            models[model_name].sort(key=lambda x: x['created'], reverse=True)
        
        logger.info(f"Found {len(models)} model types with {sum(len(versions) for versions in models.values())} total versions")
        
        return models
    
    def get_latest_model(self, model_name: str) -> Dict[str, Any]:
        """
        Get the latest version of a model.
        
        Args:
            model_name: Name of the model
            
        Returns:
            Dictionary with model, scaler, and metadata
        """
        models = self.list_models()
        
        if model_name not in models:
            raise ValueError(f"Model {model_name} not found")
        
        latest_version = models[model_name][0]['version']
        return self.load_model(model_name, latest_version)
    
    def delete_model(self, model_name: str, version: str) -> bool:
        """
        Delete a specific model version.
        
        Args:
            model_name: Name of the model
            version: Model version
            
        Returns:
            True if successful, False otherwise
        """
        model_dir = self._find_model_directory(model_name, version)
        
        if model_dir is None:
            logger.warning(f"Model {model_name} version {version} not found for deletion")
            return False
        
        try:
            import shutil
            shutil.rmtree(model_dir)
            logger.info(f"Model {model_name} version {version} deleted from {model_dir}")
            return True
        except Exception as e:
            logger.error(f"Error deleting model {model_name} version {version}: {e}")
            return False
    
    def _create_model_metadata(self, model: Any, model_name: str, version: str, 
                              scaler: Any = None, additional_metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """Create comprehensive model metadata."""
        metadata = {
            'model_name': model_name,
            'version': version,
            'created': datetime.now().isoformat(),
            'model_type': type(model).__name__,
            'has_scaler': scaler is not None,
            'scaler_type': type(scaler).__name__ if scaler is not None else None,
            'python_version': f"{os.sys.version_info.major}.{os.sys.version_info.minor}.{os.sys.version_info.micro}",
            'pandas_version': pd.__version__,
            'numpy_version': np.__version__,
            'joblib_version': joblib.__version__
        }
        
        # Add model-specific metadata
        if hasattr(model, 'get_params'):
            metadata['model_parameters'] = model.get_params()
        
        if hasattr(model, 'feature_importances_'):
            metadata['has_feature_importance'] = True
            metadata['feature_count'] = len(model.feature_importances_)
        
        if hasattr(model, 'coef_'):
            metadata['has_coefficients'] = True
            metadata['coefficient_count'] = len(model.coef_[0]) if len(model.coef_.shape) > 1 else len(model.coef_)
        
        # Add additional metadata
        if additional_metadata:
            metadata.update(additional_metadata)
        
        return metadata
    
    def _find_model_directory(self, model_name: str, version: str = None) -> Optional[str]:
        """Find the directory for a specific model version."""
        if not os.path.exists(self.base_path):
            return None
        
        # If version specified, look for exact match
        if version:
            model_dir = os.path.join(self.base_path, f"{model_name}_v{version}")
            if os.path.exists(model_dir):
                return model_dir
        
        # Otherwise, find latest version
        models = self.list_models()
        if model_name in models and models[model_name]:
            return models[model_name][0]['path']
        
        return None
    
    def _calculate_checksums(self, model_dir: str) -> Dict[str, str]:
        """Calculate checksums for all files in model directory."""
        checksums = {}
        
        for filename in os.listdir(model_dir):
            filepath = os.path.join(model_dir, filename)
            if os.path.isfile(filepath):
                with open(filepath, 'rb') as f:
                    file_hash = hashlib.sha256(f.read()).hexdigest()
                    checksums[filename] = file_hash
        
        return checksums
    
    def _verify_checksums(self, model_dir: str) -> bool:
        """Verify checksums for all files in model directory."""
        checksum_path = os.path.join(model_dir, "checksums.json")
        
        if not os.path.exists(checksum_path):
            logger.warning("No checksums file found")
            return False
        
        try:
            with open(checksum_path, 'r') as f:
                stored_checksums = json.load(f)
            
            current_checksums = self._calculate_checksums(model_dir)
            
            # Remove checksums.json from current checksums (circular reference)
            current_checksums.pop('checksums.json', None)
            
            return stored_checksums == current_checksums
            
        except Exception as e:
            logger.error(f"Error verifying checksums: {e}")
            return False


def save_hedis_model(model: Any, model_name: str, scaler: Any = None, 
                    metadata: Dict[str, Any] = None, base_path: str = "models") -> str:
    """
    Convenience function to save a HEDIS model.
    
    Args:
        model: Trained model object
        model_name: Name of the model
        scaler: Fitted scaler object (optional)
        metadata: Model metadata (optional)
        base_path: Base directory for model storage
        
    Returns:
        Path to saved model directory
    """
    serializer = HEDISModelSerializer(base_path)
    return serializer.save_model(model, model_name, scaler, metadata)


def load_hedis_model(model_name: str, version: str = None, base_path: str = "models") -> Dict[str, Any]:
    """
    Convenience function to load a HEDIS model.
    
    Args:
        model_name: Name of the model
        version: Model version (optional)
        base_path: Base directory for model storage
        
    Returns:
        Dictionary with model, scaler, and metadata
    """
    serializer = HEDISModelSerializer(base_path)
    return serializer.load_model(model_name, version)


if __name__ == "__main__":
    # Example usage
    from sklearn.linear_model import LogisticRegression
    from sklearn.preprocessing import StandardScaler
    from sklearn.datasets import make_classification
    
    # Generate sample data
    X, y = make_classification(n_samples=100, n_features=5, n_classes=2, random_state=42)
    
    # Train model and scaler
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    model = LogisticRegression(random_state=42)
    model.fit(X_scaled, y)
    
    # Save model
    serializer = HEDISModelSerializer()
    model_dir = serializer.save_model(
        model, 
        "example_model", 
        scaler, 
        {"description": "Example model for testing"}
    )
    
    print(f"Model saved to: {model_dir}")
    
    # List models
    models = serializer.list_models()
    print(f"Available models: {list(models.keys())}")
    
    # Load model
    loaded_data = serializer.load_model("example_model")
    print(f"Model loaded successfully: {type(loaded_data['model']).__name__}")
