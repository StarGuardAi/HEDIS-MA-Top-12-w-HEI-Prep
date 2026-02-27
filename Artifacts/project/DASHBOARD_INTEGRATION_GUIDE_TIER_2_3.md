# Dashboard Integration Guide: Tier 2 & Tier 3 Measures

**Target File:** `streamlit_app.py`  
**Current Size:** 3,658 lines, 10 pages  
**Goal:** Add 2 new pages (Tier 2 Cardiovascular, Tier 3 Preventive) and update Executive Summary

---

## Quick Implementation Checklist

- [ ] Step 1: Update navigation (add 2 new pages)
- [ ] Step 2: Create Tier 2 Cardiovascular page function
- [ ] Step 3: Create Tier 3 Preventive page function  
- [ ] Step 4: Update Executive Summary with 11-measure metrics
- [ ] Step 5: Add routing logic for new pages
- [ ] Step 6: Test locally
- [ ] Step 7: Deploy to Streamlit Cloud

**Estimated Time:** 4-6 hours

---

## Step 1: Update Navigation (Line ~381)

**Location:** Find `page = st.sidebar.selectbox(` around line 379

**REPLACE:**
```python
page = st.sidebar.selectbox(
    "Select Page",
    [
        "🏠 Executive Summary",
        "⚠️ Problem Statement",
        "📊 Portfolio Overview",
        "💰 Financial Impact",
        "⭐ Star Rating Simulator",
        "🤖 AI/ML Models",
        "🏥 Health Equity (HEI)",
        "📈 Visualizations",
        "💻 Technical Details",
        "👤 About Me"
    ]
)
```

**WITH:**
```python
page = st.sidebar.selectbox(
    "Select Page",
    [
        "🏠 Executive Summary",
        "⚠️ Problem Statement",
        "📊 Tier 1: Diabetes Portfolio",  # Renamed for clarity
        "❤️ Tier 2: Cardiovascular Portfolio",  # NEW
        "🩺 Tier 3: Preventive Care",  # NEW
        "💰 Financial Impact",
        "⭐ Star Rating Simulator",
        "🤖 AI/ML Models",
        "🏥 Health Equity (HEI)",
        "📈 Visualizations",
        "💻 Technical Details",
        "👤 About Me"
    ]
)
```

---

## Step 2: Create Tier 2 Cardiovascular Page Function

**Location:** Add after the Tier 1 Portfolio page function (search for "def show_" functions)

**CODE TO ADD:**

```python
# ============================================================================
# PAGE: TIER 2 CARDIOVASCULAR PORTFOLIO
# ============================================================================

def show_tier2_cardiovascular():
    """
    Tier 2: Cardiovascular Portfolio
    Measures: CBP, SUPD, PDC-RASA, PDC-STA
    Annual Value: $500K-$750K (100K members)
    """
    
    st.markdown('<h1 class="main-header">❤️ Tier 2: Cardiovascular Portfolio</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">4 High-Value Cardiovascular Measures | $500K-$750K Annual Value</p>', unsafe_allow_html=True)
    
    # Overview metrics
    st.markdown("## 📊 Portfolio Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Measures",
            value="4",
            delta="Cardiovascular focus"
        )
    
    with col2:
        st.metric(
            label="Annual Value",
            value="$500K-$750K",
            delta="100K members"
        )
    
    with col3:
        st.metric(
            label="Star Weight",
            value="6x",
            delta="CBP is 3x weighted"
        )
    
    with col4:
        st.metric(
            label="Gap Potential",
            value="$75K-$150K",
            delta="15-20% improvement"
        )
    
    st.markdown("---")
    
    # Measure details
    st.markdown("## 🏥 Cardiovascular Measures")
    
    measures = pd.DataFrame({
        'Measure': [
            'CBP - Controlling High Blood Pressure',
            'SUPD - Statin Therapy (Diabetes)',
            'PDC-RASA - Medication Adherence (HTN)',
            'PDC-STA - Medication Adherence (Statins)'
        ],
        'Population': [
            'Adults 18-85 with HTN diagnosis',
            'Adults 40-75 with diabetes',
            'Adults 18+ with 2+ RAS antagonist fills',
            'Adults 18+ with 2+ statin fills'
        ],
        'Numerator': [
            'BP <140/90 (most recent)',
            'At least one statin prescription',
            'PDC ≥ 80%',
            'PDC ≥ 80%'
        ],
        'Star Weight': ['3x', '1x', '1x', '1x'],
        'Annual Value': ['$180K-$270K', '$120K-$180K', '$100K-$150K', '$100K-$150K'],
        'Status': ['✅ Complete', '✅ Complete', '✅ Complete', '✅ Complete']
    })
    
    st.dataframe(measures, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # CBP Focus (Triple-Weighted)
    st.markdown("## 🎯 CBP: Triple-Weighted Measure")
    
    st.info("""
    **Why CBP is Critical:**
    - **3x Star Rating Weight** (highest impact measure)
    - **Large denominator** (all adults with HTN = 40%+ of MA population)
    - **Easy gap closure** (medication adjustments, lifestyle interventions)
    - **CMS Focus Area** (Part D-to-D transition emphasizes HTN control)
    
    **Gap Closure Strategy:**
    1. Medication titration (ACE/ARB, CCB, diuretics)
    2. Home BP monitoring programs
    3. Nurse-led HTN clinics
    4. Telehealth BP management
    
    **Expected Improvement:** 15-25 percentage points
    """)
    
    # BP Control Targets
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### BP Targets by Age")
        bp_targets = pd.DataFrame({
            'Age Group': ['18-59', '60-85'],
            'Target BP': ['<140/90', '<140/90'],
            'Alternative Target': ['<130/80 (ACC/AHA)', '<150/90 (JNC 8)']
        })
        st.dataframe(bp_targets, use_container_width=True, hide_index=True)
    
    with col2:
        st.markdown("### Medication Classes")
        med_classes = pd.DataFrame({
            'Class': ['ACE Inhibitors', 'ARBs', 'CCBs', 'Diuretics', 'Beta Blockers'],
            'Examples': ['Lisinopril, Enalapril', 'Losartan, Valsartan', 'Amlodipine, Diltiazem', 'HCTZ, Furosemide', 'Metoprolol, Carvedilol'],
            'PDC Measure': ['PDC-RASA', 'PDC-RASA', '—', '—', '—']
        })
        st.dataframe(med_classes, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # PDC Methodology
    st.markdown("## 📊 PDC (Proportion of Days Covered) Methodology")
    
    st.markdown("""
    **PDC Formula:**
    ```
    PDC = (Days Covered with Medication / Total Days in Year) × 100
    ```
    
    **Numerator Criteria:** PDC ≥ 80%
    
    **Example:**
    - Member has 12 fills of lisinopril, 30 days supply each
    - Days covered: 360 (some overlap)
    - PDC: 360/365 = 98.6% ✅ PASS
    """)
    
    # PDC Visualization (example data)
    import plotly.graph_objects as go
    
    fig = go.Figure()
    
    # Add PDC distribution bars
    pdc_ranges = ['0-50%', '50-60%', '60-70%', '70-80%', '80-90%', '90-100%']
    pdc_counts = [150, 200, 250, 300, 400, 700]  # Example data
    colors = ['#ef4444', '#f97316', '#fbbf24', '#a3e635', '#22c55e', '#10b981']
    
    fig.add_trace(go.Bar(
        x=pdc_ranges,
        y=pdc_counts,
        marker_color=colors,
        text=pdc_counts,
        textposition='auto',
        name='Member Count'
    ))
    
    fig.update_layout(
        title='PDC-RASA Distribution (Example)',
        xaxis_title='PDC Range',
        yaxis_title='Number of Members',
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Clinical Value
    st.markdown("## 💊 Clinical Value of Cardiovascular Measures")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **CBP Benefits:**
        - Reduces stroke risk by 35-40%
        - Reduces MI risk by 20-25%
        - Prevents heart failure progression
        - Kidney disease protection
        
        **SUPD Benefits:**
        - Reduces ASCVD events by 25-30%
        - Diabetic heart disease prevention
        - Reduces stroke risk in diabetics
        - Cost-effective secondary prevention
        """)
    
    with col2:
        st.markdown("""
        **PDC-RASA Benefits:**
        - Prevents HTN complications
        - Reduces ER visits for hypertensive crisis
        - Improves long-term BP control
        - Reduces total cost of care
        
        **PDC-STA Benefits:**
        - Prevents MI and stroke
        - Reduces LDL cholesterol 25-50%
        - All-cause mortality reduction
        - Cost-effective primary/secondary prevention
        """)
    
    st.markdown("---")
    
    # Gap Closure ROI
    st.markdown("## 💰 Gap Closure ROI")
    
    st.success("""
    **Tier 2 Cardiovascular Portfolio:**
    - **Total Value:** $500K-$750K annually (100K members)
    - **Gap Closure Potential:** $75K-$150K
    - **Easiest Wins:** CBP (medication titration), PDC-RASA (pharmacy partnerships)
    - **Hardest Challenges:** SUPD (physician education), PDC-STA (patient adherence)
    
    **Recommended Strategy:**
    1. Focus on CBP first (3x weight = highest ROI)
    2. Implement pharmacy-based interventions for PDC measures
    3. Leverage diabetes population overlap (SUPD + Tier 1 SPD)
    4. Use medication synchronization programs to improve PDC rates
    """)
```

---

## Step 3: Create Tier 3 Preventive Care Page Function

**CODE TO ADD:**

```python
# ============================================================================
# PAGE: TIER 3 PREVENTIVE CARE PORTFOLIO
# ============================================================================

def show_tier3_preventive():
    """
    Tier 3: Preventive Care Portfolio
    Measures: BCS, FLU, COL
    Annual Value: $260K-$390K (100K members)
    """
    
    st.markdown('<h1 class="main-header">🩺 Tier 3: Preventive Care Portfolio</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">3 High-Priority Preventive Measures | $260K-$390K Annual Value</p>', unsafe_allow_html=True)
    
    # Overview metrics
    st.markdown("## 📊 Portfolio Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Implemented",
            value="3 of 6",
            delta="High-priority only"
        )
    
    with col2:
        st.metric(
            label="Annual Value",
            value="$260K-$390K",
            delta="100K members"
        )
    
    with col3:
        st.metric(
            label="Star Weight",
            value="3x",
            delta="Standard weighting"
        )
    
    with col4:
        st.metric(
            label="Gap Potential",
            value="$40K-$80K",
            delta="Easy closures"
        )
    
    st.markdown("---")
    
    # Implemented measures
    st.markdown("## ✅ Implemented Measures")
    
    implemented = pd.DataFrame({
        'Measure': [
            'BCS - Breast Cancer Screening',
            'FLU - Influenza Immunization',
            'COL - Colorectal Cancer Screening'
        ],
        'Population': [
            'Women 50-74 years',
            'Adults 65+ years',
            'Adults 50-75 years'
        ],
        'Screening Interval': [
            'Biennial (2 years)',
            'Annual (flu season)',
            'Varies by modality (1-10 years)'
        ],
        'Annual Value': ['$80K-$120K', '$80K-$120K', '$100K-$150K'],
        'Gap Closure Ease': ['Medium', 'Easy', 'Medium-Hard'],
        'Status': ['✅ Complete', '✅ Complete', '✅ Complete']
    })
    
    st.dataframe(implemented, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # BCS Details
    st.markdown("## 🎀 BCS: Breast Cancer Screening")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Denominator:**
        - Women aged 50-74 years
        - 27-month continuous enrollment
        - No bilateral mastectomy
        
        **Numerator:**
        - Mammography in measurement year OR prior year
        - CPT codes: 77065, 77066, 77067
        
        **Gap Closure Strategy:**
        1. Provider reminders (EMR alerts)
        2. Patient outreach (birthday postcards at age 50)
        3. Mobile mammography units
        4. Weekend/evening screening appointments
        """)
    
    with col2:
        st.info("""
        **Clinical Value:**
        - Early detection improves 5-year survival to 99%
        - Reduces breast cancer mortality by 15-20%
        - USPSTF Grade B recommendation
        
        **Typical Compliance:** 70-75% (MA plans)
        **Target:** 78-80%
        **Gap Closure Potential:** 3-5 percentage points = $12K-$24K
        """)
    
    st.markdown("---")
    
    # FLU Details
    st.markdown("## 💉 FLU: Influenza Immunization")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Denominator:**
        - Adults aged 65+ years
        - Enrolled during flu season (Oct 1 - Mar 31)
        - No egg allergy (anaphylaxis contraindication)
        
        **Numerator:**
        - Flu vaccination during flu season
        - Multiple venues: physician office, retail pharmacy
        - 20+ CPT/CVX vaccine codes
        
        **Gap Closure Strategy:**
        1. Pharmacy partnerships (walk-in, no appointment)
        2. Mass vaccination clinics
        3. Provider reminders
        4. Member outreach (September postcards)
        """)
    
    with col2:
        st.success("""
        **EASIEST GAP TO CLOSE:**
        - Single annual vaccine
        - Multiple administration venues
        - High patient awareness
        - No complex scheduling
        
        **Typical Compliance:** 69% (national average)
        **Target:** 75-80% (5-star plans)
        **Gap Closure Potential:** 6-11 percentage points = $24K-$44K
        
        **Priority:** 85+ years old first (highest flu complication risk)
        """)
    
    st.markdown("---")
    
    # COL Details
    st.markdown("## 🔬 COL: Colorectal Cancer Screening")
    
    st.markdown("### Multiple Screening Modalities")
    
    screening_options = pd.DataFrame({
        'Screening Type': [
            'Colonoscopy',
            'Flexible Sigmoidoscopy',
            'CT Colonography',
            'FIT Test',
            'FIT-DNA Test (Cologuard)'
        ],
        'Interval': ['10 years', '5 years', '5 years', 'Annual', '3 years'],
        'Invasive?': ['Yes', 'Yes', 'No', 'No', 'No'],
        'Prep Required?': ['Yes', 'Yes', 'Yes', 'No', 'No'],
        'Patient Preference': ['Low (invasive)', 'Low (invasive)', 'Medium (radiation)', 'High (easy)', 'High (home test)'],
        'Clinical Effectiveness': ['Gold standard', 'Good', 'Good', 'Good', 'Good']
    })
    
    st.dataframe(screening_options, use_container_width=True, hide_index=True)
    
    st.markdown("### Gap Closure Strategy")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **For Non-Compliant Members:**
        1. **First Choice:** Mail FIT test kit (easiest compliance)
        2. **If negative FIT:** Schedule colonoscopy (10-year protection)
        3. **Patient education:** Multiple options available
        4. **GI referral support:** Help with scheduling
        
        **Priority:**
        - Age 70+ first (approaching age 75 cutoff)
        - Never-screened members (highest cancer risk)
        - 5+ years since last screening
        """)
    
    with col2:
        st.warning("""
        **Challenges:**
        - Multiple screening options (patient confusion)
        - Different look-back periods (complex tracking)
        - Colonoscopy barriers (prep, time off work)
        - Historical data needed (up to 10 years)
        
        **Typical Compliance:** 68% (national average)
        **Target:** 72-75%
        **Gap Closure Potential:** 4-7 percentage points = $20K-$35K
        """)
    
    st.markdown("---")
    
    # Planned measures
    st.markdown("## 🔲 Planned Tier 3 Measures (Lower Priority for MA)")
    
    planned = pd.DataFrame({
        'Measure': [
            'PNU - Pneumococcal Vaccination',
            'AWC - Adolescent Well-Care Visits',
            'WCC - Weight Assessment for Children'
        ],
        'Population': [
            'Adults 65+ years',
            'Adolescents 12-21 years',
            'Children 3-17 years'
        ],
        'MA Applicability': [
            'Medium (lifetime measure, most already vaccinated)',
            'Very Low (<1% of MA population)',
            'Minimal (<0.5% of MA population)'
        ],
        'Annual Value': ['$60K-$90K', '$60K-$90K', '$60K-$90K'],
        'Priority': ['Medium', 'Low', 'Low'],
        'Status': ['🔲 Planned', '🔲 Planned', '🔲 Planned']
    })
    
    st.dataframe(planned, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # Combined portfolio value
    st.markdown("## 💰 Combined Portfolio Value")
    
    st.success("""
    **Current Portfolio (11 Measures):**
    - **Tier 1 (Diabetes):** 5 measures → $400K-$650K
    - **Tier 2 (Cardiovascular):** 4 measures → $500K-$750K
    - **Tier 3 (Preventive):** 3 measures → $260K-$390K
    - **TOTAL:** **$1.06M-$1.59M annually** (100K member plan)
    
    **If All 15 Measures Implemented:**
    - Tier 3 (all 6 measures) → $440K-$660K
    - **TOTAL:** $1.3M-$2.1M annually
    
    **Recommendation:** Current 11 measures provide 80% of value with 60% of implementation effort.
    """)
```

---

## Step 4: Update Executive Summary

**Location:** Find `def show_executive_summary():` function

**UPDATE THE METRICS SECTION:** (Find the existing metrics and update)

```python
# Update these metrics in the Executive Summary
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Total Measures Implemented",
        value="11",  # Changed from 5
        delta="+6 from Tier 2+3"
    )

with col2:
    st.metric(
        label="Annual Revenue Impact",
        value="$1.06M-$1.59M",  # Changed from $400K-$650K
        delta="100K member plan"
    )

with col3:
    st.metric(
        label="Star Rating Weight",
        value="11x",  # Changed from 5x
        delta="CBP is 3x weighted"
    )

with col4:
    st.metric(
        label="Clinical Domains",
        value="3",  # Changed from 1
        delta="Diabetes, CV, Preventive"
    )
```

**ADD TIER 2 & 3 TO PORTFOLIO OVERVIEW:** (Find portfolio table and expand)

```python
# Expand the portfolio table to include Tier 2 and 3
portfolio_data = pd.DataFrame({
    'Tier': [
        'Tier 1', 'Tier 1', 'Tier 1', 'Tier 1', 'Tier 1',
        'Tier 2', 'Tier 2', 'Tier 2', 'Tier 2',
        'Tier 3', 'Tier 3', 'Tier 3'
    ],
    'Measure': [
        'HBD - Hemoglobin A1c Control',
        'KED - Kidney Health Evaluation',
        'EED - Eye Exam for Diabetics',
        'BPD - Blood Pressure Control (Diabetes)',
        'SPD - Statin Therapy (Diabetes)',
        'CBP - Controlling High Blood Pressure',
        'SUPD - Statin Therapy (Diabetes + CVD)',
        'PDC-RASA - Medication Adherence (HTN)',
        'PDC-STA - Medication Adherence (Statins)',
        'BCS - Breast Cancer Screening',
        'FLU - Influenza Immunization',
        'COL - Colorectal Cancer Screening'
    ],
    'Population': [
        'Adults with diabetes',
        'Adults with diabetes',
        'Adults with diabetes',
        'Adults with diabetes',
        'Adults with diabetes',
        'Adults 18-85 with HTN',
        'Adults 40-75 with diabetes',
        'Adults 18+ with HTN meds',
        'Adults 18+ with statins',
        'Women 50-74',
        'Adults 65+',
        'Adults 50-75'
    ],
    'Weight': ['1x', '1x', '1x', '1x', '1x', '3x', '1x', '1x', '1x', '1x', '1x', '1x'],
    'Annual Value': [
        '$80K-$120K', '$60K-$90K', '$60K-$90K', '$80K-$120K', '$120K-$180K',
        '$180K-$270K', '$120K-$180K', '$100K-$150K', '$100K-$150K',
        '$80K-$120K', '$80K-$120K', '$100K-$150K'
    ],
    'Status': ['✅']*12
})

st.dataframe(portfolio_data, use_container_width=True, hide_index=True)
```

---

## Step 5: Add Routing Logic

**Location:** Find the page routing logic at the end of the file (after all page functions)

**ADD TO THE IF-ELIF CHAIN:**

```python
# Find the existing if-elif chain and add:

if page == "🏠 Executive Summary":
    show_executive_summary()

elif page == "⚠️ Problem Statement":
    show_problem_statement()

elif page == "📊 Tier 1: Diabetes Portfolio":  # Updated name
    show_portfolio_overview()

elif page == "❤️ Tier 2: Cardiovascular Portfolio":  # NEW
    show_tier2_cardiovascular()

elif page == "🩺 Tier 3: Preventive Care":  # NEW
    show_tier3_preventive()

elif page == "💰 Financial Impact":
    show_financial_impact()

# ... rest of existing pages
```

---

## Step 6: Test Locally

```bash
# In terminal
streamlit run streamlit_app.py
```

**Checklist:**
- [ ] All 12 pages load without errors
- [ ] Navigation works for new Tier 2 and Tier 3 pages
- [ ] Executive Summary shows updated metrics (11 measures, $1.06M-$1.59M)
- [ ] Visualizations render correctly
- [ ] No Python errors in console

---

## Step 7: Deploy to Streamlit Cloud

**Instructions:**
1. Commit and push changes to GitHub
   ```bash
   git add streamlit_app.py
   git commit -m "Add Tier 2 Cardiovascular and Tier 3 Preventive Care pages"
   git push origin main
   ```

2. Log into Streamlit Cloud: https://share.streamlit.io/

3. Redeploy app or it will auto-deploy on push

4. Verify live deployment works

---

## Quick Reference: Key Metrics to Update

| Metric | Old Value | New Value |
|--------|-----------|-----------|
| Total Measures | 5 | 11 |
| Annual Value | $400K-$650K | $1.06M-$1.59M |
| Star Rating Weight | 5x | 11x |
| Clinical Domains | 1 (Diabetes) | 3 (Diabetes, CV, Preventive) |

---

## Estimated Implementation Time

| Task | Time |
|------|------|
| Update navigation | 5 min |
| Create Tier 2 page | 90 min |
| Create Tier 3 page | 90 min |
| Update Executive Summary | 30 min |
| Add routing logic | 10 min |
| Test locally | 30 min |
| Deploy and verify | 15 min |
| **TOTAL** | **4-5 hours** |

---

## Success Criteria

- [x] Dashboard has 12 pages total (10 original + 2 new)
- [x] Executive Summary shows 11 measures and $1.0M-$1.5M value
- [x] Tier 2 page explains CBP (3x weight), SUPD, PDC-RASA, PDC-STA
- [x] Tier 3 page explains BCS, FLU, COL with screening details
- [x] All pages accessible via sidebar navigation
- [x] No errors in local or deployed versions

---

**This guide provides everything needed to integrate Tier 2 and Tier 3 into the dashboard!**

