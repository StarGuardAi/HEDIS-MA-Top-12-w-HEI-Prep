"""
Quick XGBoost training on synthetic data.
~5 minutes instead of hours.
"""

import pandas as pd
import xgboost as xgb
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
import joblib
from pathlib import Path
import json
import sys

# Ensure UTF-8 encoding for output
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

print("Loading data...", flush=True)
# Adjust paths to point to repo-guardian data
project_root = Path(__file__).parent.parent
data_dir = project_root / "project" / "repo-guardian" / "data" / "processed"

X_train = pd.read_csv(data_dir / "X_train.csv")
y_train = pd.read_csv(data_dir / "y_train.csv").squeeze()
X_test = pd.read_csv(data_dir / "X_test.csv")
y_test = pd.read_csv(data_dir / "y_test.csv").squeeze()

print(f"Training on {len(X_train):,} samples...", flush=True)

# Train simple model
model = xgb.XGBClassifier(
    max_depth=6,
    learning_rate=0.1,
    n_estimators=100,
    scale_pos_weight=(1 - y_train.mean()) / y_train.mean(),
    random_state=42,
    n_jobs=-1
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

print("\n" + "="*50, flush=True)
print("MODEL PERFORMANCE", flush=True)
print("="*50, flush=True)
for metric, value in metrics.items():
    print(f"{metric:12s}: {value:.4f}", flush=True)
print("="*50, flush=True)

# Save model
models_dir = project_root / "project" / "repo-guardian" / "models"
models_dir.mkdir(exist_ok=True)
model_path = models_dir / "xgboost_fraud_demo.pkl"
joblib.dump(model, model_path)
print(f"\n✅ Model saved to {model_path}", flush=True)

# Save metrics
reports_dir = project_root / "project" / "repo-guardian" / "reports"
reports_dir.mkdir(exist_ok=True)
metrics_path = reports_dir / "metrics.json"
with open(metrics_path, "w") as f:
    json.dump(metrics, f, indent=2)
print(f"✅ Metrics saved to {metrics_path}", flush=True)

