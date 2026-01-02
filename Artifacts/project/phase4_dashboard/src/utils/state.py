"""
Session state management
"""
import streamlit as st
from typing import Any, Dict


def init_session_state():
    """Initialize all session state variables with defaults"""
    defaults: Dict[str, Any] = {
        'current_view': 'dashboard',
        'selected_measures': [],
        'date_range': None,
        'filters_applied': False,
        'user_preferences': {},
        'cache_initialized': True
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def get_state(key: str, default: Any = None) -> Any:
    """Safely get value from session state"""
    return st.session_state.get(key, default)


def set_state(key: str, value: Any):
    """Set value in session state"""
    st.session_state[key] = value


def clear_filters():
    """Reset all filter-related state"""
    filter_keys = ['selected_measures', 'date_range', 'filters_applied']
    for key in filter_keys:
        if key in st.session_state:
            del st.session_state[key]

