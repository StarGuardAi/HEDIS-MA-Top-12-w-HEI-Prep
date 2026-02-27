"""
Intervention Analysis
Financial impact per intervention and portfolio optimization for quality budgets
"""
from typing import Dict, List, Optional, Any

try:
    from utils.measure_definitions import get_measure_definition
except ImportError:
    def get_measure_definition(measure_id: str):
        return None


# Default quality bonus per member per star (CMS-style)
DEFAULT_QUALITY_BONUS_PER_STAR = 50.0


def _star_weight(measure_id: str) -> float:
    """Star rating weight for measure (triple-weighted ~0.15, others lower)."""
    d = get_measure_definition(measure_id)
    if d and hasattr(d, "star_rating_weight"):
        return float(d.star_rating_weight)
    # Fallback by common codes
    high_weight = {"HBA1C", "BP", "CDC", "CBP", "EED"}
    return 0.15 if (measure_id.upper() in high_weight) else 0.10


def calculate_intervention_roi(
    intervention_type: str,
    target_measure: str,
    expected_gap_closure: float,
    intervention_cost: float,
    member_count: int,
    revenue_per_closure: float = 100.0,
    quality_bonus_per_member_per_star: float = DEFAULT_QUALITY_BONUS_PER_STAR,
) -> Dict[str, Any]:
    """
    Calculate ROI for a specific intervention.

    Args:
        intervention_type: e.g. "Member Outreach Campaign", "Provider Education", "EHR Alert System"
        target_measure: e.g. "BCS", "CDC", "CBP"
        expected_gap_closure: expected rate improvement (e.g. 8 for 8%)
        intervention_cost: total cost of intervention ($)
        member_count: denominator / member count for the measure
        revenue_per_closure: revenue impact per closed gap
        quality_bonus_per_member_per_star: $ per member per star point

    Returns:
        cost_per_closure, expected_rate_improvement, financial_impact (breakdown),
        roi_ratio, confidence_score, star_rating_bonus_impact
    """
    if intervention_cost <= 0 or member_count <= 0:
        return {
            "cost_per_closure": 0.0,
            "expected_rate_improvement": expected_gap_closure,
            "financial_impact": {"total": 0.0, "revenue_from_closures": 0.0, "star_rating_bonus": 0.0},
            "roi_ratio": 0.0,
            "confidence_score": 0.0,
            "star_rating_bonus_impact": 0.0,
            "estimated_closures": 0,
            "intervention_type": intervention_type,
            "target_measure": target_measure,
        }

    # Estimated closures from rate improvement: rate_improvement% of denominator
    estimated_closures = int(member_count * (expected_gap_closure / 100.0))
    estimated_closures = max(estimated_closures, 1)

    cost_per_closure = intervention_cost / estimated_closures

    # Revenue from closures
    revenue_from_closures = estimated_closures * revenue_per_closure

    # Star rating impact: rate improvement can move star (simplified)
    # 0.1 star improvement per ~2% rate gain for weighted measures
    star_weight = _star_weight(target_measure)
    star_improvement = (expected_gap_closure / 100.0) * (star_weight / 0.10) * 0.5  # scale down
    star_rating_bonus = member_count * quality_bonus_per_member_per_star * star_improvement

    total_benefit = revenue_from_closures + star_rating_bonus
    roi_ratio = (total_benefit / intervention_cost) if intervention_cost else 0.0

    # Confidence: lower if cost per closure is very high or rate improvement is aggressive
    confidence = 85.0
    if cost_per_closure > 200:
        confidence -= 10
    if expected_gap_closure > 15:
        confidence -= 5
    confidence = max(50.0, min(95.0, confidence))

    return {
        "cost_per_closure": round(cost_per_closure, 2),
        "expected_rate_improvement": expected_gap_closure,
        "financial_impact": {
            "total": round(total_benefit, 2),
            "revenue_from_closures": round(revenue_from_closures, 2),
            "star_rating_bonus": round(star_rating_bonus, 2),
        },
        "roi_ratio": round(roi_ratio, 2),
        "confidence_score": round(confidence, 1),
        "star_rating_bonus_impact": round(star_rating_bonus, 2),
        "estimated_closures": estimated_closures,
        "intervention_type": intervention_type,
        "target_measure": target_measure,
        "total_cost": intervention_cost,
        "net_roi": round(total_benefit - intervention_cost, 2),
    }


def get_default_interventions() -> List[Dict[str, Any]]:
    """Default set of available interventions for portfolio optimization."""
    return [
        {
            "id": "outreach_bcs",
            "intervention_type": "Member Outreach Campaign",
            "target_measure": "BCS",
            "expected_gap_closure": 8.0,
            "intervention_cost": 15000.0,
            "member_count": 2000,
            "star_weight": 0.10,
        },
        {
            "id": "provider_diabetes",
            "intervention_type": "Provider Education",
            "target_measure": "CDC",
            "expected_gap_closure": 12.0,
            "intervention_cost": 25000.0,
            "member_count": 3000,
            "star_weight": 0.15,
        },
        {
            "id": "ehr_cbp",
            "intervention_type": "EHR Alert System",
            "target_measure": "CBP",
            "expected_gap_closure": 15.0,
            "intervention_cost": 50000.0,
            "member_count": 4000,
            "star_weight": 0.12,
        },
        {
            "id": "outreach_col",
            "intervention_type": "Member Outreach Campaign",
            "target_measure": "COL",
            "expected_gap_closure": 6.0,
            "intervention_cost": 12000.0,
            "member_count": 2500,
            "star_weight": 0.10,
        },
        {
            "id": "lab_reminder",
            "intervention_type": "Lab Order Reminders",
            "target_measure": "CDC",
            "expected_gap_closure": 10.0,
            "intervention_cost": 18000.0,
            "member_count": 3000,
            "star_weight": 0.15,
        },
        {
            "id": "bp_home",
            "intervention_type": "Home BP Monitoring",
            "target_measure": "CBP",
            "expected_gap_closure": 9.0,
            "intervention_cost": 22000.0,
            "member_count": 4000,
            "star_weight": 0.12,
        },
        {
            "id": "mam_outreach",
            "intervention_type": "Mammography Outreach",
            "target_measure": "MAM",
            "expected_gap_closure": 7.0,
            "intervention_cost": 14000.0,
            "member_count": 1800,
            "star_weight": 0.10,
        },
        {
            "id": "eye_exam",
            "intervention_type": "Eye Exam Reminders",
            "target_measure": "EED",
            "expected_gap_closure": 11.0,
            "intervention_cost": 20000.0,
            "member_count": 2500,
            "star_weight": 0.15,
        },
    ]


def optimize_intervention_portfolio(
    budget: float,
    available_interventions: Optional[List[Dict]] = None,
    constraints: Optional[Dict] = None,
) -> Dict[str, Any]:
    """
    Given a budget, recommend an intervention mix using three approaches.

    Approaches:
    1. Max Star Rating: prioritize triple/high-weighted measures.
    2. Max Financial Return: prioritize best ROI ratio.
    3. Balanced: mix of quick wins (high ROI) and strategic (high star weight).

    Args:
        budget: Total budget ($)
        available_interventions: List of intervention dicts (or use default)
        constraints: Optional min/max per intervention, required measures, etc.

    Returns:
        Dict with approach_1_max_star, approach_2_max_roi, approach_3_balanced,
        each with selected_interventions, total_cost, total_impact, total_star_impact.
    """
    constraints = constraints or {}
    interventions = available_interventions or get_default_interventions()

    # Compute ROI and star impact for each
    computed = []
    for i in interventions:
        roi = calculate_intervention_roi(
            intervention_type=i["intervention_type"],
            target_measure=i["target_measure"],
            expected_gap_closure=i["expected_gap_closure"],
            intervention_cost=i["intervention_cost"],
            member_count=i["member_count"],
        )
        computed.append({
            **i,
            "roi_ratio": roi["roi_ratio"],
            "net_roi": roi["net_roi"],
            "financial_impact_total": roi["financial_impact"]["total"],
            "star_rating_bonus": roi["star_rating_bonus_impact"],
            "confidence_score": roi["confidence_score"],
        })

    def select_by_budget(items: List[Dict], sort_key: str, budget_limit: float) -> List[Dict]:
        selected = []
        remaining = budget_limit
        for item in sorted(items, key=lambda x: -x.get(sort_key, 0)):
            cost = item["intervention_cost"]
            if cost <= remaining and cost > 0:
                selected.append(item)
                remaining -= cost
        return selected

    # 1. Max Star Rating: sort by star_rating_bonus (or star_weight * impact)
    by_star = sorted(computed, key=lambda x: -(x.get("star_rating_bonus", 0) or x.get("star_weight", 0) * x["financial_impact_total"]))
    selected_star = select_by_budget(by_star, "star_rating_bonus", budget)

    # 2. Max Financial Return: sort by roi_ratio
    by_roi = sorted(computed, key=lambda x: -x["roi_ratio"])
    selected_roi = select_by_budget(by_roi, "roi_ratio", budget)

    # 3. Balanced: alternate high ROI and high star (quick wins + strategic)
    quick_wins = sorted(computed, key=lambda x: -x["roi_ratio"])[:4]
    strategic = sorted(computed, key=lambda x: -(x.get("star_rating_bonus", 0)))[:4]
    combined = list({c["id"]: c for c in quick_wins + strategic}.values())
    selected_balanced = []
    remaining = budget
    for item in sorted(combined, key=lambda x: (-x["roi_ratio"], -(x.get("star_rating_bonus", 0))):
        if item["intervention_cost"] <= remaining and item["intervention_cost"] > 0:
            selected_balanced.append(item)
            remaining -= item["intervention_cost"]

    def sum_selected(sel: List[Dict]) -> Dict:
        total_cost = sum(s["intervention_cost"] for s in sel)
        total_impact = sum(s["financial_impact_total"] for s in sel)
        total_star = sum(s["star_rating_bonus"] for s in sel)
        return {
            "selected_interventions": sel,
            "total_cost": total_cost,
            "total_financial_impact": total_impact,
            "total_star_rating_bonus": total_star,
            "net_benefit": total_impact - total_cost,
            "count": len(sel),
        }

    return {
        "budget": budget,
        "approach_1_max_star": sum_selected(selected_star),
        "approach_2_max_roi": sum_selected(selected_roi),
        "approach_3_balanced": sum_selected(selected_balanced),
    }
