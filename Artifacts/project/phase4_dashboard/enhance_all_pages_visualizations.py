"""
Enhance all pages with additional visualizations, download buttons, and detailed tables
Optimize display of features and dimensions by variable separately for each page topic
"""
import os
import sys
from pathlib import Path
import re

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

def enhance_roi_page(file_path):
    """Add multiple visualizations and detailed tables to ROI page"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find where to insert additional visualizations (after the main chart)
    marker = 'st.plotly_chart(fig, use_container_width=True, config={\'responsive\': True, \'displayModeBar\': False})'
    pos = content.find(marker)
    if pos == -1:
        return False, "Chart marker not found"
    
    # Find the line number
    lines = content.split('\n')
    marker_line = -1
    for i, line in enumerate(lines):
        if marker in line:
            marker_line = i
            break
    
    if marker_line == -1:
        return False, "Could not find marker line"
    
    # Insert additional visualizations after the main chart
    additional_viz = '''
        
        st.divider()
        
        # Additional Visualizations - Multiple Dimensions
        st.header("📊 Additional Analysis Views")
        
        # View 1: Investment vs Revenue Impact (Scatter)
        col1, col2 = st.columns(2)
        with col1:
            if 'total_investment' in df_scaled.columns and 'revenue_impact' in df_scaled.columns:
                from utils.charts import create_scatter_plot
                fig_inv = create_scatter_plot(
                    df_scaled,
                    x_col="total_investment",
                    y_col="revenue_impact",
                    size_col="successful_closures" if 'successful_closures' in df_scaled.columns else None,
                    color_col="roi_ratio" if 'roi_ratio' in df_scaled.columns else None,
                    title="Investment vs Revenue Impact",
                    x_label="Total Investment ($)",
                    y_label="Revenue Impact ($)"
                )
                st.plotly_chart(fig_inv, use_container_width=True, config={'responsive': True, 'displayModeBar': False})
        
        # View 2: Success Rate by Measure (Bar Chart)
        with col2:
            if 'successful_closures' in df_scaled.columns and 'total_interventions' in df_scaled.columns:
                df_scaled['success_rate'] = (df_scaled['successful_closures'] / df_scaled['total_interventions'] * 100).round(1)
                fig_success = create_bar_chart(
                    df_scaled,
                    x_col="measure_code",
                    y_col="success_rate",
                    title="Success Rate by Measure (%)",
                    x_label="Measure Code",
                    y_label="Success Rate (%)",
                    color_col="success_rate",
                )
                st.plotly_chart(fig_success, use_container_width=True, config={'responsive': True, 'displayModeBar': False})
        
        st.divider()
        
        # View 3: Net Benefit by Measure (Grouped Bar)
        if 'revenue_impact' in df_scaled.columns and 'total_investment' in df_scaled.columns:
            df_scaled['net_benefit'] = df_scaled['revenue_impact'] - df_scaled['total_investment']
            from utils.charts import create_grouped_bar_chart
            fig_net = create_grouped_bar_chart(
                df_scaled,
                x_col="measure_code",
                y_cols=["revenue_impact", "total_investment", "net_benefit"],
                title="Financial Breakdown by Measure",
                x_label="Measure Code",
                y_label="Amount ($)"
            )
            st.plotly_chart(fig_net, use_container_width=True, config={'responsive': True, 'displayModeBar': False})
        
        st.divider()
        
        # Detailed Tables by Dimension
        st.header("📋 Detailed Data Tables by Dimension")
        
        tab1, tab2, tab3, tab4 = st.tabs(["💰 Financial Metrics", "📊 Performance Metrics", "🎯 ROI Analysis", "📈 Complete Dataset"])
        
        with tab1:
            st.subheader("Financial Metrics")
            financial_df = df_scaled[[
                "measure_code",
                "measure_name",
                "total_investment",
                "revenue_impact",
                "net_benefit"
            ]].copy()
            financial_df.columns = [
                "Measure Code",
                "Measure Name",
                "Total Investment ($)",
                "Revenue Impact ($)",
                "Net Benefit ($)"
            ]
            financial_df = financial_df.sort_values("Net Benefit ($)", ascending=False)
            st.dataframe(financial_df, use_container_width=True, hide_index=True)
            
            csv_financial = financial_df.to_csv(index=False)
            st.download_button(
                label="📥 Download Financial Metrics (CSV)",
                data=csv_financial,
                file_name=f"roi_financial_metrics_{start_date.strftime('%Y%m%d')}_{end_date.strftime('%Y%m%d')}.csv",
                mime="text/csv",
                key="download_financial"
            )
        
        with tab2:
            st.subheader("Performance Metrics")
            performance_df = df_scaled[[
                "measure_code",
                "measure_name",
                "successful_closures",
                "total_interventions",
                "success_rate"
            ]].copy()
            performance_df['success_rate'] = (performance_df['successful_closures'] / performance_df['total_interventions'] * 100).round(1)
            performance_df.columns = [
                "Measure Code",
                "Measure Name",
                "Successful Closures",
                "Total Interventions",
                "Success Rate (%)"
            ]
            performance_df = performance_df.sort_values("Success Rate (%)", ascending=False)
            st.dataframe(performance_df, use_container_width=True, hide_index=True)
            
            csv_performance = performance_df.to_csv(index=False)
            st.download_button(
                label="📥 Download Performance Metrics (CSV)",
                data=csv_performance,
                file_name=f"roi_performance_metrics_{start_date.strftime('%Y%m%d')}_{end_date.strftime('%Y%m%d')}.csv",
                mime="text/csv",
                key="download_performance"
            )
        
        with tab3:
            st.subheader("ROI Analysis")
            roi_df = df_scaled[[
                "measure_code",
                "measure_name",
                "roi_ratio",
                "total_investment",
                "revenue_impact",
                "net_benefit"
            ]].copy()
            roi_df['net_benefit'] = roi_df['revenue_impact'] - roi_df['total_investment']
            roi_df.columns = [
                "Measure Code",
                "Measure Name",
                "ROI Ratio",
                "Total Investment ($)",
                "Revenue Impact ($)",
                "Net Benefit ($)"
            ]
            roi_df = roi_df.sort_values("ROI Ratio", ascending=False)
            st.dataframe(roi_df, use_container_width=True, hide_index=True)
            
            csv_roi = roi_df.to_csv(index=False)
            st.download_button(
                label="📥 Download ROI Analysis (CSV)",
                data=csv_roi,
                file_name=f"roi_analysis_{start_date.strftime('%Y%m%d')}_{end_date.strftime('%Y%m%d')}.csv",
                mime="text/csv",
                key="download_roi"
            )
        
        with tab4:
            st.subheader("Complete Dataset")
            complete_df = df_scaled[[
                "measure_code",
                "measure_name",
                "total_investment",
                "revenue_impact",
                "roi_ratio",
                "successful_closures",
                "total_interventions"
            ]].copy()
            complete_df['success_rate'] = (complete_df['successful_closures'] / complete_df['total_interventions'] * 100).round(1)
            complete_df['net_benefit'] = complete_df['revenue_impact'] - complete_df['total_investment']
            complete_df.columns = [
                "Measure Code",
                "Measure Name",
                "Total Investment ($)",
                "Revenue Impact ($)",
                "ROI Ratio",
                "Successful Closures",
                "Total Interventions",
                "Success Rate (%)",
                "Net Benefit ($)"
            ]
            st.dataframe(complete_df, use_container_width=True, hide_index=True)
            
            csv_complete = complete_df.to_csv(index=False)
            st.download_button(
                label="📥 Download Complete Dataset (CSV)",
                data=csv_complete,
                file_name=f"roi_complete_dataset_{start_date.strftime('%Y%m%d')}_{end_date.strftime('%Y%m%d')}.csv",
                mime="text/csv",
                key="download_complete"
            )
        
        st.divider()
'''
    
    # Insert after the main chart
    insert_pos = marker_line + 1
    new_lines = lines[:insert_pos] + [additional_viz] + lines[insert_pos:]
    new_content = '\n'.join(new_lines)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    return True, "Enhanced with multiple visualizations and detailed tables"

def enhance_cost_per_closure_page(file_path):
    """Add multiple visualizations and detailed tables to Cost Per Closure page"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find where to insert (after the scatter plot)
    marker = 'st.plotly_chart(fig, use_container_width=True, config={\'responsive\': True, \'displayModeBar\': False})'
    pos = content.find(marker)
    if pos == -1:
        return False, "Chart marker not found"
    
    lines = content.split('\n')
    marker_line = -1
    for i, line in enumerate(lines):
        if marker in line:
            # Check if this is the scatter plot (look for context)
            context_start = max(0, i-5)
            context = '\n'.join(lines[context_start:i+1]).lower()
            if 'scatter' in context or 'cost_per_closure' in context:
                marker_line = i
                break
    
    if marker_line == -1:
        return False, "Could not find marker line"
    
    additional_viz = '''
        
        st.divider()
        
        # Additional Visualizations - Multiple Dimensions
        st.header("📊 Additional Analysis Views")
        
        # View 1: Success Rate vs Cost Per Closure
        col1, col2 = st.columns(2)
        with col1:
            if 'success_rate' in df_scaled.columns and 'cost_per_closure' in df_scaled.columns:
                fig_success_cost = create_scatter_plot(
                    df_scaled,
                    x_col="cost_per_closure",
                    y_col="success_rate",
                    size_col="successful_closures" if 'successful_closures' in df_scaled.columns else None,
                    color_col="times_used" if 'times_used' in df_scaled.columns else None,
                    title="Success Rate vs Cost Per Closure",
                    x_label="Cost Per Closure ($)",
                    y_label="Success Rate (%)"
                )
                st.plotly_chart(fig_success_cost, use_container_width=True, config={'responsive': True, 'displayModeBar': False})
        
        # View 2: Activity Usage Frequency
        with col2:
            if 'times_used' in df_scaled.columns and 'activity_name' in df_scaled.columns:
                from utils.charts import create_bar_chart
                fig_usage = create_bar_chart(
                    df_scaled.sort_values('times_used', ascending=False),
                    x_col="activity_name",
                    y_col="times_used",
                    title="Activity Usage Frequency",
                    x_label="Activity Name",
                    y_label="Times Used",
                    color_col="times_used",
                )
                st.plotly_chart(fig_usage, use_container_width=True, config={'responsive': True, 'displayModeBar': False})
        
        st.divider()
        
        # View 3: Cost Efficiency Comparison
        if 'cost_per_closure' in df_scaled.columns and 'success_rate' in df_scaled.columns:
            df_scaled['efficiency_score'] = (df_scaled['success_rate'] / df_scaled['cost_per_closure'] * 100).round(2)
            fig_efficiency = create_bar_chart(
                df_scaled.sort_values('efficiency_score', ascending=False),
                x_col="activity_name",
                y_col="efficiency_score",
                title="Cost Efficiency Score (Success Rate / Cost)",
                x_label="Activity Name",
                y_label="Efficiency Score",
                color_col="efficiency_score",
            )
            st.plotly_chart(fig_efficiency, use_container_width=True, config={'responsive': True, 'displayModeBar': False})
        
        st.divider()
        
        # Detailed Tables by Dimension
        st.header("📋 Detailed Data Tables by Dimension")
        
        tab1, tab2, tab3, tab4 = st.tabs(["💰 Cost Analysis", "📊 Performance Analysis", "🎯 Efficiency Analysis", "📈 Complete Dataset"])
        
        with tab1:
            st.subheader("Cost Analysis")
            cost_df = df_scaled[[
                "activity_name",
                "avg_cost",
                "cost_per_closure",
                "times_used"
            ]].copy()
            cost_df.columns = [
                "Activity Name",
                "Average Cost ($)",
                "Cost Per Closure ($)",
                "Times Used"
            ]
            cost_df = cost_df.sort_values("Cost Per Closure ($)", ascending=True)
            st.dataframe(cost_df, use_container_width=True, hide_index=True)
            
            csv_cost = cost_df.to_csv(index=False)
            st.download_button(
                label="📥 Download Cost Analysis (CSV)",
                data=csv_cost,
                file_name=f"cost_analysis_{start_date.strftime('%Y%m%d')}_{end_date.strftime('%Y%m%d')}.csv",
                mime="text/csv",
                key="download_cost"
            )
        
        with tab2:
            st.subheader("Performance Analysis")
            perf_df = df_scaled[[
                "activity_name",
                "success_rate",
                "successful_closures",
                "times_used"
            ]].copy()
            perf_df.columns = [
                "Activity Name",
                "Success Rate (%)",
                "Successful Closures",
                "Times Used"
            ]
            perf_df = perf_df.sort_values("Success Rate (%)", ascending=False)
            st.dataframe(perf_df, use_container_width=True, hide_index=True)
            
            csv_perf = perf_df.to_csv(index=False)
            st.download_button(
                label="📥 Download Performance Analysis (CSV)",
                data=csv_perf,
                file_name=f"performance_analysis_{start_date.strftime('%Y%m%d')}_{end_date.strftime('%Y%m%d')}.csv",
                mime="text/csv",
                key="download_perf"
            )
        
        with tab3:
            st.subheader("Efficiency Analysis")
            efficiency_df = df_scaled.copy()
            efficiency_df['efficiency_score'] = (efficiency_df['success_rate'] / efficiency_df['cost_per_closure'] * 100).round(2)
            efficiency_df = efficiency_df[[
                "activity_name",
                "cost_per_closure",
                "success_rate",
                "efficiency_score",
                "successful_closures"
            ]]
            efficiency_df.columns = [
                "Activity Name",
                "Cost Per Closure ($)",
                "Success Rate (%)",
                "Efficiency Score",
                "Successful Closures"
            ]
            efficiency_df = efficiency_df.sort_values("Efficiency Score", ascending=False)
            st.dataframe(efficiency_df, use_container_width=True, hide_index=True)
            
            csv_eff = efficiency_df.to_csv(index=False)
            st.download_button(
                label="📥 Download Efficiency Analysis (CSV)",
                data=csv_eff,
                file_name=f"efficiency_analysis_{start_date.strftime('%Y%m%d')}_{end_date.strftime('%Y%m%d')}.csv",
                mime="text/csv",
                key="download_eff"
            )
        
        with tab4:
            st.subheader("Complete Dataset")
            complete_df = df_scaled.copy()
            complete_df.columns = [
                "Activity Name",
                "Average Cost ($)",
                "Times Used",
                "Successful Closures",
                "Success Rate (%)",
                "Cost Per Closure ($)"
            ]
            st.dataframe(complete_df, use_container_width=True, hide_index=True)
            
            csv_complete = complete_df.to_csv(index=False)
            st.download_button(
                label="📥 Download Complete Dataset (CSV)",
                data=csv_complete,
                file_name=f"cost_per_closure_complete_{start_date.strftime('%Y%m%d')}_{end_date.strftime('%Y%m%d')}.csv",
                mime="text/csv",
                key="download_complete"
            )
        
        st.divider()
'''
    
    insert_pos = marker_line + 1
    new_lines = lines[:insert_pos] + [additional_viz] + lines[insert_pos:]
    new_content = '\n'.join(new_lines)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    return True, "Enhanced with multiple visualizations and detailed tables"

def enhance_monthly_trend_page(file_path):
    """Add multiple visualizations and detailed tables to Monthly Trend page"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find where to insert (after the line chart)
    marker = 'st.plotly_chart(fig, use_container_width=True, config={\'responsive\': True, \'displayModeBar\': False})'
    pos = content.find(marker)
    if pos == -1:
        return False, "Chart marker not found"
    
    lines = content.split('\n')
    marker_line = -1
    for i, line in enumerate(lines):
        if marker in line:
            # Check if this is the line chart (look for context)
            context_start = max(0, i-5)
            context = '\n'.join(lines[context_start:i+1]).lower()
            if 'line' in context or 'monthly' in context or 'trend' in context:
                marker_line = i
                break
    
    if marker_line == -1:
        return False, "Could not find marker line"
    
    additional_viz = '''
        
        st.divider()
        
        # Additional Visualizations - Multiple Dimensions
        st.header("📊 Additional Analysis Views")
        
        # View 1: Investment Trend Over Time
        col1, col2 = st.columns(2)
        with col1:
            if 'month' in df_scaled.columns and 'total_investment' in df_scaled.columns:
                from utils.charts import create_line_chart
                fig_inv = create_line_chart(
                    df_scaled,
                    x_col="month",
                    y_cols=["total_investment"],
                    title="Investment Trend Over Time",
                    x_label="Month",
                    y_label="Total Investment ($)"
                )
                st.plotly_chart(fig_inv, use_container_width=True, config={'responsive': True, 'displayModeBar': False})
        
        # View 2: Success Rate Trend
        with col2:
            if 'month' in df_scaled.columns and 'successful_closures' in df_scaled.columns and 'total_interventions' in df_scaled.columns:
                df_scaled['monthly_success_rate'] = (df_scaled['successful_closures'] / df_scaled['total_interventions'] * 100).round(1)
                fig_success = create_line_chart(
                    df_scaled,
                    x_col="month",
                    y_cols=["monthly_success_rate"],
                    title="Success Rate Trend Over Time",
                    x_label="Month",
                    y_label="Success Rate (%)"
                )
                st.plotly_chart(fig_success, use_container_width=True, config={'responsive': True, 'displayModeBar': False})
        
        st.divider()
        
        # View 3: Monthly Comparison (Grouped Bar)
        if 'month' in df_scaled.columns:
            from utils.charts import create_grouped_bar_chart
            y_cols = ['total_interventions']
            if 'successful_closures' in df_scaled.columns:
                y_cols.append('successful_closures')
            if 'total_investment' in df_scaled.columns:
                y_cols.append('total_investment')
            
            fig_comparison = create_grouped_bar_chart(
                df_scaled,
                x_col="month",
                y_cols=y_cols[:2],  # Limit to 2 for clarity
                title="Monthly Comparison: Interventions vs Closures",
                x_label="Month",
                y_label="Count"
            )
            st.plotly_chart(fig_comparison, use_container_width=True, config={'responsive': True, 'displayModeBar': False})
        
        st.divider()
        
        # Detailed Tables by Dimension
        st.header("📋 Detailed Data Tables by Dimension")
        
        tab1, tab2, tab3, tab4 = st.tabs(["📈 Trend Analysis", "💰 Financial Trends", "📊 Performance Trends", "📈 Complete Dataset"])
        
        with tab1:
            st.subheader("Trend Analysis")
            trend_df = df_scaled[[
                "month",
                "total_interventions",
                "successful_closures"
            ]].copy()
            trend_df['success_rate'] = (trend_df['successful_closures'] / trend_df['total_interventions'] * 100).round(1)
            trend_df.columns = [
                "Month",
                "Total Interventions",
                "Successful Closures",
                "Success Rate (%)"
            ]
            st.dataframe(trend_df, use_container_width=True, hide_index=True)
            
            csv_trend = trend_df.to_csv(index=False)
            st.download_button(
                label="📥 Download Trend Analysis (CSV)",
                data=csv_trend,
                file_name=f"monthly_trend_analysis_{start_date.strftime('%Y%m%d')}_{end_date.strftime('%Y%m%d')}.csv",
                mime="text/csv",
                key="download_trend"
            )
        
        with tab2:
            st.subheader("Financial Trends")
            if 'total_investment' in df_scaled.columns:
                financial_df = df_scaled[[
                    "month",
                    "total_investment"
                ]].copy()
                financial_df.columns = [
                    "Month",
                    "Total Investment ($)"
                ]
                st.dataframe(financial_df, use_container_width=True, hide_index=True)
                
                csv_financial = financial_df.to_csv(index=False)
                st.download_button(
                    label="📥 Download Financial Trends (CSV)",
                    data=csv_financial,
                    file_name=f"monthly_financial_trends_{start_date.strftime('%Y%m%d')}_{end_date.strftime('%Y%m%d')}.csv",
                    mime="text/csv",
                    key="download_financial"
                )
            else:
                st.info("Financial data not available for this period")
        
        with tab3:
            st.subheader("Performance Trends")
            perf_df = df_scaled[[
                "month",
                "total_interventions",
                "successful_closures"
            ]].copy()
            perf_df['success_rate'] = (perf_df['successful_closures'] / perf_df['total_interventions'] * 100).round(1)
            perf_df['closure_rate'] = (perf_df['successful_closures'] / perf_df['total_interventions'] * 100).round(1)
            perf_df.columns = [
                "Month",
                "Total Interventions",
                "Successful Closures",
                "Success Rate (%)",
                "Closure Rate (%)"
            ]
            st.dataframe(perf_df, use_container_width=True, hide_index=True)
            
            csv_perf = perf_df.to_csv(index=False)
            st.download_button(
                label="📥 Download Performance Trends (CSV)",
                data=csv_perf,
                file_name=f"monthly_performance_trends_{start_date.strftime('%Y%m%d')}_{end_date.strftime('%Y%m%d')}.csv",
                mime="text/csv",
                key="download_perf"
            )
        
        with tab4:
            st.subheader("Complete Dataset")
            complete_df = df_scaled.copy()
            if 'total_investment' in complete_df.columns:
                complete_df = complete_df[[
                    "month",
                    "total_interventions",
                    "successful_closures",
                    "total_investment"
                ]]
                complete_df['success_rate'] = (complete_df['successful_closures'] / complete_df['total_interventions'] * 100).round(1)
                complete_df.columns = [
                    "Month",
                    "Total Interventions",
                    "Successful Closures",
                    "Total Investment ($)",
                    "Success Rate (%)"
                ]
            else:
                complete_df = complete_df[[
                    "month",
                    "total_interventions",
                    "successful_closures"
                ]]
                complete_df['success_rate'] = (complete_df['successful_closures'] / complete_df['total_interventions'] * 100).round(1)
                complete_df.columns = [
                    "Month",
                    "Total Interventions",
                    "Successful Closures",
                    "Success Rate (%)"
                ]
            st.dataframe(complete_df, use_container_width=True, hide_index=True)
            
            csv_complete = complete_df.to_csv(index=False)
            st.download_button(
                label="📥 Download Complete Dataset (CSV)",
                data=csv_complete,
                file_name=f"monthly_trend_complete_{start_date.strftime('%Y%m%d')}_{end_date.strftime('%Y%m%d')}.csv",
                mime="text/csv",
                key="download_complete"
            )
        
        st.divider()
'''
    
    insert_pos = marker_line + 1
    new_lines = lines[:insert_pos] + [additional_viz] + lines[insert_pos:]
    new_content = '\n'.join(new_lines)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    return True, "Enhanced with multiple visualizations and detailed tables"

def enhance_budget_variance_page(file_path):
    """Add multiple visualizations and detailed tables to Budget Variance page"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find where to insert (after the grouped bar chart)
    marker = 'st.plotly_chart(fig, use_container_width=True, config={\'responsive\': True, \'displayModeBar\': False})'
    pos = content.find(marker)
    if pos == -1:
        return False, "Chart marker not found"
    
    lines = content.split('\n')
    marker_line = -1
    for i, line in enumerate(lines):
        if marker in line:
            marker_line = i
            break
    
    if marker_line == -1:
        return False, "Could not find marker line"
    
    additional_viz = '''
        
        st.divider()
        
        # Additional Visualizations - Multiple Dimensions
        st.header("📊 Additional Analysis Views")
        
        # View 1: Variance Percentage by Measure
        col1, col2 = st.columns(2)
        with col1:
            if 'variance_pct' in df.columns and 'measure_code' in df.columns:
                from utils.charts import create_bar_chart
                fig_var_pct = create_bar_chart(
                    df,
                    x_col="measure_code",
                    y_col="variance_pct",
                    title="Variance Percentage by Measure",
                    x_label="Measure Code",
                    y_label="Variance (%)",
                    color_col="variance_pct",
                )
                st.plotly_chart(fig_var_pct, use_container_width=True, config={'responsive': True, 'displayModeBar': False})
        
        # View 2: Budget Status Distribution
        with col2:
            if 'budget_status' in df.columns:
                status_counts = df['budget_status'].value_counts()
                import plotly.express as px
                fig_status = px.pie(
                    values=status_counts.values,
                    names=status_counts.index,
                    title="Budget Status Distribution"
                )
                fig_status.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig_status, use_container_width=True, config={'responsive': True, 'displayModeBar': False})
        
        st.divider()
        
        # View 3: Variance Scatter Analysis
        if 'budget_allocated' in df.columns and 'actual_spent' in df.columns:
            from utils.charts import create_scatter_plot
            fig_scatter = create_scatter_plot(
                df,
                x_col="budget_allocated",
                y_col="actual_spent",
                size_col="variance" if 'variance' in df.columns else None,
                color_col="variance_pct" if 'variance_pct' in df.columns else None,
                title="Budget Allocated vs Actual Spent",
                x_label="Budget Allocated ($)",
                y_label="Actual Spent ($)"
            )
            st.plotly_chart(fig_scatter, use_container_width=True, config={'responsive': True, 'displayModeBar': False})
        
        st.divider()
        
        # Detailed Tables by Dimension
        st.header("📋 Detailed Data Tables by Dimension")
        
        tab1, tab2, tab3, tab4 = st.tabs(["💰 Budget Analysis", "📊 Variance Analysis", "🎯 Status Breakdown", "📈 Complete Dataset"])
        
        with tab1:
            st.subheader("Budget Analysis")
            budget_df = df[[
                "measure_code",
                "measure_name" if 'measure_name' in df.columns else None,
                "budget_allocated",
                "actual_spent"
            ]].copy()
            budget_df = budget_df.dropna(axis=1)
            if 'measure_name' not in budget_df.columns:
                budget_df.columns = [
                    "Measure Code",
                    "Budget Allocated ($)",
                    "Actual Spent ($)"
                ]
            else:
                budget_df.columns = [
                    "Measure Code",
                    "Measure Name",
                    "Budget Allocated ($)",
                    "Actual Spent ($)"
                ]
            budget_df = budget_df.sort_values("Budget Allocated ($)", ascending=False)
            st.dataframe(budget_df, use_container_width=True, hide_index=True)
            
            csv_budget = budget_df.to_csv(index=False)
            st.download_button(
                label="📥 Download Budget Analysis (CSV)",
                data=csv_budget,
                file_name=f"budget_analysis_{start_date.strftime('%Y%m%d')}_{end_date.strftime('%Y%m%d')}.csv",
                mime="text/csv",
                key="download_budget"
            )
        
        with tab2:
            st.subheader("Variance Analysis")
            variance_df = df[[
                "measure_code",
                "measure_name" if 'measure_name' in df.columns else None,
                "variance",
                "variance_pct",
                "budget_status"
            ]].copy()
            variance_df = variance_df.dropna(axis=1)
            if 'measure_name' not in variance_df.columns:
                variance_df.columns = [
                    "Measure Code",
                    "Variance ($)",
                    "Variance (%)",
                    "Status"
                ]
            else:
                variance_df.columns = [
                    "Measure Code",
                    "Measure Name",
                    "Variance ($)",
                    "Variance (%)",
                    "Status"
                ]
            variance_df = variance_df.sort_values("Variance ($)", ascending=False)
            st.dataframe(variance_df, use_container_width=True, hide_index=True)
            
            csv_variance = variance_df.to_csv(index=False)
            st.download_button(
                label="📥 Download Variance Analysis (CSV)",
                data=csv_variance,
                file_name=f"variance_analysis_{start_date.strftime('%Y%m%d')}_{end_date.strftime('%Y%m%d')}.csv",
                mime="text/csv",
                key="download_variance"
            )
        
        with tab3:
            st.subheader("Status Breakdown")
            status_df = df.groupby('budget_status').agg({
                'measure_code': 'count',
                'variance': 'sum' if 'variance' in df.columns else None,
                'budget_allocated': 'sum' if 'budget_allocated' in df.columns else None,
                'actual_spent': 'sum' if 'actual_spent' in df.columns else None
            }).reset_index()
            status_df.columns = [
                "Status",
                "Measure Count",
                "Total Variance ($)" if 'variance' in df.columns else "Count",
                "Total Budget ($)" if 'budget_allocated' in df.columns else None,
                "Total Spent ($)" if 'actual_spent' in df.columns else None
            ]
            status_df = status_df.dropna(axis=1)
            st.dataframe(status_df, use_container_width=True, hide_index=True)
            
            csv_status = status_df.to_csv(index=False)
            st.download_button(
                label="📥 Download Status Breakdown (CSV)",
                data=csv_status,
                file_name=f"status_breakdown_{start_date.strftime('%Y%m%d')}_{end_date.strftime('%Y%m%d')}.csv",
                mime="text/csv",
                key="download_status"
            )
        
        with tab4:
            st.subheader("Complete Dataset")
            complete_df = df.copy()
            if 'measure_name' in complete_df.columns:
                complete_df = complete_df[[
                    "measure_code",
                    "measure_name",
                    "budget_allocated",
                    "actual_spent",
                    "variance",
                    "variance_pct",
                    "budget_status"
                ]]
                complete_df.columns = [
                    "Measure Code",
                    "Measure Name",
                    "Budget Allocated ($)",
                    "Actual Spent ($)",
                    "Variance ($)",
                    "Variance (%)",
                    "Status"
                ]
            else:
                complete_df = complete_df[[
                    "measure_code",
                    "budget_allocated",
                    "actual_spent",
                    "variance",
                    "variance_pct",
                    "budget_status"
                ]]
                complete_df.columns = [
                    "Measure Code",
                    "Budget Allocated ($)",
                    "Actual Spent ($)",
                    "Variance ($)",
                    "Variance (%)",
                    "Status"
                ]
            st.dataframe(complete_df, use_container_width=True, hide_index=True)
            
            csv_complete = complete_df.to_csv(index=False)
            st.download_button(
                label="📥 Download Complete Dataset (CSV)",
                data=csv_complete,
                file_name=f"budget_variance_complete_{start_date.strftime('%Y%m%d')}_{end_date.strftime('%Y%m%d')}.csv",
                mime="text/csv",
                key="download_complete"
            )
        
        st.divider()
'''
    
    insert_pos = marker_line + 1
    new_lines = lines[:insert_pos] + [additional_viz] + lines[insert_pos:]
    new_content = '\n'.join(new_lines)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    return True, "Enhanced with multiple visualizations and detailed tables"

def enhance_cost_tier_page(file_path):
    """Add multiple visualizations and detailed tables to Cost Tier Comparison page"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find where to insert (after the grouped bar chart)
    marker = 'st.plotly_chart(fig, use_container_width=True, config={\'responsive\': True, \'displayModeBar\': False})'
    pos = content.find(marker)
    if pos == -1:
        return False, "Chart marker not found"
    
    lines = content.split('\n')
    marker_line = -1
    for i, line in enumerate(lines):
        if marker in line:
            marker_line = i
            break
    
    if marker_line == -1:
        return False, "Could not find marker line"
    
    additional_viz = '''
        
        st.divider()
        
        # Additional Visualizations - Multiple Dimensions
        st.header("📊 Additional Analysis Views")
        
        # View 1: Success Rate by Cost Tier
        col1, col2 = st.columns(2)
        with col1:
            if 'success_rate' in df_scaled.columns and 'cost_tier' in df_scaled.columns:
                from utils.charts import create_bar_chart
                fig_success = create_bar_chart(
                    df_scaled,
                    x_col="cost_tier",
                    y_col="success_rate",
                    title="Success Rate by Cost Tier",
                    x_label="Cost Tier",
                    y_label="Success Rate (%)",
                    color_col="success_rate",
                )
                st.plotly_chart(fig_success, use_container_width=True, config={'responsive': True, 'displayModeBar': False})
        
        # View 2: Total Investment by Tier
        with col2:
            if 'total_investment' in df_scaled.columns and 'cost_tier' in df_scaled.columns:
                fig_investment = create_bar_chart(
                    df_scaled,
                    x_col="cost_tier",
                    y_col="total_investment",
                    title="Total Investment by Cost Tier",
                    x_label="Cost Tier",
                    y_label="Total Investment ($)",
                    color_col="total_investment",
                )
                st.plotly_chart(fig_investment, use_container_width=True, config={'responsive': True, 'displayModeBar': False})
        
        st.divider()
        
        # View 3: Cost Efficiency Scatter
        if 'cost_per_closure' in df_scaled.columns and 'success_rate' in df_scaled.columns:
            from utils.charts import create_scatter_plot
            fig_efficiency = create_scatter_plot(
                df_scaled,
                x_col="cost_per_closure",
                y_col="success_rate",
                size_col="interventions_count" if 'interventions_count' in df_scaled.columns else None,
                color_col="cost_tier",
                title="Cost Efficiency: Cost Per Closure vs Success Rate",
                x_label="Cost Per Closure ($)",
                y_label="Success Rate (%)"
            )
            st.plotly_chart(fig_efficiency, use_container_width=True, config={'responsive': True, 'displayModeBar': False})
        
        st.divider()
        
        # Detailed Tables by Dimension
        st.header("📋 Detailed Data Tables by Dimension")
        
        tab1, tab2, tab3, tab4 = st.tabs(["💰 Cost Analysis", "📊 Performance Analysis", "🎯 Tier Comparison", "📈 Complete Dataset"])
        
        with tab1:
            st.subheader("Cost Analysis")
            cost_df = df_scaled[[
                "cost_tier",
                "avg_cost",
                "cost_per_closure",
                "total_investment"
            ]].copy()
            cost_df.columns = [
                "Cost Tier",
                "Average Cost ($)",
                "Cost Per Closure ($)",
                "Total Investment ($)"
            ]
            cost_df = cost_df.sort_values("Cost Per Closure ($)", ascending=True)
            st.dataframe(cost_df, use_container_width=True, hide_index=True)
            
            csv_cost = cost_df.to_csv(index=False)
            st.download_button(
                label="📥 Download Cost Analysis (CSV)",
                data=csv_cost,
                file_name=f"cost_tier_cost_analysis_{start_date.strftime('%Y%m%d')}_{end_date.strftime('%Y%m%d')}.csv",
                mime="text/csv",
                key="download_cost"
            )
        
        with tab2:
            st.subheader("Performance Analysis")
            perf_df = df_scaled[[
                "cost_tier",
                "success_rate",
                "interventions_count",
                "successful_closures"
            ]].copy()
            perf_df.columns = [
                "Cost Tier",
                "Success Rate (%)",
                "Interventions Count",
                "Successful Closures"
            ]
            perf_df = perf_df.sort_values("Success Rate (%)", ascending=False)
            st.dataframe(perf_df, use_container_width=True, hide_index=True)
            
            csv_perf = perf_df.to_csv(index=False)
            st.download_button(
                label="📥 Download Performance Analysis (CSV)",
                data=csv_perf,
                file_name=f"cost_tier_performance_{start_date.strftime('%Y%m%d')}_{end_date.strftime('%Y%m%d')}.csv",
                mime="text/csv",
                key="download_perf"
            )
        
        with tab3:
            st.subheader("Tier Comparison")
            comparison_df = df_scaled.copy()
            comparison_df['efficiency_ratio'] = (comparison_df['success_rate'] / comparison_df['cost_per_closure'] * 100).round(2)
            comparison_df = comparison_df[[
                "cost_tier",
                "avg_cost",
                "cost_per_closure",
                "success_rate",
                "efficiency_ratio",
                "total_investment"
            ]]
            comparison_df.columns = [
                "Cost Tier",
                "Average Cost ($)",
                "Cost Per Closure ($)",
                "Success Rate (%)",
                "Efficiency Ratio",
                "Total Investment ($)"
            ]
            comparison_df = comparison_df.sort_values("Efficiency Ratio", ascending=False)
            st.dataframe(comparison_df, use_container_width=True, hide_index=True)
            
            csv_comp = comparison_df.to_csv(index=False)
            st.download_button(
                label="📥 Download Tier Comparison (CSV)",
                data=csv_comp,
                file_name=f"cost_tier_comparison_{start_date.strftime('%Y%m%d')}_{end_date.strftime('%Y%m%d')}.csv",
                mime="text/csv",
                key="download_comp"
            )
        
        with tab4:
            st.subheader("Complete Dataset")
            complete_df = df_scaled.copy()
            complete_df.columns = [
                "Cost Tier",
                "Interventions Count",
                "Successful Closures",
                "Average Cost ($)",
                "Success Rate (%)",
                "Total Investment ($)",
                "Cost Per Closure ($)"
            ]
            st.dataframe(complete_df, use_container_width=True, hide_index=True)
            
            csv_complete = complete_df.to_csv(index=False)
            st.download_button(
                label="📥 Download Complete Dataset (CSV)",
                data=csv_complete,
                file_name=f"cost_tier_complete_{start_date.strftime('%Y%m%d')}_{end_date.strftime('%Y%m%d')}.csv",
                mime="text/csv",
                key="download_complete"
            )
        
        st.divider()
'''
    
    insert_pos = marker_line + 1
    new_lines = lines[:insert_pos] + [additional_viz] + lines[insert_pos:]
    new_content = '\n'.join(new_lines)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    return True, "Enhanced with multiple visualizations and detailed tables"

def main():
    """Enhance all pages with additional visualizations and tables"""
    pages_dir = Path(__file__).parent / 'pages'
    
    enhancements = [
        ('1_📊_ROI_by_Measure.py', enhance_roi_page),
        ('2_💰_Cost_Per_Closure.py', enhance_cost_per_closure_page),
        ('3_📈_Monthly_Trend.py', enhance_monthly_trend_page),
        ('4_💵_Budget_Variance.py', enhance_budget_variance_page),
        ('5_🎯_Cost_Tier_Comparison.py', enhance_cost_tier_page),
    ]
    
    print("Enhancing all pages with additional visualizations and detailed tables...")
    print("=" * 60)
    
    stats = {'enhanced': 0, 'skipped': 0, 'errors': 0}
    
    for page_name, enhance_func in enhancements:
        page_file = pages_dir / page_name
        if not page_file.exists():
            print(f"[SKIP] {page_name} - File not found")
            stats['skipped'] += 1
            continue
        
        result, info = enhance_func(page_file)
        
        if result is True:
            print(f"[ENHANCED] {page_name} - {info}")
            stats['enhanced'] += 1
        elif result is False:
            print(f"[SKIP] {page_name} - {info}")
            stats['skipped'] += 1
        else:
            print(f"[ERROR] {page_name} - {info}")
            stats['errors'] += 1
    
    print("=" * 60)
    print(f"[SUMMARY]")
    print(f"  Enhanced: {stats['enhanced']}")
    print(f"  Skipped: {stats['skipped']}")
    print(f"  Errors: {stats['errors']}")

if __name__ == '__main__':
    main()

