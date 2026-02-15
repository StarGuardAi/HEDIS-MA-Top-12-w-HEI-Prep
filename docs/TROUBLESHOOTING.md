# Troubleshooting Guide: Common Issues & Solutions

**Quick reference for resolving common issues in HIPAA-compliant healthcare AI system**

---

## 🔧 Common Issues

### Issue 1: Ollama Not Found

**Symptoms:**
- Error: "Ollama server not found"
- Context engineering fails
- Agentic RAG fails

**Solution:**
```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Start Ollama server
ollama serve

# Pull model
ollama pull llama2

# Verify installation
ollama list
```

**Prevention:**
- Ensure Ollama is installed before deployment
- Check Ollama service status regularly
- Monitor Ollama logs for errors

---

### Issue 2: Database Connection Error

**Symptoms:**
- Error: "Database connection failed"
- API endpoints fail
- Dashboard shows database errors

**Solution:**
```bash
# Check database connection
python scripts/check_database.py

# Verify database credentials
echo $DATABASE_URL

# Test connection
psql -h localhost -U user -d hedis_db -c "SELECT 1"

# Restart database (if needed)
sudo systemctl restart postgresql
```

**Prevention:**
- Verify database credentials in `.env` file
- Check database service status
- Monitor database connection pool

---

### Issue 3: Import Errors

**Symptoms:**
- Error: "Module not found"
- Import errors in Python
- Missing dependencies

**Solution:**
```bash
# Install dependencies
pip install -r requirements.txt

# Verify Python version
python --version  # Should be 3.11+

# Check virtual environment
which python

# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

**Prevention:**
- Use virtual environment
- Keep requirements.txt updated
- Test imports after dependency changes

---

### Issue 4: Port Already in Use

**Symptoms:**
- Error: "Port 8501 already in use"
- Streamlit dashboard won't start
- API server won't start

**Solution:**
```bash
# Find process using port
lsof -i :8501

# Kill process
kill -9 <PID>

# Or use different port
streamlit run app.py --server.port 8502
```

**Prevention:**
- Check for running processes before starting
- Use process manager (systemd, supervisor)
- Monitor port usage

---

### Issue 5: PHI Detection False Positives

**Symptoms:**
- Valid queries blocked
- False PHI detection
- User complaints

**Solution:**
```bash
# Review PHI detection patterns
python scripts/test_phi_detection.py

# Adjust detection thresholds
# Edit services/security/phi_detector.py

# Test with sample queries
python scripts/test_phi_detection.py --test-queries queries.txt
```

**Prevention:**
- Regular PHI detection testing
- Monitor false positive rates
- Adjust detection patterns as needed

---

### Issue 6: Context Cache Not Working

**Symptoms:**
- Slow query responses
- Low cache hit rate
- High API costs

**Solution:**
```bash
# Check cache status
python scripts/check_cache.py

# Clear cache
python scripts/clear_cache.py

# Verify cache configuration
# Check services/context_engineering/context_builder.py

# Restart application
systemctl restart hedis-optimizer
```

**Prevention:**
- Monitor cache hit rates
- Regular cache maintenance
- Optimize cache TTLs

---

### Issue 7: Agentic RAG Execution Failures

**Symptoms:**
- Query execution fails
- Low step success rate
- Self-correction failures

**Solution:**
```bash
# Check agentic RAG logs
tail -f logs/agentic_rag.log

# Test agentic RAG
python scripts/test_agentic_rag.py

# Verify tool availability
python scripts/check_tools.py

# Review execution plan
python scripts/debug_agentic_rag.py --query "your query"
```

**Prevention:**
- Monitor step success rates
- Regular tool availability checks
- Test agentic RAG regularly

---

### Issue 8: Audit Logs Not Writing

**Symptoms:**
- No audit logs created
- Compliance concerns
- Missing audit trail

**Solution:**
```bash
# Check audit log directory
ls -la /var/log/hedis/audit.log

# Verify permissions
chmod 644 /var/log/hedis/audit.log

# Check disk space
df -h

# Test audit logging
python scripts/test_audit_logging.py
```

**Prevention:**
- Monitor disk space
- Regular log rotation
- Verify log permissions

---

## 🔍 Debugging Tools

### Debug Mode

**Enable Debug Logging:**
```bash
# Set environment variable
export LOG_LEVEL=DEBUG

# Or in .env file
LOG_LEVEL=DEBUG
```

### Log Files

**Location**: `/var/log/hedis/`

**Files:**
- `app.log`: Application logs
- `audit.log`: Audit trail logs
- `error.log`: Error logs
- `agentic_rag.log`: Agentic RAG logs

**View Logs:**
```bash
# View recent logs
tail -f /var/log/hedis/app.log

# Search logs
grep "ERROR" /var/log/hedis/app.log

# View audit logs
tail -f /var/log/hedis/audit.log
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

**Key Takeaway**: **Comprehensive troubleshooting guide** with **common issues**, **solutions**, and **debugging tools** for maintaining **HIPAA-compliant healthcare AI system**.



