# Deployment Guide - SwingCoach Live

Complete step-by-step instructions to deploy the full stack with zero costs.

---

## 🎯 Option 1: Local Development (Fastest)

### Prerequisites
- Docker & Docker Compose
- 2GB+ RAM
- 5GB disk space for videos

### Quick Start

```bash
# Clone & setup
git clone <repo-url> golf-coach-app
cd golf-coach-app
cp .env.example .env.local

# Edit .env.local with your database settings
nano .env.local

# Start entire stack with one command
docker-compose up

# That's it! Access:
# - Frontend: http://localhost:3000
# - API: http://localhost:5000
# - AI Worker: http://localhost:8000
# - Database UI: http://localhost:8080 (Adminer)
```

### Accessing the App

```
Frontend:    http://localhost:3000
API:         http://localhost:5000/health
AI Worker:   http://localhost:8000/docs
Database:    http://localhost:8080
             Username: postgres
             Password: postgres
             Database: golf_coach
```

### Stop & Cleanup

```bash
# Stop all services
docker-compose down

# Stop and remove volumes (delete data)
docker-compose down -v

# View logs
docker-compose logs -f frontend
docker-compose logs -f api
docker-compose logs -f ai_worker
```

---

## 🌐 Option 2: Vercel + Railway (Recommended for Production)

### A. Frontend on Vercel (Free Tier)

**Step 1: Push code to GitHub**
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/golf-coach-app
git push -u origin main
```

**Step 2: Deploy to Vercel**
```bash
# Install Vercel CLI
npm install -g vercel

# Login
vercel login

# Deploy frontend
cd frontend
vercel

# When prompted:
# - Project name: golf-coach-app
# - Directory: ./
# - Build command: next build
# - Output directory: .next

# Set environment variables
vercel env add NEXT_PUBLIC_API_URL https://api.your-domain.com
vercel env add NEXT_PUBLIC_AI_WORKER_URL https://ai-worker.your-domain.com
```

**Frontend URL:** `golf-coach-app.vercel.app`

---

### B. Backend API on Railway (Free Tier)

**Step 1: Create Railway account**
- Visit https://railway.app
- Sign up with GitHub
- Create new project

**Step 2: Connect GitHub**
```
1. New Project > GitHub Repo
2. Select golf-coach-app repo
3. Select backend/api as root directory
```

**Step 3: Configure environment**
```
1. Click "Configure" tab
2. Add environment variables:
   - NODE_ENV: production
   - DATABASE_URL: (See PostgreSQL setup below)
   - JWT_SECRET: (generate random string)
   - CORS_ORIGIN: https://golf-coach-app.vercel.app
   - NEXT_PUBLIC_AI_WORKER_URL: https://ai-worker-xxx.railway.app
   - API_PORT: 5000
```

**Step 4: Add PostgreSQL**
```
1. New > Database > PostgreSQL
2. Railway auto-creates DATABASE_URL
3. Copy to your config
```

**API URL:** `https://api-xxx.railway.app`

---

### C. AI Worker on Railway (Free Tier)

**Step 1: Create new service**
```
1. Same project > New Service > GitHub Repo
2. Select root directory: backend/ai-worker
3. Configure:
   - Start command: python main.py
   - Python version: 3.11
```

**Step 2: Set environment variables**
```
AI_WORKER_PORT: 8000
AI_WORKER_HOST: 0.0.0.0
MEDIAPIPE_GPU: false
MEDIAPIPE_CONFIDENCE_THRESHOLD: 0.5
```

**AI Worker URL:** `https://ai-worker-xxx.railway.app`

---

### D. Database Setup (Supabase - Free Tier)

**Step 1: Create Supabase account**
- Visit https://supabase.com
- Sign up
- Create new project

**Step 2: Get connection details**
```
1. Project Settings > Database
2. Connection string under "Connection Info"
3. Format: postgresql://user:password@host:port/database
```

**Step 3: Initialize schema**
```bash
# Option A: Use psql CLI
psql your-connection-string < backend/database/schema.sql

# Option B: Supabase SQL Editor
# Copy schema.sql content and run in Supabase dashboard
```

**Step 4: Update environment**
```
DATABASE_URL=postgresql://user:password@db.supabase.co:5432/postgres
```

---

## 🚀 Option 3: Full Stack on Fly.io (Single Platform)

### Prerequisites
```bash
# Install Fly CLI
curl -L https://fly.io/install.sh | sh

# Login
flyctl auth login

# Create Fly account if needed
```

### Deploy

```bash
# Initialize Fly app
flyctl launch

# When prompted:
# - App name: golf-coach-app
# - Region: closest to you
# - Postgres: yes
# - Redis: no

# Set secrets
flyctl secrets set NODE_ENV=production
flyctl secrets set JWT_SECRET=$(openssl rand -hex 32)
flyctl secrets set DATABASE_URL=$(flyctl postgres attach golf-coach-app-db --app golf-coach-app)

# Deploy
flyctl deploy

# View logs
flyctl logs -a golf-coach-app
```

---

## 📊 Monitoring & Debugging

### Check Frontend
```bash
# Vercel dashboard
https://vercel.com/dashboard

# View logs
vercel logs golf-coach-app
```

### Check Backend API
```bash
# Railway dashboard
https://railway.app/dashboard

# View logs
# Click project > api service > Logs tab

# Test health
curl https://api-xxx.railway.app/health
```

### Check AI Worker
```bash
# Railway dashboard
# Click project > ai-worker service > Logs tab

# Test API docs
https://ai-worker-xxx.railway.app/docs
```

### Check Database
```bash
# Supabase dashboard
https://app.supabase.com

# Connect with psql
psql your-connection-string

# Or use Adminer (local only)
http://localhost:8080
```

---

## 🔐 Security Checklist

- [ ] Change JWT_SECRET to random string
- [ ] Use HTTPS everywhere (Vercel/Railway provide this)
- [ ] Set strong database password (Supabase)
- [ ] Enable API rate limiting (add to Express middleware)
- [ ] Setup CORS properly (add domains to CORS_ORIGIN)
- [ ] Never commit .env to git (use .env.example)
- [ ] Enable HTTPS-only in production
- [ ] Regular database backups (Supabase auto-backup)
- [ ] Monitor API usage (Railway provides monitoring)

---

## 🐛 Troubleshooting

### "Connection refused" from Frontend to API
- Check API_URL in frontend .env
- Ensure backend is running
- Check CORS settings in backend
- Verify firewall allows traffic

### "No database" errors
- Check DATABASE_URL format
- Verify credentials are correct
- Ensure schema is initialized
- Check PostgreSQL is running

### "MediaPipe not found" in AI worker
- Rebuild Docker image: `docker-compose build ai_worker`
- Check Python 3.9+ is installed
- Verify all dependencies: `pip install -r requirements.txt`

### High latency on AI analysis
- Video too large (limit to <100MB)
- Reduce resolution (1080p OK, 4K slow)
- Use H.264 codec (more compatible)
- GPU disabled (expected, use CPU)

### Out of memory
- Reduce video frame rate
- Process shorter clips
- Increase Railway memory (paid)
- Use serverless auto-scaling

---

## 💰 Cost Breakdown (Free Tier)

| Service | Free Tier | Limits |
|---------|-----------|--------|
| **Vercel** | ✅ $0 | 100GB/month bandwidth |
| **Railway** | ✅ $0 | $5 credit/month (usually enough) |
| **Supabase** | ✅ $0 | 500MB storage, 2GB/month egress |
| **Docker** | ✅ $0 | Local development only |
| **GitHub** | ✅ $0 | Private repos, CI/CD |
| **Total** | **$0/month** | Perfect for hobby/learning |

**Upgrade path** (if you exceed free limits):
- Railway: $0.50/CPU-hour
- Supabase: $25/month (starts at 10GB)
- Vercel: $20/month (if needed)

---

## 📈 Production Scaling

When you need to scale beyond free tier:

1. **Database:** Supabase → AWS RDS (~$50/month)
2. **Backend:** Railway → AWS ECS (~$100/month)
3. **AI Worker:** Railway → AWS ECS (~$100/month)
4. **Storage:** Supabase → AWS S3 (~$1/month)
5. **CDN:** Vercel → CloudFlare (~$20/month)

Estimated cost: ~$270/month for production scale.

---

## 🎓 Learning Resources

- [Next.js Deployment](https://nextjs.org/docs/deployment)
- [Railway Documentation](https://railway.app/docs)
- [Supabase Docs](https://supabase.com/docs)
- [Express.js Best Practices](https://expressjs.com)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment)
- [Docker Documentation](https://docs.docker.com)

---

## 📞 Support

- **Issues:** GitHub Issues
- **Discussions:** GitHub Discussions
- **Email:** support@golfcoach.app

---

## ✅ Deployment Checklist

Before going live:

- [ ] All environment variables set
- [ ] Database schema initialized
- [ ] CORS origins configured
- [ ] JWT secret changed
- [ ] API health check passing
- [ ] Frontend can connect to API
- [ ] Video upload works
- [ ] Analysis returns results
- [ ] Error logs reviewed
- [ ] Performance acceptable
- [ ] Security scan passed
- [ ] Backup strategy in place

**You're ready to launch!** 🚀
