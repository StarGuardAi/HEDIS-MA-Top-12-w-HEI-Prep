"""
HEDIS Measure Definitions
Comprehensive definitions for all HEDIS measures
"""
from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class MeasureDefinition:
    """HEDIS measure definition structure."""
    measure_id: str
    measure_name: str
    official_definition: str
    numerator_description: str
    denominator_description: str
    exclusion_criteria: List[str]
    data_collection_period: str
    star_rating_weight: float
    quality_bonus_impact: str
    audit_requirements: List[str]
    typical_benchmark_rate: float
    age_groups: List[str]
    risk_factors: List[str]


# HEDIS Measure Definitions Database
MEASURE_DEFINITIONS: Dict[str, MeasureDefinition] = {
    "HBA1C": MeasureDefinition(
        measure_id="HBA1C",
        measure_name="HbA1c Testing",
        official_definition=(
            "The percentage of members 18-75 years of age with diabetes (type 1 or type 2) "
            "who had an HbA1c test performed during the measurement year."
        ),
        numerator_description=(
            "Members who had at least one HbA1c test (CPT: 83036, 83037; LOINC: 4548-4, 4549-2) "
            "during the measurement year."
        ),
        denominator_description=(
            "Members 18-75 years of age with diabetes (type 1 or type 2) as of December 31 "
            "of the measurement year."
        ),
        exclusion_criteria=[
            "Members in hospice or receiving palliative care",
            "Members with frailty and advanced illness",
            "Members who died during the measurement year"
        ],
        data_collection_period="January 1 - December 31 (measurement year)",
        star_rating_weight=0.15,
        quality_bonus_impact="High - Direct impact on Star Rating and quality bonus",
        audit_requirements=[
            "Lab results must be documented in medical record",
            "Results must be within measurement year",
            "CPT/LOINC codes must be valid"
        ],
        typical_benchmark_rate=85.0,
        age_groups=["18-44", "45-64", "65-75"],
        risk_factors=["Diabetes Type 1", "Diabetes Type 2", "Comorbidities"]
    ),
    "BP": MeasureDefinition(
        measure_id="BP",
        measure_name="Blood Pressure Control",
        official_definition=(
            "The percentage of members 18-85 years of age with hypertension who had their "
            "blood pressure adequately controlled (<140/90 mmHg) during the measurement year."
        ),
        numerator_description=(
            "Members with most recent blood pressure reading <140/90 mmHg during the "
            "measurement year."
        ),
        denominator_description=(
            "Members 18-85 years of age with hypertension as of December 31 of the "
            "measurement year."
        ),
        exclusion_criteria=[
            "Members in hospice",
            "Members with end-stage renal disease",
            "Members who died during the measurement year"
        ],
        data_collection_period="January 1 - December 31 (measurement year)",
        star_rating_weight=0.12,
        quality_bonus_impact="High - Significant impact on cardiovascular outcomes",
        audit_requirements=[
            "Blood pressure readings must be documented",
            "Readings must be within measurement year",
            "Multiple readings preferred for accuracy"
        ],
        typical_benchmark_rate=80.0,
        age_groups=["18-44", "45-64", "65-85"],
        risk_factors=["Hypertension", "Cardiovascular Disease", "Diabetes"]
    ),
    "COL": MeasureDefinition(
        measure_id="COL",
        measure_name="Colorectal Cancer Screening",
        official_definition=(
            "The percentage of members 45-75 years of age who had appropriate screening "
            "for colorectal cancer during the measurement year or the year prior."
        ),
        numerator_description=(
            "Members who had one of the following: FOBT, FIT, sDNA-FIT, CT colonography, "
            "flexible sigmoidoscopy, or colonoscopy during the measurement period."
        ),
        denominator_description=(
            "Members 45-75 years of age as of December 31 of the measurement year."
        ),
        exclusion_criteria=[
            "Members with total colectomy",
            "Members in hospice",
            "Members who died during the measurement year"
        ],
        data_collection_period="January 1 (prior year) - December 31 (measurement year)",
        star_rating_weight=0.10,
        quality_bonus_impact="Medium - Preventive care measure",
        audit_requirements=[
            "Screening results must be documented",
            "Appropriate CPT codes required",
            "Results within measurement period"
        ],
        typical_benchmark_rate=75.0,
        age_groups=["45-54", "55-64", "65-75"],
        risk_factors=["Family History", "Personal History", "Age"]
    ),
    "MAM": MeasureDefinition(
        measure_id="MAM",
        measure_name="Breast Cancer Screening",
        official_definition=(
            "The percentage of women 50-74 years of age who had a mammogram to screen "
            "for breast cancer during the measurement year or the year prior."
        ),
        numerator_description=(
            "Women who had a mammogram (CPT: 77067, 77066, G0202) during the measurement period."
        ),
        denominator_description=(
            "Women 50-74 years of age as of December 31 of the measurement year."
        ),
        exclusion_criteria=[
            "Women with bilateral mastectomy",
            "Women in hospice",
            "Women who died during the measurement year"
        ],
        data_collection_period="January 1 (prior year) - December 31 (measurement year)",
        star_rating_weight=0.10,
        quality_bonus_impact="Medium - Preventive care measure",
        audit_requirements=[
            "Mammogram results must be documented",
            "Appropriate CPT codes required",
            "Results within measurement period"
        ],
        typical_benchmark_rate=78.0,
        age_groups=["50-59", "60-69", "70-74"],
        risk_factors=["Family History", "Personal History", "Age"]
    ),
    "CCS": MeasureDefinition(
        measure_id="CCS",
        measure_name="Cervical Cancer Screening",
        official_definition=(
            "The percentage of women 21-64 years of age who were screened for cervical "
            "cancer during the measurement year or the year prior."
        ),
        numerator_description=(
            "Women who had a Pap test or HPV test during the measurement period."
        ),
        denominator_description=(
            "Women 21-64 years of age as of December 31 of the measurement year."
        ),
        exclusion_criteria=[
            "Women with total hysterectomy",
            "Women in hospice",
            "Women who died during the measurement year"
        ],
        data_collection_period="January 1 (prior year) - December 31 (measurement year)",
        star_rating_weight=0.08,
        quality_bonus_impact="Medium - Preventive care measure",
        audit_requirements=[
            "Screening results must be documented",
            "Appropriate CPT codes required",
            "Results within measurement period"
        ],
        typical_benchmark_rate=82.0,
        age_groups=["21-29", "30-39", "40-49", "50-64"],
        risk_factors=["Age", "Screening History"]
    )
}


def get_measure_definition(measure_id: str) -> Optional[MeasureDefinition]:
    """Get measure definition by ID."""
    return MEASURE_DEFINITIONS.get(measure_id.upper())


def get_all_measures() -> List[str]:
    """Get list of all available measure IDs."""
    return list(MEASURE_DEFINITIONS.keys())


def get_measure_name(measure_id: str) -> str:
    """Get measure name by ID."""
    definition = get_measure_definition(measure_id)
    return definition.measure_name if definition else measure_id

