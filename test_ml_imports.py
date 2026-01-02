"""Test ML library imports"""
try:
    import xgboost
    print(f"✅ xgboost: {xgboost.__version__}")
except ImportError as e:
    print(f"❌ xgboost: {e}")

try:
    import sklearn
    print(f"✅ scikit-learn: {sklearn.__version__}")
except ImportError as e:
    print(f"❌ scikit-learn: {e}")

try:
    from imblearn.over_sampling import SMOTE
    print("✅ imbalanced-learn: Available")
except ImportError as e:
    print(f"❌ imbalanced-learn: {e}")

