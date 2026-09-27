import express from 'express'
import cors from 'cors'
import helmet from 'helmet'
import compression from 'compression'
import morgan from 'morgan'
import dotenv from 'dotenv'
import { fileURLToPath } from 'url'
import { dirname, join } from 'path'
import { Pool } from 'pg'
import fs from 'fs'

// Load environment variables
dotenv.config()

// Get __dirname equivalent
const __filename = fileURLToPath(import.meta.url)
const __dirname = dirname(__filename)

// Initialize Express
const app = express()
const PORT = process.env.API_PORT || 5000
const HOST = process.env.API_HOST || '0.0.0.0'

// ============================================================================
// Database Connection
// ============================================================================
export const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  ssl: process.env.NODE_ENV === 'production' ? { rejectUnauthorized: false } : false,
})

pool.on('error', (err) => {
  console.error('Unexpected error on idle client', err)
})

// Test database connection
pool.query('SELECT NOW()', (err, res) => {
  if (err) {
    console.error('Database connection error:', err)
  } else {
    console.log('✅ Database connected:', res.rows[0].now)
  }
})

// ============================================================================
// Middleware
// ============================================================================

// Security headers
app.use(helmet())

// Compression
app.use(compression())

// CORS
const corsOrigins = (process.env.CORS_ORIGIN || 'http://localhost:3000').split(',')
app.use(cors({
  origin: corsOrigins,
  credentials: true,
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Authorization'],
}))

// Request logging
app.use(morgan('combined'))

// Body parsing
app.use(express.json({ limit: '50mb' }))
app.use(express.urlencoded({ limit: '50mb', extended: true }))

// Create uploads directory if it doesn't exist
const uploadDir = process.env.STORAGE_PATH || './uploads/videos'
if (!fs.existsSync(uploadDir)) {
  fs.mkdirSync(uploadDir, { recursive: true })
}

// Serve static files (uploaded videos)
app.use('/uploads', express.static(uploadDir))

// ============================================================================
// Routes
// ============================================================================

// Health check
app.get('/health', (req, res) => {
  res.json({
    status: 'ok',
    timestamp: new Date().toISOString(),
    uptime: process.uptime(),
  })
})

// API Routes placeholder
app.use('/api/auth', (req, res) => {
  res.json({ message: 'Auth routes - implement authentication endpoints' })
})

app.use('/api/sessions', (req, res) => {
  res.json({ message: 'Session routes - implement session management' })
})

app.use('/api/swings', (req, res) => {
  res.json({ message: 'Swing routes - implement swing logging' })
})

app.use('/api/analyze', (req, res) => {
  res.json({ message: 'Analysis routes - implement video analysis' })
})

app.use('/api/users', (req, res) => {
  res.json({ message: 'User routes - implement user management' })
})

// 404 handler
app.use((req, res) => {
  res.status(404).json({
    error: 'Not found',
    path: req.path,
    method: req.method,
  })
})

// Error handler
app.use((err, req, res, next) => {
  console.error('Error:', err)
  
  res.status(err.status || 500).json({
    error: err.message || 'Internal server error',
    ...(process.env.NODE_ENV === 'development' && { stack: err.stack }),
  })
})

// ============================================================================
// Start Server
// ============================================================================

const server = app.listen(PORT, HOST, () => {
  console.log(`
╔════════════════════════════════════════════════════════════════╗
║         🏌️  SwingCoach Live - Backend API Started              ║
║                                                                ║
║  📍 Server: http://${HOST}:${PORT}                            
║  🗄️  Database: ${process.env.DATABASE_URL ? 'Connected' : 'Disconnected'}              
║  🌍 Environment: ${process.env.NODE_ENV || 'development'}                  
║                                                                ║
║  Routes:                                                       ║
║  - GET  /health                - Health check                 ║
║  - POST /api/auth/signup       - Register                     ║
║  - POST /api/auth/login        - Login                        ║
║  - GET  /api/sessions          - List sessions                ║
║  - POST /api/sessions          - Create session               ║
║  - POST /api/analyze/video     - Upload & analyze video       ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
  `)
})

// Graceful shutdown
process.on('SIGTERM', () => {
  console.log('SIGTERM signal received: closing HTTP server')
  server.close(() => {
    console.log('HTTP server closed')
    pool.end(() => {
      console.log('Database pool closed')
      process.exit(0)
    })
  })
})

process.on('SIGINT', () => {
  console.log('SIGINT signal received: closing HTTP server')
  server.close(() => {
    console.log('HTTP server closed')
    pool.end(() => {
      console.log('Database pool closed')
      process.exit(0)
    })
  })
})

export default app
