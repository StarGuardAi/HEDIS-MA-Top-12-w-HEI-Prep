"""
UI components for displaying AI-generated insights
"""
import streamlit as st
import logging
from typing import Dict, Any, List
import pandas as pd

from src.ai.insights_engine import InsightsEngine, InsightsCache
from core.exceptions import ExternalServiceError, ConfigurationError

logger = logging.getLogger(__name__)


def render_executive_summary(portfolio_metrics: Dict[str, Any]) -> None:
    """
    Render AI-generated executive summary at top of dashboard
    
    Args:
        portfolio_metrics: Dictionary of portfolio performance metrics
    """
    st.markdown("### 🤖 AI Executive Summary")
    
    with st.spinner("Generating insights..."):
        try:
            engine = InsightsEngine()
            summary = engine.generate_executive_summary(portfolio_metrics)
            
            # Display in info box
            st.info(summary)
            
            # Add expand for details
            with st.expander("📊 Data Behind This Summary"):
                st.json(portfolio_metrics)
                
        except ConfigurationError as e:
            st.warning(f"⚠️ AI features require API key configuration. {e.message}")
            st.caption("💡 Tip: Set OPENAI_API_KEY environment variable or add to Streamlit secrets")
            logger.warning(f"AI configuration error: {e}")
        except ExternalServiceError as e:
            st.error(f"❌ Could not generate AI summary: {e.message}")
            logger.error(f"AI service error: {e}")
        except Exception as e:
            st.error(f"❌ Unexpected error generating summary: {str(e)}")
            logger.exception("Unexpected error in executive summary generation")


def render_metric_explainer(
    metric_name: str,
    metric_value: float,
    context: Dict[str, Any]
) -> None:
    """
    Render "Explain this metric" button with AI explanation
    
    Args:
        metric_name: Name of the metric to explain
        metric_value: Current value of the metric
        context: Additional context (benchmark, prior period, etc.)
    """
    button_key = f"explain_{metric_name.replace(' ', '_').lower()}"
    
    if st.button(f"❓ Explain {metric_name}", key=button_key):
        with st.spinner("Generating explanation..."):
            try:
                engine = InsightsEngine()
                explanation = engine.explain_metric(metric_name, metric_value, context)
                st.info(explanation)
            except ConfigurationError as e:
                st.warning(f"⚠️ {e.message}")
                logger.warning(f"AI configuration error: {e}")
            except ExternalServiceError as e:
                st.error(f"❌ Could not generate explanation: {e.message}")
                logger.error(f"AI service error: {e}")
            except Exception as e:
                st.error(f"❌ Unexpected error: {str(e)}")
                logger.exception("Unexpected error in metric explanation")


def render_smart_recommendations(measures_data: pd.DataFrame) -> None:
    """
    Render AI-generated recommendations section
    
    Args:
        measures_data: DataFrame with measure performance data
    """
    st.markdown("### 🎯 AI-Powered Recommendations")
    
    with st.spinner("Analyzing data and generating recommendations..."):
        try:
            engine = InsightsEngine()
            recommendations = engine.generate_recommendations(measures_data, top_n=3)
            
            if not recommendations:
                st.info("No recommendations generated. Check data availability.")
                return
            
            for i, rec in enumerate(recommendations, 1):
                priority_emoji = {
                    'High': '🔴',
                    'Medium': '🟡',
                    'Low': '🟢'
                }.get(rec.get('priority', 'Medium'), '⚪')
                
                priority = rec.get('priority', 'Medium')
                title = rec.get('title', f'Recommendation {i}')
                description = rec.get('description', 'No description available')
                expected_impact = rec.get('expected_impact', 'Not specified')
                
                with st.expander(f"{i}. {priority_emoji} {title} - {priority} Priority"):
                    st.write(description)
                    st.metric("Expected Impact", expected_impact)
                    
        except ConfigurationError as e:
            st.warning(f"⚠️ AI features require API key configuration. {e.message}")
            logger.warning(f"AI configuration error: {e}")
        except ExternalServiceError as e:
            st.error(f"❌ Could not generate recommendations: {e.message}")
            logger.error(f"AI service error: {e}")
        except Exception as e:
            st.error(f"❌ Unexpected error generating recommendations: {str(e)}")
            logger.exception("Unexpected error in recommendations generation")


def render_anomaly_alerts(
    time_series_data: pd.DataFrame,
    metric_name: str
) -> None:
    """
    Check for and display anomalies
    
    Args:
        time_series_data: DataFrame with time series data
        metric_name: Name of metric to check for anomalies
    """
    try:
        engine = InsightsEngine()
        anomaly_narrative = engine.detect_anomalies(time_series_data, metric_name)
        
        if anomaly_narrative:
            st.warning(f"⚠️ **Anomaly Detected**\n\n{anomaly_narrative}")
            logger.info(f"Anomaly detected for {metric_name}")
            
    except Exception as e:
        # Fail silently for anomaly detection to avoid disrupting UX
        logger.debug(f"Anomaly detection failed (non-critical): {e}")


def render_ai_settings() -> None:
    """
    Render AI settings/configuration UI in sidebar
    """
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🤖 AI Settings")
    
    # Check if API key is configured
    import os
    has_openai_key = bool(os.getenv("OPENAI_API_KEY"))
    has_anthropic_key = bool(os.getenv("ANTHROPIC_API_KEY"))
    
    if has_openai_key or has_anthropic_key:
        st.sidebar.success("✅ AI API configured")
        if has_openai_key:
            st.sidebar.caption("Provider: OpenAI")
        if has_anthropic_key:
            st.sidebar.caption("Provider: Anthropic")
    else:
        st.sidebar.warning("⚠️ AI features disabled")
        st.sidebar.caption("Set OPENAI_API_KEY or ANTHROPIC_API_KEY")
    
    # Cache management
    if st.sidebar.button("🗑️ Clear AI Cache"):
        InsightsCache.clear_insights_cache()
        st.sidebar.success("Cache cleared!")
        st.rerun()

