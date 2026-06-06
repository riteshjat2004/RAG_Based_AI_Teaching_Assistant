# Streamlit Cloud Deployment Checklist

Quick reference checklist for deploying RAG Teaching Assistant to Streamlit Cloud.

---

## Pre-Deployment (Local Setup)

### Code & Configuration
- [ ] `requirement.txt` has been updated and reviewed
- [ ] `.streamlit/config.toml` has been created
- [ ] `.gitignore` has been updated
- [ ] All changes committed to Git

### Files Verification
- [ ] `streamlit_app.py` exists (entry point)
- [ ] `retrieval.py` exists and contains RAG logic
- [ ] `llm.py` exists and contains LLM integration
- [ ] `embeddings.joblib` exists and is committed
- [ ] `jsons/` directory contains all 18 JSON files
- [ ] No large media files (`videos/`, `audios/`) in Git

### Code Quality
- [ ] Imports are relative (no absolute paths)
- [ ] No hardcoded secrets in code
- [ ] No debug print statements left
- [ ] Error handling is in place
- [ ] No missing dependencies in requirements.txt

---

## External Service Setup

### Ollama Service
- [ ] Ollama is installed and running
- [ ] BGE-M3 model is pulled: `ollama pull bge-m3`
- [ ] deepseek-r1 model is pulled: `ollama pull deepseek-r1:1.5b`
- [ ] Ollama service is accessible via HTTP
- [ ] Ollama API responds to health check: `curl http://server:11434/api/tags`

### For Production Deployment
- [ ] Decide on Ollama hosting option (self-hosted, cloud VM, Docker, etc.)
- [ ] Deploy Ollama to chosen platform
- [ ] Obtain public URL/IP of Ollama service
- [ ] Verify Ollama is accessible from internet
- [ ] Update base URLs in `llm.py` and `retrieval.py` (or use environment variables)

---

## GitHub Repository

### Repository Setup
- [ ] Repository is public (or granted access to Streamlit)
- [ ] All changes have been committed: `git add -A && git commit -m "Deployment prep"`
- [ ] All changes have been pushed: `git push origin main`
- [ ] No uncommitted changes: `git status` shows clean

### Branch Verification
- [ ] Working on correct branch (e.g., `main`)
- [ ] Branch is up-to-date with remote

---

## Streamlit Cloud Deployment

### Initial Connection
- [ ] Navigate to https://share.streamlit.io
- [ ] Sign in with GitHub account
- [ ] Click "New app"
- [ ] Select repository: `RAG_based_AI_Assistant`
- [ ] Select branch: `main`
- [ ] Set main file path: `streamlit_app.py`
- [ ] Click "Deploy"

### Post-Deployment Configuration

#### If Using Local/Private Ollama
- [ ] Open app settings (gear icon)
- [ ] Go to "Secrets"
- [ ] Add: `OLLAMA_BASE_URL=http://your-server:11434` (or use ngrok)
- [ ] Save secrets

#### If Using Cloud Ollama
- [ ] Open app settings (gear icon)
- [ ] Go to "Secrets"
- [ ] Add: `OLLAMA_BASE_URL=http://your-cloud-ip:11434`
- [ ] Add: `OLLAMA_API_KEY=your-key` (if required)
- [ ] Save secrets

#### Update Application Code (if using environment variables)
- [ ] In `llm.py` line 16: `base_url: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")`
- [ ] In `retrieval.py` line 21: `base_url: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")`
- [ ] Commit and push changes
- [ ] Streamlit will auto-redeploy

---

## Testing & Validation

### App Loading
- [ ] App loads without errors
- [ ] Dashboard displays correctly
- [ ] Sidebar renders with sliders
- [ ] Custom CSS displays correctly (cards, badges, colors)

### Functionality Testing
- [ ] "Check Service Status" button works
- [ ] Test query works and returns results
- [ ] Retrieved chunks display correctly
- [ ] Sources tab shows references
- [ ] Metadata tab shows retrieval scores
- [ ] Export to text file works
- [ ] Sliders for top_k and temperature work

### Error Handling
- [ ] Appropriate error message if Ollama not running
- [ ] Appropriate error message if embeddings file missing
- [ ] Appropriate error message for connection errors
- [ ] Appropriate error message for file not found errors

### Performance
- [ ] Initial load time < 30 seconds
- [ ] Query processing completes in reasonable time
- [ ] No memory errors
- [ ] No timeout errors

---

## Monitoring & Maintenance

### Initial Monitoring
- [ ] Check Streamlit Cloud dashboard for errors
- [ ] Monitor resource usage (CPU, memory)
- [ ] Check app logs for any warnings
- [ ] Monitor Ollama service logs

### Regular Checks
- [ ] Test app daily for first week
- [ ] Test query functionality weekly
- [ ] Monitor error rates monthly
- [ ] Update models if new versions available

### Scaling Decisions
- [ ] Monitor concurrent users
- [ ] Track average response time
- [ ] Monitor memory usage trends
- [ ] Plan scaling if needed (higher tier, or load balancer)

---

## Troubleshooting Quick Reference

| Issue | Solution |
|-------|----------|
| App won't deploy | Check GitHub is public, all files committed |
| "Cannot connect to Ollama" | Verify Ollama URL in secrets, check firewall |
| "embeddings.joblib not found" | Ensure file is committed to Git |
| "JSON files not found" | Ensure jsons/ directory is committed |
| Slow responses | Check Ollama server resources, network latency |
| Memory exceeded | Reduce top_k default, use smaller model |
| Models not found | Pull models: `ollama pull bge-m3 && ollama pull deepseek-r1:1.5b` |

---

## Rollback Plan

If deployment has critical issues:

1. **Immediate rollback:**
   - Go to Streamlit Cloud dashboard
   - Find the app
   - Click "Revert" to previous version

2. **Identify issue:**
   - Check app logs
   - Check Ollama logs
   - Review recent changes

3. **Fix locally:**
   - Fix issue in local code
   - Test thoroughly
   - Commit and push

4. **Redeploy:**
   - Streamlit auto-redeploys on push
   - Monitor for errors

---

## Success Indicators

✅ **Deployment is successful when:**
1. App loads at https://share.streamlit.io/your-name/RAG_based_AI_Assistant
2. "Check Service Status" button shows "✅ All services running!"
3. Can successfully query and receive RAG responses
4. Retrieved chunks display with scores and timestamps
5. Export functionality works
6. No errors in Streamlit logs
7. Response time is < 10 seconds per query

---

## Completion Status

- [ ] All pre-deployment checks completed
- [ ] External service (Ollama) is set up and running
- [ ] Repository is pushed to GitHub
- [ ] App is deployed to Streamlit Cloud
- [ ] All functionality has been tested
- [ ] Monitoring is set up
- [ ] **DEPLOYMENT COMPLETE** ✅

---

**Deployment Date:** ___________  
**Deployed By:** ___________  
**Notes:** 

---

For detailed information, see:
- `DEPLOYMENT_READINESS.md` - Full deployment report
- `OLLAMA_SETUP_GUIDE.md` - Ollama setup instructions
- Project `Readme.md` - Application documentation
