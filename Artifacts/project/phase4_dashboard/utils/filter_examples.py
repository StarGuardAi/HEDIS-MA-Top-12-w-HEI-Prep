"""
Example Usage of Advanced Filtering System

Demonstrates how to integrate the filtering system into Streamlit dashboard
"""
import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta
from utils.advanced_filters import (
    init_filter_state,
    render_sidebar_filters,
    apply_filters,
    get_filter_summary,
    count_active_filters,
    validate_filters
)


# ============================================================================
# EXAMPLE 1: Basic Integration
# ============================================================================
def example_basic_integration():
    """Basic example of filter integration"""
    
    # Initialize filters
    init_filter_state()
    
    # Render sidebar filters
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
    
    render_sidebar_filters(available_measures)
    
    # Load your data
    df = load_member_data()  # Your data loading function
    
    # Apply filters
    filtered_df = apply_filters(df)
    
    # Display results
    st.title("HEDIS Portfolio Optimizer")
    
    # Filter summary
    summary = get_filter_summary()
    st.info(f"🔍 {summary}")
    
    # Show filtered data
    st.subheader("Filtered Results")
    st.metric("Total Members", len(filtered_df))
    st.dataframe(filtered_df.head(100), use_container_width=True)


# ============================================================================
# EXAMPLE 2: With Validation and Error Handling
# ============================================================================
def example_with_validation():
    """Example with filter validation"""
    
    init_filter_state()
    
    # Render filters
    render_sidebar_filters()
    
    # Validate filters
    is_valid, error_msg = validate_filters()
    
    if not is_valid:
        st.error(f"⚠️ Filter Error: {error_msg}")
        st.stop()
    
    # Load and filter data
    df = load_member_data()
    
    try:
        filtered_df = apply_filters(df)
        
        if filtered_df.empty:
            st.warning("⚠️ No data matches current filters. Try adjusting your criteria.")
            st.info("💡 Suggestions:")
            st.markdown("""
            - Broaden date range
            - Select more measures
            - Lower financial thresholds
            - Remove demographic filters
            """)
        else:
            st.success(f"✅ Found {len(filtered_df)} records matching filters")
            # Display results...
            
    except Exception as e:
        st.error(f"Error applying filters: {str(e)}")


# ============================================================================
# EXAMPLE 3: With Performance Optimization
# ============================================================================
def example_with_caching():
    """Example with caching for performance"""
    
    @st.cache_data
    def load_and_filter_data(filters_hash: str):
        """Cached data loading and filtering"""
        df = load_member_data()
        # Apply filters (would use filters_hash to determine which filters)
        filtered_df = apply_filters(df)
        return filtered_df
    
    init_filter_state()
    render_sidebar_filters()
    
    # Create hash of filter state for caching
    import hashlib
    filters_str = str(st.session_state.filters)
    filters_hash = hashlib.md5(filters_str.encode()).hexdigest()
    
    # Load filtered data (cached)
    with st.spinner("Applying filters..."):
        filtered_df = load_and_filter_data(filters_hash)
    
    st.success(f"✅ {len(filtered_df)} records loaded")


# ============================================================================
# EXAMPLE 4: Full Dashboard Integration
# ============================================================================
def example_full_dashboard():
    """Complete dashboard with filters"""
    
    # Page config
    st.set_page_config(
        page_title="HEDIS Portfolio Optimizer",
        page_icon="⭐",
        layout="wide"
    )
    
    # Initialize filters
    init_filter_state()
    
    # Sidebar with filters
    with st.sidebar:
        st.image("logo.png", width=200)  # Your logo
        st.markdown("---")
        
        render_sidebar_filters()
    
    # Main content
    st.title("⭐ HEDIS Portfolio Optimizer")
    
    # Filter summary banner
    active_count = count_active_filters()
    if active_count > 0:
        summary = get_filter_summary()
        st.info(f"🔍 **Active Filters:** {summary}")
    
    # Load data
    df = load_member_data()
    
    # Apply filters
    filtered_df = apply_filters(df)
    
    # Display metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Members", len(filtered_df))
    
    with col2:
        if 'financial_value' in filtered_df.columns:
            total_value = filtered_df['financial_value'].sum()
            st.metric("Total Value", f"${total_value:,.0f}")
    
    with col3:
        if 'measure_name' in filtered_df.columns:
            measure_count = filtered_df['measure_name'].nunique()
            st.metric("Measures", measure_count)
    
    with col4:
        if 'gap_status' in filtered_df.columns:
            open_gaps = len(filtered_df[filtered_df['gap_status'] == 'Open'])
            st.metric("Open Gaps", open_gaps)
    
    st.markdown("---")
    
    # Tabs for different views
    tab1, tab2, tab3 = st.tabs(["📊 Overview", "👥 Members", "💰 Financial"])
    
    with tab1:
        st.subheader("Portfolio Overview")
        # Your charts/visualizations here
        st.dataframe(filtered_df.head(100), use_container_width=True)
    
    with tab2:
        st.subheader("Member List")
        # Member table here
        st.dataframe(filtered_df, use_container_width=True)
    
    with tab3:
        st.subheader("Financial Analysis")
        # Financial charts here
        if 'financial_value' in filtered_df.columns:
            st.bar_chart(filtered_df.groupby('measure_name')['financial_value'].sum())


# ============================================================================
# EXAMPLE 5: Auto-apply with Debouncing
# ============================================================================
def example_auto_apply():
    """Example with auto-apply and debouncing"""
    
    import time
    
    init_filter_state()
    render_sidebar_filters()
    
    # Check if filters changed
    if 'last_filter_hash' not in st.session_state:
        st.session_state.last_filter_hash = None
    
    current_hash = hash(str(st.session_state.filters))
    
    # Auto-apply if filters changed
    if current_hash != st.session_state.last_filter_hash:
        st.session_state.last_filter_hash = current_hash
        
        # Small delay for debouncing
        time.sleep(0.1)
        
        # Apply filters
        df = load_member_data()
        filtered_df = apply_filters(df)
        
        # Store in session state
        st.session_state.filtered_data = filtered_df
    
    # Display results
    if 'filtered_data' in st.session_state:
        st.dataframe(st.session_state.filtered_data)


# ============================================================================
# EXAMPLE 6: Filter Impact Display
# ============================================================================
def example_filter_impact():
    """Show impact of filters on data"""
    
    init_filter_state()
    render_sidebar_filters()
    
    # Load original data
    df_original = load_member_data()
    
    # Apply filters
    df_filtered = apply_filters(df_original)
    
    # Calculate impact
    original_count = len(df_original)
    filtered_count = len(df_filtered)
    reduction_pct = ((original_count - filtered_count) / original_count * 100) if original_count > 0 else 0
    
    # Display impact
    st.title("Filter Impact Analysis")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Original Records", original_count)
    
    with col2:
        st.metric("Filtered Records", filtered_count)
    
    with col3:
        st.metric("Reduction", f"{reduction_pct:.1f}%")
    
    # Visual comparison
    comparison_df = pd.DataFrame({
        'Dataset': ['Original', 'Filtered'],
        'Count': [original_count, filtered_count]
    })
    
    st.bar_chart(comparison_df.set_index('Dataset'))
    
    # Breakdown by measure
    if 'measure_name' in df_original.columns:
        st.subheader("Impact by Measure")
        
        original_by_measure = df_original.groupby('measure_name').size()
        filtered_by_measure = df_filtered.groupby('measure_name').size()
        
        impact_df = pd.DataFrame({
            'Original': original_by_measure,
            'Filtered': filtered_by_measure
        }).fillna(0)
        
        impact_df['Reduction %'] = (
            (impact_df['Original'] - impact_df['Filtered']) / impact_df['Original'] * 100
        ).round(1)
        
        st.dataframe(impact_df, use_container_width=True)


# ============================================================================
# HELPER FUNCTIONS (Placeholders)
# ============================================================================

def load_member_data() -> pd.DataFrame:
    """
    Placeholder for data loading function.
    Replace with your actual data loading logic.
    """
    # Example data structure
    return pd.DataFrame({
        'member_id': [f'M{i:08d}' for i in range(1, 1001)],
        'member_name': [f'Member {i}' for i in range(1, 1001)],
        'measure_name': ['HbA1c Testing'] * 500 + ['Blood Pressure Control'] * 500,
        'gap_status': ['Open'] * 400 + ['Pending'] * 300 + ['Closed'] * 300,
        'financial_value': [1000 + i * 10 for i in range(1000)],
        'predicted_closure_probability': [0.3 + (i % 7) * 0.1 for i in range(1000)],
        'date': [date.today() - timedelta(days=i) for i in range(1000)],
        'age_band': ['65-74'] * 500 + ['75-84'] * 500,
        'gender': ['Male'] * 500 + ['Female'] * 500,
        'risk_score': [i % 11 for i in range(1000)],
        'prediction_confidence': ['High'] * 300 + ['Medium'] * 400 + ['Low'] * 300
    })


# ============================================================================
# USAGE IN STREAMLIT APP
# ============================================================================
if __name__ == "__main__":
    # Example usage in your Streamlit app:
    
    # 1. Initialize filters (at top of app)
    init_filter_state()
    
    # 2. Render sidebar filters
    render_sidebar_filters()
    
    # 3. Load and filter data
    df = load_member_data()
    filtered_df = apply_filters(df)
    
    # 4. Display results
    st.title("HEDIS Portfolio Optimizer")
    st.dataframe(filtered_df, use_container_width=True)
    
    print("✅ Filter system ready to use!")

