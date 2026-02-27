Claude rules

1. First think through the problem, read the codebase for relevant files, and write a plan to tasks/todo.md.
2. The plan should have a list of todo items that you can check off as you complete them
3. Before you begin working, check in with me and I will verify the plan.
4. Then, begin working on the todo items, marking them as complete as you go.
5. Please every step of the way just give me a high level explanation of what changes you made
6. Make every task and code change you do as simple as possible. We want to avoid making any massive or complex changes. Every change should impact as little code as possible. Everything is about simplicity.
7. Finally, create a [todo.md](http://todo.md/) file and add a review section to the [todo.md](http://todo.md/) file with a summary of the changes you made and any other relevant information.

Security prompt: Please check through all the code you just wrote and make sure it follows security best practices. make sure there are no sensitive information in the front and there are no vulnerabilities that can be exploited

Learning from Claude prompt: Please explain the functionality and code you just built out in detail. Walk me through what you changed and how it works.

Act like you’re a senior engineer teaching me code

# HEDIS GSD Prediction Engine - Development Plan 📋

## 🎯 Project Overview

**Goal:** Build a production-ready AI system for predicting diabetic patients at risk of poor glycemic control to improve HEDIS GSD measure performance.

**Current State:** 
- ✅ Trained logistic regression model (AUC-ROC = 0.91)
- ✅ Feature engineering completed (25 features)
- ✅ Model artifacts saved (model.pkl, scaler.pkl)
- ❌ No source code or notebooks
- ❌ No deployment infrastructure
- ❌ No documentation or API

---

## 📊 Current Assets Analysis

### ✅ What We Have
- **Models:** `logistic_regression_final.pkl`, `scaler.pkl`
- **Features:** 25 engineered features (demographics, comorbidities, utilization)
- **Data:** Processed population dataset (24,935 diabetic members)
- **Performance:** AUC-ROC = 0.91 on test set
- **Visualizations:** SHAP plots and model comparisons

### ❌ What We Need to Build
- **Source Code:** Python modules for data processing, training, prediction
- **Notebooks:** Analysis and model development documentation
- **API:** REST endpoint for predictions
- **Documentation:** Technical specs, API docs, deployment guides
- **Infrastructure:** Docker, CI/CD, monitoring
- **Testing:** Unit tests, integration tests, model validation

---

## 🚀 Development Phases

### Phase 1: Foundation & Code Reconstruction (Weeks 1-2)
**Goal:** Recreate the analysis and build foundational code structure

#### 1.1 Data Pipeline Reconstruction
- [ ] **Task:** Create `src/data/` module
  - [ ] `data_loader.py` - Load and validate CMS DE-SynPUF data
  - [ ] `feature_engineering.py` - Recreate feature engineering pipeline
  - [ ] `data_preprocessing.py` - Data cleaning and validation
  - [ ] **Question:** Do you have the original raw CMS data files? Yes

#### 1.2 Model Development Recreation
- [ ] **Task:** Create `notebooks/01_data_exploration.ipynb`
  - [ ] Data exploration and EDA
  - [ ] Feature engineering walkthrough
  - [ ] Model training and validation
  - [ ] SHAP analysis and interpretation
  - [ ] **Question:** Do you want to recreate the exact same model or explore improvements? Same with improvements

#### 1.3 Model Package Creation
- [ ] **Task:** Create `src/models/` module
  - [ ] `trainer.py` - Model training pipeline
  - [ ] `predictor.py` - Prediction interface
  - [ ] `evaluator.py` - Model evaluation metrics
  - [ ] `serializer.py` - Model save/load utilities

#### 1.4 Configuration Management
- [ ] **Task:** Create configuration system
  - [ ] `config.yaml` - Model parameters, paths, settings
  - [ ] `src/config/` - Configuration management module
  - [ ] Environment-specific configs (dev, prod)

**Success Criteria:**
- ✅ Reproduce original model performance
- ✅ Clean, documented code structure
- ✅ Complete analysis notebook
- ✅ All dependencies specified

---

### Phase 2: API Development & Testing (Weeks 3-4)
**Goal:** Build production-ready API with comprehensive testing

#### 2.1 REST API Development
- [ ] **Task:** Create `src/api/` module
  - [ ] `app.py` - FastAPI application
  - [ ] `endpoints/` - Prediction, health, model info endpoints
  - [ ] `schemas/` - Pydantic models for request/response
  - [ ] `middleware/` - Authentication, logging, error handling

#### 2.2 API Endpoints Design
- [ ] **Task:** Define API specification
  - [ ] `POST /predict` - Single member prediction
  - [ ] `POST /predict/batch` - Batch predictions
  - [ ] `GET /model/info` - Model metadata and performance
  - [ ] `GET /health` - Health check endpoint
  - [ ] **Question:** Do you need authentication/authorization? No

#### 2.3 Testing Framework
- [ ] **Task:** Create comprehensive test suite
  - [ ] `tests/unit/` - Unit tests for all modules
  - [ ] `tests/integration/` - API integration tests
  - [ ] `tests/model/` - Model validation tests
  - [ ] `tests/fixtures/` - Test data and fixtures
  - [ ] **Question:** What test coverage percentage do you want? Please recommend

#### 2.4 Documentation
- [ ] **Task:** Create API documentation
  - [ ] OpenAPI/Swagger specification
  - [ ] API usage examples
  - [ ] Error handling documentation
  - [ ] **Question:** Do you prefer Swagger UI or custom docs? Please recommend

**Success Criteria:**
- ✅ Fully functional REST API
- ✅ 90%+ test coverage
- ✅ Complete API documentation
- ✅ Performance benchmarks

---

### Phase 3: Deployment & Infrastructure (Weeks 5-6)
**Goal:** Deploy to production with monitoring and CI/CD

#### 3.1 Containerization
- [ ] **Task:** Create Docker setup
  - [ ] `Dockerfile` - Application container
  - [ ] `docker-compose.yml` - Local development
  - [ ] `docker-compose.prod.yml` - Production deployment
  - [ ] **Question:** Do you have a preferred cloud platform (AWS, GCP, Azure)?

#### 3.2 CI/CD Pipeline
- [ ] **Task:** Set up automated deployment
  - [ ] GitHub Actions workflows
  - [ ] Automated testing on PR
  - [ ] Model validation checks
  - [ ] Deployment to staging/production
  - [ ] **Question:** Do you have deployment preferences?

#### 3.3 Monitoring & Logging
- [ ] **Task:** Implement observability
  - [ ] Application logging (structured logs)
  - [ ] Performance monitoring
  - [ ] Model drift detection
  - [ ] Health check endpoints
  - [ ] **Question:** Do you have monitoring tools (DataDog, New Relic, etc.)?

#### 3.4 Security & Compliance
- [ ] **Task:** Implement security measures
  - [ ] Input validation and sanitization
  - [ ] Rate limiting
  - [ ] HTTPS/TLS configuration
  - [ ] Security headers
  - [ ] **Question:** Any specific compliance requirements (HIPAA, SOC2)?

**Success Criteria:**
- ✅ Production deployment
- ✅ Automated CI/CD pipeline
- ✅ Monitoring and alerting
- ✅ Security compliance

---

### Phase 4: Advanced Features & Optimization (Weeks 7-8)
**Goal:** Add advanced features and optimize performance

#### 4.1 Model Improvements
- [ ] **Task:** Explore model enhancements
  - [ ] Ensemble methods (Random Forest + Logistic Regression)
  - [ ] Feature selection optimization
  - [ ] Hyperparameter tuning
  - [ ] Cross-validation improvements
  - [ ] **Question:** Are you open to trying different algorithms?

#### 4.2 Additional Data Sources
- [ ] **Task:** Integrate more data
  - [ ] Carrier claims data
  - [ ] Prescription drug data
  - [ ] Medication adherence features
  - [ ] Social determinants of health
  - [ ] **Question:** Do you have access to additional data sources?

#### 4.3 Real-time Features
- [ ] **Task:** Add real-time capabilities
  - [ ] Streaming predictions
  - [ ] Real-time model updates
  - [ ] Event-driven architecture
  - [ ] **Question:** Do you need real-time predictions or batch is sufficient?

#### 4.4 Dashboard & Visualization
- [ ] **Task:** Create user interface
  - [ ] Streamlit dashboard
  - [ ] Model performance monitoring
  - [ ] Prediction explanations (SHAP)
  - [ ] Member risk profiles
  - [ ] **Question:** Who will be the primary users (data scientists, clinicians, administrators)?

**Success Criteria:**
- ✅ Improved model performance
- ✅ Additional data integration
- ✅ User-friendly dashboard
- ✅ Real-time capabilities

---

### Phase 5: Production Operations & Scaling (Weeks 9-10)
**Goal:** Optimize for production scale and operations

#### 5.1 Performance Optimization
- [ ] **Task:** Optimize for scale
  - [ ] Batch prediction optimization
  - [ ] Caching strategies
  - [ ] Database optimization
  - [ ] Load balancing
  - [ ] **Question:** What's your expected prediction volume?

#### 5.2 Model Management
- [ ] **Task:** Implement MLOps practices
  - [ ] Model versioning
  - [ ] A/B testing framework
  - [ ] Automated retraining pipeline
  - [ ] Model rollback capabilities
  - [ ] **Question:** How often should the model be retrained?

#### 5.3 Data Pipeline
- [ ] **Task:** Production data pipeline
  - [ ] Automated data ingestion
  - [ ] Data quality monitoring
  - [ ] Feature store implementation
  - [ ] Data lineage tracking
  - [ ] **Question:** Do you have a data engineering team?

#### 5.4 Business Integration
- [ ] **Task:** Integrate with business systems
  - [ ] CRM integration
  - [ ] Care management system integration
  - [ ] Reporting and analytics
  - [ ] Business process automation
  - [ ] **Question:** What systems do you need to integrate with?

**Success Criteria:**
- ✅ Production-scale performance
- ✅ Automated model management
- ✅ Business system integration
- ✅ Operational excellence

---

## 🔧 Technical Decisions Needed

### Immediate Decisions (Phase 1)
1. **Data Access:** Do you have the original CMS DE-SynPUF raw data files?
2. **Model Recreation:** Should we recreate the exact same model or explore improvements?
3. **Code Structure:** Any preferences for project structure or coding standards?

### Architecture Decisions (Phase 2-3)
4. **API Framework:** FastAPI vs Flask vs Django?
5. **Database:** Do you need a database for storing predictions/history?
6. **Cloud Platform:** AWS, GCP, Azure, or on-premises?
7. **Authentication:** Do you need user authentication/authorization?

### Business Decisions (Phase 4-5)
8. **Users:** Who will be the primary users of the system?
9. **Integration:** What existing systems need integration?
10. **Compliance:** Any specific compliance requirements?
11. **Scale:** Expected prediction volume and performance requirements?

---

## 📋 Task Tracking

### Phase 1: Foundation (Weeks 1-2)
- [ ] Data pipeline reconstruction
- [ ] Model development recreation
- [ ] Model package creation
- [ ] Configuration management

### Phase 2: API Development (Weeks 3-4)
- [ ] REST API development
- [ ] API endpoints design
- [ ] Testing framework
- [ ] Documentation

### Phase 3: Deployment (Weeks 5-6)
- [ ] Containerization
- [ ] CI/CD pipeline
- [ ] Monitoring & logging
- [ ] Security & compliance

### Phase 4: Advanced Features (Weeks 7-8)
- [ ] Model improvements
- [ ] Additional data sources
- [ ] Real-time features
- [ ] Dashboard & visualization

### Phase 5: Production Operations (Weeks 9-10)
- [ ] Performance optimization
- [ ] Model management
- [ ] Data pipeline
- [ ] Business integration

---

## 🎯 Success Metrics

### Technical Metrics
- **Model Performance:** Maintain AUC-ROC ≥ 0.90
- **API Performance:** < 100ms response time for single predictions
- **Test Coverage:** ≥ 90% code coverage
- **Uptime:** ≥ 99.9% availability

### Business Metrics
- **Prediction Accuracy:** Correctly identify 80%+ of high-risk members
- **Processing Speed:** Handle 10,000+ predictions per hour
- **User Adoption:** Active usage by target user groups
- **ROI:** Demonstrate measurable business value

---

## 📞 Next Steps

1. **Review this plan** and provide feedback on priorities
2. **Answer the technical decisions** marked with questions
3. **Confirm timeline** and resource availability
4. **Start Phase 1** with data pipeline reconstruction

**Ready to begin?** Let me know which phase you'd like to start with and I'll create the detailed implementation plan for that phase.

