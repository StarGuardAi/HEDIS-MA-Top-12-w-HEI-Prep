"""
AI-specific configuration settings
"""
from typing import Dict, Any

# AI Provider Settings
AI_CONFIG: Dict[str, Any] = {
    'default_provider': 'openai',  # 'openai' or 'anthropic'
    'default_model': 'gpt-4',  # 'gpt-4', 'gpt-4-turbo', 'claude-3-opus', etc.
    'cache_ttl': 3600,  # Cache AI responses for 1 hour
    'max_tokens': {
        'executive_summary': 500,
        'metric_explanation': 200,
        'recommendations': 800,
        'anomaly_detection': 150,
        'email': 1000
    },
    'temperature': {
        'executive_summary': 0.7,
        'metric_explanation': 0.5,
        'recommendations': 0.8,
        'anomaly_detection': 0.6,
        'email': 0.7
    }
}

# Cost Management
AI_COST_CONFIG: Dict[str, Any] = {
    'enable_caching': True,
    'cache_ttl_hours': 24,
    'rate_limit_per_minute': 60,  # Max API calls per minute
    'estimated_cost_per_call': {
        'executive_summary': 0.02,
        'metric_explanation': 0.01,
        'recommendations': 0.05,
        'anomaly_detection': 0.01,
        'email': 0.03
    }
}

