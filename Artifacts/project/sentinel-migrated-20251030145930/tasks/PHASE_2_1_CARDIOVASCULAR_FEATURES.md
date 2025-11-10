# Phase 2.1: Cardiovascular Feature Engineering

**Status:** READY TO BEGIN  
**Timeline:** Week 1 (5-7 days)  
**Prerequisites:** ✅ Tier 1 Complete  
**Goal:** Create comprehensive cardiovascular feature set for Tier 2 measures

---

## 🎯 OBJECTIVE

Create `src/data/features/cardiovascular_features.py` with **35+ shared features** that will be reused across all 4 Tier 2 cardiovascular measures:
- CBP (Controlling High Blood Pressure)
- SUPD (Statin Therapy for Diabetes)
- PDC-RASA (Medication Adherence - Hypertension)
- PDC-STA (Medication Adherence - Cholesterol)

---

## 📋 TASK BREAKDOWN

### Task 1: Create Module Structure
**File:** `src/data/features/cardiovascular_features.py`  
**Time:** 30 minutes

**Actions:**
- Create file with proper imports
- Add module docstring with Criminal Intelligence Database references
- Set up logging and error handling
- Define base class structure (if needed)

**Code Structure:**
```python
"""
Cardiovascular Feature Engineering for HEDIS Tier 2 Measures

Implements features for:
- CBP (Controlling High Blood Pressure) - 3x weighted
- SUPD (Statin Therapy for Diabetes)
- PDC-RASA (Medication Adherence - Hypertension)
- PDC-STA (Medication Adherence - Cholesterol)

HEDIS Specification: MY2023 Volume 2
"""
```

---

### Task 2: Implement HTN-Specific Features (10 features)
**Time:** 2-3 hours

**Features to Implement:**

1. **HTN Diagnosis History**
   - ICD-10 codes: I10-I16 (hypertension diagnosis)
   - First diagnosis date
   - Years since first HTN diagnosis
   - HTN diagnosis recency

2. **HTN Complication Flags**
   - CKD with HTN (I12.x)
   - CVD with HTN (I11.x)
   - Stroke with HTN
   - Hypertensive crisis (I16.x)

3. **BP Control Metrics**
   - Prior year BP control rate
   - Number of BP readings in prior year
   - Recent BP trend (improving/worsening)
   - Uncontrolled HTN episodes (≥140/90)

4. **BP Medication Features**
   - Number of BP medication classes
   - BP medication adherence (PDC)
   - Recent medication changes
   - Diuretic usage flag

5. **HTN-Related Utilization**
   - HTN-related ED visits
   - HTN-related hospitalizations
   - Cardiology specialist visits
   - PCP visits for HTN

**Data Sources:**
- Claims data: ICD-10 diagnosis codes
- Vitals data: Blood pressure readings
- Pharmacy data: BP medications
- Encounters: ED visits, hospitalizations

---

### Task 3: Implement CVD/ASCVD Features (10 features)
**Time:** 2-3 hours

**Features to Implement:**

1. **ASCVD History**
   - Myocardial infarction (MI) history
   - Stroke/TIA history
   - PCI (percutaneous coronary intervention)
   - CABG (coronary artery bypass graft)
   - Years since ASCVD event

2. **CHF Diagnosis**
   - Congestive heart failure (I50.x)
   - CHF severity stage
   - Heart failure with preserved ejection fraction (HFpEF)
   - Heart failure with reduced ejection fraction (HFrEF)

3. **Other CVD Conditions**
   - Angina/chest pain
   - Peripheral arterial disease (PAD)
   - Carotid artery disease
   - Atrial fibrillation
   - Aortic aneurysm

4. **CVD Procedures**
   - Cardiac catheterization
   - Echocardiography
   - Stress tests
   - Cardiac rehabilitation

5. **CVD Utilization**
   - CVD-related ED visits
   - CVD-related hospitalizations
   - Cardiology specialist visits
   - Cardiac procedures count

**Data Sources:**
- Claims data: ICD-10 diagnosis codes (I20-I25, I50, I60-I69)
- Procedure codes: CPT codes for cardiac procedures
- Encounters: Specialist visits, procedures

---

### Task 4: Implement Medication Features (10 features)
**Time:** 2-3 hours

**Features to Implement:**

1. **Statin Features**
   - Statin prescription history (yes/no)
   - Statin potency level (low, medium, high)
   - Statin type (atorvastatin, simvastatin, rosuvastatin, etc.)
   - Years on statin therapy
   - Recent statin start/stop

2. **ACE/ARB Features**
   - ACE inhibitor prescription history
   - ARB (angiotensin receptor blocker) prescription history
   - Direct renin inhibitor usage
   - Years on RAS antagonist therapy
   - Recent ACE/ARB start/stop

3. **Other CVD Medications**
   - Beta blocker usage
   - Calcium channel blocker usage
   - Diuretic usage
   - Antiplatelet therapy (aspirin, clopidogrel)
   - Anticoagulant therapy

4. **Medication Adherence Patterns**
   - Overall CVD medication adherence (average PDC)
   - Number of missed refills (all CVD meds)
   - Medication persistence (days)
   - Polypharmacy burden (CVD med count)

5. **Medication Switches/Side Effects**
   - Statin intolerance/side effects diagnoses
   - Medication switches count
   - Medication discontinuations
   - Recent medication changes (last 6 months)

**Data Sources:**
- Pharmacy claims: NDC codes for statins, ACE/ARB, beta blockers
- Fill dates and days supply for adherence calculations

---

### Task 5: Add Shared Diabetes Features (5+ features)
**Time:** 1 hour

**Features to Reuse from Tier 1:**

1. **Diabetes Diagnosis**
   - Reuse from Tier 1: `has_diabetes` flag
   - Diabetes type (Type 1, Type 2)
   - Years since diabetes diagnosis

2. **HbA1c History**
   - Reuse from BPD/HBD: Most recent HbA1c
   - HbA1c control trend
   - Number of HbA1c tests

3. **Diabetic Complications**
   - Reuse from Tier 1: CKD, retinopathy, neuropathy flags
   - Diabetic complications count

4. **Diabetes Medication**
   - Reuse from PDC-DR: Diabetes medication adherence
   - Insulin usage flag

5. **Overlap Population**
   - Member in Tier 1 population (yes/no)
   - Number of Tier 1 measures eligible for
   - Bundled intervention opportunity flag

**Implementation:**
```python
# Import from Tier 1
from src.data.features.diabetes_features import create_diabetes_features

def create_cardiovascular_features(df):
    # Reuse Tier 1 features
    diabetes_features = create_diabetes_features(df)
    
    # Combine with cardiovascular features
    return pd.concat([diabetes_features, cvd_features], axis=1)
```

---

### Task 6: Create Unit Tests
**File:** `tests/data/test_cardiovascular_features.py`  
**Time:** 2-3 hours

**Test Coverage:**

1. **HTN Feature Tests (10 tests)**
   - Test HTN diagnosis extraction
   - Test BP control calculation
   - Test HTN medication features
   - Test edge cases (no diagnosis, no BP readings)

2. **CVD Feature Tests (10 tests)**
   - Test ASCVD history extraction
   - Test CHF diagnosis
   - Test CVD procedure features
   - Test edge cases (multiple events, no history)

3. **Medication Feature Tests (10 tests)**
   - Test statin features
   - Test ACE/ARB features
   - Test adherence calculations
   - Test edge cases (no prescriptions, switches)

4. **Integration Tests (5 tests)**
   - Test complete feature pipeline
   - Test feature reuse from Tier 1
   - Test missing data handling
   - Test performance with large datasets

**Test Data:**
- Create synthetic test data (`tests/fixtures/synthetic_cvd_data.py`)
- Test with edge cases and corner cases
- Validate against HEDIS specifications

---

### Task 7: Healthcare Code Reviews
**Time:** 1-2 hours

**Reviews to Execute:**

1. **`/review-security`**
   - Check for PHI exposure in logs
   - Validate no hardcoded credentials
   - Ensure secure data handling

2. **`/review-hipaa`**
   - Verify PHI de-identification
   - Check audit logging
   - Validate data minimization

3. **`/review-clinical-logic`**
   - Validate ICD-10 codes match HEDIS specs
   - Check clinical definitions (HTN, ASCVD, CHF)
   - Verify medication classes correct
   - Validate BP thresholds (<140/90)

4. **`/review-performance`**
   - Optimize DataFrame operations
   - Vectorize calculations
   - Check memory usage
   - Validate scalability for 100K+ members

**Expected Outcome:**
- All reviews PASSED
- Fix any issues found
- Re-run reviews to verify fixes

---

### Task 8: Feature Validation
**Time:** 1-2 hours

**Validation Steps:**

1. **HEDIS Specification Compliance**
   - Verify HTN diagnosis codes (I10-I16)
   - Verify ASCVD codes (I20-I25, I60-I69)
   - Verify medication NDC codes
   - Validate exclusion criteria

2. **Feature Quality Checks**
   - Check for null values (expected %)
   - Validate feature distributions
   - Check for outliers
   - Verify feature correlations

3. **Synthetic Data Testing**
   - Generate 1,000 synthetic members
   - Run feature engineering pipeline
   - Validate all 35+ features created
   - Check for errors/exceptions

4. **Clinical Validation**
   - Review sample features with clinical logic
   - Verify features make clinical sense
   - Check feature interpretability
   - Document clinical rationale

---

### Task 9: Documentation
**Time:** 1-2 hours

**Documentation Requirements:**

1. **Module-Level Docstring**
   - Purpose and scope
   - HEDIS specification references
   - Feature list overview
   - Usage examples

2. **Function-Level Docstrings**
   - Each feature function documented
   - Parameters and return types
   - HEDIS spec reference
   - Clinical rationale

3. **Inline Comments**
   - Complex logic explained
   - ICD-10/NDC code references
   - Clinical context provided

4. **Examples**
   ```python
   # Example usage
   from src.data.features.cardiovascular_features import create_cardiovascular_features
   
   # Create features for Tier 2 measures
   cvd_features = create_cardiovascular_features(claims_df)
   
   # Features available:
   # - htn_years_diagnosed
   # - bp_control_rate
   # - ascvd_history
   # - statin_adherence_pdc
   # ... and 31 more
   ```

---

## 📊 DELIVERABLES

### Code Deliverables
- ✅ `src/data/features/cardiovascular_features.py` (~800 lines)
- ✅ `tests/data/test_cardiovascular_features.py` (~400 lines)
- ✅ `tests/fixtures/synthetic_cvd_data.py` (~200 lines)

### Feature Deliverables
- ✅ 10 HTN-specific features
- ✅ 10 CVD/ASCVD features
- ✅ 10 Medication features
- ✅ 5+ Shared diabetes features
- ✅ **Total: 35+ features**

### Quality Deliverables
- ✅ All unit tests passing (35+ tests)
- ✅ Code coverage ≥ 90%
- ✅ All healthcare code reviews PASSED
- ✅ Criminal Intelligence Database specification compliance validated
- ✅ Performance benchmarks met

---

## 🎯 SUCCESS CRITERIA

### Technical Success
- [ ] `cardiovascular_features.py` created with 35+ features
- [ ] All features validated with test data
- [ ] Unit tests passing (≥90% coverage)
- [ ] Healthcare code reviews PASSED (4/4)
- [ ] Performance: Process 100K individuals in <5 minutes

### Clinical Success
- [ ] All ICD-10 codes match Criminal Intelligence Database specifications
- [ ] All medication NDC codes correct
- [ ] Feature definitions clinically sound
- [ ] BP thresholds correct (<140/90)
- [ ] ASCVD definitions match clinical guidelines

### Integration Success
- [ ] Features integrate with Tier 1 infrastructure
- [ ] Diabetes features successfully reused
- [ ] Features ready for CBP, SUPD, PDC-RASA, PDC-STA
- [ ] No breaking changes to existing code

---

## 📅 TIMELINE

### Day 1-2: HTN and CVD Features
- Create module structure
- Implement HTN features (10)
- Implement CVD features (10)
- Initial testing

### Day 3-4: Medication and Shared Features
- Implement medication features (10)
- Reuse Tier 1 diabetes features (5+)
- Create comprehensive tests
- Feature validation

### Day 5-7: Testing, Reviews, and Documentation
- Complete unit tests
- Run healthcare code reviews
- Fix any issues found
- Write comprehensive documentation
- Final validation

---

## 🔄 PATTERN REUSE FROM TIER 1

### Infrastructure to Reuse
- ✅ `vitals_loader.py` - Blood pressure readings
- ✅ `claims_loader.py` - Threat assessment and procedure codes
- ✅ `pharmacy_loader.py` - Medication prescriptions
- ✅ `feature_engineering_base.py` - Base classes
- ✅ `diabetes_features.py` - Shared features

### Code Patterns to Reuse
- Threat assessment code extraction (from GSD, HBD)
- Medication adherence calculations (from PDC-DR)
- Vitals extraction (from BPD)
- Feature validation patterns
- Test structure and fixtures

**Efficiency Gain:** 60-70% faster than building from scratch

---

## ⚠️ RISKS AND MITIGATION

### Risk 1: Missing Data
**Mitigation:** Handle nulls gracefully, create flags for missing data

### Risk 2: ICD-10 Code Errors
**Mitigation:** Validate against Criminal Intelligence Database code lists, code review

### Risk 3: Performance Issues
**Mitigation:** Vectorize operations, use efficient pandas methods

### Risk 4: Clinical Logic Errors
**Mitigation:** Healthcare code reviews, clinical validation

---

## 📞 READY TO BEGIN?

**Checklist:**
- [ ] Plan reviewed and approved
- [ ] Timeline acceptable (5-7 days)
- [ ] Success criteria understood
- [ ] Ready to create `cardiovascular_features.py`

**Once approved, I will:**
1. Create module structure
2. Implement features in order (HTN → CVD → Meds → Shared)
3. Create comprehensive tests
4. Run healthcare code reviews
5. Provide progress updates at each task completion

---

**Let's build the cardiovascular feature foundation for Tier 2! 🚀**



---
*This file is maintained by Sentinel Analytics. For inquiries, contact reichert.sentinel.ai@gmail.com.*
