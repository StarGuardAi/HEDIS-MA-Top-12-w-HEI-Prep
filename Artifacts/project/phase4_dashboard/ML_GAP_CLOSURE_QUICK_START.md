# ML Gap Closure Predictions - Quick Start

## 🚀 Get Started in 3 Steps

### 1. Install ML Dependencies
```bash
pip install xgboost scikit-learn imbalanced-learn
```

### 2. Train Model (Optional)
```bash
python utils/ml_model_training.py --model-type xgboost --n-samples 10000
```

### 3. Use Predictions
Navigate to **🤖 ML Gap Closure Predictions** in the sidebar

## 🤖 Key Features

### Model Features
- **Member Characteristics**: Age, risk score, compliance history
- **Clinical Factors**: Measure type, gap severity, PCP quality
- **Engagement Factors**: Portal usage, response rate, no-show history
- **Operational Factors**: Coordinator workload, intervention type, deadline

### Model Output
- Closure probability (0-100%)
- Confidence interval
- Key influencing factors
- Recommended intervention type
- Estimated time to close

### Dashboard
- Model performance metrics
- Feature importance visualization
- Prediction distribution
- Success rate by probability bucket
- ROI analysis

## 💡 Usage

### Real-Time Prediction
1. Go to ML Gap Closure Predictions page
2. Enter member and gap information
3. Click "Predict Closure Likelihood"
4. View probability and recommendations

### Batch Predictions
```python
from utils.ml_prediction_service import GapClosurePredictionService

service = GapClosurePredictionService()
predictions = service.predict_batch(gaps, member_data, engagement_data, operational_data)
```

### Integration
- Automatically used in gap workflow
- Shows predictions on mobile coordinator app
- Prioritizes high-probability gaps

## 📱 Mobile

### Member Cards
- Prediction score displayed
- Color-coded badges:
  - 🟢 High (≥75%)
  - 🟡 Medium (50-74%)
  - 🟠 Low (<50%)

### Recommendations
- Intervention type
- Estimated days to close
- Key factors

## 🎯 Best Practices

1. **Train Regularly**: Monthly retraining with new data
2. **Monitor Performance**: Track metrics continuously
3. **Detect Drift**: Watch for feature distribution changes
4. **Calibrate**: Ensure probabilities match actual rates
5. **A/B Test**: Test model improvements

## 📚 More Information

See `ML_GAP_CLOSURE_GUIDE.md` for:
- Detailed feature descriptions
- Training procedures
- Model monitoring
- Troubleshooting guide

## Support

For questions or issues:
- 📧 **Email**: reichert.starguardai@gmail.com
- 🔗 **LinkedIn**: [sentinel-analytics](https://www.linkedin.com/in/sentinel-analytics/)
- 💻 **GitHub**: [HEDIS-MA-Top-12-w-HEI-Prep](https://github.com/StarGuardAi/HEDIS-MA-Top-12-w-HEI-Prep/blob/main/README.md)
- 🎨 **Portfolio**: [Canva Portfolio](https://www.canva.com/design/DAG2WzhiLwM/N_iXUe3eEKL3dzQ2M_0PgQ/edit)

---

**Ready to predict?** Open the ML Gap Closure Predictions page!

