# SwingCoach Live - Backend API

Express.js REST API for managing golf swing sessions, analysis, and user data.

## 🚀 Quick Start

```bash
# Install dependencies
npm install

# Create .env file
cp ../../.env.example .env

# Start development server
npm run dev

# API runs on http://localhost:5000
```

## 📋 API Endpoints

### Authentication

```
POST   /api/auth/signup     - Register new user
POST   /api/auth/login      - Login user
POST   /api/auth/logout     - Logout
GET    /api/auth/profile    - Get user profile
```

### Sessions

```
POST   /api/sessions              - Create new session
GET    /api/sessions              - List user sessions
GET    /api/sessions/:id          - Get session details
PUT    /api/sessions/:id          - Update session
PUT    /api/sessions/:id/end      - End session
DELETE /api/sessions/:id          - Delete session
```

### Swings

```
POST   /api/swings                - Log new swing
GET    /api/swings/:id            - Get swing details
GET    /api/swings?session_id=    - List session swings
PUT    /api/swings/:id            - Update swing (add result)
DELETE /api/swings/:id            - Delete swing
```

### Analysis

```
POST   /api/analyze/video         - Upload & analyze video
GET    /api/analyze/:swing_id     - Get analysis results
GET    /api/analyze/history       - Get analysis history
```

### Users

```
GET    /api/users/profile         - Get user profile
PUT    /api/users/profile         - Update profile
GET    /api/users/stats           - Get user statistics
DELETE /api/users/:id             - Delete user account
```

### Health

```
GET    /health                    - Server health check
```

## 🏗️ Project Structure

```
backend/api/
├── src/
│   ├── routes/              # API route handlers
│   │   ├── auth.js
│   │   ├── sessions.js
│   │   ├── swings.js
│   │   ├── analysis.js
│   │   └── users.js
│   │
│   ├── middleware/          # Express middleware
│   │   ├── auth.js          # JWT authentication
│   │   ├── error.js         # Error handling
│   │   ├── validation.js    # Request validation
│   │   └── upload.js        # File upload handling
│   │
│   ├── models/              # Data models
│   │   ├── User.js
│   │   ├── Session.js
│   │   ├── Swing.js
│   │   └── Analysis.js
│   │
│   ├── services/            # Business logic
│   │   ├── authService.js
│   │   ├── sessionService.js
│   │   ├── swingService.js
│   │   └── analysisService.js
│   │
│   └── utils/               # Utilities
│       ├── db.js            # Database connection
│       ├── jwt.js           # JWT utilities
│       ├── validators.js    # Input validators
│       └── logger.js        # Logging
│
├── server.js               # Entry point
├── package.json
└── Dockerfile
```

## 🔌 Database

### Connection

Uses PostgreSQL with connection pooling:

```javascript
const { Pool } = require('pg')
const pool = new Pool({
  connectionString: process.env.DATABASE_URL
})
```

### Tables

- **users** - User accounts
- **sessions** - Practice sessions
- **swings** - Individual swing recordings
- **analyses** - AI analysis results
- **streaks** - Streak tracking
- **error_patterns** - Error frequency

See `../database/schema.sql` for full schema.

## 🔐 Authentication

Uses JWT (JSON Web Tokens):

```javascript
// Generate token
const token = jwt.sign({ userId }, process.env.JWT_SECRET, {
  expiresIn: '7d'
})

// Verify token in requests
app.use(authMiddleware) // Extracts and validates JWT
```

### Protected Routes

Add `authMiddleware` to protect endpoints:

```javascript
router.get('/api/sessions', authMiddleware, getSessionsHandler)
```

### Token Format

```
Authorization: Bearer <token>
```

## 📤 File Upload

Handles video uploads with Multer:

```javascript
// Limits
- Max file size: 100MB
- Allowed types: .mp4, .avi, .mov, .mkv
- Storage: ./uploads/videos/
```

Example:
```javascript
POST /api/analyze/video
Content-Type: multipart/form-data

file: <video file>
club: driver
```

## 🔍 Request Validation

Uses Joi for schema validation:

```javascript
const schema = Joi.object({
  email: Joi.string().email().required(),
  password: Joi.string().min(8).required(),
  club: Joi.string().valid('driver', 'iron', 'wedge')
})

const { error, value } = schema.validate(req.body)
```

## 🚀 Development

### Commands

```bash
# Development with auto-reload
npm run dev

# Start production
npm start

# Run tests
npm run test

# Run linter
npm run lint

# Format code
npm run format
```

### Environment Variables

```
NODE_ENV=development
API_PORT=5000
API_HOST=0.0.0.0
DATABASE_URL=postgresql://...
JWT_SECRET=your-secret-key
CORS_ORIGIN=http://localhost:3000
NEXT_PUBLIC_AI_WORKER_URL=http://localhost:8000
STORAGE_PATH=./uploads/videos
```

## 📊 Request/Response Examples

### Create Session

```
POST /api/sessions
Authorization: Bearer <token>
Content-Type: application/json

{
  "club": "driver",
  "name": "Morning Practice",
  "location": "Local Range"
}

Response (201):
{
  "id": "uuid-xxx",
  "user_id": "uuid-yyy",
  "club": "driver",
  "started_at": "2024-01-15T09:00:00Z",
  "total_swings": 0,
  "accuracy_percentage": 0
}
```

### Log Swing

```
POST /api/swings
Authorization: Bearer <token>
Content-Type: multipart/form-data

session_id: uuid-xxx
club: driver
video: <file>
shot_result: straight
sensation: clean
distance_variance_yards: 5

Response (201):
{
  "id": "uuid-swing-123",
  "session_id": "uuid-xxx",
  "swing_number": 1,
  "technical_score": 78,
  "lag_angle": 22.5,
  "issues": ["slow_tempo"],
  "suggested_tips": ["Increase backswing speed"]
}
```

### Get Session Metrics

```
GET /api/sessions/uuid-xxx/metrics
Authorization: Bearer <token>

Response (200):
{
  "session_id": "uuid-xxx",
  "total_swings": 15,
  "straight_shots": 9,
  "accuracy_percentage": 60,
  "best_streak": 4,
  "avg_technical_score": 75,
  "common_errors": ["tempo", "posture"],
  "duration_minutes": 45
}
```

## 🐛 Error Handling

All errors return consistent format:

```json
{
  "error": "Error message",
  "status": 400,
  "timestamp": "2024-01-15T09:00:00Z",
  "path": "/api/swings"
}
```

### Common Status Codes

- `200` - Success
- `201` - Created
- `400` - Bad request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not found
- `409` - Conflict
- `500` - Server error

## 📝 Logging

Logs to console with structure:

```
[2024-01-15 09:00:00] INFO - Server started on port 5000
[2024-01-15 09:00:05] POST /api/auth/login - 200
[2024-01-15 09:00:10] POST /api/sessions - 201
```

Set log level:
```
LOG_LEVEL=debug  # debug, info, warn, error
```

## 🧪 Testing

```bash
# Run all tests
npm run test

# Run with coverage
npm run test:coverage

# Run specific test
npm run test -- src/services/auth.test.js
```

### Test Example

```javascript
describe('Session Service', () => {
  test('creates new session', async () => {
    const session = await createSession(userId, { club: 'driver' })
    expect(session.club).toBe('driver')
  })
})
```

## 🔒 Security

- ✅ CORS configured properly
- ✅ Helmet.js for security headers
- ✅ Rate limiting (implement for production)
- ✅ Input validation with Joi
- ✅ JWT for authentication
- ✅ Bcrypt for password hashing
- ✅ SQL injection protection (parameterized queries)

### Security Headers

```
Strict-Transport-Security: max-age=31536000
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
Content-Security-Policy: default-src 'self'
```

## 📈 Performance

- Connection pooling: 20 connections
- Compression: gzip enabled
- Request timeout: 30 seconds
- Database query optimization (indexes on commonly queried fields)

## 🚀 Production Deploy

```bash
# Build
npm run build

# Run
NODE_ENV=production npm start

# Via Docker
docker build -t golf-coach-api .
docker run -p 5000:5000 golf-coach-api
```

## 📚 Dependencies

### Core
- **express**: Web framework
- **pg**: PostgreSQL client

### Middleware
- **cors**: Cross-origin requests
- **helmet**: Security headers
- **compression**: Response compression
- **morgan**: Request logging

### Security
- **jsonwebtoken**: JWT tokens
- **bcryptjs**: Password hashing

### Validation
- **joi**: Schema validation

### Utilities
- **uuid**: ID generation
- **dotenv**: Environment variables
- **multer**: File uploads

## 🤝 Contributing

1. Follow the code structure
2. Write tests for new features
3. Use consistent error handling
4. Document API changes
5. Keep security in mind

## 📖 Resources

- [Express.js Guide](https://expressjs.com)
- [PostgreSQL Docs](https://www.postgresql.org/docs)
- [JWT Tutorial](https://jwt.io/introduction)
- [Joi Validation](https://joi.dev)

## 📝 License

MIT License - see LICENSE file
