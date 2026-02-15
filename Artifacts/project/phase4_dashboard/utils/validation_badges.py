"""
Validation badges and confidence messaging (Option C quick wins)
Standardized "Validated against X historical...", confidence scores, and "Why Trust This?" tooltips
"""
from datetime import datetime
from typing import Optional


def validation_badge_html(
    message: str,
    last_validated: Optional[str] = None,
    compact: bool = False,
) -> str:
    """
    Return HTML for a green validation badge.
    message: e.g. "Validated against 18 months historical"
    last_validated: e.g. "2024-01-15" or None to use today
    """
    if last_validated is None:
        last_validated = datetime.now().strftime("%Y-%m-%d")
    if compact:
        return f"""
        <div style="background: #f0fdf4; border: 1px solid #10B981; border-radius: 6px; padding: 0.35rem 0.75rem; margin: 0.5rem 0; font-size: 0.85rem;">
            <span style="color: #065f46; font-weight: 600;">✓ {message}</span>
            <span style="color: #047857;"> — Last validated: {last_validated}</span>
        </div>
        """
    return f"""
    <div style="background: #f0fdf4; border: 1px solid #10B981; border-radius: 8px; padding: 0.5rem 1rem; margin: 0.75rem 0;">
        <span style="color: #065f46; font-weight: 600;">✓ {message}</span>
        <span style="color: #047857; font-size: 0.9rem;"> — Last validated: {last_validated}</span>
    </div>
    """


def confidence_score_html(score: float, label: str = "Confidence") -> str:
    """Color-coded confidence score (0-100). Green >=70, yellow 50-69, red <50."""
    score = max(0, min(100, score))
    if score >= 70:
        color = "#059669"
        bg = "#ecfdf5"
    elif score >= 50:
        color = "#b45309"
        bg = "#fffbeb"
    else:
        color = "#b91c1c"
        bg = "#fef2f2"
    return f"""
    <span style="background: {bg}; color: {color}; padding: 0.2rem 0.5rem; border-radius: 6px; font-weight: 600;">{label}: {score:.0f}%</span>
    """


def why_trust_tooltip_text() -> str:
    """Default 'Why Trust This?' tooltip content."""
    return (
        "Metrics are validated against historical interventions and, where applicable, "
        "compared to prior-year actuals. Confidence scores reflect alignment with expected variance."
    )
