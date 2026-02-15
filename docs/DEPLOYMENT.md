# Deployment Guide: Production Deployment Instructions

**HIPAA-compliant healthcare AI system deployment for production environments**

---

## 🏗️ Deployment Architecture

### Production Components

1. **Streamlit Dashboard**: User interface (port 8501)
2. **FastAPI Backend**: API server (port 8000)
3. **PostgreSQL Database**: Production database
4. **Ollama Server**: Local LLM server (port 11434)
5. **ChromaDB**: Vector database (local)
6. **Nginx**: Reverse proxy (optional)

---

## 📦 Deployment Options

### Option 1: Docker Deployment (Recommended)

**Benefits:**
- **Containerized**: Easy deployment and scaling
- **Isolated**: Secure environment isolation
- **Portable**: Works across environments

**Steps:**

1. **Build Docker Image**
```bash
docker build -t hedis-optimizer:latest .
```

2. **Run Container**
```bash
docker run -d \
  --name hedis-optimizer \
  -p 8501:8501 \
  -p 8000:8000 \
  -e DATABASE_URL=postgresql://user:pass@host:5432/db \
  -e OLLAMA_HOST=http://ollama:11434 \
  hedis-optimizer:latest
```

3. **Verify Deployment**
```bash
# Check dashboard
curl http://localhost:8501

# Check API
curl http://localhost:8000/health
```

### Option 2: Kubernetes Deployment

**Benefits:**
- **Scalable**: Horizontal scaling
- **High Availability**: Multi-replica deployment
- **Managed**: Kubernetes orchestration

**Steps:**

1. **Create Deployment YAML**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: hedis-optimizer
spec:
  replicas: 3
  selector:
    matchLabels:
      app: hedis-optimizer
  template:
    metadata:
      labels:
        app: hedis-optimizer
    spec:
      containers:
      - name: hedis-optimizer
        image: hedis-optimizer:latest
        ports:
        - containerPort: 8501
        - containerPort: 8000
```

2. **Deploy**
```bash
kubectl apply -f deployment.yaml
```

### Option 3: AWS Deployment

**Benefits:**
- **Managed Services**: AWS managed infrastructure
- **Scalability**: Auto-scaling capabilities
- **Security**: AWS security features

**Steps:**

1. **EC2 Instance**
```bash
# Launch EC2 instance
aws ec2 run-instances \
  --image-id ami-xxx \
  --instance-type t3.large \
  --security-group-ids sg-xxx \
  --key-name my-key
```

2. **RDS PostgreSQL**
```bash
# Create RDS instance
aws rds create-db-instance \
  --db-instance-identifier hedis-db \
  --db-instance-class db.t3.medium \
  --engine postgres \
  --master-username admin \
  --master-user-password password
```

3. **Deploy Application**
```bash
# SSH into EC2
ssh -i my-key.pem ec2-user@instance-ip

# Clone repository
git clone https://github.com/StarGuardAi/HEDIS-MA-Top-12-w-HEI-Prep.git

# Install dependencies
pip install -r requirements.txt

# Run application
streamlit run app.py
```

---

## 🔒 Security Configuration

### Environment Variables

**Required:**
```bash
DATABASE_URL=postgresql://user:pass@host:5432/db
OLLAMA_HOST=http://ollama:11434
SECRET_KEY=your-secret-key
```

**Optional:**
```bash
LOG_LEVEL=INFO
AUDIT_LOG_PATH=/var/log/hedis/audit.log
ENCRYPTION_KEY=your-encryption-key
```

### SSL/TLS Configuration

**Nginx Configuration:**
```nginx
server {
    listen 443 ssl;
    server_name your-domain.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    location / {
        proxy_pass http://localhost:8501;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Firewall Configuration

**Required Ports:**
- **8501**: Streamlit dashboard
- **8000**: FastAPI backend
- **11434**: Ollama server (internal only)
- **5432**: PostgreSQL (internal only)

**Firewall Rules:**
```bash
# Allow dashboard access
ufw allow 8501/tcp

# Allow API access
ufw allow 8000/tcp

# Block Ollama from external access
ufw deny 11434/tcp
```

---

## 📊 Monitoring & Logging

### Application Logs

**Log Locations:**
- **Application Logs**: `/var/log/hedis/app.log`
- **Audit Logs**: `/var/log/hedis/audit.log`
- **Error Logs**: `/var/log/hedis/error.log`

**Log Rotation:**
```bash
# Configure logrotate
/var/log/hedis/*.log {
    daily
    rotate 30
    compress
    delaycompress
    notifempty
    create 0644 user group
}
```

### Monitoring Metrics

**Key Metrics:**
- **Query Response Time**: Target <10s
- **Cache Hit Rate**: Target >80%
- **Error Rate**: Target <1%
- **PHI Detection Rate**: Target 100%

**Monitoring Tools:**
- **Prometheus**: Metrics collection
- **Grafana**: Metrics visualization
- **ELK Stack**: Log aggregation

---

## 🔄 Backup & Recovery

### Database Backups

**Automated Backups:**
```bash
# Daily backup script
#!/bin/bash
pg_dump -h localhost -U user -d hedis_db > /backups/hedis_$(date +%Y%m%d).sql
```

**Backup Retention:**
- **Daily**: 30 days
- **Weekly**: 12 weeks
- **Monthly**: 12 months

### Disaster Recovery

**Recovery Procedures:**
1. **Restore Database**: `psql -h localhost -U user -d hedis_db < backup.sql`
2. **Restore Application**: Deploy from Git repository
3. **Verify Functionality**: Run health checks

---

## 📈 Performance Optimization

### Database Optimization

**PostgreSQL Configuration:**
```sql
-- Increase shared buffers
shared_buffers = 256MB

-- Increase work memory
work_mem = 16MB

-- Enable query caching
shared_preload_libraries = 'pg_stat_statements'
```

### Application Optimization

**Caching:**
- **Context Cache**: 1-hour domain cache, 5-minute measure cache
- **Query Cache**: 30-second query cache
- **Result Cache**: 5-minute result cache

**Connection Pooling:**
```python
# Use connection pooling
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20
)
```

---

## 🧪 Testing Deployment

### Health Checks

**Dashboard Health:**
```bash
curl http://localhost:8501/_stcore/health
```

**API Health:**
```bash
curl http://localhost:8000/health
```

**Database Health:**
```bash
psql -h localhost -U user -d hedis_db -c "SELECT 1"
```

### Performance Testing

**Load Testing:**
```bash
# Use Apache Bench
ab -n 1000 -c 10 http://localhost:8501/

# Use Locust
locust -f tests/load_test.py
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

**Key Takeaway**: Production deployment with **HIPAA compliance**, **security**, **monitoring**, and **performance optimization** for **enterprise healthcare environments**.



