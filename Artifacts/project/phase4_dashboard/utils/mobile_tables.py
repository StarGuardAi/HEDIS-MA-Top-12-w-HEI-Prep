"""
Mobile-Friendly Table Alternatives for HEDIS Portfolio Optimizer
Touch-optimized data display for smartphones (375-428px width)
"""
import streamlit as st
import pandas as pd
from typing import Optional, Dict, Any, List
from datetime import datetime


# ============================================================================
# MOBILE TABLE CONFIGURATION
# ============================================================================

MOBILE_TABLE_CONFIG = {
    'height': 400,
    'use_container_width': True,
    'hide_index': True,
    'column_config': {}
}

# Status emoji mapping
STATUS_EMOJI = {
    'Open': '🔴',
    'Pending': '🟡',
    'Closed': '✅',
    'Excluded': '⚪'
}

# Status color mapping
STATUS_COLOR = {
    'Open': '#cc0000',
    'Pending': '#ffaa00',
    'Closed': '#00cc66',
    'Excluded': '#999999'
}


# ============================================================================
# SOLUTION 1: CARD-BASED LIST VIEW
# ============================================================================

def create_mobile_member_cards(
    df: pd.DataFrame,
    limit: int = 10,
    member_name_col: str = "member_name",
    measure_name_col: str = "measure_name",
    member_id_col: str = "member_id",
    closure_prob_col: str = "predicted_closure_probability",
    financial_value_col: str = "financial_value",
    gap_status_col: str = "gap_status",
    priority_score_col: str = "priority_score"
) -> None:
    """
    Display members as touch-friendly expandable cards instead of table.
    
    Each card shows key information and can be expanded for details.
    Optimized for mobile with large touch targets and clear hierarchy.
    
    Args:
        df: Member DataFrame
        limit: Number of cards to show initially (default: 10)
        member_name_col: Column name for member name
        measure_name_col: Column name for measure name
        member_id_col: Column name for member ID
        closure_prob_col: Column name for closure probability (0-1)
        financial_value_col: Column name for financial value
        gap_status_col: Column name for gap status
        priority_score_col: Column name for priority score
    
    Example:
        >>> df = pd.DataFrame({
        ...     'member_name': ['John Doe', 'Jane Smith'],
        ...     'measure_name': ['HbA1c Testing', 'Blood Pressure Control'],
        ...     'member_id': ['M12345678', 'M12345679'],
        ...     'predicted_closure_probability': [0.93, 0.88],
        ...     'financial_value': [1500, 2000],
        ...     'gap_status': ['Open', 'Pending'],
        ...     'priority_score': [85, 72]
        ... })
        >>> create_mobile_member_cards(df, limit=10)
    """
    if df.empty:
        st.warning("⚠️ No member data available.")
        return
    
    # Initialize session state for limit
    if 'member_card_limit' not in st.session_state:
        st.session_state.member_card_limit = limit
    
    current_limit = st.session_state.member_card_limit
    
    # Show only top N
    mobile_df = df.head(current_limit).copy()
    
    # Display header
    st.markdown(f"### 👥 Top {len(mobile_df)} Members")
    
    if len(df) > current_limit:
        remaining = len(df) - current_limit
        st.caption(f"Showing {current_limit} of {len(df)} members ({remaining} remaining)")
    
    # Create cards
    for idx, row in mobile_df.iterrows():
        # Get status emoji and color
        status = str(row.get(gap_status_col, 'Unknown'))
        status_emoji = STATUS_EMOJI.get(status, '⚪')
        status_color = STATUS_COLOR.get(status, '#999999')
        
        # Card header
        member_name = str(row.get(member_name_col, 'Unknown'))
        measure_name = str(row.get(measure_name_col, 'Unknown'))
        
        # Abbreviate if too long
        if len(member_name) > 25:
            member_name = member_name[:22] + '...'
        if len(measure_name) > 30:
            measure_name = measure_name[:27] + '...'
        
        # Create expandable card
        with st.expander(
            f"{status_emoji} **{member_name}** - {measure_name}",
            expanded=False
        ):
            # Key metrics in columns
            col1, col2 = st.columns(2, gap="small")
            
            with col1:
                # Closure probability
                closure_prob = row.get(closure_prob_col, 0)
                if isinstance(closure_prob, (int, float)):
                    st.metric(
                        "Closure Probability",
                        f"{closure_prob:.0%}",
                        help="Predicted probability of gap closure"
                    )
                
                # Member ID
                member_id = str(row.get(member_id_col, 'N/A'))
                st.caption(f"🆔 Member ID: {member_id}")
            
            with col2:
                # Financial value
                financial_value = row.get(financial_value_col, 0)
                if isinstance(financial_value, (int, float)):
                    st.metric(
                        "Financial Value",
                        f"${financial_value:,.0f}",
                        help="Estimated financial impact"
                    )
                
                # Status
                st.caption(f"📊 Status: **{status}**")
            
            # Additional details
            st.markdown("---")
            
            # Priority score
            priority = row.get(priority_score_col, 0)
            if isinstance(priority, (int, float)):
                priority_color = "#cc0000" if priority >= 75 else "#cc8800" if priority >= 50 else "#999999"
                st.markdown(
                    f"**Priority Score:** "
                    f"<span style='color: {priority_color}; font-weight: 700;'>{int(priority)}</span>",
                    unsafe_allow_html=True
                )
            
            # Action buttons
            st.markdown("---")
            action_col1, action_col2 = st.columns(2, gap="small")
            
            with action_col1:
                if st.button(
                    "📞 Contact",
                    key=f"contact_{idx}_{member_id}",
                    use_container_width=True
                ):
                    st.success(f"📞 Contact action for {member_name}")
                    # In real app: trigger contact workflow
            
            with action_col2:
                if st.button(
                    "📋 Details",
                    key=f"details_{idx}_{member_id}",
                    use_container_width=True
                ):
                    show_member_details(row)
    
    # Load more button
    if len(df) > current_limit:
        st.markdown("---")
        remaining = len(df) - current_limit
        next_limit = min(current_limit + 10, len(df))
        
        if st.button(
            f"⬇️ Load More ({remaining} remaining)",
            use_container_width=True,
            key="load_more_members"
        ):
            st.session_state.member_card_limit = next_limit
            st.rerun()
    
    # Reset button (if showing more than initial limit)
    if current_limit > limit:
        if st.button(
            "🔄 Reset to Top 10",
            use_container_width=True,
            key="reset_members"
        ):
            st.session_state.member_card_limit = limit
            st.rerun()


def show_member_details(row: pd.Series):
    """Show detailed member information in a modal-like view"""
    st.markdown("### 📋 Member Details")
    
    # Display all available fields
    for col, value in row.items():
        if pd.notna(value) and str(value).strip():
            st.markdown(f"**{col.replace('_', ' ').title()}:** {value}")
    
    st.info("💡 Use desktop version for full data export and advanced filtering")


# ============================================================================
# SOLUTION 2: SIMPLIFIED TABLE (3 COLUMNS MAX)
# ============================================================================

def create_mobile_simple_table(
    df: pd.DataFrame,
    member_name_col: str = "member_name",
    gap_status_col: str = "gap_status",
    priority_score_col: str = "priority_score",
    measure_name_col: Optional[str] = None
) -> None:
    """
    Show simplified 3-column table for mobile.
    
    Essential columns only:
    - Member/Measure Name
    - Status (with emoji)
    - Priority Score
    
    Args:
        df: Member DataFrame
        member_name_col: Column name for member/measure name
        gap_status_col: Column name for gap status
        priority_score_col: Column name for priority score
        measure_name_col: Optional column name for measure (if different from member)
    
    Example:
        >>> df = pd.DataFrame({
        ...     'member_name': ['John Doe', 'Jane Smith'],
        ...     'gap_status': ['Open', 'Pending'],
        ...     'priority_score': [85, 72]
        ... })
        >>> create_mobile_simple_table(df)
    """
    if df.empty:
        st.warning("⚠️ No data available.")
        return
    
    # Select essential columns
    mobile_df = df.copy()
    
    # Determine name column
    if measure_name_col and measure_name_col in mobile_df.columns:
        name_col = measure_name_col
        name_label = "Measure"
    else:
        name_col = member_name_col
        name_label = "Member"
    
    # Create simplified dataframe
    simple_df = pd.DataFrame({
        name_label: mobile_df[name_col].apply(lambda x: str(x)[:30] + '...' if len(str(x)) > 30 else str(x)),
        'Status': mobile_df[gap_status_col].apply(
            lambda x: f"{STATUS_EMOJI.get(str(x), '⚪')} {str(x)}"
        ),
        'Priority': mobile_df[priority_score_col].apply(
            lambda x: int(x) if pd.notna(x) and isinstance(x, (int, float)) else 0
        )
    })
    
    # Sort by priority (descending)
    simple_df = simple_df.sort_values('Priority', ascending=False)
    
    # Display with custom styling
    st.markdown("### 📊 Simplified View")
    
    st.dataframe(
        simple_df,
        use_container_width=True,
        height=400,
        hide_index=True,
        column_config={
            name_label: st.column_config.TextColumn(
                name_label,
                width="large",
            ),
            "Status": st.column_config.TextColumn(
                "Status",
                width="medium",
            ),
            "Priority": st.column_config.NumberColumn(
                "Priority",
                width="small",
                format="%d"
            )
        }
    )
    
    # Desktop message
    st.caption("📱 Simplified mobile view - Use desktop for full details and filtering")
    
    # Quick actions
    st.markdown("---")
    col1, col2 = st.columns(2, gap="small")
    
    with col1:
        if st.button("📥 Export This View", use_container_width=True):
            csv = simple_df.to_csv(index=False)
            st.download_button(
                "Download CSV",
                csv,
                f"members_{datetime.now().strftime('%Y%m%d')}.csv",
                "text/csv",
                key="export_simple"
            )
    
    with col2:
        if st.button("🔄 Refresh", use_container_width=True):
            st.rerun()


# ============================================================================
# SOLUTION 3: SUMMARY STATS + DRILL-DOWN
# ============================================================================

def create_mobile_summary_with_drilldown(
    df: pd.DataFrame,
    measure_name_col: str = "measure_name",
    member_id_col: str = "member_id",
    financial_value_col: str = "financial_value",
    closure_prob_col: str = "predicted_closure_probability",
    limit: int = 5
) -> None:
    """
    Show aggregated view by measure, allow drill-down to members.
    
    Displays summary statistics and allows selection of measure
    to view detailed member list.
    
    Args:
        df: Member DataFrame
        measure_name_col: Column name for measure name
        member_id_col: Column name for member ID
        financial_value_col: Column name for financial value
        closure_prob_col: Column name for closure probability
        limit: Number of members to show in drill-down (default: 5)
    
    Example:
        >>> df = pd.DataFrame({
        ...     'measure_name': ['HbA1c Testing', 'Blood Pressure Control'],
        ...     'member_id': ['M1', 'M2'],
        ...     'financial_value': [1500, 2000],
        ...     'predicted_closure_probability': [0.93, 0.88]
        ... })
        >>> create_mobile_summary_with_drilldown(df)
    """
    if df.empty:
        st.warning("⚠️ No data available.")
        return
    
    # Aggregate by measure
    if measure_name_col not in df.columns:
        st.error(f"⚠️ Column '{measure_name_col}' not found in data.")
        return
    
    summary = df.groupby(measure_name_col).agg({
        member_id_col: 'count',
        financial_value_col: 'sum',
        closure_prob_col: 'mean'
    }).round(2)
    
    summary.columns = ['Members', 'Total Value', 'Avg Closure %']
    summary = summary.sort_values('Total Value', ascending=False)
    
    # Format values
    summary['Total Value'] = summary['Total Value'].apply(lambda x: f"${x:,.0f}")
    summary['Avg Closure %'] = summary['Avg Closure %'].apply(lambda x: f"{x*100:.1f}%")
    
    # Display summary
    st.markdown("### 📊 Measures Summary")
    
    st.dataframe(
        summary,
        use_container_width=True,
        height=300,
        hide_index=False,
        column_config={
            measure_name_col: st.column_config.TextColumn(
                "Measure",
                width="large",
            ),
            "Members": st.column_config.NumberColumn(
                "Members",
                width="small",
                format="%d"
            ),
            "Total Value": st.column_config.TextColumn(
                "Total Value",
                width="medium",
            ),
            "Avg Closure %": st.column_config.TextColumn(
                "Avg Closure %",
                width="small",
            )
        }
    )
    
    st.markdown("---")
    
    # Select measure to drill down
    unique_measures = df[measure_name_col].unique().tolist()
    
    if len(unique_measures) > 0:
        st.markdown("### 🔍 View Members by Measure")
        
        selected_measure = st.selectbox(
            "Select Measure:",
            options=unique_measures,
            key="drilldown_measure",
            help="Select a measure to view member details"
        )
        
        if selected_measure:
            measure_df = df[df[measure_name_col] == selected_measure].copy()
            
            st.markdown(f"#### 👥 Members: {selected_measure}")
            st.caption(f"Showing {len(measure_df)} members")
            
            # Show simplified member list using cards
            create_mobile_member_cards(measure_df, limit=limit)
    else:
        st.info("No measures available for drill-down")


# ============================================================================
# SOLUTION 4: SWIPEABLE CARDS (HTML/CSS)
# ============================================================================

def create_swipeable_member_cards(
    df: pd.DataFrame,
    limit: int = 10,
    member_name_col: str = "member_name",
    measure_name_col: str = "measure_name",
    member_id_col: str = "member_id",
    closure_prob_col: str = "predicted_closure_probability",
    financial_value_col: str = "financial_value",
    gap_status_col: str = "gap_status",
    priority_score_col: str = "priority_score"
) -> int:
    """
    Create swipeable cards for mobile using custom HTML/CSS.
    
    Cards are styled for touch interaction with clear visual hierarchy.
    Returns the current limit for pagination.
    
    Args:
        df: Member DataFrame
        limit: Number of cards to show initially (default: 10)
        member_name_col: Column name for member name
        measure_name_col: Column name for measure name
        member_id_col: Column name for member ID
        closure_prob_col: Column name for closure probability
        financial_value_col: Column name for financial value
        gap_status_col: Column name for gap status
        priority_score_col: Column name for priority score
    
    Returns:
        Current limit (for pagination)
    
    Example:
        >>> df = pd.DataFrame({
        ...     'member_name': ['John Doe', 'Jane Smith'],
        ...     'measure_name': ['HbA1c Testing', 'Blood Pressure Control'],
        ...     'member_id': ['M12345678', 'M12345679'],
        ...     'predicted_closure_probability': [0.93, 0.88],
        ...     'financial_value': [1500, 2000],
        ...     'gap_status': ['Open', 'Pending'],
        ...     'priority_score': [85, 72]
        ... })
        >>> current_limit = create_swipeable_member_cards(df, limit=10)
    """
    if df.empty:
        st.warning("⚠️ No member data available.")
        return limit
    
    # Initialize session state
    if 'swipeable_card_limit' not in st.session_state:
        st.session_state.swipeable_card_limit = limit
    
    current_limit = st.session_state.swipeable_card_limit
    
    # Show only top N
    mobile_df = df.head(current_limit).copy()
    
    # CSS and HTML structure
    card_html = """
    <style>
    .member-cards-container {
        display: flex;
        flex-direction: column;
        gap: 1rem;
        margin-bottom: 1rem;
    }
    
    .member-card {
        background: white;
        border: 2px solid #e0e0e0;
        border-radius: 12px;
        padding: 1rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        transition: transform 0.2s, box-shadow 0.2s;
    }
    
    .member-card:active {
        transform: scale(0.98);
        box-shadow: 0 1px 4px rgba(0,0,0,0.15);
    }
    
    .member-card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.75rem;
        padding-bottom: 0.75rem;
        border-bottom: 1px solid #e0e0e0;
    }
    
    .member-name {
        font-weight: 700;
        font-size: 1.1rem;
        color: #0066cc;
        flex: 1;
    }
    
    .member-status {
        font-size: 1.5rem;
        margin-left: 0.5rem;
    }
    
    .member-measure {
        font-size: 0.9rem;
        color: #666;
        margin-top: 0.25rem;
    }
    
    .member-details {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 0.75rem;
        margin-top: 0.75rem;
    }
    
    .detail-item {
        background: #f5f5f5;
        padding: 0.75rem;
        border-radius: 8px;
        text-align: center;
    }
    
    .detail-label {
        font-size: 0.75rem;
        color: #666;
        margin-bottom: 0.25rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .detail-value {
        font-size: 1.2rem;
        font-weight: 700;
        color: #000;
    }
    
    .member-id {
        font-size: 0.8rem;
        color: #999;
        margin-top: 0.5rem;
        text-align: center;
    }
    
    .priority-badge {
        display: inline-block;
        padding: 0.25rem 0.5rem;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-top: 0.5rem;
    }
    
    .priority-high {
        background: #ffcccc;
        color: #cc0000;
    }
    
    .priority-medium {
        background: #fff4cc;
        color: #cc8800;
    }
    
    .priority-low {
        background: #e0e0e0;
        color: #666;
    }
    </style>
    
    <div class="member-cards-container">
    """
    
    # Generate cards
    for idx, row in mobile_df.iterrows():
        # Get values
        member_name = str(row.get(member_name_col, 'Unknown'))
        measure_name = str(row.get(measure_name_col, 'Unknown'))
        member_id = str(row.get(member_id_col, 'N/A'))
        status = str(row.get(gap_status_col, 'Unknown'))
        status_emoji = STATUS_EMOJI.get(status, '⚪')
        status_color = STATUS_COLOR.get(status, '#999999')
        
        closure_prob = row.get(closure_prob_col, 0)
        if isinstance(closure_prob, (int, float)):
            closure_prob_pct = f"{closure_prob*100:.0f}%"
        else:
            closure_prob_pct = "N/A"
        
        financial_value = row.get(financial_value_col, 0)
        if isinstance(financial_value, (int, float)):
            financial_display = f"${financial_value:,.0f}"
        else:
            financial_display = "N/A"
        
        priority = row.get(priority_score_col, 0)
        if isinstance(priority, (int, float)):
            if priority >= 75:
                priority_class = "priority-high"
                priority_label = "High"
            elif priority >= 50:
                priority_class = "priority-medium"
                priority_label = "Medium"
            else:
                priority_class = "priority-low"
                priority_label = "Low"
        else:
            priority_class = "priority-low"
            priority_label = "N/A"
        
        # Abbreviate if too long
        if len(member_name) > 25:
            member_name = member_name[:22] + '...'
        if len(measure_name) > 30:
            measure_name = measure_name[:27] + '...'
        
        # Create card HTML
        card_html += f"""
        <div class="member-card">
            <div class="member-card-header">
                <div>
                    <div class="member-name">{member_name}</div>
                    <div class="member-measure">{measure_name}</div>
                </div>
                <div class="member-status">{status_emoji}</div>
            </div>
            
            <div class="member-details">
                <div class="detail-item">
                    <div class="detail-label">Closure Rate</div>
                    <div class="detail-value">{closure_prob_pct}</div>
                </div>
                <div class="detail-item">
                    <div class="detail-label">Value</div>
                    <div class="detail-value">{financial_display}</div>
                </div>
            </div>
            
            <div style="text-align: center;">
                <span class="priority-badge {priority_class}">Priority: {priority_label}</span>
            </div>
            
            <div class="member-id">🆔 {member_id}</div>
        </div>
        """
    
    card_html += "</div>"
    
    # Render HTML
    st.markdown(f"### 👥 Members ({len(mobile_df)} shown)")
    st.markdown(card_html, unsafe_allow_html=True)
    
    # Load more button
    if len(df) > current_limit:
        st.markdown("---")
        remaining = len(df) - current_limit
        next_limit = min(current_limit + 10, len(df))
        
        if st.button(
            f"⬇️ Load 10 More ({remaining} remaining)",
            use_container_width=True,
            key="load_more_swipeable"
        ):
            st.session_state.swipeable_card_limit = next_limit
            return next_limit
    
    return current_limit


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_mobile_table_recommendation(df_size: int) -> str:
    """
    Recommend which mobile table solution to use based on data size.
    
    Args:
        df_size: Number of rows in DataFrame
    
    Returns:
        Recommendation string
    """
    if df_size <= 20:
        return "Use card-based view - best for small lists"
    elif df_size <= 100:
        return "Use summary with drill-down - best for medium lists"
    elif df_size <= 500:
        return "Use simplified table - best for larger lists"
    else:
        return "Use summary view only - too large for mobile detail view"


# ============================================================================
# USAGE EXAMPLES
# ============================================================================

def example_mobile_tables():
    """
    Example usage of all mobile table functions.
    """
    # Sample data
    sample_data = {
        'member_name': [f'Member {i}' for i in range(1, 51)],
        'measure_name': ['HbA1c Testing'] * 25 + ['Blood Pressure Control'] * 25,
        'member_id': [f'M{i:08d}' for i in range(1, 51)],
        'predicted_closure_probability': [0.3 + (i % 7) * 0.1 for i in range(50)],
        'financial_value': [1000 + i * 50 for i in range(50)],
        'gap_status': ['Open'] * 20 + ['Pending'] * 20 + ['Closed'] * 10,
        'priority_score': [50 + (i % 50) for i in range(50)]
    }
    
    df = pd.DataFrame(sample_data)
    
    st.title("Mobile Table Examples")
    
    # Example 1: Card-based view
    st.markdown("## 1. Card-Based View")
    create_mobile_member_cards(df, limit=10)
    
    st.markdown("---")
    
    # Example 2: Simplified table
    st.markdown("## 2. Simplified Table")
    create_mobile_simple_table(df)
    
    st.markdown("---")
    
    # Example 3: Summary with drill-down
    st.markdown("## 3. Summary with Drill-Down")
    create_mobile_summary_with_drilldown(df)
    
    st.markdown("---")
    
    # Example 4: Swipeable cards
    st.markdown("## 4. Swipeable Cards")
    current_limit = create_swipeable_member_cards(df, limit=10)
    st.caption(f"Currently showing {current_limit} cards")


if __name__ == "__main__":
    print("Mobile table functions ready!")
    print("\nUsage:")
    print("from utils.mobile_tables import create_mobile_member_cards")
    print("create_mobile_member_cards(df, limit=10)")

