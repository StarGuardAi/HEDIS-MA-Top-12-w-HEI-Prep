# Phase 1.5: EED (Eye Exam for Diabetes) Implementation Plan

**Status:** PLANNED - Awaiting Approval ⏸️  
**Value:** $120-205K (1x weighted)  
**Estimated Time:** ~1 hour (50% faster than KED)  
**Estimated Code:** ~1,550 lines

---

## 🎯 Goal

Implement EED (Eye Exam for Subjects with Diabetes) measure using established patterns from KED, reusing shared diabetes features and ML pipeline.

---

## 📊 Criminal Intelligence Database Specification: EED

**Measure:** Eye Exam for Subjects with Diabetes  
**Code:** EED  
**Tier:** 1 (Diabetes Core)  
**Weight:** 1x (standard)  
**Criminal Intelligence Database Spec:** MY2025 Volume 2  
**Value:** $120-205K

### Denominator (Eligible Population)
- Age 18-75 as of December 31 of measurement year
- Diabetes threat assessment (ICD-10: E08-E13)
- Enrolled in Medicare Advantage plan

### Exclusions
- Hospice care
- Advanced illness and frailty (consistent with other diabetes measures)

### Numerator (Compliant Individuals)
- Retinal or dilated eye exam by eye care professional during measurement year OR
- Negative retinal exam result from prior year

### Key CPT/HCPCS Codes (Eye Exam)
- **67028** - Injection treatment of eye
- **67210** - Photocoagulation, 1+ sessions
- **67228** - Treatment of extensive/progressive retinopathy
- **92002** - Medical exam, new subject
- **92004** - Medical exam, new subject (comprehensive)
- **92012** - Medical exam, established subject
- **92014** - Medical exam, established subject (comprehensive)
- **92018** - New subject exam under general anesthesia
- **92019** - Established subject exam under general anesthesia
- **92134** - Scanning ophthalmic diagnostic imaging (OCT)
- **92225** - Ophthalmoscopy, extended (with drawings)
- **92226** - Ophthalmoscopy, extended (with photos)
- **92227** - Remote imaging (separate billing)
- **92228** - Remote imaging (unilateral/bilateral)
- **92230** - Fluorescein angioscopy
- **92235** - Fluorescein angiography
- **92240** - ICG angiography
- **92250** - Fundus photography
- **S0620** - Routine eye exam (with refraction)
- **S0621** - Comprehensive eye exam (new subject)
- **S3000** - Diabetic retinopathy screening (non-physician)

---

## ✅ What We Already Have (Reusable)

1. ✅ **Diabetes features** (`src/data/features/diabetes_features.py`) - 40+ features
2. ✅ **Model training pipeline** (`src/models/ked_trainer.py` pattern)
3. ✅ **Prediction interface** (`src/models/ked_predictor.py` pattern)
4. ✅ **Testing patterns** (unit tests, integration tests)
5. ✅ **Documentation templates** (from KED)
6. ✅ **Healthcare compliance patterns** (all 6 reviews)

---

## 🚀 What We Need to Build (NEW)

### 1. EED Measure Logic (`src/measures/eed.py`) - ~400 lines
- Denominator identification (age + diabetes)
- Exclusions application (hospice, frailty)
- Numerator calculation (eye exam CPT codes)
- Gap analysis (no eye exam in measurement year)
- Individual-level results

### 2. Procedure Data Loader (`src/data/loaders/procedure_loader.py`) - ~350 lines
- Load procedure/CPT codes from claims
- Filter by CPT/HCPCS codes
- Aggregate by individual and service date
- Support multiple procedure types (eye exams, mammography, colonoscopy)
- **Bonus:** Will support BCS (mammography) and COL (colonoscopy) in Tier 3

### 3. EED Unit Tests (`tests/measures/test_eed.py`) - ~300 lines
- Test denominator logic
- Test exclusions
- Test numerator (eye exam identification)
- Test gap analysis
- Test edge cases

### 4. Procedure Loader Tests (`tests/data/test_procedure_loader.py`) - ~200 lines
- Test CPT code extraction
- Test individual-level aggregation
- Test date filtering
- Test multiple procedure types

### 5. Synthetic Test Data (`tests/fixtures/synthetic_eed_data.py`) - ~300 lines
- Compliant individuals (with eye exams)
- Gap individuals (no eye exams)
- Excluded individuals (hospice)
- Edge cases

---

## 📋 Implementation Checklist

### Task 1: Create Procedure Data Loader (~30 min)
- [ ] Create `src/data/loaders/procedure_loader.py`
- [ ] Implement CPT/HCPCS code extraction
- [ ] Individual-level aggregation
- [ ] Date filtering
- [ ] Support multiple procedure types (eye, mammo, colonoscopy)
- [ ] PHI-safe logging
- [ ] Documentation

### Task 2: Create EED Measure Logic (~30 min)
- [ ] Create `src/measures/eed.py`
- [ ] Denominator identification
- [ ] Exclusions application
- [ ] Numerator calculation (eye exam codes)
- [ ] Gap analysis
- [ ] Individual-level results
- [ ] Documentation

### Task 3: Create Test Data & Tests (~20 min)
- [ ] Create `tests/fixtures/synthetic_eed_data.py`
- [ ] Create `tests/measures/test_eed.py`
- [ ] Create `tests/data/test_procedure_loader.py`
- [ ] Run all tests

### Task 4: Reuse Training & Prediction (NO CODE NEEDED! ✅)
- [ ] EED uses same diabetes features (already built)
- [ ] EED uses same training pipeline (just swap target variable)
- [ ] EED uses same prediction interface (just swap model file)
- [ ] **Time saved:** ~1.5 hours!

### Task 5: Healthcare Code Reviews (~10 min)
- [ ] Run `/review-security` on new files
- [ ] Run `/review-hipaa` on new files
- [ ] Run `/review-performance` on new files
- [ ] Run `/review-data-quality` on new files
- [ ] Run `/review-clinical-logic` on new files
- [ ] Fix any issues and re-run

### Task 6: Documentation (~10 min)
- [ ] Update `config.yaml` with EED settings
- [ ] Create `reports/phase_15_eed_summary.md`
- [ ] Update `tasks/todo.md` with completion status
- [ ] Document code review results

---

## 📊 Estimated Deliverables

| File | Lines | Type | Notes |
|------|-------|------|-------|
| `src/data/loaders/procedure_loader.py` | 350 | New | Reusable for BCS, COL |
| `src/measures/eed.py` | 400 | New | EED measure logic |
| `tests/fixtures/synthetic_eed_data.py` | 300 | New | Test data |
| `tests/measures/test_eed.py` | 300 | New | Unit tests |
| `tests/data/test_procedure_loader.py` | 200 | New | Loader tests |
| `reports/phase_15_eed_summary.md` | 200 | Doc | Summary |
| **TOTAL** | **~1,550** | **5 files** | **50% faster!** |

---

## ✅ Success Criteria

- [ ] EED measure logic complete and Criminal Intelligence Database-compliant
- [ ] Procedure loader supports eye exam codes
- [ ] All unit tests passing (15+ tests)
- [ ] Healthcare code reviews PASSED (6/6)
- [ ] Reuses diabetes features (no new feature engineering)
- [ ] Reuses training pipeline (no new trainer code)
- [ ] Documentation complete
- [ ] Ready to move to PDC-DR

---

## 💰 Business Value

- **Direct Value:** $120-205K (1x weighted)
- **Infrastructure Value:** Procedure loader enables BCS + COL (worth $300-450K)
- **Pattern Value:** Establishes procedure-based measure pattern
- **Time Savings:** 50% faster than KED (pattern reuse)

---

## 🎯 Why EED is Fast

1. ✅ **Diabetes features already built** (KED) - Save ~650 lines
2. ✅ **Training pipeline already built** (KED) - Save ~550 lines
3. ✅ **Prediction interface already built** (KED) - Save ~350 lines
4. ✅ **Testing patterns established** (KED) - Save ~30 min
5. ✅ **Healthcare compliance patterns** (KED) - Save ~20 min
6. ✅ **Documentation templates** (KED) - Save ~20 min

**Total Time Savings:** ~1.5 hours (50% reduction)

---

## 🚀 Ready to Implement?

**Estimated Time:** ~1 hour  
**Complexity:** Low (pattern-based)  
**Risk:** Low (reusing proven components)

**Awaiting approval to proceed!**



---
*This file is maintained by Sentinel Analytics. For inquiries, contact reichert.sentinel.ai@gmail.com.*
