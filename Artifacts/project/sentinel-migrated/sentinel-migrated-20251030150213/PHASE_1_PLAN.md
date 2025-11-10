# Phase 1: Tier 1 Diabetes Portfolio Implementation

**Status:** In Progress  
**Started:** October 23, 2025  
**Estimated Duration:** 2-3 weeks  
**Portfolio Value:** $720K-$1.23M

---

## 📋 Tier 1 Diabetes Measures (5 Total)

| Code | Measure | Weight | Status | Value |
|------|---------|--------|--------|-------|
| GSD | Glycemic Status Assessment | 3x | ✅ Production (AUC 0.91) | $360-615K |
| KED | Kidney Health Evaluation | 3x | 🔨 In Development | $360-615K |
| EED | Eye Exam for Diabetes | 1x | 📝 Planned | $120-205K |
| PDC-DR | Medication Adherence (Diabetes) | 1x | 📝 Planned | $120-205K |
| BPD | Blood Pressure Control (Diabetes) | 1x | 📝 Planned | $120-205K |

**NEW 2025 Measures:** KED, BPD

---

## 🎯 Phase 1 Objectives

### 1.1 Implement KED (Kidney Health Evaluation) - Triple-Weighted
- **Value:** $360-615K
- **NEW 2025 measure** - Critical for portfolio
- **Requirements:**
  - eGFR lab test (LOINC codes)
  - ACR/Urine albumin test (LOINC codes)
  - Diabetes threat assessment (ICD-10)
  - Age 18-75
- **Data Sources:** Claims, Labs
- **Target AUC:** 0.85+

### 1.2 Implement EED (Eye Exam for Diabetes)
- **Value:** $120-205K
- **Requirements:**
  - Retinal or dilated eye exam (CPT codes)
  - Diabetes threat assessment (ICD-10)
  - Negative retinopathy screening (exclusion)
  - Age 18-75
- **Data Sources:** Claims, Procedure codes
- **Target AUC:** 0.85+

### 1.3 Implement PDC-DR (Medication Adherence - Diabetes)
- **Value:** $120-205K
- **Requirements:**
  - Diabetes medication fills (NDC codes)
  - Proportion of Days Covered ≥80%
  - Diabetes threat assessment (ICD-10)
  - Age 18-75
- **Data Sources:** Pharmacy claims
- **Target AUC:** 0.85+

### 1.4 Implement BPD (Blood Pressure Control - Diabetes)
- **Value:** $120-205K
- **NEW 2025 measure**
- **Requirements:**
  - BP reading <140/90 mmHg
  - Diabetes threat assessment (ICD-10)
  - Vitals/encounter data
  - Age 18-75
- **Data Sources:** Claims, Vitals
- **Target AUC:** 0.85+

---

## 🏗️ Implementation Tasks

### Task 1: Data Loaders (src/data/loaders/)
- [ ] `labs_loader.py` - Lab results (eGFR, ACR, HbA1c)
- [ ] `pharmacy_loader.py` - Medication fills (NDC codes)
- [ ] `vitals_loader.py` - Blood pressure readings
- [ ] `procedure_loader.py` - Eye exams (CPT codes)

### Task 2: Feature Engineering (src/data/features/)
- [ ] `diabetes_features.py` - Shared diabetes features
  - Diabetes threat assessment indicators
  - Comorbidity flags (CKD, CVD, retinopathy)
  - Utilization patterns
  - Demographics
  - SDOH factors

### Task 3: Measure Implementations (src/measures/)
- [ ] `ked.py` - Kidney Health Evaluation
  - Denominator: Diabetes dx + age 18-75
  - Numerator: eGFR + ACR in measurement year
  - Exclusions: ESRD, kidney transplant
- [ ] `eed.py` - Eye Exam for Diabetes
  - Denominator: Diabetes dx + age 18-75
  - Numerator: Retinal exam in measurement year
  - Exclusions: Bilateral eye enucleation
- [ ] `pdc_dr.py` - Medication Adherence
  - Denominator: 2+ diabetes med fills
  - Numerator: PDC ≥80%
  - Exclusions: None
- [ ] `bpd.py` - Blood Pressure Control
  - Denominator: Diabetes dx + age 18-75
  - Numerator: Most recent BP <140/90
  - Exclusions: Frailty, advanced illness

### Task 4: Models
- [ ] Train KED prediction model
- [ ] Train EED prediction model
- [ ] Train PDC-DR prediction model
- [ ] Train BPD prediction model

### Task 5: Evaluation & Testing
- [ ] Unit tests for each measure
- [ ] Integration tests for portfolio
- [ ] Performance evaluation (AUC, precision, recall)
- [ ] Star rating simulation
- [ ] ROI analysis

### Task 6: Documentation
- [ ] Measure specifications
- [ ] Feature documentation
- [ ] Model performance reports
- [ ] Phase 1 completion summary

---

## 📊 Success Criteria

| Criterion | Target | Status |
|-----------|--------|--------|
| All 4 measures implemented | 4/4 | 🔨 In Progress |
| AUC ≥ 0.85 for each measure | 4/4 | Pending |
| Portfolio Star Rating calculator | Working | Pending |
| Data loaders functional | 4/4 | Pending |
| Feature engineering complete | Diabetes features | Pending |
| Tests passing | 100% | Pending |
| Documentation complete | All measures | Pending |

---

## 🚀 Quick Start

### Step 1: Implement KED (Triple-Weighted Priority)
```bash
# Create KED measure implementation
python src/measures/ked.py

# Create labs loader
python src/data/loaders/labs_loader.py

# Train KED model
python scripts/train_ked_model.py
```

### Step 2: Implement Remaining Measures
- EED (eye exams)
- PDC-DR (medication adherence)
- BPD (blood pressure)

### Step 3: Portfolio Integration
```bash
# Calculate Tier 1 portfolio performance
python scripts/calculate_tier1_portfolio.py

# Generate performance report
python scripts/generate_phase1_report.py
```

---

## 💰 Expected ROI

### Tier 1 Diabetes Portfolio Value
- **GSD (Production):** $360-615K
- **KED (3x weight):** $360-615K
- **EED:** $120-205K
- **PDC-DR:** $120-205K
- **BPD:** $120-205K
- **Total Tier 1:** $1.08M-$1.85M

### Improvement Assumptions
- 10-20% gap closure from predictive targeting
- $150 average intervention cost per individual
- 3:1 ROI target

### Risk Mitigation
- Two triple-weighted measures (GSD, KED)
- NEW 2025 measures get early attention
- Comprehensive diabetes management approach
- Shared population optimization

---

## 📝 Notes

### Data Requirements
- **Minimum:** 12 months lookback for threat assessment
- **Ideal:** 24 months for pattern analysis
- **Synthetic data available:** Yes (for development)

### Integration with Existing GSD Model
- Leverage existing diabetes identification logic
- Share feature engineering pipeline
- Portfolio-level optimization opportunities
- Cross-measure subject identification

### NEW 2025 Measures Priority
- **KED** - Triple-weighted, must launch strong
- **BPD** - Additional diabetes measure, builds on vitals infrastructure

---

**Next Step:** Start with KED implementation (highest value, triple-weighted, NEW 2025)



---
*This file is maintained by Sentinel Analytics. For inquiries, contact reichert.sentinel.ai@gmail.com.*
