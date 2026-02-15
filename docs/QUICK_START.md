# Quick Start Guide: Get Started in 15 Minutes

**HIPAA-compliant healthcare AI system ready for deployment**

---

## 🚀 Prerequisites

### System Requirements

- **Python 3.11+**: Core development language
- **PostgreSQL** (optional): For production deployment
- **Docker** (optional): For containerized deployment
- **Git**: Version control

### Dependencies

- **Streamlit**: Dashboard framework
- **FastAPI**: API framework
- **XGBoost/LightGBM**: Machine learning models
- **Ollama**: Local LLM server
- **ChromaDB**: Vector database

---

## 📦 Installation

### Step 1: Clone Repository

```bash
git clone https://github.com/StarGuardAi/HEDIS-MA-Top-12-w-HEI-Prep.git
cd HEDIS-MA-Top-12-w-HEI-Prep
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Set Up Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your configuration
# - Database connection
# - API keys (if needed)
# - Security settings
```

### Step 4: Initialize Database

```bash
# SQLite (development)
python scripts/init_database.py

# PostgreSQL (production)
python scripts/init_database.py --postgres
```

---

## 🎯 Quick Start Options

### Option 1: Streamlit Dashboard (Recommended)

**Fastest way to explore the system:**

```bash
# Navigate to dashboard directory
cd Artifacts/project/phase4_dashboard

# Launch dashboard
streamlit run app.py
```

**Access**: http://localhost:8501

**Features Available:**
- 22+ dashboard pages
- Interactive visualizations
- Secure AI chatbot
- ROI calculator
- Star rating simulator

### Option 2: FastAPI Backend

**For API integration:**

```bash
# Navigate to project directory
cd project

# Launch API server
uvicorn src.api.main:app --reload
```

**Access**: http://localhost:8000

**API Documentation**: http://localhost:8000/docs

### Option 3: Docker Deployment

**For production deployment:**

```bash
# Build Docker image
docker build -t hedis-optimizer .

# Run container
docker run -p 8501:8501 hedis-optimizer
```

---

## 🧠 Context Engineering Setup

### Step 1: Install Ollama

**Local LLM server:**

```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Pull model
ollama pull llama2
```

### Step 2: Initialize Vector Store

```bash
# Initialize ChromaDB
python scripts/init_vector_store.py
```

### Step 3: Test Context Engineering

```bash
# Test context builder
python -c "
from services.context_engineering import HierarchicalContextBuilder
builder = HierarchicalContextBuilder()
context = builder.build_context('Calculate ROI for diabetes interventions')
print(f'Efficiency: {context[\"metadata\"][\"efficiency_score\"]}%')
"
```

---

## 🤖 Agentic RAG Setup

### Step 1: Initialize Agentic RAG

```bash
# Test agentic planner
python -c "
from services.agentic_rag import AgenticPlanner
planner = AgenticPlanner()
plan = planner.create_plan('Find gaps and calculate ROI')
print(f'Steps: {plan[\"total_steps\"]}, Time: {plan[\"estimated_time\"]}s')
"
```

### Step 2: Test Secure Chatbot

1. Launch Streamlit dashboard
2. Navigate to "Secure AI Chatbot" page
3. Select "Context-Aware RAG" mode
4. Enter test query: "Calculate ROI for HbA1c testing interventions"
5. Review results and performance metrics

---

## 📊 Demo Data

### Synthetic Data Available

**Pre-loaded demo data:**
- 100K synthetic members
- 12 HEDIS measures
- Claims, labs, pharmacy data
- SDOH data

**No PHI**: All data is synthetic and HIPAA-compliant

### Load Demo Data

```bash
# Load demo data
python scripts/load_demo_data.py
```

---

## 🧪 Testing

### Run Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=src

# View coverage report
open htmlcov/index.html
```

### Test Coverage

- **99% code coverage**: Comprehensive test suite
- **200+ tests**: Unit, integration, and end-to-end tests

---

## 📈 Performance Verification

### Verify Context Engineering

```bash
# Test cache hit rate
python scripts/test_context_engineering.py

# Expected results:
# - Cache hit rate: ~82%
# - Response time: ~7.2s
# - Cost per query: ~$0.006
```

### Verify Agentic RAG

```bash
# Test agentic RAG
python scripts/test_agentic_rag.py

# Expected results:
# - Step success rate: ~94%
# - Self-correction success: ~98%
# - Avg steps per query: ~3.6
```

---

## 🔒 Security Verification

### Verify PHI Detection

```bash
# Test PHI detection
python scripts/test_phi_detection.py

# Expected results:
# - PHI detection rate: 100%
# - False positive rate: <1%
# - Validation time: <50ms
```

### Verify Audit Trails

```bash
# Test audit logging
python scripts/test_audit_trails.py

# Expected results:
# - Log coverage: 100%
# - Log encryption: 100%
# - Log retention: 7 years
```

---

## 🎓 Next Steps

### Explore Documentation

1. **[Context Engineering Guide](CONTEXT_ENGINEERING_AGENTIC_RAG.md)**: Deep-dive into context engineering
2. **[Security Architecture](SECURITY_ARCHITECTURE.md)**: Security and compliance details
3. **[API Documentation](API_DOCUMENTATION.md)**: Complete API reference
4. **[Deployment Guide](DEPLOYMENT.md)**: Production deployment instructions

### Explore Dashboard

1. **ROI Calculator**: Interactive financial projections
2. **Star Rating Simulator**: Crisis prevention scenarios
3. **Secure AI Chatbot**: HIPAA-compliant conversational interface
4. **AI Capabilities Demo**: Context engineering showcase

### Explore Code

1. **Services**: `services/context_engineering/`, `services/agentic_rag/`
2. **API**: `src/api/main.py`
3. **Dashboard**: `Artifacts/project/phase4_dashboard/app.py`
4. **Tests**: `tests/`

---

## 🐛 Troubleshooting

### Common Issues

**Issue**: Ollama not found
```bash
# Solution: Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh
```

**Issue**: Database connection error
```bash
# Solution: Check database configuration
python scripts/check_database.py
```

**Issue**: Import errors
```bash
# Solution: Install dependencies
pip install -r requirements.txt
```

**Issue**: Port already in use
```bash
# Solution: Use different port
streamlit run app.py --server.port 8502
```

---

## 📞 Support

**Robert Reichert**  
Healthcare AI Architect

📧 **Email**: reichert.starguardai@gmail.com  
🔗 **LinkedIn**: [rreichert-HEDIS-Data-Science-AI](https://www.linkedin.com/in/rreichert-HEDIS-Data-Science-AI)  
💻 **GitHub**: [StarGuardAi/HEDIS-MA-Top-12-w-HEI-Prep](https://github.com/StarGuardAi/HEDIS-MA-Top-12-w-HEI-Prep)

**Status**: Available for contract work starting **Late April 2025**

---

**Key Takeaway**: Get started in **15 minutes** with this **HIPAA-compliant healthcare AI system** featuring **context engineering**, **agentic RAG**, and **zero PHI exposure**.



