"""
Quick XGBoost training on synthetic data.
~5 minutes instead of hours.
"""

import sys
import pandas as pd
import xgboost as xgb
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
import joblib
from pathlib import Path
import json
import logging

# Add src to path (from root scripts to repo-guardian/src)
script_dir = Path(__file__).parent
project_root = script_dir.parent
repo_guardian_src = project_root / "project" / "repo-guardian" / "src"
sys.path.append(str(repo_guardian_src))

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Train quick XGBoost model on synthetic demo data."""
    print("Loading data...")
    
    # Get project root (repo-guardian)
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    repo_guardian = project_root / "project" / "repo-guardian"
    data_dir = repo_guardian / "data" / "processed"
    models_dir = repo_guardian / "models"
    reports_dir = repo_guardian / "reports"
    
    # Create directories
    models_dir.mkdir(exist_ok=True)
    reports_dir.mkdir(exist_ok=True)
    
    # Load data
    X_train = pd.read_csv(data_dir / "X_train.csv")
    y_train = pd.read_csv(data_dir / "y_train.csv").squeeze()
    X_test = pd.read_csv(data_dir / "X_test.csv")
    y_test = pd.read_csv(data_dir / "y_test.csv").squeeze()
    
    print(f"Training on {len(X_train):,} samples...")
    
    # Train simple model (optimized for speed)
    model = xgb.XGBClassifier(
        max_depth=6,
        learning_rate=0.1,
        n_estimators=100,
        scale_pos_weight=(1 - y_train.mean()) / y_train.mean(),
        random_state=42,
        n_jobs=-1,
        eval_metric='auc'
    )
    
    model.fit(X_train, y_train, eval_set=[(X_test, y_test)], verbose=10)
    
    # Evaluate
    y_pred_proba = model.predict_proba(X_test)[:, 1]
    y_pred = (y_pred_proba >= 0.5).astype(int)
    
    metrics = {
        'accuracy': float(accuracy_score(y_test, y_pred)),
        'precision': float(precision_score(y_test, y_pred)),
        'recall': float(recall_score(y_test, y_pred)),
        'f1_score': float(f1_score(y_test, y_pred)),
        'auc_roc': float(roc_auc_score(y_test, y_pred_proba))
    }
    
    # Print results
    print("\n" + "="*50)
    print("MODEL PERFORMANCE")
    print("="*50)
    for metric, value in metrics.items():
        print(f"{metric:12s}: {value:.4f}")
    print("="*50)
    
    # Save model
    model_path = models_dir / "xgboost_fraud_demo.pkl"
    joblib.dump(model, model_path)
    print(f"\n✅ Model saved to {model_path}")
    
    # Save metrics
    metrics_path = reports_dir / "metrics.json"
    with open(metrics_path, "w") as f:
        json.dump(metrics, f, indent=2)
    print(f"✅ Metrics saved to {metrics_path}")


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    try:
        main()
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)

