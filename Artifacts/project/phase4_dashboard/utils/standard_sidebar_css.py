"""
Standard Sidebar CSS for all pages
Matches the home page sidebar styling exactly
"""

STANDARD_SIDEBAR_CSS = """
/* ========== PURPLE SIDEBAR THEME ========== */
/* Match the StarGuard AI header purple gradient */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #4A3D6F 0%, #6F5F96 100%) !important;
}

[data-testid="stSidebar"] > div:first-child {
    background: linear-gradient(180deg, #4A3D6F 0%, #6F5F96 100%) !important;
}

/* ========== ALL SIDEBAR TEXT WHITE ========== */
/* Force ALL text in sidebar to be white */
[data-testid="stSidebar"],
[data-testid="stSidebar"] *,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] div,
[data-testid="stSidebar"] a,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] button,
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] h4 {
    color: #FFFFFF !important;
}

/* ========== LEFT ALIGN SIDEBAR NAVIGATION LINKS ========== */
/* Left align all sidebar navigation page labels - must override centering rules */
[data-testid="stSidebarNav"],
[data-testid="stSidebarNav"] *,
[data-testid="stSidebarNav"] ul,
[data-testid="stSidebarNav"] ul *,
[data-testid="stSidebarNav"] li,
[data-testid="stSidebarNav"] li *,
[data-testid="stSidebarNav"] a,
[data-testid="stSidebarNav"] a *,
[data-testid="stSidebarNav"] a span,
[data-testid="stSidebarNav"] a div,
[data-testid="stSidebarNav"] a p {
    text-align: left !important;
    margin-left: 0 !important;
    margin-right: auto !important;
}

[data-testid="stSidebarNav"] a {
    display: block !important;
    text-align: left !important;
    justify-content: flex-start !important;
}

/* ========== HOME BUTTON STYLING - MATCH OTHER LINKS ========== */
/* Hide the default "app" text and replace with "🏠 Home" - match other navigation links exactly */
[data-testid="stSidebarNav"] ul li:first-child a {
    font-size: 0 !important;  /* Hide original text */
    background: transparent !important;
    padding: 0 !important;
    border-radius: 0 !important;
    border: none !important;
    margin: 0 !important;
    text-align: left !important;
}

/* Add "🏠 Home" text - exactly match other navigation links styling */
[data-testid="stSidebarNav"] ul li:first-child a::before {
    content: "🏠 Home" !important;
    font-size: inherit !important;
    color: #FFFFFF !important;
    font-weight: inherit !important;
    display: inline !important;
    text-align: left !important;
    margin: 0 !important;
}

/* ========== SIDEBAR WIDGET STYLING ========== */
/* Sidebar selectbox and other widgets */
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stMultiSelect label,
[data-testid="stSidebar"] .stSlider label,
[data-testid="stSidebar"] .stRadio label {
    color: white !important;
}

/* Sidebar widget backgrounds - make them visible on purple */
[data-testid="stSidebar"] .stSelectbox > div > div,
[data-testid="stSidebar"] .stMultiSelect > div > div {
    background-color: rgba(255, 255, 255, 0.95) !important;
    border-radius: 5px !important;
}

[data-testid="stSidebar"] .stSelectbox > div > div *,
[data-testid="stSidebar"] .stMultiSelect > div > div * {
    color: #4A3D6F !important;
}

/* Sidebar success/info boxes */
[data-testid="stSidebar"] [data-testid="stSuccess"],
[data-testid="stSidebar"] [data-testid="stInfo"] {
    background-color: rgba(255, 255, 255, 0.1) !important;
    border: 1px solid rgba(255, 255, 255, 0.3) !important;
}

[data-testid="stSidebar"] [data-testid="stSuccess"] *,
[data-testid="stSidebar"] [data-testid="stInfo"] * {
    color: white !important;
}

/* Sidebar button styling */
[data-testid="stSidebar"] button {
    background-color: rgba(255, 255, 255, 0.2) !important;
    color: white !important;
    border: 1px solid rgba(255, 255, 255, 0.3) !important;
}

/* ========== SIDEBAR SEPARATOR STYLING - SUBTLE GREEN GRADIENT ========== */
[data-testid="stSidebar"] hr {
    border: none !important;
    height: 4px !important;
    margin: 1rem 0 !important;
    background: linear-gradient(
        90deg,
        transparent 0%,
        rgba(74, 222, 128, 0.8) 50%,
        transparent 100%
    ) !important;
}

/* Mobile responsive */
@media (max-width: 768px) {
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #4A3D6F 0%, #6F5F96 100%) !important;
    }
    
    [data-testid="stSidebar"] * {
        color: white !important;
    }
}
"""
