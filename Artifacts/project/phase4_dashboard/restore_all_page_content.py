"""
Restore full page content to all pages
Adds query execution, charts, and data display based on available queries
"""
import os
import sys
from pathlib import Path

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# Page content templates based on query availability
PAGE_CONTENT_TEMPLATES = {
    '4_💵_Budget_Variance.py': '''
# Page content
st.markdown("### 💵 Budget Variance by Measure")
st.markdown("Compare budget allocations vs actual spending")

# Check data availability
show_data_availability_warning(start_date, end_date)

# Execute query
try:
    from utils.queries import get_budget_variance_by_measure_query
    from utils.charts import create_grouped_bar_chart
    
    query = get_budget_variance_by_measure_query(
        start_date.strftime("%Y-%m-%d"),
        end_date.strftime("%Y-%m-%d")
    )
    df = execute_query(query)
    
    if df.empty:
        date_range = get_data_date_range()
        if date_range:
            st.info(f"💡 Available data: {format_date_display(date_range[0])} to {format_date_display(date_range[1])}")
    else:
        # Create chart
        if 'measure_code' in df.columns and 'budget_allocated' in df.columns and 'actual_spent' in df.columns:
            fig = create_grouped_bar_chart(
                df,
                x_col="measure_code",
                y_cols=["budget_allocated", "actual_spent"],
                title="Budget Variance by Measure",
                x_label="Measure Code",
                y_label="Amount ($)"
            )
            st.plotly_chart(fig, use_container_width=True, config={'responsive': True, 'displayModeBar': False})
        
        # Summary metrics
        if 'variance' in df.columns:
            total_variance = df['variance'].sum()
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Variance", f"${total_variance:,.2f}")
            with col2:
                over_budget = len(df[df['variance'] > 0])
                st.metric("Measures Over Budget", f"{over_budget}")
        
        # Data table
        with st.expander("📋 View Detailed Data"):
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            # Export button
            csv = df.to_csv(index=False)
            st.download_button(
                label="📥 Download as CSV",
                data=csv,
                file_name=f"budget_variance_{start_date.strftime('%Y%m%d')}_{end_date.strftime('%Y%m%d')}.csv",
                mime="text/csv",
            )
            
except Exception as e:
    st.error(f"Error loading data: {e}")
''',

    '5_🎯_Cost_Tier_Comparison.py': '''
# Page content
st.markdown("### 🎯 Cost Tier Comparison")
st.markdown("Compare performance across cost tiers")

# Check data availability
show_data_availability_warning(start_date, end_date)

# Execute query
try:
    from utils.queries import get_cost_tier_comparison_query
    from utils.charts import create_grouped_bar_chart
    
    query = get_cost_tier_comparison_query(
        start_date.strftime("%Y-%m-%d"),
        end_date.strftime("%Y-%m-%d")
    )
    df = execute_query(query)
    
    if df.empty:
        date_range = get_data_date_range()
        if date_range:
            st.info(f"💡 Available data: {format_date_display(date_range[0])} to {format_date_display(date_range[1])}")
    else:
        # Create chart
        if 'cost_tier' in df.columns and 'avg_cost' in df.columns:
            fig = create_grouped_bar_chart(
                df,
                x_col="cost_tier",
                y_cols=["avg_cost", "cost_per_closure"] if 'cost_per_closure' in df.columns else ["avg_cost"],
                title="Cost Tier Comparison",
                x_label="Cost Tier",
                y_label="Cost ($)"
            )
            st.plotly_chart(fig, use_container_width=True, config={'responsive': True, 'displayModeBar': False})
        
        # Summary metrics
        if 'success_rate' in df.columns:
            avg_success = df['success_rate'].mean()
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Avg Success Rate", f"{avg_success:.1f}%")
            with col2:
                total_interventions = df['interventions_count'].sum() if 'interventions_count' in df.columns else 0
                st.metric("Total Interventions", f"{int(total_interventions):,}")
        
        # Data table
        with st.expander("📋 View Detailed Data"):
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            # Export button
            csv = df.to_csv(index=False)
            st.download_button(
                label="📥 Download as CSV",
                data=csv,
                file_name=f"cost_tier_comparison_{start_date.strftime('%Y%m%d')}_{end_date.strftime('%Y%m%d')}.csv",
                mime="text/csv",
            )
            
except Exception as e:
    st.error(f"Error loading data: {e}")
''',

    # Placeholder content for pages without specific queries
    'default': '''
# Page content
st.markdown("### 📊 Dashboard")
st.markdown("This page is under development")

st.info("💡 **Coming Soon:** Full functionality will be available in the next update.")

# Placeholder metrics
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Records", "0")
with col2:
    st.metric("Success Rate", "0%")
with col3:
    st.metric("Total Investment", "$0")
'''
}

# Footer template
FOOTER_TEMPLATE = '''
# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 1.5rem; margin-top: 1.5rem; background: #f8f9fa;'>
    <p style='font-weight: 700; font-size: 1.1rem; color: #333; margin-bottom: 0.8rem;'>HEDIS Portfolio Optimizer | StarGuard AI</p>
    <p style='color: #666; font-size: 0.9rem; margin-bottom: 1.2rem;'>Built with Streamlit • Plotly • PostgreSQL | Development: 2024-2026</p>
    <div style='background: #e3f2fd; border-left: 4px solid #2196f3; padding: 12px 16px; margin: 12px auto; max-width: 1200px; text-align: left; border-radius: 6px;'>
        <p style='color: #1565c0; font-size: 0.9rem; line-height: 1.5; margin: 0;'>🔒 <strong>Secure AI Architect</strong> | Healthcare AI that sees everything, exposes nothing. On-premises architecture delivers 2.8-4.1x ROI and $148M+ proven savings while keeping PHI locked down. Zero API transmission • HIPAA-first design.</p>
    </div>
    <div style='background: #fff9e6; border-left: 4px solid #ff9800; padding: 12px 16px; margin: 12px auto; max-width: 1200px; text-align: left; border-radius: 6px;'>
        <p style='color: #d84315; font-size: 0.9rem; line-height: 1.5; margin: 0;'>⚠️ <strong>Portfolio demonstration</strong> using synthetic data to showcase real methodology.</p>
    </div>
    <p style='color: #999; font-size: 0.85rem; margin-top: 1.2rem;'>© 2024-2026 Robert Reichert | StarGuard AI™</p>
</div>
""", unsafe_allow_html=True)
'''

def restore_page_content(file_path):
    """Add page content to a file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if content already exists (has query execution or charts)
        if 'execute_query' in content and 'st.plotly_chart' in content:
            return False, "Already has content"
        
        # Find where to insert (after date range variables)
        date_range_marker = '# Get date range from sidebar'
        date_range_pos = content.find(date_range_marker)
        
        if date_range_pos == -1:
            return False, "Date range marker not found"
        
        # Find the end of date range section
        lines = content.split('\n')
        date_range_line = -1
        for i, line in enumerate(lines):
            if date_range_marker in line:
                date_range_line = i
                break
        
        if date_range_line == -1:
            return False, "Could not find date range line"
        
        # Find where date range section ends (before footer or end of file)
        insert_line = date_range_line + 1
        while insert_line < len(lines):
            if lines[insert_line].strip() and not lines[insert_line].strip().startswith('#'):
                if 'start_date' in lines[insert_line] or 'end_date' in lines[insert_line]:
                    insert_line += 1
                    continue
                break
            insert_line += 1
        
        # Get page-specific content or default
        page_name = Path(file_path).name
        page_content = PAGE_CONTENT_TEMPLATES.get(page_name, PAGE_CONTENT_TEMPLATES['default'])
        
        # Check if footer exists
        has_footer = '# Footer' in content or 'HEDIS Portfolio Optimizer | StarGuard AI' in content
        
        # Insert content
        new_lines = (
            lines[:insert_line] +
            [page_content] +
            ([FOOTER_TEMPLATE] if not has_footer else []) +
            lines[insert_line:]
        )
        
        new_content = '\n'.join(new_lines)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        return True, "Content added"
            
    except Exception as e:
        return None, str(e)

def main():
    """Process all page files"""
    pages_dir = Path(__file__).parent / 'pages'
    
    if not pages_dir.exists():
        print(f"Error: {pages_dir} does not exist")
        return
    
    print("Restoring full page content to all pages...")
    print("=" * 60)
    
    # Exclude pages that already have full content or are special cases
    excluded_files = ['8_📋_Campaign_Builder.py']  # Has its own content
    
    page_files = sorted([
        f for f in pages_dir.glob('*.py') 
        if f.name != '__init__.py' and f.name not in excluded_files
    ])
    
    stats = {
        'added': 0,
        'skipped': 0,
        'errors': 0
    }
    
    for page_file in page_files:
        result, info = restore_page_content(page_file)
        
        if result is True:
            print(f"[ADDED] {page_file.name}")
            stats['added'] += 1
        elif result is False:
            print(f"[SKIP] {page_file.name} - {info}")
            stats['skipped'] += 1
        else:
            print(f"[ERROR] {page_file.name} - {info}")
            stats['errors'] += 1
    
    print("=" * 60)
    print(f"[SUMMARY]")
    print(f"  Added: {stats['added']}")
    print(f"  Skipped: {stats['skipped']}")
    print(f"  Errors: {stats['errors']}")
    print(f"  Total: {len(page_files)} files")

if __name__ == '__main__':
    main()


