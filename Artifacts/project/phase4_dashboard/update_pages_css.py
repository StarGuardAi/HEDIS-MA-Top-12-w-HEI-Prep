"""
Script to update all page files to use apply_compact_css() instead of inline CSS
"""
import os
import re

pages_dir = "pages"
old_css_pattern = r'# Ultra-compact CSS for vertical space reduction.*?</style>""", unsafe_allow_html=True\)'
old_css_regex = re.compile(old_css_pattern, re.DOTALL)

new_css_code = '''import pandas as pd
from datetime import datetime

from utils.database import execute_query
from src.ui.layout import render_page_footer, render_sidebar_footer, render_header, apply_compact_css

# Apply ultra-compact CSS
apply_compact_css()

st.sidebar.success("📱 Mobile Optimized")

# Sidebar footer
render_sidebar_footer()'''

# This is a helper script - we'll update pages manually for better control





