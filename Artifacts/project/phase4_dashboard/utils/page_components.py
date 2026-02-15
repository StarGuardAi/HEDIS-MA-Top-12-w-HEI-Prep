"""
Page Components Utility
Reusable UI components for Streamlit pages in the HEDIS Portfolio Optimizer

This module provides standardized components for consistent page design
across desktop and mobile devices.
"""
import streamlit as st
from typing import Optional, List, Dict, Any
from datetime import datetime


# ============================================================================
# CENTERED METRIC FUNCTION (Replaces st.metric() for guaranteed centering)
# ============================================================================

def centered_metric(label, value, delta=None, delta_color="normal", help_text=None):
    """
    Custom metric display with GUARANTEED centered alignment.
    Replaces st.metric() which cannot be reliably centered via CSS.
    
    Args:
        label: The metric label (e.g., "Potential ROI")
        value: The metric value (e.g., "33%")
        delta: Optional delta text (e.g., "+$1,264,020 annually")
        delta_color: "normal" (green for positive), "inverse" (red for positive), or "off" (gray)
        help_text: Optional tooltip text
    """
    # Determine delta color
    if delta_color == "normal":
        d_color = "#10b981" if delta and (str(delta).startswith("+") or str(delta).startswith("↑")) else "#ef4444"
    elif delta_color == "inverse":
        d_color = "#ef4444" if delta and (str(delta).startswith("+") or str(delta).startswith("↑")) else "#10b981"
    else:
        d_color = "#6b7280"  # gray for "off"
    
    # Help icon
    help_icon = ' <span title="' + str(help_text) + '" style="cursor: help; color: #9ca3af; font-size: 0.75rem;">ⓘ</span>' if help_text else ""
    
    # Format delta - handle cases where delta already has arrow
    if delta:
        delta_text = str(delta)
        if not delta_text.startswith("↑") and not delta_text.startswith("+"):
            delta_text = "↑ " + delta_text
        delta_html = f'<p style="color: {d_color}; font-size: 0.85rem; margin: 0.25rem 0 0 0; font-weight: 500; text-align: center; width: 100%; display: block;">{delta_text}</p>'
    else:
        delta_html = ""
    
    st.markdown(f"""
    <div class="centered-metric-container" style="text-align: center; padding: 0.5rem 0; width: 100%; margin: 0 auto; display: flex; flex-direction: column; align-items: center;">
        <p style="color: #6b7280; font-size: 0.875rem; margin: 0 0 0.25rem 0; font-weight: 500; text-align: center; width: 100%; display: block;">{label}{help_icon}</p>
        <p style="color: #1f2937; font-size: 2rem; font-weight: 700; margin: 0; line-height: 1.2; text-align: center; width: 100%; display: block;">{value}</p>
        {delta_html}
    </div>
    """, unsafe_allow_html=True)


# ============================================================================
# ESSENTIAL PAGE COMPONENTS (Add to every page)
# ============================================================================

def apply_header_spacing() -> None:
    """
    Apply consistent header spacing CSS.
    Call this immediately after st.set_page_config() on every page.
    
    This ensures consistent spacing across all pages for desktop and mobile.
    """
    st.markdown("""
    <style>
    /* Consistent header spacing for all pages */
    div.block-container {
        padding-top: 1rem !important;
        padding-bottom: 1rem !important;
    }
    
    /* Mobile spacing optimization */
    @media (max-width: 768px) {
        div.block-container {
            padding-top: 1.5rem !important;
            padding-left: 0.75rem !important;
            padding-right: 0.75rem !important;
            padding-bottom: 1rem !important;
        }
        
        h1 {
            margin-top: 0.5rem !important;
            margin-bottom: 0.75rem !important;
            font-size: 1.5rem !important;
        }
    }
    
    /* Desktop spacing */
    @media (min-width: 769px) {
        div.block-container {
            padding-left: 2rem !important;
            padding-right: 2rem !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)


# def add_mobile_ready_badge() -> None:
#     """
#     Add a mobile-ready badge to the sidebar.
#     Call this inside the sidebar context (with st.sidebar:).
#     
#     This badge indicates the page is optimized for mobile devices.
#     """
#     st.markdown("""
#     <style>
#     /* Mobile badge styling - visible on desktop, hidden on mobile */
#     .mobile-ready-badge {
#         background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
#         color: #2d7d32;
#         padding: 0.5rem 0.75rem;
#         border-radius: 8px;
#         border-left: 3px solid #4caf50;
#         font-size: 0.85rem;
#         font-weight: 600;
#         text-align: center;
#         margin: 0.5rem 0;
#         box-shadow: 0 2px 4px rgba(76, 175, 80, 0.1);
#     }
#     
#     /* Hide badge on mobile devices */
#     @media (max-width: 768px) {
#         .mobile-ready-badge {
#             display: none !important;
#         }
#     }
#     </style>
#     """, unsafe_allow_html=True)
#     
#     st.markdown("""
#     <div class="mobile-ready-badge">
#         📱 Mobile Optimized
#     </div>
#     """, unsafe_allow_html=True)


def render_footer():
    """Render colorful professional footer with inline styles."""
    st.markdown("---")
    
    # Hashtags row - purple gradient pills
    st.markdown("""
    <div style="display: flex; justify-content: center; flex-wrap: wrap; gap: 8px; margin-bottom: 20px;">
        <span style="background: linear-gradient(135deg, #6366f1, #8b5cf6); color: white; padding: 6px 14px; border-radius: 20px; font-size: 12px; font-weight: 500;">#HealthcareAnalytics</span>
        <span style="background: linear-gradient(135deg, #6366f1, #8b5cf6); color: white; padding: 6px 14px; border-radius: 20px; font-size: 12px; font-weight: 500;">#MedicareAdvantage</span>
        <span style="background: linear-gradient(135deg, #6366f1, #8b5cf6); color: white; padding: 6px 14px; border-radius: 20px; font-size: 12px; font-weight: 500;">#HEDIS</span>
        <span style="background: linear-gradient(135deg, #6366f1, #8b5cf6); color: white; padding: 6px 14px; border-radius: 20px; font-size: 12px; font-weight: 500;">#DataScience</span>
        <span style="background: linear-gradient(135deg, #6366f1, #8b5cf6); color: white; padding: 6px 14px; border-radius: 20px; font-size: 12px; font-weight: 500;">#HealthcareAI</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Main card with purple gradient
    st.markdown("""
    <div style="background: linear-gradient(135deg, #4A3D6F 0%, #6F5F96 100%); border-radius: 16px; padding: 24px; margin-bottom: 16px; border-top: 4px solid; border-image: linear-gradient(90deg, #10b981, #6366f1, #f59e0b, #ef4444) 1;">
        <div style="text-align: center; margin-bottom: 16px;">
            <div style="color: white; font-size: 22px; font-weight: 700;">⭐ HEDIS Portfolio Optimizer | StarGuard AI</div>
            <div style="color: rgba(255,255,255,0.8); font-size: 14px; font-style: italic;">Turning Data Into Stars</div>
        </div>
        
        <div style="display: flex; justify-content: center; flex-wrap: wrap; gap: 8px; margin-bottom: 20px;">
            <span style="background: rgba(255,255,255,0.15); color: white; padding: 5px 12px; border-radius: 6px; font-size: 12px; border: 1px solid rgba(255,255,255,0.2);">🐍 Python</span>
            <span style="background: rgba(255,255,255,0.15); color: white; padding: 5px 12px; border-radius: 6px; font-size: 12px; border: 1px solid rgba(255,255,255,0.2);">📊 Streamlit</span>
            <span style="background: rgba(255,255,255,0.15); color: white; padding: 5px 12px; border-radius: 6px; font-size: 12px; border: 1px solid rgba(255,255,255,0.2);">📈 Plotly</span>
            <span style="background: rgba(255,255,255,0.15); color: white; padding: 5px 12px; border-radius: 6px; font-size: 12px; border: 1px solid rgba(255,255,255,0.2);">🐘 PostgreSQL</span>
            <span style="background: rgba(255,255,255,0.15); color: white; padding: 5px 12px; border-radius: 6px; font-size: 12px; border: 1px solid rgba(255,255,255,0.2);">🤖 ML/AI</span>
        </div>
        
        <div style="background: rgba(16, 185, 129, 0.15); border: 2px solid rgba(16, 185, 129, 0.5); border-radius: 12px; padding: 16px; margin: 0 auto; max-width: 600px;">
            <div style="text-align: center; margin-bottom: 8px;">
                <span style="color: #10b981; font-size: 18px; font-weight: 700;">🔒 Secure AI Architecture</span>
            </div>
            <div style="color: rgba(255,255,255,0.9); font-size: 13px; text-align: center; margin-bottom: 12px;">
                Healthcare AI that sees everything, exposes nothing.
            </div>
            
            <div style="display: flex; justify-content: center; gap: 32px; flex-wrap: wrap; margin-bottom: 12px;">
                <div style="text-align: center;">
                    <div style="color: #10b981; font-size: 18px; font-weight: 700;">2.8-4.1x</div>
                    <div style="color: rgba(255,255,255,0.7); font-size: 11px;">ROI Delivered</div>
                </div>
                <div style="text-align: center;">
                    <div style="color: #10b981; font-size: 18px; font-weight: 700;">$148M+</div>
                    <div style="color: rgba(255,255,255,0.7); font-size: 11px;">Proven Savings</div>
                </div>
                <div style="text-align: center;">
                    <div style="color: #10b981; font-size: 18px; font-weight: 700;">Zero</div>
                    <div style="color: rgba(255,255,255,0.7); font-size: 11px;">PHI Exposure</div>
                </div>
            </div>
            
            <div style="display: flex; justify-content: center; flex-wrap: wrap; gap: 8px;">
                <span style="background: rgba(255,255,255,0.1); color: rgba(255,255,255,0.9); padding: 4px 10px; border-radius: 20px; font-size: 11px;">🏢 On-Premises</span>
                <span style="background: rgba(255,255,255,0.1); color: rgba(255,255,255,0.9); padding: 4px 10px; border-radius: 20px; font-size: 11px;">🚫 Zero API Transmission</span>
                <span style="background: rgba(255,255,255,0.1); color: rgba(255,255,255,0.9); padding: 4px 10px; border-radius: 20px; font-size: 11px;">🏥 HIPAA-First Design</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Yellow disclaimer bar
    st.markdown("""
    <div style="background: linear-gradient(135deg, #fef3c7, #fde68a); border-left: 4px solid #f59e0b; border-radius: 0 10px 10px 0; padding: 12px 16px; margin-bottom: 12px; display: flex; align-items: center; gap: 10px;">
        <span style="font-size: 20px;">⚠️</span>
        <span style="color: #92400e; font-size: 13px;"><strong>Portfolio Demonstration:</strong> Using synthetic data to showcase real methodology and production-grade analytics capabilities.</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Copyright
    st.markdown("""
    <div style="text-align: center; padding: 12px 0; color: #6b7280; font-size: 13px;">
        © 2024-2026 <span style="color: #4A3D6F; font-weight: 600;">Robert Reichert</span> | StarGuard AI™ | Healthcare AI Architect
    </div>
    """, unsafe_allow_html=True)


# Backward compatibility alias
def add_page_footer(author: str = "Robert Reichert", version: str = "4.0") -> None:
    """Backward compatibility wrapper - calls render_footer()."""
    render_footer()


# ============================================================================
# METRIC CARDS
# ============================================================================

def render_metric_card(
    label: str,
    value: str,
    delta: Optional[str] = None,
    help_text: Optional[str] = None,
    color: str = "#0066cc"
) -> None:
    """
    Render a styled metric card with consistent formatting.
    
    Args:
        label: Metric label
        value: Metric value (formatted string)
        delta: Optional delta/change indicator
        help_text: Optional help tooltip text
        color: Accent color (default: blue)
    """
    st.metric(
        label=label,
        value=value,
        delta=delta,
        help=help_text
    )


def render_kpi_card(
    title: str,
    value: str,
    subtitle: Optional[str] = None,
    color: str = "#0066cc",
    icon: Optional[str] = None
) -> None:
    """
    Render a custom KPI card with icon and styling.
    
    Args:
        title: KPI title
        value: Main value display
        subtitle: Optional subtitle text
        color: Accent color
        icon: Optional emoji or icon
    """
    icon_html = f"{icon} " if icon else ""
    
    st.markdown(f"""
    <div class="kpi-card" style="
        background: white;
        border-radius: 8px;
        padding: 1rem;
        border-left: 4px solid {color};
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
    ">
        <div class="kpi-title" style="
            font-size: 0.9rem;
            color: #666;
            margin-bottom: 0.5rem;
            font-weight: 600;
        ">{icon_html}{title}</div>
        <div class="kpi-value" style="
            font-size: 2rem;
            font-weight: 700;
            color: {color};
            margin-bottom: 0.25rem;
        ">{value}</div>
        {f'<div class="kpi-subtitle" style="font-size: 0.85rem; color: #999;">{subtitle}</div>' if subtitle else ''}
    </div>
    """, unsafe_allow_html=True)


# ============================================================================
# ALERT BOXES
# ============================================================================

def render_info_box(
    message: str,
    title: Optional[str] = None,
    icon: str = "ℹ️"
) -> None:
    """
    Render a styled info box.
    
    Args:
        message: Info message text
        title: Optional title
        icon: Icon emoji
    """
    title_html = f"<strong>{title}</strong><br>" if title else ""
    st.info(f"{icon} {title_html}{message}")


def render_success_box(
    message: str,
    title: Optional[str] = None,
    icon: str = "✅"
) -> None:
    """
    Render a styled success box.
    
    Args:
        message: Success message text
        title: Optional title
        icon: Icon emoji
    """
    title_html = f"<strong>{title}</strong><br>" if title else ""
    st.success(f"{icon} {title_html}{message}")


def render_warning_box(
    message: str,
    title: Optional[str] = None,
    icon: str = "⚠️"
) -> None:
    """
    Render a styled warning box.
    
    Args:
        message: Warning message text
        title: Optional title
        icon: Icon emoji
    """
    title_html = f"<strong>{title}</strong><br>" if title else ""
    st.warning(f"{icon} {title_html}{message}")


def render_error_box(
    message: str,
    title: Optional[str] = None,
    icon: str = "❌"
) -> None:
    """
    Render a styled error box.
    
    Args:
        message: Error message text
        title: Optional title
        icon: Icon emoji
    """
    title_html = f"<strong>{title}</strong><br>" if title else ""
    st.error(f"{icon} {title_html}{message}")


# ============================================================================
# SECTION HEADERS
# ============================================================================

def render_section_header(
    title: str,
    subtitle: Optional[str] = None,
    icon: Optional[str] = None,
    level: int = 2
) -> None:
    """
    Render a styled section header.
    
    Args:
        title: Section title
        subtitle: Optional subtitle
        icon: Optional emoji icon
        level: Heading level (2-6)
    """
    icon_html = f"{icon} " if icon else ""
    subtitle_html = f"<p style='color: #666; font-size: 0.9rem; margin-top: 0.25rem;'>{subtitle}</p>" if subtitle else ""
    
    heading_tag = f"h{level}"
    st.markdown(f"""
    <{heading_tag} style="
        margin-top: 1rem;
        margin-bottom: 0.5rem;
        text-align: center;
        font-weight: 600;
    ">
        {icon_html}{title}
    </{heading_tag}>
    {subtitle_html}
    """, unsafe_allow_html=True)


def render_page_header(
    title: str,
    subtitle: Optional[str] = None,
    badge: Optional[str] = None
) -> None:
    """
    Render a page-level header with optional badge.
    
    Args:
        title: Page title
        subtitle: Optional subtitle
        badge: Optional badge text (e.g., "Mobile Optimized")
    """
    badge_html = f"<span style='background: #e8f5e9; color: #2d7d32; padding: 0.25rem 0.75rem; border-radius: 12px; font-size: 0.75rem; font-weight: 600; margin-left: 0.5rem;'>{badge}</span>" if badge else ""
    subtitle_html = f"<p style='color: #666; font-size: 1rem; margin-top: 0.5rem; text-align: center;'>{subtitle}</p>" if subtitle else ""
    
    st.markdown(f"""
    <h1 style="
        text-align: center;
        margin-top: 0.5rem;
        margin-bottom: 0.5rem;
        font-weight: 700;
    ">
        {title}{badge_html}
    </h1>
    {subtitle_html}
    """, unsafe_allow_html=True)


# ============================================================================
# STATUS BADGES
# ============================================================================

def render_status_badge(
    status: str,
    variant: str = "info"
) -> str:
    """
    Generate HTML for a status badge.
    
    Args:
        status: Status text
        variant: Badge variant (info, success, warning, error, primary)
    
    Returns:
        HTML string for badge
    """
    colors = {
        "info": {"bg": "#e3f2fd", "text": "#1976d2", "border": "#2196f3"},
        "success": {"bg": "#e8f5e9", "text": "#2d7d32", "border": "#4caf50"},
        "warning": {"bg": "#fff3e0", "text": "#e65100", "border": "#ff9800"},
        "error": {"bg": "#ffebee", "text": "#c62828", "border": "#f44336"},
        "primary": {"bg": "#e8d4ff", "text": "#4A3D6F", "border": "#6F5F96"}
    }
    
    color = colors.get(variant, colors["info"])
    
    return f"""
    <span style="
        background: {color['bg']};
        color: {color['text']};
        padding: 0.25rem 0.75rem;
        border-radius: 12px;
        font-size: 0.85rem;
        font-weight: 600;
        border: 1px solid {color['border']};
        display: inline-block;
    ">{status}</span>
    """


def render_badge_row(badges: List[Dict[str, Any]]) -> None:
    """
    Render a row of status badges.
    
    Args:
        badges: List of badge dicts with 'text' and 'variant' keys
    """
    badge_html = " ".join([
        render_status_badge(badge['text'], badge.get('variant', 'info'))
        for badge in badges
    ])
    
    st.markdown(f"""
    <div style="text-align: center; margin: 1rem 0;">
        {badge_html}
    </div>
    """, unsafe_allow_html=True)


# ============================================================================
# DATA DISPLAY COMPONENTS
# ============================================================================

def render_data_summary(
    total_records: int,
    filtered_records: Optional[int] = None,
    label: str = "Records"
) -> None:
    """
    Render a data summary card showing total and filtered counts.
    
    Args:
        total_records: Total number of records
        filtered_records: Number of filtered records (if None, shows total only)
        label: Label for the records
    """
    if filtered_records is not None and filtered_records != total_records:
        delta = filtered_records - total_records
        delta_text = f"{delta:+,}" if delta != 0 else None
        st.metric(
            label=f"📊 {label} Shown",
            value=f"{filtered_records:,}",
            delta=delta_text
        )
    else:
        st.metric(
            label=f"📊 Total {label}",
            value=f"{total_records:,}"
        )


def render_filter_status(
    active_filters: List[str],
    show_reset: bool = True
) -> None:
    """
    Render active filter status with optional reset button.
    
    Args:
        active_filters: List of active filter descriptions
        show_reset: Whether to show reset button
    """
    if active_filters:
        filter_text = ", ".join(active_filters)
        st.info(f"🔍 **Active Filters:** {filter_text}")
        
        if show_reset:
            if st.button("🔄 Reset All Filters", use_container_width=True):
                # Clear filter session state
                if 'filters' in st.session_state:
                    st.session_state.filters = {}
                st.rerun()
    else:
        st.success("✓ No filters active - showing all data")


# ============================================================================
# LOADING STATES
# ============================================================================

def render_loading_state(message: str = "Loading...") -> None:
    """
    Render a loading state indicator.
    
    Args:
        message: Loading message
    """
    st.markdown(f"""
    <div style="text-align: center; padding: 2rem;">
        <div style="font-size: 2rem; margin-bottom: 1rem;">⏳</div>
        <div style="color: #666;">{message}</div>
    </div>
    """, unsafe_allow_html=True)


def render_empty_state(
    message: str,
    icon: str = "📭",
    action_label: Optional[str] = None,
    action_callback: Optional[callable] = None
) -> None:
    """
    Render an empty state message.
    
    Args:
        message: Empty state message
        icon: Icon emoji
        action_label: Optional action button label
        action_callback: Optional callback function for action button
    """
    st.markdown(f"""
    <div style="text-align: center; padding: 3rem 1rem;">
        <div style="font-size: 3rem; margin-bottom: 1rem;">{icon}</div>
        <div style="color: #666; font-size: 1.1rem; margin-bottom: 1rem;">{message}</div>
    </div>
    """, unsafe_allow_html=True)
    
    if action_label and action_callback:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button(action_label, use_container_width=True):
                action_callback()


# ============================================================================
# FOOTER COMPONENTS
# ============================================================================

def render_page_footer(
    author: str = "Robert Reichert",
    version: str = "4.0",
    last_updated: Optional[datetime] = None
) -> None:
    """
    Render a standardized page footer.
    
    Args:
        author: Author name
        version: Version number
        last_updated: Optional last updated timestamp
    """
    updated_text = ""
    if last_updated:
        updated_text = f" | Last Updated: {last_updated.strftime('%Y-%m-%d')}"
    
    st.markdown("---")
    st.markdown(f"""
    <div style="
        text-align: center;
        color: #999;
        font-size: 0.85rem;
        padding: 1rem 0;
    ">
        <p style="margin: 0;">
            Built by <strong>{author}</strong> | Version {version}{updated_text}
        </p>
        <p style="margin: 0.5rem 0 0 0;">
            🔒 HIPAA-Compliant Architecture | Zero External API Exposure
        </p>
    </div>
    """, unsafe_allow_html=True)


# ============================================================================
# SECURITY BADGES
# ============================================================================

def render_security_badge(
    show_details: bool = True
) -> None:
    """
    Render a security compliance badge.
    
    Args:
        show_details: Whether to show detailed security information
    """
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #2d7d32;
        margin-bottom: 1rem;
        text-align: center;
    ">
        <h3 style="color: #2d7d32; margin: 0 0 0.5rem 0; font-size: 1.1rem;">
            🔒 ZERO PHI TRANSMITTED TO EXTERNAL APIS
        </h3>
        <p style="color: #1b5e20; margin: 0; font-size: 0.9rem;">
            All processing occurs on-premises using local models (Ollama/ChromaDB)
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if show_details:
        with st.expander("🔐 Security Architecture Details", expanded=False):
            st.markdown("""
            **Data Flow:** User → Local Model → Internal DB
            
            **Key Features:**
            - ✅ On-premises LLM deployment (Ollama)
            - ✅ Local vector search (ChromaDB)
            - ✅ Zero external API calls
            - ✅ Full audit trails
            - ✅ HIPAA-compliant architecture
            
            **Compliance:**
            - HIPAA Compliance
            - SOC 2 Type II
            - HITRUST
            - ISO 27001
            """)


# ============================================================================
# METRIC GRID
# ============================================================================

def render_metric_grid(
    metrics: List[Dict[str, Any]],
    columns: int = 4
) -> None:
    """
    Render a grid of metrics.
    
    Args:
        metrics: List of metric dicts with 'label', 'value', 'delta' keys
        columns: Number of columns (default: 4)
    """
    cols = st.columns(columns, gap="small")
    
    for idx, metric in enumerate(metrics):
        col_idx = idx % len(cols)
        with cols[col_idx]:
            render_metric_card(
                label=metric.get('label', 'Metric'),
                value=metric.get('value', 'N/A'),
                delta=metric.get('delta'),
                help_text=metric.get('help')
            )


# ============================================================================
# EXPORT BUTTONS
# ============================================================================

def render_export_buttons(
    export_formats: List[str] = ["CSV", "Excel", "PDF"],
    callback_prefix: str = "export_"
) -> None:
    """
    Render export buttons for different formats.
    
    Args:
        export_formats: List of export formats
        callback_prefix: Prefix for button keys
    """
    cols = st.columns(len(export_formats), gap="small")
    
    for col, format_type in zip(cols, export_formats):
        with col:
            icon = {
                "CSV": "📄",
                "Excel": "📊",
                "PDF": "📑",
                "JSON": "📋"
            }.get(format_type, "📥")
            
            if st.button(
                f"{icon} {format_type}",
                key=f"{callback_prefix}{format_type.lower()}",
                use_container_width=True
            ):
                st.session_state[f"export_{format_type.lower()}"] = True
                st.rerun()


# ============================================================================
# USAGE EXAMPLES
# ============================================================================

def example_usage():
    """Example usage of page components"""
    # Page header
    render_page_header(
        title="Example Page",
        subtitle="Demonstrating page components",
        badge="Mobile Optimized"
    )
    
    # Section header
    render_section_header(
        title="Key Metrics",
        subtitle="Performance indicators",
        icon="📊"
    )
    
    # Metric grid
    metrics = [
        {"label": "ROI", "value": "498%", "delta": "+$935K"},
        {"label": "Star Rating", "value": "4.5 ⭐", "delta": "+0.5"},
        {"label": "Members", "value": "10,000+", "delta": "+1,200"},
        {"label": "Compliance", "value": "93%", "delta": "+8%"}
    ]
    render_metric_grid(metrics)
    
    # Status badges
    badges = [
        {"text": "Active", "variant": "success"},
        {"text": "HIPAA Compliant", "variant": "info"},
        {"text": "On-Premises", "variant": "primary"}
    ]
    render_badge_row(badges)
    
    # Info boxes
    render_info_box("This is an info message", title="Information")
    render_success_box("Operation completed successfully", title="Success")
    
    # Footer
    render_page_footer(
        author="Robert Reichert",
        version="4.0",
        last_updated=datetime.now()
    )


if __name__ == "__main__":
    st.set_page_config(page_title="Page Components Examples", layout="wide")
    example_usage()

