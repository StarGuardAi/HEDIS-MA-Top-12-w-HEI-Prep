"""
Example Usage of Desktop-Optimized Healthcare Analytics Visualizations

This file demonstrates how to use the 4 production-ready Plotly visualizations
for the HEDIS Portfolio Optimizer dashboard.
"""
import pandas as pd
from datetime import datetime, timedelta
from utils.desktop_visualizations import (
    create_priority_matrix,
    create_star_gauge,
    create_measure_comparison,
    create_trend_chart
)


# ============================================================================
# EXAMPLE 1: Priority Matrix Bubble Chart
# ============================================================================
def example_priority_matrix():
    """Example usage of create_priority_matrix()"""
    
    # Sample data matching expected structure
    df = pd.DataFrame({
        'measure_name': [
            'HbA1c Testing',
            'Blood Pressure Control',
            'Breast Cancer Screening',
            'Colorectal Cancer Screening',
            'Diabetes Care - Eye Exam',
            'Statin Therapy - CVD'
        ],
        'predicted_closure_rate': [45.2, 52.8, 48.5, 43.1, 40.8, 46.9],
        'financial_impact': [285000, 320000, 275000, 290000, 265000, 310000],
        'member_count': [1200, 1500, 1100, 1300, 1000, 1400],
        'star_rating_impact': [0.15, 0.22, 0.18, 0.16, 0.14, 0.20]
    })
    
    # Create the chart
    fig = create_priority_matrix(df)
    
    # Display (in Streamlit: st.plotly_chart(fig, use_container_width=True))
    return fig


# ============================================================================
# EXAMPLE 2: Star Rating Gauge Chart
# ============================================================================
def example_star_gauge():
    """Example usage of create_star_gauge()"""
    
    # Create gauge showing current vs target rating
    fig = create_star_gauge(
        current_rating=4.0,
        target_rating=4.5,
        title="Medicare Advantage Star Rating"
    )
    
    # Display (in Streamlit: st.plotly_chart(fig, use_container_width=True))
    return fig


# ============================================================================
# EXAMPLE 3: Measure Comparison Grouped Bar Chart
# ============================================================================
def example_measure_comparison():
    """Example usage of create_measure_comparison()"""
    
    # Sample data matching expected structure
    df = pd.DataFrame({
        'measure_name': [
            'HbA1c Testing',
            'Blood Pressure Control',
            'Breast Cancer Screening',
            'Colorectal Cancer Screening',
            'Diabetes Care - Eye Exam',
            'Statin Therapy - CVD',
            'Annual Flu Vaccine',
            'Pneumonia Vaccine'
        ],
        'current_compliance_rate': [35.2, 42.8, 38.5, 33.1, 30.8, 36.9, 45.2, 40.1],
        'benchmark_rate': [40.0, 45.0, 42.0, 38.0, 35.0, 40.0, 50.0, 45.0],
        'predicted_closure_rate': [45.2, 52.8, 48.5, 43.1, 40.8, 46.9, 55.2, 50.1],
        'financial_impact': [285000, 320000, 275000, 290000, 265000, 310000, 300000, 280000]
    })
    
    # Create the chart
    fig = create_measure_comparison(df, max_measures=8)
    
    # Display (in Streamlit: st.plotly_chart(fig, use_container_width=True))
    return fig


# ============================================================================
# EXAMPLE 4: Trend Chart with Confidence Intervals
# ============================================================================
def example_trend_chart():
    """Example usage of create_trend_chart()"""
    
    # Generate sample time series data
    start_date = datetime(2024, 1, 1)
    dates = [start_date + timedelta(days=30*i) for i in range(12)]
    
    # Create data for multiple measures
    measures = ['HbA1c Testing', 'Blood Pressure Control', 'Breast Cancer Screening']
    data_rows = []
    
    for measure in measures:
        base_rate = 35.0 if measure == 'HbA1c Testing' else 42.0 if measure == 'Blood Pressure Control' else 38.0
        for i, date in enumerate(dates):
            compliance_rate = base_rate + (i * 1.5)  # Trend upward
            confidence_lower = compliance_rate - 2.0
            confidence_upper = compliance_rate + 2.0
            
            data_rows.append({
                'date': date,
                'measure_name': measure,
                'compliance_rate': compliance_rate,
                'confidence_lower': confidence_lower,
                'confidence_upper': confidence_upper
            })
    
    df = pd.DataFrame(data_rows)
    
    # Create the chart
    fig = create_trend_chart(
        df,
        date_col='date',
        measure_name_col='measure_name',
        compliance_rate_col='compliance_rate',
        confidence_lower_col='confidence_lower',
        confidence_upper_col='confidence_upper',
        max_measures=5,
        title="Compliance Rate Trend with Confidence Intervals"
    )
    
    # Display (in Streamlit: st.plotly_chart(fig, use_container_width=True))
    return fig


# ============================================================================
# STREAMLIT INTEGRATION EXAMPLE
# ============================================================================
def streamlit_integration_example():
    """
    Example of how to integrate these visualizations into a Streamlit app.
    
    In your Streamlit app.py or page file:
    
    import streamlit as st
    from utils.desktop_visualizations import (
        create_priority_matrix,
        create_star_gauge,
        create_measure_comparison,
        create_trend_chart
    )
    
    # Load your data
    df = load_your_data()  # Your data loading function
    
    # Display Priority Matrix
    st.subheader("Priority Matrix: Measure Impact Analysis")
    fig1 = create_priority_matrix(df)
    st.plotly_chart(fig1, use_container_width=True)
    
    # Display Star Rating Gauge
    st.subheader("Star Rating Dashboard")
    fig2 = create_star_gauge(current_rating=4.0, target_rating=4.5)
    st.plotly_chart(fig2, use_container_width=True)
    
    # Display Measure Comparison
    st.subheader("Measure Performance Comparison")
    fig3 = create_measure_comparison(df, max_measures=8)
    st.plotly_chart(fig3, use_container_width=True)
    
    # Display Trend Chart
    st.subheader("Compliance Rate Trends")
    fig4 = create_trend_chart(df_timeseries)
    st.plotly_chart(fig4, use_container_width=True)
    """
    pass


if __name__ == "__main__":
    # Run examples (for testing)
    print("Generating example visualizations...")
    
    print("\n1. Priority Matrix:")
    fig1 = example_priority_matrix()
    print(f"   Created figure with {len(fig1.data)} traces")
    
    print("\n2. Star Rating Gauge:")
    fig2 = example_star_gauge()
    print(f"   Created gauge chart")
    
    print("\n3. Measure Comparison:")
    fig3 = example_measure_comparison()
    print(f"   Created figure with {len(fig3.data)} traces")
    
    print("\n4. Trend Chart:")
    fig4 = example_trend_chart()
    print(f"   Created figure with {len(fig4.data)} traces")
    
    print("\n✅ All visualizations created successfully!")
    print("\nTo view charts, use: fig.show() or integrate into Streamlit app")

