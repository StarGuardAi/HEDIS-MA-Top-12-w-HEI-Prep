"""
Advanced Filtering System for HEDIS Portfolio Optimizer
Enterprise-grade sidebar filters with preset management
"""
import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta
from typing import Dict, List, Optional, Tuple, Any
import json


# ============================================================================
# FILTER STATE INITIALIZATION
# ============================================================================

def init_filter_state():
    """Initialize filter state in session_state with defaults"""
    if 'filters' not in st.session_state:
        st.session_state.filters = {
            # Time Period
            'time_preset': 'Current Quarter',
            'start_date': date.today().replace(month=1, day=1) if date.today().month <= 3 else date.today().replace(month=4, day=1),
            'end_date': date.today(),
            'compare_previous': False,
            
            # Measures & Metrics
            'measures': [],
            'gap_status': ['Open', 'Pending'],
            'prediction_confidence': ['High', 'Medium', 'Low'],
            'star_rating_impact': [],
            
            # Demographics
            'age_bands': [],
            'gender': 'All',
            'risk_score_min': 0.0,
            'risk_score_max': 10.0,
            'member_tenure': 'All',
            
            # Financial Thresholds
            'min_member_count': 0,
            'min_financial_impact': 0.0,
            'min_closure_rate': 0.0,
            'max_budget_cap': None,
            
            # Advanced Options
            'high_confidence_only': False,
            'include_historical': True,
            'exclude_recent_contact': False,
            'min_data_quality': 0.0,
            
            # Provider & Geographic
            'provider_networks': [],
            'geographic_regions': [],
            'counties': [],
            'zip_codes': []
        }
    
    # Initialize presets
    if 'filter_presets' not in st.session_state:
        st.session_state.filter_presets = {
            'Executive Summary': {
                'time_preset': 'Current Quarter',
                'measures': [],
                'gap_status': ['Open'],
                'min_financial_impact': 1000.0,
                'high_confidence_only': True,
                'created_date': datetime.now().isoformat(),
                'description': 'High-level view for executive reporting'
            },
            'Care Coordinator View': {
                'time_preset': 'Last 90 Days',
                'gap_status': ['Open', 'Pending'],
                'min_member_count': 10,
                'exclude_recent_contact': True,
                'created_date': datetime.now().isoformat(),
                'description': 'Actionable list for care coordinators'
            },
            'Financial Focus': {
                'time_preset': 'Year to Date',
                'min_financial_impact': 5000.0,
                'min_closure_rate': 30.0,
                'prediction_confidence': ['High', 'Medium'],
                'created_date': datetime.now().isoformat(),
                'description': 'Focus on high-value opportunities'
            }
        }
    
    # Initialize filter metadata
    if 'filter_metadata' not in st.session_state:
        st.session_state.filter_metadata = {
            'last_applied': None,
            'active_count': 0,
            'last_preset_loaded': None
        }


# ============================================================================
# TIME PERIOD FILTERS
# ============================================================================

def render_time_period_filters():
    """Render time period filter section"""
    with st.expander("📅 Time Period", expanded=True):
        # Preset selection
        time_presets = {
            'Current Quarter': get_current_quarter(),
            'Last 90 Days': (date.today() - timedelta(days=90), date.today()),
            'Year to Date': (date.today().replace(month=1, day=1), date.today()),
            'Last Quarter': get_last_quarter(),
            'Last 12 Months': (date.today() - timedelta(days=365), date.today()),
            'Custom': None
        }
        
        selected_preset = st.radio(
            "Period Preset:",
            options=list(time_presets.keys()),
            index=list(time_presets.keys()).index(st.session_state.filters['time_preset']),
            key='time_preset_radio'
        )
        
        st.session_state.filters['time_preset'] = selected_preset
        
        # Date range based on preset
        if selected_preset == 'Custom':
            date_range = st.date_input(
                "Select Date Range:",
                value=(
                    st.session_state.filters['start_date'],
                    st.session_state.filters['end_date']
                ),
                key='custom_date_range'
            )
            
            if len(date_range) == 2:
                st.session_state.filters['start_date'] = date_range[0]
                st.session_state.filters['end_date'] = date_range[1]
        else:
            start, end = time_presets[selected_preset]
            st.session_state.filters['start_date'] = start
            st.session_state.filters['end_date'] = end
            
            # Display period summary
            days = (end - start).days
            st.info(f"📆 **{selected_preset}**: {start.strftime('%b %d, %Y')} to {end.strftime('%b %d, %Y')} ({days} days)")
        
        # Compare to previous period
        st.session_state.filters['compare_previous'] = st.checkbox(
            "📊 Compare to Previous Period",
            value=st.session_state.filters['compare_previous'],
            help="Enable to show comparison metrics with previous period"
        )


def get_current_quarter() -> Tuple[date, date]:
    """Get current quarter date range"""
    today = date.today()
    quarter = (today.month - 1) // 3
    start_month = quarter * 3 + 1
    start = date(today.year, start_month, 1)
    
    if quarter == 3:
        end = date(today.year, 12, 31)
    else:
        end = date(today.year, start_month + 3, 1) - timedelta(days=1)
    
    return start, end


def get_last_quarter() -> Tuple[date, date]:
    """Get last quarter date range"""
    today = date.today()
    quarter = (today.month - 1) // 3
    if quarter == 0:
        start = date(today.year - 1, 10, 1)
        end = date(today.year - 1, 12, 31)
    else:
        start_month = (quarter - 1) * 3 + 1
        start = date(today.year, start_month, 1)
        end = date(today.year, start_month + 3, 1) - timedelta(days=1)
    
    return start, end


# ============================================================================
# MEASURES & METRICS FILTERS
# ============================================================================

def render_measures_filters(available_measures: List[str]):
    """Render measures and metrics filter section"""
    with st.expander("📊 Measures & Metrics", expanded=True):
        # Quick presets
        preset_col1, preset_col2, preset_col3 = st.columns(3, gap="small")
        
        with preset_col1:
            if st.button("🎯 Top 5 by ROI", use_container_width=True, help="Select top 5 measures by ROI"):
                # This would need actual ROI data - placeholder
                st.session_state.filters['measures'] = available_measures[:5] if len(available_measures) >= 5 else available_measures
        
        with preset_col2:
            if st.button("🩺 All Diabetes", use_container_width=True, help="Select all diabetes-related measures"):
                diabetes_measures = [m for m in available_measures if 'diabetes' in m.lower() or 'hba1c' in m.lower()]
                st.session_state.filters['measures'] = diabetes_measures
        
        with preset_col3:
            if st.button("⭐ Star Critical", use_container_width=True, help="Select measures critical for star rating"):
                # Placeholder - would filter by star_rating_impact
                st.session_state.filters['measures'] = available_measures[:3] if len(available_measures) >= 3 else available_measures
        
        st.markdown("---")
        
        # Multi-select with search
        selected_measures = st.multiselect(
            "Select HEDIS Measures:",
            options=available_measures,
            default=st.session_state.filters['measures'],
            key='measures_multiselect',
            help="Select one or more HEDIS measures to include in analysis"
        )
        st.session_state.filters['measures'] = selected_measures
        
        # Select All / Clear All
        select_col1, select_col2 = st.columns(2, gap="small")
        with select_col1:
            if st.button("✅ Select All", use_container_width=True):
                st.session_state.filters['measures'] = available_measures
                st.rerun()
        
        with select_col2:
            if st.button("❌ Clear All", use_container_width=True):
                st.session_state.filters['measures'] = []
                st.rerun()
        
        # Show count
        measure_count = len(st.session_state.filters['measures'])
        if measure_count > 0:
            st.success(f"✓ {measure_count} measure{'s' if measure_count != 1 else ''} selected")
        else:
            st.info("ℹ️ No measures selected - all measures will be included")
        
        st.markdown("---")
        
        # Gap Status
        gap_status_options = ['Open', 'Pending', 'Closed', 'Excluded']
        selected_status = st.multiselect(
            "Gap Status:",
            options=gap_status_options,
            default=st.session_state.filters['gap_status'],
            key='gap_status_multiselect',
            help="Filter by care gap status"
        )
        st.session_state.filters['gap_status'] = selected_status
        
        # Prediction Confidence
        confidence_options = ['High', 'Medium', 'Low']
        selected_confidence = st.multiselect(
            "Prediction Confidence:",
            options=confidence_options,
            default=st.session_state.filters['prediction_confidence'],
            key='confidence_multiselect',
            help="Filter by prediction confidence level"
        )
        st.session_state.filters['prediction_confidence'] = selected_confidence
        
        # Star Rating Impact (if available in data)
        star_impact_options = ['Critical', 'High', 'Medium', 'Low']
        selected_star_impact = st.multiselect(
            "Star Rating Impact:",
            options=star_impact_options,
            default=st.session_state.filters['star_rating_impact'],
            key='star_impact_multiselect',
            help="Filter by impact on CMS Star Rating"
        )
        st.session_state.filters['star_rating_impact'] = selected_star_impact


# ============================================================================
# DEMOGRAPHICS FILTERS
# ============================================================================

def render_demographics_filters():
    """Render member demographics filter section"""
    with st.expander("👥 Member Demographics", expanded=False):
        # Age Bands
        age_band_options = [
            '18-34', '35-44', '45-54', '55-64', 
            '65-74', '75-84', '85+'
        ]
        selected_age_bands = st.multiselect(
            "Age Bands:",
            options=age_band_options,
            default=st.session_state.filters['age_bands'],
            key='age_bands_multiselect',
            help="Select age ranges to include"
        )
        st.session_state.filters['age_bands'] = selected_age_bands
        
        # Gender
        gender_options = ['All', 'Male', 'Female', 'Other', 'Unknown']
        selected_gender = st.radio(
            "Gender:",
            options=gender_options,
            index=gender_options.index(st.session_state.filters['gender']) if st.session_state.filters['gender'] in gender_options else 0,
            key='gender_radio',
            help="Filter by member gender"
        )
        st.session_state.filters['gender'] = selected_gender
        
        # Risk Score Range
        st.markdown("**Risk Score Range:**")
        risk_range = st.slider(
            "Risk Score:",
            min_value=0.0,
            max_value=10.0,
            value=(
                st.session_state.filters['risk_score_min'],
                st.session_state.filters['risk_score_max']
            ),
            step=0.1,
            key='risk_score_slider',
            help="Filter by member risk score (0 = low risk, 10 = high risk)"
        )
        st.session_state.filters['risk_score_min'] = risk_range[0]
        st.session_state.filters['risk_score_max'] = risk_range[1]
        st.caption(f"Range: {risk_range[0]:.1f} - {risk_range[1]:.1f}")
        
        # Member Tenure
        tenure_options = ['All', 'New (< 1 year)', '1-2 years', '2+ years']
        selected_tenure = st.selectbox(
            "Member Tenure:",
            options=tenure_options,
            index=tenure_options.index(st.session_state.filters['member_tenure']) if st.session_state.filters['member_tenure'] in tenure_options else 0,
            key='tenure_selectbox',
            help="Filter by how long member has been enrolled"
        )
        st.session_state.filters['member_tenure'] = selected_tenure


# ============================================================================
# FINANCIAL THRESHOLDS
# ============================================================================

def render_financial_filters():
    """Render financial threshold filters"""
    with st.expander("💰 Financial Thresholds", expanded=False):
        # Min Member Count
        min_members = st.number_input(
            "Minimum Member Count:",
            min_value=0,
            max_value=100000,
            value=st.session_state.filters['min_member_count'],
            step=10,
            key='min_members_input',
            help="Exclude measures/groups with fewer than this many members"
        )
        st.session_state.filters['min_member_count'] = int(min_members)
        
        # Min Financial Impact
        min_impact = st.number_input(
            "Minimum Financial Impact ($):",
            min_value=0.0,
            max_value=1000000.0,
            value=float(st.session_state.filters['min_financial_impact']),
            step=100.0,
            format="%.2f",
            key='min_impact_input',
            help="Minimum total financial impact to include"
        )
        st.session_state.filters['min_financial_impact'] = min_impact
        
        # Min Predicted Closure Rate
        min_closure_rate = st.slider(
            "Minimum Predicted Closure Rate (%):",
            min_value=0.0,
            max_value=100.0,
            value=float(st.session_state.filters['min_closure_rate']),
            step=1.0,
            key='min_closure_slider',
            help="Minimum predicted closure rate percentage"
        )
        st.session_state.filters['min_closure_rate'] = min_closure_rate
        st.caption(f"Threshold: {min_closure_rate:.1f}%")
        
        # Budget Cap
        budget_cap = st.number_input(
            "Total Budget Cap ($):",
            min_value=0.0,
            value=float(st.session_state.filters['max_budget_cap']) if st.session_state.filters['max_budget_cap'] else 0.0,
            step=1000.0,
            format="%.2f",
            key='budget_cap_input',
            help="Maximum total budget for recommendations (leave 0 for no limit)"
        )
        st.session_state.filters['max_budget_cap'] = budget_cap if budget_cap > 0 else None


# ============================================================================
# ADVANCED OPTIONS
# ============================================================================

def render_advanced_filters():
    """Render advanced filter options"""
    with st.expander("⚙️ Advanced Options", expanded=False):
        # High Confidence Only
        st.session_state.filters['high_confidence_only'] = st.checkbox(
            "Show Only High Confidence Predictions",
            value=st.session_state.filters['high_confidence_only'],
            help="Filter to only include predictions with high confidence scores"
        )
        
        # Include Historical Data
        st.session_state.filters['include_historical'] = st.checkbox(
            "Include Historical Data",
            value=st.session_state.filters['include_historical'],
            help="Include historical/completed interventions in analysis"
        )
        
        # Exclude Recent Contact
        st.session_state.filters['exclude_recent_contact'] = st.checkbox(
            "Exclude Members with Recent Contact",
            value=st.session_state.filters['exclude_recent_contact'],
            help="Exclude members contacted within last 30 days"
        )
        
        # Min Data Quality Score
        min_quality = st.slider(
            "Minimum Data Quality Score:",
            min_value=0.0,
            max_value=100.0,
            value=float(st.session_state.filters['min_data_quality']),
            step=1.0,
            key='min_quality_slider',
            help="Filter by data completeness/quality score"
        )
        st.session_state.filters['min_data_quality'] = min_quality
        st.caption(f"Quality threshold: {min_quality:.0f}%")
        
        # Provider Networks (if available)
        provider_options = []  # Would be populated from data
        if provider_options:
            selected_providers = st.multiselect(
                "Provider Networks:",
                options=provider_options,
                default=st.session_state.filters['provider_networks'],
                key='providers_multiselect'
            )
            st.session_state.filters['provider_networks'] = selected_providers
        
        # Geographic Filters (if available)
        geographic_options = []  # Would be populated from data
        if geographic_options:
            selected_regions = st.multiselect(
                "Geographic Regions:",
                options=geographic_options,
                default=st.session_state.filters['geographic_regions'],
                key='regions_multiselect'
            )
            st.session_state.filters['geographic_regions'] = selected_regions


# ============================================================================
# FILTER PRESETS MANAGEMENT
# ============================================================================

def render_preset_management():
    """Render filter preset save/load interface"""
    with st.expander("💾 Filter Presets", expanded=False):
        # Load Preset
        preset_names = ['-- Select Preset --'] + list(st.session_state.filter_presets.keys())
        selected_preset_name = st.selectbox(
            "Load Preset:",
            options=preset_names,
            key='preset_selectbox',
            help="Load a saved filter configuration"
        )
        
        if selected_preset_name != '-- Select Preset --':
            if st.button("📂 Load Preset", use_container_width=True):
                load_preset(selected_preset_name)
                st.success(f"✓ Loaded preset: {selected_preset_name}")
                st.rerun()
        
        st.markdown("---")
        
        # Save Current Preset
        preset_name = st.text_input(
            "Preset Name:",
            key='preset_name_input',
            help="Enter a name for the current filter configuration"
        )
        
        col1, col2 = st.columns(2, gap="small")
        with col1:
            if st.button("💾 Save Preset", use_container_width=True, disabled=not preset_name):
                if preset_name:
                    save_preset(preset_name)
                    st.success(f"✓ Saved preset: {preset_name}")
                    st.rerun()
        
        with col2:
            if st.button("🗑️ Delete Preset", use_container_width=True, disabled=selected_preset_name == '-- Select Preset --'):
                if selected_preset_name != '-- Select Preset --':
                    delete_preset(selected_preset_name)
                    st.success(f"✓ Deleted preset: {selected_preset_name}")
                    st.rerun()
        
        # Export/Import
        st.markdown("---")
        export_col1, export_col2 = st.columns(2, gap="small")
        with export_col1:
            if st.button("📤 Export Presets", use_container_width=True):
                export_presets()
        
        with export_col2:
            uploaded_file = st.file_uploader("📥 Import Presets", type=['json'], key='preset_upload')
            if uploaded_file:
                import_presets(uploaded_file)


def save_preset(name: str):
    """Save current filter state as a preset"""
    preset = st.session_state.filters.copy()
    preset['created_date'] = datetime.now().isoformat()
    preset['description'] = f"Saved on {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    
    st.session_state.filter_presets[name] = preset


def load_preset(name: str):
    """Load a saved preset into current filters"""
    if name in st.session_state.filter_presets:
        preset = st.session_state.filter_presets[name].copy()
        # Remove metadata
        preset.pop('created_date', None)
        preset.pop('description', None)
        
        st.session_state.filters.update(preset)
        st.session_state.filter_metadata['last_preset_loaded'] = name


def delete_preset(name: str):
    """Delete a saved preset"""
    if name in st.session_state.filter_presets:
        del st.session_state.filter_presets[name]


def export_presets() -> str:
    """Export all presets as JSON"""
    export_data = {
        'presets': st.session_state.filter_presets,
        'export_date': datetime.now().isoformat()
    }
    return json.dumps(export_data, indent=2)


def import_presets(uploaded_file):
    """Import presets from JSON file"""
    try:
        data = json.load(uploaded_file)
        if 'presets' in data:
            st.session_state.filter_presets.update(data['presets'])
            st.success("✓ Presets imported successfully")
        else:
            st.error("Invalid preset file format")
    except Exception as e:
        st.error(f"Error importing presets: {str(e)}")


# ============================================================================
# FILTER SUMMARY & ACTIONS
# ============================================================================

def render_filter_actions():
    """Render filter action buttons and summary"""
    st.markdown("---")
    
    # Active filters count
    active_count = count_active_filters()
    
    if active_count > 0:
        st.markdown(f"### 🔍 {active_count} Filter{'s' if active_count != 1 else ''} Active")
    else:
        st.markdown("### ℹ️ No Filters Applied")
    
    # Action buttons
    action_col1, action_col2 = st.columns(2, gap="small")
    
    with action_col1:
        if st.button("🔄 Reset All", use_container_width=True, type="secondary"):
            reset_filters()
            st.rerun()
    
    with action_col2:
        if st.button("✅ Apply Filters", use_container_width=True, type="primary"):
            st.session_state.filter_metadata['last_applied'] = datetime.now().isoformat()
            st.rerun()
    
    # Filter impact summary (would need data to calculate)
    # This is a placeholder - would show actual impact
    if active_count > 0:
        st.caption("💡 Filters are auto-applied. Click 'Apply Filters' to refresh.")


def count_active_filters() -> int:
    """Count number of active (non-default) filters"""
    count = 0
    filters = st.session_state.filters
    
    # Time period (custom counts)
    if filters['time_preset'] != 'Current Quarter':
        count += 1
    if filters['compare_previous']:
        count += 1
    
    # Measures
    if filters['measures']:
        count += 1
    if filters['gap_status'] != ['Open', 'Pending']:
        count += 1
    if filters['prediction_confidence'] != ['High', 'Medium', 'Low']:
        count += 1
    if filters['star_rating_impact']:
        count += 1
    
    # Demographics
    if filters['age_bands']:
        count += 1
    if filters['gender'] != 'All':
        count += 1
    if filters['risk_score_min'] > 0.0 or filters['risk_score_max'] < 10.0:
        count += 1
    if filters['member_tenure'] != 'All':
        count += 1
    
    # Financial
    if filters['min_member_count'] > 0:
        count += 1
    if filters['min_financial_impact'] > 0.0:
        count += 1
    if filters['min_closure_rate'] > 0.0:
        count += 1
    if filters['max_budget_cap']:
        count += 1
    
    # Advanced
    if filters['high_confidence_only']:
        count += 1
    if not filters['include_historical']:
        count += 1
    if filters['exclude_recent_contact']:
        count += 1
    if filters['min_data_quality'] > 0.0:
        count += 1
    
    return count


def reset_filters():
    """Reset all filters to defaults"""
    init_filter_state()
    st.session_state.filter_metadata['last_applied'] = None


def get_filter_summary() -> str:
    """Get human-readable filter summary"""
    active_count = count_active_filters()
    
    if active_count == 0:
        return "No filters applied - showing all data"
    
    summary_parts = []
    filters = st.session_state.filters
    
    # Time period
    if filters['time_preset'] != 'Current Quarter':
        summary_parts.append(f"Period: {filters['time_preset']}")
    
    # Measures
    if filters['measures']:
        summary_parts.append(f"{len(filters['measures'])} measures")
    
    # Status
    if filters['gap_status']:
        summary_parts.append(f"Status: {', '.join(filters['gap_status'])}")
    
    # Financial
    if filters['min_financial_impact'] > 0:
        summary_parts.append(f"Min impact: ${filters['min_financial_impact']:,.0f}")
    
    return " | ".join(summary_parts) if summary_parts else "Filters active"


# ============================================================================
# MAIN SIDEBAR RENDERER
# ============================================================================

def render_sidebar_filters(available_measures: List[str] = None):
    """
    Render complete filter sidebar with all sections.
    
    Args:
        available_measures: List of available HEDIS measure names
    """
    # Initialize if needed
    init_filter_state()
    
    # Use default measures if not provided
    if available_measures is None:
        available_measures = [
            'HbA1c Testing',
            'Blood Pressure Control',
            'Breast Cancer Screening',
            'Colorectal Cancer Screening',
            'Diabetes Care - Eye Exam',
            'Statin Therapy - CVD',
            'Annual Flu Vaccine',
            'Pneumonia Vaccine'
        ]
    
    with st.sidebar:
        # Logo/Header
        st.markdown("### 🎛️ Filters")
        st.markdown("---")
        
        # Filter Sections
        render_time_period_filters()
        st.markdown("---")
        
        render_measures_filters(available_measures)
        st.markdown("---")
        
        render_demographics_filters()
        st.markdown("---")
        
        render_financial_filters()
        st.markdown("---")
        
        render_advanced_filters()
        st.markdown("---")
        
        render_preset_management()
        st.markdown("---")
        
        render_filter_actions()


# ============================================================================
# FILTER APPLICATION
# ============================================================================

def apply_filters(df: pd.DataFrame) -> pd.DataFrame:
    """
    Apply all active filters to DataFrame.
    
    Args:
        df: Input DataFrame with member/measure data
    
    Returns:
        Filtered DataFrame
    """
    if df.empty:
        return df
    
    filtered_df = df.copy()
    filters = st.session_state.filters
    
    # Time Period Filter
    if 'date' in filtered_df.columns or 'intervention_date' in filtered_df.columns:
        date_col = 'date' if 'date' in filtered_df.columns else 'intervention_date'
        filtered_df[date_col] = pd.to_datetime(filtered_df[date_col], errors='coerce')
        filtered_df = filtered_df[
            (filtered_df[date_col].dt.date >= filters['start_date']) &
            (filtered_df[date_col].dt.date <= filters['end_date'])
        ]
    
    # Measures Filter
    if filters['measures'] and 'measure_name' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['measure_name'].isin(filters['measures'])]
    
    # Gap Status Filter
    if filters['gap_status'] and 'gap_status' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['gap_status'].isin(filters['gap_status'])]
    
    # Prediction Confidence Filter
    if filters['prediction_confidence'] and 'prediction_confidence' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['prediction_confidence'].isin(filters['prediction_confidence'])]
    
    # Age Bands Filter
    if filters['age_bands'] and 'age_band' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['age_band'].isin(filters['age_bands'])]
    
    # Gender Filter
    if filters['gender'] != 'All' and 'gender' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['gender'] == filters['gender']]
    
    # Risk Score Filter
    if 'risk_score' in filtered_df.columns:
        filtered_df = filtered_df[
            (filtered_df['risk_score'] >= filters['risk_score_min']) &
            (filtered_df['risk_score'] <= filters['risk_score_max'])
        ]
    
    # Member Tenure Filter
    if filters['member_tenure'] != 'All' and 'member_tenure' in filtered_df.columns:
        if filters['member_tenure'] == 'New (< 1 year)':
            filtered_df = filtered_df[filtered_df['member_tenure'] < 1]
        elif filters['member_tenure'] == '1-2 years':
            filtered_df = filtered_df[(filtered_df['member_tenure'] >= 1) & (filtered_df['member_tenure'] < 2)]
        elif filters['member_tenure'] == '2+ years':
            filtered_df = filtered_df[filtered_df['member_tenure'] >= 2]
    
    # Financial Thresholds
    if filters['min_member_count'] > 0:
        # Group by measure and filter
        if 'measure_name' in filtered_df.columns:
            measure_counts = filtered_df.groupby('measure_name').size()
            valid_measures = measure_counts[measure_counts >= filters['min_member_count']].index
            filtered_df = filtered_df[filtered_df['measure_name'].isin(valid_measures)]
    
    if filters['min_financial_impact'] > 0 and 'financial_value' in filtered_df.columns:
        # Filter at measure level
        if 'measure_name' in filtered_df.columns:
            measure_totals = filtered_df.groupby('measure_name')['financial_value'].sum()
            valid_measures = measure_totals[measure_totals >= filters['min_financial_impact']].index
            filtered_df = filtered_df[filtered_df['measure_name'].isin(valid_measures)]
    
    if filters['min_closure_rate'] > 0 and 'predicted_closure_probability' in filtered_df.columns:
        filtered_df = filtered_df[
            (filtered_df['predicted_closure_probability'] * 100) >= filters['min_closure_rate']
        ]
    
    # Advanced Filters
    if filters['high_confidence_only'] and 'prediction_confidence' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['prediction_confidence'] == 'High']
    
    if not filters['include_historical'] and 'is_historical' in filtered_df.columns:
        filtered_df = filtered_df[~filtered_df['is_historical']]
    
    if filters['exclude_recent_contact'] and 'last_contact_date' in filtered_df.columns:
        cutoff_date = date.today() - timedelta(days=30)
        filtered_df['last_contact_date'] = pd.to_datetime(filtered_df['last_contact_date'], errors='coerce')
        filtered_df = filtered_df[
            (filtered_df['last_contact_date'].isna()) |
            (filtered_df['last_contact_date'].dt.date < cutoff_date)
        ]
    
    if filters['min_data_quality'] > 0 and 'data_quality_score' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['data_quality_score'] >= filters['min_data_quality']]
    
    return filtered_df


def get_filter_values() -> Dict[str, Any]:
    """
    Extract current filter values from session_state.
    
    Returns:
        Dictionary of current filter values
    """
    return st.session_state.filters.copy()


def validate_filters() -> Tuple[bool, Optional[str]]:
    """
    Validate filter combinations for logical consistency.
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    filters = st.session_state.filters
    
    # Date validation
    if filters['start_date'] > filters['end_date']:
        return False, "Start date must be before end date"
    
    # Risk score validation
    if filters['risk_score_min'] > filters['risk_score_max']:
        return False, "Minimum risk score must be less than maximum"
    
    # Financial validation
    if filters['min_financial_impact'] < 0:
        return False, "Minimum financial impact cannot be negative"
    
    if filters['max_budget_cap'] and filters['max_budget_cap'] < filters['min_financial_impact']:
        return False, "Budget cap must be greater than minimum financial impact"
    
    return True, None

