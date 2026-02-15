# API Documentation: Complete API Reference

**HIPAA-compliant FastAPI backend with 15+ endpoints**

---

## 🚀 Base URL

**Development**: `http://localhost:8000`  
**Production**: `https://your-domain.com/api`

**API Documentation**: `http://localhost:8000/docs` (Swagger UI)

---

## 🔐 Authentication

### API Key Authentication

**Header:**
```
X-API-Key: your-api-key
```

**Example:**
```python
import requests

headers = {
    "X-API-Key": "your-api-key",
    "Content-Type": "application/json"
}

response = requests.get("http://localhost:8000/api/health", headers=headers)
```

---

## 📊 Endpoints

### Health Check

**GET** `/health`

**Description**: Check API health status

**Response:**
```json
{
    "status": "healthy",
    "timestamp": "2024-12-01T10:30:00Z",
    "version": "1.0.0"
}
```

### Predict Gap-in-Care

**POST** `/api/predict/gap-in-care`

**Description**: Predict gap-in-care for a member

**Request Body:**
```json
{
    "member_id": "M123456",
    "measure_id": "GSD",
    "features": {
        "age": 65,
        "diabetes_diagnosis_date": "2023-01-15",
        "last_hba1c_date": "2024-06-01",
        "last_hba1c_value": 7.2
    }
}
```

**Response:**
```json
{
    "member_id": "M123456",
    "measure_id": "GSD",
    "prediction": true,
    "probability": 0.87,
    "confidence": "high",
    "recommendations": [
        "Schedule HbA1c test within 30 days",
        "Consider diabetes education program"
    ]
}
```

### Calculate ROI

**POST** `/api/calculate/roi`

**Description**: Calculate ROI for interventions

**Request Body:**
```json
{
    "measure_id": "GSD",
    "member_count": 1000,
    "intervention_cost_per_member": 50,
    "star_rating_impact": 0.1
}
```

**Response:**
```json
{
    "measure_id": "GSD",
    "member_count": 1000,
    "intervention_cost": 50000,
    "star_rating_impact": 0.1,
    "revenue_impact": 1500000,
    "roi": 30.0,
    "payback_period_months": 0.4
}
```

### Get Member Gaps

**GET** `/api/members/{member_id}/gaps`

**Description**: Get all gaps for a member

**Response:**
```json
{
    "member_id": "M123456",
    "gaps": [
        {
            "measure_id": "GSD",
            "measure_name": "Glycemic Status Assessment",
            "gap_status": "open",
            "prediction_probability": 0.87,
            "last_updated": "2024-12-01T10:30:00Z"
        }
    ],
    "total_gaps": 1
}
```

### Get Measure Performance

**GET** `/api/measures/{measure_id}/performance`

**Description**: Get performance metrics for a measure

**Response:**
```json
{
    "measure_id": "GSD",
    "measure_name": "Glycemic Status Assessment",
    "compliance_rate": 0.85,
    "gap_rate": 0.15,
    "model_accuracy": 0.89,
    "recall": 0.83,
    "precision": 0.86
}
```

### Context Engineering

**POST** `/api/context/build`

**Description**: Build hierarchical context for a query

**Request Body:**
```json
{
    "query": "Calculate ROI for diabetes interventions",
    "max_tokens": 4000
}
```

**Response:**
```json
{
    "context": {
        "layer_1_domain": {...},
        "layer_2_measure": {...},
        "layer_3_query": {...}
    },
    "metadata": {
        "efficiency_score": 85,
        "cache_hits": 2,
        "cache_misses": 1,
        "total_size": 3500
    }
}
```

### Agentic RAG

**POST** `/api/rag/agentic`

**Description**: Process query using agentic RAG

**Request Body:**
```json
{
    "query": "Find gaps and calculate ROI",
    "context": {...}
}
```

**Response:**
```json
{
    "query": "Find gaps and calculate ROI",
    "plan": {
        "steps": [...],
        "total_steps": 3,
        "estimated_time": 8.5,
        "estimated_cost": 0.008
    },
    "results": [...],
    "execution_time": 7.2,
    "success": true
}
```

---

## 🔒 Security Endpoints

### PHI Detection

**POST** `/api/security/detect-phi`

**Description**: Detect PHI in text

**Request Body:**
```json
{
    "text": "Member John Doe, DOB 01/15/1960, SSN 123-45-6789"
}
```

**Response:**
```json
{
    "phi_detected": true,
    "phi_types": ["name", "dob", "ssn"],
    "sanitized_text": "Member [REDACTED], DOB [REDACTED], SSN [REDACTED]"
}
```

### Audit Logs

**GET** `/api/audit/logs`

**Description**: Get audit logs (admin only)

**Query Parameters:**
- `start_date`: Start date (ISO format)
- `end_date`: End date (ISO format)
- `user_id`: Filter by user ID
- `limit`: Number of results (default: 100)

**Response:**
```json
{
    "logs": [
        {
            "timestamp": "2024-12-01T10:30:00Z",
            "user_id": "user_123",
            "query": "Calculate ROI for diabetes interventions",
            "response_time_ms": 7200,
            "phi_detected": false
        }
    ],
    "total": 1000,
    "page": 1,
    "limit": 100
}
```

---

## 📊 Error Handling

### Error Response Format

```json
{
    "error": {
        "code": "VALIDATION_ERROR",
        "message": "Invalid member_id format",
        "details": {
            "field": "member_id",
            "issue": "Must be alphanumeric"
        }
    }
}
```

### Error Codes

| Code | Description | HTTP Status |
|------|-------------|-------------|
| `VALIDATION_ERROR` | Request validation failed | 400 |
| `NOT_FOUND` | Resource not found | 404 |
| `UNAUTHORIZED` | Authentication required | 401 |
| `FORBIDDEN` | Insufficient permissions | 403 |
| `INTERNAL_ERROR` | Server error | 500 |

---

## 📈 Rate Limiting

**Rate Limits:**
- **Standard**: 100 requests/minute
- **Premium**: 1000 requests/minute

**Headers:**
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1609459200
```

---

## 🔍 Examples

### Python Example

```python
import requests

# Base URL
base_url = "http://localhost:8000"

# Headers
headers = {
    "X-API-Key": "your-api-key",
    "Content-Type": "application/json"
}

# Predict gap-in-care
response = requests.post(
    f"{base_url}/api/predict/gap-in-care",
    headers=headers,
    json={
        "member_id": "M123456",
        "measure_id": "GSD",
        "features": {
            "age": 65,
            "diabetes_diagnosis_date": "2023-01-15",
            "last_hba1c_date": "2024-06-01",
            "last_hba1c_value": 7.2
        }
    }
)

result = response.json()
print(f"Prediction: {result['prediction']}")
print(f"Probability: {result['probability']}")
```

### JavaScript Example

```javascript
const baseUrl = 'http://localhost:8000';

// Predict gap-in-care
async function predictGapInCare(memberId, measureId, features) {
    const response = await fetch(`${baseUrl}/api/predict/gap-in-care`, {
        method: 'POST',
        headers: {
            'X-API-Key': 'your-api-key',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            member_id: memberId,
            measure_id: measureId,
            features: features
        })
    });
    
    return await response.json();
}

// Usage
const result = await predictGapInCare('M123456', 'GSD', {
    age: 65,
    diabetes_diagnosis_date: '2023-01-15',
    last_hba1c_date: '2024-06-01',
    last_hba1c_value: 7.2
});

console.log(`Prediction: ${result.prediction}`);
console.log(`Probability: ${result.probability}`);
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

**Key Takeaway**: **Complete API reference** with **15+ endpoints**, **HIPAA compliance**, and **comprehensive documentation** for healthcare AI integration.



