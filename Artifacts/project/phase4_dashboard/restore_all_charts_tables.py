"""
Restore all charts and tables to all pages using available queries and chart functions
Preserves all formatting work including centered mobile badge
"""
import os
import sys
from pathlib import Path

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

def restore_performance_dashboard(file_path):
    """Restore Performance Dashboard with portfolio summary query and charts"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find where to insert (after data availability check)
    marker = '# Check data availability'
    pos = content.find(marker)
    if pos == -1:
        return False, "Marker not found"
    
    # Find end of data availability section
    lines = content.split('\n')
    marker_line = -1
    for i, line in enumerate(lines):
        if marker in line:
            marker_line = i
            break
    
    if marker_line == -1:
        return False, "Could not find marker line"
    
    # Find insert point (after show_data_availability_warning call)
    insert_line = marker_line + 1
    while insert_line < len(lines):
        if 'show_data_availability_warning' in lines[insert_line]:
            insert_line += 1
            continue
        if lines[insert_line].strip() and not lines[insert_line].strip().startswith('#'):
            break
        insert_line += 1
    
    # New content with actual query and charts
    new_content_section = '''
# Execute portfolio summary query
try:
    from utils.queries import get_portfolio_summary_query
    query = get_portfolio_summary_query(
        start_date.strftime("%Y-%m-%d"),
        end_date.strftime("%Y-%m-%d")
    )
    df = execute_query(query)
    
    if df.empty:
        date_range = get_data_date_range()
        if date_range:
            st.warning(f"⚠️ No data found for the selected date range: {format_date_display(start_date)} to {format_date_display(end_date)}")
            st.info(f"💡 Available data: {format_date_display(date_range[0])} to {format_date_display(date_range[1])}")
    else:
        # Scale data
        df_scaled = df.copy()
        membership_size = st.session_state.get('membership_size', 10000)
        BASELINE_MEMBERS = 10000
        scale_factor = membership_size / BASELINE_MEMBERS
        
        if 'total_investment' in df_scaled.columns:
            df_scaled['total_investment'] = df_scaled['total_investment'].astype(float) * scale_factor
        if 'total_closures' in df_scaled.columns:
            df_scaled['total_closures'] = df_scaled['total_closures'].astype(float) * scale_factor
        if 'revenue_impact' in df_scaled.columns:
            df_scaled['revenue_impact'] = df_scaled['revenue_impact'].astype(float) * scale_factor
        if 'net_benefit' in df_scaled.columns:
            df_scaled['net_benefit'] = df_scaled['net_benefit'].astype(float) * scale_factor
        if 'total_interventions' in df_scaled.columns:
            df_scaled['total_interventions'] = df_scaled['total_interventions'].astype(float) * scale_factor
        
        # Extract metrics
        total_investment = df_scaled['total_investment'].iloc[0] if 'total_investment' in df_scaled.columns else 0
        total_closures = int(df_scaled['total_closures'].iloc[0]) if 'total_closures' in df_scaled.columns else 0
        revenue_impact = df_scaled['revenue_impact'].iloc[0] if 'revenue_impact' in df_scaled.columns else 0
        net_benefit = df_scaled['net_benefit'].iloc[0] if 'net_benefit' in df_scaled.columns else 0
        roi_ratio = df_scaled['roi_ratio'].iloc[0] if 'roi_ratio' in df_scaled.columns else 0
        total_interventions = int(df_scaled['total_interventions'].iloc[0]) if 'total_interventions' in df_scaled.columns else 0
        success_rate = df_scaled['overall_success_rate'].iloc[0] if 'overall_success_rate' in df_scaled.columns else 0
        
        # Update metrics display
        st.header("⚡ Portfolio Performance")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Measures", "12")
        with col2:
            st.metric("Avg ROI", f"{roi_ratio:.2f}x" if roi_ratio > 0 else "N/A")
        with col3:
            st.metric("Success Rate", f"{success_rate:.1f}%" if success_rate > 0 else "0%")
        with col4:
            st.metric("Net Benefit", f"${net_benefit:,.0f}" if net_benefit != 0 else "$0")
        
        st.divider()
        
        # Additional metrics
        col5, col6, col7 = st.columns(3)
        with col5:
            st.metric("Total Investment", f"${total_investment:,.0f}" if total_investment > 0 else "$0")
        with col6:
            st.metric("Successful Closures", f"{total_closures:,}" if total_closures > 0 else "0")
        with col7:
            st.metric("Total Interventions", f"{total_interventions:,}" if total_interventions > 0 else "0")
        
        st.divider()
        
        # Get ROI by measure for chart
        from utils.queries import get_roi_by_measure_query
        from utils.charts import create_bar_chart
        
        roi_query = get_roi_by_measure_query(
            start_date.strftime("%Y-%m-%d"),
            end_date.strftime("%Y-%m-%d")
        )
        roi_df = execute_query(roi_query)
        
        if not roi_df.empty:
            # Scale ROI data
            roi_df_scaled = roi_df.copy()
            roi_df_scaled['total_investment'] = roi_df_scaled['total_investment'].astype(float) * scale_factor
            roi_df_scaled['revenue_impact'] = roi_df_scaled['revenue_impact'].astype(float) * scale_factor
            roi_df_scaled['successful_closures'] = roi_df_scaled['successful_closures'].astype(float) * scale_factor
            roi_df_scaled['total_interventions'] = roi_df_scaled['total_interventions'].astype(float) * scale_factor
            
            # Create chart
            fig = create_bar_chart(
                roi_df_scaled,
                x_col="measure_code",
                y_col="roi_ratio",
                title="ROI by HEDIS Measure",
                x_label="Measure Code",
                y_label="ROI Ratio",
                color_col="roi_ratio",
            )
            st.plotly_chart(fig, use_container_width=True, config={'responsive': True, 'displayModeBar': False})
        
        # Data table
        with st.expander("📋 View Portfolio Summary Data"):
            display_df = df_scaled.copy()
            display_df.columns = [
                "Total Investment ($)",
                "Total Closures",
                "Revenue Impact ($)",
                "ROI Ratio",
                "Net Benefit ($)",
                "Total Interventions",
                "Success Rate (%)"
            ]
            st.dataframe(display_df, use_container_width=True, hide_index=True)
            
            # Export button
            csv = display_df.to_csv(index=False)
            st.download_button(
                label="📥 Download as CSV",
                data=csv,
                file_name=f"portfolio_summary_{start_date.strftime('%Y%m%d')}_{end_date.strftime('%Y%m%d')}.csv",
                mime="text/csv",
            )
            
except Exception as e:
    st.error(f"Error loading data: {e}")

st.divider()
'''
    
    # Replace placeholder content
    old_placeholder = '''st.header("⚡ Portfolio Performance")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Measures", "12")
with col2:
    st.metric("Avg ROI", "1.25x")
with col3:
    st.metric("Success Rate", "42%")
with col4:
    st.metric("Net Benefit", "$0")

st.divider()

st.markdown("""
<div style='background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); padding: 16px; border-radius: 12px; border-left: 6px solid #4A3D6F; margin: 12px 0;'>
    <h3 style='color: #4A3D6F; font-size: 1.4rem; font-weight: 700; margin-bottom: 12px;'>⚡ Dashboard Features</h3>
    <div style='background: white; padding: 12px 16px; border-radius: 10px; margin-bottom: 10px; border-left: 4px solid #10B981;'>
        <p style='color: #1f2937; font-size: 1rem; line-height: 1.5; margin: 0; font-weight: 500;'><strong style='color: #10B981;'>📊 Real-Time Metrics:</strong> Live performance indicators.</p>
    </div>
    <div style='background: white; padding: 12px 16px; border-radius: 10px; margin-bottom: 10px; border-left: 4px solid #3b82f6;'>
        <p style='color: #1f2937; font-size: 1rem; line-height: 1.5; margin: 0; font-weight: 500;'><strong style='color: #3b82f6;'>📈 Visualizations:</strong> Charts and graphs for quick insights.</p>
    </div>
    <div style='background: white; padding: 12px 16px; border-radius: 10px; border-left: 4px solid #f59e0b;'>
        <p style='color: #1f2937; font-size: 1rem; line-height: 1.5; margin: 0; font-weight: 500;'><strong style='color: #f59e0b;'>⚡ Quick Actions:</strong> Access key functions from one place.</p>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")
st.markdown("**🚧 Performance dashboard enhancements coming soon**")'''
    
    if old_placeholder in content:
        new_content = content.replace(old_placeholder, new_content_section)
    else:
        # Insert after data availability check
        new_lines = lines[:insert_line] + [new_content_section] + lines[insert_line:]
        new_content = '\n'.join(new_lines)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    return True, "Content restored"

def main():
    """Restore charts and tables to Performance Dashboard"""
    pages_dir = Path(__file__).parent / 'pages'
    performance_file = pages_dir / 'Performance_Dashboard.py'
    
    if not performance_file.exists():
        print(f"[ERROR] {performance_file} not found")
        return
    
    print("Restoring charts and tables to Performance Dashboard...")
    print("=" * 60)
    
    result, info = restore_performance_dashboard(performance_file)
    
    if result:
        print(f"[SUCCESS] Performance Dashboard - {info}")
    else:
        print(f"[SKIP] Performance Dashboard - {info}")
    
    print("=" * 60)
    print("Note: Pages 1-5 already have charts and tables.")
    print("Pages 6+ are placeholder pages that will be enhanced later.")

if __name__ == '__main__':
    main()


