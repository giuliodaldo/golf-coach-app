# SwingCoach Live - Golf Swing Analysis App

**Real-time golf swing analysis with AI-powered coaching during your practice session.**

Built with: Next.js + Node.js + Python FastAPI + PostgreSQL + MediaPipe

---

## 🚀 Quick Start

### Prerequisites
- Node.js 18+
- Python 3.9+
- PostgreSQL (or use Supabase free tier)
- Docker (optional, for containerized deployment)

### 1. Clone & Setup Environment

```bash
git clone <repo-url>
cd golf-coach-app

# Copy environment template
cp .env.example .env.local

# Edit .env.local with your database credentials
nano .env.local
```

### 2. Frontend Setup

```bash
cd frontend
npm install
npm run dev
# App runs on http://localhost:3000
```

### 3. Backend API Setup

```bash
cd backend/api
npm install
npm start
# API runs on http://localhost:5000
```

### 4. AI Worker Setup

```bash
cd backend/ai-worker
pip install -r requirements.txt
python main.py
# Worker runs on http://localhost:8000
```

### 5. Database Setup

```bash
# Option A: Use Supabase free tier
# 1. Create account at https://supabase.com
# 2. Create new project
# 3. Get connection string from Project Settings > Database
# 4. Add to .env.local as DATABASE_URL

# Option B: Local PostgreSQL
createdb golf_coach
psql golf_coach < backend/database/schema.sql
```

---

## 📁 Project Structure

```
golf-coach-app/
├── frontend/                 # Next.js + React web app
│   ├── app/                  # Next.js app router
│   ├── components/           # Reusable React components
│   ├── lib/                  # Utilities, API clients
│   ├── public/              # Static assets
│   ├── package.json
│   └── next.config.js
│
├── backend/
│   ├── api/                 # Node.js + Express REST API
│   │   ├── src/
│   │   │   ├── routes/      # API endpoints
│   │   │   ├── middleware/  # Auth, logging, error handling
│   │   │   ├── models/      # Database models
│   │   │   ├── services/    # Business logic
│   │   │   └── utils/       # Helpers
│   │   ├── package.json
│   │   └── server.js
│   │
│   ├── ai-worker/           # Python FastAPI AI engine
│   │   ├── main.py          # FastAPI app
│   │   ├── pose_detector.py # MediaPipe integration
│   │   ├── swing_analyzer.py # Swing analysis logic
│   │   ├── requirements.txt
│   │   └── models/          # ML models
│   │
│   └── database/
│       ├── schema.sql       # Database schema
│       └── migrations/      # Schema changes
│
├── docker-compose.yml       # Container orchestration
├── .env.example            # Environment variables template
└── README.md               # This file
```

---

## 🔑 Environment Variables

Create `.env.local`:

```
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/golf_coach
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_ANON_KEY=xxxxx
SUPABASE_SERVICE_KEY=xxxxx

# Storage
STORAGE_PATH=./uploads/videos

# API Keys
NEXT_PUBLIC_API_URL=http://localhost:5000
NEXT_PUBLIC_AI_WORKER_URL=http://localhost:8000

# JWT
JWT_SECRET=your-secret-key-change-this

# Node Environment
NODE_ENV=development
```

---

## 🎯 Features

### ✅ Real-Time Swing Analysis
- Upload video (side + front view)
- Instant AI analysis with MediaPipe pose detection
- Biomechanical metrics (lag angle, face angle, posture)
- Error detection & correction tips

### ✅ Live Coaching During Session
- Record shot result (straight/slight/miss)
- Log sensation (clean/good/off/poor)
- Track distance variance
- Immediate corrective feedback

### ✅ Session Dashboard
- Live metrics (accuracy %, streak counter, best streak)
- Heatmap of common errors
- Achievement tracking
- Progression visualization

### ✅ Swing History
- Per-swing logging with timestamps
- Video library
- Progressive trend analysis
- Benchmark vs personal best

### ✅ AI-Powered Coaching
- MediaPipe pose detection (body landmarks, angles)
- Swing anomaly detection (ML classification)
- Personalized drill suggestions
- Emotion/sensation correlation

---

## 🏗️ Tech Stack

### Frontend
- **Framework**: Next.js 14 (App Router)
- **UI**: React 18 + CSS Modules
- **State**: React Context + hooks
- **HTTP Client**: Fetch API
- **Video**: HTML5 Video API
- **Charts**: Chart.js

### Backend API
- **Runtime**: Node.js 18
- **Framework**: Express.js
- **DB ORM**: Prisma
- **Auth**: JWT
- **Validation**: Joi
- **File Upload**: Multer

### AI Worker
- **Framework**: FastAPI (Python)
- **CV**: MediaPipe, OpenCV
- **ML**: TensorFlow/PyTorch
- **Pose Detection**: MediaPipe Pose
- **Data Processing**: NumPy, Pandas

### Database
- **Primary**: PostgreSQL (Supabase free tier)
- **Caching**: Redis (optional)
- **Storage**: Supabase Storage / S3 (optional)

### DevOps
- **Containerization**: Docker
- **Orchestration**: Docker Compose
- **Frontend Deploy**: Vercel (free)
- **Backend Deploy**: Railway.app or Fly.io (free tier)

---

## 📊 API Endpoints

### Swings
```
POST   /api/swings              - Create swing
GET    /api/swings/:id          - Get swing details
GET    /api/swings?session_id=  - List session swings
PUT    /api/swings/:id          - Update swing result
DELETE /api/swings/:id          - Delete swing
```

### Sessions
```
POST   /api/sessions            - Create session
GET    /api/sessions/:id        - Get session metrics
GET    /api/sessions            - List user sessions
PUT    /api/sessions/:id/end    - End session
```

### Analysis
```
POST   /api/analyze/video       - Upload & analyze swing video
GET    /api/analyze/history     - Get analysis history
```

### Auth
```
POST   /api/auth/signup         - Register user
POST   /api/auth/login          - Login user
POST   /api/auth/logout         - Logout
GET    /api/auth/profile        - Get user profile
```

---

## 🚀 Deployment

### Option 1: Vercel + Railway (Recommended)

**Frontend on Vercel:**
```bash
cd frontend
npm install -g vercel
vercel
# Follow prompts, connect GitHub repo
```

**Backend API on Railway:**
1. Push code to GitHub
2. Create Railway.app account
3. New Project > GitHub > Select repo
4. Add PostgreSQL plugin
5. Set environment variables
6. Deploy

**AI Worker on Railway:**
1. Create new service in same Railway project
2. Select `backend/ai-worker` root directory
3. Set startup command: `python main.py`
4. Deploy

### Option 2: Docker Compose (Local/Self-Hosted)

```bash
docker-compose up -d
# Frontend: http://localhost:3000
# API: http://localhost:5000
# AI Worker: http://localhost:8000
# Database: PostgreSQL on port 5432
```

### Option 3: Fly.io (Full Stack)

```bash
# Install Fly CLI
curl -L https://fly.io/install.sh | sh

# Deploy entire stack
fly launch --dockerfile docker-compose.yml
```

---

## 🔐 Security Notes

- Always use HTTPS in production
- Never commit `.env.local` to git (use `.env.example`)
- Rotate `JWT_SECRET` in production
- Use strong database passwords
- Enable API rate limiting
- Validate all file uploads
- Run database migrations before deploy

---

## 🧪 Testing

### Frontend Tests
```bash
cd frontend
npm run test
npm run test:watch
```

### Backend Tests
```bash
cd backend/api
npm run test
npm run test:coverage
```

### AI Tests
```bash
cd backend/ai-worker
pytest tests/ -v
```

---

## 📝 Database Schema

See `backend/database/schema.sql` for full schema.

**Core Tables:**
- `users` - User accounts
- `sessions` - Practice sessions
- `swings` - Individual swing recordings
- `analyses` - AI analysis results
- `videos` - Video metadata & storage

---

## 🐛 Troubleshooting

### Frontend won't connect to API
- Check `NEXT_PUBLIC_API_URL` matches API server
- Ensure CORS is enabled in API
- Check firewall/proxy settings

### AI Worker crashes on video upload
- Check Python dependencies: `pip install -r requirements.txt`
- Ensure MediaPipe is compiled for your OS
- Check disk space for video processing

### Database connection fails
- Verify PostgreSQL is running
- Check `DATABASE_URL` format
- Ensure user has CREATE permissions

### Video not processing
- Check file size (max 100MB recommended)
- Verify video codec (H.264 preferred)
- Check worker logs for errors

---

## 📚 Documentation

- [Frontend Setup Guide](./frontend/README.md)
- [API Documentation](./backend/api/README.md)
- [AI Worker Guide](./backend/ai-worker/README.md)
- [Database Schema](./backend/database/README.md)

---

## 🤝 Contributing

1. Fork the repo
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit: `git commit -m 'Add amazing feature'`
4. Push: `git push origin feature/amazing-feature`
5. Open Pull Request

---

## 📄 License

MIT License - see LICENSE file

---

## 👨‍💼 Built for

Golf coaching during live practice sessions. Real-time feedback to improve swing mechanics instantly.

**Made with ⛳ and code**
