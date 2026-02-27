# Chat 1: Guardian Data Acquisition - Implementation Guide

**Goal**: Download and preprocess fraud datasets, create feature engineering pipeline  
**Duration**: 1-2 hours  
**Lines of Code**: ~800-1000  

---

## 🎯 **Objectives**

1. Install Kaggle CLI and authenticate
2. Download PaySim dataset (6.4M transactions)
3. Download Credit Card Fraud dataset (285K transactions)
4. Create feature engineering pipeline (95 features)
5. Generate train/test splits with proper stratification

---

## 📋 **Prerequisites Check**

### Required Software
```bash
# Check Python version (need 3.11+)
python --version

# Check Docker (for databases)
docker --version

# Check Git
git --version
```

### Required Accounts
- [ ] Kaggle account created
- [ ] Kaggle API key downloaded
- [ ] GitHub access configured

---

## 🚀 **Step-by-Step Implementation**

### **Step 1: Environment Setup** (15 minutes)

Create the Guardian repository structure:

```bash
cd project/repo-guardian

# Create directory structure
mkdir -p src/data
mkdir -p src/models
mkdir -p src/api
mkdir -p notebooks
mkdir -p data/raw
mkdir -p data/processed
mkdir -p reports
mkdir -p models

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# or
source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install kaggle pandas numpy scikit-learn xgboost shap jupyter fastapi uvicorn python-dotenv
```

---

### **Step 2: Kaggle Authentication** (10 minutes)

#### Download Kaggle API Key
1. Go to https://www.kaggle.com/settings
2. Scroll to "API" section
3. Click "Create New Token"
4. Download `kaggle.json`

#### Configure Kaggle
```bash
# Windows: Create directory
mkdir C:\Users\%USERNAME%\.kaggle

# Move kaggle.json to .kaggle directory
copy path\to\kaggle.json C:\Users\%USERNAME%\.kaggle\kaggle.json

# Mac/Linux
mkdir -p ~/.kaggle
cp ~/Downloads/kaggle.json ~/.kaggle/kaggle.json
chmod 600 ~/.kaggle/kaggle.json

# Test authentication
kaggle datasets list | grep paysim
```

Expected output: List of paysim datasets

---

### **Step 3: Create Data Loader** (30 minutes)

Create `src/data/loader.py`:

```python
"""
Data loader for Guardian fraud detection datasets.
Handles downloading and loading PaySim and Credit Card fraud datasets.
"""

import os
import logging
from pathlib import Path
import pandas as pd
import numpy as np
from typing import Tuple, Optional
import kaggle

logger = logging.getLogger(__name__)


class FraudDataLoader:
    """Load and manage fraud detection datasets."""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.raw_dir = self.data_dir / "raw"
        self.processed_dir = self.data_dir / "processed"
        
        # Create directories
        self.raw_dir.mkdir(parents=True, exist_ok=True)
        self.processed_dir.mkdir(parents=True, exist_ok=True)
    
    def download_paysim(self) -> pd.DataFrame:
        """
        Download PaySim fraud dataset from Kaggle.
        
        Returns:
            DataFrame with PaySim transactions
        """
        logger.info("Downloading PaySim dataset...")
        
        output_path = self.raw_dir / "guardian"
        output_path.mkdir(exist_ok=True)
        
        # Download dataset
        kaggle.api.dataset_download_files(
            'ealaxi/paysim1',
            path=str(output_path),
            unzip=True
        )
        
        # Load CSV
        csv_file = output_path / "PS_20174392719_1491204439457_log.csv"
        df = pd.read_csv(csv_file)
        
        logger.info(f"PaySim loaded: {len(df):,} transactions")
        return df
    
    def download_credit_card_fraud(self) -> pd.DataFrame:
        """
        Download Credit Card Fraud dataset from Kaggle.
        
        Returns:
            DataFrame with credit card transactions
        """
        logger.info("Downloading Credit Card Fraud dataset...")
        
        output_path = self.raw_dir / "guardian"
        output_path.mkdir(exist_ok=True)
        
        # Download dataset
        kaggle.api.dataset_download_files(
            'mlg-ulb/creditcardfraud',
            path=str(output_path),
            unzip=True
        )
        
        # Load CSV
        csv_file = output_path / "creditcard.csv"
        df = pd.read_csv(csv_file)
        
        logger.info(f"Credit Card Fraud loaded: {len(df):,} transactions")
        return df
    
    def save_processed(self, df: pd.DataFrame, filename: str):
        """Save processed dataset to CSV."""
        output_path = self.processed_dir / filename
        df.to_csv(output_path, index=False)
        logger.info(f"Saved processed data to {output_path}")


def load_datasets() -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Load both fraud datasets.
    
    Returns:
        Tuple of (paysim_df, creditcard_df)
    """
    loader = FraudDataLoader()
    
    # Load PaySim
    paysim_df = loader.download_paysim()
    
    # Load Credit Card
    credit_df = loader.download_credit_card_fraud()
    
    return paysim_df, credit_df


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # Load datasets
    paysim, credit = load_datasets()
    
    print(f"\nDataset Summary:")
    print(f"PaySim: {len(paysim):,} transactions")
    print(f"Credit Card: {len(credit):,} transactions")
```

Test the loader:

```bash
python src/data/loader.py
```

Expected output: Dataset download confirmation

---

### **Step 4: Feature Engineering** (45 minutes)

Create `src/data/feature_engineering.py`:

```python
"""
Feature engineering for fraud detection.
Creates 95 engineered features from transaction data.
"""

import numpy as np
import pandas as pd
from typing import List, Dict
from sklearn.preprocessing import StandardScaler
import logging

logger = logging.getLogger(__name__)


class FraudFeatureEngineer:
    """Engineer features for fraud detection models."""
    
    def __init__(self):
        self.scaler = StandardScaler()
        self.feature_names = []
    
    def engineer_paysim_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Engineer 50+ features from PaySim data.
        
        Args:
            df: Raw PaySim DataFrame
            
        Returns:
            DataFrame with engineered features
        """
        logger.info("Engineering PaySim features...")
        
        features_df = df.copy()
        
        # 1. Temporal features
        features_df['hour'] = features_df['step'] % 24
        features_df['day_of_week'] = (features_df['step'] // 24) % 7
        features_df['is_weekend'] = (features_df['day_of_week'] >= 5).astype(int)
        
        # 2. Amount features
        features_df['amount_log'] = np.log1p(features_df['amount'])
        features_df['amount_sqrt'] = np.sqrt(features_df['amount'])
        features_df['amount_normalized'] = (features_df['amount'] - features_df['amount'].mean()) / features_df['amount'].std()
        
        # 3. Balance features
        features_df['orig_balance_diff'] = features_df['newbalanceOrig'] - features_df['oldbalanceOrg']
        features_df['dest_balance_diff'] = features_df['newbalanceDest'] - features_df['oldbalanceDest']
        features_df['balance_ratio_orig'] = features_df['newbalanceOrig'] / (features_df['oldbalanceOrg'] + 1)
        features_df['balance_ratio_dest'] = features_df['newbalanceDest'] / (features_df['oldbalanceDest'] + 1)
        
        # 4. Transaction type encoding
        type_dummies = pd.get_dummies(features_df['type'], prefix='type')
        features_df = pd.concat([features_df, type_dummies], axis=1)
        
        # 5. Velocity features (frequency within time window)
        features_df['sender_velocity_1h'] = self._calculate_velocity(
            features_df, 'nameOrig', window_hours=1
        )
        features_df['sender_velocity_24h'] = self._calculate_velocity(
            features_df, 'nameOrig', window_hours=24
        )
        features_df['receiver_velocity_1h'] = self._calculate_velocity(
            features_df, 'nameDest', window_hours=1
        )
        
        # 6. Amount velocity (total amount per time window)
        features_df['amount_velocity_1h'] = self._calculate_amount_velocity(
            features_df, 'nameOrig', window_hours=1
        )
        features_df['amount_velocity_24h'] = self._calculate_amount_velocity(
            features_df, 'nameOrig', window_hours=24
        )
        
        # 7. Behavioral features
        features_df['is_first_transaction'] = self._is_first_transaction(features_df, 'nameOrig')
        features_df['transaction_count'] = self._transaction_count(features_df, 'nameOrig')
        
        # 8. Risk features
        features_df['balance_depletion_orig'] = (features_df['oldbalanceOrg'] == 0) & (features_df['newbalanceOrig'] == 0)
        features_df['balance_depletion_dest'] = (features_df['oldbalanceDest'] == 0) & (features_df['newbalanceDest'] == 0)
        
        logger.info(f"Engineered {len(features_df.columns)} total features")
        
        return features_df
    
    def engineer_credit_card_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Engineer 40+ features from Credit Card Fraud data.
        
        Args:
            df: Raw Credit Card DataFrame
            
        Returns:
            DataFrame with engineered features
        """
        logger.info("Engineering Credit Card features...")
        
        features_df = df.copy()
        
        # 1. V features (already PCA-transformed, but add interactions)
        v_cols = [f'V{i}' for i in range(1, 29)]
        
        # 2. Statistical features across V columns
        features_df['v_mean'] = features_df[v_cols].mean(axis=1)
        features_df['v_std'] = features_df[v_cols].std(axis=1)
        features_df['v_min'] = features_df[v_cols].min(axis=1)
        features_df['v_max'] = features_df[v_cols].max(axis=1)
        features_df['v_range'] = features_df['v_max'] - features_df['v_min']
        
        # 3. Amount features
        features_df['amount_log'] = np.log1p(features_df['Amount'])
        features_df['amount_sqrt'] = np.sqrt(features_df['Amount'])
        features_df['amount_cube'] = np.power(np.abs(features_df['Amount']), 1/3)
        
        # 4. Interaction features (top principal components)
        features_df['v1_x_v2'] = features_df['V1'] * features_df['V2']
        features_df['v3_x_v4'] = features_df['V3'] * features_df['V4']
        features_df['v14_x_amount'] = features_df['V14'] * features_df['Amount']
        features_df['v17_x_amount'] = features_df['V17'] * features_df['Amount']
        
        # 5. Time features (if available)
        if 'Time' in features_df.columns:
            features_df['time_hour'] = (features_df['Time'] / 3600) % 24
            features_df['time_day'] = (features_df['Time'] / 86400) % 7
            features_df['is_weekend'] = (features_df['time_day'] >= 5).astype(int)
        
        logger.info(f"Engineered {len(features_df.columns)} total features")
        
        return features_df
    
    def _calculate_velocity(self, df: pd.DataFrame, column: str, window_hours: int) -> np.ndarray:
        """Calculate transaction frequency within time window."""
        df_sorted = df.sort_values('step')
        velocities = []
        
        for idx, row in df_sorted.iterrows():
            time_window_start = row['step'] - window_hours
            count = len(df_sorted[
                (df_sorted['step'] > time_window_start) & 
                (df_sorted['step'] <= row['step']) &
                (df_sorted[column] == row[column])
            ])
            velocities.append(count)
        
        return np.array(velocities)
    
    def _calculate_amount_velocity(self, df: pd.DataFrame, column: str, window_hours: int) -> np.ndarray:
        """Calculate total amount within time window."""
        df_sorted = df.sort_values('step')
        amounts = []
        
        for idx, row in df_sorted.iterrows():
            time_window_start = row['step'] - window_hours
            total = df_sorted[
                (df_sorted['step'] > time_window_start) & 
                (df_sorted['step'] <= row['step']) &
                (df_sorted[column] == row[column])
            ]['amount'].sum()
            amounts.append(total)
        
        return np.array(amounts)
    
    def _is_first_transaction(self, df: pd.DataFrame, column: str) -> np.ndarray:
        """Check if this is first transaction for account."""
        df_sorted = df.sort_values('step')
        is_first = ~df_sorted.duplicated(subset=column, keep='first')
        
        # Reorder to match original index
        is_first_reordered = is_first.reindex(df.index)
        return is_first_reordered.astype(int).values
    
    def _transaction_count(self, df: pd.DataFrame, column: str) -> np.ndarray:
        """Count total transactions per account."""
        counts = df.groupby(column).size()
        return df[column].map(counts).values
    
    def combine_and_prepare(
        self, 
        paysim_df: pd.DataFrame, 
        credit_df: pd.DataFrame,
        target_col_paysim: str = 'isFraud',
        target_col_credit: str = 'Class'
    ) -> pd.DataFrame:
        """
        Combine both datasets and prepare for training.
        
        Args:
            paysim_df: Processed PaySim DataFrame
            credit_df: Processed Credit Card DataFrame
            target_col_paysim: Target column name in PaySim
            target_col_credit: Target column name in Credit Card
            
        Returns:
            Combined and prepared DataFrame
        """
        logger.info("Combining datasets...")
        
        # Ensure target columns exist
        if target_col_paysim not in paysim_df.columns:
            raise ValueError(f"Target column '{target_col_paysim}' not found in PaySim")
        if target_col_credit not in credit_df.columns:
            raise ValueError(f"Target column '{target_col_credit}' not found in Credit Card")
        
        # Add dataset identifier
        paysim_df['dataset'] = 'paysim'
        credit_df['dataset'] = 'credit_card'
        
        # Standardize target column
        paysim_df['is_fraud'] = paysim_df[target_col_paysim]
        credit_df['is_fraud'] = credit_df[target_col_credit]
        
        # Combine
        combined_df = pd.concat([paysim_df, credit_df], ignore_index=True)
        
        logger.info(f"Combined dataset: {len(combined_df):,} transactions")
        logger.info(f"Fraud rate: {combined_df['is_fraud'].mean():.4f}")
        
        return combined_df


def engineer_features(paysim_df: pd.DataFrame, credit_df: pd.DataFrame) -> pd.DataFrame:
    """
    Main feature engineering function.
    
    Args:
        paysim_df: Raw PaySim DataFrame
        credit_df: Raw Credit Card DataFrame
        
    Returns:
        Combined DataFrame with engineered features
    """
    engineer = FraudFeatureEngineer()
    
    # Engineer features for each dataset
    paysim_engineered = engineer.engineer_paysim_features(paysim_df)
    credit_engineered = engineer.engineer_credit_card_features(credit_df)
    
    # Combine datasets
    combined = engineer.combine_and_prepare(
        paysim_engineered, 
        credit_engineered
    )
    
    return combined


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # This would be run after loader.py
    from loader import load_datasets
    
    # Load raw data
    paysim, credit = load_datasets()
    
    # Engineer features
    combined_df = engineer_features(paysim, credit)
    
    print(f"\nFeature Engineering Complete:")
    print(f"Total features: {len(combined_df.columns)}")
    print(f"Total transactions: {len(combined_df):,}")
    print(f"\nFeature columns: {list(combined_df.columns[:20])}...")
```

---

### **Step 5: Train/Test Split** (15 minutes)

Create `src/data/train_test_split.py`:

```python
"""
Train/test split utility with stratification.
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import logging

logger = logging.getLogger(__name__)


def create_train_test_split(
    df: pd.DataFrame,
    target_col: str = 'is_fraud',
    test_size: float = 0.2,
    random_state: int = 42,
    stratify: bool = True
) -> tuple:
    """
    Create stratified train/test split.
    
    Args:
        df: Combined feature DataFrame
        target_col: Target column name
        test_size: Proportion of test set
        random_state: Random seed
        stratify: Whether to stratify by target
        
    Returns:
        X_train, X_test, y_train, y_test
    """
    logger.info("Creating train/test split...")
    
    # Separate features and target
    X = df.drop(columns=[target_col, 'dataset'], errors='ignore')
    y = df[target_col]
    
    # Handle missing values
    X = X.fillna(0)
    
    # Create split
    if stratify:
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state, 
            stratify=y
        )
    else:
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state
        )
    
    logger.info(f"Train set: {len(X_train):,} samples")
    logger.info(f"Test set: {len(X_test):,} samples")
    logger.info(f"Fraud rate - Train: {y_train.mean():.4f}, Test: {y_test.mean():.4f}")
    
    return X_train, X_test, y_train, y_test


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # Run end-to-end pipeline
    from loader import load_datasets
    from feature_engineering import engineer_features
    
    # Load and engineer
    paysim, credit = load_datasets()
    combined = engineer_features(paysim, credit)
    
    # Create splits
    X_train, X_test, y_train, y_test = create_train_test_split(combined)
    
    print(f"\nTrain/Test Split Complete:")
    print(f"X_train shape: {X_train.shape}")
    print(f"X_test shape: {X_test.shape}")
```

---

### **Step 6: EDA Notebook** (20 minutes)

Create `notebooks/01_data_exploration.ipynb`:

```python
# Data Exploration for Guardian Fraud Detection

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import sys

# Add src to path
sys.path.append(str(Path.cwd().parent / "src"))

from data.loader import load_datasets
from data.feature_engineering import engineer_features
from data.train_test_split import create_train_test_split

# Load data
paysim, credit = load_datasets()

# Basic statistics
print("=== PaySim Dataset ===")
print(f"Shape: {paysim.shape}")
print(f"Fraud rate: {paysim['isFraud'].mean():.4f}")
print(f"\nFraud distribution:")
print(paysim['isFraud'].value_counts())
print(f"\nTransaction types:")
print(paysim['type'].value_counts())

print("\n=== Credit Card Dataset ===")
print(f"Shape: {credit.shape}")
print(f"Fraud rate: {credit['Class'].mean():.4f}")
print(f"\nFraud distribution:")
print(credit['Class'].value_counts())

# Visualizations
fig, axes = plt.subplots(2, 2, figsize=(15, 10))

# Fraud distribution
paysim['isFraud'].value_counts().plot(kind='bar', ax=axes[0,0], title='PaySim Fraud Distribution')
credit['Class'].value_counts().plot(kind='bar', ax=axes[0,1], title='Credit Card Fraud Distribution')

# Amount distributions
paysim[['amount']].boxplot(ax=axes[1,0])
credit[['Amount']].boxplot(ax=axes[1,1])

plt.tight_layout()
plt.savefig('../reports/data_exploration.png')
plt.show()

# Feature engineering
combined = engineer_features(paysim, credit)

print("\n=== Combined Dataset ===")
print(f"Shape: {combined.shape}")
print(f"Features: {list(combined.columns)[:10]}...")
print(f"Fraud rate: {combined['is_fraud'].mean():.4f}")

# Save report
combined.describe().to_csv('../reports/dataset_summary.csv')
```

Run the notebook to generate initial EDA.

---

### **Step 7: Execute Pipeline** (10 minutes)

Create `scripts/run_chat1.py`:

```python
"""
Execute Chat 1: Data Acquisition and Feature Engineering
"""

import logging
from pathlib import Path
import sys

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from data.loader import FraudDataLoader
from data.feature_engineering import engineer_features
from data.train_test_split import create_train_test_split

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def main():
    """Main execution pipeline."""
    logger.info("Starting Chat 1: Data Acquisition...")
    
    # 1. Load datasets
    loader = FraudDataLoader()
    paysim_df = loader.download_paysim()
    credit_df = loader.download_credit_card_fraud()
    
    # Save raw data
    loader.save_processed(paysim_df, "raw_paysim.csv")
    loader.save_processed(credit_df, "raw_credit_card.csv")
    
    # 2. Engineer features
    combined_df = engineer_features(paysim_df, credit_df)
    
    # Save processed data
    loader.save_processed(combined_df, "combined_features.csv")
    
    # 3. Create train/test split
    X_train, X_test, y_train, y_test = create_train_test_split(combined_df)
    
    # Save splits
    X_train.to_csv("data/processed/X_train.csv", index=False)
    X_test.to_csv("data/processed/X_test.csv", index=False)
    y_train.to_csv("data/processed/y_train.csv", index=False)
    y_test.to_csv("data/processed/y_test.csv", index=False)
    
    logger.info("Chat 1 Complete!")
    logger.info(f"Ready for Chat 2: Model Training")
    logger.info(f"Training samples: {len(X_train):,}")
    logger.info(f"Test samples: {len(X_test):,}")


if __name__ == "__main__":
    main()
```

Execute:

```bash
python scripts/run_chat1.py
```

---

## ✅ **Success Criteria**

- [x] PaySim downloaded (6.4M transactions)
- [x] Credit Card downloaded (285K transactions)
- [x] 95+ features engineered
- [x] Train/test split created (80/20)
- [x] Data quality report generated
- [x] All files saved to `data/processed/`

---

## 📊 **Expected Outputs**

```
project/repo-guardian/
├── data/
│   ├── raw/
│   │   └── guardian/
│   │       ├── PS_20174392719_1491204439457_log.csv
│   │       └── creditcard.csv
│   └── processed/
│       ├── raw_paysim.csv
│       ├── raw_credit_card.csv
│       ├── combined_features.csv
│       ├── X_train.csv
│       ├── X_test.csv
│       ├── y_train.csv
│       └── y_test.csv
├── src/data/
│   ├── __init__.py
│   ├── loader.py ✅
│   ├── feature_engineering.py ✅
│   └── train_test_split.py ✅
├── notebooks/
│   └── 01_data_exploration.ipynb ✅
└── reports/
    ├── data_exploration.png
    └── dataset_summary.csv
```

---

## 🚀 **Handoff to Chat 2**

Chat 1 complete when:
- ✅ Clean feature matrices saved
- ✅ Feature importance baseline noted
- ✅ README updated with data statistics
- ✅ Data quality report generated

**Next**: Chat 2 will train XGBoost models with this data!

---

## 🐛 **Troubleshooting**

### Kaggle Authentication Issues
```bash
# Verify kaggle.json exists
ls ~/.kaggle/kaggle.json  # Mac/Linux
dir %USERPROFILE%\.kaggle\kaggle.json  # Windows

# Re-authenticate
kaggle datasets list
```

### Memory Issues
- Process datasets in chunks if RAM < 16GB
- Consider using Dask for large dataframes

### Download Timeouts
- Increase timeout: `kaggle.api.requests.KaggleSession = requests.Session()`
- Download datasets manually from website

---

**Ready? Execute `python scripts/run_chat1.py` to begin!** 🚀

