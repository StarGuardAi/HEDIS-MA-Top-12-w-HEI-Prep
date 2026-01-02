"""
Mobile Navigation System for HEDIS Portfolio Optimizer
Complete navigation with state management, deep linking, and modals
"""
import streamlit as st
from datetime import datetime
from typing import Optional, Dict, Any, Callable
import urllib.parse


# ============================================================================
# MOBILE NAVIGATION STATE INITIALIZATION
# ============================================================================

def init_mobile_state():
    """
    Initialize all session state variables for mobile navigation.
    
    Sets up default values for navigation, views, filters, and UI state.
    """
    defaults = {
        # Navigation
        'current_view': 'dashboard',
        'nav_history': [],
        'previous_view': None,
        
        # Context
        'selected_measure': None,
        'selected_member_id': None,
        'selected_measure_name': None,
        
        # Filters
        'filter_preset': 'default',
        'mobile_filters': {},
        
        # UI State
        'show_export': False,
        'show_share': False,
        'show_help': False,
        'show_menu': False,
        'show_filters': False,
        
        # Data State
        'member_card_limit': 10,
        'swipeable_card_limit': 10,
        'table_limit': 20,
        
        # Metadata
        'last_updated': None,
        'last_nav_time': None,
        'view_count': {}
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
    
    # Initialize view count
    if 'current_view' in st.session_state:
        view = st.session_state.current_view
        if view not in st.session_state.view_count:
            st.session_state.view_count[view] = 0


# ============================================================================
# MOBILE NAVIGATION HEADER
# ============================================================================

def create_mobile_nav_header(show_menu_button: bool = True):
    """
    Create sticky mobile navigation header with logo and menu button.
    
    Args:
        show_menu_button: Whether to show hamburger menu button (default: True)
    """
    header_css = """
    <style>
    .mobile-header {
        position: sticky;
        top: 0;
        z-index: 999;
        background: white;
        border-bottom: 2px solid #0066cc;
        padding: 0.75rem 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    
    .mobile-header-content {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .mobile-logo {
        font-size: 1.3rem;
        font-weight: 700;
        color: #0066cc;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .mobile-menu-btn {
        font-size: 1.5rem;
        cursor: pointer;
        color: #0066cc;
        background: none;
        border: none;
        padding: 0.25rem 0.5rem;
    }
    
    .mobile-header-actions {
        display: flex;
        gap: 0.5rem;
        align-items: center;
    }
    
    .mobile-badge {
        background: #0066cc;
        color: white;
        border-radius: 12px;
        padding: 0.25rem 0.5rem;
        font-size: 0.75rem;
        font-weight: 600;
    }
    </style>
    """
    
    st.markdown(header_css, unsafe_allow_html=True)
    
    # Get last updated time
    last_updated = st.session_state.get('last_updated')
    time_ago = get_time_ago(last_updated) if last_updated else "Just now"
    
    # Header HTML
    header_html = f"""
    <div class="mobile-header">
        <div class="mobile-header-content">
            <div class="mobile-logo">
                ⭐ HEDIS
            </div>
            <div class="mobile-header-actions">
                <span class="mobile-badge">{time_ago}</span>
                {"<button class='mobile-menu-btn' onclick='document.getElementById(\"menu-toggle\").click()'>☰</button>" if show_menu_button else ""}
            </div>
        </div>
    </div>
    """
    
    st.markdown(header_html, unsafe_allow_html=True)
    
    # Hidden button for menu toggle (handled by Streamlit)
    if show_menu_button:
        st.markdown('<button id="menu-toggle" style="display:none;"></button>', unsafe_allow_html=True)


def get_time_ago(timestamp: Optional[datetime]) -> str:
    """Get human-readable time ago string"""
    if not timestamp:
        return "Just now"
    
    delta = datetime.now() - timestamp
    
    if delta.days > 0:
        return f"{delta.days}d ago"
    elif delta.seconds > 3600:
        hours = delta.seconds // 3600
        return f"{hours}h ago"
    elif delta.seconds > 60:
        minutes = delta.seconds // 60
        return f"{minutes}m ago"
    else:
        return "Just now"


# ============================================================================
# VIEW SELECTOR (PRIMARY NAVIGATION)
# ============================================================================

def mobile_view_selector() -> str:
    """
    Main navigation using selectbox for view selection.
    
    Returns:
        Current view identifier (e.g., 'dashboard', 'opportunities')
    """
    views = {
        "📊 Dashboard": "dashboard",
        "🎯 Top Opportunities": "opportunities",
        "📈 Measure Deep-Dive": "measures",
        "👥 Member Lists": "members",
        "💰 ROI Analysis": "roi",
        "🔒 Secure Query": "secure_query",
        "⚙️ Settings": "settings"
    }
    
    # Get current view from session state
    if 'current_view' not in st.session_state:
        st.session_state.current_view = "dashboard"
    
    # Find current label
    current_view = st.session_state.current_view
    current_label = None
    for label, view_id in views.items():
        if view_id == current_view:
            current_label = label
            break
    
    if not current_label:
        current_label = list(views.keys())[0]
        st.session_state.current_view = views[current_label]
    
    # View selector
    selected_label = st.selectbox(
        "Navigation",
        options=list(views.keys()),
        index=list(views.keys()).index(current_label),
        label_visibility="collapsed",
        key="nav_selector"
    )
    
    # Update state if changed
    new_view = views[selected_label]
    if new_view != st.session_state.current_view:
        # Save previous view
        st.session_state.previous_view = st.session_state.current_view
        st.session_state.current_view = new_view
        
        # Update view count
        if new_view not in st.session_state.view_count:
            st.session_state.view_count[new_view] = 0
        st.session_state.view_count[new_view] += 1
        
        # Update navigation time
        st.session_state.last_nav_time = datetime.now()
        
        # Rerun to load new view
        st.rerun()
    
    return st.session_state.current_view


# ============================================================================
# HAMBURGER MENU (SECONDARY OPTIONS)
# ============================================================================

def mobile_hamburger_menu():
    """
    Collapsible menu for secondary actions and account options.
    """
    with st.expander("☰ Menu", expanded=st.session_state.get('show_menu', False)):
        st.markdown("### Quick Actions")
        
        action_col1, action_col2 = st.columns(2, gap="small")
        
        with action_col1:
            if st.button("🔄 Refresh", use_container_width=True, key="menu_refresh"):
                st.cache_data.clear()
                st.session_state.last_updated = datetime.now()
                st.success("✅ Data refreshed")
                st.rerun()
            
            if st.button("📥 Export", use_container_width=True, key="menu_export"):
                st.session_state.show_export = True
                st.rerun()
        
        with action_col2:
            if st.button("📧 Share", use_container_width=True, key="menu_share"):
                st.session_state.show_share = True
                st.rerun()
            
            if st.button("❓ Help", use_container_width=True, key="menu_help"):
                st.session_state.show_help = True
                st.rerun()
        
        st.markdown("---")
        
        st.markdown("### Filters")
        if st.button("🔍 Quick Filters", use_container_width=True, key="menu_filters"):
            st.session_state.show_filters = True
            st.rerun()
        
        st.markdown("---")
        
        st.markdown("### Account")
        st.write("👤 Healthcare Manager")
        
        account_col1, account_col2 = st.columns(2, gap="small")
        with account_col1:
            if st.button("⚙️ Preferences", use_container_width=True, key="menu_prefs"):
                st.session_state.current_view = "settings"
                st.rerun()
        
        with account_col2:
            if st.button("🚪 Sign Out", use_container_width=True, key="menu_signout"):
                st.info("Sign out functionality would be implemented here")
        
        st.markdown("---")
        
        st.markdown("### About")
        st.caption("HEDIS Portfolio Optimizer")
        st.caption("Version 4.0 - Mobile Optimized")
        st.caption("Built by Robert Reichert")


# ============================================================================
# STATE MANAGEMENT
# ============================================================================

def save_nav_state(view: str, context: Optional[Dict[str, Any]] = None):
    """
    Save navigation state for back button functionality.
    
    Args:
        view: Current view identifier
        context: Optional context dictionary to save
    """
    if 'nav_history' not in st.session_state:
        st.session_state.nav_history = []
    
    nav_item = {
        'view': view,
        'context': context or {},
        'timestamp': datetime.now()
    }
    
    # Don't add duplicate consecutive entries
    if (not st.session_state.nav_history or 
        st.session_state.nav_history[-1]['view'] != view):
        st.session_state.nav_history.append(nav_item)
    
    # Keep only last 10 items
    if len(st.session_state.nav_history) > 10:
        st.session_state.nav_history = st.session_state.nav_history[-10:]


def get_nav_context() -> Dict[str, Any]:
    """
    Get current navigation context for saving.
    
    Returns:
        Dictionary of current context state
    """
    return {
        'selected_measure': st.session_state.get('selected_measure'),
        'selected_member_id': st.session_state.get('selected_member_id'),
        'member_card_limit': st.session_state.get('member_card_limit', 10),
        'filter_preset': st.session_state.get('filter_preset', 'default')
    }


# ============================================================================
# BACK BUTTON FUNCTIONALITY
# ============================================================================

def mobile_back_button():
    """
    Show back button and handle navigation to previous view.
    """
    if len(st.session_state.get('nav_history', [])) > 1:
        if st.button("⬅️ Back", key="back_btn", use_container_width=True):
            # Remove current state
            nav_history = st.session_state.nav_history.copy()
            nav_history.pop()
            
            if nav_history:
                # Get previous state
                prev_state = nav_history[-1]
                st.session_state.current_view = prev_state['view']
                
                # Restore context if available
                if prev_state.get('context'):
                    for key, value in prev_state['context'].items():
                        st.session_state[key] = value
                
                # Update history
                st.session_state.nav_history = nav_history
                
                st.rerun()


# ============================================================================
# DEEP LINKING / URL PARAMETERS
# ============================================================================

def handle_mobile_url_params():
    """
    Handle URL parameters for deep linking.
    
    Example URLs:
    - ?view=opportunities
    - ?view=measures&measure=HbA1c+Testing
    - ?view=members&member=M12345678
    """
    try:
        # Streamlit 1.28+ uses st.query_params
        if hasattr(st, 'query_params'):
            params = st.query_params
        else:
            # Fallback for older versions
            params = st.experimental_get_query_params()
        
        # Handle view parameter
        if 'view' in params:
            view = params['view']
            if isinstance(view, list):
                view = view[0]
            if view in ['dashboard', 'opportunities', 'measures', 'members', 'roi', 'secure_query', 'settings']:
                st.session_state.current_view = view
        
        # Handle measure parameter
        if 'measure' in params:
            measure = params['measure']
            if isinstance(measure, list):
                measure = measure[0]
            st.session_state.selected_measure = measure
            st.session_state.selected_measure_name = measure
        
        # Handle member parameter
        if 'member' in params:
            member = params['member']
            if isinstance(member, list):
                member = member[0]
            st.session_state.selected_member_id = member
        
        # Handle filter preset
        if 'preset' in params:
            preset = params['preset']
            if isinstance(preset, list):
                preset = preset[0]
            st.session_state.filter_preset = preset
            
    except Exception as e:
        # Silently fail if URL params not available
        pass


def create_shareable_mobile_link(base_url: Optional[str] = None) -> str:
    """
    Generate shareable URL with current state.
    
    Args:
        base_url: Base URL for the app (default: None, uses current)
    
    Returns:
        Shareable URL with query parameters
    """
    if not base_url:
        # Try to get from session state or use placeholder
        base_url = st.session_state.get('app_url', 'https://your-app.streamlit.app')
    
    params = {}
    
    # Add view
    if st.session_state.get('current_view'):
        params['view'] = st.session_state.current_view
    
    # Add measure if selected
    if st.session_state.get('selected_measure'):
        params['measure'] = st.session_state.selected_measure
    
    # Add member if selected
    if st.session_state.get('selected_member_id'):
        params['member'] = st.session_state.selected_member_id
    
    # Add filter preset if not default
    if st.session_state.get('filter_preset') != 'default':
        params['preset'] = st.session_state.filter_preset
    
    # Build query string
    if params:
        query = "&".join([f"{k}={urllib.parse.quote(str(v))}" for k, v in params.items()])
        shareable_url = f"{base_url}?{query}"
    else:
        shareable_url = base_url
    
    return shareable_url


# ============================================================================
# VIEW ROUTER
# ============================================================================

def mobile_router(view_handlers: Dict[str, Callable]):
    """
    Route to appropriate view based on current_view state.
    
    Args:
        view_handlers: Dictionary mapping view IDs to render functions
    
    Example:
        >>> view_handlers = {
        ...     'dashboard': render_dashboard,
        ...     'opportunities': render_opportunities
        ... }
        >>> mobile_router(view_handlers)
    """
    view = st.session_state.get('current_view', 'dashboard')
    
    if view in view_handlers:
        try:
            view_handlers[view]()
        except Exception as e:
            st.error(f"Error rendering view '{view}': {str(e)}")
            st.session_state.current_view = 'dashboard'
            st.rerun()
    else:
        st.error(f"Unknown view: {view}")
        st.session_state.current_view = 'dashboard'
        st.rerun()


# ============================================================================
# MODAL/OVERLAY SYSTEM
# ============================================================================

def show_mobile_modal(
    title: str,
    content_func: Callable,
    key: str = "modal",
    show_close: bool = True
):
    """
    Show full-screen modal on mobile (simulated with Streamlit).
    
    Args:
        title: Modal title
        content_func: Function to render modal content
        key: Unique key for modal state
        show_close: Whether to show close button (default: True)
    """
    modal_css = """
    <style>
    .mobile-modal-overlay {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        margin: 1rem 0;
    }
    
    .modal-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #0066cc;
    }
    
    .modal-title {
        font-size: 1.3rem;
        font-weight: 700;
        color: #0066cc;
    }
    </style>
    """
    
    st.markdown(modal_css, unsafe_allow_html=True)
    
    # Modal container
    with st.container():
        col1, col2 = st.columns([4, 1], gap="small")
        
        with col1:
            st.markdown(f"### {title}")
        
        with col2:
            if show_close:
                if st.button("✖️", key=f"close_{key}", help="Close"):
                    st.session_state[f"show_{key}"] = False
                    st.rerun()
        
        st.markdown("---")
        
        # Render content
        try:
            content_func()
        except Exception as e:
            st.error(f"Error rendering modal content: {str(e)}")
        
        st.markdown("---")
        
        # Close button at bottom
        if show_close:
            if st.button("Close", key=f"close_bottom_{key}", use_container_width=True):
                st.session_state[f"show_{key}"] = False
                st.rerun()


def render_export_options():
    """Render export options in modal"""
    st.markdown("### Export Options")
    
    export_format = st.radio(
        "Format:",
        options=["CSV", "Excel", "PDF Summary"],
        key="export_format"
    )
    
    export_scope = st.radio(
        "Scope:",
        options=["Current View", "All Data", "Selected Items"],
        key="export_scope"
    )
    
    if st.button("📥 Generate Export", use_container_width=True, type="primary"):
        st.success(f"✅ Exporting as {export_format}...")
        st.info("Export functionality would be implemented here")


def render_share_content():
    """Render share options in modal"""
    st.markdown("### Share Dashboard")
    
    url = create_shareable_mobile_link()
    
    st.markdown("**Shareable Link:**")
    st.code(url, language=None)
    
    col1, col2 = st.columns(2, gap="small")
    
    with col1:
        if st.button("📋 Copy Link", use_container_width=True):
            st.success("✅ Link copied to clipboard!")
    
    with col2:
        if st.button("📧 Email Link", use_container_width=True):
            st.info("Email functionality would be implemented here")
    
    st.markdown("---")
    st.caption("Share this link to let others view the same data and filters")


def render_help_content():
    """Render help content in modal"""
    st.markdown("### Help & Support")
    
    st.markdown("""
    **Navigation:**
    - Use the dropdown at the top to switch views
    - Tap ⬅️ Back to return to previous view
    - Use ☰ Menu for additional options
    
    **Views:**
    - **Dashboard**: Overview of key metrics
    - **Top Opportunities**: Best opportunities by impact
    - **My Measures**: Measure-specific analysis
    - **Members**: Member lists and details
    - **Settings**: Preferences and configuration
    
    **Tips:**
    - Tap cards to expand for details
    - Use "Load More" to see additional items
    - Export data for detailed analysis on desktop
    
    **Need More Help?**
    - Email: support@example.com
    - Phone: 1-800-HELP
    """)


# ============================================================================
# BREADCRUMBS
# ============================================================================

def mobile_breadcrumbs():
    """
    Show breadcrumb navigation for deep navigation.
    """
    breadcrumbs = []
    
    # Home/Dashboard
    breadcrumbs.append(("📊", "dashboard"))
    
    # Current view
    current_view = st.session_state.get('current_view', 'dashboard')
    view_names = {
        'dashboard': 'Dashboard',
        'opportunities': 'Opportunities',
        'measures': 'Measures',
        'members': 'Members',
        'settings': 'Settings'
    }
    
    if current_view != 'dashboard':
        breadcrumbs.append((view_names.get(current_view, current_view), current_view))
    
    # Selected measure
    if st.session_state.get('selected_measure_name'):
        measure_name = st.session_state.selected_measure_name
        if len(measure_name) > 20:
            measure_name = measure_name[:17] + '...'
        breadcrumbs.append((measure_name, None))
    
    # Selected member
    if st.session_state.get('selected_member_id'):
        member_id = st.session_state.selected_member_id
        if len(member_id) > 15:
            member_id = member_id[:12] + '...'
        breadcrumbs.append((f"Member {member_id}", None))
    
    # Display breadcrumbs
    if len(breadcrumbs) > 1:
        breadcrumb_html = " > ".join([f"<strong>{name}</strong>" if link else name 
                                      for name, link in breadcrumbs])
        st.caption(f"📍 {breadcrumb_html}")


# ============================================================================
# COMPLETE MOBILE APP STRUCTURE
# ============================================================================

def create_mobile_app_structure(
    view_handlers: Dict[str, Callable],
    show_header: bool = True,
    show_back_button: bool = True,
    show_breadcrumbs: bool = True,
    show_menu: bool = True
):
    """
    Create complete mobile app structure with navigation.
    
    Args:
        view_handlers: Dictionary mapping view IDs to render functions
        show_header: Whether to show navigation header (default: True)
        show_back_button: Whether to show back button (default: True)
        show_breadcrumbs: Whether to show breadcrumbs (default: True)
        show_menu: Whether to show hamburger menu (default: True)
    
    Example:
        >>> view_handlers = {
        ...     'dashboard': lambda: st.write("Dashboard"),
        ...     'opportunities': lambda: st.write("Opportunities")
        ... }
        >>> create_mobile_app_structure(view_handlers)
    """
    # Initialize state
    init_mobile_state()
    
    # Handle URL parameters (deep linking)
    handle_mobile_url_params()
    
    # Navigation header
    if show_header:
        create_mobile_nav_header(show_menu_button=show_menu)
    
    # Back button
    if show_back_button:
        mobile_back_button()
    
    # Breadcrumbs
    if show_breadcrumbs:
        mobile_breadcrumbs()
    
    # Main navigation
    current_view = mobile_view_selector()
    
    # Save navigation state
    context = get_nav_context()
    save_nav_state(current_view, context)
    
    st.markdown("---")
    
    # Route to appropriate view
    mobile_router(view_handlers)
    
    st.markdown("---")
    
    # Hamburger menu
    if show_menu:
        mobile_hamburger_menu()
    
    # Modals (if triggered)
    if st.session_state.get('show_export', False):
        show_mobile_modal("Export Data", render_export_options, "export")
    
    if st.session_state.get('show_share', False):
        show_mobile_modal("Share", render_share_content, "share")
    
    if st.session_state.get('show_help', False):
        show_mobile_modal("Help & Support", render_help_content, "help")


# ============================================================================
# USAGE EXAMPLE
# ============================================================================

def example_mobile_navigation():
    """
    Example usage of mobile navigation system.
    """
    # Define view handlers
    def render_dashboard():
        st.markdown("### Dashboard View")
        st.metric("Total Members", "10,000+")
        st.metric("Star Rating", "4.5 ⭐")
    
    def render_opportunities():
        st.markdown("### Top Opportunities")
        st.write("Opportunities content here")
    
    def render_measures():
        st.markdown("### My Measures")
        st.write("Measures content here")
    
    def render_members():
        st.markdown("### Members")
        st.write("Members content here")
    
    def render_settings():
        st.markdown("### Settings")
        st.write("Settings content here")
    
    # Create app structure
    view_handlers = {
        'dashboard': render_dashboard,
        'opportunities': render_opportunities,
        'measures': render_measures,
        'members': render_members,
        'settings': render_settings
    }
    
    create_mobile_app_structure(view_handlers)


if __name__ == "__main__":
    print("Mobile navigation system ready!")
    print("\nUsage:")
    print("from utils.mobile_navigation import create_mobile_app_structure")
    print("create_mobile_app_structure(view_handlers)")

