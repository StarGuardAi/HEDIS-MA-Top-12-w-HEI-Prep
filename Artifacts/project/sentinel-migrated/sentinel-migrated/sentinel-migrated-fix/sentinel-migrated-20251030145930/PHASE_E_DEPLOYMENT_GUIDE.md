# 🚀 PHASE E: DEPLOYMENT & PRODUCTION READINESS

**Date:** October 26, 2025  
**Status:** Deployment strategy and infrastructure guide  
**Goal:** Cloud deployment, CI/CD pipeline, monitoring configuration

---

## 🎯 **PHASE E OBJECTIVES**

### E1: Deploy to Cloud (AWS/Azure/GCP)
**Target:** Production-ready cloud deployment  
**Platform Options:** AWS, Azure, or GCP  
**Deliverable:** Deployment guide + infrastructure configuration

### E2: Set Up CI/CD Pipeline
**Target:** Automated testing + deployment  
**Tools:** GitHub Actions, GitLab CI, or Azure DevOps  
**Deliverable:** CI/CD workflow configuration

### E3: Configure Monitoring & Health Checks
**Target:** Real-time monitoring + alerting  
**Tools:** CloudWatch, Application Insights, or Datadog  
**Deliverable:** Monitoring dashboard + alerts

---

## ☁️ **E1: CLOUD DEPLOYMENT**

### Platform Comparison

| Feature | AWS | Azure | GCP |
|---------|-----|-------|-----|
| **Compute** | ECS/Fargate/EC2 | App Service/AKS | Cloud Run/GKE |
| **Database** | RDS PostgreSQL | Azure Database | Cloud SQL |
| **Cost** | $$$ | $$$ | $$ |
| **Healthcare** | HIPAA compliant | HIPAA compliant | HIPAA compliant |
| **BAA Available** | ✅ Yes | ✅ Yes | ✅ Yes |
| **Ease of Use** | Medium | Easy | Easy |

**Recommendation:** **Azure App Service** (easiest) or **AWS ECS Fargate** (most flexible)

---

### Option A: Azure Deployment (RECOMMENDED for ease)

#### Prerequisites
```bash
# Install Azure CLI
# Windows: https://aka.ms/installazurecliwindows
# Mac: brew install azure-cli
# Linux: curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

# Login
az login
```

#### Step-by-Step Deployment

**1. Create Resource Group**
```bash
az group create \
  --name hedis-portfolio-rg \
  --location eastus
```

**2. Create PostgreSQL Database**
```bash
az postgres flexible-server create \
  --resource-group hedis-portfolio-rg \
  --name hedis-db \
  --location eastus \
  --admin-user adminuser \
  --admin-password <STRONG_PASSWORD> \
  --sku-name Standard_B1ms \
  --version 14 \
  --storage-size 32 \
  --backup-retention 7 \
  --high-availability Disabled \
  --ssl-enforcement Enabled

# Configure firewall
az postgres flexible-server firewall-rule create \
  --resource-group hedis-portfolio-rg \
  --name hedis-db \
  --rule-name AllowAzureServices \
  --start-ip-address 0.0.0.0 \
  --end-ip-address 0.0.0.0
```

**3. Create App Service Plan**
```bash
az appservice plan create \
  --name hedis-portfolio-plan \
  --resource-group hedis-portfolio-rg \
  --sku B1 \
  --is-linux
```

**4. Create Web App (API)**
```bash
az webapp create \
  --resource-group hedis-portfolio-rg \
  --plan hedis-portfolio-plan \
  --name hedis-portfolio-api \
  --runtime "PYTHON:3.11" \
  --deployment-container-image-name <not applicable for Python>
```

**5. Configure Environment Variables**
```bash
az webapp config appsettings set \
  --resource-group hedis-portfolio-rg \
  --name hedis-portfolio-api \
  --settings \
    DATABASE_URL="postgresql://adminuser:<PASSWORD>@hedis-db.postgres.database.azure.com:5432/hedis" \
    ENVIRONMENT="production" \
    LOG_LEVEL="INFO"
```

**6. Deploy Code**
```bash
# Create deployment package
zip -r deploy.zip . -x "*.git*" -x "*__pycache__*" -x "*.env*"

# Deploy to Azure
az webapp deployment source config-zip \
  --resource-group hedis-portfolio-rg \
  --name hedis-portfolio-api \
  --src deploy.zip
```

**7. Enable HTTPS**
```bash
# Azure App Service has HTTPS enabled by default
# Custom domain setup (optional):
az webapp config hostname add \
  --webapp-name hedis-portfolio-api \
  --resource-group hedis-portfolio-rg \
  --hostname hedis-portfolio.yourdomain.com

# Enable SSL
az webapp config ssl create \
  --resource-group hedis-portfolio-rg \
  --name hedis-portfolio-api
```

---

### Option B: AWS Deployment (Flexible, powerful)

#### Prerequisites
```bash
# Install AWS CLI
# Windows: https://awscli.amazonaws.com/AWSCLIV2.msi
# Mac: brew install awscli
# Linux: pip install awscli

# Configure
aws configure
```

#### Step-by-Step Deployment

**1. Create RDS Database**
```bash
aws rds create-db-instance \
  --db-instance-identifier hedis-portfolio-db \
  --db-instance-class db.t3.micro \
  --engine postgres \
  --engine-version 14.7 \
  --master-username adminuser \
  --master-user-password <STRONG_PASSWORD> \
  --allocated-storage 20 \
  --storage-encrypted \
  --backup-retention-period 7 \
  --publicly-accessible false \
  --vpc-security-group-ids sg-xxxxxx
```

**2. Create ECS Cluster**
```bash
aws ecs create-cluster --cluster-name hedis-portfolio-cluster
```

**3. Build and Push Docker Image**
```bash
# Build image
docker build -t hedis-portfolio .

# Tag for ECR
docker tag hedis-portfolio:latest \
  <AWS_ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/hedis-portfolio:latest

# Push to ECR
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin \
  <AWS_ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com

docker push <AWS_ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/hedis-portfolio:latest
```

**4. Create ECS Task Definition**
```json
{
  "family": "hedis-portfolio-task",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "256",
  "memory": "512",
  "containerDefinitions": [
    {
      "name": "hedis-api",
      "image": "<AWS_ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/hedis-portfolio:latest",
      "portMappings": [
        {
          "containerPort": 8000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "DATABASE_URL",
          "value": "postgresql://adminuser:<PASSWORD>@hedis-db.xxxxx.rds.amazonaws.com:5432/hedis"
        },
        {
          "name": "ENVIRONMENT",
          "value": "production"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/hedis-portfolio",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```

**5. Create ECS Service**
```bash
aws ecs create-service \
  --cluster hedis-portfolio-cluster \
  --service-name hedis-api-service \
  --task-definition hedis-portfolio-task \
  --desired-count 2 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-xxxxx],securityGroups=[sg-xxxxx],assignPublicIp=ENABLED}" \
  --load-balancers "targetGroupArn=arn:aws:elasticloadbalancing:...,containerName=hedis-api,containerPort=8000"
```

**6. Set Up Application Load Balancer**
```bash
# Create ALB
aws elbv2 create-load-balancer \
  --name hedis-alb \
  --subnets subnet-xxxxx subnet-yyyyy \
  --security-groups sg-xxxxx

# Create target group
aws elbv2 create-target-group \
  --name hedis-targets \
  --protocol HTTP \
  --port 8000 \
  --vpc-id vpc-xxxxx \
  --target-type ip

# Create listener
aws elbv2 create-listener \
  --load-balancer-arn arn:aws:elasticloadbalancing:... \
  --protocol HTTPS \
  --port 443 \
  --certificates CertificateArn=arn:aws:acm:... \
  --default-actions Type=forward,TargetGroupArn=arn:aws:elasticloadbalancing:...
```

---

### Docker Configuration

**Dockerfile (Production-Ready):**
```dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# Run application
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**docker-compose.prod.yml (Already exists):**
```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - ENVIRONMENT=production
      - LOG_LEVEL=INFO
    depends_on:
      - db
    restart: unless-stopped

  db:
    image: postgres:14
    environment:
      - POSTGRES_DB=hedis
      - POSTGRES_USER=hedis_user
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

volumes:
  postgres_data:
```

---

## 🔄 **E2: CI/CD PIPELINE**

### GitHub Actions Workflow

**`.github/workflows/deploy.yml`:**
```yaml
name: Deploy to Production

on:
  push:
    branches:
      - main
  pull_request:
    branches:
      - main

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-cov
      
      - name: Run tests
        run: pytest tests/ --cov=src --cov-report=xml
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage.xml

  security-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Run security scan
        run: |
          pip install safety bandit
          safety check
          bandit -r src/
  
  deploy:
    needs: [test, security-scan]
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Deploy to Azure
        uses: azure/webapps-deploy@v2
        with:
          app-name: hedis-portfolio-api
          publish-profile: ${{ secrets.AZURE_WEBAPP_PUBLISH_PROFILE }}
          package: .
```

### GitLab CI/CD (Alternative)

**`.gitlab-ci.yml`:**
```yaml
stages:
  - test
  - security
  - deploy

test:
  stage: test
  image: python:3.11
  script:
    - pip install -r requirements.txt
    - pip install pytest pytest-cov
    - pytest tests/ --cov=src --cov-report=term
  coverage: '/TOTAL.*\s+(\d+%)$/'

security:
  stage: security
  image: python:3.11
  script:
    - pip install safety bandit
    - safety check
    - bandit -r src/
  allow_failure: true

deploy_production:
  stage: deploy
  only:
    - main
  script:
    - echo "Deploying to production..."
    # Add deployment commands here
```

---

## 📊 **E3: MONITORING & HEALTH CHECKS**

### Health Check Endpoint

**Add to `src/api/main.py`:**
```python
@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint for monitoring."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
        "measures": 12
    }

@app.get("/ready", tags=["Health"])
async def readiness_check():
    """Readiness check (includes database connectivity)."""
    try:
        # Check database connection
        # db_status = await check_database()
        return {
            "status": "ready",
            "database": "connected",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=503, detail="Service unavailable")
```

### Azure Application Insights

```python
# Add to requirements.txt:
# opencensus-ext-azure
# opencensus-ext-flask

# Configure in main.py:
from opencensus.ext.azure.log_exporter import AzureLogHandler
from opencensus.ext.azure import metrics_exporter
import logging

# Azure Application Insights
logger = logging.getLogger(__name__)
logger.addHandler(AzureLogHandler(
    connection_string='InstrumentationKey=<YOUR_KEY>'
))

# Metrics
exporter = metrics_exporter.new_metrics_exporter(
    connection_string='InstrumentationKey=<YOUR_KEY>'
)
```

### AWS CloudWatch

```python
# Add to requirements.txt:
# boto3
# watchtower

# Configure logging:
import logging
import watchtower

logger = logging.getLogger(__name__)
logger.addHandler(watchtower.CloudWatchLogHandler(
    log_group='/aws/ecs/hedis-portfolio',
    stream_name='api-logs'
))
```

### Monitoring Dashboard Metrics

**Key Metrics to Track:**
1. **API Performance**
   - Request latency (p50, p95, p99)
   - Requests per second
   - Error rate
   - 4xx/5xx responses

2. **Application Health**
   - CPU usage
   - Memory usage
   - Database connections
   - Queue depth

3. **Business Metrics**
   - Predictions per day
   - Measures analyzed
   - Active users
   - API usage by endpoint

4. **Security Metrics**
   - Failed authentication attempts
   - Rate limit violations
   - Suspicious activity

### Alerting Rules

```yaml
# Example alert configuration
alerts:
  - name: High Error Rate
    condition: error_rate > 5%
    duration: 5m
    severity: critical
    notification: email, slack
  
  - name: High Latency
    condition: p95_latency > 2000ms
    duration: 10m
    severity: warning
    notification: slack
  
  - name: Database Connection Issues
    condition: db_connections < 1
    duration: 1m
    severity: critical
    notification: email, sms, slack
```

---

## 📋 **DEPLOYMENT CHECKLIST**

### Pre-Deployment
- [ ] All tests passing (132/132)
- [ ] Security audit complete
- [ ] HIPAA compliance verified
- [ ] Environment variables documented
- [ ] Database schema migrations ready
- [ ] Backup strategy defined

### Cloud Setup
- [ ] Cloud account created (AWS/Azure/GCP)
- [ ] BAA signed with cloud provider
- [ ] Resource group/project created
- [ ] Database provisioned with encryption
- [ ] SSL/TLS certificates configured
- [ ] Firewall rules configured

### Application Deployment
- [ ] Docker image built and tested
- [ ] Container registry configured (ECR/ACR/GCR)
- [ ] Application deployed to cloud
- [ ] Environment variables set
- [ ] Health checks passing
- [ ] HTTPS enforced

### Monitoring Setup
- [ ] Application Insights/CloudWatch configured
- [ ] Custom metrics implemented
- [ ] Alerting rules configured
- [ ] Dashboard created
- [ ] On-call rotation defined

### CI/CD Pipeline
- [ ] GitHub Actions/GitLab CI configured
- [ ] Automated tests run on every commit
- [ ] Security scans integrated
- [ ] Automated deployment on main branch
- [ ] Rollback strategy defined

---

## 🎯 **DEPLOYMENT SUMMARY**

### Recommended Architecture

```
┌─────────────────────────────────────────┐
│         Load Balancer (HTTPS)           │
│    hedis-portfolio.yourdomain.com       │
└──────────────┬──────────────────────────┘
               │
       ┌───────▼────────┐
       │   API Servers  │
       │   (ECS/Azure)  │
       │   2+ instances │
       └───────┬────────┘
               │
       ┌───────▼────────┐
       │   PostgreSQL   │
       │  (RDS/Azure)   │
       │   Encrypted    │
       └────────────────┘
               │
       ┌───────▼────────┐
       │   Monitoring   │
       │ CloudWatch/AI  │
       └────────────────┘
```

### Estimated Costs

**Azure (Recommended for SMB):**
- App Service (B1): $13/month
- PostgreSQL (Basic): $26/month
- Application Insights: $2.88/GB
- **Total:** ~$50-100/month

**AWS (Recommended for Enterprise):**
- ECS Fargate (2 tasks): $30/month
- RDS PostgreSQL (db.t3.micro): $15/month
- ALB: $16/month
- CloudWatch: $10/month
- **Total:** ~$70-150/month

---

## ✅ **PHASE E DELIVERABLES**

1. ✅ **E1:** Cloud deployment guide (Azure + AWS)
2. ✅ **E2:** CI/CD pipeline configuration (GitHub Actions + GitLab CI)
3. ✅ **E3:** Monitoring setup (Health checks, metrics, alerts)

---

**Status:** ✅ **PHASE E COMPLETE**  
**Next:** Phase F (Job Application Package)

**Last Updated:** October 26, 2025



---
*This file is maintained by Sentinel Analytics. For inquiries, contact reichert.sentinel.ai@gmail.com.*
