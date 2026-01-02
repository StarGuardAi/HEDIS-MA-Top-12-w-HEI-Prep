"""
Responsive Layout System for HEDIS Portfolio Optimizer
Universal codebase that adapts to desktop, tablet, and mobile
"""
import streamlit as st
from typing import Dict, List, Optional, Any, Tuple
import plotly.graph_objects as go


# ============================================================================
# DEVICE DETECTION
# ============================================================================

class DeviceDetector:
    """Detect and manage device type for responsive layouts"""
    
    DEVICE_TYPES = ['desktop', 'tablet', 'mobile']
    
    @staticmethod
    def init():
        """Initialize device detection in session state"""
        if 'device_type' not in st.session_state:
            # Default to desktop, allow manual override
            st.session_state.device_type = 'desktop'
        
        if 'auto_detect' not in st.session_state:
            st.session_state.auto_detect = False
    
    @staticmethod
    def get_device_type() -> str:
        """Get current device type from session state"""
        DeviceDetector.init()
        return st.session_state.device_type
    
    @staticmethod
    def set_device_type(device_type: str):
        """Manually set device type"""
        if device_type not in DeviceDetector.DEVICE_TYPES:
            raise ValueError(f"Invalid device type. Must be one of {DeviceDetector.DEVICE_TYPES}")
        
        st.session_state.device_type = device_type
    
    @staticmethod
    def render_device_toggle(show_in_sidebar: bool = True):
        """
        Render device type selector for testing/manual override.
        
        Args:
            show_in_sidebar: Whether to show in sidebar (default: True)
        """
        device_icons = {
            'desktop': '🖥️',
            'tablet': '📱',
            'mobile': '📱'
        }
        
        device_labels = {
            'desktop': 'Desktop',
            'tablet': 'Tablet',
            'mobile': 'Mobile'
        }
        
        current = DeviceDetector.get_device_type()
        
        if show_in_sidebar:
            with st.sidebar:
                st.markdown("### Device Preview")
                col1, col2, col3 = st.columns(3, gap="small")
                
                with col1:
                    if st.button(
                        device_icons['desktop'],
                        type="primary" if current == 'desktop' else "secondary",
                        use_container_width=True,
                        key="device_desktop",
                        help="Desktop view"
                    ):
                        DeviceDetector.set_device_type('desktop')
                        st.rerun()
                
                with col2:
                    if st.button(
                        device_icons['tablet'],
                        type="primary" if current == 'tablet' else "secondary",
                        use_container_width=True,
                        key="device_tablet",
                        help="Tablet view"
                    ):
                        DeviceDetector.set_device_type('tablet')
                        st.rerun()
                
                with col3:
                    if st.button(
                        device_icons['mobile'],
                        type="primary" if current == 'mobile' else "secondary",
                        use_container_width=True,
                        key="device_mobile",
                        help="Mobile view"
                    ):
                        DeviceDetector.set_device_type('mobile')
                        st.rerun()
                
                st.caption(f"Current: {device_labels[current]}")
        else:
            # Show in main area
            st.markdown("### Device Preview")
            col1, col2, col3 = st.columns(3, gap="small")
            
            with col1:
                if st.button(
                    f"{device_icons['desktop']} Desktop",
                    type="primary" if current == 'desktop' else "secondary",
                    use_container_width=True,
                    key="device_desktop_main"
                ):
                    DeviceDetector.set_device_type('desktop')
                    st.rerun()
            
            with col2:
                if st.button(
                    f"{device_icons['tablet']} Tablet",
                    type="primary" if current == 'tablet' else "secondary",
                    use_container_width=True,
                    key="device_tablet_main"
                ):
                    DeviceDetector.set_device_type('tablet')
                    st.rerun()
            
            with col3:
                if st.button(
                    f"{device_icons['mobile']} Mobile",
                    type="primary" if current == 'mobile' else "secondary",
                    use_container_width=True,
                    key="device_mobile_main"
                ):
                    DeviceDetector.set_device_type('mobile')
                    st.rerun()


# ============================================================================
# RESPONSIVE CONFIGURATION
# ============================================================================

class ResponsiveConfig:
    """Device-specific configuration values"""
    
    CONFIGS = {
        'desktop': {
            'chart_height': 600,
            'table_height': 600,
            'font_size_h1': '2.5rem',
            'font_size_h2': '2.0rem',
            'font_size_h3': '1.5rem',
            'font_size_body': '1rem',
            'metric_font_size': '2.5rem',
            'metric_label_size': '1rem',
            'container_padding': '2rem 3rem',
            'show_sidebar': True,
            'use_tabs': True,
            'max_table_columns': None,
            'items_per_page': 50,
            'show_tooltips': True,
            'button_height': 'auto',
            'column_gap': '1rem',
            'card_padding': '1.5rem'
        },
        'tablet': {
            'chart_height': 400,
            'table_height': 500,
            'font_size_h1': '2.0rem',
            'font_size_h2': '1.6rem',
            'font_size_h3': '1.3rem',
            'font_size_body': '1rem',
            'metric_font_size': '2.0rem',
            'metric_label_size': '0.95rem',
            'container_padding': '1.5rem 2rem',
            'show_sidebar': True,
            'use_tabs': True,
            'max_table_columns': 6,
            'items_per_page': 30,
            'show_tooltips': True,
            'button_height': '48px',
            'column_gap': '0.75rem',
            'card_padding': '1rem'
        },
        'mobile': {
            'chart_height': 300,
            'table_height': 400,
            'font_size_h1': '1.8rem',
            'font_size_h2': '1.4rem',
            'font_size_h3': '1.2rem',
            'font_size_body': '1rem',
            'metric_font_size': '2.0rem',
            'metric_label_size': '1rem',
            'container_padding': '1rem 0.5rem',
            'show_sidebar': False,
            'use_tabs': False,
            'max_table_columns': 3,
            'items_per_page': 10,
            'show_tooltips': False,
            'button_height': '48px',
            'column_gap': '0.5rem',
            'card_padding': '0.75rem'
        }
    }
    
    @staticmethod
    def get(key: str, default: Any = None) -> Any:
        """
        Get configuration value for current device.
        
        Args:
            key: Configuration key
            default: Default value if key not found
        
        Returns:
            Configuration value for current device
        """
        device = DeviceDetector.get_device_type()
        return ResponsiveConfig.CONFIGS[device].get(key, default)
    
    @staticmethod
    def get_all() -> Dict[str, Any]:
        """Get all configuration for current device"""
        device = DeviceDetector.get_device_type()
        return ResponsiveConfig.CONFIGS[device].copy()
    
    @staticmethod
    def get_css() -> str:
        """Generate CSS for current device"""
        device = DeviceDetector.get_device_type()
        config = ResponsiveConfig.CONFIGS[device]
        
        css = f"""
        <style>
            /* Container padding */
            .main .block-container {{
                padding: {config['container_padding']} !important;
                max-width: 100% !important;
            }}
            
            /* Typography */
            h1 {{
                font-size: {config['font_size_h1']} !important;
                line-height: 1.2 !important;
            }}
            
            h2 {{
                font-size: {config['font_size_h2']} !important;
                line-height: 1.3 !important;
            }}
            
            h3 {{
                font-size: {config['font_size_h3']} !important;
                line-height: 1.3 !important;
            }}
            
            /* Metrics */
            [data-testid="stMetricValue"] {{
                font-size: {config['metric_font_size']} !important;
                font-weight: 700 !important;
            }}
            
            [data-testid="stMetricLabel"] {{
                font-size: {config['metric_label_size']} !important;
                font-weight: 600 !important;
            }}
            
            /* Buttons */
            .stButton > button {{
                min-height: {config['button_height']} !important;
                font-size: {config['font_size_body']} !important;
            }}
            
            /* Sidebar */
            {'section[data-testid="stSidebar"] { display: none !important; }' 
             if not config['show_sidebar'] else ''}
            
            /* Cards */
            .responsive-card {{
                padding: {config['card_padding']} !important;
                margin-bottom: {config['column_gap']} !important;
            }}
        </style>
        """
        
        return css


# ============================================================================
# RESPONSIVE COLUMN SYSTEM
# ============================================================================

class ResponsiveColumns:
    """Create responsive column layouts"""
    
    def __init__(self):
        """Initialize with current device type"""
        self.device = DeviceDetector.get_device_type()
        self.config = ResponsiveConfig.get_all()
    
    def get_columns(self, desktop: int = 4, tablet: int = 2, mobile: int = 1) -> List:
        """
        Get appropriate number of columns for current device.
        
        Args:
            desktop: Number of columns on desktop (default: 4)
            tablet: Number of columns on tablet (default: 2)
            mobile: Number of columns on mobile (default: 1)
        
        Returns:
            List of Streamlit columns
        """
        if self.device == 'mobile':
            num_cols = mobile
        elif self.device == 'tablet':
            num_cols = tablet
        else:
            num_cols = desktop
        
        return st.columns(num_cols, gap="small")
    
    def metric_grid(self, metrics_data: List[Dict[str, Any]], show_separators: bool = True):
        """
        Display metrics in responsive grid.
        
        Args:
            metrics_data: List of dicts with keys: label, value, delta (optional), help (optional)
            show_separators: Whether to show separators between metrics on mobile (default: True)
        
        Example:
            >>> metrics = [
            ...     {'label': 'ROI', 'value': '498%', 'delta': '+$935K'},
            ...     {'label': 'Star Rating', 'value': '4.5 ⭐', 'delta': '+0.5'}
            ... ]
            >>> rc = ResponsiveColumns()
            >>> rc.metric_grid(metrics)
        """
        if not metrics_data:
            return
        
        cols = self.get_columns(desktop=len(metrics_data), tablet=2, mobile=1)
        
        for idx, metric in enumerate(metrics_data):
            col_idx = idx % len(cols)
            
            with cols[col_idx]:
                st.metric(
                    label=metric.get('label', 'Metric'),
                    value=metric.get('value', 'N/A'),
                    delta=metric.get('delta', None),
                    help=metric.get('help', None) if ResponsiveConfig.get('show_tooltips') else None
                )
                
                # Add separator on mobile
                if self.device == 'mobile' and show_separators and idx < len(metrics_data) - 1:
                    st.markdown("---")
    
    def card_grid(self, cards_data: List[Dict[str, Any]], cards_per_row: Dict[str, int] = None):
        """
        Display cards in responsive grid.
        
        Args:
            cards_data: List of dicts with card content
            cards_per_row: Dict with 'desktop', 'tablet', 'mobile' keys (optional)
        
        Example:
            >>> cards = [
            ...     {'title': 'Card 1', 'content': 'Content 1'},
            ...     {'title': 'Card 2', 'content': 'Content 2'}
            ... ]
            >>> rc = ResponsiveColumns()
            >>> rc.card_grid(cards)
        """
        if not cards_data:
            return
        
        if cards_per_row is None:
            cards_per_row = {'desktop': 3, 'tablet': 2, 'mobile': 1}
        
        cols = self.get_columns(
            desktop=cards_per_row.get('desktop', 3),
            tablet=cards_per_row.get('tablet', 2),
            mobile=cards_per_row.get('mobile', 1)
        )
        
        for idx, card in enumerate(cards_data):
            col_idx = idx % len(cols)
            
            with cols[col_idx]:
                st.markdown(f"""
                <div class="responsive-card" style="
                    background: white;
                    border-radius: 8px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                    border-left: 4px solid #0066cc;
                ">
                    <h4>{card.get('title', 'Card')}</h4>
                    <p>{card.get('content', '')}</p>
                </div>
                """, unsafe_allow_html=True)


# ============================================================================
# RESPONSIVE NAVIGATION
# ============================================================================

class ResponsiveNav:
    """Adaptive navigation system"""
    
    def __init__(self, views: Dict[str, str]):
        """
        Initialize responsive navigation.
        
        Args:
            views: Dict of {label: view_id} pairs
        
        Example:
            >>> views = {
            ...     '📊 Dashboard': 'dashboard',
            ...     '🎯 Opportunities': 'opportunities'
            ... }
            >>> nav = ResponsiveNav(views)
        """
        self.views = views
        self.device = DeviceDetector.get_device_type()
        self.config = ResponsiveConfig.get_all()
    
    def render(self) -> Any:
        """
        Render navigation appropriate for device.
        
        Returns:
            Generator for tabs, or view_id for selectbox
        """
        if self.config['use_tabs']:
            return self._render_tabs()
        else:
            return self._render_selectbox()
    
    def _render_tabs(self):
        """Render tab-based navigation (desktop/tablet)"""
        tabs = st.tabs(list(self.views.keys()))
        
        for idx, (label, view_id) in enumerate(self.views.items()):
            with tabs[idx]:
                yield view_id
    
    def _render_selectbox(self) -> str:
        """Render dropdown navigation (mobile)"""
        if 'current_view' not in st.session_state:
            st.session_state.current_view = list(self.views.values())[0]
        
        # Find current label
        current_view = st.session_state.current_view
        current_label = None
        for label, view_id in self.views.items():
            if view_id == current_view:
                current_label = label
                break
        
        if not current_label:
            current_label = list(self.views.keys())[0]
            st.session_state.current_view = self.views[current_label]
        
        # View selector
        new_label = st.selectbox(
            "Navigate to:",
            options=list(self.views.keys()),
            index=list(self.views.keys()).index(current_label),
            label_visibility="collapsed",
            key="responsive_nav_select"
        )
        
        # Update state if changed
        new_view = self.views[new_label]
        if new_view != st.session_state.current_view:
            st.session_state.current_view = new_view
            st.rerun()
        
        return st.session_state.current_view


# ============================================================================
# RESPONSIVE CHARTS
# ============================================================================

class ResponsiveChart:
    """Create device-adaptive charts"""
    
    @staticmethod
    def get_plotly_config() -> Dict[str, Any]:
        """
        Get Plotly config for current device.
        
        Returns:
            Plotly configuration dictionary
        """
        device = DeviceDetector.get_device_type()
        
        if device == 'mobile':
            return {
                'displayModeBar': False,
                'staticPlot': False,
                'responsive': True,
                'doubleClick': False,
                'showTips': False,
                'scrollZoom': False,
                'displaylogo': False
            }
        elif device == 'tablet':
            return {
                'displayModeBar': True,
                'displaylogo': False,
                'modeBarButtonsToRemove': ['pan2d', 'lasso2d', 'select2d'],
                'responsive': True
            }
        else:  # desktop
            return {
                'displayModeBar': True,
                'displaylogo': False,
                'modeBarButtonsToRemove': ['pan2d', 'lasso2d'],
                'responsive': True
            }
    
    @staticmethod
    def get_layout_updates() -> Dict[str, Any]:
        """
        Get layout updates for current device.
        
        Returns:
            Dictionary of layout updates for Plotly figure
        """
        config = ResponsiveConfig.get_all()
        device = DeviceDetector.get_device_type()
        
        layout = {
            'height': config['chart_height'],
            'font': {
                'size': 11 if device == 'mobile' else 12 if device == 'tablet' else 14,
                'family': 'Arial, sans-serif'
            },
            'showlegend': device != 'mobile',
            'margin': {
                'l': 20 if device == 'mobile' else 40 if device == 'tablet' else 60,
                'r': 20 if device == 'mobile' else 40 if device == 'tablet' else 60,
                't': 30 if device == 'mobile' else 50,
                'b': 20 if device == 'mobile' else 30 if device == 'tablet' else 40
            },
            'paper_bgcolor': 'white',
            'plot_bgcolor': '#f9f9f9' if device == 'mobile' else 'white'
        }
        
        return layout
    
    @staticmethod
    def render(fig: go.Figure, **kwargs) -> None:
        """
        Render Plotly chart with device-appropriate settings.
        
        Args:
            fig: Plotly figure object
            **kwargs: Additional arguments for st.plotly_chart
        
        Example:
            >>> import plotly.express as px
            >>> fig = px.bar(x=[1,2,3], y=[1,2,3])
            >>> ResponsiveChart.render(fig)
        """
        # Apply layout updates
        layout_updates = ResponsiveChart.get_layout_updates()
        fig.update_layout(**layout_updates)
        
        # Render with appropriate config
        config = ResponsiveChart.get_plotly_config()
        
        st.plotly_chart(
            fig,
            use_container_width=True,
            config=config,
            **kwargs
        )


# ============================================================================
# RESPONSIVE TABLES
# ============================================================================

class ResponsiveTable:
    """Create device-adaptive tables"""
    
    @staticmethod
    def render(df, max_columns: Optional[int] = None, height: Optional[int] = None, **kwargs):
        """
        Render DataFrame with device-appropriate settings.
        
        Args:
            df: pandas DataFrame
            max_columns: Maximum columns to show (overrides device default)
            height: Table height (overrides device default)
            **kwargs: Additional arguments for st.dataframe
        
        Example:
            >>> df = pd.DataFrame({'A': [1,2,3], 'B': [4,5,6]})
            >>> ResponsiveTable.render(df)
        """
        config = ResponsiveConfig.get_all()
        
        # Limit columns if needed
        if max_columns is None:
            max_columns = config.get('max_table_columns')
        
        if max_columns and len(df.columns) > max_columns:
            # Show only first N columns
            df_display = df.iloc[:, :max_columns].copy()
            st.caption(f"Showing {max_columns} of {len(df.columns)} columns. Use desktop for full view.")
        else:
            df_display = df
        
        # Set height
        if height is None:
            height = config.get('table_height', 400)
        
        # Render
        st.dataframe(
            df_display,
            use_container_width=True,
            height=height,
            hide_index=True,
            **kwargs
        )


# ============================================================================
# RESPONSIVE BUTTONS
# ============================================================================

class ResponsiveButton:
    """Create device-adaptive buttons"""
    
    @staticmethod
    def render(label: str, key: Optional[str] = None, **kwargs) -> bool:
        """
        Render button with device-appropriate styling.
        
        Args:
            label: Button label
            key: Unique key for button
            **kwargs: Additional arguments for st.button
        
        Returns:
            True if button was clicked
        """
        config = ResponsiveConfig.get_all()
        
        # Set default height for mobile/tablet
        if config.get('button_height') != 'auto':
            # Height is handled by CSS, but we can add styling
            pass
        
        return st.button(
            label,
            key=key,
            use_container_width=True,
            **kwargs
        )


# ============================================================================
# USAGE EXAMPLES
# ============================================================================

def example_responsive_app():
    """
    Complete example of responsive app structure.
    """
    import pandas as pd
    import plotly.express as px
    
    # Page config
    st.set_page_config(
        page_title="HEDIS Portfolio Optimizer",
        page_icon="⭐",
        layout="wide",
        initial_sidebar_state="auto"
    )
    
    # Initialize device detection
    DeviceDetector.init()
    
    # Apply responsive CSS
    st.markdown(ResponsiveConfig.get_css(), unsafe_allow_html=True)
    
    # Device toggle (remove in production or hide)
    with st.sidebar:
        st.markdown("### Device Preview")
        DeviceDetector.render_device_toggle()
        st.markdown("---")
    
    # Header
    st.title("⭐ HEDIS Portfolio Optimizer")
    
    # Responsive metrics
    metrics_data = [
        {'label': 'Potential ROI', 'value': '498%', 'delta': '+$935K annually'},
        {'label': 'Star Rating', 'value': '4.5 ⭐', 'delta': '+0.5 stars'},
        {'label': 'Members', 'value': '10,000+', 'delta': '+1,200 this month'},
        {'label': 'Compliance', 'value': '93%', 'delta': '+8% improvement'}
    ]
    
    rc = ResponsiveColumns()
    rc.metric_grid(metrics_data)
    
    st.markdown("---")
    
    # Responsive navigation
    views = {
        '📊 Dashboard': 'dashboard',
        '🎯 Opportunities': 'opportunities',
        '📈 Measures': 'measures',
        '👥 Members': 'members'
    }
    
    nav = ResponsiveNav(views)
    
    # Route based on device
    if ResponsiveConfig.get('use_tabs'):
        # Tab-based navigation (desktop/tablet)
        tabs = list(nav.render())
        for tab_view_id in tabs:
            if tab_view_id == 'dashboard':
                st.write("Dashboard content")
            elif tab_view_id == 'opportunities':
                st.write("Opportunities content")
            elif tab_view_id == 'measures':
                st.write("Measures content")
            elif tab_view_id == 'members':
                st.write("Members content")
    else:
        # Selectbox navigation (mobile)
        view_id = nav.render()
        
        if view_id == 'dashboard':
            st.write("Dashboard content")
        elif view_id == 'opportunities':
            st.write("Opportunities content")
        elif view_id == 'measures':
            st.write("Measures content")
        elif view_id == 'members':
            st.write("Members content")
    
    st.markdown("---")
    
    # Responsive chart
    sample_data = pd.DataFrame({
        'x': [1, 2, 3, 4, 5],
        'y': [10, 20, 15, 25, 30]
    })
    
    fig = px.line(sample_data, x='x', y='y', title="Sample Chart")
    ResponsiveChart.render(fig)
    
    st.markdown("---")
    
    # Responsive table
    table_data = pd.DataFrame({
        'Measure': ['HbA1c Testing', 'Blood Pressure Control', 'Breast Cancer Screening'],
        'ROI': [1.38, 1.25, 1.32],
        'Members': [847, 623, 512],
        'Value': [285000, 320000, 275000]
    })
    
    ResponsiveTable.render(table_data)


if __name__ == "__main__":
    print("Responsive layout system ready!")
    print("\nUsage:")
    print("from utils.responsive_layout import DeviceDetector, ResponsiveColumns, ResponsiveConfig")
    print("DeviceDetector.init()")
    print("st.markdown(ResponsiveConfig.get_css(), unsafe_allow_html=True)")

