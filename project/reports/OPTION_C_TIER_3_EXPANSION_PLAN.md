# Option C: Tier 3 Expansion Plan

**Date:** October 25, 2025  
**Focus:** Expand to 6 preventive care measures  
**Status:** 🚧 **IN PROGRESS** (1/6 implemented)  
**Target Value:** $500K-$800K additional (Tier 3 only)

---

## Executive Summary

**Tier 3 Expansion** adds 6 preventive care measures to complement the existing Tier 1 (diabetes) and Tier 2 (cardiovascular) portfolios. This brings the total to **15 HEDIS measures** with a combined annual value of **$1.5M-$2.5M** for a 100K member Medicare Advantage plan.

**Current Status:**
- ✅ BCS (Breast Cancer Screening) - Implemented
- 🔲 COL (Colorectal Cancer Screening) - Planned
- 🔲 FLU (Influenza Immunization) - Planned
- 🔲 PNU (Pneumococcal Vaccination) - Planned
- 🔲 AWC (Adolescent Well-Care Visits) - Planned
- 🔲 WCC (Weight Assessment for Children) - Planned

---

## 1. Tier 3 Measures Overview

| Measure | Description | Age Range | Weight | Annual Value | Implementation |
|---------|-------------|-----------|--------|--------------|----------------|
| **BCS** | Breast Cancer Screening | Women 50-74 | 1x | $80K-$120K | ✅ Complete |
| **COL** | Colorectal Cancer Screening | 50-75 | 1x | $100K-$150K | 🔲 Planned |
| **FLU** | Influenza Immunization | 65+ | 1x | $80K-$120K | 🔲 Planned |
| **PNU** | Pneumococcal Vaccination | 65+ | 1x | $60K-$90K | 🔲 Planned |
| **AWC** | Adolescent Well-Care Visits | 12-21 | 1x | $60K-$90K | 🔲 Planned |
| **WCC** | Weight Assessment (Children) | 3-17 | 1x | $60K-$90K | 🔲 Planned |
| **TOTAL** | **6 Preventive Measures** | **Varied** | **6x** | **$440K-$660K** | **1/6 (17%)** |

---

## 2. BCS Implementation (COMPLETE)

### Breast Cancer Screening (BCS)

**File:** `src/measures/tier3_bcs.py`  
**Status:** ✅ **IMPLEMENTED**

**Key Features:**
- Age 50-74 calculation (HEDIS standard)
- 27-month continuous enrollment check
- Mammography CPT codes (77065, 77066, 77067)
- Bilateral mastectomy exclusion
- 2-year screening window (measurement year + prior year)
- Gap prioritization by age (older = higher priority)

**Population:** Women aged 50-74 with continuous enrollment  
**Numerator:** Mammography screening in measurement or prior year  
**Annual Value:** $80K-$120K (100K members)

**Clinical Rationale:**
- U.S. Preventive Services Task Force (USPSTF) Grade B recommendation
- Biennial mammography reduces breast cancer mortality by 15-20%
- Early detection improves 5-year survival rates to 99%

---

## 3. Remaining Tier 3 Measures (PLANNED)

### A. COL - Colorectal Cancer Screening

**Planned File:** `src/measures/tier3_col.py`

**Specification:**
- **Age Range:** 50-75 years (both genders)
- **Screening Options:**
  - Colonoscopy (10 years)
  - Flexible sigmoidoscopy (5 years)
  - CT colonography (5 years)
  - FIT test (annual)
  - FIT-DNA test (3 years)
- **Exclusions:** Total colectomy, colorectal cancer history, hospice
- **Look-back Period:** Varies by screening type (1-10 years)

**Implementation Complexity:** HIGH
- Multiple screening modalities with different look-back periods
- Complex exclusion logic (colectomy codes)
- Requires historical claims data (up to 10 years for colonoscopy)

**CPT Codes:**
- Colonoscopy: 44388-44408, 45378-45398, G0105, G0121
- Sigmoidoscopy: 45330-45345, G0104
- FIT test: 82270, 82274, G0328
- CT Colonography: 74263

**Annual Value:** $100K-$150K (highest value in Tier 3)

**Priority:** HIGH (triple-weighted in some Star Ratings formulas)

---

### B. FLU - Influenza Immunization

**Planned File:** `src/measures/tier3_flu.py`

**Specification:**
- **Age Range:** 65+ years
- **Screening Window:** October 1 - March 31 (flu season)
- **Vaccine Codes:**
  - CPT: 90630, 90653, 90654, 90655, 90656, 90662, 90672, 90673, 90685, 90686, 90687, 90688
  - CVX: 135, 140, 141, 144, 150, 155, 158, 161, 166, 168, 171, 185, 186
- **Exclusions:** Egg allergy (ICD-10 Z91.012), hospice

**Implementation Complexity:** MEDIUM
- Seasonal date window (crosses measurement year boundary)
- Multiple vaccine formulations (standard, high-dose, adjuvanted)
- Requires pharmacy and/or procedure claims

**Annual Value:** $80K-$120K

**Priority:** HIGH (easiest measure to close gaps - single annual vaccine)

---

### C. PNU - Pneumococcal Vaccination

**Planned File:** `src/measures/tier3_pnu.py`

**Specification:**
- **Age Range:** 65+ years
- **Vaccine Types:**
  - PCV13 (Prevnar 13) - conjugate vaccine
  - PPSV23 (Pneumovax 23) - polysaccharide vaccine
- **Vaccination Schedule:**
  - PCV13 first, then PPSV23 ≥8 weeks later
  - OR PPSV23 alone (if already received PCV13)
- **Look-back Period:** Lifetime (once vaccinated, always compliant)

**Implementation Complexity:** MEDIUM-HIGH
- Lifetime look-back (requires historical data)
- Sequence validation (PCV13 before PPSV23)
- Multiple vaccine administration sites (pharmacy, physician office)

**CPT Codes:**
- PCV13: 90670, CVX 133
- PPSV23: 90732, CVX 33

**Annual Value:** $60K-$90K

**Priority:** MEDIUM (lifetime measure, most members already vaccinated)

---

### D. AWC - Adolescent Well-Care Visits

**Planned File:** `src/measures/tier3_awc.py`

**Specification:**
- **Age Range:** 12-21 years
- **Visit Types:**
  - Comprehensive well-care visit
  - At least one visit in measurement year
- **Exclusions:** None (except hospice)

**Implementation Complexity:** LOW
- Simple age range
- Single annual visit requirement
- Well-defined CPT codes

**CPT Codes:**
- Preventive visits: 99381-99385, 99391-99395, 99461
- Adolescent-specific: 99401-99404

**Annual Value:** $60K-$90K

**Priority:** LOW (smaller population in Medicare Advantage)

**Note:** This measure is more relevant for Medicaid/commercial plans. Medicare Advantage has limited adolescent membership.

---

### E. WCC - Weight Assessment for Children

**Planned File:** `src/measures/tier3_wcc.py`

**Specification:**
- **Age Range:** 3-17 years
- **Requirements:**
  - BMI percentile documented
  - Counseling for nutrition
  - Counseling for physical activity
- **Visit Window:** Outpatient visit in measurement year

**Implementation Complexity:** HIGH
- Requires clinical data (BMI values)
- Counseling documentation (CPT codes or procedure codes)
- Multiple components must be met

**CPT Codes:**
- BMI percentile: Z68.51-Z68.54
- Nutrition counseling: 97802-97804, G0447, S9470
- Physical activity counseling: 99401-99404

**Annual Value:** $60K-$90K

**Priority:** LOW (very small pediatric population in Medicare Advantage)

**Note:** This measure is primarily for Medicaid/commercial plans. MA plans have minimal pediatric enrollment.

---

## 4. Implementation Priority Ranking

### Recommended Implementation Order

**Phase 1 (Highest ROI):**
1. ✅ **BCS** - Completed (largest female population, high value)
2. **FLU** - Easy to implement, easiest gap closure
3. **COL** - Highest value ($100K-$150K), but complex

**Phase 2 (Medium ROI):**
4. **PNU** - Medium complexity, lifetime measure
5. **AWC** - Simple implementation, but small MA population

**Phase 3 (Lower Priority for MA):**
6. **WCC** - Limited applicability to Medicare Advantage

### Business Case by Measure

| Measure | Implementation Effort | Population Size (MA) | Annual Value | ROI Rank |
|---------|----------------------|---------------------|--------------|----------|
| BCS | Medium | Large (50% of 50-74F) | $80K-$120K | 1 (High) |
| FLU | Low | Large (all 65+) | $80K-$120K | 2 (High) |
| COL | High | Large (50-75) | $100K-$150K | 3 (High) |
| PNU | Medium | Large (all 65+) | $60K-$90K | 4 (Medium) |
| AWC | Low | Very Small (<1% MA) | $60K-$90K | 5 (Low) |
| WCC | High | Minimal (<0.5% MA) | $60K-$90K | 6 (Low) |

---

## 5. Combined Portfolio Value (Tier 1 + 2 + 3)

### Total Value Projection

| Tier | Measures | Population | Annual Value (100K) | Star Weight | Status |
|------|----------|------------|---------------------|-------------|--------|
| Tier 1 | 5 Diabetes | Adults with diabetes | $400K-$650K | 5x | ✅ Complete |
| Tier 2 | 4 Cardiovascular | Adults with HTN/CVD | $500K-$750K | 6x (CBP 3x) | ✅ Complete |
| Tier 3 | 6 Preventive | Age-specific | $440K-$660K | 6x | 🚧 1/6 (17%) |
| **TOTAL** | **15 Measures** | **Population-wide** | **$1.34M-$2.06M** | **17x** | **73% Complete** |

**With Full Tier 3 Implementation:**
- **Total Measures:** 15 HEDIS measures
- **Annual Value:** $1.3M-$2.1M (100K member plan)
- **Star Rating Impact:** Up to 17x weighted points
- **Portfolio Completion:** From 60% to 100% (most valuable measures)

---

## 6. Technical Implementation Strategy

### Reusable Components (From Tier 1 & 2)

All Tier 3 measures will leverage existing optimized infrastructure:

1. **Age Calculation** (HEDIS standard, Dec 31 reference)
2. **Continuous Enrollment Checks**
3. **Exclusion Logic** (hospice, cancer history)
4. **Gap Prioritization Scoring**
5. **Pre-grouped DataFrames** (performance optimization)
6. **Vectorized Operations**
7. **Standardized Return Types**

**Code Reuse:** ~60% (measure-specific logic only)

---

### Measure Template Structure

```python
class Tier3Measure:
    def __init__(self, measurement_year: int):
        # Standard initialization
        pass
    
    def calculate_age(self, birth_date: datetime) -> int:
        # Reuse from existing measures
        pass
    
    def is_in_denominator(self, member_df, claims_df) -> Tuple[bool, str]:
        # Measure-specific denominator logic
        pass
    
    def is_in_numerator(self, claims_df) -> Tuple[bool, str]:
        # Measure-specific numerator logic
        pass
    
    def calculate_member_status(self, member_df, claims_df) -> Dict:
        # Standard status calculation
        pass
    
    def calculate_population_rate(self, members_df, claims_df) -> Dict:
        # OPTIMIZED: Use pre-grouped DataFrames from Option B
        pass


def generate_gap_list(members_df, claims_df, measurement_year) -> pd.DataFrame:
    # Standard gap list generation
    pass
```

---

## 7. Implementation Timeline

### Estimated Effort by Measure

| Measure | Code (hours) | Testing (hours) | Reviews (hours) | Total | Status |
|---------|-------------|----------------|----------------|-------|--------|
| BCS | 2 | 1 | 0.5 | 3.5 | ✅ Complete |
| FLU | 1.5 | 1 | 0.5 | 3 | 🔲 Planned |
| COL | 4 | 2 | 1 | 7 | 🔲 Planned |
| PNU | 3 | 1.5 | 0.5 | 5 | 🔲 Planned |
| AWC | 1 | 0.5 | 0.5 | 2 | 🔲 Planned |
| WCC | 3 | 1.5 | 0.5 | 5 | 🔲 Planned |
| **TOTAL** | **14.5** | **7.5** | **3.5** | **25.5 hours** | **14% Done** |

**Completed:** 3.5 hours (BCS)  
**Remaining:** 22 hours (5 measures)

### Recommended Schedule

**Week 1:** BCS ✅, FLU, COL (High Priority)  
**Week 2:** PNU, AWC, WCC (Complete Tier 3)  
**Week 3:** Integration testing, dashboard updates, documentation

---

## 8. Decision Point: Full Tier 3 vs. Dashboard Integration

### Option C.1: Complete All 6 Tier 3 Measures (22 hours remaining)
**Pros:**
- Complete 15-measure portfolio ($1.3M-$2.1M value)
- Demonstrate breadth across all clinical domains
- Strongest possible portfolio for job applications

**Cons:**
- Additional 22 hours of implementation
- Diminishing returns (WCC/AWC have minimal MA applicability)
- Delays dashboard integration and deployment

---

### Option C.2: Implement High-Priority Tier 3 Only (FLU + COL) (10 hours)
**Pros:**
- Focus on highest-value MA measures
- Reaches 11 measures ($1.0M-$1.5M value)
- Moves quickly to dashboard integration

**Cons:**
- Incomplete Tier 3 (3/6 measures)
- Missing some clinical domain coverage

---

### Option C.3: Proceed Directly to Option A (Dashboard Integration)
**Pros:**
- Showcase existing 9 measures ($900K-$1.4M) immediately
- Live demo ready for job applications
- Can add Tier 3 measures later

**Cons:**
- Portfolio only 60% complete (9/15 measures)
- Misses opportunity to demonstrate full clinical breadth

---

## 9. Recommendation

**RECOMMENDED:** **Option C.2** (Implement FLU + COL, then proceed to Dashboard Integration)

**Rationale:**
1. **FLU** is easy to implement (3 hours) and has high gap closure potential
2. **COL** is highest-value Tier 3 measure ($100K-$150K)
3. Brings total to **11 measures** with **$1.0M-$1.5M** value
4. Allows proceeding to dashboard integration while maintaining strong portfolio
5. AWC/WCC can be added later (minimal MA applicability)

**Adjusted Timeline:**
- FLU implementation: 3 hours
- COL implementation: 7 hours
- **Total: 10 hours** (vs 22 hours for full Tier 3)
- Then proceed to **Option A: Dashboard Integration**

---

## 10. Next Steps

### Immediate Actions (User Decision Required)

**Choice 1:** Complete all 6 Tier 3 measures (22 hours) ← Comprehensive but slower  
**Choice 2:** Implement FLU + COL only (10 hours) ← **Recommended** (balanced)  
**Choice 3:** Proceed directly to Option A ← Fastest to live demo

**Please advise which path to take!**

---

## 11. Sign-Off

**Option C Status:** 🚧 **17% COMPLETE** (BCS implemented)  
**Tier 3 Value:** **$440K-$660K** (full implementation)  
**Combined Value:** **$1.3M-$2.1M** (Tier 1+2+3)

**Completed By:** AI Analytics Team  
**Date:** October 25, 2025  
**Awaiting:** User decision on implementation path

---

**End of Tier 3 Expansion Plan**

