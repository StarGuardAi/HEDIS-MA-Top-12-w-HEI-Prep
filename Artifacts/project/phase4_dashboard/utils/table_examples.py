"""
Example Usage of Interactive Member Tables

Demonstrates how to integrate AgGrid tables into Streamlit dashboard
"""
import pandas as pd
import streamlit as st
from datetime import datetime, timedelta
from utils.member_tables import (
    create_member_grid,
    create_summary_grid,
    export_selected_to_excel_format,
    get_selection_summary
)


# ============================================================================
# EXAMPLE 1: Master Member List Table
# ============================================================================
def example_member_table():
    """Example usage of create_member_grid() in Streamlit"""
    
    # Sample member data
    sample_data = {
        'member_id': [f'M{i:08d}' for i in range(1, 101)],
        'member_name': [f'Member {i}' for i in range(1, 101)],
        'date_of_birth': [datetime(1950, 1, 1) + timedelta(days=i*100) for i in range(100)],
        'measure_name': ['HbA1c Testing'] * 50 + ['Blood Pressure Control'] * 50,
        'gap_status': ['Open'] * 40 + ['Pending'] * 30 + ['Closed'] * 20 + ['Excluded'] * 10,
        'predicted_closure_probability': [0.3 + (i % 7) * 0.1 for i in range(100)],
        'financial_value': [1000 + i * 50 for i in range(100)],
        'last_contact_date': [datetime(2024, 1, 1) + timedelta(days=i*5) for i in range(100)],
        'assigned_care_coordinator': [f'Coordinator {(i % 5) + 1}' for i in range(100)],
        'priority_score': [50 + (i % 50) for i in range(100)],
        'days_until_deadline': [90 - i for i in range(100)]
    }
    
    df = pd.DataFrame(sample_data)
    
    # In Streamlit app:
    st.title("Member Management Dashboard")
    
    # Display grid
    st.subheader("Master Member List")
    grid_response, selected_members = create_member_grid(
        df,
        height=600,
        enable_sidebar=True,
        enable_grouping=True,
        page_size=50
    )
    
    # Handle selections
    if len(selected_members) > 0:
        st.success(f"✅ Selected {len(selected_members)} members")
        
        # Display selection summary
        summary = get_selection_summary(selected_members)
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Selected Members", summary['count'])
        
        with col2:
            st.metric("Total Value", f"${summary['total_financial_value']:,.2f}")
        
        with col3:
            st.metric("Avg Priority", f"{summary['avg_priority_score']:.1f}")
        
        with col4:
            st.metric("Measures", len(summary['measures']))
        
        # Bulk actions
        st.subheader("Bulk Actions")
        action_col1, action_col2, action_col3 = st.columns(3)
        
        with action_col1:
            if st.button("📧 Assign to Coordinator", use_container_width=True):
                # Your assignment logic here
                st.info("Assignment functionality would be implemented here")
        
        with action_col2:
            if st.button("📥 Export to Excel", use_container_width=True):
                export_df = export_selected_to_excel_format(selected_members)
                # Use pandas to_excel or streamlit download_button
                st.download_button(
                    label="Download Excel File",
                    data=export_df.to_csv(index=False),
                    file_name=f"selected_members_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
        
        with action_col3:
            if st.button("📊 View Details", use_container_width=True):
                st.dataframe(selected_members, use_container_width=True)
        
        # Show gap status breakdown
        if summary['gap_status_counts']:
            st.subheader("Selection Breakdown by Status")
            status_df = pd.DataFrame(
                list(summary['gap_status_counts'].items()),
                columns=['Status', 'Count']
            )
            st.bar_chart(status_df.set_index('Status'))
    
    else:
        st.info("👆 Select members using checkboxes to perform bulk actions")


# ============================================================================
# EXAMPLE 2: Summary Measures Table
# ============================================================================
def example_summary_table():
    """Example usage of create_summary_grid() in Streamlit"""
    
    # Sample member data (will be aggregated)
    sample_data = {
        'member_id': [f'M{i:08d}' for i in range(1, 201)],
        'measure_name': ['HbA1c Testing'] * 60 + ['Blood Pressure Control'] * 50 + 
                        ['Breast Cancer Screening'] * 40 + ['Colorectal Cancer Screening'] * 50,
        'gap_status': ['Open'] * 100 + ['Pending'] * 50 + ['Closed'] * 50,
        'predicted_closure_probability': [0.3 + (i % 7) * 0.1 for i in range(200)],
        'financial_value': [1000 + i * 50 for i in range(200)]
    }
    
    df = pd.DataFrame(sample_data)
    
    # In Streamlit app:
    st.title("HEDIS Measures Summary")
    
    # Quick search box
    search_term = st.text_input("🔍 Quick Search", placeholder="Search by measure name...")
    
    if search_term:
        df_filtered = df[df['measure_name'].str.contains(search_term, case=False, na=False)]
    else:
        df_filtered = df
    
    # Display summary grid
    st.subheader("Measures Overview")
    grid_response, clicked_row = create_summary_grid(
        df_filtered,
        height=400,
        page_size=20
    )
    
    # Handle row click (drill down)
    if clicked_row:
        measure_name = clicked_row.get('Measure')
        st.success(f"📊 Selected measure: **{measure_name}**")
        
        # Filter original data for drill-down
        drill_down_df = df[df['measure_name'] == measure_name]
        
        st.subheader(f"Member Details: {measure_name}")
        
        # Show filtered member list
        member_grid_response, selected_members = create_member_grid(
            drill_down_df,
            height=400,
            enable_sidebar=True,
            enable_grouping=False,
            page_size=25
        )
        
        # Show statistics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Members", len(drill_down_df))
        
        with col2:
            open_gaps = len(drill_down_df[drill_down_df['gap_status'] == 'Open'])
            st.metric("Open Gaps", open_gaps)
        
        with col3:
            total_value = drill_down_df['financial_value'].sum()
            st.metric("Total Value", f"${total_value:,.2f}")
    
    else:
        st.info("👆 Click a row to drill down into member details")


# ============================================================================
# EXAMPLE 3: Full Integration in Streamlit App
# ============================================================================
def full_integration_example():
    """
    Complete example showing both tables in a tabbed interface.
    
    This demonstrates a production-ready implementation.
    """
    
    # Load your data (replace with actual data loading)
    # df = load_member_data()  # Your function
    
    # For demo, create sample data
    sample_data = {
        'member_id': [f'M{i:08d}' for i in range(1, 501)],
        'member_name': [f'Member {i}' for i in range(1, 501)],
        'date_of_birth': [datetime(1950, 1, 1) + timedelta(days=i*50) for i in range(500)],
        'measure_name': ['HbA1c Testing'] * 150 + ['Blood Pressure Control'] * 120 + 
                        ['Breast Cancer Screening'] * 100 + ['Colorectal Cancer Screening'] * 130,
        'gap_status': ['Open'] * 200 + ['Pending'] * 150 + ['Closed'] * 100 + ['Excluded'] * 50,
        'predicted_closure_probability': [0.3 + (i % 7) * 0.1 for i in range(500)],
        'financial_value': [1000 + i * 30 for i in range(500)],
        'last_contact_date': [datetime(2024, 1, 1) + timedelta(days=i*3) for i in range(500)],
        'assigned_care_coordinator': [f'Coordinator {(i % 10) + 1}' for i in range(500)],
        'priority_score': [30 + (i % 70) for i in range(500)],
        'days_until_deadline': [120 - (i % 90) for i in range(500)]
    }
    
    df = pd.DataFrame(sample_data)
    
    # Tabbed interface
    tab1, tab2 = st.tabs(["📊 Summary View", "👥 Member List"])
    
    with tab1:
        st.header("HEDIS Measures Summary")
        
        # Quick filters
        col1, col2 = st.columns(2)
        with col1:
            search_term = st.text_input("🔍 Search Measures", key="summary_search")
        with col2:
            min_value = st.number_input("Min Total Value", min_value=0, value=0, step=10000)
        
        # Apply filters
        df_filtered = df.copy()
        if search_term:
            df_filtered = df_filtered[df_filtered['measure_name'].str.contains(search_term, case=False, na=False)]
        
        # Display summary grid
        summary_response, clicked_row = create_summary_grid(df_filtered, height=500)
        
        # Handle drill-down
        if clicked_row:
            measure_name = clicked_row.get('Measure')
            st.divider()
            st.subheader(f"📋 Members for: {measure_name}")
            
            measure_df = df[df['measure_name'] == measure_name]
            member_response, selected = create_member_grid(measure_df, height=400, page_size=25)
    
    with tab2:
        st.header("Master Member List")
        
        # Filters
        col1, col2, col3 = st.columns(3)
        with col1:
            measure_filter = st.multiselect(
                "Filter by Measure",
                options=df['measure_name'].unique(),
                default=[]
            )
        with col2:
            status_filter = st.multiselect(
                "Filter by Status",
                options=df['gap_status'].unique(),
                default=[]
            )
        with col3:
            priority_threshold = st.slider("Min Priority Score", 0, 100, 0)
        
        # Apply filters
        df_filtered = df.copy()
        if measure_filter:
            df_filtered = df_filtered[df_filtered['measure_name'].isin(measure_filter)]
        if status_filter:
            df_filtered = df_filtered[df_filtered['gap_status'].isin(status_filter)]
        if priority_threshold > 0:
            df_filtered = df_filtered[df_filtered['priority_score'] >= priority_threshold]
        
        # Display member grid
        member_response, selected_members = create_member_grid(
            df_filtered,
            height=600,
            enable_sidebar=True,
            enable_grouping=True,
            page_size=50
        )
        
        # Selection handling
        if len(selected_members) > 0:
            st.divider()
            st.subheader("Selected Members")
            
            # Summary metrics
            summary = get_selection_summary(selected_members)
            
            metric_cols = st.columns(5)
            metric_cols[0].metric("Count", summary['count'])
            metric_cols[1].metric("Total Value", f"${summary['total_financial_value']:,.0f}")
            metric_cols[2].metric("Avg Priority", f"{summary['avg_priority_score']:.1f}")
            metric_cols[3].metric("Measures", len(summary['measures']))
            metric_cols[4].metric("Open Gaps", summary['gap_status_counts'].get('Open', 0))
            
            # Action buttons
            action_cols = st.columns(4)
            
            with action_cols[0]:
                if st.button("📧 Assign Coordinator", use_container_width=True):
                    st.session_state['assign_action'] = True
            
            with action_cols[1]:
                if st.button("📥 Export Excel", use_container_width=True):
                    export_df = export_selected_to_excel_format(selected_members)
                    csv = export_df.to_csv(index=False)
                    st.download_button(
                        "Download CSV",
                        csv,
                        f"members_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        "text/csv"
                    )
            
            with action_cols[2]:
                if st.button("📊 View Details", use_container_width=True):
                    st.dataframe(selected_members, use_container_width=True, height=300)
            
            with action_cols[3]:
                if st.button("🔄 Clear Selection", use_container_width=True):
                    st.rerun()


# ============================================================================
# EXAMPLE 4: Session State Management
# ============================================================================
def session_state_example():
    """
    Example showing how to persist selections and filters in session state.
    """
    
    # Initialize session state
    if 'selected_member_ids' not in st.session_state:
        st.session_state.selected_member_ids = []
    
    if 'applied_filters' not in st.session_state:
        st.session_state.applied_filters = {}
    
    # Sample data
    df = pd.DataFrame({
        'member_id': [f'M{i:08d}' for i in range(1, 101)],
        'member_name': [f'Member {i}' for i in range(1, 101)],
        'measure_name': ['HbA1c Testing'] * 50 + ['Blood Pressure Control'] * 50,
        'gap_status': ['Open'] * 50 + ['Pending'] * 50,
        'financial_value': [1000 + i * 50 for i in range(100)],
        'priority_score': [50 + (i % 50) for i in range(100)],
        'date_of_birth': [datetime(1950, 1, 1) + timedelta(days=i*100) for i in range(100)],
        'predicted_closure_probability': [0.3 + (i % 7) * 0.1 for i in range(100)],
        'last_contact_date': [datetime(2024, 1, 1) + timedelta(days=i*5) for i in range(100)],
        'assigned_care_coordinator': [f'Coordinator {(i % 5) + 1}' for i in range(100)],
        'days_until_deadline': [90 - i for i in range(100)]
    })
    
    st.title("Member Management with Session State")
    
    # Display grid
    grid_response, selected_members = create_member_grid(df, height=500)
    
    # Update session state with selections
    if len(selected_members) > 0:
        st.session_state.selected_member_ids = selected_members['member_id'].tolist()
        
        st.success(f"✅ {len(selected_members)} members selected")
        st.write("Selected Member IDs:", st.session_state.selected_member_ids[:10], "...")
    
    # Show persisted selections
    if st.session_state.selected_member_ids:
        st.subheader("Persisted Selections")
        persisted_df = df[df['member_id'].isin(st.session_state.selected_member_ids)]
        st.dataframe(persisted_df[['member_id', 'member_name', 'measure_name', 'gap_status']])


if __name__ == "__main__":
    # For testing
    print("Member table examples created successfully!")
    print("\nTo use in Streamlit:")
    print("1. Import: from utils.member_tables import create_member_grid, create_summary_grid")
    print("2. Call: grid_response, selected = create_member_grid(df)")
    print("3. Handle: if len(selected) > 0: ...")

