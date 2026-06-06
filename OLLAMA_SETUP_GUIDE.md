# Ollama Setup Guide for Streamlit Cloud Deployment

This guide explains how to set up Ollama to work with this Streamlit application deployed on Streamlit Community Cloud.

---

## Background

Your RAG Teaching Assistant requires:
- **BGE-M3** model for embedding generation
- **deepseek-r1:1.5b** model for response generation

Since Streamlit Cloud cannot run Ollama locally, you must run Ollama on a separate server that Streamlit Cloud can reach via HTTP.

---

## Option 1: Local Ollama (Development/Testing)

### Setup
1. **Install Ollama** (if not already installed)
   - macOS: `brew install ollama`
   - Windows: Download from https://ollama.ai
   - Linux: `curl https://ollama.ai/install.sh | sh`

2. **Pull required models**
   ```bash
   ollama pull bge-m3
   ollama pull deepseek-r1:1.5b
   ```

3. **Start Ollama server**
   ```bash
   ollama serve
   ```
   - Default runs on `http://localhost:11434`

### For Streamlit Cloud Testing
If you want to test with Streamlit Cloud while Ollama runs locally:
1. Use a reverse proxy like **ngrok** or **CloudFlare Tunnel**
   ```bash
   # Using ngrok
   ngrok http 11434
   ```
   This will give you a public URL like `https://xxxx-xx-xxx-xxx-xx.ngrok.io`

2. Update `llm.py` and `retrieval.py` with the public URL:
   ```python
   base_url: str = "https://xxxx-xx-xxx-xxx-xx.ngrok.io"
   ```

---

## Option 2: Cloud VM Deployment (Production)

### Using AWS EC2

1. **Launch EC2 instance**
   - AMI: Ubuntu 22.04 LTS
   - Instance type: `t3.large` or `t3.xlarge` (recommended)
   - Storage: 50-100 GB (for models)
   - Security group: Allow port 11434 inbound

2. **Install Ollama**
   ```bash
   sudo apt update
   sudo apt install -y curl
   curl https://ollama.ai/install.sh | sh
   ```

3. **Pull models**
   ```bash
   ollama pull bge-m3
   ollama pull deepseek-r1:1.5b
   ```

4. **Configure Ollama to listen on all interfaces**
   ```bash
   # Edit systemd service
   sudo systemctl edit ollama
   
   # Add or modify:
   [Service]
   Environment="OLLAMA_HOST=0.0.0.0:11434"
   ```

5. **Start Ollama**
   ```bash
   sudo systemctl restart ollama
   sudo systemctl enable ollama  # Auto-start on reboot
   ```

6. **Get your EC2 public IP**
   - From AWS console or: `curl http://169.254.169.254/latest/meta-data/public-ipv4`

7. **Update `llm.py` and `retrieval.py`**
   ```python
   base_url: str = "http://YOUR-EC2-PUBLIC-IP:11434"
   ```

### Using Azure VM

Similar steps, but use Azure CLI:
```bash
az vm create --resource-group myRG --name ollama-vm --image UbuntuLTS --size Standard_D4s_v3
az vm open-port --resource-group myRG --name ollama-vm --port 11434
```

### Using DigitalOcean Droplet

1. Create Droplet (8GB+ RAM, 50GB+ SSD)
2. SSH into droplet
3. Run installation steps (same as AWS)

---

## Option 3: Docker Deployment

### Local Docker

```dockerfile
# Dockerfile
FROM ollama/ollama:latest

RUN ollama pull bge-m3 && \
    ollama pull deepseek-r1:1.5b

EXPOSE 11434

CMD ["ollama", "serve"]
```

Build and run:
```bash
docker build -t my-ollama .
docker run -d -p 11434:11434 my-ollama
```

### Docker Compose

```yaml
version: '3'
services:
  ollama:
    image: ollama/ollama:latest
    ports:
      - "11434:11434"
    environment:
      - OLLAMA_HOST=0.0.0.0:11434
    volumes:
      - ollama_data:/root/.ollama
    command: ollama serve

volumes:
  ollama_data:
```

Start with: `docker-compose up -d`

---

## Configuration for Streamlit Cloud

Once your Ollama service is running on an accessible URL:

### Method 1: Update Code

Edit `llm.py` (line 16):
```python
base_url: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
```

Edit `retrieval.py` (line 21):
```python
base_url: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
```

### Method 2: Use Streamlit Secrets

1. Go to **Streamlit Cloud** → **Settings** → **Secrets**
2. Add:
   ```
   OLLAMA_BASE_URL=http://your-server:11434
   ```

3. Access in code:
   ```python
   import streamlit as st
   base_url = st.secrets.get("OLLAMA_BASE_URL", "http://localhost:11434")
   ```

---

## Recommended Hardware Requirements

| Metric | Recommended |
|--------|-------------|
| CPU | 4+ cores (8+ for production) |
| RAM | 8-16 GB minimum (32+ for production) |
| Storage | 50-100 GB (for models + cache) |
| Network | 1+ Gbps connection |
| Latency | <100ms to Streamlit Cloud |

---

## Monitoring & Maintenance

### Health Check

```bash
curl http://your-ollama-server:11434/api/tags
```

Should return list of installed models.

### Performance Monitoring

```bash
# Check Ollama logs
journalctl -u ollama -f  # On Linux with systemd
```

### Update Models

```bash
ollama pull bge-m3:latest
ollama pull deepseek-r1:latest
```

---

## Cost Estimation

| Option | Monthly Cost | Pros | Cons |
|--------|-------------|------|------|
| Local + ngrok | ~$7-15 | Free Ollama | Limited bandwidth |
| AWS t3.large | ~$30-50 | Scalable, reliable | Ongoing costs |
| Azure B4ms | ~$40-60 | Good performance | Ongoing costs |
| DigitalOcean 8GB | ~$25-40 | Simple setup | Limited scaling |
| Custom hardware | $0 (home PC) | No costs | Electricity + maintenance |

---

## Troubleshooting

### "Connection refused" Error

**Cause:** Ollama not running or unreachable

**Solution:**
1. Verify Ollama is running: `curl http://your-server:11434/api/tags`
2. Check firewall allows port 11434
3. Verify URL is correct in `llm.py` and `retrieval.py`

### "Model not found" Error

**Cause:** Models not pulled or not in Ollama

**Solution:**
```bash
ollama pull bge-m3
ollama pull deepseek-r1:1.5b
ollama list  # Verify models are installed
```

### Slow Responses

**Cause:** Network latency or server overload

**Solution:**
1. Check network latency: `ping your-server`
2. Monitor Ollama: `journalctl -u ollama -f`
3. Increase server resources
4. Consider using faster model (trade-off with quality)

### Memory Limit Exceeded

**Cause:** Streamlit Cloud running out of memory

**Solution:**
1. Reduce `top_k` slider default value
2. Optimize prompt size
3. Use faster/smaller model
4. Contact Streamlit for higher tier

---

## Security Best Practices

1. **Use HTTPS** when possible
   - Consider using ngrok or Cloudflare Tunnel (both support HTTPS)
   - For self-hosted: Use nginx reverse proxy with SSL

2. **Restrict access**
   - Use VPC/security groups to limit access
   - Consider API key authentication

3. **Monitor usage**
   - Log API calls
   - Set rate limits
   - Monitor for abuse

4. **Keep updated**
   - Regular `ollama pull` for latest models
   - Keep host OS patched
   - Monitor Ollama releases

---

## Next Steps

1. Choose deployment option (Local, Cloud VM, or Docker)
2. Set up Ollama server
3. Pull required models
4. Update base URLs in Streamlit app
5. Deploy to Streamlit Cloud
6. Test and monitor

---

**Need Help?**
- Ollama docs: https://github.com/ollama/ollama
- Streamlit Cloud docs: https://docs.streamlit.io/streamlit-community-cloud
- This project's README.md
