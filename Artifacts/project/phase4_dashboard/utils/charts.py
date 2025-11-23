"""
Phase 4 Dashboard - Chart Generation Utilities
Helper functions for creating Plotly visualizations
"""
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from typing import Optional
import pandas.api.types as pd_types


# Professional medical theme colors
MEDICAL_THEME = {
    "primary": "#4e2a84",      # Deep purple
    "secondary": "#8f67d1",    # Light purple
    "accent": "#2d7d32",       # Healthcare green
    "warning": "#f57c00",      # Orange
    "error": "#c62828",        # Red
    "success": "#388e3c",      # Green
    "info": "#1976d2",         # Blue
    "background": "#f8f9fa",   # Light gray
    "text": "#212529",         # Dark gray
}

# Label mapping for common column names - All columns from queries mapped with headline capitalization
LABEL_MAP = {
    # Query 1: ROI by Measure
    "measure_code": "HEDIS Measure",
    "measure_name": "Measure Name",
    "total_investment": "Total Investment ($)",
    "revenue_impact": "Revenue Impact ($)",
    "roi_ratio": "ROI Ratio",
    "successful_closures": "Successful Closures",
    "total_interventions": "Total Interventions",
    
    # Query 2: Cost per Closure by Activity
    "activity_name": "Activity Name",
    "avg_cost": "Average Cost ($)",
    "success_rate": "Success Rate (%)",
    "times_used": "Times Used",
    "cost_per_closure": "Cost per Closure ($)",
    
    # Query 3: Monthly Intervention Trend
    "month": "Month",
    "month_start": "Month",
    "total_investment": "Total Investment ($)",
    
    # Query 4: Budget Variance
    "budget_allocated": "Budget Allocated ($)",
    "actual_spent": "Actual Spent ($)",
    "variance": "Variance ($)",
    "variance_pct": "Variance (%)",
    "budget_status": "Budget Status",
    
    # Query 5: Cost Tier Comparison
    "cost_tier": "Cost Tier",
    "interventions_count": "Intervention Count",
    
    # Common/Additional
    "total_closures": "Total Closures",
    "overall_success_rate": "Overall Success Rate (%)",
    "net_benefit": "Net Benefit ($)",
}


def format_column_label(column_name: str) -> str:
    """
    Convert a column name to a human-readable label with headline capitalization.
    
    Args:
        column_name: Column name from dataframe
        
    Returns:
        Formatted label string with headline capitalization (never "Undefined")
    """
    if not column_name or str(column_name).strip() == "":
        return "Value"
    
    column_name = str(column_name).strip()
    
    # Check if we have a direct mapping first
    if column_name in LABEL_MAP:
        label = LABEL_MAP[column_name]
        if label and label != "Undefined" and label.lower() != "undefined":
            return label
    
    # Otherwise format the column name with headline capitalization (Title Case)
    # Replace underscores with spaces
    label = column_name.replace("_", " ")
    
    # Apply headline capitalization - capitalize first letter of each word
    words = label.split()
    formatted_words = []
    
    for word in words:
        if len(word) > 0:
            # Capitalize first letter, lowercase rest
            formatted_word = word[0].upper() + word[1:].lower() if len(word) > 1 else word[0].upper()
            formatted_words.append(formatted_word)
    
    label = " ".join(formatted_words)
    
    # Handle special cases and acronyms (preserve uppercase for known acronyms)
    label = label.replace("Roi", "ROI")
    label = label.replace("Id", "ID")
    label = label.replace("Hedis", "HEDIS")
    label = label.replace("Pct", "%")
    label = label.replace("Avg", "Average")
    label = label.replace("Avg Cost", "Average Cost")
    
    # Add units if suggested by column name but not present
    if "cost" in column_name.lower() and "$" not in label:
        if "avg" in column_name.lower() or "average" in column_name.lower():
            label = "Average Cost ($)"
        elif "total" in column_name.lower():
            label = "Total Investment ($)" if "investment" in column_name.lower() or "spent" in column_name.lower() else f"{label} ($)"
        else:
            label = f"{label} ($)" if label else "Cost ($)"
    elif "rate" in column_name.lower() and "%" not in label and "ratio" not in label.lower():
        label = f"{label} (%)"
    elif "pct" in column_name.lower() or "percentage" in column_name.lower():
        label = label.replace(" Pct", " (%)").replace("Pct", "%")
        if "%" not in label:
            label = f"{label} (%)"
    
    # Final check - never return "Undefined" or empty
    if not label or label.strip() == "" or label.lower() == "undefined" or label == "Undefined":
        # Ultimate fallback - use column name with proper title case formatting
        label = column_name.replace("_", " ").title()
        label = label.replace("Roi", "ROI").replace("Id", "ID").replace("Hedis", "HEDIS")
    
    return label


def create_bar_chart(
    df: pd.DataFrame,
    x_col: str,
    y_col: str,
    title: str,
    x_label: Optional[str] = None,
    y_label: Optional[str] = None,
    color_col: Optional[str] = None,
    color_scale: Optional[list] = None,
) -> go.Figure:
    """Create a professional bar chart."""
    # Format labels for all columns used in the chart
    labels_dict = {}
    
    # Always add labels for all columns used - force proper formatting
    for col in [x_col, y_col, color_col]:
        if col:
            if col == x_col:
                # Use provided x_label or format the column name
                label = x_label if x_label else format_column_label(col)
                labels_dict[col] = label
            elif col == y_col:
                # Use provided y_label or format the column name
                label = y_label if y_label else format_column_label(col)
                labels_dict[col] = label
            else:
                # Format color column name
                # If color_col equals y_col, reuse the y_col label
                if col == color_col and color_col == y_col:
                    label = labels_dict.get(y_col, format_column_label(col))
                else:
                    label = format_column_label(col)
                labels_dict[col] = label
            
            # Final safety check - ensure label is never "Undefined"
            if col in labels_dict:
                if not labels_dict[col] or labels_dict[col] == "Undefined" or labels_dict[col].lower() == "undefined":
                    labels_dict[col] = format_column_label(col)
                    # If still undefined, use manual formatting
                    if not labels_dict[col] or labels_dict[col] == "Undefined":
                        labels_dict[col] = col.replace("_", " ").title()
                        labels_dict[col] = labels_dict[col].replace("Roi", "ROI").replace("Id", "ID").replace("Hedis", "HEDIS")
    
    if color_col:
        # Check if color column is categorical (string type) or continuous (numeric)
        is_categorical = df[color_col].dtype == 'object' or pd_types.is_string_dtype(df[color_col]) or df[color_col].dtype.name == 'category'
        
        if is_categorical:
            # Use discrete color sequence for categorical data
            fig = px.bar(
                df,
                x=x_col,
                y=y_col,
                color=color_col,
                title=title,
                labels=labels_dict,
                color_discrete_map={
                    "Over Budget": MEDICAL_THEME["error"],
                    "Under Budget": MEDICAL_THEME["success"],
                    "On Budget": MEDICAL_THEME["accent"],
                } if color_col == "budget_status" else None,
                color_discrete_sequence=[MEDICAL_THEME["primary"], MEDICAL_THEME["secondary"], MEDICAL_THEME["accent"]],
            )
            # Update legend title for categorical color - set it explicitly
            legend_label = labels_dict.get(color_col, format_column_label(color_col))
            if not legend_label or legend_label == "Undefined" or legend_label.lower() == "undefined":
                legend_label = color_col.replace("_", " ").title()
                legend_label = legend_label.replace("Roi", "ROI").replace("Id", "ID")
            fig.update_layout(
                legend_title_text=str(legend_label),
                legend=dict(
                    title_text=str(legend_label),
                    font=dict(size=11),
                    orientation="h",  # Horizontal legend
                    yanchor="bottom",
                    y=-0.35,  # Further below chart to avoid overlap
                    xanchor="center",
                    x=0.5,
                    bgcolor='rgba(255,255,255,0.9)',
                    bordercolor='rgba(0,0,0,0.1)',
                    borderwidth=1
                ),
                height=550  # Preserve height
            )
        else:
            # Use continuous color scale for numeric data
            # Get colorbar label BEFORE creating figure - ensure it's never undefined
            # Special handling: if color_col equals y_col, prefer y_label if provided
            if color_col == y_col and y_label:
                colorbar_label = y_label
            else:
                colorbar_label = labels_dict.get(color_col)
                if not colorbar_label:
                    colorbar_label = format_column_label(color_col)
            
            # Final check - ensure label is never "Undefined"
            if not colorbar_label or colorbar_label == "Undefined" or colorbar_label.lower() == "undefined" or str(colorbar_label).strip() == "":
                colorbar_label = format_column_label(color_col)
                if not colorbar_label or colorbar_label == "Undefined":
                    colorbar_label = color_col.replace("_", " ").title()
                    colorbar_label = colorbar_label.replace("Roi", "ROI").replace("Id", "ID").replace("Hedis", "HEDIS")
            
            # Ensure it's a string
            colorbar_label = str(colorbar_label).strip()
            if not colorbar_label:
                colorbar_label = format_column_label(color_col)
            
            # Create figure WITHOUT labels dict first - we'll set labels manually
            fig = px.bar(
                df,
                x=x_col,
                y=y_col,
                color=color_col,
                title=title,
                labels=labels_dict,  # Still pass it but override manually after
                color_continuous_scale=color_scale or [MEDICAL_THEME["primary"], MEDICAL_THEME["secondary"]],
            )
            
            # FORCE set colorbar title - use the most direct method that works
            # Set colorbar title immediately using update_coloraxes (this is the standard method)
            fig.update_coloraxes(colorbar_title=colorbar_label)
            
            # Also set it via update_layout as backup
            fig.update_layout(
                coloraxis_colorbar_title=colorbar_label,
                coloraxis_colorbar_title_side="right",
                coloraxis_colorbar_title_font_size=11,
                height=550  # Preserve height
            )
            
            # Directly access and force set the colorbar title text
            # This is the most reliable method - directly modify the object
            if hasattr(fig.layout, 'coloraxis') and fig.layout.coloraxis:
                if hasattr(fig.layout.coloraxis, 'colorbar') and fig.layout.coloraxis.colorbar:
                    # Direct assignment - this is the most reliable
                    if hasattr(fig.layout.coloraxis.colorbar, 'title'):
                        if fig.layout.coloraxis.colorbar.title:
                            # Force set the text attribute directly
                            if hasattr(fig.layout.coloraxis.colorbar.title, 'text'):
                                fig.layout.coloraxis.colorbar.title.text = colorbar_label
                            else:
                                # Create a new title object
                                fig.layout.coloraxis.colorbar.title = dict(text=colorbar_label, side="right", font=dict(size=11))
                        else:
                            fig.layout.coloraxis.colorbar.title = dict(text=colorbar_label, side="right", font=dict(size=11))
                    else:
                        # Create title attribute
                        fig.layout.coloraxis.colorbar.title = dict(text=colorbar_label, side="right", font=dict(size=11))
    else:
        fig = px.bar(
            df,
            x=x_col,
            y=y_col,
            title=title,
            labels=labels_dict,
            color_discrete_sequence=[MEDICAL_THEME["primary"]],
        )
    
    # Format axis labels
    x_axis_title = x_label or format_column_label(x_col) if x_label is None else x_label
    y_axis_title = y_label or format_column_label(y_col) if y_label is None else y_label
    
    # Build layout dict - ensure title is set properly with responsive design
    layout_dict = {
        "template": "plotly_white",
        "plot_bgcolor": "white",
        "paper_bgcolor": "white",
        "font": dict(family="Arial, sans-serif", size=12, color=MEDICAL_THEME["text"]),
        "title": dict(
            text=str(title) if title else "",
            font=dict(size=14, color=MEDICAL_THEME["primary"]),
            x=0.5,
            xanchor="center",
            y=0.98,  # Position title higher
            yanchor="top",
            automargin=True,
            pad=dict(t=0, b=10)  # Minimal padding
        ),
        "xaxis": dict(
            gridcolor="#e0e0e0", 
            title=None,  # Remove axis title text ("HEDIS Measure", "Month", etc.)
            showticklabels=True,  # Show data labels (BPD, BCS, dates, etc.)
            showline=True,  # Show the axis line
            showgrid=True,  # Show grid lines
            automargin=True
        ),
        "yaxis": dict(
            gridcolor="#e0e0e0", 
            title=None,  # Remove axis title text ("ROI", "Success Rate", etc.)
            showticklabels=True,  # Show numbers (1.0, 1.2, etc.)
            showline=True,  # Show the axis line
            showgrid=True,  # Show grid lines
            automargin=True
        ),
        "hovermode": "x unified",
        "autosize": True,  # Make chart responsive for mobile
        "height": 550,  # Reduced height for better mobile display
        "margin": dict(l=60, r=30, t=80, b=80),  # Reduced margins for tighter spacing
    }
    
    # Apply layout - don't override legend/colorbar titles that were already set in categorical/continuous sections
    fig.update_layout(**layout_dict)
    
    # Final aggressive safety check - ensure colorbar/legend titles are never "Undefined"
    if color_col:
        is_categorical = (
            df[color_col].dtype == 'object' or 
            pd_types.is_string_dtype(df[color_col]) or 
            df[color_col].dtype.name == 'category'
        )
        
        # Get label from our dictionary - ensure it's properly formatted
        final_label = labels_dict.get(color_col)
        if not final_label:
            final_label = format_column_label(color_col)
        
        # Ensure label is never "Undefined"
        if not final_label or final_label == "Undefined" or final_label.lower() == "undefined" or final_label.strip() == "":
            final_label = format_column_label(color_col)
            if not final_label or final_label == "Undefined":
                final_label = color_col.replace("_", " ").title()
                final_label = final_label.replace("Roi", "ROI").replace("Id", "ID").replace("Hedis", "HEDIS")
        
        # Convert to string and strip
        final_label = str(final_label).strip()
        
        # Force update to ensure it's set correctly - try multiple methods
        if is_categorical:
            # Update legend title - preserve height
            fig.update_layout(legend_title_text=final_label, height=550)
            if hasattr(fig.layout, 'legend') and fig.layout.legend:
                if hasattr(fig.layout.legend, 'title'):
                    if hasattr(fig.layout.legend.title, 'text'):
                        fig.layout.legend.title.text = final_label
        else:
            # Update colorbar title - try all methods
            try:
                fig.update_coloraxes(colorbar_title=final_label)
            except:
                pass
            
            try:
                fig.update_layout(coloraxis_colorbar_title=final_label, height=550)
            except:
                pass
            
            # Update colorbar directly on traces - FORCE update
            for trace in fig.data:
                if hasattr(trace, 'marker') and trace.marker:
                    if hasattr(trace.marker, 'colorbar'):
                        # Force create/update colorbar title
                        if trace.marker.colorbar:
                            trace.marker.colorbar.title = dict(
                                text=final_label,
                                side="right",
                                font=dict(size=11)
                            )
                        else:
                            trace.marker.colorbar = dict(
                                title=dict(text=final_label, side="right", font=dict(size=11))
                            )
    
    # Final aggressive check - ensure NO trace has "Undefined" as name and no legend/colorbar has "Undefined" title
    for trace in fig.data:
        # Check trace name
        if hasattr(trace, 'name'):
            trace_name = str(trace.name) if trace.name else ""
            if not trace_name or trace_name.strip() == "" or trace_name.strip() == "Undefined" or trace_name.strip().lower() == "undefined":
                # Get proper label from y_col if available
                if y_col in labels_dict:
                    trace.name = labels_dict[y_col]
                else:
                    trace.name = format_column_label(y_col) if y_col else "Data Series"
        
        # Check colorbar if it exists - FORCE create/update
        if color_col and hasattr(trace, 'marker') and trace.marker:
            replacement_label = labels_dict.get(color_col, format_column_label(color_col))
            if not replacement_label or replacement_label == "Undefined":
                replacement_label = format_column_label(color_col)
            
            replacement_label = str(replacement_label).strip()
            
            # Force set colorbar title - create dict if needed
            if hasattr(trace.marker, 'colorbar'):
                if trace.marker.colorbar:
                    # Update existing colorbar
                    if hasattr(trace.marker.colorbar, 'title'):
                        if trace.marker.colorbar.title:
                            # Check if title is undefined
                            current_title = ""
                            if hasattr(trace.marker.colorbar.title, 'text'):
                                current_title = str(trace.marker.colorbar.title.text) if trace.marker.colorbar.title.text else ""
                            
                            if not current_title or current_title.strip() == "Undefined" or current_title.strip().lower() == "undefined":
                                trace.marker.colorbar.title = dict(text=replacement_label, side="right", font=dict(size=11))
                        else:
                            trace.marker.colorbar.title = dict(text=replacement_label, side="right", font=dict(size=11))
                    else:
                        trace.marker.colorbar.title = dict(text=replacement_label, side="right", font=dict(size=11))
                else:
                    # Create colorbar if it doesn't exist
                    trace.marker.colorbar = dict(
                        title=dict(text=replacement_label, side="right", font=dict(size=11))
                    )
    
    # Final check on layout legend/colorbar titles
    if hasattr(fig.layout, 'legend') and fig.layout.legend:
        if hasattr(fig.layout.legend, 'title') and fig.layout.legend.title:
            if hasattr(fig.layout.legend.title, 'text'):
                legend_title = str(fig.layout.legend.title.text) if fig.layout.legend.title.text else ""
                if not legend_title or legend_title.strip() == "Undefined" or legend_title.strip().lower() == "undefined":
                    if color_col:
                        replacement_label = labels_dict.get(color_col, format_column_label(color_col))
                    if not replacement_label or replacement_label == "Undefined":
                        replacement_label = format_column_label(color_col)
                        fig.update_layout(legend_title_text=str(replacement_label), height=550)
    
    # Final check on axis titles - ensure they're not "Undefined"
    if hasattr(fig.layout, 'xaxis') and fig.layout.xaxis:
        if hasattr(fig.layout.xaxis, 'title') and fig.layout.xaxis.title:
            if hasattr(fig.layout.xaxis.title, 'text'):
                x_title = str(fig.layout.xaxis.title.text) if fig.layout.xaxis.title.text else ""
                if not x_title or x_title.strip() == "Undefined" or x_title.strip().lower() == "undefined":
                    replacement_label = labels_dict.get(x_col, format_column_label(x_col))
                    fig.update_xaxes(title_text=str(replacement_label))
    
    if hasattr(fig.layout, 'yaxis') and fig.layout.yaxis:
        if hasattr(fig.layout.yaxis, 'title') and fig.layout.yaxis.title:
            if hasattr(fig.layout.yaxis.title, 'text'):
                y_title = str(fig.layout.yaxis.title.text) if fig.layout.yaxis.title.text else ""
                if not y_title or y_title.strip() == "Undefined" or y_title.strip().lower() == "undefined":
                    replacement_label = labels_dict.get(y_col, format_column_label(y_col))
                    fig.update_yaxes(title_text=str(replacement_label))
    
    # Final check on layout-level colorbar (for continuous color scales)
    if color_col:
        replacement_label = labels_dict.get(color_col, format_column_label(color_col))
        if not replacement_label or replacement_label == "Undefined":
            replacement_label = format_column_label(color_col)
        replacement_label = str(replacement_label).strip()
        
        # Check coloraxis.colorbar in layout (common location for continuous scales)
        if hasattr(fig.layout, 'coloraxis') and fig.layout.coloraxis:
            if hasattr(fig.layout.coloraxis, 'colorbar') and fig.layout.coloraxis.colorbar:
                if hasattr(fig.layout.coloraxis.colorbar, 'title'):
                    if fig.layout.coloraxis.colorbar.title:
                        current_title = str(fig.layout.coloraxis.colorbar.title.text) if hasattr(fig.layout.coloraxis.colorbar.title, 'text') and fig.layout.coloraxis.colorbar.title.text else ""
                        if not current_title or current_title.strip() == "Undefined" or current_title.strip().lower() == "undefined":
                            fig.layout.coloraxis.colorbar.title = dict(text=replacement_label, side="right", font=dict(size=11))
                    else:
                        fig.layout.coloraxis.colorbar.title = dict(text=replacement_label, side="right", font=dict(size=11))
                else:
                    # Create colorbar title if it doesn't exist
                    if not hasattr(fig.layout.coloraxis.colorbar, 'title'):
                        fig.layout.coloraxis.colorbar.title = dict(text=replacement_label, side="right", font=dict(size=11))
    
    # Final safety check: ensure height is always an integer, never None
    if not hasattr(fig.layout, 'height') or fig.layout.height is None:
        fig.update_layout(height=550)
    elif not isinstance(fig.layout.height, int):
        fig.update_layout(height=550)
    
    return fig


def create_scatter_plot(
    df: pd.DataFrame,
    x_col: str,
    y_col: str,
    size_col: Optional[str] = None,
    color_col: Optional[str] = None,
    text_col: Optional[str] = None,
    title: str = "",
    x_label: Optional[str] = None,
    y_label: Optional[str] = None,
) -> go.Figure:
    """Create a professional scatter plot with optional bubble sizing."""
    # Format labels for all columns used in the chart
    labels_dict = {}
    
    # Add labels for all columns that exist in dataframe
    for col in [x_col, y_col, size_col, color_col, text_col]:
        if col and col in df.columns:
            if col == x_col:
                labels_dict[col] = x_label or format_column_label(col)
            elif col == y_col:
                labels_dict[col] = y_label or format_column_label(col)
            else:
                labels_dict[col] = format_column_label(col)
    
    # Create scatter plot WITHOUT text labels to avoid overlap
    # All information will be shown in hover tooltips instead
    hover_data_dict = {}
    if text_col:
        hover_data_dict[text_col] = True  # Include text in hover but not as visible label
    
    fig = px.scatter(
        df,
        x=x_col,
        y=y_col,
        size=size_col,
        color=color_col,
        title=title,
        labels=labels_dict,
        color_continuous_scale=[MEDICAL_THEME["primary"], MEDICAL_THEME["secondary"], MEDICAL_THEME["accent"]],
        size_max=30,
        hover_data=hover_data_dict if hover_data_dict else None,
    )
    
    # Format axis labels
    x_axis_title = x_label or format_column_label(x_col) if x_label is None else x_label
    y_axis_title = y_label or format_column_label(y_col) if y_label is None else y_label
    
    # Format colorbar label if color column exists - do this BEFORE layout update
    colorbar_title = None
    if color_col:
        colorbar_title = format_column_label(color_col)
    
    fig.update_layout(
        template="plotly_white",
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(family="Arial, sans-serif", size=12, color=MEDICAL_THEME["text"]),
        title=dict(
            text=str(title) if title else "",
            font=dict(size=14, color=MEDICAL_THEME["primary"]),
            x=0.5,
            xanchor="center",
            y=0.98,  # Position title higher
            yanchor="top",
            automargin=True,
            pad=dict(t=0, b=10)  # Minimal padding
        ),
        xaxis=dict(
            gridcolor="#e0e0e0", 
            title=None,  # Remove axis title text ("HEDIS Measure", "Month", etc.)
            showticklabels=True,  # Show data labels (BPD, BCS, dates, etc.)
            showline=True,  # Show the axis line
            showgrid=True,  # Show grid lines
            automargin=True
        ),
        yaxis=dict(
            gridcolor="#e0e0e0", 
            title=None,  # Remove axis title text ("ROI", "Success Rate", etc.)
            showticklabels=True,  # Show numbers (1.0, 1.2, etc.)
            showline=True,  # Show the axis line
            showgrid=True,  # Show grid lines
            automargin=True
        ),
        hovermode="closest",
        autosize=True,  # Make chart responsive for mobile
        height=550,  # Reduced height for better mobile display
        margin=dict(l=60, r=30, t=80, b=80),  # Reduced margins for tighter spacing
    )
    
    # Set colorbar title after layout update
    if color_col and colorbar_title:
        # Ensure label is never "Undefined"
        if not colorbar_title or colorbar_title == "Undefined" or colorbar_title.lower() == "undefined":
            colorbar_title = color_col.replace("_", " ").title()
        
        # Try multiple methods to ensure colorbar title is set
        try:
            fig.update_coloraxes(colorbar_title=colorbar_title)
        except:
            try:
                fig.update_layout(coloraxis_colorbar_title=colorbar_title, height=550)
            except:
                # Last resort: try updating traces
                try:
                    fig.update_traces(marker_colorbar_title=colorbar_title)
                except:
                    pass
    
    # Update hover template to show all information clearly
    # Remove text labels from points - show everything in hover tooltips instead
    if text_col:
        # Build hover template with activity name from hover_data
        # Plotly Express puts hover_data columns in customdata array
        # customdata[0] contains the text_col values when hover_data is used
        hover_template = (
            f'<b>%{{customdata[0]}}</b><br>' +
            f'{x_axis_title}: $%{{x:.2f}}<br>' +
            f'{y_axis_title}: %{{y:.1f}}%<br>'
        )
        if size_col:
            hover_template += f'{format_column_label(size_col)}: %{{marker.size}}<br>'
        hover_template += '<extra></extra>'
        
        fig.update_traces(hovertemplate=hover_template)
    else:
        # Standard hover template without text column
        hover_template = (
            f'<b>{x_axis_title}:</b> $%{{x:.2f}}<br>' +
            f'<b>{y_axis_title}:</b> %{{y:.1f}}%<br>'
        )
        if size_col:
            hover_template += f'<b>{format_column_label(size_col)}:</b> %{{marker.size}}<br>'
        hover_template += '<extra></extra>'
        
        fig.update_traces(hovertemplate=hover_template)
    
    # Final safety check: ensure height is always an integer, never None
    if not hasattr(fig.layout, 'height') or fig.layout.height is None:
        fig.update_layout(height=550)
    elif not isinstance(fig.layout.height, int):
        fig.update_layout(height=550)
    
    return fig


def create_line_chart(
    df: pd.DataFrame,
    x_col: str,
    y_cols: list,
    title: str,
    x_label: Optional[str] = None,
    y_label: Optional[str] = None,
) -> go.Figure:
    """Create a professional multi-line chart."""
    fig = go.Figure()
    
    colors = [MEDICAL_THEME["primary"], MEDICAL_THEME["secondary"], MEDICAL_THEME["accent"], MEDICAL_THEME["info"]]
    
    # Better label mapping for line charts
    line_label_map = {
        "total_interventions": "Total Interventions",
        "successful_closures": "Successful Closures",
        "success_rate": "Success Rate (%)",
        "avg_cost": "Average Cost ($)",
        "total_investment": "Total Investment ($)",
    }
    
    for i, y_col in enumerate(y_cols):
        # Use specific mapping if available, otherwise use format function
        if y_col in line_label_map:
            label = line_label_map[y_col]
        else:
            label = format_column_label(y_col)
        
        # Final safety check - ensure label is never empty or "Undefined"
        if not label or label.strip() == "" or label == "Undefined" or label.lower() == "undefined":
            # Fallback to manual formatting
            label = y_col.replace("_", " ").title()
            label = label.replace("Roi", "ROI")
            label = label.replace("Id", "ID")
        
        fig.add_trace(
            go.Scatter(
                x=df[x_col],
                y=df[y_col],
                mode="lines+markers",
                name=str(label),  # Ensure it's a string
                line=dict(color=colors[i % len(colors)], width=3),
                marker=dict(size=8),
                hovertemplate=f"<b>{label}</b><br>%{{x}}<br>%{{y}}<extra></extra>",
            )
        )
    
    # Format axis labels
    x_axis_title = x_label or format_column_label(x_col) if x_label is None else x_label
    y_axis_title = y_label or "Value" if y_label is None else y_label
    
    fig.update_layout(
        template="plotly_white",
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(family="Arial, sans-serif", size=12, color=MEDICAL_THEME["text"]),
        title=dict(
            text=str(title) if title else "",
            font=dict(size=14, color=MEDICAL_THEME["primary"]),
            x=0.5,
            xanchor="center",
            y=0.98,  # Position title higher
            yanchor="top",
            automargin=True,
            pad=dict(t=0, b=10)  # Minimal padding
        ),
        xaxis=dict(
            gridcolor="#e0e0e0", 
            title=None,  # Remove axis title text ("HEDIS Measure", "Month", etc.)
            showticklabels=True,  # Show data labels (BPD, BCS, dates, etc.)
            showline=True,  # Show the axis line
            showgrid=True,  # Show grid lines
            automargin=True
        ),
        yaxis=dict(
            gridcolor="#e0e0e0", 
            title=None,  # Remove axis title text ("ROI", "Success Rate", etc.)
            showticklabels=True,  # Show numbers (1.0, 1.2, etc.)
            showline=True,  # Show the axis line
            showgrid=True,  # Show grid lines
            automargin=True
        ),
        hovermode="x unified",
        legend=dict(
            orientation="h", 
            yanchor="bottom", 
            y=-0.3,  # Below chart
            xanchor="center", 
            x=0.5,
            title_text="",
            font=dict(size=11),
            bgcolor='rgba(255,255,255,0.9)',
            bordercolor='rgba(0,0,0,0.1)',
            borderwidth=1
        ),
        autosize=True,  # Make chart responsive for mobile
        height=550,  # Reduced height for better mobile display
        margin=dict(l=60, r=30, t=80, b=80),  # Reduced margins for tighter spacing
    )
    
    # Explicitly update ALL trace names to ensure proper labels - FORCE update regardless of current state
    for i, trace in enumerate(fig.data):
        if i < len(y_cols):
            y_col = y_cols[i]
            # Always set the label from our mapping - force it
            if y_col in line_label_map:
                new_name = line_label_map[y_col]
            else:
                new_name = format_column_label(y_col)
                # Final fallback
                if not new_name or new_name == "Undefined" or new_name.lower() == "undefined":
                    new_name = y_col.replace("_", " ").title()
                    new_name = new_name.replace("Roi", "ROI").replace("Id", "ID")
            
            # Force update - convert to string and strip any whitespace
            trace.name = str(new_name).strip()
            
            # Also update hovertemplate to ensure it uses the correct name
            if hasattr(trace, 'hovertemplate') and trace.hovertemplate:
                trace.hovertemplate = trace.hovertemplate.replace(trace.name or "", str(new_name))
            if not hasattr(trace, 'hovertemplate') or not trace.hovertemplate:
                trace.hovertemplate = f"<b>{new_name}</b><br>%{{x}}<br>%{{y}}<extra></extra>"
    
    # Final check - ensure NO trace has "Undefined" as name
    for trace in fig.data:
        if not trace.name or str(trace.name).strip() == "" or str(trace.name).strip() == "Undefined" or str(trace.name).strip().lower() == "undefined":
            trace.name = "Data Series"  # Safe fallback
    
    # Final safety check: ensure height is always an integer, never None
    if not hasattr(fig.layout, 'height') or fig.layout.height is None:
        fig.update_layout(height=550)
    elif not isinstance(fig.layout.height, int):
        fig.update_layout(height=550)
    
    return fig


def create_waterfall_chart(
    df: pd.DataFrame,
    measure_col: str,
    budget_col: str,
    actual_col: str,
    variance_col: str,
    title: str,
) -> go.Figure:
    """Create a waterfall-style variance chart."""
    fig = go.Figure()
    
    # Add budget bars
    fig.add_trace(
        go.Bar(
            name="Budget Allocated",
            x=df[measure_col],
            y=df[budget_col],
            marker_color=MEDICAL_THEME["info"],
            text=df[budget_col].apply(lambda x: f"${x:,.0f}"),
            textposition="outside",
        )
    )
    
    # Add actual bars
    fig.add_trace(
        go.Bar(
            name="Actual Spent",
            x=df[measure_col],
            y=df[actual_col],
            marker_color=MEDICAL_THEME["primary"],
            text=df[actual_col].apply(lambda x: f"${x:,.0f}"),
            textposition="outside",
        )
    )
    
    # Add variance indicator
    df_variance = df.copy()
    df_variance["variance_color"] = df_variance[variance_col].apply(
        lambda x: MEDICAL_THEME["error"] if x > 0 else MEDICAL_THEME["success"] if x < 0 else MEDICAL_THEME["accent"]
    )
    
    fig.add_trace(
        go.Bar(
            name="Variance",
            x=df[measure_col],
            y=df[variance_col].abs(),
            marker_color=df_variance["variance_color"],
            text=df[variance_col].apply(lambda x: f"${x:+,.0f}"),
            textposition="outside",
        )
    )
    
    fig.update_layout(
        template="plotly_white",
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(family="Arial, sans-serif", size=12, color=MEDICAL_THEME["text"]),
        title=dict(
            text=str(title) if title else "",
            font=dict(size=14, color=MEDICAL_THEME["primary"]),
            x=0.5,
            xanchor="center",
            y=0.98,  # Position title higher
            yanchor="top",
            automargin=True,
            pad=dict(t=0, b=10)  # Minimal padding
        ),
        xaxis=dict(
            gridcolor="#e0e0e0", 
            title=None,  # Remove axis title text ("HEDIS Measure", "Month", etc.)
            showticklabels=True,  # Show data labels (BPD, BCS, dates, etc.)
            showline=True,  # Show the axis line
            showgrid=True,  # Show grid lines
            automargin=True
        ),
        yaxis=dict(
            gridcolor="#e0e0e0", 
            title=None,  # Remove axis title text ("ROI", "Success Rate", etc.)
            showticklabels=True,  # Show numbers (1.0, 1.2, etc.)
            showline=True,  # Show the axis line
            showgrid=True,  # Show grid lines
            automargin=True
        ),
        barmode="group",
        hovermode="x unified",
        legend=dict(
            orientation="h", 
            yanchor="bottom", 
            y=-0.3,  # Below chart
            xanchor="center", 
            x=0.5,
            bgcolor='rgba(255,255,255,0.9)',
            bordercolor='rgba(0,0,0,0.1)',
            borderwidth=1
        ),
        autosize=True,  # Make chart responsive for mobile
        height=550,  # Reduced height for better mobile display
        margin=dict(l=60, r=30, t=80, b=80),  # Reduced margins for tighter spacing
    )
    
    # Final safety check: ensure height is always an integer, never None
    if not hasattr(fig.layout, 'height') or fig.layout.height is None:
        fig.update_layout(height=550)
    elif not isinstance(fig.layout.height, int):
        fig.update_layout(height=550)
    
    return fig


def create_grouped_bar_chart(
    df: pd.DataFrame,
    x_col: str,
    y_cols: list,
    title: str,
    x_label: Optional[str] = None,
    y_label: Optional[str] = None,
) -> go.Figure:
    """Create a grouped bar chart."""
    fig = go.Figure()
    
    colors = [MEDICAL_THEME["primary"], MEDICAL_THEME["secondary"], MEDICAL_THEME["accent"]]
    
    # Better label mapping for grouped bar charts
    bar_label_map = {
        "avg_cost": "Average Cost ($)",
        "cost_per_closure": "Cost per Closure ($)",
        "interventions_count": "Intervention Count",
        "successful_closures": "Successful Closures",
        "total_investment": "Total Investment ($)",
        "success_rate": "Success Rate (%)",
    }
    
    for i, y_col in enumerate(y_cols):
        # Use specific mapping if available, otherwise use format function
        if y_col in bar_label_map:
            label = bar_label_map[y_col]
        else:
            label = format_column_label(y_col)
        
        # Final safety check - ensure label is never empty or "Undefined"
        if not label or label.strip() == "" or label == "Undefined" or label.lower() == "undefined":
            # Fallback to manual formatting
            label = y_col.replace("_", " ").title()
            label = label.replace("Roi", "ROI")
            label = label.replace("Id", "ID")
        
        # Format text based on column type
        if "cost" in y_col.lower() or "investment" in y_col.lower():
            text_values = df[y_col].apply(lambda x: f"${x:,.0f}" if isinstance(x, (int, float)) else str(x))
        else:
            text_values = df[y_col].apply(lambda x: f"{x:.1f}" if isinstance(x, (int, float)) else str(x))
        
        fig.add_trace(
            go.Bar(
                name=str(label),  # Ensure it's a string
                x=df[x_col],
                y=df[y_col],
                marker_color=colors[i % len(colors)],
                text=text_values,
                textposition="outside",
                hovertemplate=f"<b>{label}</b><br>%{{x}}<br>%{{y}}<extra></extra>",
            )
        )
    
    # Format axis labels
    x_axis_title = x_label or format_column_label(x_col) if x_label is None else x_label
    y_axis_title = y_label or "Value" if y_label is None else y_label
    
    fig.update_layout(
        template="plotly_white",
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(family="Arial, sans-serif", size=12, color=MEDICAL_THEME["text"]),
        title=dict(
            text=str(title) if title else "",
            font=dict(size=14, color=MEDICAL_THEME["primary"]),
            x=0.5,
            xanchor="center",
            y=0.98,  # Position title higher
            yanchor="top",
            automargin=True,
            pad=dict(t=0, b=10)  # Minimal padding
        ),
        xaxis=dict(
            gridcolor="#e0e0e0", 
            title=None,  # Remove axis title text ("HEDIS Measure", "Month", etc.)
            showticklabels=True,  # Show data labels (BPD, BCS, dates, etc.)
            showline=True,  # Show the axis line
            showgrid=True,  # Show grid lines
            automargin=True
        ),
        yaxis=dict(
            gridcolor="#e0e0e0", 
            title=None,  # Remove axis title text ("ROI", "Success Rate", etc.)
            showticklabels=True,  # Show numbers (1.0, 1.2, etc.)
            showline=True,  # Show the axis line
            showgrid=True,  # Show grid lines
            automargin=True
        ),
        barmode="group",
        hovermode="x unified",
        legend=dict(
            orientation="h", 
            yanchor="bottom", 
            y=-0.3,  # Below chart
            xanchor="center", 
            x=0.5,
            title_text="",
            font=dict(size=11),
            bgcolor='rgba(255,255,255,0.9)',
            bordercolor='rgba(0,0,0,0.1)',
            borderwidth=1
        ),
        autosize=True,  # Make chart responsive for mobile
        height=550,  # Reduced height for better mobile display
        margin=dict(l=60, r=30, t=80, b=80),  # Reduced margins for tighter spacing
    )
    
    # Explicitly update ALL trace names to ensure proper labels - FORCE update regardless of current state
    for i, trace in enumerate(fig.data):
        if i < len(y_cols):
            y_col = y_cols[i]
            # Always set the label from our mapping - force it
            if y_col in bar_label_map:
                new_name = bar_label_map[y_col]
            else:
                new_name = format_column_label(y_col)
                # Final fallback
                if not new_name or new_name == "Undefined" or new_name.lower() == "undefined":
                    new_name = y_col.replace("_", " ").title()
                    new_name = new_name.replace("Roi", "ROI").replace("Id", "ID")
            
            # Force update - convert to string and strip any whitespace
            trace.name = str(new_name).strip()
            
            # Also update hovertemplate to ensure it uses the correct name
            if hasattr(trace, 'hovertemplate') and trace.hovertemplate:
                trace.hovertemplate = trace.hovertemplate.replace(trace.name or "", str(new_name))
            if not hasattr(trace, 'hovertemplate') or not trace.hovertemplate:
                trace.hovertemplate = f"<b>{new_name}</b><br>%{{x}}<br>%{{y}}<extra></extra>"
    
    # Final check - ensure NO trace has "Undefined" as name
    for trace in fig.data:
        if not trace.name or str(trace.name).strip() == "" or str(trace.name).strip() == "Undefined" or str(trace.name).strip().lower() == "undefined":
            trace.name = "Data Series"  # Safe fallback
    
    # Final safety check: ensure height is always an integer, never None
    if not hasattr(fig.layout, 'height') or fig.layout.height is None:
        fig.update_layout(height=550)
    elif not isinstance(fig.layout.height, int):
        fig.update_layout(height=550)
    
    return fig

