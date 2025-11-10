"""
Generate synthetic fraud detection dataset with command-line arguments.

This script creates realistic fraud scenarios for demonstration purposes.
NOT for production use.
"""

import argparse
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.model_selection import train_test_split
from datetime import datetime, timedelta
import uuid
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Set random seed for reproducibility
np.random.seed(42)


def create_synthetic_fraud_data(n_samples=100_000, fraud_rate=0.015):
    """Generate synthetic fraud dataset."""
    
    logger.info(f"Generating {n_samples:,} synthetic transactions...")
    logger.info(f"Target fraud rate: {fraud_rate*100:.1f}%")
    
    n_fraud = int(n_samples * fraud_rate)
    n_legit = n_samples - n_fraud
    
    # Generate transaction IDs
    transaction_ids = [str(uuid.uuid4()) for _ in range(n_samples)]
    
    # Generate timestamps
    start_date = datetime(2024, 1, 1)
    timestamps = [
        start_date + timedelta(minutes=np.random.randint(0, 30*24*60))
        for _ in range(n_samples)
    ]
    
    # Generate customer IDs
    num_customers = 25_000
    customer_ids = [
        f"CUST_{np.random.randint(1, num_customers+1):06d}"
        for _ in range(n_samples)
    ]
    
    # Generate merchant IDs
    num_merchants = 5_000
    merchant_ids = [
        f"MERCH_{np.random.randint(1, num_merchants+1):05d}"
        for _ in range(n_samples)
    ]
    
    # Generate legitimate transactions
    legit_data = {
        'transaction_id': transaction_ids[:n_legit],
        'customer_id': customer_ids[:n_legit],
        'merchant_id': merchant_ids[:n_legit],
        'timestamp': timestamps[:n_legit],
        'amount': np.random.lognormal(4.5, 0.8, n_legit).clip(1, 5000),
        'hour': np.random.choice(range(8, 22), n_legit),  # Business hours
        'is_fraud': 0
    }
    
    # Generate fraud transactions
    fraud_data = {
        'transaction_id': transaction_ids[n_legit:],
        'customer_id': customer_ids[n_legit:],
        'merchant_id': merchant_ids[n_legit:],
        'timestamp': timestamps[n_legit:],
        'amount': np.random.lognormal(6.0, 1.2, n_fraud).clip(100, 10000),
        'hour': np.random.choice(range(0, 7), n_fraud),  # Night time
        'is_fraud': 1
    }
    
    # Combine
    df_legit = pd.DataFrame(legit_data)
    df_fraud = pd.DataFrame(fraud_data)
    df = pd.concat([df_legit, df_fraud], ignore_index=True)
    
    # Sort by timestamp
    df = df.sort_values('timestamp').reset_index(drop=True)
    
    # Add more features
    df['amount_log'] = np.log1p(df['amount'])
    df['is_weekend'] = (df['timestamp'].dt.dayofweek >= 5).astype(int)
    df['velocity_24h'] = np.where(
        df['is_fraud'] == 1,
        np.random.poisson(15, n_samples),  # High velocity for fraud
        np.random.poisson(3, n_samples)    # Low velocity for legit
    )
    df['amount_deviation'] = np.where(
        df['is_fraud'] == 1,
        np.random.exponential(2.5, n_samples),  # High deviation for fraud
        np.random.exponential(0.5, n_samples)   # Low deviation for legit
    )
    df['merchant_risk_score'] = np.where(
        df['is_fraud'] == 1,
        np.random.beta(8, 2, n_samples),   # Fraud: high-risk merchants
        np.random.beta(2, 8, n_samples)    # Legitimate: low-risk merchants
    )
    
    # Shuffle
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)
    
    logger.info(f"✅ Generated {len(df):,} transactions")
    logger.info(f"   Fraud: {df['is_fraud'].sum():,} ({df['is_fraud'].mean()*100:.2f}%)")
    logger.info(f"   Legitimate: {(~df['is_fraud'].astype(bool)).sum():,}")
    
    return df


def create_train_test_split(df, test_size=0.2):
    """Split into train/test."""
    X = df.drop('is_fraud', axis=1)
    y = df['is_fraud']
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=42, stratify=y
    )
    
    return X_train, X_test, y_train, y_test


def main():
    """Main function with command-line argument parsing."""
    parser = argparse.ArgumentParser(
        description='Generate synthetic fraud detection dataset',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/generate_synthetic_data.py --num-transactions 600000 --fraud-rate 0.015 --output data/processed/
  python scripts/generate_synthetic_data.py -n 100000 -f 0.02 -o data/processed/
        """
    )
    
    parser.add_argument(
        '--num-transactions', '-n',
        type=int,
        default=100_000,
        help='Number of transactions to generate (default: 100000)'
    )
    
    parser.add_argument(
        '--fraud-rate', '-f',
        type=float,
        default=0.015,
        help='Fraud rate as decimal (default: 0.015)'
    )
    
    parser.add_argument(
        '--output', '-o',
        type=str,
        default='data/processed/',
        help='Output directory for processed data (default: data/processed/)'
    )
    
    args = parser.parse_args()
    
    # Validate arguments
    if args.num_transactions <= 0:
        logger.error("Number of transactions must be positive")
        return 1
    
    if not (0 < args.fraud_rate < 1):
        logger.error("Fraud rate must be between 0 and 1")
        return 1
    
    # Create output directory
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    logger.info(f"Output directory: {output_dir.absolute()}")
    
    # Generate data
    df = create_synthetic_fraud_data(
        n_samples=args.num_transactions,
        fraud_rate=args.fraud_rate
    )
    
    # Create train/test split
    logger.info("Creating train/test split...")
    X_train, X_test, y_train, y_test = create_train_test_split(df, test_size=0.2)
    
    # Save datasets
    logger.info(f"Saving datasets to {output_dir}...")
    
    # Save train/test splits (X and y separate)
    X_train.to_csv(output_dir / "X_train.csv", index=False)
    X_test.to_csv(output_dir / "X_test.csv", index=False)
    y_train.to_csv(output_dir / "y_train.csv", index=False)
    y_test.to_csv(output_dir / "y_test.csv", index=False)
    
    # Save combined train/test datasets with target included
    train_df = X_train.copy()
    train_df['is_fraud'] = y_train.values
    train_df.to_csv(output_dir / "train.csv", index=False)
    
    test_df = X_test.copy()
    test_df['is_fraud'] = y_test.values
    test_df.to_csv(output_dir / "test.csv", index=False)
    
    # Also save full dataset
    df.to_csv(output_dir / "full_dataset.csv", index=False)
    
    logger.info("=" * 60)
    logger.info("✅ Dataset generation complete!")
    logger.info(f"   Training samples: {len(X_train):,}")
    logger.info(f"   Test samples: {len(X_test):,}")
    logger.info(f"   Features: {X_train.shape[1]}")
    logger.info(f"   Fraud rate: {y_train.mean()*100:.2f}%")
    logger.info(f"   Data saved to: {output_dir.absolute()}")
    logger.info("=" * 60)
    
    return 0


if __name__ == "__main__":
    exit(main())

