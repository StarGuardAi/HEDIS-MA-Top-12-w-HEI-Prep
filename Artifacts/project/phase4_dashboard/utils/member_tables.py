"""
Interactive Data Tables for HEDIS Member Management
Production-ready AgGrid implementations for healthcare managers
"""
import pandas as pd
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, JsCode, ColumnsAutoSizeMode
from typing import Tuple, Optional, Dict, Any
from datetime import datetime


def create_member_grid(
    df: pd.DataFrame,
    height: int = 600,
    theme: str = 'streamlit',
    enable_sidebar: bool = True,
    enable_grouping: bool = True,
    enable_pagination: bool = True,
    page_size: int = 50
) -> Tuple[Any, pd.DataFrame]:
    """
    Create interactive master member list table with full Excel-like features.
    
    Features:
    - Multi-row selection with checkboxes
    - Column grouping by measure_name
    - Row grouping capability
    - Inline editing for assigned_care_coordinator
    - Column pinning (member_id always visible)
    - Sidebar filters for all columns
    - Color coding by gap_status
    - Formatted currency and dates
    - Priority badge column
    - Aggregation footer
    
    Args:
        df: Member-level DataFrame with required columns:
            - member_id: String
            - member_name: String (PHI)
            - date_of_birth: Date
            - measure_name: String
            - gap_status: String ("Open", "Pending", "Closed", "Excluded")
            - predicted_closure_probability: Float 0-1
            - financial_value: Float
            - last_contact_date: Date
            - assigned_care_coordinator: String
            - priority_score: Integer 1-100
            - days_until_deadline: Integer
        height: Grid height in pixels (default: 600)
        theme: AgGrid theme ('streamlit' or 'alpine', default: 'streamlit')
        enable_sidebar: Enable sidebar filters (default: True)
        enable_grouping: Enable row grouping (default: True)
        enable_pagination: Enable pagination (default: True)
        page_size: Rows per page (default: 50)
    
    Returns:
        tuple: (AgGrid response object, selected_rows_dataframe)
    
    Example:
        >>> df = pd.DataFrame({
        ...     'member_id': ['M12345678', 'M12345679'],
        ...     'member_name': ['John Doe', 'Jane Smith'],
        ...     'gap_status': ['Open', 'Pending'],
        ...     'financial_value': [1500.50, 2000.00],
        ...     'priority_score': [85, 60]
        ... })
        >>> grid_response, selected = create_member_grid(df)
        >>> if len(selected) > 0:
        ...     st.success(f"Selected {len(selected)} members")
    """
    # Validate DataFrame
    if df.empty:
        st.warning("⚠️ No member data available.")
        return None, pd.DataFrame()
    
    # Required columns check
    required_cols = [
        'member_id', 'member_name', 'date_of_birth', 'measure_name',
        'gap_status', 'predicted_closure_probability', 'financial_value',
        'last_contact_date', 'assigned_care_coordinator', 'priority_score',
        'days_until_deadline'
    ]
    
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        st.error(f"⚠️ Missing required columns: {missing_cols}")
        return None, pd.DataFrame()
    
    # Create a copy to avoid modifying original
    df_work = df.copy()
    
    # Add calculated Priority badge column
    def get_priority_badge(score: int) -> str:
        """Convert priority score to badge label"""
        if pd.isna(score):
            return "Low"
        if score >= 75:
            return "High"
        elif score >= 50:
            return "Medium"
        else:
            return "Low"
    
    df_work['priority_badge'] = df_work['priority_score'].apply(get_priority_badge)
    
    # Format dates for display
    date_cols = ['date_of_birth', 'last_contact_date']
    for col in date_cols:
        if col in df_work.columns:
            df_work[col] = pd.to_datetime(df_work[col], errors='coerce').dt.strftime('%m/%d/%Y')
    
    # Format predicted_closure_probability as percentage
    if 'predicted_closure_probability' in df_work.columns:
        df_work['predicted_closure_probability'] = (
            df_work['predicted_closure_probability'] * 100
        ).round(1)
    
    # Build grid options
    gb = GridOptionsBuilder.from_dataframe(df_work)
    
    # ========================================================================
    # COLUMN CONFIGURATION
    # ========================================================================
    
    # Pin member_id column (always visible)
    gb.configure_column(
        'member_id',
        pinned='left',
        width=120,
        headerCheckboxSelection=True,
        checkboxSelection=True,
        lockPosition='left'
    )
    
    # Member name (PHI - handle carefully)
    gb.configure_column(
        'member_name',
        width=150,
        editable=False
    )
    
    # Date columns
    gb.configure_column(
        'date_of_birth',
        width=120,
        type=['dateColumn'],
        filter='agDateColumnFilter'
    )
    
    gb.configure_column(
        'last_contact_date',
        width=130,
        type=['dateColumn'],
        filter='agDateColumnFilter'
    )
    
    # Measure name - enable grouping
    gb.configure_column(
        'measure_name',
        width=200,
        rowGroup=enable_grouping,
        hide=enable_grouping,  # Hide when grouped, show in group panel
        enableRowGroup=enable_grouping,
        filter='agTextColumnFilter'
    )
    
    # Gap status with color coding
    gap_status_cell_renderer = JsCode("""
        function(params) {
            const status = params.value;
            let color = '#999999';
            let bgColor = '#f0f0f0';
            
            if (status === 'Open') {
                color = '#cc0000';
                bgColor = '#ffcccc';
            } else if (status === 'Pending') {
                color = '#cc8800';
                bgColor = '#fff4cc';
            } else if (status === 'Closed') {
                color = '#00cc66';
                bgColor = '#ccffcc';
            } else if (status === 'Excluded') {
                color = '#666666';
                bgColor = '#e0e0e0';
            }
            
            return `<span style="
                background-color: ${bgColor};
                color: ${color};
                padding: 4px 8px;
                border-radius: 12px;
                font-weight: 600;
                font-size: 11px;
                display: inline-block;
            ">${status}</span>`;
        }
    """)
    
    gb.configure_column(
        'gap_status',
        width=120,
        cellRenderer=gap_status_cell_renderer,
        filter='agTextColumnFilter',
        filterParams={'filterOptions': ['equals', 'notEqual']}
    )
    
    # Predicted closure probability (percentage)
    gb.configure_column(
        'predicted_closure_probability',
        width=180,
        type=['numericColumn'],
        valueFormatter="params.value + '%'",
        filter='agNumberColumnFilter',
        aggFunc='avg'
    )
    
    # Financial value (currency)
    financial_value_cell_renderer = JsCode("""
        function(params) {
            if (params.value == null) return '';
            const value = parseFloat(params.value);
            return '$' + value.toLocaleString('en-US', {
                minimumFractionDigits: 2,
                maximumFractionDigits: 2
            });
        }
    """)
    
    gb.configure_column(
        'financial_value',
        width=140,
        type=['numericColumn'],
        cellRenderer=financial_value_cell_renderer,
        filter='agNumberColumnFilter',
        aggFunc='sum',
        valueGetter="params.data.financial_value"
    )
    
    # Assigned care coordinator (editable)
    gb.configure_column(
        'assigned_care_coordinator',
        width=180,
        editable=True,
        filter='agTextColumnFilter',
        cellEditor='agTextCellEditor'
    )
    
    # Priority score
    gb.configure_column(
        'priority_score',
        width=120,
        type=['numericColumn'],
        filter='agNumberColumnFilter',
        sort='desc'  # Default sort by priority
    )
    
    # Priority badge (calculated column)
    priority_badge_cell_renderer = JsCode("""
        function(params) {
            const badge = params.value;
            let color = '#666666';
            let bgColor = '#e0e0e0';
            
            if (badge === 'High') {
                color = '#cc0000';
                bgColor = '#ffcccc';
            } else if (badge === 'Medium') {
                color = '#cc8800';
                bgColor = '#fff4cc';
            } else {
                color = '#666666';
                bgColor = '#e0e0e0';
            }
            
            return `<span style="
                background-color: ${bgColor};
                color: ${color};
                padding: 4px 8px;
                border-radius: 12px;
                font-weight: 600;
                font-size: 11px;
                display: inline-block;
            ">${badge}</span>`;
        }
    """)
    
    gb.configure_column(
        'priority_badge',
        width=100,
        cellRenderer=priority_badge_cell_renderer,
        filter='agTextColumnFilter'
    )
    
    # Days until deadline
    days_deadline_cell_renderer = JsCode("""
        function(params) {
            const days = params.value;
            if (days == null) return '';
            let color = '#cc0000';
            if (days > 30) color = '#00cc66';
            else if (days > 14) color = '#cc8800';
            
            return `<span style="color: ${color}; font-weight: 600;">${days} days</span>`;
        }
    """)
    
    gb.configure_column(
        'days_until_deadline',
        width=140,
        cellRenderer=days_deadline_cell_renderer,
        type=['numericColumn'],
        filter='agNumberColumnFilter'
    )
    
    # ========================================================================
    # GRID OPTIONS CONFIGURATION
    # ========================================================================
    
    gb.configure_selection(
        'multiple',
        use_checkbox=True,
        header_checkbox=True,
        pre_selected_rows=[],
        rowMultiSelectWithClick=True
    )
    
    gb.configure_pagination(
        enabled=enable_pagination,
        paginationAutoPageSize=False,
        paginationPageSize=page_size
    )
    
    gb.configure_side_bar(
        filters_panel=enable_sidebar,
        columns_panel=enable_sidebar,
        defaultToolPanel='filters',
        toolPanelParams={'suppressRowGroups': False, 'suppressValues': False}
    )
    
    gb.configure_grid_options(
        enableRangeSelection=True,
        enableCharts=True,
        enableRangeHandle=True,
        rowGroupPanelShow='always' if enable_grouping else 'never',
        pivotPanelShow='always' if enable_grouping else 'never',
        sideBar=enable_sidebar,
        suppressRowClickSelection=False,
        rowSelection='multiple',
        animateRows=True,
        enableCellTextSelection=True,
        ensureDomOrder=True,
        suppressAggFuncInHeader=False,
        suppressMenuHide=True,
        enableStatusBar=True,
        statusBar={
            'statusPanels': [
                {'statusPanel': 'agTotalAndFilteredRowCountComponent'},
                {'statusPanel': 'agTotalRowCountComponent'},
                {'statusPanel': 'agFilteredRowCountComponent'},
                {'statusPanel': 'agSelectedRowCountComponent'},
                {'statusPanel': 'agAggregationComponent'}
            ]
        },
        defaultColDef={
            'sortable': True,
            'filter': True,
            'resizable': True,
            'enableRowGroup': enable_grouping,
            'enablePivot': enable_grouping,
            'enableValue': True,
            'floatingFilter': True
        }
    )
    
    # Auto-size columns
    gb.configure_columns_auto_size_mode(ColumnsAutoSizeMode.FIT_CONTENTS)
    
    # Build grid options
    gridOptions = gb.build()
    
    # ========================================================================
    # RENDER GRID
    # ========================================================================
    
    grid_response = AgGrid(
        df_work,
        gridOptions=gridOptions,
        height=height,
        width='100%',
        theme=theme,
        update_mode=GridUpdateMode.SELECTION_CHANGED | GridUpdateMode.VALUE_CHANGED,
        allow_unsafe_jscode=True,
        enable_enterprise_modules=False,  # Set to True if you have enterprise license
        custom_css="""
            .ag-theme-streamlit {
                --ag-header-background-color: #0066cc;
                --ag-header-foreground-color: white;
                --ag-odd-row-background-color: #f8f9fa;
                --ag-row-hover-color: #e3f2fd;
                --ag-selected-row-background-color: #b3d9ff;
            }
            .ag-status-bar {
                background-color: #f0f4f8;
                border-top: 1px solid #e0e0e0;
            }
        """
    )
    
    # Extract selected rows
    selected_rows = pd.DataFrame(grid_response['selected_rows']) if grid_response['selected_rows'] else pd.DataFrame()
    
    return grid_response, selected_rows


def create_summary_grid(
    df: pd.DataFrame,
    height: int = 400,
    theme: str = 'streamlit',
    page_size: int = 20
) -> Tuple[Any, Optional[Dict[str, Any]]]:
    """
    Create simplified summary measures table (read-only, aggregated view).
    
    Features:
    - Aggregated view by measure_name
    - Sortable, filterable columns
    - Conditional formatting by thresholds
    - Click row to drill down
    - Quick search box
    - Auto-fit columns
    
    Args:
        df: Member-level DataFrame (will be aggregated by measure_name)
        height: Grid height in pixels (default: 400)
        theme: AgGrid theme ('streamlit' or 'alpine', default: 'streamlit')
        page_size: Rows per page (default: 20)
    
    Returns:
        tuple: (AgGrid response object, clicked_row_dict or None)
    
    Example:
        >>> df = pd.DataFrame({
        ...     'measure_name': ['HbA1c Testing', 'Blood Pressure Control'],
        ...     'gap_status': ['Open', 'Open'],
        ...     'financial_value': [1500, 2000]
        ... })
        >>> grid_response, clicked_row = create_summary_grid(df)
        >>> if clicked_row:
        ...     measure = clicked_row['measure_name']
        ...     st.info(f"Selected measure: {measure}")
    """
    # Validate DataFrame
    if df.empty:
        st.warning("⚠️ No data available for summary.")
        return None, None
    
    # Required columns check
    required_cols = ['measure_name', 'gap_status', 'financial_value', 'predicted_closure_probability']
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        st.error(f"⚠️ Missing required columns: {missing_cols}")
        return None, None
    
    # Aggregate data by measure_name
    summary_df = df.groupby('measure_name').agg({
        'member_id': 'count',
        'gap_status': lambda x: (x == 'Open').sum(),
        'predicted_closure_probability': 'mean',
        'financial_value': 'sum'
    }).reset_index()
    
    # Rename columns for clarity
    summary_df.columns = [
        'Measure',
        'Total Members',
        'Open Gaps',
        'Predicted Closure Rate',
        'Total Value'
    ]
    
    # Format predicted closure rate as percentage
    summary_df['Predicted Closure Rate'] = (summary_df['Predicted Closure Rate'] * 100).round(1)
    
    # Calculate closure rate percentage
    summary_df['Closure Rate %'] = (
        (summary_df['Total Members'] - summary_df['Open Gaps']) / summary_df['Total Members'] * 100
    ).round(1)
    
    # Build grid options
    gb = GridOptionsBuilder.from_dataframe(summary_df)
    
    # ========================================================================
    # COLUMN CONFIGURATION
    # ========================================================================
    
    # Measure name
    gb.configure_column(
        'Measure',
        width=250,
        pinned='left',
        lockPosition='left',
        filter='agTextColumnFilter',
        cellStyle={'fontWeight': '600'}
    )
    
    # Total Members
    gb.configure_column(
        'Total Members',
        width=130,
        type=['numericColumn'],
        filter='agNumberColumnFilter',
        aggFunc='sum'
    )
    
    # Open Gaps
    open_gaps_cell_renderer = JsCode("""
        function(params) {
            const value = params.value;
            const total = params.data['Total Members'];
            const pct = total > 0 ? (value / total * 100).toFixed(1) : 0;
            
            let color = '#00cc66';
            if (pct > 50) color = '#cc0000';
            else if (pct > 25) color = '#cc8800';
            
            return `<span style="color: ${color}; font-weight: 600;">${value} <span style="color: #666; font-size: 0.9em;">(${pct}%)</span></span>`;
        }
    """)
    
    gb.configure_column(
        'Open Gaps',
        width=140,
        type=['numericColumn'],
        cellRenderer=open_gaps_cell_renderer,
        filter='agNumberColumnFilter',
        aggFunc='sum'
    )
    
    # Predicted Closure Rate with conditional formatting
    closure_rate_cell_renderer = JsCode("""
        function(params) {
            const value = params.value;
            if (value == null) return '';
            
            let color = '#cc0000';
            let bgColor = '#ffcccc';
            if (value >= 50) {
                color = '#00cc66';
                bgColor = '#ccffcc';
            } else if (value >= 30) {
                color = '#cc8800';
                bgColor = '#fff4cc';
            }
            
            return `<span style="
                background-color: ${bgColor};
                color: ${color};
                padding: 4px 8px;
                border-radius: 12px;
                font-weight: 600;
                font-size: 11px;
                display: inline-block;
            ">${value.toFixed(1)}%</span>`;
        }
    """)
    
    gb.configure_column(
        'Predicted Closure Rate',
        width=180,
        type=['numericColumn'],
        cellRenderer=closure_rate_cell_renderer,
        filter='agNumberColumnFilter',
        aggFunc='avg',
        sort='desc'  # Default sort by predicted rate
    )
    
    # Closure Rate % (calculated)
    gb.configure_column(
        'Closure Rate %',
        width=140,
        type=['numericColumn'],
        valueFormatter="params.value + '%'",
        filter='agNumberColumnFilter',
        aggFunc='avg'
    )
    
    # Total Value (currency)
    total_value_cell_renderer = JsCode("""
        function(params) {
            if (params.value == null) return '';
            const value = parseFloat(params.value);
            return '<span style="font-weight: 600; color: #0066cc;">$' + 
                   value.toLocaleString('en-US', {
                       minimumFractionDigits: 2,
                       maximumFractionDigits: 2
                   }) + '</span>';
        }
    """)
    
    gb.configure_column(
        'Total Value',
        width=150,
        type=['numericColumn'],
        cellRenderer=total_value_cell_renderer,
        filter='agNumberColumnFilter',
        aggFunc='sum'
    )
    
    # ========================================================================
    # GRID OPTIONS CONFIGURATION
    # ========================================================================
    
    gb.configure_selection('single')  # Single row selection for drill-down
    
    gb.configure_pagination(
        enabled=True,
        paginationAutoPageSize=False,
        paginationPageSize=page_size
    )
    
    gb.configure_grid_options(
        enableRangeSelection=False,
        suppressRowClickSelection=False,
        rowSelection='single',
        animateRows=True,
        enableCellTextSelection=True,
        ensureDomOrder=True,
        suppressMenuHide=True,
        enableStatusBar=True,
        statusBar={
            'statusPanels': [
                {'statusPanel': 'agTotalAndFilteredRowCountComponent'},
                {'statusPanel': 'agTotalRowCountComponent'},
                {'statusPanel': 'agFilteredRowCountComponent'}
            ]
        },
        defaultColDef={
            'sortable': True,
            'filter': True,
            'resizable': True,
            'floatingFilter': True
        },
        onRowClicked=JsCode("""
            function(params) {
                // Row click handled by Streamlit
                // Selection will be available in grid_response['selected_rows']
            }
        """)
    )
    
    # Auto-size columns
    gb.configure_columns_auto_size_mode(ColumnsAutoSizeMode.FIT_CONTENTS)
    
    # Build grid options
    gridOptions = gb.build()
    
    # ========================================================================
    # RENDER GRID
    # ========================================================================
    
    grid_response = AgGrid(
        summary_df,
        gridOptions=gridOptions,
        height=height,
        width='100%',
        theme=theme,
        update_mode=GridUpdateMode.SELECTION_CHANGED,
        allow_unsafe_jscode=True,
        enable_enterprise_modules=False,
        custom_css="""
            .ag-theme-streamlit {
                --ag-header-background-color: #0066cc;
                --ag-header-foreground-color: white;
                --ag-odd-row-background-color: #f8f9fa;
                --ag-row-hover-color: #e3f2fd;
                --ag-selected-row-background-color: #b3d9ff;
            }
            .ag-status-bar {
                background-color: #f0f4f8;
                border-top: 1px solid #e0e0e0;
            }
        """
    )
    
    # Extract clicked/selected row
    selected_rows = grid_response['selected_rows']
    clicked_row = selected_rows[0] if selected_rows else None
    
    return grid_response, clicked_row


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def export_selected_to_excel_format(selected_df: pd.DataFrame) -> pd.DataFrame:
    """
    Format selected rows DataFrame for Excel export.
    
    Restores original formatting (dates, currency, percentages) for export.
    
    Args:
        selected_df: DataFrame from selected rows
    
    Returns:
        Formatted DataFrame ready for Excel export
    """
    if selected_df.empty:
        return pd.DataFrame()
    
    export_df = selected_df.copy()
    
    # Restore date formatting if needed
    date_cols = ['date_of_birth', 'last_contact_date']
    for col in date_cols:
        if col in export_df.columns:
            # Convert back to datetime if needed
            export_df[col] = pd.to_datetime(export_df[col], errors='coerce')
    
    # Ensure financial_value is numeric
    if 'financial_value' in export_df.columns:
        export_df['financial_value'] = pd.to_numeric(export_df['financial_value'], errors='coerce')
    
    # Ensure predicted_closure_probability is percentage (0-100)
    if 'predicted_closure_probability' in export_df.columns:
        export_df['predicted_closure_probability'] = pd.to_numeric(
            export_df['predicted_closure_probability'], errors='coerce'
        )
    
    return export_df


def get_selection_summary(selected_df: pd.DataFrame) -> Dict[str, Any]:
    """
    Get summary statistics for selected members.
    
    Args:
        selected_df: DataFrame from selected rows
    
    Returns:
        Dictionary with summary statistics
    """
    if selected_df.empty:
        return {
            'count': 0,
            'total_financial_value': 0,
            'avg_priority_score': 0,
            'gap_status_counts': {},
            'measures': []
        }
    
    summary = {
        'count': len(selected_df),
        'total_financial_value': selected_df['financial_value'].sum() if 'financial_value' in selected_df.columns else 0,
        'avg_priority_score': selected_df['priority_score'].mean() if 'priority_score' in selected_df.columns else 0,
        'gap_status_counts': selected_df['gap_status'].value_counts().to_dict() if 'gap_status' in selected_df.columns else {},
        'measures': selected_df['measure_name'].unique().tolist() if 'measure_name' in selected_df.columns else []
    }
    
    return summary

