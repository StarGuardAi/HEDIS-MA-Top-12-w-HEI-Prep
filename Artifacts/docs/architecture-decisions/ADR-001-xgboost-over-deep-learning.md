# ADR-001: Use XGBoost/LightGBM over Deep Learning

## Status
Accepted

## Context
HEDIS gap-in-care prediction requires:
- High interpretability for clinical trust
- Low latency for real-time predictions (<500ms)
- Good performance with limited training data (typical health plan datasets)
- Explainability requirements for regulatory compliance

## Decision
Use XGBoost and LightGBM gradient boosting models instead of deep learning (neural networks).

## Consequences

**Positive:**
- ✅ Interpretable predictions with SHAP values (critical for clinical trust)
- ✅ Lower latency (<100ms per prediction vs. 300-500ms for neural networks)
- ✅ Better performance with limited data (typical health plan datasets are 10K-100K members)
- ✅ Feature importance readily available (SHAP, built-in feature importance)
- ✅ Easier to debug and validate (decision trees are human-readable)

**Negative:**
- ⚠️ Potentially lower accuracy ceiling (though achieved 91% AUC-ROC, which is excellent)
- ⚠️ Less automatic feature learning (requires manual feature engineering)
- ⚠️ May need more hyperparameter tuning

## Alternatives Considered

**Neural Networks (PyTorch/TensorFlow):**
- ❌ Black box predictions (hard to explain to clinicians)
- ❌ Higher latency (300-500ms vs. <100ms)
- ❌ Requires more data to generalize well
- ✅ Could potentially achieve higher accuracy with enough data
- **Decision:** Healthcare context prioritizes interpretability over marginal accuracy gains

**Random Forest:**
- ✅ Interpretable (feature importance available)
- ✅ Fast predictions
- ❌ Lower accuracy than XGBoost/LightGBM (typically 2-3% lower AUC-ROC)
- **Decision:** XGBoost/LightGBM provide better accuracy with similar interpretability

## Implementation Notes
- Used XGBoost for primary models
- LightGBM as ensemble alternative (slightly faster, similar accuracy)
- SHAP TreeExplainer for post-hoc interpretability
- Achieved 91% average AUC-ROC across 12 HEDIS measures

## References
- XGBoost paper: "XGBoost: A Scalable Tree Boosting System" (Chen & Guestrin, 2016)
- SHAP paper: "A Unified Approach to Interpreting Model Predictions" (Lundberg & Lee, 2017)

