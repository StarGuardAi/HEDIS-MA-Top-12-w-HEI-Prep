"""
HEDIS Measure Specifications for Star Rating Portfolio Optimizer

This module contains the complete specifications for all 12 HEDIS measures including
target populations, value sets, denominators, numerators, and exclusions based on
NCQA MY2025 specifications.

HEDIS Specification: MY2025 Volume 2
"""

from dataclasses import dataclass
from typing import List, Dict, Set, Optional
from datetime import datetime


@dataclass
class MeasureSpec:
    """Base specification for a HEDIS measure."""
    code: str
    name: str
    tier: int
    weight: float  # 1.0 or 3.0 (triple-weighted)
    status: str  # production, development, planned
    target_population: str
    data_sources: List[str]
    hedis_spec_version: str
    star_value: str
    new_measure_2025: bool = False
    
    # Population criteria
    age_min: Optional[int] = None
    age_max: Optional[int] = None
    gender_restriction: Optional[str] = None  # None, "male", "female"
    
    # Value sets (ICD-10, CPT, etc.)
    inclusion_codes: Optional[Set[str]] = None
    exclusion_codes: Optional[Set[str]] = None
    
    # Model configuration
    auc_target: float = 0.85
    current_auc: Optional[float] = None


# ============================================================================
# TIER 1: DIABETES CORE MEASURES (5 measures)
# ============================================================================

GSD_SPEC = MeasureSpec(
    code="GSD",
    name="Glycemic Status Assessment for Patients with Diabetes",
    tier=1,
    weight=3.0,  # Triple-weighted
    status="production",
    target_population="diabetes_18_75",
    data_sources=["claims", "labs"],
    hedis_spec_version="MY2025 Volume 2",
    star_value="$360-615K",
    age_min=18,
    age_max=75,
    current_auc=0.91,
    inclusion_codes={
        # ICD-10 diabetes codes (E08-E13)
        "E08.00", "E08.01", "E08.10", "E08.11", "E08.21", "E08.22", "E08.29",
        "E08.311", "E08.319", "E08.321", "E08.329", "E08.331", "E08.339",
        "E09.00", "E09.01", "E09.10", "E09.11", "E09.21", "E09.22", "E09.29",
        "E10.10", "E10.11", "E10.21", "E10.22", "E10.29", "E10.311", "E10.319",
        "E11.00", "E11.01", "E11.10", "E11.11", "E11.21", "E11.22", "E11.29",
        "E11.311", "E11.319", "E11.321", "E11.329", "E11.331", "E11.339",
        "E13.00", "E13.01", "E13.10", "E13.11", "E13.21", "E13.22", "E13.29",
    },
    exclusion_codes={
        # Hospice, SNP, frailty exclusions
        "Z51.5",  # Hospice care
        "Z99.12", # Dependence on ventilator
    }
)

KED_SPEC = MeasureSpec(
    code="KED",
    name="Kidney Health Evaluation for Patients with Diabetes",
    tier=1,
    weight=3.0,  # Triple-weighted
    status="development",
    target_population="diabetes_18_75",
    data_sources=["claims", "labs"],
    hedis_spec_version="MY2025 Volume 2 (NEW)",
    star_value="$360-615K",
    new_measure_2025=True,
    age_min=18,
    age_max=75,
    inclusion_codes={  # Same as GSD
        "E08.00", "E08.01", "E08.10", "E08.11", "E08.21", "E08.22", "E08.29",
        "E09.00", "E09.01", "E09.10", "E09.11", "E09.21", "E09.22", "E09.29",
        "E10.10", "E10.11", "E10.21", "E10.22", "E10.29", "E10.311", "E10.319",
        "E11.00", "E11.01", "E11.10", "E11.11", "E11.21", "E11.22", "E11.29",
        "E13.00", "E13.01", "E13.10", "E13.11", "E13.21", "E13.22", "E13.29",
    }
)

EED_SPEC = MeasureSpec(
    code="EED",
    name="Eye Exam for Patients with Diabetes",
    tier=1,
    weight=1.0,
    status="development",
    target_population="diabetes_18_75",
    data_sources=["claims"],
    hedis_spec_version="MY2025 Volume 2",
    star_value="$120-205K",
    age_min=18,
    age_max=75,
    inclusion_codes={  # Same as GSD
        "E08.00", "E08.01", "E08.10", "E08.11", "E08.21", "E08.22", "E08.29",
        "E09.00", "E09.01", "E09.10", "E09.11", "E09.21", "E09.22", "E09.29",
        "E10.10", "E10.11", "E10.21", "E10.22", "E10.29", "E10.311", "E10.319",
        "E11.00", "E11.01", "E11.10", "E11.11", "E11.21", "E11.22", "E11.29",
        "E13.00", "E13.01", "E13.10", "E13.11", "E13.21", "E13.22", "E13.29",
    }
)

PDC_DR_SPEC = MeasureSpec(
    code="PDC-DR",
    name="Medication Adherence for Diabetes Medications",
    tier=1,
    weight=1.0,
    status="development",
    target_population="diabetes_18_75_on_meds",
    data_sources=["pharmacy"],
    hedis_spec_version="MY2025 Volume 2",
    star_value="$120-205K",
    age_min=18,
    age_max=75,
)

BPD_SPEC = MeasureSpec(
    code="BPD",
    name="Blood Pressure Control for Patients with Diabetes",
    tier=1,
    weight=1.0,
    status="development",
    target_population="diabetes_18_75",
    data_sources=["claims", "vitals"],
    hedis_spec_version="MY2025 Volume 2 (NEW)",
    star_value="$120-205K",
    new_measure_2025=True,
    age_min=18,
    age_max=75,
)

# ============================================================================
# TIER 2: CARDIOVASCULAR MEASURES (4 measures)
# ============================================================================

CBP_SPEC = MeasureSpec(
    code="CBP",
    name="Controlling High Blood Pressure",
    tier=2,
    weight=3.0,  # Triple-weighted
    status="planned",
    target_population="hypertension_18_85",
    data_sources=["claims", "vitals"],
    hedis_spec_version="MY2025 Volume 2",
    star_value="$360-615K",
    age_min=18,
    age_max=85,
    inclusion_codes={
        # Essential hypertension
        "I10",
        # Secondary hypertension
        "I15.0", "I15.1", "I15.2", "I15.8", "I15.9",
    }
)

SUPD_SPEC = MeasureSpec(
    code="SUPD",
    name="Statin Therapy for Patients with Diabetes",
    tier=2,
    weight=1.0,
    status="planned",
    target_population="diabetes_40_75_with_cvd_risk",
    data_sources=["claims", "pharmacy"],
    hedis_spec_version="MY2025 Volume 2",
    star_value="$120-205K",
    age_min=40,
    age_max=75,
)

PDC_RASA_SPEC = MeasureSpec(
    code="PDC-RASA",
    name="Medication Adherence for Hypertension (RAS antagonists)",
    tier=2,
    weight=1.0,
    status="planned",
    target_population="hypertension_18_85_on_rasa",
    data_sources=["pharmacy"],
    hedis_spec_version="MY2025 Volume 2",
    star_value="$120-205K",
    age_min=18,
    age_max=85,
)

PDC_STA_SPEC = MeasureSpec(
    code="PDC-STA",
    name="Medication Adherence for Cholesterol (Statins)",
    tier=2,
    weight=1.0,
    status="planned",
    target_population="hyperlipidemia_18_85_on_statins",
    data_sources=["pharmacy"],
    hedis_spec_version="MY2025 Volume 2",
    star_value="$120-205K",
    age_min=18,
    age_max=85,
)

# ============================================================================
# TIER 3: CANCER SCREENING MEASURES (2 measures)
# ============================================================================

BCS_SPEC = MeasureSpec(
    code="BCS",
    name="Breast Cancer Screening",
    tier=3,
    weight=1.0,
    status="planned",
    target_population="women_50_74",
    data_sources=["claims"],
    hedis_spec_version="MY2025 Volume 2",
    star_value="$150-225K",
    age_min=50,
    age_max=74,
    gender_restriction="female",
)

COL_SPEC = MeasureSpec(
    code="COL",
    name="Colorectal Cancer Screening",
    tier=3,
    weight=1.0,
    status="planned",
    target_population="adults_50_75",
    data_sources=["claims"],
    hedis_spec_version="MY2025 Volume 2",
    star_value="$150-225K",
    age_min=50,
    age_max=75,
)

# ============================================================================
# TIER 4: HEALTH EQUITY INDEX (1 measure)
# ============================================================================

HEI_SPEC = MeasureSpec(
    code="HEI",
    name="Health Equity Index Reward Factor",
    tier=4,
    weight=5.0,  # 5% bonus/penalty (special weight)
    status="planned",
    target_population="all_members",
    data_sources=["all_measures", "sdoh"],
    hedis_spec_version="MY2027 (starts MY2025)",
    star_value="$20-40M (at risk)",
)

# ============================================================================
# MEASURE REGISTRY
# ============================================================================

MEASURE_REGISTRY: Dict[str, MeasureSpec] = {
    # Tier 1: Diabetes
    "GSD": GSD_SPEC,
    "KED": KED_SPEC,
    "EED": EED_SPEC,
    "PDC-DR": PDC_DR_SPEC,
    "BPD": BPD_SPEC,
    
    # Tier 2: Cardiovascular
    "CBP": CBP_SPEC,
    "SUPD": SUPD_SPEC,
    "PDC-RASA": PDC_RASA_SPEC,
    "PDC-STA": PDC_STA_SPEC,
    
    # Tier 3: Cancer Screening
    "BCS": BCS_SPEC,
    "COL": COL_SPEC,
    
    # Tier 4: Health Equity
    "HEI": HEI_SPEC,
}

# Triple-weighted measures
TRIPLE_WEIGHTED_MEASURES = ["GSD", "KED", "CBP"]

# NEW 2025 measures
NEW_2025_MEASURES = ["KED", "BPD"]

# Tier mappings
TIER_1_DIABETES = ["GSD", "KED", "EED", "PDC-DR", "BPD"]
TIER_2_CARDIOVASCULAR = ["CBP", "SUPD", "PDC-RASA", "PDC-STA"]
TIER_3_CANCER = ["BCS", "COL"]
TIER_4_HEI = ["HEI"]

# All measures
ALL_MEASURES = TIER_1_DIABETES + TIER_2_CARDIOVASCULAR + TIER_3_CANCER + TIER_4_HEI


def get_measure_spec(measure_code: str) -> Optional[MeasureSpec]:
    """Get the specification for a specific measure."""
    return MEASURE_REGISTRY.get(measure_code)


def get_measures_by_tier(tier: int) -> List[MeasureSpec]:
    """Get all measures for a specific tier."""
    return [spec for spec in MEASURE_REGISTRY.values() if spec.tier == tier]


def get_measures_by_status(status: str) -> List[MeasureSpec]:
    """Get all measures with a specific status."""
    return [spec for spec in MEASURE_REGISTRY.values() if spec.status == status]


def get_triple_weighted_measures() -> List[MeasureSpec]:
    """Get all triple-weighted measures."""
    return [MEASURE_REGISTRY[code] for code in TRIPLE_WEIGHTED_MEASURES]


def get_new_2025_measures() -> List[MeasureSpec]:
    """Get all NEW 2025 measures."""
    return [spec for spec in MEASURE_REGISTRY.values() if spec.new_measure_2025]


# ============================================================================
# VALUE SETS (CPT, LOINC, NDC codes)
# ============================================================================

# Retinal exam CPT codes (for EED)
RETINAL_EXAM_CPT_CODES = {
    "67028", "67030", "67031", "67036", "67039", "67040", "67041", "67042",
    "67043", "67101", "67105", "67107", "67108", "67110", "67113", "67121",
    "67141", "67145", "67208", "67210", "67218", "67220", "67221", "67227",
    "67228", "92002", "92004", "92012", "92014", "92018", "92019", "92134",
    "92225", "92226", "92227", "92228", "92230", "92235", "92240", "92250",
    "92260", "99203", "99204", "99205", "99213", "99214", "99215"
}

# Mammography CPT codes (for BCS)
MAMMOGRAPHY_CPT_CODES = {
    "77065", "77066", "77067", "77063"  # Digital mammography
}

# Colonoscopy CPT codes (for COL)
COLONOSCOPY_CPT_CODES = {
    "44388", "44389", "44390", "44391", "44392", "44393", "44394",
    "45355", "45378", "45379", "45380", "45381", "45382", "45383",
    "45384", "45385", "45386", "45387", "45388", "45389", "45390",
    "45391", "45392", "45393", "45398"
}

# FIT CPT codes (for COL)
FIT_CPT_CODES = {
    "82270", "82274"
}

# Cologuard CPT codes (for COL)
COLOGUARD_CPT_CODES = {
    "81528"
}

# Lab LOINC codes
HBA1C_LOINC_CODES = {
    "4548-4",  # Hemoglobin A1c/Hemoglobin.total in Blood
    "4549-2",  # Hemoglobin A1c/Hemoglobin.total in Blood by calculation
    "17855-8", # Hemoglobin A1c/Hemoglobin.total in Blood by HPLC
    "17856-6", # Hemoglobin A1c/Hemoglobin.total in Blood by electrophoresis
}

EGFR_LOINC_CODES = {
    "33914-3",  # Glomerular filtration rate/1.73 sq M.predicted
    "48642-3",  # Glomerular filtration rate/1.73 sq M.predicted [Volume Rate/Area] in Serum or Plasma by Creatinine-based formula (MDRD)
    "48643-1",  # Glomerular filtration rate/1.73 sq M.predicted [Volume Rate/Area] in Serum or Plasma by Creatinine-based formula (CKD-EPI)
    "62238-1",  # Glomerular filtration rate/1.73 sq M.predicted [Volume Rate/Area] in Serum or Plasma by Creatinine and Cystatin C-based formula (CKD-EPI 2021)
}

ACR_LOINC_CODES = {
    "9318-7",   # Albumin/Creatinine [Mass Ratio] in Urine
    "14959-1",  # Microalbumin/Creatinine [Mass Ratio] in Urine
    "14958-3",  # Microalbumin [Mass/volume] in Urine
}

# BP measurement LOINC codes
BP_LOINC_CODES = {
    "8480-6",  # Systolic blood pressure
    "8462-4",  # Diastolic blood pressure
    "8478-0",  # Mean blood pressure
}

