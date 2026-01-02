"""
AI Insights Engine - Generate natural language insights from data

Uses OpenAI GPT-4 or Anthropic Claude to generate executive summaries,
recommendations, and explanations of HEDIS analytics.
"""
import os
import json
import logging
from typing import Dict, Any, List, Optional
import pandas as pd
import streamlit as st

try:
    from openai import OpenAI
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False
    OpenAI = None

try:
    from anthropic import Anthropic
    HAS_ANTHROPIC = True
except ImportError:
    HAS_ANTHROPIC = False
    Anthropic = None

from core.exceptions import ExternalServiceError, ConfigurationError

logger = logging.getLogger(__name__)


class InsightsEngine:
    """
    Main AI insights generation engine
    
    Generates:
    - Executive summaries
    - Metric explanations
    - Recommendations
    - Anomaly narratives
    - Trend analyses
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "gpt-4",
        provider: str = "openai"
    ) -> None:
        """
        Initialize insights engine
        
        Args:
            api_key: API key (defaults to env var)
            model: Model to use (gpt-4, gpt-4-turbo, claude-3-opus, etc.)
            provider: Provider to use (openai or anthropic)
        
        Raises:
            ConfigurationError: If API key not set or provider not available
        """
        self.provider = provider.lower()
        self.model = model
        self.api_key = api_key or os.getenv("OPENAI_API_KEY") or os.getenv("ANTHROPIC_API_KEY")
        
        if not self.api_key:
            raise ConfigurationError(
                "API key not set. Set OPENAI_API_KEY or ANTHROPIC_API_KEY environment variable.",
                error_code="AI_CONFIG_MISSING"
            )
        
        # Initialize client based on provider
        if self.provider == "openai":
            if not HAS_OPENAI:
                raise ConfigurationError(
                    "OpenAI package not installed. Install with: pip install openai",
                    error_code="AI_PACKAGE_MISSING"
                )
            self.client = OpenAI(api_key=self.api_key)
        elif self.provider == "anthropic":
            if not HAS_ANTHROPIC:
                raise ConfigurationError(
                    "Anthropic package not installed. Install with: pip install anthropic",
                    error_code="AI_PACKAGE_MISSING"
                )
            self.client = Anthropic(api_key=self.api_key)
        else:
            raise ConfigurationError(
                f"Unknown provider: {provider}. Use 'openai' or 'anthropic'",
                error_code="AI_PROVIDER_INVALID"
            )
        
        logger.info(f"InsightsEngine initialized with provider={self.provider}, model={self.model}")
    
    @st.cache_data(ttl=3600)
    def generate_executive_summary(
        _self,  # Note: _self to avoid hashing
        portfolio_metrics: Dict[str, Any]
    ) -> str:
        """
        Generate executive summary of portfolio performance
        
        Args:
            portfolio_metrics: Dict with keys:
                - total_members: int
                - total_gaps: int
                - predicted_closure_rate: float (0-100)
                - total_financial_value: float
                - star_rating_current: float
                - star_rating_predicted: float
                - top_measures: List[Dict] with measure details
        
        Returns:
            Natural language executive summary (2-3 paragraphs)
        
        Raises:
            ExternalServiceError: If API call fails
        """
        from src.ai.prompts import EXECUTIVE_SUMMARY_PROMPT
        
        try:
            # Build context from metrics
            context = _self._build_context_string(portfolio_metrics)
            
            # Generate with AI
            if _self.provider == "openai":
                response = _self.client.chat.completions.create(
                    model=_self.model,
                    messages=[
                        {
                            "role": "system",
                            "content": EXECUTIVE_SUMMARY_PROMPT
                        },
                        {
                            "role": "user",
                            "content": f"Generate an executive summary based on this data:\n\n{context}"
                        }
                    ],
                    temperature=0.7,
                    max_tokens=500
                )
                summary = response.choices[0].message.content
            else:  # anthropic
                response = _self.client.messages.create(
                    model=_self.model,
                    max_tokens=500,
                    system=EXECUTIVE_SUMMARY_PROMPT,
                    messages=[{
                        "role": "user",
                        "content": f"Generate an executive summary based on this data:\n\n{context}"
                    }]
                )
                summary = response.content[0].text
            
            logger.info("Executive summary generated successfully")
            return summary
            
        except Exception as e:
            logger.error(f"Error generating executive summary: {e}")
            raise ExternalServiceError(
                f"Failed to generate executive summary: {str(e)}",
                error_code="AI_EXECUTIVE_SUMMARY_FAILED"
            )
    
    @st.cache_data(ttl=1800)
    def explain_metric(
        _self,
        metric_name: str,
        metric_value: float,
        context: Dict[str, Any]
    ) -> str:
        """
        Generate plain-English explanation of a specific metric
        
        Args:
            metric_name: Name of the metric (e.g., "ROI Percentage")
            metric_value: Current value
            context: Additional context (benchmark, prior period, etc.)
        
        Returns:
            Clear explanation of what the metric means and why it matters
        
        Raises:
            ExternalServiceError: If API call fails
        """
        from src.ai.prompts import METRIC_EXPLANATION_PROMPT
        
        try:
            prompt = f"""
            Metric: {metric_name}
            Value: {metric_value}
            Context: {context}
            
            Explain this metric in plain English for a healthcare executive.
            Include:
            1. What this metric measures
            2. Why it matters for Medicare Advantage plans
            3. Whether this value is good/bad/neutral
            4. What action (if any) should be taken
            
            Keep it concise (3-4 sentences).
            """
            
            if _self.provider == "openai":
                response = _self.client.chat.completions.create(
                    model=_self.model,
                    messages=[
                        {"role": "system", "content": METRIC_EXPLANATION_PROMPT},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.5,
                    max_tokens=200
                )
                explanation = response.choices[0].message.content
            else:  # anthropic
                response = _self.client.messages.create(
                    model=_self.model,
                    max_tokens=200,
                    system=METRIC_EXPLANATION_PROMPT,
                    messages=[{
                        "role": "user",
                        "content": prompt
                    }]
                )
                explanation = response.content[0].text
            
            logger.info(f"Metric explanation generated for {metric_name}")
            return explanation
            
        except Exception as e:
            logger.error(f"Error explaining metric {metric_name}: {e}")
            raise ExternalServiceError(
                f"Failed to explain metric: {str(e)}",
                error_code="AI_METRIC_EXPLANATION_FAILED"
            )
    
    @st.cache_data(ttl=3600)
    def generate_recommendations(
        _self,
        measures_data: pd.DataFrame,
        top_n: int = 3
    ) -> List[Dict[str, str]]:
        """
        Generate top N actionable recommendations
        
        Args:
            measures_data: DataFrame with measure performance data
            top_n: Number of recommendations to generate
        
        Returns:
            List of dicts with keys: title, description, priority, expected_impact
        
        Raises:
            ExternalServiceError: If API call fails
        """
        from src.ai.prompts import RECOMMENDATIONS_PROMPT
        
        try:
            # Prepare data summary
            if measures_data.empty:
                return []
            
            data_summary = measures_data.to_dict('records')
            
            prompt = f"""
            Based on this HEDIS measure data:
            {json.dumps(data_summary, indent=2)}
            
            Generate {top_n} actionable recommendations for improving Star Ratings.
            
            For each recommendation, provide:
            1. Title (concise action)
            2. Description (why and how)
            3. Priority (High/Medium/Low)
            4. Expected Impact (specific numbers)
            
            Format as JSON array with key "recommendations".
            """
            
            if _self.provider == "openai":
                response = _self.client.chat.completions.create(
                    model=_self.model,
                    messages=[
                        {"role": "system", "content": RECOMMENDATIONS_PROMPT},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.8,
                    max_tokens=800,
                    response_format={"type": "json_object"}
                )
                content = response.choices[0].message.content
            else:  # anthropic
                response = _self.client.messages.create(
                    model=_self.model,
                    max_tokens=800,
                    system=RECOMMENDATIONS_PROMPT,
                    messages=[{
                        "role": "user",
                        "content": prompt
                    }]
                )
                content = response.content[0].text
            
            # Parse JSON response
            recommendations_data = json.loads(content)
            recommendations = recommendations_data.get('recommendations', [])
            
            logger.info(f"Generated {len(recommendations)} recommendations")
            return recommendations[:top_n]
            
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing recommendations JSON: {e}")
            return []
        except Exception as e:
            logger.error(f"Error generating recommendations: {e}")
            raise ExternalServiceError(
                f"Failed to generate recommendations: {str(e)}",
                error_code="AI_RECOMMENDATIONS_FAILED"
            )
    
    def detect_anomalies(
        self,
        time_series_data: pd.DataFrame,
        metric_name: str
    ) -> Optional[str]:
        """
        Detect anomalies and generate narrative explanation
        
        Args:
            time_series_data: DataFrame with date and metric columns
            metric_name: Name of metric being analyzed
        
        Returns:
            Anomaly narrative if detected, None otherwise
        
        Raises:
            ExternalServiceError: If API call fails
        """
        from src.ai.prompts import ANOMALY_DETECTION_PROMPT
        
        try:
            if time_series_data.empty or metric_name not in time_series_data.columns:
                return None
            
            # Simple anomaly detection
            mean = time_series_data[metric_name].mean()
            std = time_series_data[metric_name].std()
            latest = time_series_data[metric_name].iloc[-1]
            
            # Check if latest value is anomalous (>2 std devs)
            if std == 0 or abs(latest - mean) <= 2 * std:
                return None
            
            prompt = f"""
            The metric "{metric_name}" just showed an unusual value:
            - Latest: {latest:.2f}
            - Historical average: {mean:.2f}
            - Standard deviation: {std:.2f}
            
            This is a {abs(latest - mean) / std:.1f} standard deviation change.
            
            Generate a brief alert message (2-3 sentences) explaining:
            1. What changed
            2. Possible reasons
            3. Recommended action
            """
            
            if self.provider == "openai":
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": ANOMALY_DETECTION_PROMPT},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.6,
                    max_tokens=150
                )
                narrative = response.choices[0].message.content
            else:  # anthropic
                response = self.client.messages.create(
                    model=self.model,
                    max_tokens=150,
                    system=ANOMALY_DETECTION_PROMPT,
                    messages=[{
                        "role": "user",
                        "content": prompt
                    }]
                )
                narrative = response.content[0].text
            
            logger.info(f"Anomaly detected and narrative generated for {metric_name}")
            return narrative
            
        except Exception as e:
            logger.error(f"Error detecting anomalies: {e}")
            return None
    
    def generate_weekly_insights_email(
        self,
        portfolio_metrics: Dict[str, Any],
        top_opportunities: List[Dict],
        alerts: List[str]
    ) -> str:
        """
        Generate formatted email with weekly insights
        
        Args:
            portfolio_metrics: Portfolio performance metrics
            top_opportunities: List of top opportunities
            alerts: List of alert messages
        
        Returns:
            HTML formatted email body
        
        Raises:
            ExternalServiceError: If API call fails
        """
        from src.ai.prompts import EMAIL_INSIGHTS_PROMPT
        
        try:
            prompt = f"""
            Generate a professional weekly insights email for healthcare executives.
            
            Portfolio Metrics:
            {json.dumps(portfolio_metrics, indent=2)}
            
            Top Opportunities:
            {json.dumps(top_opportunities, indent=2)}
            
            Alerts:
            {json.dumps(alerts, indent=2)}
            
            Format as HTML email with:
            - Professional greeting
            - Executive summary (2-3 sentences)
            - Key metrics section
            - Top 3 opportunities
            - Any alerts
            - Call to action
            - Professional closing
            
            Keep it concise but informative.
            """
            
            if self.provider == "openai":
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": EMAIL_INSIGHTS_PROMPT},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=1000
                )
                email = response.choices[0].message.content
            else:  # anthropic
                response = self.client.messages.create(
                    model=self.model,
                    max_tokens=1000,
                    system=EMAIL_INSIGHTS_PROMPT,
                    messages=[{
                        "role": "user",
                        "content": prompt
                    }]
                )
                email = response.content[0].text
            
            logger.info("Weekly insights email generated successfully")
            return email
            
        except Exception as e:
            logger.error(f"Error generating weekly insights email: {e}")
            raise ExternalServiceError(
                f"Failed to generate email: {str(e)}",
                error_code="AI_EMAIL_GENERATION_FAILED"
            )
    
    def _build_context_string(self, metrics: Dict[str, Any]) -> str:
        """
        Helper to convert metrics dict to readable string
        
        Args:
            metrics: Dictionary of metrics
        
        Returns:
            Formatted string representation
        """
        lines = []
        for key, value in metrics.items():
            if isinstance(value, float):
                lines.append(f"{key}: {value:.2f}")
            elif isinstance(value, list):
                lines.append(f"{key}: {len(value)} items")
            else:
                lines.append(f"{key}: {value}")
        return "\n".join(lines)


class InsightsCache:
    """
    Manage caching of AI-generated insights
    
    Since AI API calls are expensive, cache aggressively
    """
    
    @staticmethod
    @st.cache_data(ttl=86400)  # Cache for 24 hours
    def cache_insight(key: str, content: str) -> str:
        """
        Cache insight with 24-hour TTL
        
        Args:
            key: Cache key
            content: Content to cache
        
        Returns:
            Cached content
        """
        return content
    
    @staticmethod
    def clear_insights_cache() -> None:
        """Clear all cached insights"""
        st.cache_data.clear()
        logger.info("AI insights cache cleared")

