"""
AI Insights Generator Module
Uses OpenAI or Anthropic Claude API to generate natural language executive insights
"""
import os
import json
from typing import Dict, Optional, List
import streamlit as st

# Try importing OpenAI
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    openai = None

# Try importing Anthropic
try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False
    anthropic = None


def get_api_provider() -> str:
    """
    Determine which API provider to use based on available keys.
    Priority: OpenAI > Anthropic
    
    Checks:
    1. Environment variables (OPENAI_API_KEY, ANTHROPIC_API_KEY)
    2. Streamlit secrets (.streamlit/secrets.toml)
    """
    # Check OpenAI
    if OPENAI_AVAILABLE:
        openai_key = os.getenv("OPENAI_API_KEY")
        if not openai_key and hasattr(st, 'secrets'):
            try:
                if 'openai' in st.secrets and 'api_key' in st.secrets["openai"]:
                    openai_key = str(st.secrets["openai"]["api_key"])
            except (KeyError, AttributeError, TypeError):
                pass
        if openai_key and len(openai_key.strip()) > 0:
            return "openai"
    
    # Check Anthropic
    if ANTHROPIC_AVAILABLE:
        anthropic_key = os.getenv("ANTHROPIC_API_KEY")
        if not anthropic_key and hasattr(st, 'secrets'):
            try:
                if 'anthropic' in st.secrets and 'api_key' in st.secrets["anthropic"]:
                    anthropic_key = str(st.secrets["anthropic"]["api_key"])
            except (KeyError, AttributeError, TypeError):
                pass
        if anthropic_key and len(anthropic_key.strip()) > 0:
            return "anthropic"
    
    return "none"


def get_openai_client():
    """Get OpenAI client with API key."""
    api_key = os.getenv("OPENAI_API_KEY")
    
    # Try Streamlit secrets if not in environment
    if not api_key and hasattr(st, 'secrets'):
        try:
            if 'openai' in st.secrets and 'api_key' in st.secrets["openai"]:
                api_key = str(st.secrets["openai"]["api_key"])
        except (KeyError, AttributeError, TypeError):
            pass
    
    if not api_key or len(api_key.strip()) == 0:
        raise ValueError("OpenAI API key not found. Set OPENAI_API_KEY environment variable or add to Streamlit secrets.")
    
    return openai.OpenAI(api_key=api_key.strip())


def get_anthropic_client():
    """Get Anthropic client with API key."""
    api_key = os.getenv("ANTHROPIC_API_KEY")
    
    # Try Streamlit secrets if not in environment
    if not api_key and hasattr(st, 'secrets'):
        try:
            if 'anthropic' in st.secrets and 'api_key' in st.secrets["anthropic"]:
                api_key = str(st.secrets["anthropic"]["api_key"])
        except (KeyError, AttributeError, TypeError):
            pass
    
    if not api_key or len(api_key.strip()) == 0:
        raise ValueError(
            "Anthropic API key not found. Set ANTHROPIC_API_KEY environment variable "
            "or add to .streamlit/secrets.toml as:\n"
            "[anthropic]\n"
            "api_key = \"your-key-here\""
        )
    
    return anthropic.Anthropic(api_key=api_key.strip())


def format_metrics_text(metrics: Dict) -> str:
    """
    Format metrics dictionary into readable text for AI prompt.
    """
    text = "=== HEDIS PORTFOLIO METRICS ===\n\n"
    
    # Portfolio Summary
    portfolio = metrics.get("portfolio_summary", {})
    text += f"PORTFOLIO OVERVIEW:\n"
    text += f"- Total Investment: ${portfolio.get('total_investment', 0):,.2f}\n"
    text += f"- Total Closures: {portfolio.get('total_closures', 0):,}\n"
    text += f"- Revenue Impact: ${portfolio.get('revenue_impact', 0):,.2f}\n"
    text += f"- ROI Ratio: {portfolio.get('roi_ratio', 0):.2f}\n"
    text += f"- Net Benefit: ${portfolio.get('net_benefit', 0):,.2f}\n"
    text += f"- Overall Success Rate: {portfolio.get('overall_success_rate', 0):.1f}%\n"
    text += f"- Total Interventions: {portfolio.get('total_interventions', 0):,}\n\n"
    
    # Measure Details
    measure = metrics.get("measure_details", {})
    if measure:
        text += f"TOP MEASURE PERFORMANCE:\n"
        text += f"- Measure: {measure.get('measure_name', 'N/A')} ({measure.get('measure_code', 'N/A')})\n"
        text += f"- Total Investment: ${measure.get('total_investment', 0):,.2f}\n"
        text += f"- Successful Closures: {measure.get('successful_closures', 0):,}\n"
        text += f"- ROI Ratio: {measure.get('roi_ratio', 0):.2f}\n"
        text += f"- Revenue Impact: ${measure.get('revenue_impact', 0):,.2f}\n\n"
    
    # Member Prioritization
    member_data = metrics.get("member_prioritization", [])
    if member_data:
        text += f"MEMBER PRIORITIZATION (Next 30 Days):\n"
        for item in member_data[:5]:  # Top 5
            text += f"- {item.get('measure_name', 'N/A')}: {item.get('members_needing_intervention', 0):,} members, "
            text += f"{item.get('predicted_success_rate', 0):.1f}% predicted closure rate, "
            text += f"${item.get('potential_revenue', 0):,.2f} potential revenue\n"
        text += "\n"
    
    # Top Opportunities
    opportunities = metrics.get("top_opportunities", [])
    if opportunities:
        text += f"TOP OPPORTUNITIES:\n"
        for i, opp in enumerate(opportunities, 1):
            text += f"{i}. {opp.get('measure_name', 'N/A')}:\n"
            text += f"   - ROI Ratio: {opp.get('roi_ratio', 0):.2f}\n"
            text += f"   - Predicted Closure Rate: {opp.get('predicted_closure_rate', 0):.1f}%\n"
            text += f"   - Members Needing Intervention: {opp.get('members_count', 0):,}\n"
            text += f"   - Potential Revenue: ${opp.get('potential_revenue', 0):,.2f}\n"
            text += f"   - Potential Net Benefit: ${opp.get('potential_net_benefit', 0):,.2f}\n"
        text += "\n"
    
    # Activity Metrics (top 3)
    activities = metrics.get("activity_metrics", [])
    if activities:
        text += f"TOP ACTIVITIES BY SUCCESS RATE:\n"
        for item in activities[:3]:
            text += f"- {item.get('activity_name', 'N/A')}: {item.get('success_rate', 0):.1f}% success rate, "
            text += f"${item.get('cost_per_closure', 0):.2f} per closure\n"
        text += "\n"
    
    # Budget Metrics
    budget = metrics.get("budget_metrics", [])
    if budget:
        text += f"BUDGET PERFORMANCE:\n"
        for item in budget[:3]:
            text += f"- {item.get('measure_name', 'N/A')}: "
            text += f"${item.get('budget_allocated', 0):,.2f} allocated, "
            text += f"${item.get('actual_spent', 0):,.2f} spent, "
            text += f"{item.get('variance_pct', 0):.1f}% variance ({item.get('budget_status', 'N/A')})\n"
    
    return text


def generate_insights_openai(metrics: Dict, model: str = "gpt-4o-mini") -> Dict[str, str]:
    """
    Generate insights using OpenAI API.
    Returns dictionary with 'summary', 'recommendations', and 'why_matters' keys.
    """
    client = get_openai_client()
    metrics_text = format_metrics_text(metrics)
    
    prompt = f"""You are an expert healthcare analytics consultant providing executive insights for a HEDIS portfolio optimization program.

Analyze the following HEDIS portfolio metrics and generate:

1. A concise executive summary (2-3 sentences) highlighting the most important finding
2. Actionable recommendations (3-5 specific, prioritized recommendations with numbers and timelines)
3. A "Why this matters" explanation (2-3 sentences explaining business impact for non-technical executives)

Format your response as JSON with these exact keys:
- "summary": executive summary text
- "recommendations": array of recommendation strings
- "why_matters": explanation text

Be specific with numbers, percentages, and dollar amounts from the data. Use natural, conversational language suitable for C-level executives.

METRICS DATA:
{metrics_text}

Generate insights now:"""

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are an expert healthcare analytics consultant. Always respond with valid JSON only."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        
        content = response.choices[0].message.content.strip()
        
        # Try to parse JSON from response
        # Sometimes the model wraps JSON in markdown code blocks
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()
        
        result = json.loads(content)
        
        # Ensure all required keys exist
        if "summary" not in result:
            result["summary"] = "Analysis complete. Review recommendations below."
        if "recommendations" not in result:
            result["recommendations"] = []
        if "why_matters" not in result:
            result["why_matters"] = "These insights help optimize HEDIS performance and maximize ROI."
        
        return result
        
    except json.JSONDecodeError as e:
        # Fallback if JSON parsing fails
        return {
            "summary": content[:200] + "..." if len(content) > 200 else content,
            "recommendations": ["Review the detailed metrics above for specific recommendations."],
            "why_matters": "These insights help optimize HEDIS performance and maximize ROI."
        }
    except Exception as e:
        raise Exception(f"OpenAI API error: {str(e)}")


def generate_insights_anthropic(metrics: Dict, model: str = "claude-3-haiku-20240307") -> Dict[str, str]:
    """
    Generate insights using Anthropic Claude API.
    Returns dictionary with 'summary', 'recommendations', and 'why_matters' keys.
    """
    client = get_anthropic_client()
    metrics_text = format_metrics_text(metrics)
    
    prompt = f"""You are an expert healthcare analytics consultant providing executive insights for a HEDIS portfolio optimization program.

Analyze the following HEDIS portfolio metrics and generate:

1. A concise executive summary (2-3 sentences) highlighting the most important finding
2. Actionable recommendations (3-5 specific, prioritized recommendations with numbers and timelines)
3. A "Why this matters" explanation (2-3 sentences explaining business impact for non-technical executives)

Format your response as JSON with these exact keys:
- "summary": executive summary text
- "recommendations": array of recommendation strings
- "why_matters": explanation text

Be specific with numbers, percentages, and dollar amounts from the data. Use natural, conversational language suitable for C-level executives.

METRICS DATA:
{metrics_text}

Generate insights now. Respond with valid JSON only:"""

    try:
        message = client.messages.create(
            model=model,
            max_tokens=1000,
            temperature=0.7,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        content = message.content[0].text.strip()
        
        # Try to parse JSON from response
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()
        
        result = json.loads(content)
        
        # Ensure all required keys exist
        if "summary" not in result:
            result["summary"] = "Analysis complete. Review recommendations below."
        if "recommendations" not in result:
            result["recommendations"] = []
        if "why_matters" not in result:
            result["why_matters"] = "These insights help optimize HEDIS performance and maximize ROI."
        
        return result
        
    except json.JSONDecodeError as e:
        # Fallback if JSON parsing fails
        return {
            "summary": content[:200] + "..." if len(content) > 200 else content,
            "recommendations": ["Review the detailed metrics above for specific recommendations."],
            "why_matters": "These insights help optimize HEDIS performance and maximize ROI."
        }
    except Exception as e:
        raise Exception(f"Anthropic API error: {str(e)}")


def generate_executive_insights(metrics: Dict, provider: Optional[str] = None, model: Optional[str] = None) -> Dict[str, str]:
    """
    Generate executive insights using the configured AI provider.
    
    Args:
        metrics: Dictionary of formatted metrics from ai_insights_data
        provider: Optional provider override ("openai", "anthropic", or None for auto-detect)
        model: Optional model name override
    
    Returns:
        Dictionary with 'summary', 'recommendations', and 'why_matters' keys
    """
    if provider is None:
        provider = get_api_provider()
    
    if provider == "none":
        raise ValueError(
            "No AI API provider configured. Please set either OPENAI_API_KEY or ANTHROPIC_API_KEY "
            "environment variable, or add to Streamlit secrets."
        )
    
    # Set default models
    if model is None:
        if provider == "openai":
            model = "gpt-4o-mini"
        else:
            model = "claude-3-haiku-20240307"
    
    if provider == "openai":
        if not OPENAI_AVAILABLE:
            raise ImportError("OpenAI package not installed. Install with: pip install openai")
        return generate_insights_openai(metrics, model)
    elif provider == "anthropic":
        if not ANTHROPIC_AVAILABLE:
            raise ImportError("Anthropic package not installed. Install with: pip install anthropic")
        return generate_insights_anthropic(metrics, model)
    else:
        raise ValueError(f"Unknown provider: {provider}")

