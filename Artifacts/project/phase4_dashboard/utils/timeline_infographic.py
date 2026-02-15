"""
StarGuard AI Development Timeline Infographic
Shows the 6-month development journey condensed from 22 years of experience
"""

import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
from datetime import datetime, timedelta

def create_timeline_infographic():
    """
    Create a professional timeline infographic showing StarGuard AI development
    """
    
    # Timeline data
    timeline_data = [
        {
            "month": "Month 1-2",
            "title": "Core Data Architecture",
            "subtitle": "Synthetic Data Generation",
            "description": "Foundation: PostgreSQL schema design, data modeling, synthetic HEDIS data generation",
            "color": "#4A3D6F",
            "start": 0,
            "end": 2
        },
        {
            "month": "Month 2-3",
            "title": "Dashboard Development",
            "subtitle": "Visualization & UI",
            "description": "Streamlit dashboard, Plotly visualizations, responsive design, user interface",
            "color": "#6F5F96",
            "start": 2,
            "end": 3
        },
        {
            "month": "Month 3-4",
            "title": "Predictive Models",
            "subtitle": "ML Integration",
            "description": "Gap closure predictions, ROI models, scenario modeling, machine learning pipelines",
            "color": "#8B7BA8",
            "start": 3,
            "end": 4
        },
        {
            "month": "Month 4-5",
            "title": "AI Context Engineering",
            "subtitle": "Chatbot & RAG",
            "description": "Local LLM processing, context engineering, agentic RAG, secure AI chatbot",
            "color": "#A896C0",
            "start": 4,
            "end": 5
        },
        {
            "month": "Month 5-6",
            "title": "Production Hardening",
            "subtitle": "Mobile Optimization",
            "description": "Mobile responsiveness, performance optimization, security hardening, deployment",
            "color": "#C5B3D8",
            "start": 5,
            "end": 6
        }
    ]
    
    # Create figure
    fig = go.Figure()
    
    # Add timeline bars
    y_positions = []
    for i, phase in enumerate(timeline_data):
        y_pos = len(timeline_data) - i - 1
        y_positions.append(y_pos)
        
        # Main timeline bar
        fig.add_trace(go.Scatter(
            x=[phase["start"], phase["end"]],
            y=[y_pos, y_pos],
            mode='lines+markers',
            line=dict(color=phase["color"], width=12),
            marker=dict(size=20, color=phase["color"]),
            name=phase["month"],
            hovertemplate=f"<b>{phase['month']}</b><br>" +
                         f"<b>{phase['title']}</b><br>" +
                         f"{phase['subtitle']}<br>" +
                         f"{phase['description']}<extra></extra>",
            showlegend=False
        ))
        
        # Add text annotations
        mid_x = (phase["start"] + phase["end"]) / 2
        
        # Month label
        fig.add_annotation(
            x=mid_x,
            y=y_pos + 0.25,
            text=f"<b>{phase['month']}</b>",
            showarrow=False,
            font=dict(size=14, color=phase["color"], family="Arial Black"),
            xref="x",
            yref="y"
        )
        
        # Title
        fig.add_annotation(
            x=mid_x,
            y=y_pos,
            text=f"<b>{phase['title']}</b>",
            showarrow=False,
            font=dict(size=16, color="#FFFFFF", family="Arial"),
            xref="x",
            yref="y",
            bgcolor=phase["color"],
            bordercolor=phase["color"],
            borderwidth=2,
            borderpad=8
        )
        
        # Subtitle
        fig.add_annotation(
            x=mid_x,
            y=y_pos - 0.25,
            text=phase['subtitle'],
            showarrow=False,
            font=dict(size=12, color="#666666", family="Arial"),
            xref="x",
            yref="y"
        )
    
    # Add vertical timeline line
    fig.add_trace(go.Scatter(
        x=[0, 6],
        y=[-0.5, -0.5],
        mode='lines',
        line=dict(color="#4ade80", width=4),
        showlegend=False,
        hoverinfo='skip'
    ))
    
    # Add start and end markers
    fig.add_trace(go.Scatter(
        x=[0, 6],
        y=[-0.5, -0.5],
        mode='markers',
        marker=dict(size=25, color="#4ade80", symbol="circle", line=dict(width=3, color="#FFFFFF")),
        showlegend=False,
        hoverinfo='skip'
    ))
    
    # Add "Start" and "6 Months" labels
    fig.add_annotation(
        x=0,
        y=-0.9,
        text="<b>START</b>",
        showarrow=False,
        font=dict(size=12, color="#4ade80", family="Arial Black"),
        xref="x",
        yref="y"
    )
    
    fig.add_annotation(
        x=6,
        y=-0.9,
        text="<b>6 MONTHS</b>",
        showarrow=False,
        font=dict(size=12, color="#4ade80", family="Arial Black"),
        xref="x",
        yref="y"
    )
    
    # Add experience note at the top
    fig.add_annotation(
        x=3,
        y=len(timeline_data) + 0.5,
        text="<b>22 Years of Healthcare Data Experience</b><br>" +
             "<i>Condensed into a portfolio showing thinking, not just coding</i>",
        showarrow=False,
        font=dict(size=14, color="#4A3D6F", family="Arial"),
        xref="x",
        yref="y",
        bgcolor="#E8F5E9",
        bordercolor="#4ade80",
        borderwidth=2,
        borderpad=10,
        align="center"
    )
    
    # Update layout
    fig.update_layout(
        title={
            'text': '<b>StarGuard AI Development Timeline</b><br>' +
                   '<span style="font-size:14px; color:#666666">Built in Evenings & Weekends Over 6 Months</span>',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 24, 'color': '#4A3D6F', 'family': 'Arial Black'}
        },
        xaxis=dict(
            range=[-0.5, 6.5],
            showgrid=False,
            showticklabels=False,
            zeroline=False
        ),
        yaxis=dict(
            range=[-1.5, len(timeline_data) + 1],
            showgrid=False,
            showticklabels=False,
            zeroline=False
        ),
        plot_bgcolor='white',
        paper_bgcolor='white',
        height=600,
        margin=dict(l=50, r=50, t=120, b=80),
        hovermode='closest'
    )
    
    return fig


def create_compact_timeline():
    """
    Create a more compact horizontal timeline version
    """
    
    timeline_data = [
        {"month": "1-2", "title": "Core Architecture", "color": "#4A3D6F"},
        {"month": "2-3", "title": "Dashboard Dev", "color": "#6F5F96"},
        {"month": "3-4", "title": "ML Models", "color": "#8B7BA8"},
        {"month": "4-5", "title": "AI Engineering", "color": "#A896C0"},
        {"month": "5-6", "title": "Production", "color": "#C5B3D8"}
    ]
    
    fig = go.Figure()
    
    # Create horizontal bars
    for i, phase in enumerate(timeline_data):
        y_pos = len(timeline_data) - i - 1
        
        # Timeline bar
        fig.add_trace(go.Bar(
            x=[1],  # Width of 1 month
            y=[phase["title"]],
            base=i,
            orientation='h',
            marker=dict(color=phase["color"]),
            name=phase["month"],
            showlegend=False,
            hovertemplate=f"<b>Month {phase['month']}</b><br>{phase['title']}<extra></extra>"
        ))
        
        # Month label
        fig.add_annotation(
            x=0.5,
            y=i + 0.5,
            text=f"<b>{phase['month']}</b>",
            showarrow=False,
            font=dict(size=12, color="#FFFFFF", family="Arial Black"),
            xref="x",
            yref="y"
        )
    
    # Add connecting line
    fig.add_trace(go.Scatter(
        x=[0, 0],
        y=[-0.5, len(timeline_data) - 0.5],
        mode='lines',
        line=dict(color="#4ade80", width=4),
        showlegend=False,
        hoverinfo='skip'
    ))
    
    fig.update_layout(
        title={
            'text': '<b>6 Months Development • 22 Years Experience</b>',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20, 'color': '#4A3D6F'}
        },
        xaxis=dict(
            range=[0, 1],
            showgrid=False,
            showticklabels=False,
            zeroline=False
        ),
        yaxis=dict(
            showgrid=False,
            showticklabels=True,
            tickmode='array',
            tickvals=list(range(len(timeline_data))),
            ticktext=[phase["title"] for phase in timeline_data],
            zeroline=False
        ),
        plot_bgcolor='white',
        paper_bgcolor='white',
        height=400,
        margin=dict(l=150, r=50, t=80, b=50)
    )
    
    return fig


def render_timeline_infographic():
    """
    Render the timeline infographic in Streamlit
    """
    st.markdown("""
    <style>
    .timeline-container {
        background: linear-gradient(135deg, #f0f4f8 0%, #ffffff 100%);
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(74, 61, 111, 0.15);
        margin: 1rem 0;
    }
    
    .timeline-header {
        text-align: center;
        color: #4A3D6F;
        margin-bottom: 2rem;
    }
    
    .timeline-header h2 {
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .timeline-header p {
        font-size: 1.1rem;
        color: #666666;
    }
    
    .experience-note {
        background: linear-gradient(135deg, #E8F5E9 0%, #C8E6C9 100%);
        border-left: 4px solid #4ade80;
        padding: 1.5rem;
        border-radius: 8px;
        margin: 2rem 0;
        text-align: center;
    }
    
    .experience-note h3 {
        color: #2E7D32;
        font-size: 1.3rem;
        margin-bottom: 0.5rem;
    }
    
    .experience-note p {
        color: #1B5E20;
        font-size: 1rem;
        line-height: 1.6;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="timeline-container">
        <div class="timeline-header">
            <h2>⏱️ How Long Did It Take to Build StarGuard AI?</h2>
            <p>6 Months of Evenings & Weekends</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Create and display timeline
    fig = create_timeline_infographic()
    st.plotly_chart(fig, use_container_width=True)
    
    # Experience note
    st.markdown("""
    <div class="experience-note">
        <h3>💡 But Here's What That Time Really Represents</h3>
        <p>
            <b>22 years of healthcare data experience</b> condensed into a portfolio showing my thinking, not just my coding.<br><br>
            The architecture decisions—why PostgreSQL, why Streamlit, why local LLM processing—reflect lessons from building systems at scale.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Key highlights
    st.markdown("### 🎯 Key Development Phases")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Month 1-2: Core Data Architecture**
        - PostgreSQL schema design
        - Synthetic HEDIS data generation
        - Data modeling & relationships
        
        **Month 2-3: Dashboard Development**
        - Streamlit multi-page app
        - Plotly visualizations
        - Responsive UI design
        """)
    
    with col2:
        st.markdown("""
        **Month 3-4: Predictive Models**
        - Gap closure predictions
        - ROI modeling
        - Scenario analysis
        
        **Month 4-5: AI Context Engineering**
        - Local LLM processing
        - Agentic RAG implementation
        - Secure AI chatbot
        """)
    
    st.markdown("""
    **Month 5-6: Production Hardening**
    - Mobile optimization
    - Performance tuning
    - Security hardening
    - Deployment preparation
    """)
    
    # Architecture decisions
    st.markdown("---")
    st.markdown("### 🏗️ Architecture Decisions Reflect Experience")
    
    arch_cols = st.columns(3)
    
    with arch_cols[0]:
        st.markdown("""
        **PostgreSQL**
        - Proven reliability at scale
        - Complex query optimization
        - Healthcare data compliance
        """)
    
    with arch_cols[1]:
        st.markdown("""
        **Streamlit**
        - Rapid prototyping
        - Python-native stack
        - Easy deployment
        """)
    
    with arch_cols[2]:
        st.markdown("""
        **Local LLM Processing**
        - Zero PHI exposure
        - HIPAA compliance
        - On-premises security
        """)
    
    # Hashtags
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666666; font-size: 0.9rem;">
        #BuildProcess #Portfolio #HealthcareAnalytics #Development #DataScience
    </div>
    """, unsafe_allow_html=True)
