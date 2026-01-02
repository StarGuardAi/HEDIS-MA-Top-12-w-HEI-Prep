"""Check ML library availability"""
import sys

print("Python version:", sys.version)
print("Python path:", sys.executable)
print()

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

print()
print("Testing ml_gap_closure_model import:")
try:
    import sys
    sys.path.insert(0, 'Artifacts/project/phase4_dashboard')
    from utils.ml_gap_closure_model import ML_LIBRARIES_AVAILABLE
    print(f"ML_LIBRARIES_AVAILABLE: {ML_LIBRARIES_AVAILABLE}")
except Exception as e:
    print(f"Error: {e}")

