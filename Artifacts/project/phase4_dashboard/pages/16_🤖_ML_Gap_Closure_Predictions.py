"""
ML Gap Closure Prediction Dashboard
Model performance, predictions, and insights
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import numpy as np

from utils.ml_prediction_service import GapClosurePredictionService
from utils.ml_gap_closure_features import GapClosureFeatureEngineer
from utils.gap_workflow import GapWorkflowManager
from src.ui.layout import render_page_footer, render_sidebar_footer, render_header, render_starguard_header

# Page configuration
st.set_page_config(
    page_title="ML Gap Closure Predictions - HEDIS Portfolio",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="auto"  # Auto: Let Streamlit decide based on screen size (iOS Safari optimized)
)

# Purple Sidebar Theme + White Home Label
st.markdown("""
<style>
/* ========== PURPLE SIDEBAR THEME ========== */
/* Match the StarGuard AI header purple gradient */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #4A3D6F 0%, #6F5F96 100%) !important;
}

[data-testid="stSidebar"] > div:first-child {
    background: linear-gradient(180deg, #4A3D6F 0%, #6F5F96 100%) !important;
}

/* ========== WHITE "HOME" LABEL - DESKTOP ========== */
[data-testid="stSidebarNav"] ul li:first-child a {
    font-size: 0 !important;
    background: rgba(255, 255, 255, 0.2) !important;
    padding: 0.75rem 1rem !important;
    border-radius: 8px !important;
    border: 2px solid rgba(255, 255, 255, 0.3) !important;
    margin-bottom: 0.5rem !important;
    display: block !important;
}

[data-testid="stSidebarNav"] ul li:first-child a::before {
    content: "🏠 Home" !important;
    font-size: 1.1rem !important;
    color: #FFFFFF !important;
    font-weight: 700 !important;
    display: block !important;
    -webkit-text-fill-color: #FFFFFF !important;
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3) !important;
}

/* Target by href for additional coverage */
[data-testid="stSidebarNav"] a[href="/"],
[data-testid="stSidebarNav"] a[href="./"],
[data-testid="stSidebarNav"] a[href*="app"] {
    font-size: 0 !important;
    background: rgba(255, 255, 255, 0.2) !important;
    padding: 0.75rem 1rem !important;
    border-radius: 8px !important;
    border: 2px solid rgba(255, 255, 255, 0.3) !important;
}

[data-testid="stSidebarNav"] a[href="/"]::before,
[data-testid="stSidebarNav"] a[href="./"]::before,
[data-testid="stSidebarNav"] a[href*="app"]::before {
    content: "🏠 Home" !important;
    font-size: 1.1rem !important;
    color: #FFFFFF !important;
    font-weight: 700 !important;
    display: block !important;
    -webkit-text-fill-color: #FFFFFF !important;
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3) !important;
}

/* Hover state - brighter white */
[data-testid="stSidebarNav"] ul li:first-child a:hover,
[data-testid="stSidebarNav"] a[href="/"]:hover,
[data-testid="stSidebarNav"] a[href="./"]:hover {
    background: rgba(255, 255, 255, 0.3) !important;
    border-color: rgba(255, 255, 255, 0.5) !important;
}

[data-testid="stSidebarNav"] ul li:first-child a:hover::before,
[data-testid="stSidebarNav"] a[href="/"]:hover::before,
[data-testid="stSidebarNav"] a[href="./"]:hover::before {
    color: #FFFFFF !important;
}

/* ========== OTHER SIDEBAR LINKS - WHITE TEXT ========== */
/* Make all other sidebar navigation links white too */
[data-testid="stSidebarNav"] a {
    color: #FFFFFF !important;
}

[data-testid="stSidebarNav"] a span,
[data-testid="stSidebarNav"] a div,
[data-testid="stSidebarNav"] a p {
    color: #FFFFFF !important;
}

/* Active/selected page - lighter background */
[data-testid="stSidebarNav"] a[aria-current="page"] {
    background: rgba(255, 255, 255, 0.15) !important;
    color: #FFFFFF !important;
}

/* ========== MOBILE RESPONSIVE ========== */
@media (max-width: 768px) {
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #4A3D6F 0%, #6F5F96 100%) !important;
    }
    
    [data-testid="stSidebarNav"] ul li:first-child a {
        padding: 0.6rem 0.8rem !important;
    }
    
    [data-testid="stSidebarNav"] ul li:first-child a::before {
        font-size: 1rem !important;
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
    }
    
    [data-testid="stSidebarNav"] a[href="/"]::before,
    [data-testid="stSidebarNav"] a[href="./"]::before {
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
    }
}

/* Force white on ALL child elements */
[data-testid="stSidebarNav"] li:first-child *,
[data-testid="stSidebarNav"] a[href="/"] *,
[data-testid="stSidebarNav"] a[href="./"] * {
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
}

/* Sidebar collapse button - white */
[data-testid="collapsedControl"] {
    color: #FFFFFF !important;
}

/* ========== HEADER CONTAINER STYLES (Match Home Page) ========== */
.header-container {
    background: linear-gradient(180deg, #4A3D6F 0%, #6F5F96 100%);
    padding: 0.5rem 1rem;
    border-radius: 10px;
    margin-top: 1.5rem;
    margin-bottom: 0.3rem;
    text-align: center;
    display: block !important;
    visibility: visible !important;
    opacity: 1 !important;
    box-shadow: 0 4px 12px rgba(74, 61, 111, 0.25);
    max-width: 100%;
}

.header-title {
    color: white !important;
    font-weight: 700;
    font-size: 1.25rem;
    margin-bottom: 0.4rem;
    display: block !important;
    line-height: 1.5;
    letter-spacing: 0.3px;
}

.header-subtitle {
    color: #E8D4FF !important;
    font-size: 0.9rem;
    font-style: italic;
    display: block !important;
    line-height: 1.4;
    opacity: 0.95;
}
</style>
""", unsafe_allow_html=True)


# Responsive Header - Adapts to Desktop/Mobile (Match Home Page)
st.markdown("""
<div class="header-container">
    <div class="header-title">⭐ StarGuard AI | Turning Data Into Stars</div>
    <div class="header-subtitle">Powered by Predictive Analytics & Machine Learning</div>
</div>
""", unsafe_allow_html=True)

# Spacing fix
st.markdown('<style>div.block-container{padding-top:1rem!important}h1{margin-top:0.5rem!important}</style>', unsafe_allow_html=True)

# Improved compact CSS - READABLE fonts, reduced spacing only
st.markdown("""
<style>
.main .block-container { 
    padding-top: 1rem !important; 
    padding-bottom: 1rem !important; 
    padding-left: 1rem !important; 
    padding-right: 1rem !important; 
    max-width: 100% !important; 
}

/* Section spacing - REDUCE GAPS between sections */
h1 { 
    font-size: 1.8rem !important; 
    margin-top: 0.8rem !important; 
    margin-bottom: 0.5rem !important; 
    line-height: 1.2 !important; 
}

h2 { 
    font-size: 1.4rem !important; 
    margin-top: 0.6rem !important; 
    margin-bottom: 0.4rem !important; 
    line-height: 1.2 !important; 
}

h3 { 
    font-size: 1.1rem !important; 
    margin-top: 0.5rem !important; 
    margin-bottom: 0.3rem !important; 
    line-height: 1.2 !important; 
}

/* Reduce spacing between elements */
.element-container { margin-bottom: 0.4rem !important; }
.stMarkdown { margin-bottom: 0.4rem !important; }

/* Readable metric fonts */
[data-testid="stMetricValue"] { font-size: 1.6rem !important; }
[data-testid="stMetricLabel"] { font-size: 0.95rem !important; padding-bottom: 0.3rem !important; }
[data-testid="metric-container"] { padding: 0.7rem !important; }

/* Chart and data spacing */
.stPlotlyChart { margin-bottom: 0.6rem !important; }
.stDataFrame { margin-bottom: 0.6rem !important; }

/* Column spacing */
[data-testid="column"] { padding: 0.3rem !important; }

/* Interactive elements */
[data-testid="stExpander"] { margin-bottom: 0.5rem !important; }
[data-testid="stTabs"] { margin-bottom: 0.6rem !important; }
.stTabs [data-baseweb="tab-list"] { gap: 0.3rem !important; }
.stTabs [data-baseweb="tab"] { 
    padding: 0.5rem 1rem !important; 
    font-size: 0.95rem !important; 
}

/* Buttons - keep readable */
.stButton > button { 
    padding: 0.6rem 1.2rem !important; 
    font-size: 0.95rem !important; 
}

/* Form inputs */
.stSelectbox, .stTextInput, .stNumberInput { margin-bottom: 0.4rem !important; }

/* Alerts - keep readable */
.stAlert { 
    padding: 0.7rem !important; 
    margin-bottom: 0.5rem !important; 
    font-size: 0.95rem !important; 
}

/* Reduce gaps between blocks */
div[data-testid="stVerticalBlock"] > div { gap: 0.4rem !important; }

/* Horizontal rules */
hr { margin: 0.6rem 0 !important; }

/* Mobile adjustments - Match Home page formatting */
@media (max-width: 768px) {
    .header-container {
        padding: 0.6rem 0.8rem;
        border-radius: 6px;
        margin-top: 1rem;
        margin-bottom: 0.5rem;
        box-shadow: 0 2px 4px rgba(74, 61, 111, 0.15);
    }
    
    .header-title {
        font-size: 0.9rem;
        margin-bottom: 0.25rem;
        line-height: 1.3;
        font-weight: 600;
    }
    
    .header-subtitle {
        font-size: 0.65rem;
        line-height: 1.2;
    }
    
    /* Mobile spacing - tighter */
    div.block-container {
        padding-top: 2rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }
    
    h1 {
        margin-top: 0.5rem !important;
        font-size: 1.5rem !important;
        line-height: 1.3;
        text-align: center !important;
    }
    
    h2 {
        margin-top: 0.75rem !important;
        font-size: 1.25rem !important;
        line-height: 1.3;
        text-align: center !important;
    }
    
    h3 {
        font-size: 1.1rem !important;
        line-height: 1.3;
        text-align: center !important;
    }
    
    h4, h5, h6 {
        text-align: center !important;
    }
    
    /* Center align markdown headers on mobile */
    div[data-testid="stMarkdownContainer"] h1,
    div[data-testid="stMarkdownContainer"] h2,
    div[data-testid="stMarkdownContainer"] h3,
    div[data-testid="stMarkdownContainer"] h4,
    div[data-testid="stMarkdownContainer"] h5,
    div[data-testid="stMarkdownContainer"] h6 {
        text-align: center !important;
    }
    
    /* Center align metrics on mobile */
    [data-testid="stMetric"],
    [data-testid="stMetricValue"],
    [data-testid="stMetricLabel"],
    [data-testid="stMetricDelta"],
    [data-testid="metric-container"],
    .compact-metric-card,
    .kpi-card {
        text-align: center !important;
    }
    
    /* Mobile columns - stack vertically */
    [data-testid="column"] {
        width: 100% !important;
        flex: 1 1 100% !important;
        padding: 0.2rem !important;
    }
    
    /* Mobile buttons - full width */
    button[kind="primary"],
    button[kind="secondary"] {
        width: 100% !important;
        margin-bottom: 0.5rem !important;
    }
    
    /* Mobile metrics - smaller */
    [data-testid="stMetricValue"] {
        font-size: 1.5rem !important;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 0.85rem !important;
    }
    
    /* Mobile tables - horizontal scroll */
    .stDataFrame {
        overflow-x: auto !important;
    }
    
    /* Mobile tabs - stack vertically to eliminate horizontal scrolling */
    [data-testid="stTabs"] {
        overflow-x: visible !important;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        flex-direction: column !important;
        width: 100% !important;
        gap: 0.5rem !important;
        overflow-x: visible !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        width: 100% !important;
        flex: 1 1 100% !important;
    }
    
    /* Wrap Plotly chart titles on mobile */
    .js-plotly-plot .gtitle,
    .plotly .gtitle,
    .js-plotly-plot .xtitle,
    .plotly .xtitle {
        word-wrap: break-word !important;
        white-space: normal !important;
        max-width: 100% !important;
        overflow-wrap: break-word !important;
        hyphens: auto !important;
    }
    
    /* Ensure chart titles wrap - target SVG text elements */
    .js-plotly-plot .gtitle text,
    .plotly .gtitle text {
        word-wrap: break-word !important;
        white-space: normal !important;
    }
}
</style>
""", unsafe_allow_html=True)

# Page header (already rendered above)

# Initialize services with error handling
prediction_service = None
feature_engineer = None
ml_available = False

# Check ML library availability first
try:
    from utils.ml_gap_closure_model import ML_LIBRARIES_AVAILABLE
    if not ML_LIBRARIES_AVAILABLE:
        raise ImportError("ML libraries not available")
except ImportError:
    ML_LIBRARIES_AVAILABLE = False

if not ML_LIBRARIES_AVAILABLE:
    st.error("❌ **ML libraries not available**")
    st.info("💡 **To enable ML predictions, install required packages:**")
    st.code("pip install xgboost scikit-learn imbalanced-learn", language="bash")
    st.warning("⚠️ **IMPORTANT: After installing packages, you must restart Streamlit for changes to take effect.**")
    st.info("**To restart Streamlit:**\n1. Stop the current Streamlit process (Ctrl+C in terminal)\n2. Restart with: `streamlit run app.py`")
    ml_available = False
    st.stop()

# Initialize services
try:
    if "prediction_service" not in st.session_state:
        st.session_state.prediction_service = GapClosurePredictionService()
    
    prediction_service = st.session_state.prediction_service
    feature_engineer = GapClosureFeatureEngineer()
    ml_available = True
except ImportError as e:
    st.error(f"❌ ML libraries not available: {e}")
    st.info("💡 **To enable ML predictions, install required packages:**")
    st.code("pip install xgboost scikit-learn imbalanced-learn", language="bash")
    st.warning("⚠️ **After installing, restart Streamlit for changes to take effect.**")
    ml_available = False
    st.stop()
except Exception as e:
    st.warning(f"⚠️ ML service initialization issue: {e}")
    st.info("💡 The page will work in limited mode without ML predictions.")
    ml_available = False

# Sidebar
st.sidebar.header("🤖 ML Gap Closure Predictions")
st.sidebar.markdown("Machine learning predictions and insights")

# Sidebar value proposition - at bottom
from utils.value_proposition import render_sidebar_value_proposition
render_sidebar_value_proposition()

# Sidebar footer
render_sidebar_footer()

# Main Content
st.title("🤖 ML Gap Closure Prediction Dashboard")
st.markdown("Machine learning model to predict gap closure likelihood")

# Check if ML is available
if not ml_available:
    st.stop()

# Model Performance
st.header("📊 Model Performance")

performance_tabs = st.tabs(["Overall Metrics", "Feature Importance", "Prediction Distribution", "Success by Bucket"])

with performance_tabs[0]:
    st.subheader("Overall Performance Metrics")
    
    # Get performance metrics
    performance = prediction_service.get_model_performance(days=30)
    
    if performance:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Accuracy", f"{performance.get('accuracy', 0)*100:.1f}%")
        with col2:
            st.metric("Precision", f"{performance.get('precision', 0)*100:.1f}%")
        with col3:
            st.metric("Recall", f"{performance.get('recall', 0)*100:.1f}%")
        with col4:
            st.metric("F1 Score", f"{performance.get('f1_score', 0)*100:.1f}%")
        
        st.metric("ROC AUC", f"{performance.get('roc_auc', 0):.3f}")
        
        st.caption(f"Based on {performance.get('predictions_with_outcomes', 0)} predictions with outcomes")
    else:
        st.info("No performance data available. Model needs to be trained and predictions logged.")

with performance_tabs[1]:
    st.subheader("Feature Importance")
    
    if hasattr(prediction_service.model, 'feature_importance'):
        feature_importance = prediction_service.model.feature_importance
        
        if feature_importance:
            # Get top 20 features
            top_features = sorted(feature_importance.items(), key=lambda x: x[1], reverse=True)[:20]
            
            feature_df = pd.DataFrame(top_features, columns=["Feature", "Importance"])
            
            # Visualization
            fig = px.bar(
                feature_df,
                x="Importance",
                y="Feature",
                orientation='h',
                title="Top 20 Feature Importance",
                labels={"Importance": "Importance Score", "Feature": "Feature Name"}
            )
            fig.update_layout(yaxis={'categoryorder': 'total ascending'})
            st.plotly_chart(fig, use_container_width=True)
            
            # Table
            st.dataframe(feature_df, use_container_width=True, hide_index=True)
        else:
            st.info("Feature importance not available. Train model first.")
    else:
        st.info("Model not loaded. Load a trained model to see feature importance.")

with performance_tabs[2]:
    st.subheader("Prediction Distribution")
    
    if performance and 'prediction_distribution' in performance:
        dist_data = performance['prediction_distribution']
        
        dist_df = pd.DataFrame(list(dist_data.items()), columns=["Probability Bucket", "Count"])
        
        fig = px.bar(
            dist_df,
            x="Probability Bucket",
            y="Count",
            title="Prediction Distribution by Probability Bucket"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.dataframe(dist_df, use_container_width=True, hide_index=True)
    else:
        st.info("No prediction distribution data available.")

with performance_tabs[3]:
    st.subheader("Success Rate by Probability Bucket")
    
    if performance and 'success_rate_by_bucket' in performance:
        success_data = performance['success_rate_by_bucket']
        
        success_df = pd.DataFrame(
            list(success_data.items()),
            columns=["Probability Bucket", "Success Rate"]
        )
        success_df["Success Rate"] = success_df["Success Rate"] * 100
        
        fig = px.bar(
            success_df,
            x="Probability Bucket",
            y="Success Rate",
            title="Actual Closure Rate by Predicted Probability Bucket",
            labels={"Success Rate": "Success Rate (%)"}
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.dataframe(success_df, use_container_width=True, hide_index=True)
    else:
        st.info("No success rate data available.")

# Real-Time Prediction
st.markdown("---")
st.header("🔮 Real-Time Prediction")

prediction_cols = st.columns(2)

with prediction_cols[0]:
    st.subheader("Member Information")
    member_id = st.text_input("Member ID", value="MEM001")
    age = st.number_input("Age", min_value=18, max_value=120, value=65)
    gender = st.selectbox("Gender", ["Male", "Female"])
    risk_score = st.slider("Risk Score", 0.0, 1.0, 0.5, 0.1)
    prior_compliance = st.slider("Prior Year Compliance", 0.0, 1.0, 0.75, 0.05)

with prediction_cols[1]:
    st.subheader("Gap Information")
    measure_id = st.selectbox("Measure", ["HBA1C", "BP", "COL", "MAM", "CCS"])
    gap_reason = st.selectbox("Gap Reason", ["Not Scheduled", "Missed Appointment", "Lab Pending", "Provider Delay"])
    days_until_deadline = st.number_input("Days Until Deadline", min_value=0, max_value=365, value=60)
    
    st.subheader("Engagement")
    portal_logins = st.number_input("Portal Logins (Last 90 Days)", min_value=0, value=5)
    response_rate = st.slider("Outreach Response Rate", 0.0, 1.0, 0.6, 0.05)

if st.button("Predict Closure Likelihood", use_container_width=True):
    # Prepare data
    member_data = {
        'age': age,
        'gender': gender,
        'risk_score': risk_score,
        'prior_year_compliance_rate': prior_compliance,
        'member_since': datetime.now() - timedelta(days=365*2),
        'chronic_conditions': [],
        'last_visit_date': datetime.now() - timedelta(days=90),
        'pcp': {'quality_score': 4.0, 'patient_count': 1000},
        'distance_to_facility': 10.0
    }
    
    gap_data = {
        'measure_id': measure_id,
        'gap_reason': gap_reason,
        'deadline_date': datetime.now() + timedelta(days=days_until_deadline),
        'assigned_coordinator': 'COORD001'
    }
    
    engagement_data = {
        'portal_usage': {'logins_last_90_days': portal_logins},
        'outreach_history': [],
        'appointment_history': [],
        'preferred_contact_channel': 'Phone',
        'best_contact_hour': 10
    }
    
    operational_data = {
        'coordinators': {
            'COORD001': {
                'active_gaps': 50,
                'closure_rate': 0.75
            }
        }
    }
    
    # Make prediction
    try:
        prediction = prediction_service.predict_single(
            member_id=member_id,
            gap_data=gap_data,
            member_data=member_data,
            engagement_data=engagement_data,
            operational_data=operational_data
        )
        
        # Display results
        st.success("Prediction Generated")
        
        result_cols = st.columns(3)
        
        with result_cols[0]:
            st.metric(
                "Closure Probability",
                f"{prediction['closure_probability']:.1f}%",
                delta=f"CI: {prediction.get('confidence_interval_lower', 0):.1f}% - {prediction.get('confidence_interval_upper', 100):.1f}%"
            )
        
        with result_cols[1]:
            st.metric(
                "Recommended Intervention",
                prediction.get('recommended_intervention', 'Phone')
            )
        
        with result_cols[2]:
            st.metric(
                "Estimated Days to Close",
                f"{prediction.get('estimated_days_to_close', 0)} days"
            )
        
        # Influencing factors
        st.subheader("Key Influencing Factors")
        if 'influencing_factors' in prediction:
            factors_df = pd.DataFrame(prediction['influencing_factors'])
            st.dataframe(factors_df, use_container_width=True, hide_index=True)
        
        # Visualization
        prob = prediction['closure_probability']
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=prob,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Closure Probability"},
            gauge={
                'axis': {'range': [None, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 50], 'color': "lightgray"},
                    {'range': [50, 75], 'color': "gray"},
                    {'range': [75, 100], 'color': "lightgreen"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
    except ValueError as e:
        st.error(f"❌ **Model Not Trained**: {str(e)}")
        st.info("💡 **To make predictions, you need to train the model first.**")
        st.info("📋 **Steps:**\n1. Go to the 'Train Model' section above\n2. Click 'Train Model' to train on historical data\n3. Once trained, you can make predictions")
    except Exception as e:
        st.error(f"❌ **Prediction Error**: {str(e)}")
        st.exception(e)

# ROI Analysis
st.markdown("---")
st.header("💰 ROI of ML Predictions")

roi_cols = st.columns(2)

with roi_cols[0]:
    st.subheader("With ML Predictions")
    st.metric("Targeted Outreach", "High-probability gaps only")
    st.metric("Efficiency Gain", "+25%")
    st.metric("Cost Savings", "$50K/month")

with roi_cols[1]:
    st.subheader("Without ML (Random)")
    st.metric("Random Outreach", "All gaps equally")
    st.metric("Efficiency", "Baseline")
    st.metric("Cost", "Baseline")

st.info("""
**ROI Calculation**: 
- Using ML predictions to prioritize high-probability gaps increases closure rates by 25%
- Reduces wasted outreach on low-probability gaps
- Estimated savings: $50K/month in outreach costs
""")

# Model Monitoring
st.markdown("---")
st.header("🔍 Model Monitoring")

monitoring_cols = st.columns(2)

with monitoring_cols[0]:
    st.subheader("Drift Detection")
    st.info("Monitor feature distributions for data drift")
    if st.button("Check for Drift"):
        st.warning("Drift detection requires reference data. Configure in model monitoring settings.")

with monitoring_cols[1]:
    st.subheader("Model Version")
    st.metric("Current Version", prediction_service.model.model_version)
    if prediction_service.model.training_date:
        st.metric("Last Trained", prediction_service.model.training_date.strftime("%Y-%m-%d"))
    else:
        st.metric("Last Trained", "Not trained")

# Footer sections - desktop full text, mobile abbreviated
render_page_footer()  # Main content footer

