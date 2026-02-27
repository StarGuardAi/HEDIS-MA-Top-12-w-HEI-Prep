# Phase 3: API Development & Testing - Implementation Plan

**Start Date:** October 22, 2025  
**Expected Duration:** 2-3 weeks  
**Target Completion:** Mid-November 2025  
**Status:** 🚀 READY TO START

---

## 🎯 Goal

Build a production-ready REST API that exposes the HEDIS GSD prediction model with comprehensive testing, documentation, and < 100ms response times.

---

## 📋 Success Criteria

- ✅ Fully functional REST API with FastAPI
- ✅ 90%+ API test coverage
- ✅ < 100ms response time for single predictions
- ✅ Complete OpenAPI/Swagger documentation
- ✅ All healthcare code reviews passed
- ✅ HIPAA-compliant request/response handling

---

## 🏗️ Architecture Overview

```
src/api/
├── __init__.py
├── app.py                    # FastAPI application entry point
├── endpoints/
│   ├── __init__.py
│   ├── prediction.py         # Prediction endpoints
│   ├── health.py             # Health check endpoints
│   └── model.py              # Model info endpoints
├── schemas/
│   ├── __init__.py
│   ├── request.py            # Pydantic request models
│   └── response.py           # Pydantic response models
├── middleware/
│   ├── __init__.py
│   ├── logging.py            # Request/response logging
│   └── error_handling.py     # Custom error handlers
└── dependencies.py           # Dependency injection

tests/api/
├── __init__.py
├── test_endpoints.py         # Endpoint tests
├── test_schemas.py           # Schema validation tests
├── test_integration.py       # Integration tests
└── test_performance.py       # Performance benchmarks
```

---

## 📝 Detailed Tasks

### Phase 3.1: FastAPI Application Setup (Days 1-3)

#### Task 3.1.1: Create FastAPI Project Structure
- [ ] Create `src/api/` package
- [ ] Create `app.py` with FastAPI instance
- [ ] Set up CORS middleware
- [ ] Configure Uvicorn server settings
- [ ] Add health check endpoint
- [ ] Create API versioning structure (v1)

**Deliverable:** Basic FastAPI app running on http://localhost:8000

#### Task 3.1.2: Request/Response Schemas
- [ ] Create Pydantic models for prediction requests
  - Single member prediction request
  - Batch prediction request
- [ ] Create Pydantic models for responses
  - Single prediction response
  - Batch prediction response
  - Model info response
  - Health check response
  - Error response
- [ ] Add validation rules
  - Age range validation (18-75)
  - Required field validation
  - Data type validation
- [ ] Add HIPAA-safe field descriptions

**Deliverable:** `schemas/request.py` and `schemas/response.py`

#### Task 3.1.3: Dependency Injection
- [ ] Create model loader dependency
- [ ] Create configuration loader dependency
- [ ] Add model caching (singleton pattern)
- [ ] Create PHI-safe logger dependency

**Deliverable:** `dependencies.py`

**Code Review:** `/review-security src/api/app.py src/api/schemas/`

---

### Phase 3.2: Prediction Endpoints (Days 4-7)

#### Task 3.2.1: Single Prediction Endpoint
- [ ] Create `POST /api/v1/predict` endpoint
- [ ] Load trained model from artifacts
- [ ] Validate input features
- [ ] Make prediction
- [ ] Return prediction with confidence score
- [ ] Add SHAP values for interpretability
- [ ] Handle missing features gracefully
- [ ] Add request/response logging (PHI-safe)

**Example Request:**
```json
{
  "member_id": "SYNTH_001234",  // Optional for tracking
  "age_at_my_end": 65,
  "is_female": 1,
  "is_white": 1,
  "has_diabetes_comprehensive": 1,
  "has_ckd": 0,
  "has_cvd": 1,
  "has_retinopathy": 0,
  "inpatient_claim_count": 2,
  "outpatient_claim_count": 8,
  "inpatient_total_payment": 15000.00,
  "outpatient_total_payment": 3200.00,
  ...
}
```

**Example Response:**
```json
{
  "prediction": 1,
  "risk_score": 0.73,
  "risk_level": "high",
  "confidence": 0.91,
  "shap_values": {
    "has_ckd": 0.15,
    "age_at_my_end": 0.12,
    "has_cvd": 0.10,
    ...
  },
  "top_risk_factors": [
    {"feature": "has_ckd", "impact": 0.15},
    {"feature": "age_at_my_end", "impact": 0.12},
    {"feature": "has_cvd", "impact": 0.10}
  ],
  "model_version": "1.0.0",
  "timestamp": "2025-10-22T12:30:45Z"
}
```

**Deliverable:** `endpoints/prediction.py` with single prediction

#### Task 3.2.2: Batch Prediction Endpoint
- [ ] Create `POST /api/v1/predict/batch` endpoint
- [ ] Accept list of member features
- [ ] Process predictions in batches
- [ ] Return array of predictions
- [ ] Add batch size limit (max 1000)
- [ ] Optimize for performance
- [ ] Add progress tracking for large batches

**Example Request:**
```json
{
  "members": [
    {"age_at_my_end": 65, "has_ckd": 1, ...},
    {"age_at_my_end": 45, "has_ckd": 0, ...},
    ...
  ]
}
```

**Example Response:**
```json
{
  "predictions": [
    {"member_index": 0, "risk_score": 0.73, ...},
    {"member_index": 1, "risk_score": 0.42, ...}
  ],
  "total_processed": 100,
  "high_risk_count": 25,
  "processing_time_ms": 85
}
```

**Deliverable:** Batch prediction endpoint

**Code Review:** `/review-performance endpoints/prediction.py`

---

### Phase 3.3: Model Info & Health Endpoints (Days 8-9)

#### Task 3.3.1: Model Info Endpoint
- [ ] Create `GET /api/v1/model/info` endpoint
- [ ] Return model metadata
  - Model type (Logistic Regression)
  - Version (1.0.0)
  - Training date
  - Performance metrics (AUC-ROC, sensitivity, etc.)
  - Feature list
  - HEDIS specification alignment
- [ ] Add model feature importance
- [ ] Include SHAP summary

**Example Response:**
```json
{
  "model_name": "HEDIS GSD Logistic Regression",
  "version": "1.0.0",
  "model_type": "LogisticRegression",
  "training_date": "2025-10-15",
  "performance": {
    "auc_roc": 0.91,
    "sensitivity": 0.87,
    "specificity": 0.81,
    "ppv": 0.83,
    "npv": 0.86
  },
  "features": ["age_at_my_end", "has_ckd", ...],
  "feature_count": 25,
  "hedis_specification": "MY2023 Volume 2 - HBD",
  "compliance": {
    "hipaa": true,
    "hedis_aligned": true
  }
}
```

**Deliverable:** `endpoints/model.py`

#### Task 3.3.2: Health Check Endpoints
- [ ] Create `GET /health` endpoint (simple up/down)
- [ ] Create `GET /health/ready` endpoint (ready for requests)
- [ ] Create `GET /health/live` endpoint (liveness probe)
- [ ] Check model loaded status
- [ ] Check disk space
- [ ] Check memory usage
- [ ] Return system status

**Example Response:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "uptime_seconds": 3600,
  "version": "1.0.0",
  "timestamp": "2025-10-22T12:30:45Z"
}
```

**Deliverable:** `endpoints/health.py`

**Code Review:** `/review-security endpoints/model.py endpoints/health.py`

---

### Phase 3.4: Middleware & Error Handling (Days 10-11)

#### Task 3.4.1: Logging Middleware
- [ ] Create request/response logging middleware
- [ ] Log request method, path, timestamp
- [ ] Log response status code, time taken
- [ ] **Do NOT log** request bodies (may contain PHI)
- [ ] Log aggregate statistics only
- [ ] Add correlation IDs for tracing

**Deliverable:** `middleware/logging.py`

**Code Review:** `/review-hipaa middleware/logging.py`

#### Task 3.4.2: Error Handling
- [ ] Create custom exception classes
  - `ModelNotLoadedError`
  - `InvalidFeatureError`
  - `ValidationError`
  - `RateLimitError`
- [ ] Create global exception handlers
- [ ] Return user-friendly error messages
- [ ] Log detailed errors server-side
- [ ] Add error codes for client integration

**Example Error Response:**
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid age_at_my_end value",
    "details": "Age must be between 18 and 75",
    "timestamp": "2025-10-22T12:30:45Z"
  }
}
```

**Deliverable:** `middleware/error_handling.py`

---

### Phase 3.5: Testing & Documentation (Days 12-15)

#### Task 3.5.1: Unit Tests
- [ ] Test schema validation
  - Valid inputs pass
  - Invalid inputs rejected
  - Required fields enforced
- [ ] Test prediction logic
  - Single prediction accuracy
  - Batch prediction accuracy
  - Feature validation
- [ ] Test error handling
  - Missing model
  - Invalid features
  - Malformed requests

**Deliverable:** `tests/api/test_schemas.py`, `tests/api/test_endpoints.py`

#### Task 3.5.2: Integration Tests
- [ ] Test full request/response cycle
- [ ] Test with real model predictions
- [ ] Test batch processing
- [ ] Test error responses
- [ ] Test health check endpoints

**Deliverable:** `tests/api/test_integration.py`

#### Task 3.5.3: Performance Tests
- [ ] Benchmark single prediction response time
  - Target: < 100ms
- [ ] Benchmark batch prediction throughput
  - Target: > 1000 predictions/second
- [ ] Test concurrent requests
  - Target: 100 concurrent users
- [ ] Memory leak testing
- [ ] Load testing

**Deliverable:** `tests/api/test_performance.py`

**Code Review:** `/review-testing tests/api/`

#### Task 3.5.4: API Documentation
- [ ] Enable Swagger UI (`/docs`)
- [ ] Enable ReDoc (`/redoc`)
- [ ] Write comprehensive endpoint descriptions
- [ ] Add request/response examples
- [ ] Document error codes
- [ ] Create API usage guide
- [ ] Add authentication docs (if needed)

**Deliverable:** Auto-generated OpenAPI docs + `docs/API_GUIDE.md`

---

### Phase 3.6: Deployment Preparation (Days 16-18)

#### Task 3.6.1: Configuration
- [ ] Create API configuration file
- [ ] Add environment variables
  - `API_HOST`, `API_PORT`
  - `MODEL_PATH`
  - `LOG_LEVEL`
  - `ENABLE_CORS`
- [ ] Create Docker-ready config
- [ ] Add production settings
  - Rate limiting
  - Request size limits
  - Timeout settings

**Deliverable:** `api_config.yaml`

#### Task 3.6.2: Requirements & Setup
- [ ] Update `requirements.txt` with FastAPI dependencies
  - `fastapi`
  - `uvicorn`
  - `pydantic`
  - `python-multipart`
- [ ] Create `start_api.sh` script
- [ ] Create `start_api.bat` script (Windows)
- [ ] Add API section to README

**Deliverable:** Updated `requirements.txt`, startup scripts

#### Task 3.6.3: Final Code Reviews
- [ ] `/review-security src/api/**/*.py`
- [ ] `/review-hipaa src/api/**/*.py`
- [ ] `/review-performance src/api/**/*.py`
- [ ] `/review-gen-ai src/api/**/*.py` (if using LLMs)
- [ ] Address all findings

**Deliverable:** Code review report

---

## 📊 Acceptance Criteria Checklist

### Functional Requirements
- [ ] Single prediction endpoint works
- [ ] Batch prediction endpoint works
- [ ] Model info endpoint returns correct data
- [ ] Health check endpoints work
- [ ] All endpoints return valid JSON
- [ ] Input validation works correctly
- [ ] Error handling works properly

### Performance Requirements
- [ ] Single prediction < 100ms (p95)
- [ ] Batch prediction > 1000/sec
- [ ] Can handle 100 concurrent requests
- [ ] No memory leaks after 10,000 requests
- [ ] API starts up in < 10 seconds

### Quality Requirements
- [ ] 90%+ test coverage
- [ ] All tests passing
- [ ] No linting errors
- [ ] All code reviews passed
- [ ] Documentation complete

### Healthcare Compliance
- [ ] No PHI in logs
- [ ] Request/response validation
- [ ] HIPAA-safe error messages
- [ ] Audit logging implemented
- [ ] Model predictions auditable

---

## 🛠️ Technology Stack

### Core Framework
- **FastAPI** 0.115.0 - Modern, fast API framework
- **Uvicorn** - ASGI server
- **Pydantic** - Data validation

### Testing
- **pytest** - Unit testing
- **pytest-asyncio** - Async test support
- **httpx** - HTTP client for testing
- **locust** - Load testing (optional)

### Documentation
- **Swagger UI** (built-in to FastAPI)
- **ReDoc** (built-in to FastAPI)
- **OpenAPI** 3.0 spec (auto-generated)

---

## 📈 Progress Tracking

### Week 1 (Days 1-7)
- [ ] FastAPI setup complete
- [ ] Schemas defined
- [ ] Single prediction endpoint working
- [ ] Batch prediction endpoint working

### Week 2 (Days 8-14)
- [ ] Model info endpoint complete
- [ ] Health check endpoints complete
- [ ] Middleware implemented
- [ ] Error handling complete
- [ ] Unit tests written

### Week 3 (Days 15-18)
- [ ] Integration tests complete
- [ ] Performance tests complete
- [ ] Documentation complete
- [ ] All code reviews passed
- [ ] Deployment ready

---

## 🚀 Next Steps After Phase 3

**Phase 4: Deployment & Infrastructure**
- Dockerize the application
- Set up CI/CD pipeline
- Deploy to cloud (AWS/GCP/Azure)
- Set up monitoring and logging
- Implement rate limiting
- Add authentication (if needed)

---

## 📞 Questions for User

1. **Authentication:** Do we need API authentication/authorization?
   - Options: API keys, OAuth2, JWT
   - Recommendation: API keys for simplicity

2. **Rate Limiting:** Should we implement rate limiting?
   - Recommendation: Yes (e.g., 1000 requests/hour per key)

3. **Caching:** Should we cache predictions?
   - Recommendation: No (predictions should be fresh)

4. **Database:** Do we need to store prediction history?
   - Recommendation: Optional (can add in Phase 5)

---

## 📝 Notes

- Keep API responses PHI-safe (no member names, SSNs, etc.)
- Log aggregate statistics only, not individual predictions
- Use correlation IDs for request tracing
- Consider adding API versioning (/api/v1/ prefix)
- Plan for backward compatibility

---

**Status:** 🚀 Ready to Start  
**Created:** October 21, 2025  
**Owner:** Boba Reichert

