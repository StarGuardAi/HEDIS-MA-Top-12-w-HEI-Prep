# HEDIS Multi-Measure Portfolio Expansion Plan

## 🎯 Executive Summary

**Current State:** HEDIS GSD Prediction Engine (single measure)
**Target State:** HEDIS Star Rating Portfolio Optimizer (12 measures across 4 tiers)
**Estimated Value Impact:** $1.67M - $2.68M direct Star revenue + $20-40M HEI at risk
**Timeline:** 8-10 weeks (phased approach)

---

## 📊 PROJECT RE-TITLING

### Recommended New Names (Choose One)

1. **HEDIS Star Rating Portfolio Optimizer** ⭐ RECOMMENDED
   - Professional, strategic focus
   - Emphasizes ROI and business value
   - Clear differentiation from single-measure tools

2. **Multi-Measure HEDIS Prediction Engine**
   - Clear evolution from current name
   - Technical focus
   - Easy to understand

3. **HEDIS Quality Measures Intelligence Platform**
   - Enterprise-level branding
   - Positions as comprehensive solution
   - Forward-looking

**Decision Needed:** Which naming convention do you prefer?

---

## 🏗️ ARCHITECTURAL STRATEGY

### Current Architecture (GSD-Only)
```
src/
├── data/
│   ├── data_loader.py          # CMS claims only
│   ├── feature_engineering.py  # GSD features only
│   └── data_preprocessing.py
├── models/
│   ├── trainer.py              # Single model
│   └── predictor.py            # Single prediction
```

### Target Architecture (12 Measures)
```
src/
├── data/
│   ├── loaders/                # NEW: Measure-specific loaders
│   │   ├── claims_loader.py
│   │   ├── pharmacy_loader.py
│   │   ├── lab_loader.py
│   │   └── screening_loader.py
│   ├── features/               # NEW: Measure-specific features
│   │   ├── diabetes_features.py
│   │   ├── cardiovascular_features.py
│   │   ├── cancer_screening_features.py
│   │   └── health_equity_features.py
│   └── preprocessing.py
├── measures/                   # NEW: Measure definitions
│   ├── tier1_diabetes.py
│   ├── tier2_cardiovascular.py
│   ├── tier3_cancer_screening.py
│   └── tier4_health_equity.py
├── models/
│   ├── multi_measure_trainer.py  # NEW: Portfolio training
│   ├── measure_predictor.py      # NEW: Measure-specific
│   └── portfolio_optimizer.py    # NEW: Portfolio optimization
├── api/                        # Phase 2: Multi-measure API
│   ├── endpoints/
│   │   ├── diabetes.py
│   │   ├── cardiovascular.py
│   │   ├── cancer_screening.py
│   │   └── portfolio.py
└── utils/
    ├── hedis_specs.py          # NEW: HEDIS specifications
    └── star_calculator.py      # NEW: Star rating calculator
```

---

## 📋 12-MEASURE PORTFOLIO DETAILS

### TIER 1: Diabetes Core (5 measures) - $720K-$1.23M

#### ✅ GSD - Glycemic Status Assessment [3x weighted]
- **Current:** ✅ IMPLEMENTED (AUC-ROC = 0.91)
- **Action:** Enhance with 2025 HEDIS updates
- **Data:** Claims, lab results (HbA1c)

#### 🆕 KED - Kidney Health Evaluation [3x weighted] (NEW 2025)
- **Action:** NEW IMPLEMENTATION
- **Data:** Claims, lab results (eGFR, ACR/urine albumin)
- **Features:** eGFR trends, medication adherence (ACE/ARB), nephrology visits
- **HEDIS Spec:** MY2025 Volume 2 (new measure)

#### 🔄 EED - Eye Exam for Diabetes
- **Action:** NEW IMPLEMENTATION
- **Data:** Claims (CPT codes for retinal exams)
- **Features:** Last exam date, exam frequency, retinopathy diagnosis history
- **HEDIS Spec:** MY2023 Volume 2

#### 🔄 PDC-DR - Medication Adherence for Diabetes
- **Action:** NEW IMPLEMENTATION
- **Data:** Pharmacy claims (diabetes medications)
- **Features:** PDC calculation, gaps in therapy, med switches
- **HEDIS Spec:** MY2023 Volume 2 (PDC ≥ 80% = adherent)

#### 🆕 BPD - Blood Pressure Control for Diabetes (NEW 2025)
- **Action:** NEW IMPLEMENTATION
- **Data:** Claims, vitals (BP readings)
- **Features:** BP trends, HTN diagnosis, medication adherence
- **HEDIS Spec:** MY2025 Volume 2 (BP <140/90)

---

### TIER 2: Cardiovascular Comorbidity (4 measures) - $650K-$1M

#### 🔄 CBP - Controlling High Blood Pressure [3x weighted]
- **Action:** NEW IMPLEMENTATION
- **Data:** Claims, vitals (BP readings)
- **Features:** BP trends, HTN diagnosis, medication classes
- **HEDIS Spec:** MY2023 Volume 2 (BP <140/90)

#### 🔄 SUPD - Statin Therapy for Patients with Diabetes
- **Action:** NEW IMPLEMENTATION
- **Data:** Claims, pharmacy (statin prescriptions)
- **Features:** Statin type, dosage, adherence, ASCVD risk
- **HEDIS Spec:** MY2023 Volume 2

#### 🔄 PDC-RASA - Medication Adherence for Hypertension
- **Action:** NEW IMPLEMENTATION
- **Data:** Pharmacy claims (ACE/ARB/RASA medications)
- **Features:** PDC calculation, therapy gaps, switches
- **HEDIS Spec:** MY2023 Volume 2 (PDC ≥ 80%)

#### 🔄 PDC-STA - Medication Adherence for Cholesterol
- **Action:** NEW IMPLEMENTATION
- **Data:** Pharmacy claims (statins)
- **Features:** PDC calculation, statin potency, switches
- **HEDIS Spec:** MY2023 Volume 2 (PDC ≥ 80%)

---

### TIER 3: Cancer Screening (2 measures) - $300-450K

#### 🔄 BCS - Breast Cancer Screening
- **Action:** NEW IMPLEMENTATION
- **Data:** Claims (mammography CPT codes)
- **Features:** Last mammogram date, screening history, age group
- **HEDIS Spec:** MY2023 Volume 2 (women 50-74)

#### 🔄 COL - Colorectal Cancer Screening
- **Action:** NEW IMPLEMENTATION
- **Data:** Claims (colonoscopy, FIT, Cologuard CPT codes)
- **Features:** Last screening date, screening type, age group
- **HEDIS Spec:** MY2023 Volume 2 (ages 50-75)

---

### TIER 4: The 2027 Game-Changer - $20-40M at risk

#### 🆕 HEI - Health Equity Index Reward Factor
- **Action:** NEW IMPLEMENTATION (CRITICAL)
- **Data:** All measures above + SDOH data
- **Features:** Dual-eligible status, LIS, disability, race/ethnicity
- **HEDIS Spec:** MY2027 (starts 2025 measurement)
- **Impact:** 5% Star bonus or penalty

---

## 🚀 IMPLEMENTATION PHASES

### Phase 0: Foundation Refactoring (Week 1)
**Goal:** Refactor current GSD code to support multi-measure architecture

- [ ] **0.1: Project Renaming**
  - [ ] Update `README.md` with new project name
  - [ ] Update `setup.py` metadata
  - [ ] Update all docstrings and comments
  - [ ] Update GitHub repository name and description
  - [ ] Update LinkedIn/portfolio materials

- [ ] **0.2: Architecture Refactoring**
  - [ ] Create `src/measures/` package structure
  - [ ] Create `src/data/loaders/` for data source types
  - [ ] Create `src/data/features/` for measure-specific features
  - [ ] Move existing GSD code to new structure
  - [ ] Create `src/utils/hedis_specs.py` with measure definitions
  - [ ] Create `src/utils/star_calculator.py` for Star rating logic

- [ ] **0.3: Configuration Enhancement**
  - [ ] Add multi-measure configuration to `config.yaml`
  - [ ] Define measure registry with specifications
  - [ ] Add Star rating weights (1x, 3x)
  - [ ] Add HEI configuration

- [ ] **0.4: Testing Framework Update**
  - [ ] Update unit tests for refactored structure
  - [ ] Create measure-specific test fixtures
  - [ ] Add portfolio-level integration tests

**Success Criteria:**
- ✅ GSD code works in new architecture
- ✅ All existing tests pass
- ✅ Multi-measure configuration complete
- ✅ Documentation updated

---

### Phase 1: Diabetes Portfolio (Weeks 2-3)
**Goal:** Complete all 5 Tier 1 diabetes measures

#### 1.1: Data Loader Enhancement
- [ ] Extend `claims_loader.py` for additional diabetes data
- [ ] Create `lab_loader.py` for HbA1c, eGFR, ACR data
- [ ] Create `pharmacy_loader.py` for medication claims
- [ ] Create `vitals_loader.py` for BP readings

#### 1.2: KED - Kidney Health Evaluation (NEW 2025)
- [ ] Define KED measure specifications
- [ ] Create `diabetes_features.py::create_ked_features()`
- [ ] Implement eGFR calculation logic
- [ ] Add ACE/ARB medication features
- [ ] Train KED prediction model
- [ ] Run healthcare code reviews

#### 1.3: EED - Eye Exam for Diabetes
- [ ] Define EED measure specifications
- [ ] Create `diabetes_features.py::create_eed_features()`
- [ ] Extract retinal exam CPT codes
- [ ] Calculate exam frequency features
- [ ] Train EED prediction model
- [ ] Run healthcare code reviews

#### 1.4: PDC-DR - Medication Adherence (Diabetes)
- [ ] Define PDC-DR measure specifications
- [ ] Create `diabetes_features.py::create_pdc_dr_features()`
- [ ] Implement PDC calculation (days covered / days in period)
- [ ] Identify therapy gaps and switches
- [ ] Train PDC-DR prediction model
- [ ] Run healthcare code reviews

#### 1.5: BPD - Blood Pressure Control (Diabetes) (NEW 2025)
- [ ] Define BPD measure specifications
- [ ] Create `diabetes_features.py::create_bpd_features()`
- [ ] Calculate BP control rates (<140/90)
- [ ] Add HTN medication features
- [ ] Train BPD prediction model
- [ ] Run healthcare code reviews

**Deliverables:**
- ✅ 5 diabetes measure models trained
- ✅ `src/data/features/diabetes_features.py` complete
- ✅ `src/measures/tier1_diabetes.py` with all 5 measures
- ✅ All healthcare code reviews passed

**Value:** $720K-$1.23M direct Star revenue

---

### Phase 2: Cardiovascular Portfolio (Weeks 4-5)
**Goal:** Complete all 4 Tier 2 cardiovascular measures

#### 2.1: CBP - Controlling High Blood Pressure [3x weighted]
- [ ] Define CBP measure specifications
- [ ] Create `cardiovascular_features.py::create_cbp_features()`
- [ ] Extract BP vitals from claims
- [ ] Calculate BP control rates
- [ ] Train CBP prediction model
- [ ] Run healthcare code reviews

#### 2.2: SUPD - Statin Therapy for Diabetes
- [ ] Define SUPD measure specifications
- [ ] Create `cardiovascular_features.py::create_supd_features()`
- [ ] Identify statin prescriptions
- [ ] Calculate ASCVD risk features
- [ ] Train SUPD prediction model
- [ ] Run healthcare code reviews

#### 2.3: PDC-RASA - Medication Adherence (Hypertension)
- [ ] Define PDC-RASA measure specifications
- [ ] Create `cardiovascular_features.py::create_pdc_rasa_features()`
- [ ] Implement PDC calculation for ACE/ARB/RASA
- [ ] Identify therapy gaps
- [ ] Train PDC-RASA prediction model
- [ ] Run healthcare code reviews

#### 2.4: PDC-STA - Medication Adherence (Cholesterol)
- [ ] Define PDC-STA measure specifications
- [ ] Create `cardiovascular_features.py::create_pdc_sta_features()`
- [ ] Implement PDC calculation for statins
- [ ] Add statin potency features
- [ ] Train PDC-STA prediction model
- [ ] Run healthcare code reviews

**Deliverables:**
- ✅ 4 cardiovascular measure models trained
- ✅ `src/data/features/cardiovascular_features.py` complete
- ✅ `src/measures/tier2_cardiovascular.py` with all 4 measures
- ✅ All healthcare code reviews passed

**Value:** $650K-$1M direct Star revenue

---

### Phase 3: Cancer Screening Portfolio (Week 6)
**Goal:** Complete all 2 Tier 3 cancer screening measures

#### 3.1: BCS - Breast Cancer Screening
- [ ] Define BCS measure specifications
- [ ] Create `cancer_screening_features.py::create_bcs_features()`
- [ ] Extract mammography CPT codes
- [ ] Calculate screening adherence
- [ ] Train BCS prediction model
- [ ] Run healthcare code reviews

#### 3.2: COL - Colorectal Cancer Screening
- [ ] Define COL measure specifications
- [ ] Create `cancer_screening_features.py::create_col_features()`
- [ ] Extract colonoscopy, FIT, Cologuard CPT codes
- [ ] Calculate screening adherence
- [ ] Train COL prediction model
- [ ] Run healthcare code reviews

**Deliverables:**
- ✅ 2 cancer screening measure models trained
- ✅ `src/data/features/cancer_screening_features.py` complete
- ✅ `src/measures/tier3_cancer_screening.py` with both measures
- ✅ All healthcare code reviews passed

**Value:** $300-450K direct Star revenue

---

### Phase 4: Health Equity Index (Week 7)
**Goal:** Implement HEI reward factor calculation

#### 4.1: HEI Data Collection
- [ ] Define HEI data requirements (SDOH, dual-eligible, LIS, disability)
- [ ] Create `src/data/loaders/sdoh_loader.py`
- [ ] Extract race/ethnicity data (with HIPAA compliance)
- [ ] Extract dual-eligible and LIS flags
- [ ] Create `health_equity_features.py`

#### 4.2: HEI Calculation
- [ ] Implement HEI reward factor calculation
- [ ] Calculate measure performance by underserved populations
- [ ] Implement HEI scoring logic (5% bonus/penalty)
- [ ] Create HEI reporting dashboard

#### 4.3: Disparity Analysis
- [ ] Analyze performance gaps across populations
- [ ] Identify high-disparity measures
- [ ] Create intervention targeting logic
- [ ] Run healthcare code reviews (focus on bias)

**Deliverables:**
- ✅ `src/data/features/health_equity_features.py` complete
- ✅ `src/measures/tier4_health_equity.py` with HEI calculation
- ✅ HEI reporting and disparity analysis
- ✅ All healthcare code reviews passed (bias analysis)

**Value:** $20-40M at risk (5% of total Star revenue)

---

### Phase 5: Portfolio Optimization (Week 8)
**Goal:** Implement portfolio-level optimization and ROI analysis

#### 5.1: Multi-Measure Training Pipeline
- [ ] Create `multi_measure_trainer.py`
- [ ] Implement parallel model training for all 12 measures
- [ ] Add cross-measure feature sharing
- [ ] Implement ensemble methods across measures

#### 5.2: Portfolio Predictor
- [ ] Create `portfolio_optimizer.py`
- [ ] Implement member-level risk scoring across all measures
- [ ] Calculate intervention ROI by measure
- [ ] Prioritize interventions by Star impact

#### 5.3: Star Rating Calculator
- [ ] Implement Star rating calculation logic
- [ ] Add measure weights (1x vs 3x)
- [ ] Calculate expected Star revenue by measure
- [ ] Create Star impact forecasting

#### 5.4: Portfolio Dashboard
- [ ] Create portfolio-level metrics
- [ ] Build measure comparison visualizations
- [ ] Add ROI and Star revenue projections
- [ ] Create executive summary reports

**Deliverables:**
- ✅ `src/models/multi_measure_trainer.py` complete
- ✅ `src/models/portfolio_optimizer.py` complete
- ✅ `src/utils/star_calculator.py` complete
- ✅ Portfolio dashboard and reporting
- ✅ All healthcare code reviews passed

**Value:** $1.67M - $2.68M total portfolio value + $20-40M HEI

---

## 🔧 DATA REQUIREMENTS

### Current Data (CMS DE-SynPUF)
- ✅ Beneficiary summary (demographics)
- ✅ Inpatient claims
- ✅ Outpatient claims
- ✅ Carrier claims

### Additional Data Needed

#### Lab Results
- HbA1c values and dates
- eGFR values and trends
- ACR/urine albumin results
- Lipid panels (LDL, HDL, total cholesterol)

#### Pharmacy Claims
- NDC codes for medications
- Fill dates and days supply
- Statin prescriptions
- ACE/ARB/RASA prescriptions
- Diabetes medications

#### Vitals
- Blood pressure readings (systolic/diastolic)
- Reading dates and locations

#### Screening Procedures
- Mammography CPT codes and dates
- Colonoscopy/FIT/Cologuard CPT codes and dates
- Retinal exam CPT codes and dates

#### SDOH Data (for HEI)
- Dual-eligible status
- Low-Income Subsidy (LIS) status
- Disability status
- Race/ethnicity (HIPAA-compliant)

**Question:** Do you have access to this additional data, or should we use synthetic data for demonstration?

---

## 📊 CONFIGURATION STRUCTURE

### New `config.yaml` Structure

```yaml
# Project Metadata
project:
  name: "HEDIS Star Rating Portfolio Optimizer"
  version: "2.0.0"
  measurement_year: 2025

# Measure Registry
measures:
  # Tier 1: Diabetes Core
  GSD:
    name: "Glycemic Status Assessment"
    tier: 1
    weight: 3  # Triple-weighted
    target_population: "diabetes"
    data_sources: ["claims", "labs"]
    status: "production"
  
  KED:
    name: "Kidney Health Evaluation"
    tier: 1
    weight: 3  # Triple-weighted
    target_population: "diabetes"
    data_sources: ["claims", "labs"]
    status: "new_2025"
  
  EED:
    name: "Eye Exam for Diabetes"
    tier: 1
    weight: 1
    target_population: "diabetes"
    data_sources: ["claims"]
    status: "development"
  
  PDC_DR:
    name: "Medication Adherence - Diabetes"
    tier: 1
    weight: 1
    target_population: "diabetes"
    data_sources: ["pharmacy"]
    status: "development"
  
  BPD:
    name: "Blood Pressure Control - Diabetes"
    tier: 1
    weight: 1
    target_population: "diabetes"
    data_sources: ["claims", "vitals"]
    status: "new_2025"
  
  # Tier 2: Cardiovascular
  CBP:
    name: "Controlling High Blood Pressure"
    tier: 2
    weight: 3  # Triple-weighted
    target_population: "hypertension"
    data_sources: ["claims", "vitals"]
    status: "development"
  
  SUPD:
    name: "Statin Therapy - Diabetes"
    tier: 2
    weight: 1
    target_population: "diabetes_cvd"
    data_sources: ["claims", "pharmacy"]
    status: "development"
  
  PDC_RASA:
    name: "Medication Adherence - Hypertension"
    tier: 2
    weight: 1
    target_population: "hypertension"
    data_sources: ["pharmacy"]
    status: "development"
  
  PDC_STA:
    name: "Medication Adherence - Cholesterol"
    tier: 2
    weight: 1
    target_population: "hyperlipidemia"
    data_sources: ["pharmacy"]
    status: "development"
  
  # Tier 3: Cancer Screening
  BCS:
    name: "Breast Cancer Screening"
    tier: 3
    weight: 1
    target_population: "women_50_74"
    data_sources: ["claims"]
    status: "development"
  
  COL:
    name: "Colorectal Cancer Screening"
    tier: 3
    weight: 1
    target_population: "ages_50_75"
    data_sources: ["claims"]
    status: "development"
  
  # Tier 4: Health Equity
  HEI:
    name: "Health Equity Index"
    tier: 4
    weight: "5%"  # 5% bonus/penalty
    target_population: "all"
    data_sources: ["all_measures", "sdoh"]
    status: "critical_2027"

# Star Rating Configuration
star_rating:
  triple_weighted_measures: ["GSD", "KED", "CBP"]
  total_possible_points: 100
  hei_bonus_max: 5  # 5% bonus
  hei_penalty_max: -5  # 5% penalty

# ROI Configuration
roi:
  star_revenue_per_point: 50000  # $50K per 0.1 Star point
  intervention_cost_per_member: 150  # Average cost
  target_roi: 3.0  # 3:1 ROI target
```

---

## 🎯 SUCCESS METRICS

### Technical Metrics
- **Model Performance:** AUC-ROC ≥ 0.85 for all measures
- **Portfolio Coverage:** All 12 measures operational
- **API Performance:** < 200ms response time for portfolio predictions
- **Test Coverage:** ≥ 90% code coverage
- **Healthcare Compliance:** 100% reviews passed

### Business Metrics
- **Star Revenue Impact:** $1.67M - $2.68M annual
- **HEI Risk Mitigation:** Prevent $20-40M penalty
- **Intervention ROI:** ≥ 3:1 return on intervention costs
- **Member Reach:** Predict risk for 100% of eligible population
- **Gap Closure Rate:** ≥ 15% improvement in measure rates

---

## 🔍 HEALTHCARE CODE REVIEWS

### Review Requirements for Each Measure

**For ALL measure code:**
```
/review-security [filename]
/review-hipaa [filename]
/review-performance [filename]
/review-clinical-logic [filename]
```

**For pharmacy/PDC measures:**
```
/review-data-quality [filename]  # NDC validation, fill date logic
```

**For HEI code:**
```
/review-model-code [filename]  # Bias detection critical
```

---

## 📞 NEXT STEPS

### Immediate Actions (This Week)

1. **Review this expansion plan** and provide feedback
2. **Answer key questions:**
   - Preferred project name?
   - Do you have access to pharmacy, lab, vitals, screening data?
   - Should we use synthetic data for demonstration?
   - Timeline preferences (8-10 weeks realistic?)
3. **Approve Phase 0** (Foundation Refactoring) to begin
4. **Prioritize measures** if we need to implement in stages

### Long-Term Roadmap

**Phase 6 (Week 9-10):** API Development
- Multi-measure REST API
- Portfolio-level endpoints
- Batch prediction capabilities
- Interactive dashboard

**Phase 7 (Week 11-12):** Deployment & Operations
- Containerization (Docker)
- CI/CD pipeline
- Monitoring and alerting
- Production deployment

---

## 💰 BUSINESS VALUE SUMMARY

### Direct Star Revenue Impact
| Tier | Measures | Value Range | Status |
|------|----------|-------------|--------|
| Tier 1 | 5 diabetes | $720K - $1.23M | 1 implemented, 4 new |
| Tier 2 | 4 cardiovascular | $650K - $1M | All new |
| Tier 3 | 2 cancer screening | $300K - $450K | All new |
| **TOTAL** | **11 measures** | **$1.67M - $2.68M** | - |

### Health Equity Index Impact
- **HEI Risk:** $20-40M at risk (5% of total Star revenue)
- **Timeline:** Starts MY2025, mandatory MY2027
- **Strategy:** Proactive disparity reduction

### Total Portfolio Value
- **Best Case:** $2.68M direct + $20-40M HEI protection = **$22.68M - $42.68M**
- **ROI:** Estimated 10-15:1 return on development investment

---

## ✅ DECISION CHECKLIST

Before proceeding, please confirm:

- [ ] Approve overall expansion strategy
- [ ] Choose project name (see options in Section 2)
- [ ] Confirm data availability or synthetic data approach
- [ ] Review timeline (8-10 weeks)
- [ ] Approve Phase 0 to begin refactoring
- [ ] Prioritize measure implementation order (or follow Tier 1→4)

**Ready to transform your single-measure engine into a comprehensive portfolio optimizer?**

Let me know your decisions and I'll begin Phase 0 immediately! 🚀

