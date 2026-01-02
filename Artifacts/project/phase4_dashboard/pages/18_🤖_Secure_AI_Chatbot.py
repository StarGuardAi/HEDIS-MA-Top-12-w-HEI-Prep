"""
Secure Healthcare Data Chatbot - Zero External API Exposure
Demonstrates on-premises AI processing with zero PHI transmission
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import sys
import os

# Page config MUST be first Streamlit command
st.set_page_config(
    page_title="Secure AI Chatbot",
    page_icon="🤖",
    layout="wide"
)

# Rename "app" to "Home" in sidebar navigation
st.markdown("""
<style>
/* Method 1: Replace text content with CSS */
[data-testid="stSidebarNav"] ul li:first-child a {
    font-size: 0 !important;  /* Hide original "app" text */
    background: linear-gradient(135deg, rgba(139,122,184,0.3), rgba(111,95,150,0.3)) !important;
    padding: 0.75rem 1rem !important;
    border-radius: 8px !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
    margin-bottom: 0.5rem !important;
}

[data-testid="stSidebarNav"] ul li:first-child a::before {
    content: "🏠 Home";  /* Replace with "Home" */
    font-size: 1.1rem !important;
    color: white !important;
    font-weight: 700 !important;
}

[data-testid="stSidebarNav"] ul li:first-child a:hover {
    background: linear-gradient(135deg, rgba(139,122,184,0.5), rgba(111,95,150,0.5)) !important;
}

/* Method 2: Also target by href */
[data-testid="stSidebarNav"] a[href="/"],
[data-testid="stSidebarNav"] a[href="./"] {
    font-size: 0 !important;
    background: linear-gradient(135deg, rgba(139,122,184,0.3), rgba(111,95,150,0.3)) !important;
    padding: 0.75rem 1rem !important;
    border-radius: 8px !important;
}

[data-testid="stSidebarNav"] a[href="/"]::before,
[data-testid="stSidebarNav"] a[href="./"]::before {
    content: "🏠 Home";
    font-size: 1.1rem !important;
    color: white !important;
    font-weight: 700 !important;
}

/* ========== PURPLE SIDEBAR THEME (Match Home Page) ========== */
/* Match the StarGuard AI header purple gradient */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #4A3D6F 0%, #6F5F96 100%) !important;
}

[data-testid="stSidebar"] > div:first-child {
    background: linear-gradient(180deg, #4A3D6F 0%, #6F5F96 100%) !important;
}

/* ========== ALL SIDEBAR TEXT WHITE ========== */
/* Force ALL text in sidebar to be white */
[data-testid="stSidebar"] * {
    color: #FFFFFF !important;
}

[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] div,
[data-testid="stSidebar"] a,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] button {
    color: #FFFFFF !important;
}

/* ========== WHITE "HOME" LABEL ========== */
[data-testid="stSidebarNav"] ul li:first-child a {
    font-size: 0 !important;
    background: rgba(255, 255, 255, 0.2) !important;
    padding: 0.75rem 1rem !important;
    border-radius: 8px !important;
    border: 2px solid rgba(255, 255, 255, 0.3) !important;
    margin-bottom: 0.5rem !important;
}

[data-testid="stSidebarNav"] ul li:first-child a::before {
    content: "🏠 Home" !important;
    font-size: 1.1rem !important;
    color: #FFFFFF !important;
    font-weight: 700 !important;
    display: block !important;
    -webkit-text-fill-color: #FFFFFF !important;
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3) !important;
}

/* All sidebar navigation links white */
[data-testid="stSidebarNav"] a {
    color: #FFFFFF !important;
}

[data-testid="stSidebarNav"] a span,
[data-testid="stSidebarNav"] a div,
[data-testid="stSidebarNav"] a p {
    color: #FFFFFF !important;
}

/* "Mobile Optimized" badge - white text */
[data-testid="stSidebar"] .element-container div[data-testid="stMarkdownContainer"] p {
    color: #FFFFFF !important;
}

/* Success/Info boxes in sidebar - white text */
[data-testid="stSidebar"] [data-testid="stSuccess"],
[data-testid="stSidebar"] [data-testid="stInfo"] {
    color: #FFFFFF !important;
    background: rgba(255, 255, 255, 0.15) !important;
    border-color: rgba(255, 255, 255, 0.3) !important;
}

[data-testid="stSidebar"] [data-testid="stSuccess"] *,
[data-testid="stSidebar"] [data-testid="stInfo"] * {
    color: #FFFFFF !important;
}

/* View less/more links - white */
[data-testid="stSidebar"] button {
    color: #FFFFFF !important;
}

/* Mobile responsive */
@media (max-width: 768px) {
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #4A3D6F 0%, #6F5F96 100%) !important;
    }
    
    [data-testid="stSidebar"] * {
        color: #FFFFFF !important;
    }
}

/* ========== HEADER CONTAINER STYLES (Match Home Page) ========== */
.header-container {
    background: linear-gradient(180deg, #4A3D6F 0%, #6F5F96 100%);
    padding: 0.5rem 1rem;
    border-radius: 10px;
    margin-top: 1.5rem;
    margin-bottom: 0.3rem;
    text-align: center;
    display: block !important;
    visibility: visible !important;
    opacity: 1 !important;
    box-shadow: 0 4px 12px rgba(74, 61, 111, 0.25);
    max-width: 100%;
}

.header-title {
    color: white !important;
    font-weight: 700;
    font-size: 1.25rem;
    margin-bottom: 0.4rem;
    display: block !important;
    line-height: 1.5;
    letter-spacing: 0.3px;
}

.header-subtitle {
    color: #E8D4FF !important;
    font-size: 0.9rem;
    font-style: italic;
    display: block !important;
    line-height: 1.4;
    opacity: 0.95;
}
</style>
""", unsafe_allow_html=True)


# Responsive Header - Adapts to Desktop/Mobile (Match Home Page)
st.markdown("""
<div class="header-container">
    <div class="header-title">⭐ StarGuard AI | Turning Data Into Stars</div>
    <div class="header-subtitle">Powered by Predictive Analytics & Machine Learning</div>
</div>
""", unsafe_allow_html=True)

# Spacing fix
st.markdown('<style>div.block-container{padding-top:1rem!important}h1{margin-top:0.5rem!important}</style>', unsafe_allow_html=True)

# Improved compact CSS - READABLE fonts, reduced spacing only
st.markdown("""
<style>
.main .block-container { 
    padding-top: 1rem !important; 
    padding-bottom: 1rem !important; 
    padding-left: 1rem !important; 
    padding-right: 1rem !important; 
    max-width: 100% !important; 
}

/* Section spacing - REDUCE GAPS between sections */
h1 { 
    font-size: 1.8rem !important; 
    margin-top: 0.8rem !important; 
    margin-bottom: 0.5rem !important; 
    line-height: 1.2 !important; 
}

h2 { 
    font-size: 1.4rem !important; 
    margin-top: 0.6rem !important; 
    margin-bottom: 0.4rem !important; 
    line-height: 1.2 !important; 
}

h3 { 
    font-size: 1.1rem !important; 
    margin-top: 0.5rem !important; 
    margin-bottom: 0.3rem !important; 
    line-height: 1.2 !important; 
}

/* Reduce spacing between elements */
.element-container { margin-bottom: 0.4rem !important; }
.stMarkdown { margin-bottom: 0.4rem !important; }

/* Readable metric fonts */
[data-testid="stMetricValue"] { font-size: 1.6rem !important; }
[data-testid="stMetricLabel"] { font-size: 0.95rem !important; padding-bottom: 0.3rem !important; }
[data-testid="metric-container"] { padding: 0.7rem !important; }

/* Chart and data spacing */
.stPlotlyChart { margin-bottom: 0.6rem !important; }
.stDataFrame { margin-bottom: 0.6rem !important; }

/* Column spacing */
[data-testid="column"] { padding: 0.3rem !important; }

/* Interactive elements */
[data-testid="stExpander"] { margin-bottom: 0.5rem !important; }
[data-testid="stTabs"] { margin-bottom: 0.6rem !important; }
.stTabs [data-baseweb="tab-list"] { gap: 0.3rem !important; }
.stTabs [data-baseweb="tab"] { 
    padding: 0.5rem 1rem !important; 
    font-size: 0.95rem !important; 
}

/* Buttons - keep readable */
.stButton > button { 
    padding: 0.6rem 1.2rem !important; 
    font-size: 0.95rem !important; 
}

/* Form inputs */
.stSelectbox, .stTextInput, .stNumberInput { margin-bottom: 0.4rem !important; }

/* Alerts - keep readable */
.stAlert { 
    padding: 0.7rem !important; 
    margin-bottom: 0.5rem !important; 
    font-size: 0.95rem !important; 
}

/* Reduce gaps between blocks */
div[data-testid="stVerticalBlock"] > div { gap: 0.4rem !important; }

/* Horizontal rules */
hr { margin: 0.6rem 0 !important; }

/* Mobile adjustments - Match Home page formatting */
@media (max-width: 768px) {
    .header-container {
        padding: 0.6rem 0.8rem;
        border-radius: 6px;
        margin-top: 1rem;
        margin-bottom: 0.5rem;
        box-shadow: 0 2px 4px rgba(74, 61, 111, 0.15);
    }
    
    .header-title {
        font-size: 0.9rem;
        margin-bottom: 0.25rem;
        line-height: 1.3;
        font-weight: 600;
    }
    
    .header-subtitle {
        font-size: 0.65rem;
        line-height: 1.2;
    }
    
    /* Mobile spacing - tighter */
    div.block-container {
        padding-top: 2rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }
    
    h1 {
        margin-top: 0.5rem !important;
        font-size: 1.5rem !important;
        line-height: 1.3;
        text-align: center !important;
    }
    
    h2 {
        margin-top: 0.75rem !important;
        font-size: 1.25rem !important;
        line-height: 1.3;
        text-align: center !important;
    }
    
    h3 {
        font-size: 1.1rem !important;
        line-height: 1.3;
        text-align: center !important;
    }
    
    h4, h5, h6 {
        text-align: center !important;
    }
    
    /* Center align markdown headers on mobile */
    div[data-testid="stMarkdownContainer"] h1,
    div[data-testid="stMarkdownContainer"] h2,
    div[data-testid="stMarkdownContainer"] h3,
    div[data-testid="stMarkdownContainer"] h4,
    div[data-testid="stMarkdownContainer"] h5,
    div[data-testid="stMarkdownContainer"] h6 {
        text-align: center !important;
    }
    
    /* Center align metrics on mobile */
    [data-testid="stMetric"],
    [data-testid="stMetricValue"],
    [data-testid="stMetricLabel"],
    [data-testid="stMetricDelta"],
    [data-testid="metric-container"],
    .compact-metric-card,
    .kpi-card {
        text-align: center !important;
    }
    
    /* Mobile columns - stack vertically */
    [data-testid="column"] {
        width: 100% !important;
        flex: 1 1 100% !important;
        padding: 0.2rem !important;
    }
    
    /* Mobile buttons - full width */
    button[kind="primary"],
    button[kind="secondary"] {
        width: 100% !important;
        margin-bottom: 0.5rem !important;
    }
    
    /* Mobile metrics - smaller */
    [data-testid="stMetricValue"] {
        font-size: 1.5rem !important;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 0.85rem !important;
    }
    
    /* Mobile tables - horizontal scroll */
    .stDataFrame {
        overflow-x: auto !important;
    }
    
    /* Mobile tabs - stack vertically to eliminate horizontal scrolling */
    [data-testid="stTabs"] {
        overflow-x: visible !important;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        flex-direction: column !important;
        width: 100% !important;
        gap: 0.5rem !important;
        overflow-x: visible !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        width: 100% !important;
        flex: 1 1 100% !important;
    }
    
    /* Wrap Plotly chart titles on mobile */
    .js-plotly-plot .gtitle,
    .plotly .gtitle,
    .js-plotly-plot .xtitle,
    .plotly .xtitle {
        word-wrap: break-word !important;
        white-space: normal !important;
        max-width: 100% !important;
        overflow-wrap: break-word !important;
        hyphens: auto !important;
    }
    
    /* Ensure chart titles wrap - target SVG text elements */
    .js-plotly-plot .gtitle text,
    .plotly .gtitle text {
        word-wrap: break-word !important;
        white-space: normal !important;
    }
}
</style>
""", unsafe_allow_html=True)

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Try to import secure chatbot service
try:
    from src.services.secure_chatbot_service import SecureChatbotService
    HAS_SERVICE = True
except ImportError:
    HAS_SERVICE = False

# Import footer functions
from src.ui.layout import render_page_footer, render_sidebar_footer, render_header

# Page header (already rendered above)

# Sidebar value proposition - at bottom
from utils.value_proposition import render_sidebar_value_proposition
render_sidebar_value_proposition()

# Sidebar footer
render_sidebar_footer()

st.title("🤖 Secure Healthcare Data Chatbot")
st.markdown("### Zero External API Exposure | On-Premises Processing")

# Demo mode banner (if service not available)
if not HAS_SERVICE:
    st.info("""
    🎯 **Demo Mode Active**: The secure chatbot service is not available. This page demonstrates the interface and capabilities using pattern-matching responses. 
    In production, this would use local LLM (Ollama) and ChromaDB for secure, on-premises processing with zero external API exposure.
    """)

# Security badge - Prominent display
st.markdown("""
<div style="background-color: #e8f5e9; padding: 20px; border-radius: 8px; border-left: 6px solid #2d7d32; margin-bottom: 20px; text-align: center;">
    <h2 style="color: #2d7d32; margin: 0; font-size: 1.8rem;">🔒 ZERO PHI TRANSMITTED TO EXTERNAL APIS</h2>
    <p style="margin: 10px 0 0 0; color: #1b5e20; font-size: 1.1rem;">All processing occurs on-premises using local models (Ollama/ChromaDB)</p>
</div>
""", unsafe_allow_html=True)

# Enhanced Data Flow Architecture Diagram
st.markdown("---")
st.markdown("### 📊 Data Flow Architecture: User → Local Model → Internal DB")

# Create interactive data flow diagram using Plotly
fig_flow = go.Figure()

# Define flow steps
flow_steps = [
    {"name": "User Question", "x": 0, "y": 0, "color": "#4CAF50"},
    {"name": "Local Embedding\n(Ollama)", "x": 1, "y": 0, "color": "#2196F3"},
    {"name": "Vector Search\n(ChromaDB)", "x": 2, "y": 0, "color": "#FF9800"},
    {"name": "SQL Generation\n(Local LLM)", "x": 3, "y": 0, "color": "#9C27B0"},
    {"name": "Database Query\n(Internal)", "x": 4, "y": 0, "color": "#F44336"},
    {"name": "Response\n(De-identified)", "x": 5, "y": 0, "color": "#00BCD4"}
]

# Add nodes
for step in flow_steps:
    fig_flow.add_trace(go.Scatter(
        x=[step["x"]],
        y=[step["y"]],
        mode='markers+text',
        marker=dict(
            size=80,
            color=step["color"],
            line=dict(width=2, color='white')
        ),
        text=[step["name"]],
        textposition="middle center",
        textfont=dict(size=10, color='white', family='Arial Black'),
        name=step["name"],
        showlegend=False,
        hovertemplate=f"<b>{step['name']}</b><extra></extra>"
    ))

# Add arrows (connections)
for i in range(len(flow_steps) - 1):
    fig_flow.add_annotation(
        x=flow_steps[i+1]["x"],
        y=flow_steps[i+1]["y"],
        ax=flow_steps[i]["x"],
        ay=flow_steps[i]["y"],
        xref="x",
        yref="y",
        axref="x",
        ayref="y",
        showarrow=True,
        arrowhead=2,
        arrowsize=1.5,
        arrowwidth=2,
        arrowcolor="#666"
    )

# Update layout
fig_flow.update_layout(
    title=dict(
        text="<b>Secure Data Flow: Zero External API Calls</b>",
        x=0.5,
        font=dict(size=16, color="#2d7d32")
    ),
    xaxis=dict(showgrid=False, showticklabels=False, range=[-0.5, 5.5]),
    yaxis=dict(showgrid=False, showticklabels=False, range=[-0.5, 0.5]),
    height=200,
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=20, r=20, t=60, b=20)
)

st.plotly_chart(fig_flow, use_container_width=True)

# Security architecture details
with st.expander("🔐 Detailed Security Architecture", expanded=False):
    st.markdown("""
    ```
    ┌─────────────────────────────────────────────────────────────┐
    │                    SECURE NETWORK                            │
    │                                                              │
    │  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
    │  │   User       │───▶│  Streamlit   │───▶│   Ollama     │  │
    │  │  Interface   │    │   App        │    │  (Local LLM)  │  │
    │  └──────────────┘    └──────┬───────┘    └──────────────┘  │
    │                              │                              │
    │                              ▼                              │
    │                    ┌──────────────┐                         │
    │                    │  ChromaDB    │                         │
    │                    │ (Vector DB)   │                         │
    │                    └──────┬───────┘                         │
    │                           │                                  │
    │                           ▼                                  │
    │                    ┌──────────────┐                         │
    │                    │   Database   │                         │
    │                    │ (Encrypted)  │                         │
    │                    └──────────────┘                         │
    │                                                              │
    │  ⚠️  ZERO EXTERNAL API CALLS                                 │
    │  🔒  ALL PROCESSING ON-PREMISES                             │
    │  🛡️  FULL DATA CONTROL                                      │
    └─────────────────────────────────────────────────────────────┘
    ```
    """)

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'local_processing' not in st.session_state:
    st.session_state.local_processing = True
if 'chatbot_service' not in st.session_state and HAS_SERVICE:
    try:
        st.session_state.chatbot_service = SecureChatbotService()
    except Exception as e:
        st.warning(f"Could not initialize chatbot service: {e}")
        st.session_state.chatbot_service = None

# Sidebar with info
with st.sidebar:
    st.markdown("### 🔐 Security Features")
    st.markdown("""
    - ✅ **Local LLM**: Ollama (on-premises)
    - ✅ **Local Vector Store**: ChromaDB
    - ✅ **Encrypted Database**: AES-256
    - ✅ **Access Logging**: All queries logged
    - ✅ **De-identification**: Automatic PHI removal
    - ✅ **Audit Trail**: Complete interaction logs
    """)
    
    st.markdown("---")
    st.markdown("### 📋 Sample Questions")
    sample_questions = [
        "Which measures have declining trends?",
        "What's the ROI for HbA1c testing?",
        "Show me measures with low compliance rates",
        "Which interventions are most cost-effective?",
        "What are the top 3 measures by financial impact?"
    ]
    
    for i, question in enumerate(sample_questions):
        if st.button(question, key=f"sample_{i}", use_container_width=True):
            st.session_state.current_question = question
            st.rerun()
    
    st.markdown("---")
    st.markdown("### 🔍 Processing Status")
    if HAS_SERVICE and st.session_state.get('chatbot_service'):
        st.success("✅ Secure chatbot service active")
        if hasattr(st.session_state.chatbot_service, 'embedding_model'):
            if st.session_state.chatbot_service.embedding_model:
                st.info("✅ Local embeddings available")
            else:
                st.warning("⚠️ Using fallback embeddings")
        if st.session_state.chatbot_service.vector_store:
            st.info("✅ ChromaDB vector store active")
        else:
            st.warning("⚠️ Using keyword search fallback")
    else:
        st.info("🎯 **Demo Mode**")
        st.caption("Using pattern-matching responses for demonstration. In production, this would use local LLM processing.")

# Main chat interface
st.markdown("---")
st.markdown("### 💬 Ask a Question About Your HEDIS Data")

# Get portfolio data for demonstration
if 'portfolio_data' in st.session_state:
    portfolio_data = st.session_state.portfolio_data.copy()
else:
    # Generate sample data for demo
    import numpy as np
    measures = [
        "HbA1c Testing (CDC)", "Blood Pressure Control (CBP)",
        "Colorectal Cancer Screening (COL)", "Breast Cancer Screening (BCS)",
        "Diabetes Eye Exam (EED)", "Statin Therapy for CVD (SPC)"
    ]
    portfolio_data = pd.DataFrame({
        'measure_name': measures * 2,
        'roi_ratio': np.random.uniform(1.2, 1.8, 12),
        'compliance_rate': np.random.uniform(35, 75, 12),
        'financial_impact': np.random.uniform(50000, 200000, 12),
        'trend': np.random.uniform(-3, 3, 12)
    })

# Chat input
user_question = st.text_input(
    "Ask a question:",
    value=st.session_state.get('current_question', ''),
    key="chat_input",
    placeholder="e.g., Which measures have declining trends?"
)

if st.button("🔍 Ask", type="primary") or (user_question and user_question != st.session_state.get('last_question', '')):
    if user_question:
        st.session_state.last_question = user_question
        
        # Use secure chatbot service if available
        if HAS_SERVICE and st.session_state.get('chatbot_service'):
            with st.spinner("🔄 Processing locally (no external API calls)..."):
                try:
                    result = st.session_state.chatbot_service.process_query(
                        user_question,
                        portfolio_data
                    )
                    
                    # Add to chat history
                    st.session_state.chat_history.append({
                        'role': 'user',
                        'content': user_question
                    })
                    st.session_state.chat_history.append({
                        'role': 'assistant',
                        'content': result['response'],
                        'processing_steps': result['processing_steps'],
                        'context_measures': result.get('context_measures', []),
                        'sql_query': result.get('sql_query', '')
                    })
                except Exception as e:
                    st.error(f"Error processing query: {e}")
                    # Fallback to simple response
                    st.session_state.chat_history.append({
                        'role': 'user',
                        'content': user_question
                    })
                    st.session_state.chat_history.append({
                        'role': 'assistant',
                        'content': "I encountered an error processing your query. Please try again."
                    })
        else:
            # Fallback to pattern matching
            with st.spinner("🔄 Processing locally (no external API calls)..."):
                st.session_state.chat_history.append({
                    'role': 'user',
                    'content': user_question
                })
                
                # Simple pattern matching for demo
                question_lower = user_question.lower()
                
                if 'declining' in question_lower or 'trend' in question_lower:
                    declining = portfolio_data[portfolio_data['trend'] < 0].copy()
                    if len(declining) > 0:
                        response = f"**Measures with declining trends:**\n\n"
                        for _, row in declining.head(5).iterrows():
                            response += f"- **{row['measure_name']}**: {row['trend']:.1f}% trend\n"
                        response += f"\n*Found {len(declining)} measures with declining trends.*"
                    else:
                        response = "No measures currently show declining trends."
                elif 'roi' in question_lower:
                    if 'hba1c' in question_lower or 'cdc' in question_lower:
                        hba1c = portfolio_data[portfolio_data['measure_name'].str.contains('HbA1c|CDC', case=False, na=False)]
                        if len(hba1c) > 0:
                            avg_roi = hba1c['roi_ratio'].mean()
                            avg_impact = hba1c['financial_impact'].mean()
                            response = f"""**HbA1c Testing ROI Analysis:**

- **Average ROI Ratio**: {avg_roi:.2f}x
- **Average Financial Impact**: ${avg_impact:,.0f}
- **Net Benefit**: ${avg_impact * (avg_roi - 1):,.0f}

*This measure shows strong return on investment.*"""
                        else:
                            response = "HbA1c Testing data not found in current dataset."
                    else:
                        top_roi = portfolio_data.nlargest(3, 'roi_ratio')
                        response = "**Top 3 Measures by ROI:**\n\n"
                        for _, row in top_roi.iterrows():
                            response += f"- **{row['measure_name']}**: {row['roi_ratio']:.2f}x ROI\n"
                elif 'compliance' in question_lower or 'low' in question_lower:
                    low_compliance = portfolio_data[portfolio_data['compliance_rate'] < 50].copy()
                    if len(low_compliance) > 0:
                        response = "**Measures with Low Compliance Rates (<50%):**\n\n"
                        for _, row in low_compliance.head(5).iterrows():
                            response += f"- **{row['measure_name']}**: {row['compliance_rate']:.1f}% compliance\n"
                        response += f"\n*Found {len(low_compliance)} measures needing attention.*"
                    else:
                        response = "All measures show compliance rates above 50%."
                elif 'cost' in question_lower or 'effective' in question_lower:
                    top_impact = portfolio_data.nlargest(3, 'financial_impact')
                    response = "**Top 3 Most Cost-Effective Measures:**\n\n"
                    for _, row in top_impact.iterrows():
                        response += f"- **{row['measure_name']}**: ${row['financial_impact']:,.0f} impact, {row['roi_ratio']:.2f}x ROI\n"
                else:
                    response = """I can help you analyze your HEDIS data. Here are some example questions:

- **Trends**: "Which measures have declining trends?"
- **ROI**: "What's the ROI for HbA1c testing?" or "Show me top measures by ROI"
- **Compliance**: "Show me measures with low compliance rates"
- **Cost-effectiveness**: "Which interventions are most cost-effective?"

*Note: This is demo mode using pattern matching. In production, this would use advanced local LLM processing.*"""
                
                st.session_state.chat_history.append({
                    'role': 'assistant',
                    'content': response
                })
        
        # Clear the input
        if 'current_question' in st.session_state:
            del st.session_state.current_question

# Display chat history with processing details
st.markdown("---")
st.markdown("### 💬 Conversation History")

if st.session_state.chat_history:
    for i, message in enumerate(st.session_state.chat_history):
        if message['role'] == 'user':
            with st.chat_message("user"):
                st.write(message['content'])
        else:
            with st.chat_message("assistant"):
                st.markdown(message['content'])
                
                # Show processing steps if available
                if 'processing_steps' in message and message['processing_steps']:
                    with st.expander("🔍 View Processing Steps", expanded=False):
                        for step in message['processing_steps']:
                            st.markdown(f"**{step['step']}**")
                            st.markdown(f"Status: {step['status']}")
                            st.markdown(f"Details: {step['details']}")
                            st.markdown("---")
                
                # Show SQL query if available
                if 'sql_query' in message and message['sql_query']:
                    with st.expander("📝 Generated SQL Query", expanded=False):
                        st.code(message['sql_query'], language='sql')
else:
    st.info("👆 Ask a question above to start a conversation. All processing happens locally with zero external API calls.")

# Comparison table
st.markdown("---")
st.markdown("### 📊 Comparison: Traditional Cloud AI vs Secure On-Premises Approach")

comparison_df = pd.DataFrame({
    'Aspect': [
        'Data Location',
        'PHI Transmission',
        'Compliance Risk',
        'Latency',
        'Cost Model',
        'Scalability',
        'Data Control',
        'Audit Capability',
        'Customization',
        'Offline Capability',
        'Security Model',
        'Breach Impact',
        'Regulatory Approval'
    ],
    'Traditional Cloud AI': [
        'External cloud servers',
        'Data sent to external APIs',
        'High (data leaves organization)',
        'Network-dependent',
        'Per-API-call pricing',
        'Auto-scaling cloud',
        'Limited (vendor-dependent)',
        'Vendor logs only',
        'Limited by vendor API',
        'Requires internet',
        'Shared responsibility',
        'Vendor breach affects you',
        'May require BAA'
    ],
    'Secure On-Premises': [
        'On-premises infrastructure',
        'Zero external transmission',
        'Low (data stays internal)',
        'Low (local processing)',
        'Fixed infrastructure cost',
        'Controlled scaling',
        'Full control',
        'Complete internal logs',
        'Full customization',
        'Works offline',
        'Full responsibility',
        'Isolated to your network',
        'Internal approval only'
    ]
})

st.dataframe(comparison_df, use_container_width=True, hide_index=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 20px; background-color: #f5f5f5; border-radius: 8px;">
    <h3 style="color: #2d7d32;">🔒 Zero PHI Exposure | 🛡️ Full Data Control | ✅ HIPAA Compliant</h3>
    <p>This demonstration shows how AI-powered analytics can be deployed securely in healthcare environments.</p>
    <p><strong>Technology Stack:</strong> Ollama (Local LLM) | ChromaDB (Local Vector Store) | Streamlit (Interface)</p>
</div>
""", unsafe_allow_html=True)

# Footer sections - desktop full text, mobile abbreviated
render_page_footer()  # Main content footer
