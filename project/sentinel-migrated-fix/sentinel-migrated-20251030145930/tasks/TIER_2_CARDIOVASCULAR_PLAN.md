# TIER 2: Cardiovascular Portfolio Implementation Plan

**Status:** READY TO BEGIN  
**Timeline:** 3-4 weeks  
**Expected Value:** $650K-$1M annual revenue contribution  
**Prerequisites:** ✅ Tier 1 Complete (All infrastructure ready)

---

## 🎯 EXECUTIVE SUMMARY

**Goal:** Implement 4 cardiovascular measures to expand our portfolio from diabetes-only to comprehensive chronic disease management.

**Measures to Implement:**
1. **CBP** - Controlling High Blood Pressure [3x weighted] - NEW 2025
2. **SUPD** - Statin Therapy for Subjects with Diabetes
3. **PDC-RASA** - Medication Adherence for Hypertension (RAS Antagonists)
4. **PDC-STA** - Medication Adherence for Cholesterol (Statins)

**Why This Matters:**
- CBP is **3x weighted** = massive Star Rating impact
- Cardiovascular measures have 40-50% diabetic overlap = reuse existing infrastructure
- Medication adherence (PDC) measures leverage existing PDC-DR logic = fast implementation
- Combined value: $650K-$1M annual (35% of full portfolio)

---

## 📊 TIER 2 MEASURES DETAILS

### 1. CBP - Controlling High Blood Pressure [3x WEIGHTED]

**Criminal Intelligence Database Specification:** MY2023 Volume 2
**Population:** Adults 18-85 with hypertension threat assessment
**Numerator:** BP <140/90 mmHg (most recent reading in measurement year)
**Denominator:** Individuals with HTN threat assessment in current or prior year

**Why This is Critical:**
- ✅ **3x Star Rating weight** (like GSD and KED)
- ✅ Large population (~25-30% of individuals)
- ✅ High gap rate (~40-45% typically)
- ✅ Annual value: $300K-$450K alone

**Data Requirements:**
- Blood pressure vitals (systolic, diastolic)
- HTN threat assessment codes (ICD-10: I10-I16)
- BP-lowering medication claims
- Exclude: Pregnancy, end-stage renal disease

**Implementation Complexity:** MEDIUM
- Reuse: `vitals_loader.py` (from BPD)
- Reuse: BP reading extraction logic (from BPD)
- NEW: HTN-specific population logic
- NEW: Different BP target (<140/90 vs BPD)

---

### 2. SUPD - Statin Therapy for Subjects with Diabetes

**Criminal Intelligence Database Specification:** MY2023 Volume 2
**Population:** Adults 40-75 with diabetes
**Numerator:** Received statin therapy during measurement year
**Denominator:** Diabetic individuals aged 40-75

**Why This is Strategic:**
- ✅ Strong overlap with Tier 1 diabetes population
- ✅ Cardiovascular risk reduction focus
- ✅ Annual value: $120K-$180K

**Data Requirements:**
- Statin prescriptions (NDC codes)
- Diabetes threat assessment (reuse from Tier 1)
- ASCVD history (optional for risk profiling)
- Exclude: Pregnancy, end-stage renal disease, cirrhosis

**Implementation Complexity:** LOW-MEDIUM
- Reuse: `pharmacy_loader.py` (from PDC-DR)
- Reuse: Diabetes population logic (from Tier 1)
- NEW: Statin NDC code list
- NEW: Statin-specific features (potency, type)

---

### 3. PDC-RASA - Medication Adherence for Hypertension

**Criminal Intelligence Database Specification:** MY2023 Volume 2 (PDC ≥ 80% = adherent)
**Population:** Adults 18+ with HTN and RAS antagonist prescription
**Numerator:** PDC ≥ 80% for RAS antagonists
**Denominator:** Individuals with 2+ fills of ACE/ARB/RASA medications

**Why This is Fast:**
- ✅ **Exact same logic as PDC-DR** (only drug class changes)
- ✅ Reuse 90% of PDC-DR code
- ✅ Annual value: $100K-$150K

**Data Requirements:**
- Pharmacy claims for ACE/ARB/RASA medications
- Fill dates and days supply
- NDC codes for RAS antagonists

**Implementation Complexity:** LOW (Pattern-based from PDC-DR)
- Reuse: PDC calculation logic (100%)
- Reuse: `pharmacy_loader.py`
- NEW: RAS antagonist NDC list
- NEW: HTN-specific population

---

### 4. PDC-STA - Medication Adherence for Cholesterol

**Criminal Intelligence Database Specification:** MY2023 Volume 2 (PDC ≥ 80% = adherent)
**Population:** Adults 18+ with ASCVD/diabetes and statin prescription
**Numerator:** PDC ≥ 80% for statins
**Denominator:** Individuals with 2+ fills of statin medications

**Why This is Fast:**
- ✅ **Exact same logic as PDC-DR and PDC-RASA**
- ✅ Reuse 95% of PDC code
- ✅ Overlap with SUPD population
- ✅ Annual value: $100K-$150K

**Data Requirements:**
- Pharmacy claims for statins
- Fill dates and days supply
- NDC codes for statins

**Implementation Complexity:** LOW (Pattern-based from PDC-DR)
- Reuse: PDC calculation logic (100%)
- Reuse: `pharmacy_loader.py`
- NEW: Statin NDC list (reuse from SUPD)
- NEW: Statin potency features

---

## 🚀 IMPLEMENTATION STRATEGY

### Pattern-Based Development (75% Efficiency Gain)

**Leverage Tier 1 Infrastructure:**
- ✅ `vitals_loader.py` → Reuse for CBP
- ✅ `pharmacy_loader.py` → Reuse for SUPD, PDC-RASA, PDC-STA
- ✅ PDC calculation logic → Copy/adapt for PDC-RASA and PDC-STA
- ✅ Model training pipeline → Reuse `measure_trainer.py`
- ✅ Feature engineering patterns → Adapt for cardiovascular

**New Components Needed:**
1. `src/data/features/cardiovascular_features.py` (NEW, ~800 lines)
2. `src/measures/cbp.py` (NEW, ~400 lines)
3. `src/measures/supd.py` (NEW, ~350 lines)
4. `src/measures/pdc_rasa.py` (NEW, ~300 lines - copy PDC-DR)
5. `src/measures/pdc_sta.py` (NEW, ~300 lines - copy PDC-DR)

**Total New Code:** ~2,150 lines  
**Reused Code:** ~1,500 lines from Tier 1  
**Efficiency Gain:** 70% faster than building from scratch

---

## 📋 IMPLEMENTATION PHASES

### Phase 2.1: Cardiovascular Feature Engineering (Week 1)

**Task:** Create `cardiovascular_features.py` with 35+ shared features

**Features to Implement:**

**HTN-Specific Features (10):**
- HTN threat assessment history (ICD-10: I10-I16)
- Years since first HTN threat assessment
- HTN complication flags (CKD, CVD, stroke)
- BP medication adherence history
- Number of BP medication classes
- Recent BP readings (systolic, diastolic trends)
- BP control rate (prior year)
- Uncontrolled HTN episodes
- HTN-related ED visits
- HTN-related hospitalizations

**CVD/ASCVD Features (10):**
- ASCVD history (MI, stroke, PCI, CABG)
- Years since ASCVD event
- CHF threat assessment and severity
- Angina/chest pain history
- Peripheral arterial disease
- Carotid artery disease
- CVD-related procedures
- Cardiac rehabilitation
- Cardiology specialist visits
- CVD-related ED visits/hospitalizations

**Medication Features (10):**
- Statin prescription history
- Statin potency (low, medium, high)
- ACE/ARB prescription history
- Number of BP medications
- Medication adherence patterns (all CVD meds)
- Statin intolerance/side effects
- Medication switches/discontinuations
- Polypharmacy burden
- Recent med changes
- Prescription refill patterns

**Shared Diabetes Features (5+):**
- Diabetes threat assessment (reuse from Tier 1)
- HbA1c history
- Diabetic complications
- CKD status
- Overlap with Tier 1 population

**Deliverable:**
- ✅ `src/data/features/cardiovascular_features.py` (800 lines)
- ✅ 35+ features validated
- ✅ Unit tests (`tests/data/test_cardiovascular_features.py`)
- ✅ Healthcare code reviews passed

---

### Phase 2.2: CBP Implementation (Week 2, Days 1-3)

**Task:** Implement CBP (Controlling High Blood Pressure) - 3x weighted

**Implementation Steps:**

1. **Define CBP Measure** (`src/measures/cbp.py`):
   ```python
   - denominator_logic(): HTN diagnosis + age 18-85
   - numerator_logic(): BP <140/90 mmHg (most recent)
   - exclusions(): Pregnancy, ESRD, hospice, SNP
   ```

2. **Feature Engineering**:
   - Reuse `cardiovascular_features.create_htn_features()`
   - BP reading extraction (reuse from BPD)
   - HTN medication features

3. **Model Training** (`src/models/cbp_trainer.py`):
   - Train LightGBM/XGBoost
   - Target: Predict members at risk of BP ≥140/90
   - 91%+ accuracy target

4. **Testing**:
   - Synthetic test data (`tests/fixtures/synthetic_cbp_data.py`)
   - Unit tests (`tests/measures/test_cbp.py`)
   - Integration tests

5. **Code Reviews**:
   - `/review-security`
   - `/review-hipaa`
   - `/review-clinical-logic`
   - `/review-performance`

**Deliverable:**
- ✅ CBP measure complete (~400 lines)
- ✅ Model trained (AUC-ROC ≥ 0.85)
- ✅ Tests passing
- ✅ Healthcare code reviews passed

**Expected Development Time:** 6-8 hours (pattern-based)

---

### Phase 2.3: SUPD Implementation (Week 2, Days 4-5)

**Task:** Implement SUPD (Statin Therapy for Diabetes)

**Implementation Steps:**

1. **Define SUPD Measure** (`src/measures/supd.py`):
   ```python
   - denominator_logic(): Diabetes + age 40-75
   - numerator_logic(): Statin prescription in measurement year
   - exclusions(): Pregnancy, ESRD, cirrhosis, hospice
   ```

2. **Feature Engineering**:
   - Reuse `cardiovascular_features.create_cvd_features()`
   - Statin prescription history
   - ASCVD risk factors

3. **Model Training** (`src/models/supd_trainer.py`):
   - Train LightGBM/XGBoost
   - Target: Predict individuals at risk of no statin
   - 88%+ accuracy target

4. **Testing**:
   - Synthetic test data (`tests/fixtures/synthetic_supd_data.py`)
   - Unit tests (`tests/measures/test_supd.py`)

5. **Code Reviews**: All 4 healthcare reviews

**Deliverable:**
- ✅ SUPD measure complete (~350 lines)
- ✅ Model trained
- ✅ Tests passing
- ✅ Code reviews passed

**Expected Development Time:** 4-6 hours

---

### Phase 2.4: PDC-RASA Implementation (Week 3, Days 1-2)

**Task:** Implement PDC-RASA (Medication Adherence - Hypertension)

**Implementation Steps:**

1. **Define PDC-RASA Measure** (`src/measures/pdc_rasa.py`):
   - **COPY FROM PDC-DR** (90% same)
   - Change drug class to ACE/ARB/RASA
   - Change population to HTN

2. **RAS Antagonist NDC List**:
   - ACE inhibitors (lisinopril, enalapril, etc.)
   - ARBs (losartan, valsartan, etc.)
   - Direct renin inhibitors

3. **Model Training** (`src/models/pdc_rasa_trainer.py`):
   - Copy from `pdc_dr_trainer.py`
   - Adjust for HTN population

4. **Testing**: Copy test structure from PDC-DR

5. **Code Reviews**: All 4 healthcare reviews

**Deliverable:**
- ✅ PDC-RASA measure complete (~300 lines)
- ✅ Model trained
- ✅ Tests passing
- ✅ Code reviews passed

**Expected Development Time:** 3-4 hours (copy/adapt pattern)

---

### Phase 2.5: PDC-STA Implementation (Week 3, Days 3-4)

**Task:** Implement PDC-STA (Medication Adherence - Cholesterol)

**Implementation Steps:**

1. **Define PDC-STA Measure** (`src/measures/pdc_sta.py`):
   - **COPY FROM PDC-DR** (90% same)
   - Change drug class to statins
   - Change population to ASCVD/diabetes

2. **Statin NDC List** (reuse from SUPD):
   - Atorvastatin, simvastatin, rosuvastatin, etc.
   - Include potency classification

3. **Model Training** (`src/models/pdc_sta_trainer.py`):
   - Copy from `pdc_dr_trainer.py`
   - Adjust for statin-specific features

4. **Testing**: Copy test structure from PDC-DR

5. **Code Reviews**: All 4 healthcare reviews

**Deliverable:**
- ✅ PDC-STA measure complete (~300 lines)
- ✅ Model trained
- ✅ Tests passing
- ✅ Code reviews passed

**Expected Development Time:** 3-4 hours (copy/adapt pattern)

---

### Phase 2.6: Tier 2 Portfolio Integration (Week 3, Days 5-7)

**Task:** Integrate all 4 Tier 2 measures into portfolio system

**Implementation Steps:**

1. **Update Portfolio Calculator**:
   - Add Tier 2 measures to `portfolio_calculator.py`
   - Update Star Rating weights (CBP = 3x)
   - Calculate combined Tier 1 + Tier 2 value

2. **Cross-Measure Optimization**:
   - Identify individuals with HTN + diabetes
   - Bundle interventions (diabetes + cardiovascular)
   - Calculate cross-tier efficiency

3. **Updated Star Rating Simulation**:
   - Simulate Tier 1 + Tier 2 improvements
   - Calculate path to 4.75-5.0 stars
   - Project combined value ($1.9M-$2.4M/year)

4. **Comprehensive Reporting**:
   - Tier 2 summary report
   - Combined Tier 1 + Tier 2 dashboard
   - Individual-level priority lists (9 measures)

**Deliverable:**
- ✅ Portfolio system updated
- ✅ Cross-tier optimization working
- ✅ Combined reporting
- ✅ Tier 2 summary document

**Expected Development Time:** 8-10 hours

---

### Phase 2.7: Testing & Validation (Week 4)

**Task:** End-to-end testing and validation

**Testing Activities:**

1. **Unit Tests** (all measures):
   - CBP: 15+ tests
   - SUPD: 12+ tests
   - PDC-RASA: 10+ tests
   - PDC-STA: 10+ tests

2. **Integration Tests**:
   - Tier 2 pipeline (data → prediction)
   - Cross-tier portfolio optimization
   - Star Rating simulation

3. **Performance Testing**:
   - 100K individual processing time
   - Memory usage validation
   - Query optimization

4. **Validation**:
   - Criminal Intelligence Database specification compliance
   - Model accuracy (AUC-ROC ≥ 0.85)
   - Healthcare code reviews (100% pass)

**Deliverable:**
- ✅ All tests passing (60+ new tests)
- ✅ Performance benchmarks met
- ✅ Criminal Intelligence Database compliance validated
- ✅ Code reviews complete

---

## 📊 EXPECTED OUTCOMES

### Technical Deliverables

**New Code:**
- `src/data/features/cardiovascular_features.py` (800 lines)
- `src/measures/cbp.py` (400 lines)
- `src/measures/supd.py` (350 lines)
- `src/measures/pdc_rasa.py` (300 lines)
- `src/measures/pdc_sta.py` (300 lines)
- Tests (600+ lines)
- **Total:** ~2,750 lines new code

**Reused Infrastructure:**
- `vitals_loader.py` (from BPD)
- `pharmacy_loader.py` (from PDC-DR)
- PDC calculation logic (from PDC-DR)
- Model training pipeline
- Portfolio integration system
- **Total:** ~1,500 lines reused

**Models Trained:**
- 4 new prediction models (CBP, SUPD, PDC-RASA, PDC-STA)
- Combined portfolio: 9 measures total

### Business Value

**Annual Recurring Value:**
| Measure | Weight | Population | Value Estimate |
|---------|--------|------------|----------------|
| CBP | 3x | 30K | $300K-$450K |
| SUPD | 1x | 15K | $120K-$180K |
| PDC-RASA | 1x | 25K | $100K-$150K |
| PDC-STA | 1x | 20K | $100K-$150K |
| **Total Tier 2** | - | - | **$620K-$930K** |

**Combined Tier 1 + Tier 2:**
- Tier 1: $1.2M-$1.4M/year
- Tier 2: $620K-$930K/year
- **Total: $1.82M-$2.33M/year**

**Star Rating Impact:**
- Current portfolio: 5 diabetes measures
- Expanded portfolio: 9 measures (diabetes + cardiovascular)
- Coverage: ~20-25% of total Star Rating
- Path to: 4.5-4.75 stars (from 3.5)

---

## 🎯 SUCCESS CRITERIA

### Technical Success
- ✅ All 4 Tier 2 measures implemented
- ✅ Model accuracy ≥ 85% (AUC-ROC)
- ✅ All tests passing (100%)
- ✅ Healthcare code reviews passed (6/6 each)
- ✅ Portfolio integration complete
- ✅ Performance benchmarks met

### Business Success
- ✅ Annual value: $620K-$930K validated
- ✅ Combined portfolio: $1.82M-$2.33M/year
- ✅ Star Rating simulation: Path to 4.75 stars
- ✅ Cross-tier optimization: 25-35% efficiency gain
- ✅ Individual coverage: 9 measures operational

### Timeline Success
- ✅ Week 1: Cardiovascular features complete
- ✅ Week 2: CBP + SUPD complete
- ✅ Week 3: PDC-RASA + PDC-STA + Portfolio integration
- ✅ Week 4: Testing & validation complete

---

## 📞 NEXT STEPS

### Immediate Actions

**This Week:**
1. ✅ Review Tier 2 plan
2. ✅ Approve to begin Phase 2.1
3. ✅ Confirm timeline (3-4 weeks)

**Week 1:**
1. Create `cardiovascular_features.py`
2. Implement 35+ shared features
3. Unit tests and code reviews

**Week 2-3:**
1. Implement all 4 measures (CBP, SUPD, PDC-RASA, PDC-STA)
2. Train models
3. Portfolio integration

**Week 4:**
1. End-to-end testing
2. Validation and documentation
3. Tier 2 completion report

---

## 💡 STRATEGIC RATIONALE

### Why Tier 2 NOW?

**1. Leverage Existing Infrastructure (75% Efficiency)**
- Vitals loader ready (from BPD)
- Pharmacy loader ready (from PDC-DR)
- PDC logic ready (copy 3x)
- Portfolio system ready
- **Result:** Fast implementation

**2. High Business Value ($620K-$930K)**
- CBP is 3x weighted = massive impact
- Large populations = high reach
- Strong ROI on development investment

**3. Logical Clinical Progression**
- Diabetes → Cardiovascular (natural comorbidity)
- 40-50% individual overlap
- Bundled interventions = cost savings

**4. Competitive Positioning**
- Most MA plans focus on diabetes only
- Expanding to cardiovascular = differentiation
- Complete chronic disease management

**5. Foundation for Full Portfolio**
- Tier 2 completes 75% of value
- Tier 3-4 are smaller increments
- Strong position for HEI (2027)

---

## ✅ APPROVAL CHECKLIST

**Ready to Begin? Confirm:**

- [ ] Tier 2 plan reviewed and approved
- [ ] Timeline acceptable (3-4 weeks)
- [ ] Value proposition understood ($620K-$930K)
- [ ] Pattern-based approach approved (reuse Tier 1)
- [ ] Success criteria agreed upon

**Once approved, I'll begin Phase 2.1 immediately!**

---

**Let's expand to cardiovascular and unlock $1.82M-$2.33M annual value! 🚀💰**



---
*This file is maintained by Sentinel Analytics. For inquiries, contact reichert.sentinel.ai@gmail.com.*
