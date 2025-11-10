"""
Create demo data for quick prototyping and testing.
Uses synthetic fraud detection dataset generator.
"""

import sys
import logging
from pathlib import Path

# Add src to path (from root scripts to repo-guardian/src)
script_dir = Path(__file__).parent
project_root = script_dir.parent
repo_guardian_src = project_root / "project" / "repo-guardian" / "src"
sys.path.append(str(repo_guardian_src))

from data.generate_synthetic_fraud_data import (
    create_synthetic_fraud_data,
    create_train_test_split
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Create demo fraud detection dataset."""
    logger.info("Creating demo fraud detection dataset...")
    logger.info("=" * 60)
    
    # Get project root (repo-guardian)
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    repo_guardian = project_root / "project" / "repo-guardian"
    data_dir = repo_guardian / "data" / "processed"
    data_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate synthetic data (100K samples for fast iteration)
    logger.info("Generating 100,000 synthetic transactions...")
    df = create_synthetic_fraud_data(n_samples=100_000, fraud_rate=0.015)
    
    # Create train/test split
    logger.info("Creating train/test split...")
    X_train, X_test, y_train, y_test = create_train_test_split(df, test_size=0.2)
    
    # Save datasets
    logger.info(f"Saving datasets to {data_dir}...")
    X_train.to_csv(data_dir / "X_train.csv", index=False)
    X_test.to_csv(data_dir / "X_test.csv", index=False)
    y_train.to_csv(data_dir / "y_train.csv", index=False)
    y_test.to_csv(data_dir / "y_test.csv", index=False)
    
    logger.info("=" * 60)
    logger.info("✅ Demo data creation complete!")
    logger.info(f"   Training samples: {len(X_train):,}")
    logger.info(f"   Test samples: {len(X_test):,}")
    logger.info(f"   Features: {X_train.shape[1]}")
    logger.info(f"   Fraud rate: {y_train.mean()*100:.2f}%")
    logger.info(f"   Data saved to: {data_dir}")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()

