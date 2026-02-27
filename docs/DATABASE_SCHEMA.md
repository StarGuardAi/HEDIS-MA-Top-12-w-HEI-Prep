# Database Schema: Data Model Documentation

**PostgreSQL schema supporting HIPAA-compliant healthcare AI system**

---

## 📊 Schema Overview

### Database: `hedis_optimizer`

**Tables:**
- **members**: Member demographics and attributes
- **claims**: Medical claims data
- **labs**: Laboratory results
- **pharmacy**: Pharmacy claims
- **gaps**: Gap-in-care records
- **predictions**: ML model predictions
- **audit_logs**: Complete audit trail
- **context_cache**: Context engineering cache
- **interventions**: Intervention records

---

## 🗄️ Table Definitions

### Members Table

**Table**: `members`

**Columns:**
```sql
CREATE TABLE members (
    member_id VARCHAR(50) PRIMARY KEY,
    age INTEGER,
    gender VARCHAR(10),
    race VARCHAR(50),
    ethnicity VARCHAR(50),
    zip_code VARCHAR(10),
    insurance_type VARCHAR(50),
    enrollment_date DATE,
    disenrollment_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Indexes:**
- `idx_members_zip_code`: On `zip_code`
- `idx_members_enrollment`: On `enrollment_date`, `disenrollment_date`

### Claims Table

**Table**: `claims`

**Columns:**
```sql
CREATE TABLE claims (
    claim_id VARCHAR(50) PRIMARY KEY,
    member_id VARCHAR(50) REFERENCES members(member_id),
    claim_date DATE,
    service_date DATE,
    provider_id VARCHAR(50),
    diagnosis_code VARCHAR(20),
    procedure_code VARCHAR(20),
    claim_amount DECIMAL(10, 2),
    claim_type VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Indexes:**
- `idx_claims_member_id`: On `member_id`
- `idx_claims_service_date`: On `service_date`
- `idx_claims_diagnosis`: On `diagnosis_code`

### Labs Table

**Table**: `labs`

**Columns:**
```sql
CREATE TABLE labs (
    lab_id VARCHAR(50) PRIMARY KEY,
    member_id VARCHAR(50) REFERENCES members(member_id),
    lab_date DATE,
    lab_type VARCHAR(50),
    lab_code VARCHAR(20),
    lab_value DECIMAL(10, 2),
    lab_unit VARCHAR(20),
    provider_id VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Indexes:**
- `idx_labs_member_id`: On `member_id`
- `idx_labs_lab_date`: On `lab_date`
- `idx_labs_lab_type`: On `lab_type`

### Pharmacy Table

**Table**: `pharmacy`

**Columns:**
```sql
CREATE TABLE pharmacy (
    pharmacy_id VARCHAR(50) PRIMARY KEY,
    member_id VARCHAR(50) REFERENCES members(member_id),
    fill_date DATE,
    medication_name VARCHAR(100),
    ndc_code VARCHAR(20),
    days_supply INTEGER,
    quantity INTEGER,
    provider_id VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Indexes:**
- `idx_pharmacy_member_id`: On `member_id`
- `idx_pharmacy_fill_date`: On `fill_date`
- `idx_pharmacy_ndc`: On `ndc_code`

### Gaps Table

**Table**: `gaps`

**Columns:**
```sql
CREATE TABLE gaps (
    gap_id VARCHAR(50) PRIMARY KEY,
    member_id VARCHAR(50) REFERENCES members(member_id),
    measure_id VARCHAR(10),
    gap_status VARCHAR(20),
    gap_date DATE,
    closure_date DATE,
    intervention_id VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Indexes:**
- `idx_gaps_member_id`: On `member_id`
- `idx_gaps_measure_id`: On `measure_id`
- `idx_gaps_status`: On `gap_status`

### Predictions Table

**Table**: `predictions`

**Columns:**
```sql
CREATE TABLE predictions (
    prediction_id VARCHAR(50) PRIMARY KEY,
    member_id VARCHAR(50) REFERENCES members(member_id),
    measure_id VARCHAR(10),
    prediction_date DATE,
    prediction_probability DECIMAL(5, 4),
    prediction_confidence VARCHAR(20),
    model_version VARCHAR(20),
    features JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Indexes:**
- `idx_predictions_member_id`: On `member_id`
- `idx_predictions_measure_id`: On `measure_id`
- `idx_predictions_date`: On `prediction_date`

### Audit Logs Table

**Table**: `audit_logs`

**Columns:**
```sql
CREATE TABLE audit_logs (
    log_id VARCHAR(50) PRIMARY KEY,
    user_id VARCHAR(50),
    query_text TEXT,
    query_type VARCHAR(50),
    context_layers JSONB,
    tools_executed JSONB,
    response_text TEXT,
    response_time_ms INTEGER,
    phi_detected BOOLEAN,
    validation_passed BOOLEAN,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Indexes:**
- `idx_audit_logs_user_id`: On `user_id`
- `idx_audit_logs_created_at`: On `created_at`
- `idx_audit_logs_phi_detected`: On `phi_detected`

### Context Cache Table

**Table**: `context_cache`

**Columns:**
```sql
CREATE TABLE context_cache (
    cache_id VARCHAR(50) PRIMARY KEY,
    cache_key VARCHAR(255) UNIQUE,
    cache_layer VARCHAR(20),
    cache_content JSONB,
    ttl_seconds INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP
);
```

**Indexes:**
- `idx_context_cache_key`: On `cache_key`
- `idx_context_cache_expires`: On `expires_at`

---

## 🔗 Relationships

### Entity Relationship Diagram

```
members (1) ────< (many) claims
members (1) ────< (many) labs
members (1) ────< (many) pharmacy
members (1) ────< (many) gaps
members (1) ────< (many) predictions
gaps (many) ────> (1) interventions
```

---

## 🔒 Security Considerations

### Data De-identification

**PHI Fields Never Stored:**
- Social Security Numbers (SSN)
- Full names (stored as member_id only)
- Complete addresses (ZIP code only)
- Phone numbers
- Email addresses

**De-identified Fields:**
- Member IDs: Hashed identifiers
- Dates: Year and month only (no day)
- ZIP codes: First 3 digits only

### Access Control

**Role-Based Access:**
- **Admin**: Full access to all tables
- **Analyst**: Read-only access to de-identified data
- **API User**: Limited access to specific endpoints

**Audit Trail:**
- All queries logged in `audit_logs` table
- 7-year retention policy
- Encrypted log storage

---

## 📊 Performance Optimization

### Indexing Strategy

**Primary Indexes:**
- All primary keys indexed
- Foreign keys indexed
- Frequently queried columns indexed

**Composite Indexes:**
- `(member_id, measure_id)` for gap queries
- `(member_id, service_date)` for claims queries
- `(member_id, lab_date)` for lab queries

### Partitioning

**Partitioning Strategy:**
- **audit_logs**: Partitioned by `created_at` (monthly)
- **claims**: Partitioned by `service_date` (monthly)
- **labs**: Partitioned by `lab_date` (monthly)

---

## 🔄 Data Migration

### Migration Scripts

**Location**: `scripts/migrations/`

**Migration Files:**
- `001_create_tables.sql`: Initial table creation
- `002_create_indexes.sql`: Index creation
- `003_create_partitions.sql`: Partition creation
- `004_load_demo_data.sql`: Demo data loading

**Migration Command:**
```bash
python scripts/run_migrations.py
```

---

## 📞 Contact

**Robert Reichert**  
Healthcare AI Architect

📧 **Email**: reichert.starguardai@gmail.com  
🔗 **LinkedIn**: [rreichert-HEDIS-Data-Science-AI](https://www.linkedin.com/in/rreichert-HEDIS-Data-Science-AI)  
💻 **GitHub**: [StarGuardAi/HEDIS-MA-Top-12-w-HEI-Prep](https://github.com/StarGuardAi/HEDIS-MA-Top-12-w-HEI-Prep)

**Status**: Available for contract work starting **Late April 2025**

---

**Key Takeaway**: **Production-ready database schema** with **HIPAA compliance**, **performance optimization**, and **complete audit trails** for healthcare AI systems.



