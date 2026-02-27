"""
Desktop-Optimized Healthcare Analytics Visualizations
Production-ready Plotly visualizations for HEDIS Portfolio Optimizer dashboard
"""
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from typing import Optional


def create_priority_matrix(
    df: pd.DataFrame,
    measure_name_col: str = "measure_name",
    closure_rate_col: str = "predicted_closure_rate",
    financial_impact_col: str = "financial_impact",
    member_count_col: str = "member_count",
    star_rating_col: str = "star_rating_impact"
) -> go.Figure:
    """
    Create a Priority Matrix Bubble Chart for HEDIS measure prioritization.
    
    This chart helps executives identify high-impact measures by plotting:
    - X-axis: Predicted closure rate (0-100%)
    - Y-axis: Financial impact (in $K)
    - Bubble size: Member count
    - Bubble color: Star rating impact (red→yellow→green)
    
    Args:
        df: DataFrame with measure data
        measure_name_col: Column name for measure names
        closure_rate_col: Column name for predicted closure rate (0-100)
        financial_impact_col: Column name for financial impact in dollars
        member_count_col: Column name for member count
        star_rating_col: Column name for star rating impact (0-1)
    
    Returns:
        Plotly figure object ready for display
    
    Example:
        >>> df = pd.DataFrame({
        ...     'measure_name': ['HbA1c Testing', 'Blood Pressure Control'],
        ...     'predicted_closure_rate': [45.2, 52.8],
        ...     'financial_impact': [285000, 320000],
        ...     'member_count': [1200, 1500],
        ...     'star_rating_impact': [0.15, 0.22]
        ... })
        >>> fig = create_priority_matrix(df)
        >>> fig.show()
    """
    # Prepare data
    df_plot = df.copy()
    
    # Convert financial impact to $K for Y-axis
    df_plot['financial_impact_k'] = df_plot[financial_impact_col] / 1000
    
    # Normalize member count for bubble sizing (min 10, max 50)
    min_members = df_plot[member_count_col].min()
    max_members = df_plot[member_count_col].max()
    if max_members > min_members:
        df_plot['bubble_size'] = 10 + (df_plot[member_count_col] - min_members) / (max_members - min_members) * 40
    else:
        df_plot['bubble_size'] = 30
    
    # Calculate mean values for quadrant lines
    mean_closure_rate = df_plot[closure_rate_col].mean()
    mean_financial_impact = df_plot['financial_impact_k'].mean()
    
    # Create figure
    fig = go.Figure()
    
    # Add quadrant reference lines
    fig.add_hline(
        y=mean_financial_impact,
        line_dash="dash",
        line_color="#cccccc",
        line_width=1,
        annotation_text=f"Mean: ${mean_financial_impact:.0f}K",
        annotation_position="right",
        annotation_font_size=11,
        annotation_font_color="#666666"
    )
    
    fig.add_vline(
        x=mean_closure_rate,
        line_dash="dash",
        line_color="#cccccc",
        line_width=1,
        annotation_text=f"Mean: {mean_closure_rate:.1f}%",
        annotation_position="top",
        annotation_font_size=11,
        annotation_font_color="#666666"
    )
    
    # Add bubbles with color scale (red→yellow→green)
    fig.add_trace(
        go.Scatter(
            x=df_plot[closure_rate_col],
            y=df_plot['financial_impact_k'],
            mode='markers',
            marker=dict(
                size=df_plot['bubble_size'],
                color=df_plot[star_rating_col],
                colorscale=[[0, '#cc0000'], [0.5, '#ffcc00'], [1, '#00cc66']],  # Red→Yellow→Green
                showscale=True,
                colorbar=dict(
                    title=dict(text="Star Rating<br>Impact", font=dict(size=12)),
                    titleside="right",
                    thickness=15,
                    len=0.5,
                    y=0.75,
                    yanchor="middle"
                ),
                line=dict(width=2, color='white'),
                sizemode='diameter',
                sizeref=1,
                opacity=0.8
            ),
            text=df_plot[measure_name_col],
            customdata=df_plot[[member_count_col, financial_impact_col, star_rating_col]].values,
            name="Measures"
        )
    )
    
    # Update hover template to use customdata for dynamic values
    fig.update_traces(
        hovertemplate=(
            '<b>%{text}</b><br>' +
            'Predicted Closure Rate: %{x:.1f}%<br>' +
            'Financial Impact: $%{y:,.0f}K<br>' +
            'Members: %{customdata[0]:,}<br>' +
            'Star Rating Impact: %{customdata[2]:.3f}<br>' +
            '<extra></extra>'
        )
    )
    
    # Layout configuration
    fig.update_layout(
        title=dict(
            text="Priority Matrix: Measure Impact Analysis",
            font=dict(size=20, family='Arial, sans-serif', color='#0066cc'),
            x=0.5,
            xanchor='center',
            y=0.98,
            yanchor='top'
        ),
        xaxis=dict(
            title=None,  # Remove axis title text completely
            showticklabels=False,  # Hide tick labels (prevents overlap on mobile)
            range=[0, 100],
            gridcolor='#e0e0e0',
            gridwidth=1,
            showline=True,
            linecolor='#333333',
            linewidth=1,
            zeroline=False,
            automargin=True
        ),
        yaxis=dict(
            title=None,  # Remove y-axis title text
            showticklabels=True,  # Keep y-axis numbers visible
            gridcolor='#e0e0e0',
            gridwidth=1,
            showline=True,
            linecolor='#333333',
            linewidth=1,
            zeroline=False,
            automargin=True
        ),
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family='Arial, sans-serif', size=12),
        height=450,
        margin=dict(l=50, r=30, t=60, b=50),
        hovermode='closest',
        showlegend=False
    )
    
    # Configure mode bar - remove logo, minimize mode bar
    fig.update_layout(
        modebar=dict(
            remove=['lasso2d', 'select2d'],
            add=['zoom', 'pan', 'reset', 'toImage']
        )
    )
    
    # Remove Plotly logo
    fig.update_layout(showlegend=False)
    fig.update_layout(plot_bgcolor='white', paper_bgcolor='white')
    
    return fig


def create_star_gauge(
    current_rating: float,
    target_rating: float = 4.5,
    title: str = "Medicare Advantage Star Rating"
) -> go.Figure:
    """
    Create a Star Rating Gauge Chart showing current vs target rating.
    
    Displays a gauge with color zones (Red 1-3, Yellow 3-4, Green 4-5)
    and shows delta improvement.
    
    Args:
        current_rating: Current star rating (1.0 to 5.0)
        target_rating: Target star rating (default: 4.5)
        title: Chart title (default: "Medicare Advantage Star Rating")
    
    Returns:
        Plotly figure object ready for display
    
    Example:
        >>> fig = create_star_gauge(current_rating=4.0, target_rating=4.5)
        >>> fig.show()
    """
    # Calculate delta
    delta = target_rating - current_rating
    
    # Create gauge indicator
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=current_rating,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': title, 'font': {'size': 20, 'family': 'Arial, sans-serif', 'color': '#0066cc'}},
        delta={
            'reference': target_rating,
            'position': "top",
            'valueformat': ".1f",
            'increasing': {'color': "#00cc66"},
            'decreasing': {'color': "#cc0000"},
            'font': {'size': 16, 'family': 'Arial, sans-serif'}
        },
        number={
            'font': {'size': 48, 'family': 'Arial, sans-serif', 'color': '#0066cc'},
            'valueformat': '.1f',
            'suffix': ' ⭐'
        },
        gauge={
            'axis': {'range': [None, 5.0], 'tickwidth': 1, 'tickcolor': "#333333"},
            'bar': {'color': "#0066cc"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "#333333",
            'steps': [
                {'range': [1, 3], 'color': '#ffcccc'},      # Red zone
                {'range': [3, 4], 'color': '#fff4cc'},      # Yellow zone
                {'range': [4, 5], 'color': '#ccffcc'}       # Green zone
            ],
            'threshold': {
                'line': {'color': "#003d7a", 'width': 4},
                'thickness': 0.75,
                'value': target_rating
            }
        }
    ))
    
    # Layout configuration
    fig.update_layout(
        font=dict(family='Arial, sans-serif', size=12),
        paper_bgcolor='white',
        plot_bgcolor='white',
        height=400,
        margin=dict(l=50, r=30, t=60, b=50)
    )
    
    # Configure mode bar
    fig.update_layout(
        modebar=dict(
            remove=['lasso2d', 'select2d'],
            add=['zoom', 'pan', 'reset', 'toImage']
        )
    )
    
    return fig


def create_measure_comparison(
    df: pd.DataFrame,
    measure_name_col: str = "measure_name",
    current_rate_col: str = "current_compliance_rate",
    benchmark_rate_col: str = "benchmark_rate",
    predicted_rate_col: str = "predicted_closure_rate",
    financial_impact_col: str = "financial_impact",
    max_measures: int = 8
) -> go.Figure:
    """
    Create a horizontal grouped bar chart comparing current, benchmark, and predicted rates.
    
    Measures are sorted by financial impact (descending) and displayed horizontally
    for better readability of measure names.
    
    Args:
        df: DataFrame with measure data
        measure_name_col: Column name for measure names
        current_rate_col: Column name for current compliance rate (0-100)
        benchmark_rate_col: Column name for benchmark rate (0-100)
        predicted_rate_col: Column name for predicted closure rate (0-100)
        financial_impact_col: Column name for financial impact (used for sorting)
        max_measures: Maximum number of measures to display (default: 8)
    
    Returns:
        Plotly figure object ready for display
    
    Example:
        >>> df = pd.DataFrame({
        ...     'measure_name': ['HbA1c Testing', 'Blood Pressure Control'],
        ...     'current_compliance_rate': [35.2, 42.8],
        ...     'benchmark_rate': [40.0, 45.0],
        ...     'predicted_closure_rate': [45.2, 52.8],
        ...     'financial_impact': [285000, 320000]
        ... })
        >>> fig = create_measure_comparison(df)
        >>> fig.show()
    """
    # Prepare data
    df_plot = df.copy()
    
    # Sort by financial impact descending and limit to max_measures
    df_plot = df_plot.sort_values(by=financial_impact_col, ascending=False).head(max_measures)
    
    # Reverse order for horizontal bar chart (top to bottom)
    df_plot = df_plot.iloc[::-1]
    
    # Create figure
    fig = go.Figure()
    
    # Add bars: Current (Red), Benchmark (Gray), Predicted (Green)
    fig.add_trace(go.Bar(
        name='Current Rate',
        y=df_plot[measure_name_col],
        x=df_plot[current_rate_col],
        orientation='h',
        marker=dict(color='#cc0000', line=dict(width=1, color='white')),
        text=[f"{val:.1f}%" for val in df_plot[current_rate_col]],
        textposition='outside',
        hovertemplate='<b>%{y}</b><br>Current Rate: %{x:.1f}%<extra></extra>'
    ))
    
    fig.add_trace(go.Bar(
        name='Benchmark Rate',
        y=df_plot[measure_name_col],
        x=df_plot[benchmark_rate_col],
        orientation='h',
        marker=dict(color='#999999', line=dict(width=1, color='white')),
        text=[f"{val:.1f}%" for val in df_plot[benchmark_rate_col]],
        textposition='outside',
        hovertemplate='<b>%{y}</b><br>Benchmark Rate: %{x:.1f}%<extra></extra>'
    ))
    
    fig.add_trace(go.Bar(
        name='Predicted Rate',
        y=df_plot[measure_name_col],
        x=df_plot[predicted_rate_col],
        orientation='h',
        marker=dict(color='#00cc66', line=dict(width=1, color='white')),
        text=[f"{val:.1f}%" for val in df_plot[predicted_rate_col]],
        textposition='outside',
        hovertemplate='<b>%{y}</b><br>Predicted Rate: %{x:.1f}%<extra></extra>'
    ))
    
    # Layout configuration
    fig.update_layout(
        title=dict(
            text="Measure Comparison: Current vs Benchmark vs Predicted",
            font=dict(size=20, family='Arial, sans-serif', color='#0066cc'),
            x=0.5,
            xanchor='center',
            y=0.98,
            yanchor='top'
        ),
        xaxis=dict(
            title=None,  # Remove axis title text completely
            showticklabels=False,  # Hide tick labels (prevents overlap on mobile)
            range=[0, 100],
            gridcolor='#e0e0e0',
            gridwidth=1,
            showline=True,
            linecolor='#333333',
            linewidth=1,
            automargin=True
        ),
        yaxis=dict(
            title=None,  # Remove y-axis title text
            showticklabels=True,  # Keep y-axis numbers visible
            gridcolor='#e0e0e0',
            gridwidth=1,
            showline=True,
            linecolor='#333333',
            linewidth=1,
            automargin=True
        ),
        barmode='group',
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family='Arial, sans-serif', size=12),
        height=450,
        margin=dict(l=150, r=30, t=60, b=50),  # Optimized margins for measure names
        hovermode='closest',
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=-0.15,
            xanchor='center',
            x=0.5,
            font=dict(size=12, family='Arial, sans-serif'),
            bgcolor='rgba(255,255,255,0.9)',
            bordercolor='rgba(0,0,0,0.1)',
            borderwidth=1
        )
    )
    
    # Configure mode bar
    fig.update_layout(
        modebar=dict(
            remove=['lasso2d', 'select2d'],
            add=['zoom', 'pan', 'reset', 'toImage']
        )
    )
    
    return fig


def create_trend_chart(
    df: pd.DataFrame,
    date_col: str = "date",
    measure_name_col: str = "measure_name",
    compliance_rate_col: str = "compliance_rate",
    confidence_lower_col: str = "confidence_lower",
    confidence_upper_col: str = "confidence_upper",
    max_measures: int = 5,
    title: str = "Compliance Rate Trend with Confidence Intervals"
) -> go.Figure:
    """
    Create a multi-line trend chart with confidence intervals.
    
    Shows monthly compliance rates for multiple measures with shaded
    confidence intervals. Includes legend with toggle functionality.
    
    Args:
        df: DataFrame with time series data
        date_col: Column name for date values
        measure_name_col: Column name for measure names
        compliance_rate_col: Column name for compliance rate (0-100)
        confidence_lower_col: Column name for lower confidence bound
        confidence_upper_col: Column name for upper confidence bound
        max_measures: Maximum number of measures to display (default: 5)
        title: Chart title
    
    Returns:
        Plotly figure object ready for display
    
    Example:
        >>> import pandas as pd
        >>> df = pd.DataFrame({
        ...     'date': pd.date_range('2024-01-01', periods=12, freq='ME'),
        ...     'measure_name': ['HbA1c Testing'] * 12,
        ...     'compliance_rate': [35 + i*1.5 for i in range(12)],
        ...     'confidence_lower': [33 + i*1.5 for i in range(12)],
        ...     'confidence_upper': [37 + i*1.5 for i in range(12)]
        ... })
        >>> fig = create_trend_chart(df)
        >>> fig.show()
    """
    # Prepare data
    df_plot = df.copy()
    
    # Ensure date column is datetime
    if not pd.api.types.is_datetime64_any_dtype(df_plot[date_col]):
        df_plot[date_col] = pd.to_datetime(df_plot[date_col])
    
    # Get unique measures and limit to max_measures
    unique_measures = df_plot[measure_name_col].unique()[:max_measures]
    df_plot = df_plot[df_plot[measure_name_col].isin(unique_measures)]
    
    # Color palette for measures
    colors = ['#0066cc', '#00cc66', '#ffcc00', '#cc0000', '#9933cc']
    
    # Create figure
    fig = go.Figure()
    
    # Add traces for each measure
    for idx, measure in enumerate(unique_measures):
        measure_data = df_plot[df_plot[measure_name_col] == measure].sort_values(date_col)
        color = colors[idx % len(colors)]
        
        # Add confidence interval (shaded area)
        if confidence_lower_col in df_plot.columns and confidence_upper_col in df_plot.columns:
            # Convert hex color to RGB for rgba
            rgb = tuple(int(color[i:i+2], 16) for i in (1, 3, 5))
            rgba = f'rgba({rgb[0]}, {rgb[1]}, {rgb[2]}, 0.2)'
            
            fig.add_trace(go.Scatter(
                x=pd.concat([measure_data[date_col], measure_data[date_col][::-1]]),
                y=pd.concat([measure_data[confidence_upper_col], measure_data[confidence_lower_col][::-1]]),
                fill='toself',
                fillcolor=rgba,
                line=dict(color='rgba(255,255,255,0)'),
                hoverinfo="skip",
                showlegend=False,
                name=f'{measure} (CI)'
            ))
        
        # Add main trend line
        fig.add_trace(go.Scatter(
            x=measure_data[date_col],
            y=measure_data[compliance_rate_col],
            mode='lines+markers',
            name=measure,
            line=dict(color=color, width=3),
            marker=dict(size=8, color=color),
            hovertemplate=(
                f'<b>{measure}</b><br>' +
                'Date: %{x|%Y-%m-%d}<br>' +
                'Compliance Rate: %{y:.1f}%<br>' +
                '<extra></extra>'
            )
        ))
    
    # Layout configuration
    fig.update_layout(
        title=dict(
            text=title,
            font=dict(size=20, family='Arial, sans-serif', color='#0066cc'),
            x=0.5,
            xanchor='center',
            y=0.98,
            yanchor='top'
        ),
        xaxis=dict(
            title=None,  # Remove axis title text completely
            showticklabels=False,  # Hide tick labels (prevents overlap on mobile)
            gridcolor='#e0e0e0',
            gridwidth=1,
            showline=True,
            linecolor='#333333',
            linewidth=1,
            type='date',
            rangeslider=dict(visible=True, thickness=0.1),  # Date range selector at bottom
            automargin=True
        ),
        yaxis=dict(
            title=None,  # Remove y-axis title text
            showticklabels=True,  # Keep y-axis numbers visible
            range=[0, 100],
            gridcolor='#e0e0e0',
            gridwidth=1,
            showline=True,
            linecolor='#333333',
            linewidth=1,
            automargin=True
        ),
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family='Arial, sans-serif', size=12),
        height=500,
        margin=dict(l=50, r=30, t=60, b=50),  # Optimized margins (range slider still visible)
        hovermode='x unified',
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=-0.15,  # Closer to chart now that x-axis labels are gone
            xanchor='center',
            x=0.5,
            font=dict(size=12, family='Arial, sans-serif'),
            bgcolor='rgba(255,255,255,0.9)',
            bordercolor='rgba(0,0,0,0.1)',
            borderwidth=1
        )
    )
    
    # Configure mode bar
    fig.update_layout(
        modebar=dict(
            remove=['lasso2d', 'select2d'],
            add=['zoom', 'pan', 'reset', 'toImage']
        )
    )
    
    return fig

