"""
Enhanced Chart Utilities
WOW-factor visualizations with varied chart types, colors, and shapes
"""
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from typing import Optional, List, Dict
from utils.charts import MEDICAL_THEME, format_column_label

# Enhanced color palettes for WOW factor
COLOR_PALETTES = {
    "vibrant": ["#FF6B6B", "#4ECDC4", "#45B7D1", "#FFA07A", "#98D8C8", "#F7DC6F", "#BB8FCE", "#85C1E2"],
    "medical": ["#4A3D6F", "#6F5F96", "#8F67D1", "#2D7D32", "#4CAF50", "#81C784", "#FF9800", "#FF5722"],
    "gradient_purple": ["#667eea", "#764ba2", "#f093fb", "#4facfe", "#00f2fe"],
    "gradient_green": ["#11998e", "#38ef7d", "#06beb6", "#48b1bf"],
    "sunset": ["#FF6B6B", "#FF8E53", "#FFA07A", "#FFB347", "#FFD700"],
    "ocean": ["#0077BE", "#00A8E8", "#00C9FF", "#00E5FF", "#87CEEB"],
}

# Marker shapes for variety
MARKER_SHAPES = ["circle", "square", "diamond", "star", "triangle-up", "triangle-down", "pentagon", "hexagon"]

# Radar chart color palettes (bright, vibrant colors for WOW factor)
RADAR_COLORS = {
    "rainbow": ["#FF0000", "#FF7F00", "#FFFF00", "#00FF00", "#0000FF", "#4B0082", "#9400D3"],
    "vibrant": ["#FF6B6B", "#4ECDC4", "#45B7D1", "#FFA07A", "#98D8C8", "#F7DC6F", "#BB8FCE", "#85C1E2"],
    "medical": ["#4A3D6F", "#6F5F96", "#8F67D1", "#2D7D32", "#4CAF50", "#81C784", "#FF9800", "#FF5722"],
    "gradient_purple": ["#667eea", "#764ba2", "#f093fb", "#4facfe", "#00f2fe"],
    "sunset": ["#FF6B6B", "#FF8E53", "#FFA07A", "#FFB347", "#FFD700"],
    "ocean": ["#0077BE", "#00A8E8", "#00C9FF", "#00E5FF", "#87CEEB"],
}


def create_wow_scatter(
    df: pd.DataFrame,
    x_col: str,
    y_col: str,
    size_col: Optional[str] = None,
    color_col: Optional[str] = None,
    title: str = "",
    x_label: Optional[str] = None,
    y_label: Optional[str] = None,
    color_palette: str = "vibrant",
    marker_shape: str = "circle",
    show_trendline: bool = True,
) -> go.Figure:
    """Create a WOW scatter plot with enhanced styling and optional trendline."""
    fig = go.Figure()
    
    # Get color scale
    colors = COLOR_PALETTES.get(color_palette, COLOR_PALETTES["vibrant"])
    
    # Create scatter trace with enhanced styling
    # Normalize size column if provided (scale to reasonable marker sizes)
    if size_col and size_col in df.columns:
        size_values = df[size_col].astype(float)
        # Normalize to 0-1 range, then scale to 5-20 pixel range for markers
        if size_values.max() > size_values.min():
            normalized_size = (size_values - size_values.min()) / (size_values.max() - size_values.min())
            marker_sizes = 5 + (normalized_size * 15)  # Range: 5-20 pixels
        else:
            marker_sizes = 8  # Default if all values are same
    else:
        marker_sizes = 8  # Default size when no size_col provided
    
    if color_col and color_col in df.columns:
        fig.add_trace(go.Scatter(
            x=df[x_col],
            y=df[y_col],
            mode='markers',
            marker=dict(
                size=marker_sizes,
                color=df[color_col],
                colorscale=colors,
                showscale=True,
                colorbar=dict(title=format_column_label(color_col)),
                line=dict(width=1, color='white'),
                symbol=marker_shape,
                opacity=0.8
            ),
            text=df.index if hasattr(df.index, 'tolist') else None,
            hovertemplate=f'<b>%{{text}}</b><br>{x_label or x_col}: %{{x}}<br>{y_label or y_col}: %{{y}}<extra></extra>',
            name="Data Points"
        ))
    else:
        fig.add_trace(go.Scatter(
            x=df[x_col],
            y=df[y_col],
            mode='markers',
            marker=dict(
                size=marker_sizes,
                color=colors[0],
                line=dict(width=1, color='white'),
                symbol=marker_shape,
                opacity=0.8
            ),
            hovertemplate=f'{x_label or x_col}: %{{x}}<br>{y_label or y_col}: %{{y}}<extra></extra>',
            name="Data Points"
        ))
    
    # Add trendline if requested
    if show_trendline and len(df) > 1:
        z = np.polyfit(df[x_col].astype(float), df[y_col].astype(float), 1)
        p = np.poly1d(z)
        fig.add_trace(go.Scatter(
            x=df[x_col],
            y=p(df[x_col].astype(float)),
            mode='lines',
            name='Trend Line',
            line=dict(color=colors[-1], width=2, dash='dash'),
            hoverinfo='skip'
        ))
    
    fig.update_layout(
        title=dict(text=title, font=dict(size=18, color=MEDICAL_THEME["primary"])),
        xaxis_title=x_label or format_column_label(x_col),
        yaxis_title=y_label or format_column_label(y_col),
        template="plotly_white",
        plot_bgcolor="white",
        paper_bgcolor="white",
        height=450,
        hovermode='closest',
    )
    
    return fig


def create_wow_bar_chart(
    df: pd.DataFrame,
    x_col: str,
    y_col: str,
    color_col: Optional[str] = None,
    title: str = "",
    x_label: Optional[str] = None,
    y_label: Optional[str] = None,
    color_palette: str = "vibrant",
    show_values: bool = True,
) -> go.Figure:
    """Create a WOW bar chart with gradient colors and value labels."""
    colors = COLOR_PALETTES.get(color_palette, COLOR_PALETTES["vibrant"])
    
    if color_col and color_col in df.columns:
        fig = px.bar(
            df,
            x=x_col,
            y=y_col,
            color=color_col,
            color_continuous_scale=colors,
            title=title,
            labels={x_col: x_label or format_column_label(x_col), y_col: y_label or format_column_label(y_col)}
        )
    else:
        fig = px.bar(
            df,
            x=x_col,
            y=y_col,
            color=y_col,
            color_continuous_scale=colors,
            title=title,
            labels={x_col: x_label or format_column_label(x_col), y_col: y_label or format_column_label(y_col)}
        )
    
    if show_values:
        fig.update_traces(
            texttemplate='%{y:,.0f}',
            textposition='outside',
            marker=dict(line=dict(width=2, color='white'))
        )
    
    fig.update_layout(
        title=dict(font=dict(size=18, color=MEDICAL_THEME["primary"])),
        template="plotly_white",
        plot_bgcolor="white",
        paper_bgcolor="white",
        height=450,
        hovermode='x unified',
    )
    
    return fig


def create_wow_line_chart(
    df: pd.DataFrame,
    x_col: str,
    y_cols: List[str],
    title: str = "",
    x_label: Optional[str] = None,
    y_label: Optional[str] = None,
    color_palette: str = "vibrant",
    marker_shape: str = "circle",
) -> go.Figure:
    """Create a WOW multi-line chart with varied styles and markers."""
    fig = go.Figure()
    colors = COLOR_PALETTES.get(color_palette, COLOR_PALETTES["vibrant"])
    
    for i, y_col in enumerate(y_cols):
        fig.add_trace(go.Scatter(
            x=df[x_col],
            y=df[y_col],
            mode='lines+markers',
            name=format_column_label(y_col),
            line=dict(color=colors[i % len(colors)], width=3),
            marker=dict(size=8, symbol=marker_shape, color=colors[i % len(colors)]),
            hovertemplate=f'<b>{format_column_label(y_col)}</b><br>%{{x}}<br>%{{y}}<extra></extra>',
        ))
    
    fig.update_layout(
        title=dict(text=title, font=dict(size=18, color=MEDICAL_THEME["primary"])),
        xaxis_title=x_label or format_column_label(x_col),
        yaxis_title=y_label or "Value",
        template="plotly_white",
        plot_bgcolor="white",
        paper_bgcolor="white",
        height=450,
        hovermode='x unified',
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
    )
    
    return fig


def create_wow_pie_chart(
    df: pd.DataFrame,
    values_col: str,
    names_col: str,
    title: str = "",
    color_palette: str = "vibrant",
    hole: float = 0.4,
) -> go.Figure:
    """Create a WOW donut chart with enhanced styling."""
    colors = COLOR_PALETTES.get(color_palette, COLOR_PALETTES["vibrant"])
    
    fig = go.Figure(data=[go.Pie(
        labels=df[names_col],
        values=df[values_col],
        hole=hole,
        marker=dict(
            colors=colors[:len(df)],
            line=dict(color='white', width=2)
        ),
        textinfo='label+percent',
        textposition='outside',
        hovertemplate='<b>%{label}</b><br>Value: %{value}<br>Percentage: %{percent}<extra></extra>',
    )])
    
    fig.update_layout(
        title=dict(text=title, font=dict(size=18, color=MEDICAL_THEME["primary"])),
        template="plotly_white",
        plot_bgcolor="white",
        paper_bgcolor="white",
        height=450,
        showlegend=True,
    )
    
    return fig


def create_wow_heatmap(
    df: pd.DataFrame,
    x_col: str,
    y_col: str,
    values_col: str,
    title: str = "",
    color_palette: str = "vibrant",
) -> go.Figure:
    """Create a WOW gradient heatmap."""
    colors = COLOR_PALETTES.get(color_palette, COLOR_PALETTES["vibrant"])
    
    # Create pivot table for heatmap
    pivot_df = df.pivot_table(values=values_col, index=y_col, columns=x_col, aggfunc='mean')
    
    fig = go.Figure(data=go.Heatmap(
        z=pivot_df.values,
        x=pivot_df.columns,
        y=pivot_df.index,
        colorscale=colors,
        text=pivot_df.values,
        texttemplate='%{text:.1f}',
        textfont={"size": 10},
        hovertemplate='<b>%{y}</b> × <b>%{x}</b><br>Value: %{z}<extra></extra>',
    ))
    
    fig.update_layout(
        title=dict(text=title, font=dict(size=18, color=MEDICAL_THEME["primary"])),
        xaxis_title=format_column_label(x_col),
        yaxis_title=format_column_label(y_col),
        template="plotly_white",
        plot_bgcolor="white",
        paper_bgcolor="white",
        height=450,
    )
    
    return fig


def create_wow_area_chart(
    df: pd.DataFrame,
    x_col: str,
    y_cols: List[str],
    title: str = "",
    x_label: Optional[str] = None,
    y_label: Optional[str] = None,
    color_palette: str = "gradient_green",
    stacked: bool = False,
) -> go.Figure:
    """Create a WOW area chart with gradient fills."""
    fig = go.Figure()
    colors = COLOR_PALETTES.get(color_palette, COLOR_PALETTES["gradient_green"])
    
    for i, y_col in enumerate(y_cols):
        fig.add_trace(go.Scatter(
            x=df[x_col],
            y=df[y_col],
            mode='lines',
            name=format_column_label(y_col),
            fill='tonexty' if stacked and i > 0 else 'tozeroy',
            fillcolor=colors[i % len(colors)],
            line=dict(color=colors[i % len(colors)], width=3),
            hovertemplate=f'<b>{format_column_label(y_col)}</b><br>%{{x}}<br>%{{y}}<extra></extra>',
        ))
    
    fig.update_layout(
        title=dict(text=title, font=dict(size=18, color=MEDICAL_THEME["primary"])),
        xaxis_title=x_label or format_column_label(x_col),
        yaxis_title=y_label or "Value",
        template="plotly_white",
        plot_bgcolor="white",
        paper_bgcolor="white",
        height=450,
        hovermode='x unified',
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
    )
    
    return fig


def create_wow_radar_chart(
    df: pd.DataFrame,
    categories: List[str],
    values: Optional[List[str]] = None,
    group_col: Optional[str] = None,
    title: str = "",
    color_palette: str = "rainbow",
    fill_opacity: float = 0.3,
    show_legend: bool = True,
) -> go.Figure:
    """
    Create a colorful WOW radar chart for multi-dimensional comparisons.
    
    Args:
        df: DataFrame with data
        categories: List of column names for radar axes (categories)
        values: Optional list of value columns (if None, uses categories as both)
        group_col: Optional column name to group by (creates multiple radar traces)
        title: Chart title
        color_palette: Color palette name from RADAR_COLORS
        fill_opacity: Opacity of filled areas (0-1)
        show_legend: Whether to show legend
    
    Returns:
        Plotly Figure with radar chart
    """
    fig = go.Figure()
    
    # Get colors
    colors = RADAR_COLORS.get(color_palette, RADAR_COLORS["rainbow"])
    
    # If values not provided, use categories as both axes and values
    if values is None:
        values = categories
    
    # If group_col is provided, create multiple traces
    if group_col and group_col in df.columns:
        groups = df[group_col].unique()
        for idx, group in enumerate(groups):
            group_df = df[df[group_col] == group]
            if len(group_df) == 0:
                continue
            
            # Prepare data for this group
            theta = categories
            r = []
            for cat in categories:
                if cat in group_df.columns:
                    val = float(group_df[cat].iloc[0]) if len(group_df) > 0 else 0
                    r.append(val)
                else:
                    r.append(0)
            
            # Close the radar chart (connect last point to first)
            theta = theta + [theta[0]]
            r = r + [r[0]]
            
            fig.add_trace(go.Scatterpolar(
                r=r,
                theta=theta,
                fill='toself',
                fillcolor=colors[idx % len(colors)],
                line=dict(color=colors[idx % len(colors)], width=3),
                marker=dict(size=8, color=colors[idx % len(colors)]),
                name=str(group),
                opacity=fill_opacity,
                hovertemplate=f'<b>{group}</b><br>%{{theta}}: %{{r}}<extra></extra>',
            ))
    else:
        # Single trace - use first row or aggregate
        if len(df) > 1:
            # Aggregate if multiple rows
            data_row = df[categories].mean() if all(cat in df.columns for cat in categories) else df.iloc[0]
        else:
            data_row = df.iloc[0]
        
        # Prepare data
        theta = categories
        r = [float(data_row[cat]) if cat in data_row.index else 0 for cat in categories]
        
        # Close the radar chart
        theta = theta + [theta[0]]
        r = r + [r[0]]
        
        fig.add_trace(go.Scatterpolar(
            r=r,
            theta=theta,
            fill='toself',
            fillcolor=colors[0],
            line=dict(color=colors[0], width=4),
            marker=dict(size=10, color=colors[0]),
            name="Values",
            opacity=fill_opacity,
            hovertemplate='<b>%{theta}</b><br>Value: %{r}<extra></extra>',
        ))
    
    # Calculate max value for radial axis
    max_val = 0
    if all(cat in df.columns for cat in categories):
        max_val = max([df[cat].max() for cat in categories if cat in df.columns])
    elif len(df) > 0:
        max_val = max([float(df[cat].iloc[0]) if cat in df.columns else 0 for cat in categories])
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, max_val * 1.1] if max_val > 0 else [0, 100],
                showline=True,
                linecolor="gray",
                gridcolor="lightgray",
                gridwidth=1,
            ),
            angularaxis=dict(
                showline=True,
                linecolor="gray",
                gridcolor="lightgray",
                gridwidth=1,
            ),
            bgcolor="white",
        ),
        title=dict(
            text=title,
            font=dict(size=20, color=MEDICAL_THEME["primary"], family="Arial Black"),
            x=0.5,
            xanchor="center"
        ),
        showlegend=show_legend,
        legend=dict(
            orientation="v",
            yanchor="top",
            y=1,
            xanchor="left",
            x=1.1,
            font=dict(size=12)
        ) if show_legend else None,
        paper_bgcolor="white",
        plot_bgcolor="white",
        height=500,
        margin=dict(l=50, r=50, t=80, b=50),
    )
    
    return fig
