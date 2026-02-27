"""
Application configuration and constants
"""
from typing import Dict, Any

# Application Settings
APP_CONFIG: Dict[str, Any] = {
    'app_title': 'StarGuard AI - HEDIS Portfolio Optimizer',
    'page_icon': '⭐',
    'layout': 'wide',
    'initial_sidebar_state': 'auto'  # Auto: Let Streamlit decide based on screen size (iOS Safari optimized)
}

# Data Settings
DATA_CONFIG: Dict[str, Any] = {
    'cache_ttl': 3600,  # 1 hour
    'max_rows': 10000,
    'date_format': '%Y-%m-%d'
}

# Model Settings
MODEL_CONFIG: Dict[str, Any] = {
    'prediction_threshold': 0.5,
    'confidence_level': 0.95
}

# UI Settings
UI_CONFIG: Dict[str, Any] = {
    'colors': {
        'primary': '#0066cc',
        'secondary': '#00cc66',
        'danger': '#cc0000',
        'warning': '#ffaa00'
    },
    'chart_height': {
        'desktop': 600,
        'tablet': 400,
        'mobile': 300
    }
}

# HEDIS Measure Definitions
HEDIS_MEASURES: Dict[str, Dict[str, Any]] = {
    'HbA1c_Testing': {
        'name': 'HbA1c Testing',
        'category': 'Diabetes',
        'star_weight': 3.0,
        'description': 'Percentage of members with diabetes who had HbA1c testing'
    },
    'BP_Control': {
        'name': 'Blood Pressure Control',
        'category': 'Cardiovascular',
        'star_weight': 3.0,
        'description': 'Percentage of members with controlled blood pressure'
    },
    'Breast_Cancer_Screening': {
        'name': 'Breast Cancer Screening',
        'category': 'Cancer',
        'star_weight': 2.0,
        'description': 'Percentage of women who received breast cancer screening'
    },
    'Colorectal_Cancer_Screening': {
        'name': 'Colorectal Cancer Screening',
        'category': 'Cancer',
        'star_weight': 2.0,
        'description': 'Percentage of members who received colorectal cancer screening'
    },
    'Statin_Therapy_CVD': {
        'name': 'Statin Therapy - Cardiovascular Disease',
        'category': 'Cardiovascular',
        'star_weight': 2.0,
        'description': 'Percentage of members with cardiovascular disease on statin therapy'
    },
    'Statin_Therapy_Diabetes': {
        'name': 'Statin Therapy - Diabetes',
        'category': 'Diabetes',
        'star_weight': 2.0,
        'description': 'Percentage of members with diabetes on statin therapy'
    },
    'Eye_Exam': {
        'name': 'Diabetes Care - Eye Exam',
        'category': 'Diabetes',
        'star_weight': 2.0,
        'description': 'Percentage of members with diabetes who received eye exam'
    },
    'Nephropathy_Screening': {
        'name': 'Diabetes Care - Nephropathy Screening',
        'category': 'Diabetes',
        'star_weight': 2.0,
        'description': 'Percentage of members with diabetes who received nephropathy screening'
    },
    'Flu_Vaccination': {
        'name': 'Annual Flu Vaccine',
        'category': 'Prevention',
        'star_weight': 1.0,
        'description': 'Percentage of members who received flu vaccination'
    },
    'Pneumonia_Vaccination': {
        'name': 'Pneumonia Vaccination',
        'category': 'Prevention',
        'star_weight': 1.0,
        'description': 'Percentage of members who received pneumonia vaccination'
    },
    'Depression_Screening': {
        'name': 'Depression Screening',
        'category': 'Behavioral Health',
        'star_weight': 1.0,
        'description': 'Percentage of members who received depression screening'
    },
    'Falls_Risk_Assessment': {
        'name': 'Falls Risk Assessment',
        'category': 'Safety',
        'star_weight': 1.0,
        'description': 'Percentage of members who received falls risk assessment'
    }
}

