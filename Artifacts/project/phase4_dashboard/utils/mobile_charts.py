"""
Mobile-Optimized Plotly Charts for HEDIS Portfolio Optimizer
Touch-friendly visualizations for smartphones (375-428px width)
"""
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from typing import Optional, Dict, Any
from datetime import datetime, timedelta


# ============================================================================
# MOBILE CONFIGURATION
# ============================================================================

# Mobile-optimized Plotly config
MOBILE_CONFIG = {
    'displayModeBar': False,  # Hide all toolbar buttons
    'staticPlot': False,  # Keep basic interactivity
    'doubleClick': False,  # Prevent accidental zoom
    'showTips': False,  # No hover tips
    'responsive': True,  # Resize with container
    'scrollZoom': False,  # Disable pinch zoom
    'displaylogo': False  # Remove Plotly logo
}

# Mobile color scheme (high contrast)
MOBILE_COLORS = {
    'primary': '#0066cc',      # Strong blue
    'success': '#00cc66',      # Bright green
    'warning': '#ffaa00',      # Orange
    'danger': '#cc0000',       # Red
    'text': '#000000',         # Black
    'background': '#ffffff',   # White
    'light_gray': '#f5f5f5',   # Light background
    'medium_gray': '#999999'   # Medium gray
}

# Mobile layout defaults
MOBILE_LAYOUT = {
    'height': 300,
    'margin': {'l': 20, 'r': 20, 't': 60, 'b': 20},  # Increased top margin for wrapped titles
    'font': {'size': 12, 'family': 'Arial, sans-serif'},
    'showlegend': False,
    'paper_bgcolor': 'white',
    'plot_bgcolor': '#f9f9f9',
    'dragmode': False,  # Prevent pan/zoom gestures
    'hovermode': False,  # Disable hover
    'autosize': True,  # Enable autosizing for proper title wrapping
    'xaxis': {
        'showgrid': True,
        'gridcolor': '#e0e0e0',
        'gridwidth': 1,
        'showline': True,
        'linecolor': '#333333',
        'linewidth': 1
    },
    'yaxis': {
        'showgrid': True,
        'gridcolor': '#e0e0e0',
        'gridwidth': 1,
        'showline': True,
        'linecolor': '#333333',
        'linewidth': 1
    }
}


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def abbreviate_text(text: str, max_length: int = 25) -> str:
    """Abbreviate text for mobile display"""
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + '...'


def get_color_for_value(value: float, threshold: float = 0.5) -> str:
    """Get color based on value (green if above threshold, red if below)"""
    if value >= threshold:
        return MOBILE_COLORS['success']
    else:
        return MOBILE_COLORS['danger']


# ============================================================================
# 1. MOBILE PRIORITY BARS
# ============================================================================

def create_mobile_priority_bars(
    df: pd.DataFrame,
    measure_name_col: str = "measure_name",
    financial_impact_col: str = "financial_impact",
    closure_rate_col: str = "predicted_closure_rate",
    top_n: int = 5,
    height: int = 300
) -> go.Figure:
    """
    Mobile-optimized priority chart - Top N opportunities as horizontal bars.
    
    Shows top opportunities with financial impact and color-coded by closure rate.
    Optimized for touch interaction and readability on small screens.
    
    Args:
        df: DataFrame with measure data, sorted by priority
        measure_name_col: Column name for measure names
        financial_impact_col: Column name for financial impact (dollars)
        closure_rate_col: Column name for predicted closure rate (0-1)
        top_n: Number of top opportunities to show (default: 5)
        height: Chart height in pixels (default: 300)
    
    Returns:
        Plotly figure optimized for mobile
    
    Example:
        >>> df = pd.DataFrame({
        ...     'measure_name': ['HbA1c Testing', 'Blood Pressure Control'],
        ...     'financial_impact': [285000, 320000],
        ...     'predicted_closure_rate': [0.93, 0.88]
        ... })
        >>> fig = create_mobile_priority_bars(df)
        >>> st.plotly_chart(fig, use_container_width=True, config=MOBILE_CONFIG)
    """
    # Validate input
    if df.empty:
        # Return empty chart with message
        fig = go.Figure()
        fig.add_annotation(
            text="No data available",
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            showarrow=False,
            font=dict(size=14, color=MOBILE_COLORS['medium_gray'])
        )
        fig.update_layout(**MOBILE_LAYOUT, height=height)
        return fig
    
    # Check if required columns exist
    if financial_impact_col not in df.columns:
        # Try alternative column names
        if 'financial_value' in df.columns:
            financial_impact_col = 'financial_value'
        else:
            # Return error chart
            fig = go.Figure()
            fig.add_annotation(
                text=f"Missing column: {financial_impact_col}",
                xref="paper", yref="paper",
                x=0.5, y=0.5,
                showarrow=False,
                font=dict(size=14, color=MOBILE_COLORS['danger'])
            )
            fig.update_layout(**MOBILE_LAYOUT, height=height)
            return fig
    
    # Validate top_n
    if top_n <= 0:
        top_n = min(5, len(df))
    
    # Take top N only (handle case where df has fewer rows than top_n)
    try:
        mobile_df = df.nlargest(min(top_n, len(df)), financial_impact_col).copy()
    except Exception as e:
        # Fallback: sort and take top N
        mobile_df = df.sort_values(financial_impact_col, ascending=False).head(min(top_n, len(df))).copy()
    
    # Abbreviate long measure names
    mobile_df['measure_short'] = mobile_df[measure_name_col].apply(
        lambda x: abbreviate_text(str(x), max_length=25)
    )
    
    # Convert financial impact to $K
    mobile_df['financial_impact_k'] = mobile_df[financial_impact_col] / 1000
    
    # Sort by financial impact (descending) for display
    mobile_df = mobile_df.sort_values('financial_impact_k', ascending=True)
    
    # Create horizontal bar chart
    fig = go.Figure()
    
    # Add bars with color based on closure rate
    for idx, row in mobile_df.iterrows():
        closure_rate = row[closure_rate_col]
        color = get_color_for_value(closure_rate, threshold=0.5)
        
        fig.add_trace(go.Bar(
            y=[row['measure_short']],
            x=[row['financial_impact_k']],
            orientation='h',
            marker=dict(
                color=color,
                line=dict(width=1, color='white')
            ),
            text=[f"${row['financial_impact_k']:.0f}K"],
            textposition='outside',
            textfont=dict(size=11, color=MOBILE_COLORS['text']),
            hovertemplate=(
                f"<b>{row[measure_name_col]}</b><br>" +
                f"Financial Impact: ${row['financial_impact_k']:.0f}K<br>" +
                f"Closure Rate: {closure_rate*100:.1f}%<br>" +
                "<extra></extra>"
            ),
            name=row['measure_short']
        ))
    
    # Layout configuration
    layout = MOBILE_LAYOUT.copy()
    layout.update({
        'height': height,
        'title': {
            'text': f'Top {top_n} Opportunities',
            'font': {'size': 14, 'family': 'Arial, sans-serif', 'color': MOBILE_COLORS['text']},
            'x': 0.5,
            'xanchor': 'center',
            'y': 0.98,
            'yanchor': 'top',
            'pad': {'t': 10, 'b': 5},
            'automargin': True
        },
        'xaxis': {
            'title': {
                'text': 'Financial Impact ($K)',
                'font': {'size': 13, 'family': 'Arial, sans-serif'}
            },
            'showgrid': True,
            'gridcolor': '#e0e0e0',
            'gridwidth': 1,
            'showline': True,
            'linecolor': '#333333',
            'linewidth': 1,
            'tickfont': {'size': 11}
        },
        'yaxis': {
            'title': '',
            'showgrid': False,
            'showline': False,
            'tickfont': {'size': 11, 'family': 'Arial, sans-serif'},
            'automargin': True
        },
        'margin': {'l': 120, 'r': 20, 't': 60, 'b': 30},  # Extra top margin for wrapped title
        'autosize': True
    })
    
    fig.update_layout(**layout)
    
    return fig


# ============================================================================
# 2. MOBILE STAR GAUGE
# ============================================================================

def create_mobile_star_gauge(
    current_value: float,
    min_value: float = 1.0,
    max_value: float = 5.0,
    height: int = 250
) -> go.Figure:
    """
    Mobile-optimized star rating gauge - simplified display.
    
    Shows only current value with minimal gauge decoration.
    Large number display for easy reading on mobile.
    
    Args:
        current_value: Current star rating (1.0 to 5.0)
        min_value: Minimum gauge value (default: 1.0)
        max_value: Maximum gauge value (default: 5.0)
        height: Chart height in pixels (default: 250)
    
    Returns:
        Plotly figure optimized for mobile
    
    Example:
        >>> fig = create_mobile_star_gauge(4.5)
        >>> st.plotly_chart(fig, use_container_width=True, config=MOBILE_CONFIG)
    """
    # Clamp value to valid range
    current_value = max(min_value, min(max_value, current_value))
    
    # Create simplified gauge
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=current_value,
        domain={'x': [0, 1], 'y': [0, 1]},
        number={
            'font': {
                'size': 48,  # Large for mobile
                'family': 'Arial, sans-serif',
                'color': MOBILE_COLORS['primary']
            },
            'valueformat': '.1f',
            'suffix': ' ⭐'
        },
        gauge={
            'axis': {
                'range': [min_value, max_value],
                'tickwidth': 1,
                'tickcolor': MOBILE_COLORS['text'],
                'tickfont': {'size': 11}
            },
            'bar': {'color': MOBILE_COLORS['primary']},
            'bgcolor': 'white',
            'borderwidth': 2,
            'bordercolor': MOBILE_COLORS['text'],
            'steps': [
                {'range': [1, 3], 'color': '#ffcccc'},      # Red zone
                {'range': [3, 4], 'color': '#fff4cc'},      # Yellow zone
                {'range': [4, 5], 'color': '#ccffcc'}       # Green zone
            ],
            'threshold': {
                'line': {'color': MOBILE_COLORS['text'], 'width': 2},
                'thickness': 0.75,
                'value': current_value
            }
        }
    ))
    
    # Layout configuration
    layout = {
        'font': {'family': 'Arial, sans-serif', 'size': 12},
        'paper_bgcolor': 'white',
        'plot_bgcolor': 'white',
        'height': height,
        'margin': {'l': 40, 'r': 40, 't': 50, 'b': 20},  # Extra top margin for title
        'autosize': True
    }
    
    fig.update_layout(**layout)
    
    return fig


# ============================================================================
# 3. MOBILE METRIC BAR
# ============================================================================

def create_mobile_metric_bar(
    measure_name: str,
    current_value: float,
    benchmark_value: float,
    value_type: str = "percentage",
    height: int = 150
) -> go.Figure:
    """
    Mobile-optimized single measure comparison bar.
    
    Shows current vs benchmark for a single measure.
    Color-coded: Green if above benchmark, Red if below.
    Large percentage labels on bars.
    
    Args:
        measure_name: Name of the measure (will be abbreviated)
        current_value: Current compliance rate (0-100 for percentage)
        benchmark_value: Benchmark rate (0-100 for percentage)
        value_type: Type of value ("percentage" or "currency")
        height: Chart height in pixels (default: 150)
    
    Returns:
        Plotly figure optimized for mobile
    
    Example:
        >>> fig = create_mobile_metric_bar(
        ...     "HbA1c Testing",
        ...     current_value=45.2,
        ...     benchmark_value=40.0
        ... )
        >>> st.plotly_chart(fig, use_container_width=True, config=MOBILE_CONFIG)
    """
    # Abbreviate measure name
    short_name = abbreviate_text(measure_name, max_length=20)
    
    # Determine colors
    current_color = MOBILE_COLORS['success'] if current_value >= benchmark_value else MOBILE_COLORS['danger']
    benchmark_color = MOBILE_COLORS['medium_gray']
    
    # Format values
    if value_type == "percentage":
        current_text = f"{current_value:.1f}%"
        benchmark_text = f"{benchmark_value:.1f}%"
        xaxis_title = "Compliance Rate (%)"
    else:
        current_text = f"${current_value:,.0f}"
        benchmark_text = f"${benchmark_value:,.0f}"
        xaxis_title = "Value ($)"
    
    # Create bar chart
    fig = go.Figure()
    
    # Add benchmark bar
    fig.add_trace(go.Bar(
        name='Benchmark',
        x=[benchmark_value],
        y=[short_name],
        orientation='h',
        marker=dict(
            color=benchmark_color,
            line=dict(width=1, color='white')
        ),
        text=[benchmark_text],
        textposition='inside',
        textfont=dict(size=12, color='white', family='Arial, sans-serif'),
        hovertemplate=f"<b>Benchmark</b><br>{xaxis_title}: {benchmark_text}<extra></extra>",
        showlegend=False
    ))
    
    # Add current bar
    fig.add_trace(go.Bar(
        name='Current',
        x=[current_value],
        y=[short_name],
        orientation='h',
        marker=dict(
            color=current_color,
            line=dict(width=1, color='white')
        ),
        text=[current_text],
        textposition='outside',
        textfont=dict(size=12, color=MOBILE_COLORS['text'], family='Arial, sans-serif'),
        hovertemplate=f"<b>Current</b><br>{xaxis_title}: {current_text}<extra></extra>",
        showlegend=False
    ))
    
    # Layout configuration
    layout = MOBILE_LAYOUT.copy()
    layout.update({
        'height': height,
        'barmode': 'overlay',
        'xaxis': {
            'title': {
                'text': xaxis_title,
                'font': {'size': 12, 'family': 'Arial, sans-serif'}
            },
            'range': [0, max(current_value, benchmark_value) * 1.2],
            'showgrid': True,
            'gridcolor': '#e0e0e0',
            'gridwidth': 1,
            'showline': True,
            'linecolor': '#333333',
            'linewidth': 1,
            'tickfont': {'size': 11}
        },
        'yaxis': {
            'title': '',
            'showgrid': False,
            'showline': False,
            'tickfont': {'size': 12, 'family': 'Arial, sans-serif'},
            'automargin': True
        },
        'margin': {'l': 100, 'r': 20, 't': 40, 'b': 30},  # Extra top margin for potential title
        'autosize': True
    })
    
    fig.update_layout(**layout)
    
    return fig


# ============================================================================
# 4. MOBILE SPARKLINE
# ============================================================================

def create_mobile_sparkline(
    df: pd.DataFrame,
    date_col: str = "date",
    value_col: str = "compliance_rate",
    measure_name: str = "",
    days: int = 90,
    height: int = 100
) -> go.Figure:
    """
    Mobile-optimized trend sparkline - minimal styling, last N days only.
    
    Shows trend direction without detailed axes or labels.
    Pure sparkline style for quick visual reference.
    
    Args:
        df: DataFrame with time series data
        date_col: Column name for dates
        value_col: Column name for values to plot
        measure_name: Name of measure (for title)
        days: Number of days to show (default: 90)
        height: Chart height in pixels (default: 100)
    
    Returns:
        Plotly figure optimized for mobile
    
    Example:
        >>> df = pd.DataFrame({
        ...     'date': pd.date_range('2024-01-01', periods=90, freq='D'),
        ...     'compliance_rate': [35 + i*0.1 for i in range(90)]
        ... })
        >>> fig = create_mobile_sparkline(df, measure_name="HbA1c Testing")
        >>> st.plotly_chart(fig, use_container_width=True, config=MOBILE_CONFIG)
    """
    # Validate input
    if df.empty or date_col not in df.columns or value_col not in df.columns:
        # Return empty sparkline
        fig = go.Figure()
        fig.add_annotation(
            text="No data",
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            showarrow=False,
            font=dict(size=11, color=MOBILE_COLORS['medium_gray'])
        )
        fig.update_layout(**MOBILE_LAYOUT, height=height)
        return fig
    
    # Prepare data
    mobile_df = df.copy()
    
    # Ensure date column is datetime
    if not pd.api.types.is_datetime64_any_dtype(mobile_df[date_col]):
        mobile_df[date_col] = pd.to_datetime(mobile_df[date_col], errors='coerce')
    
    # Filter to last N days
    cutoff_date = datetime.now() - timedelta(days=days)
    mobile_df = mobile_df[mobile_df[date_col] >= cutoff_date].copy()
    
    # Sort by date
    mobile_df = mobile_df.sort_values(date_col)
    
    # Calculate trend direction
    if len(mobile_df) > 1:
        first_value = mobile_df[value_col].iloc[0]
        last_value = mobile_df[value_col].iloc[-1]
        trend = "up" if last_value > first_value else "down" if last_value < first_value else "flat"
        trend_symbol = "📈" if trend == "up" else "📉" if trend == "down" else "➡️"
    else:
        trend = "flat"
        trend_symbol = "➡️"
    
    # Create sparkline
    fig = go.Figure()
    
    # Add trend line
    fig.add_trace(go.Scatter(
        x=mobile_df[date_col],
        y=mobile_df[value_col],
        mode='lines',
        line=dict(
            color=MOBILE_COLORS['primary'],
            width=2
        ),
        fill='tozeroy',
        fillcolor=f"rgba(0, 102, 204, 0.1)",
        hovertemplate=f"<b>{date_col}</b><br>{value_col}: %{{y:.1f}}<extra></extra>",
        showlegend=False
    ))
    
    # Add trend indicator
    if len(mobile_df) > 0:
        last_date = mobile_df[date_col].iloc[-1]
        last_value = mobile_df[value_col].iloc[-1]
        
        fig.add_annotation(
            text=trend_symbol,
            x=last_date,
            y=last_value,
            showarrow=False,
            font=dict(size=16),
            bgcolor='white',
            bordercolor=MOBILE_COLORS['text'],
            borderwidth=1
        )
    
    # Layout configuration (minimal - sparkline style)
    layout = {
        'height': height,
        'margin': {'l': 5, 'r': 5, 't': 5, 'b': 5},
        'font': {'size': 10, 'family': 'Arial, sans-serif'},
        'showlegend': False,
        'paper_bgcolor': 'white',
        'plot_bgcolor': '#f9f9f9',
        'xaxis': {
            'showgrid': False,
            'showline': False,
            'showticklabels': False,
            'zeroline': False
        },
        'yaxis': {
            'showgrid': False,
            'showline': False,
            'showticklabels': False,
            'zeroline': False
        },
        'hovermode': False
    }
    
    # Add title if measure name provided
    if measure_name:
        short_name = abbreviate_text(measure_name, max_length=15)
        layout['title'] = {
            'text': f"{short_name} {trend_symbol}",
            'font': {'size': 11, 'family': 'Arial, sans-serif', 'color': MOBILE_COLORS['text']},
            'x': 0.5,
            'xanchor': 'center',
            'y': 0.95,
            'yanchor': 'top',
            'pad': {'t': 5, 'b': 2},
            'automargin': True
        }
        layout['margin']['t'] = 35  # Increased for wrapped title
        layout['autosize'] = True
    else:
        layout['autosize'] = True
    
    fig.update_layout(**layout)
    
    return fig


# ============================================================================
# USAGE EXAMPLES
# ============================================================================

def example_mobile_charts():
    """
    Example usage of all mobile chart functions.
    
    This demonstrates how to use the mobile charts in a Streamlit app.
    """
    import streamlit as st
    
    # Sample data
    measures_df = pd.DataFrame({
        'measure_name': [
            'HbA1c Testing',
            'Blood Pressure Control',
            'Breast Cancer Screening',
            'Colorectal Cancer Screening',
            'Diabetes Care - Eye Exam'
        ],
        'financial_impact': [285000, 320000, 275000, 290000, 265000],
        'predicted_closure_rate': [0.93, 0.88, 0.85, 0.82, 0.79]
    })
    
    # 1. Priority bars
    st.markdown("### Top 5 Opportunities")
    fig1 = create_mobile_priority_bars(measures_df, top_n=5)
    st.plotly_chart(fig1, use_container_width=True, config=MOBILE_CONFIG)
    
    # 2. Star gauge
    st.markdown("### Current Star Rating")
    fig2 = create_mobile_star_gauge(4.5)
    st.plotly_chart(fig2, use_container_width=True, config=MOBILE_CONFIG)
    
    # 3. Metric bars (stacked vertically)
    st.markdown("### Key Measures")
    top_3_measures = [
        {'name': 'HbA1c Testing', 'current': 45.2, 'benchmark': 40.0},
        {'name': 'Blood Pressure Control', 'current': 52.8, 'benchmark': 45.0},
        {'name': 'Breast Cancer Screening', 'current': 48.5, 'benchmark': 42.0}
    ]
    
    for measure in top_3_measures:
        fig3 = create_mobile_metric_bar(
            measure['name'],
            measure['current'],
            measure['benchmark']
        )
        st.plotly_chart(fig3, use_container_width=True, config=MOBILE_CONFIG)
    
    # 4. Sparkline
    st.markdown("### Trend (Last 90 Days)")
    trend_df = pd.DataFrame({
        'date': pd.date_range('2024-01-01', periods=90, freq='D'),
        'compliance_rate': [35 + i*0.15 for i in range(90)]
    })
    fig4 = create_mobile_sparkline(trend_df, measure_name="HbA1c Testing")
    st.plotly_chart(fig4, use_container_width=True, config=MOBILE_CONFIG)


if __name__ == "__main__":
    print("Mobile chart functions ready!")
    print("\nUsage:")
    print("from utils.mobile_charts import create_mobile_priority_bars, MOBILE_CONFIG")
    print("fig = create_mobile_priority_bars(df)")
    print("st.plotly_chart(fig, use_container_width=True, config=MOBILE_CONFIG)")

