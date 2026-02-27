# TIER 3: Cancer Screening Portfolio Implementation Plan

**Status:** STARTING NOW  
**Timeline:** 2-3 hours (pattern-based, very fast)  
**Expected Value:** +$300K-$450K/year  
**Total Portfolio:** 11 measures, $2.1M-$2.8M/year

---

## 🎯 Overview

**Goal:** Implement 2 cancer screening measures to expand portfolio coverage

**Measures:**
1. **BCS** - Breast Cancer Screening (mammography)
2. **COL** - Colorectal Cancer Screening (colonoscopy/FIT/Cologuard)

**Why Fast:**
- ✅ Proven architecture established
- ✅ Pattern to copy (EED eye exam similar)
- ✅ Screening data loader exists (procedure_loader.py)
- ✅ Simple numerator/denominator logic
- ✅ No complex calculations (PDC, BP, labs)

**Expected Time:** 2-3 hours total

---

## 📊 Measure Details

### 1. BCS - Breast Cancer Screening

**Criminal Intelligence Database Specification:** MY2023 Volume 2  
**Star Rating Weight:** 1x  
**Annual Value:** $150K-$225K (100K individual plan)

**Population:**
- Women ages 50-74
- Continuous enrollment in measurement year
- At least one outpatient encounter

**Numerator:**
- At least one mammography in measurement year or year prior
- CPT codes: 77065-77067 (digital mammography)

**Denominator:**
- Women 50-74 as of December 31
- Exclude: Bilateral mastectomy, hospice

**Complexity:** LOW
- Simple age/gender filtering
- Procedure code lookup (CPT)
- 2-year lookback (measurement year + prior)
- Minimal exclusions

**Reuse:**
- `procedure_loader.py` (exists from EED)
- Population filtering pattern (from all measures)
- Simple compliance check (has procedure = yes/no)

**Development Time:** 45-60 minutes

---

### 2. COL - Colorectal Cancer Screening

**Criminal Intelligence Database Specification:** MY2023 Volume 2  
**Star Rating Weight:** 1x  
**Annual Value:** $150K-$225K (100K individual plan)

**Population:**
- Adults ages 50-75 (both genders)
- Continuous enrollment in measurement year
- At least one outpatient encounter

**Numerator (Multiple Options):**
- Colonoscopy in past 10 years
- FIT (fecal immunochemical test) annually
- Cologuard (FIT-DNA) every 3 years
- Flexible sigmoidoscopy every 5 years

**Denominator:**
- Adults 50-75 as of December 31
- Exclude: Total colectomy, hospice

**Complexity:** MEDIUM
- Multiple screening modalities (different lookback periods)
- 10-year lookback for colonoscopy
- Annual for FIT
- 3-year for Cologuard
- Procedure code lookup (CPT)

**Reuse:**
- `procedure_loader.py` (exists)
- Multi-year lookback logic (from EED 2-year)
- Population filtering pattern

**Development Time:** 60-75 minutes

---

## 🏗️ Implementation Strategy

### Phase 3.1: Cancer Screening Features (30-45 min)

**Create:** `src/data/features/cancer_screening_features.py`

**Features (15-20):**

**Demographic Features (5):**
- Age at measurement year end
- Gender
- Years enrolled
- Outpatient encounters count
- Has PCP assignment

**Screening History Features (5):**
- Last mammography date (BCS)
- Mammography frequency (annual, biennial)
- Last colonoscopy date (COL)
- Last FIT date (COL)
- Last Cologuard date (COL)

**Risk Factors (5):**
- Family history of cancer
- Personal cancer history
- High-risk conditions
- Screening refusal history
- Barriers to screening (geographic, etc.)

**Shared Features (5):**
- Age group (50-64, 65-75)
- Preventive visit history
- Healthcare utilization
- Specialist visits (oncology, gastro)
- Screening compliance patterns

**Code:** ~400 lines (simple, mostly lookups)

---

### Phase 3.2: BCS Implementation (45-60 min)

**Create:** `src/measures/bcs.py` (~350 lines)

**Implementation Steps:**

1. **Define BCS Measure Class**
   ```python
   class BCSMeasure:
       def __init__(self, measurement_year: int = 2025)
       def calculate_age(self, birth_date) -> int
       def is_in_denominator(member_df, claims_df) -> Tuple[bool, str]
       def is_in_numerator(procedure_df) -> Tuple[bool, str]
       def calculate_member_status(...) -> Dict
       def calculate_population_rate(...) -> Dict
   ```

2. **Denominator Logic:**
   - Female gender
   - Age 50-74 (Dec 31)
   - Continuous enrollment
   - Exclusions: bilateral mastectomy, hospice

3. **Numerator Logic:**
   - Mammography CPT codes: 77065, 77066, 77067
   - Lookback: Current year + prior year (2 years)
   - Any one occurrence = compliant

4. **Gap List Generation:**
   - Priority: Age 60+ (higher risk)
   - Never screened > overdue > on schedule

**Pattern:** Copy from EED (very similar - procedure-based screening)

---

### Phase 3.3: COL Implementation (60-75 min)

**Create:** `src/measures/col.py` (~400 lines)

**Implementation Steps:**

1. **Define COL Measure Class**
   ```python
   class COLMeasure:
       def __init__(self, measurement_year: int = 2025)
       def is_in_denominator(member_df, claims_df) -> Tuple[bool, str]
       def is_in_numerator_colonoscopy(procedure_df) -> bool
       def is_in_numerator_fit(procedure_df) -> bool
       def is_in_numerator_cologuard(procedure_df) -> bool
       def is_in_numerator(procedure_df) -> Tuple[bool, str]
       ...
   ```

2. **Denominator Logic:**
   - Both genders
   - Age 50-75 (Dec 31)
   - Continuous enrollment
   - Exclusions: total colectomy, hospice

3. **Numerator Logic (Multiple Paths):**
   - **Colonoscopy:** CPT 44388-44394, 45378-45398 (10-year lookback)
   - **FIT:** CPT 82270, 82274 (annual)
   - **Cologuard:** CPT 81528 (3-year lookback)
   - **Flexible sig:** CPT 45330-45347 (5-year lookback)
   - ANY one method = compliant

4. **Gap List Generation:**
   - Priority: Age 60+ (higher risk)
   - Never screened > overdue colonoscopy > FIT needed

**Pattern:** Copy from EED but with multiple modality checks

---

### Phase 3.4: Testing (30 min)

**Create Tests:**

1. `tests/data/test_cancer_screening_features.py` (~300 lines)
   - Feature extraction validation
   - Age/gender filtering
   - Screening history tracking

2. `tests/measures/test_bcs.py` (~250 lines)
   - Denominator criteria
   - Numerator (mammography detection)
   - Exclusions
   - 2-year lookback

3. `tests/measures/test_col.py` (~300 lines)
   - Multiple screening modalities
   - Different lookback periods
   - Colonoscopy 10-year
   - FIT annual
   - Cologuard 3-year

4. `tests/fixtures/synthetic_cancer_screening_data.py` (~200 lines)
   - Test scenarios for BCS
   - Test scenarios for COL
   - Various screening patterns

---

### Phase 3.5: Portfolio Integration (30 min)

**Update Portfolio Calculator:**

1. **Add to MEASURE_WEIGHTS:**
   ```python
   "BCS": 1.0,  # Standard
   "COL": 1.0,  # Standard
   ```

2. **Add to MEASURE_VALUES:**
   ```python
   "BCS": (150000, 225000),  # $150K-$225K
   "COL": (150000, 225000),  # $150K-$225K
   ```

3. **Add to TIER_3_MEASURES:**
   ```python
   TIER_3_MEASURES = {"BCS", "COL"}
   ```

4. **Update Documentation:**
   - Portfolio calculator docstring
   - Total measures: 11
   - Total value: $2.1M-$2.8M

---

## 📈 Expected Outcomes

### Portfolio Expansion

**Before Tier 3:**
- Measures: 9 (Tier 1 + Tier 2)
- Annual Value: $1.82M-$2.33M

**After Tier 3:**
- Measures: 11 (Tier 1 + Tier 2 + Tier 3)
- Annual Value: $2.12M-$2.78M (+$300K-$450K)

### Code Additions

**New Code:**
- Cancer screening features: ~400 lines
- BCS measure: ~350 lines
- COL measure: ~400 lines
- Tests: ~1,050 lines
- **Total:** ~2,200 lines

**Total Code Base After Tier 3:**
- Production: ~10,350 lines
- Tests: ~4,250 lines
- **Total:** ~14,600 lines

### Business Value

**Tier 3 Contribution:**
- BCS: $150K-$225K/year
- COL: $150K-$225K/year
- Total: $300K-$450K/year

**Combined Portfolio (11 measures):**
- Tier 1: $1.2M-$1.4M
- Tier 2: $620K-$930K
- Tier 3: $300K-$450K
- **Total: $2.12M-$2.78M/year**

**5-Year Impact:**
- Additional revenue: +$1.5M-$2.25M (Tier 3)
- Combined net benefit: $7.3M-$8M
- ROI: Still excellent (~200%+)

---

## 🎯 Success Criteria

### Technical
- ✅ BCS measure implemented (denominator, numerator, exclusions)
- ✅ COL measure implemented (all 4 modalities)
- ✅ Cancer screening features operational (15-20 features)
- ✅ Tests passing (all measure logic validated)
- ✅ Portfolio calculator updated (11 measures)

### Business
- ✅ Tier 3 value: $300K-$450K/year validated
- ✅ Combined portfolio: $2.1M-$2.8M/year
- ✅ Coverage expansion: Preventive care measures added
- ✅ Population reach: +15-20K additional members

### Timeline
- ✅ Phase 3.1: 45 min (features)
- ✅ Phase 3.2: 60 min (BCS)
- ✅ Phase 3.3: 75 min (COL)
- ✅ Phase 3.4: 30 min (tests)
- ✅ Phase 3.5: 30 min (integration)
- **Total: ~3.5 hours**

---

## 💡 Why This is Fast

### 1. Proven Architecture
- All infrastructure exists
- Data loaders ready
- Portfolio calculator scalable
- Testing framework established

### 2. Similar Pattern to EED
- BCS = eye exam pattern (procedure-based screening)
- COL = slightly more complex (multiple modalities)
- Both simpler than PDC measures (no adherence calc)
- Both simpler than BP/lab measures (no vitals/results)

### 3. Simple Logic
- Denominator: Age + gender filtering
- Numerator: "Has procedure in timeframe?"
- No complex calculations
- No multi-step algorithms

### 4. High Code Reuse
- procedure_loader.py exists
- Population filtering pattern proven
- Testing patterns established
- Documentation templates ready

---

## 🚀 Starting Now

**Phases:**
1. ⏳ Phase 3.1: Cancer screening features (starting)
2. ⏸️ Phase 3.2: BCS implementation
3. ⏸️ Phase 3.3: COL implementation
4. ⏸️ Phase 3.4: Testing
5. ⏸️ Phase 3.5: Portfolio integration

**Let's build Tier 3 and reach $2.1M-$2.8M/year portfolio value!** 🚀

---

## 📊 Final Portfolio Preview

```
TIER 1 (Diabetes):              $1.2M - $1.4M      (5 measures)
TIER 2 (Cardiovascular):        $620K - $930K      (4 measures)
TIER 3 (Cancer Screening):      $300K - $450K      (2 measures)
════════════════════════════════════════════════════════════
TOTAL 11-MEASURE PORTFOLIO:     $2.12M - $2.78M    ✅

Remaining:
TIER 4 (HEI + 1 measure):       $10M-$20M protection

FULL 12-MEASURE PORTFOLIO:      $13M - $27M potential
```

**Ready to implement!**



---
*This file is maintained by Sentinel Analytics. For inquiries, contact reichert.sentinel.ai@gmail.com.*
