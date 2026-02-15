"""
Reusable visualization components for StarGuard AI
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, List, Any, Optional
import pandas as pd

def render_efficiency_gauge(efficiency_score: float, title: str = "Efficiency Score"):
    """
    Render an efficiency gauge chart.
    
    Args:
        efficiency_score: Score from 0-100
        title: Chart title
        
    Returns:
        plotly.graph_objects.Figure: The gauge chart figure
    """
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=efficiency_score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': title, 'font': {'size': 24}},
        delta={'reference': 50, 'increasing': {'color': "green"}},
        gauge={
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "darkblue"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 50], 'color': '#FEE2E2'},
                {'range': [50, 75], 'color': '#FEF3C7'},
                {'range': [75, 100], 'color': '#D1FAE5'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    
    fig.update_layout(
        height=300,
        margin=dict(l=20, r=20, t=50, b=20),
        font={'color': "darkblue", 'family': "Arial"}
    )
    
    return fig

def render_context_layers(context: Dict[str, Any]):
    """
    Render 3-layer context visualization.
    
    Args:
        context: Context dict with layer_1_domain, layer_2_measure, layer_3_query
    """
    col1, col2, col3 = st.columns(3)
    
    with col1:
        has_layer_1 = bool(context.get('layer_1_domain', {}).get('hedis_overview'))
        st.markdown(f"""
        <div style='background: #DBEAFE; padding: 20px; border-radius: 10px; border-left: 4px solid #2563EB;'>
            <h4>Layer 1: Domain</h4>
            <p style='font-size: 36px; margin: 10px 0;'>{'✅' if has_layer_1 else '❌'}</p>
            <p>{'Cached' if has_layer_1 else 'Missing'}</p>
            <small>{'TTL: 1 hour' if has_layer_1 else 'Needs retrieval'}</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        layer_2_count = len(context.get('layer_2_measure', {}))
        st.markdown(f"""
        <div style='background: #D1FAE5; padding: 20px; border-radius: 10px; border-left: 4px solid #10B981;'>
            <h4>Layer 2: Measures</h4>
            <p style='font-size: 36px; margin: 10px 0;'>{'✅' if layer_2_count > 0 else '⚠️'}</p>
            <p>{layer_2_count} measures</p>
            <small>TTL: 5 minutes</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div style='background: #E9D5FF; padding: 20px; border-radius: 10px; border-left: 4px solid #8B5CF6;'>
            <h4>Layer 3: Query</h4>
            <p style='font-size: 36px; margin: 10px 0;'>🔄</p>
            <p>Fresh data</p>
            <small>TTL: 30 seconds</small>
        </div>
        """, unsafe_allow_html=True)

def render_execution_timeline(steps: List[Any], results: Optional[List[Any]] = None):
    """
    Render execution timeline with steps.
    
    Args:
        steps: List of ExecutionStep objects (or dicts with type, reasoning, depends_on, confidence)
        results: Optional list of ExecutionResult objects (or dicts with success, execution_time, error)
    """
    for i, step in enumerate(steps, 1):
        # Handle both objects and dicts
        step_type = step.type.value if hasattr(step, 'type') else step.get('type', 'unknown')
        if isinstance(step_type, str) and not step_type.startswith('step_'):
            step_type_display = step_type.upper()
        else:
            step_type_display = step_type
            
        step_reasoning = step.reasoning if hasattr(step, 'reasoning') else step.get('reasoning', 'N/A')
        step_depends = step.depends_on if hasattr(step, 'depends_on') else step.get('depends_on', [])
        step_confidence = step.confidence if hasattr(step, 'confidence') else step.get('confidence', 0)
        
        with st.expander(f"**Step {i}: {step_type_display}**", expanded=(i==1)):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"**Reasoning:** {step_reasoning}")
                if step_depends:
                    st.caption(f"Depends on: {', '.join(step_depends)}")
                
                # Show result if available
                if results and i <= len(results):
                    result = results[i-1]
                    result_success = result.success if hasattr(result, 'success') else result.get('success', False)
                    result_time = result.execution_time if hasattr(result, 'execution_time') else result.get('execution_time', 0)
                    result_error = result.error if hasattr(result, 'error') else result.get('error', '')
                    
                    if result_success:
                        st.success(f"✅ Completed in {result_time}s")
                    else:
                        st.error(f"❌ Failed: {result_error}")
            
            with col2:
                st.metric("Confidence", f"{step_confidence:.0%}")

def render_performance_comparison(
    baseline_time: float,
    optimized_time: float,
    baseline_cost: float,
    optimized_cost: float,
    baseline_tools: int,
    optimized_tools: int
):
    """
    Render performance comparison chart.
    
    Args:
        baseline_time: Baseline execution time (seconds)
        optimized_time: Optimized execution time (seconds)
        baseline_cost: Baseline cost ($)
        optimized_cost: Optimized cost ($)
        baseline_tools: Baseline number of tools
        optimized_tools: Optimized number of tools
    """
    # Calculate improvements
    time_improvement = -((1 - optimized_time/baseline_time)*100) if baseline_time > 0 else 0
    cost_improvement = -((1 - optimized_cost/baseline_cost)*100) if baseline_cost > 0 else 0
    tools_improvement = -((1 - optimized_tools/baseline_tools)*100) if baseline_tools > 0 else 0
    
    comparison_df = pd.DataFrame({
        'Metric': ['Time (s)', 'Cost ($)', 'Tools'],
        'Traditional RAG': [baseline_time, baseline_cost, baseline_tools],
        'StarGuard AI': [optimized_time, optimized_cost, optimized_tools],
        'Improvement': [
            f'{time_improvement:.0f}%',
            f'{cost_improvement:.0f}%',
            f'{tools_improvement:.0f}%'
        ]
    })
    
    st.dataframe(
        comparison_df,
        use_container_width=True,
        hide_index=True
    )
    
    # Bar chart
    fig = go.Figure()
    
    metrics = ['Time (s)', 'Cost ($)', 'Tools']
    
    fig.add_trace(go.Bar(
        name='Traditional RAG',
        x=metrics,
        y=[baseline_time, baseline_cost, baseline_tools],
        marker_color='#EF4444'
    ))
    
    fig.add_trace(go.Bar(
        name='StarGuard AI',
        x=metrics,
        y=[optimized_time, optimized_cost, optimized_tools],
        marker_color='#10B981'
    ))
    
    fig.update_layout(
        title="Performance Comparison",
        barmode='group',
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)

def render_success_box(title: str, content: str):
    """Render a success message box."""
    st.markdown(f"""
    <div style='background: #D1FAE5; padding: 20px; border-radius: 10px; border-left: 5px solid #10B981;'>
        <h3 style='color: #065F46; margin-top: 0;'>{title}</h3>
        <p style='color: #065F46;'>{content}</p>
    </div>
    """, unsafe_allow_html=True)

def render_warning_box(title: str, content: str):
    """Render a warning message box."""
    st.markdown(f"""
    <div style='background: #FEF3C7; padding: 20px; border-radius: 10px; border-left: 5px solid #F59E0B;'>
        <h3 style='color: #92400E; margin-top: 0;'>{title}</h3>
        <p style='color: #92400E;'>{content}</p>
    </div>
    """, unsafe_allow_html=True)

def render_metric_card(title: str, value: str, subtitle: str = "", color: str = "#2563EB"):
    """Render a metric card."""
    st.markdown(f"""
    <div style='background: #F8FAFC; padding: 20px; border-radius: 10px; border-left: 4px solid {color};'>
        <h4 style='margin: 0 0 10px 0; color: #64748B;'>{title}</h4>
        <p style='font-size: 36px; font-weight: bold; margin: 10px 0; color: {color};'>{value}</p>
        <p style='margin: 0; color: #64748B; font-size: 14px;'>{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)



