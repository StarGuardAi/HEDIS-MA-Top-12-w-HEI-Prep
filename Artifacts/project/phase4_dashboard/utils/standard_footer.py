"""
Standard Footer Template
Provides consistent footer formatting across all pages with purple gradient box design and rainbow border
"""

STANDARD_FOOTER_HTML = """
# ============================================================================
# FOOTER - Purple Gradient Box Design with Rainbow Border
# ============================================================================
st.markdown("---")
st.markdown(\"\"\"
<div style="
    background: linear-gradient(135deg, #4A3D6F 0%, #6F5F96 100%);
    border-radius: 12px;
    padding: 2rem 1.5rem;
    padding-top: 2.5rem;
    margin: 2rem 0 1rem 0;
    box-shadow: 0 4px 12px rgba(74, 61, 111, 0.25);
    text-align: center;
    position: relative;
    overflow: hidden;
">
    <!-- Rainbow top border using gradient -->
    <div style="
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 6px;
        background: linear-gradient(90deg, #ff0000, #ff7f00, #ffff00, #00ff00, #0000ff, #4b0082, #9400d3);
        border-radius: 12px 12px 0 0;
        z-index: 1;
    "></div>
    
    <!-- Top Hashtags -->
    <div style="
        margin: 0.5rem 0 1.5rem 0;
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 0.5rem;
        position: relative;
        z-index: 2;
    ">
        <span style="
            background: rgba(255, 255, 255, 0.2);
            color: white;
            padding: 0.3rem 0.8rem;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 500;
        ">#HealthcareAnalytics</span>
        <span style="
            background: rgba(255, 255, 255, 0.2);
            color: white;
            padding: 0.3rem 0.8rem;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 500;
        ">#MedicareAdvantage</span>
        <span style="
            background: rgba(255, 255, 255, 0.2);
            color: white;
            padding: 0.3rem 0.8rem;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 500;
        ">#HEDIS</span>
        <span style="
            background: rgba(255, 255, 255, 0.2);
            color: white;
            padding: 0.3rem 0.8rem;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 500;
        ">#DataScience</span>
    </div>
    
    <!-- Title -->
    <h2 style="
        color: white;
        font-size: 1.8rem;
        font-weight: 700;
        margin: 0 0 0.5rem 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        position: relative;
        z-index: 2;
    ">
        ⭐ HEDIS Portfolio Optimizer | StarGuard AI
    </h2>
    
    <!-- Subtitle -->
    <p style="
        color: rgba(255, 255, 255, 0.95);
        font-size: 1.1rem;
        margin: 0 0 1.5rem 0;
        font-weight: 500;
        position: relative;
        z-index: 2;
    ">
        Turning Data Into Stars
    </p>
    
    <!-- Technology Badges -->
    <div style="
        margin: 1rem 0 1.5rem 0;
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 0.5rem;
        position: relative;
        z-index: 2;
    ">
        <span style="
            background: rgba(255, 255, 255, 0.25);
            color: white;
            padding: 0.4rem 0.9rem;
            border-radius: 20px;
            font-size: 0.9rem;
            font-weight: 600;
            border: 1px solid rgba(255, 255, 255, 0.3);
        ">🐍 Python</span>
        <span style="
            background: rgba(255, 255, 255, 0.25);
            color: white;
            padding: 0.4rem 0.9rem;
            border-radius: 20px;
            font-size: 0.9rem;
            font-weight: 600;
            border: 1px solid rgba(255, 255, 255, 0.3);
        ">📊 Streamlit</span>
        <span style="
            background: rgba(255, 255, 255, 0.25);
            color: white;
            padding: 0.4rem 0.9rem;
            border-radius: 20px;
            font-size: 0.9rem;
            font-weight: 600;
            border: 1px solid rgba(255, 255, 255, 0.3);
        ">📈 Plotly</span>
        <span style="
            background: rgba(255, 255, 255, 0.25);
            color: white;
            padding: 0.4rem 0.9rem;
            border-radius: 20px;
            font-size: 0.9rem;
            font-weight: 600;
            border: 1px solid rgba(255, 255, 255, 0.3);
        ">🐘 PostgreSQL</span>
        <span style="
            background: rgba(255, 255, 255, 0.25);
            color: white;
            padding: 0.4rem 0.9rem;
            border-radius: 20px;
            font-size: 0.9rem;
            font-weight: 600;
            border: 1px solid rgba(255, 255, 255, 0.3);
        ">🤖 ML/AI</span>
    </div>
    
    <!-- Green Secure AI Architecture Box -->
    <div style="
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.2) 0%, rgba(5, 150, 105, 0.25) 100%);
        border: 3px solid #10b981;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1.5rem auto;
        max-width: 850px;
        text-align: center;
        box-shadow: 0 4px 8px rgba(16, 185, 129, 0.2);
        position: relative;
        z-index: 2;
    ">
        <p style="
            color: white;
            font-size: 1.1rem;
            font-weight: 700;
            margin: 0 0 1rem 0;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
        ">
            🔒 Secure AI Architecture
        </p>
        <p style="
            color: rgba(255, 255, 255, 0.95);
            font-size: 0.95rem;
            line-height: 1.6;
            margin: 0 0 1.25rem 0;
        ">
            Healthcare AI that sees everything, exposes nothing.
        </p>
        
        <!-- Metrics Grid -->
        <div style="
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 1rem;
            margin: 1rem 0;
        ">
            <div style="
                background: rgba(255, 255, 255, 0.15);
                padding: 0.75rem;
                border-radius: 8px;
                border: 1px solid rgba(255, 255, 255, 0.2);
            ">
                <p style="
                    color: white;
                    font-size: 1.1rem;
                    font-weight: 700;
                    margin: 0 0 0.25rem 0;
                ">2.8-4.1x</p>
                <p style="
                    color: rgba(255, 255, 255, 0.9);
                    font-size: 0.8rem;
                    margin: 0;
                ">ROI Delivered</p>
            </div>
            <div style="
                background: rgba(255, 255, 255, 0.15);
                padding: 0.75rem;
                border-radius: 8px;
                border: 1px solid rgba(255, 255, 255, 0.2);
            ">
                <p style="
                    color: white;
                    font-size: 1.1rem;
                    font-weight: 700;
                    margin: 0 0 0.25rem 0;
                ">$148M+</p>
                <p style="
                    color: rgba(255, 255, 255, 0.9);
                    font-size: 0.8rem;
                    margin: 0;
                ">Proven Savings</p>
            </div>
            <div style="
                background: rgba(255, 255, 255, 0.15);
                padding: 0.75rem;
                border-radius: 8px;
                border: 1px solid rgba(255, 255, 255, 0.2);
            ">
                <p style="
                    color: white;
                    font-size: 1.1rem;
                    font-weight: 700;
                    margin: 0 0 0.25rem 0;
                ">Zero</p>
                <p style="
                    color: rgba(255, 255, 255, 0.9);
                    font-size: 0.8rem;
                    margin: 0;
                ">PHI Exposure</p>
            </div>
        </div>
        
        <!-- Architecture Badges -->
        <div style="
            margin-top: 1rem;
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 0.5rem;
        ">
            <span style="
                background: rgba(16, 185, 129, 0.3);
                color: white;
                padding: 0.4rem 0.9rem;
                border-radius: 20px;
                font-size: 0.85rem;
                font-weight: 600;
                border: 1px solid #10b981;
            ">🏢 On-Premises</span>
            <span style="
                background: rgba(16, 185, 129, 0.3);
                color: white;
                padding: 0.4rem 0.9rem;
                border-radius: 20px;
                font-size: 0.85rem;
                font-weight: 600;
                border: 1px solid #10b981;
            ">🚫 Zero API</span>
            <span style="
                background: rgba(16, 185, 129, 0.3);
                color: white;
                padding: 0.4rem 0.9rem;
                border-radius: 20px;
                font-size: 0.85rem;
                font-weight: 600;
                border: 1px solid #10b981;
            ">🏥 HIPAA-First</span>
        </div>
    </div>
</div>

<!-- Warning Box -->
<div style="
    background: #fff9e6;
    border-left: 4px solid #ff9800;
    border-radius: 6px;
    padding: 1rem 1.5rem;
    margin: 1rem 0;
    text-align: center;
">
    <p style="
        color: #d84315;
        font-size: 0.9rem;
        font-weight: 500;
        margin: 0;
        line-height: 1.5;
    ">
        ⚠️ Portfolio Demonstration: Using synthetic data to showcase real methodology and production-grade analytics.
    </p>
</div>

<!-- Copyright -->
<div style="
    text-align: center;
    padding: 1rem 0;
    margin-top: 1rem;
">
    <p style="
        color: #6b7280;
        font-size: 0.85rem;
        margin: 0;
    ">
        © 2024-2026 Robert Reichert | StarGuard AI™
    </p>
</div>

<style>
/* Mobile responsive adjustments */
@media (max-width: 768px) {
    div[style*="background: linear-gradient(135deg, #4A3D6F"] {
        padding: 1.5rem 1rem !important;
        padding-top: 2rem !important;
    }
    
    div[style*="background: linear-gradient(135deg, #4A3D6F"] h2 {
        font-size: 1.4rem !important;
    }
    
    div[style*="background: linear-gradient(135deg, #4A3D6F"] p {
        font-size: 0.95rem !important;
    }
    
    div[style*="background: rgba(255, 255, 255, 0.2)"] {
        font-size: 0.75rem !important;
        padding: 0.25rem 0.6rem !important;
    }
    
    /* Metrics grid becomes single column on mobile */
    div[style*="grid-template-columns: repeat(3, 1fr)"] {
        grid-template-columns: 1fr !important;
    }
}
</style>
\"\"\", unsafe_allow_html=True)
"""

def get_standard_footer():
    """Return the standard footer HTML code with purple gradient box design and rainbow border"""
    return """
st.markdown("---")
st.markdown(\"\"\"
<div style="
    background: linear-gradient(135deg, #4A3D6F 0%, #6F5F96 100%);
    border-radius: 12px;
    padding: 2rem 1.5rem;
    padding-top: 2.5rem;
    margin: 2rem 0 1rem 0;
    box-shadow: 0 4px 12px rgba(74, 61, 111, 0.25);
    text-align: center;
    position: relative;
    overflow: hidden;
">
    <!-- Rainbow top border using gradient -->
    <div style="
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 6px;
        background: linear-gradient(90deg, #ff0000, #ff7f00, #ffff00, #00ff00, #0000ff, #4b0082, #9400d3);
        border-radius: 12px 12px 0 0;
        z-index: 1;
    "></div>
    
    <!-- Top Hashtags -->
    <div style="
        margin: 0.5rem 0 1.5rem 0;
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 0.5rem;
        position: relative;
        z-index: 2;
    ">
        <span style="
            background: rgba(255, 255, 255, 0.2);
            color: white;
            padding: 0.3rem 0.8rem;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 500;
        ">#HealthcareAnalytics</span>
        <span style="
            background: rgba(255, 255, 255, 0.2);
            color: white;
            padding: 0.3rem 0.8rem;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 500;
        ">#MedicareAdvantage</span>
        <span style="
            background: rgba(255, 255, 255, 0.2);
            color: white;
            padding: 0.3rem 0.8rem;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 500;
        ">#HEDIS</span>
        <span style="
            background: rgba(255, 255, 255, 0.2);
            color: white;
            padding: 0.3rem 0.8rem;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 500;
        ">#DataScience</span>
    </div>
    
    <!-- Title -->
    <h2 style="
        color: white;
        font-size: 1.8rem;
        font-weight: 700;
        margin: 0 0 0.5rem 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        position: relative;
        z-index: 2;
    ">
        ⭐ HEDIS Portfolio Optimizer | StarGuard AI
    </h2>
    
    <!-- Subtitle -->
    <p style="
        color: rgba(255, 255, 255, 0.95);
        font-size: 1.1rem;
        margin: 0 0 1.5rem 0;
        font-weight: 500;
        position: relative;
        z-index: 2;
    ">
        Turning Data Into Stars
    </p>
    
    <!-- Technology Badges -->
    <div style="
        margin: 1rem 0 1.5rem 0;
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 0.5rem;
        position: relative;
        z-index: 2;
    ">
        <span style="
            background: rgba(255, 255, 255, 0.25);
            color: white;
            padding: 0.4rem 0.9rem;
            border-radius: 20px;
            font-size: 0.9rem;
            font-weight: 600;
            border: 1px solid rgba(255, 255, 255, 0.3);
        ">🐍 Python</span>
        <span style="
            background: rgba(255, 255, 255, 0.25);
            color: white;
            padding: 0.4rem 0.9rem;
            border-radius: 20px;
            font-size: 0.9rem;
            font-weight: 600;
            border: 1px solid rgba(255, 255, 255, 0.3);
        ">📊 Streamlit</span>
        <span style="
            background: rgba(255, 255, 255, 0.25);
            color: white;
            padding: 0.4rem 0.9rem;
            border-radius: 20px;
            font-size: 0.9rem;
            font-weight: 600;
            border: 1px solid rgba(255, 255, 255, 0.3);
        ">📈 Plotly</span>
        <span style="
            background: rgba(255, 255, 255, 0.25);
            color: white;
            padding: 0.4rem 0.9rem;
            border-radius: 20px;
            font-size: 0.9rem;
            font-weight: 600;
            border: 1px solid rgba(255, 255, 255, 0.3);
        ">🐘 PostgreSQL</span>
        <span style="
            background: rgba(255, 255, 255, 0.25);
            color: white;
            padding: 0.4rem 0.9rem;
            border-radius: 20px;
            font-size: 0.9rem;
            font-weight: 600;
            border: 1px solid rgba(255, 255, 255, 0.3);
        ">🤖 ML/AI</span>
    </div>
    
    <!-- Green Secure AI Architecture Box -->
    <div style="
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.2) 0%, rgba(5, 150, 105, 0.25) 100%);
        border: 3px solid #10b981;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1.5rem auto;
        max-width: 850px;
        text-align: center;
        box-shadow: 0 4px 8px rgba(16, 185, 129, 0.2);
        position: relative;
        z-index: 2;
    ">
        <p style="
            color: white;
            font-size: 1.1rem;
            font-weight: 700;
            margin: 0 0 1rem 0;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
        ">
            🔒 Secure AI Architecture
        </p>
        <p style="
            color: rgba(255, 255, 255, 0.95);
            font-size: 0.95rem;
            line-height: 1.6;
            margin: 0 0 1.25rem 0;
        ">
            Healthcare AI that sees everything, exposes nothing.
        </p>
        
        <!-- Metrics Grid -->
        <div style="
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 1rem;
            margin: 1rem 0;
        ">
            <div style="
                background: rgba(255, 255, 255, 0.15);
                padding: 0.75rem;
                border-radius: 8px;
                border: 1px solid rgba(255, 255, 255, 0.2);
            ">
                <p style="
                    color: white;
                    font-size: 1.1rem;
                    font-weight: 700;
                    margin: 0 0 0.25rem 0;
                ">2.8-4.1x</p>
                <p style="
                    color: rgba(255, 255, 255, 0.9);
                    font-size: 0.8rem;
                    margin: 0;
                ">ROI Delivered</p>
            </div>
            <div style="
                background: rgba(255, 255, 255, 0.15);
                padding: 0.75rem;
                border-radius: 8px;
                border: 1px solid rgba(255, 255, 255, 0.2);
            ">
                <p style="
                    color: white;
                    font-size: 1.1rem;
                    font-weight: 700;
                    margin: 0 0 0.25rem 0;
                ">$148M+</p>
                <p style="
                    color: rgba(255, 255, 255, 0.9);
                    font-size: 0.8rem;
                    margin: 0;
                ">Proven Savings</p>
            </div>
            <div style="
                background: rgba(255, 255, 255, 0.15);
                padding: 0.75rem;
                border-radius: 8px;
                border: 1px solid rgba(255, 255, 255, 0.2);
            ">
                <p style="
                    color: white;
                    font-size: 1.1rem;
                    font-weight: 700;
                    margin: 0 0 0.25rem 0;
                ">Zero</p>
                <p style="
                    color: rgba(255, 255, 255, 0.9);
                    font-size: 0.8rem;
                    margin: 0;
                ">PHI Exposure</p>
            </div>
        </div>
        
        <!-- Architecture Badges -->
        <div style="
            margin-top: 1rem;
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 0.5rem;
        ">
            <span style="
                background: rgba(16, 185, 129, 0.3);
                color: white;
                padding: 0.4rem 0.9rem;
                border-radius: 20px;
                font-size: 0.85rem;
                font-weight: 600;
                border: 1px solid #10b981;
            ">🏢 On-Premises</span>
            <span style="
                background: rgba(16, 185, 129, 0.3);
                color: white;
                padding: 0.4rem 0.9rem;
                border-radius: 20px;
                font-size: 0.85rem;
                font-weight: 600;
                border: 1px solid #10b981;
            ">🚫 Zero API</span>
            <span style="
                background: rgba(16, 185, 129, 0.3);
                color: white;
                padding: 0.4rem 0.9rem;
                border-radius: 20px;
                font-size: 0.85rem;
                font-weight: 600;
                border: 1px solid #10b981;
            ">🏥 HIPAA-First</span>
        </div>
    </div>
</div>

<!-- Warning Box -->
<div style="
    background: #fff9e6;
    border-left: 4px solid #ff9800;
    border-radius: 6px;
    padding: 1rem 1.5rem;
    margin: 1rem 0;
    text-align: center;
">
    <p style="
        color: #d84315;
        font-size: 0.9rem;
        font-weight: 500;
        margin: 0;
        line-height: 1.5;
    ">
        ⚠️ Portfolio Demonstration: Using synthetic data to showcase real methodology and production-grade analytics.
    </p>
</div>

<!-- Copyright -->
<div style="
    text-align: center;
    padding: 1rem 0;
    margin-top: 1rem;
">
    <p style="
        color: #6b7280;
        font-size: 0.85rem;
        margin: 0;
    ">
        © 2024-2026 Robert Reichert | StarGuard AI™
    </p>
</div>

<style>
/* Mobile responsive adjustments */
@media (max-width: 768px) {
    div[style*="background: linear-gradient(135deg, #4A3D6F"] {
        padding: 1.5rem 1rem !important;
        padding-top: 2rem !important;
    }
    
    div[style*="background: linear-gradient(135deg, #4A3D6F"] h2 {
        font-size: 1.4rem !important;
    }
    
    div[style*="background: linear-gradient(135deg, #4A3D6F"] p {
        font-size: 0.95rem !important;
    }
    
    div[style*="background: rgba(255, 255, 255, 0.2)"] {
        font-size: 0.75rem !important;
        padding: 0.25rem 0.6rem !important;
    }
    
    /* Metrics grid becomes single column on mobile */
    div[style*="grid-template-columns: repeat(3, 1fr)"] {
        grid-template-columns: 1fr !important;
    }
}
</style>
\"\"\", unsafe_allow_html=True)
"""
