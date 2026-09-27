-- ============================================================================
-- SwingCoach Live - Database Schema
-- PostgreSQL Database
-- ============================================================================

-- ============================================================================
-- Users Table
-- ============================================================================
CREATE TABLE IF NOT EXISTS users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  first_name VARCHAR(255),
  last_name VARCHAR(255),
  handicap INT,
  skill_level VARCHAR(50) DEFAULT 'amateur', -- amateur, intermediate, advanced
  timezone VARCHAR(100) DEFAULT 'UTC',
  preferences JSONB DEFAULT '{}',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  deleted_at TIMESTAMP,
  
  CONSTRAINT email_format CHECK (email ~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$')
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_created_at ON users(created_at);

-- ============================================================================
-- Sessions Table (practice sessions)
-- ============================================================================
CREATE TABLE IF NOT EXISTS sessions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  club VARCHAR(50) NOT NULL, -- driver, iron, wedge, etc
  name VARCHAR(255),
  description TEXT,
  location VARCHAR(255),
  weather JSONB DEFAULT '{}',
  started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  ended_at TIMESTAMP,
  duration_minutes INT,
  
  -- Session statistics
  total_swings INT DEFAULT 0,
  straight_shots INT DEFAULT 0,
  accuracy_percentage DECIMAL(5, 2) DEFAULT 0,
  best_streak INT DEFAULT 0,
  avg_technical_score DECIMAL(5, 2) DEFAULT 0,
  
  metadata JSONB DEFAULT '{}',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_sessions_user_id ON sessions(user_id);
CREATE INDEX idx_sessions_started_at ON sessions(started_at);
CREATE INDEX idx_sessions_club ON sessions(club);

-- ============================================================================
-- Swings Table (individual swing recordings)
-- ============================================================================
CREATE TABLE IF NOT EXISTS swings (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  session_id UUID NOT NULL REFERENCES sessions(id) ON DELETE CASCADE,
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  club VARCHAR(50) NOT NULL,
  swing_number INT NOT NULL,
  
  -- Video metadata
  video_path VARCHAR(500),
  video_duration_seconds DECIMAL(10, 2),
  video_angles VARCHAR(100), -- side, front, both
  
  -- Swing mechanics
  lag_angle DECIMAL(5, 2),
  face_angle DECIMAL(5, 2),
  posture VARCHAR(50), -- poor, fair, good, excellent
  backswing_plane VARCHAR(50),
  tempo_score DECIMAL(5, 2),
  
  -- Technical analysis
  technical_score DECIMAL(5, 2),
  issues TEXT[], -- array of issue strings
  
  -- User input
  shot_result VARCHAR(50) NOT NULL, -- straight, slight_right, slight_left, miss
  distance_variance_yards INT, -- vs normal
  sensation VARCHAR(50), -- clean, good, off, poor
  
  -- Corrections
  suggested_tips TEXT[],
  correction_focus VARCHAR(255),
  
  sequence_number INT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_swings_session_id ON swings(session_id);
CREATE INDEX idx_swings_user_id ON swings(user_id);
CREATE INDEX idx_swings_created_at ON swings(created_at);
CREATE INDEX idx_swings_club ON swings(club);

-- ============================================================================
-- Analyses Table (AI analysis results)
-- ============================================================================
CREATE TABLE IF NOT EXISTS analyses (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  swing_id UUID NOT NULL REFERENCES swings(id) ON DELETE CASCADE,
  
  -- Analysis metadata
  analysis_type VARCHAR(50) NOT NULL, -- biomechanics, error_detection, etc
  model_version VARCHAR(50),
  processing_time_ms INT,
  
  -- Detected issues
  primary_issue VARCHAR(255),
  secondary_issues VARCHAR(255)[],
  issue_severity VARCHAR(50)[], -- minor, moderate, major
  
  -- Recommendations
  correction_exercises TEXT[],
  drill_suggestions TEXT[],
  estimated_impact TEXT,
  
  -- Raw analysis data
  landmarks JSONB, -- MediaPipe pose landmarks
  angles JSONB,
  metrics JSONB,
  
  confidence_score DECIMAL(5, 2),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_analyses_swing_id ON analyses(swing_id);

-- ============================================================================
-- Streaks Table
-- ============================================================================
CREATE TABLE IF NOT EXISTS streaks (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  session_id UUID NOT NULL REFERENCES sessions(id) ON DELETE CASCADE,
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  
  streak_type VARCHAR(50) NOT NULL, -- straight_shots, good_technique, etc
  current_count INT DEFAULT 1,
  highest_count INT DEFAULT 1,
  
  started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_streaks_session_id ON streaks(session_id);
CREATE INDEX idx_streaks_user_id ON streaks(user_id);

-- ============================================================================
-- Progress History Table
-- ============================================================================
CREATE TABLE IF NOT EXISTS progress_history (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  
  metric_name VARCHAR(100) NOT NULL, -- accuracy_percentage, avg_score, etc
  metric_value DECIMAL(10, 2),
  session_id UUID REFERENCES sessions(id) ON DELETE SET NULL,
  
  recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_progress_history_user_id ON progress_history(user_id);
CREATE INDEX idx_progress_history_metric_name ON progress_history(metric_name);

-- ============================================================================
-- Error Patterns Table (for heatmap)
-- ============================================================================
CREATE TABLE IF NOT EXISTS error_patterns (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  session_id UUID REFERENCES sessions(id) ON DELETE CASCADE,
  
  error_type VARCHAR(100) NOT NULL, -- tempo, posture, alignment, etc
  frequency INT DEFAULT 1,
  last_occurred TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  
  -- Metadata
  context JSONB DEFAULT '{}'
);

CREATE INDEX idx_error_patterns_user_id ON error_patterns(user_id);
CREATE INDEX idx_error_patterns_error_type ON error_patterns(error_type);

-- ============================================================================
-- Achievements/Badges Table
-- ============================================================================
CREATE TABLE IF NOT EXISTS achievements (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  
  badge_type VARCHAR(100) NOT NULL, -- first_session, 10_straight_shots, etc
  badge_name VARCHAR(255),
  description TEXT,
  
  earned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  session_id UUID REFERENCES sessions(id)
);

CREATE INDEX idx_achievements_user_id ON achievements(user_id);

-- ============================================================================
-- Training Plans Table (optional for future)
-- ============================================================================
CREATE TABLE IF NOT EXISTS training_plans (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  
  name VARCHAR(255) NOT NULL,
  description TEXT,
  focus_areas VARCHAR(100)[],
  exercises JSONB,
  
  is_active BOOLEAN DEFAULT true,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_training_plans_user_id ON training_plans(user_id);

-- ============================================================================
-- Views for Common Queries
-- ============================================================================

-- User session statistics
CREATE OR REPLACE VIEW user_session_stats AS
SELECT 
  u.id as user_id,
  u.email,
  COUNT(DISTINCT s.id) as total_sessions,
  COUNT(DISTINCT sw.id) as total_swings,
  AVG(s.accuracy_percentage) as avg_accuracy,
  AVG(s.avg_technical_score) as avg_score,
  MAX(s.best_streak) as personal_best_streak,
  MAX(s.started_at) as last_session_date
FROM users u
LEFT JOIN sessions s ON u.id = s.user_id AND s.deleted_at IS NULL
LEFT JOIN swings sw ON s.id = sw.session_id
GROUP BY u.id, u.email;

-- Recent swings with analysis
CREATE OR REPLACE VIEW recent_swings_with_analysis AS
SELECT 
  sw.id,
  sw.swing_number,
  sw.session_id,
  sw.user_id,
  sw.club,
  sw.technical_score,
  sw.shot_result,
  sw.sensation,
  a.primary_issue,
  a.issue_severity,
  sw.created_at
FROM swings sw
LEFT JOIN analyses a ON sw.id = a.swing_id
ORDER BY sw.created_at DESC;

-- ============================================================================
-- Create Triggers for Updated Timestamps
-- ============================================================================

CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = CURRENT_TIMESTAMP;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_sessions_updated_at BEFORE UPDATE ON sessions
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_swings_updated_at BEFORE UPDATE ON swings
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_analyses_updated_at BEFORE UPDATE ON analyses
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ============================================================================
-- Initial Data (optional sample data)
-- ============================================================================

-- Uncomment to seed sample data
-- INSERT INTO users (email, password_hash, first_name, last_name, handicap, skill_level)
-- VALUES ('demo@golfcoach.app', '$2a$10$...', 'Demo', 'User', 10, 'intermediate');
