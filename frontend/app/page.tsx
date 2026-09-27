'use client'

import Link from 'next/link'
import { useRouter } from 'next/navigation'
import { useState } from 'react'
import toast from 'react-hot-toast'
import styles from './page.module.css'

export default function Home() {
  const router = useRouter()
  const [selectedClub, setSelectedClub] = useState('driver')
  const [isLoading, setIsLoading] = useState(false)

  const handleStartSession = async () => {
    setIsLoading(true)
    try {
      // Create a new session in the backend
      const response = await fetch('/api/sessions', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ club: selectedClub })
      })
      
      if (!response.ok) throw new Error('Failed to start session')
      
      const session = await response.json()
      toast.success(`Session started with ${selectedClub}`)
      router.push(`/session/${session.id}`)
    } catch (error) {
      toast.error('Failed to start session')
      console.error(error)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className={styles.container}>
      {/* Header */}
      <header className={styles.header}>
        <nav className={styles.nav}>
          <div className={styles.logo}>
            <span className={styles.icon}>⛳</span>
            <h1>SwingCoach Live</h1>
          </div>
          <div className={styles.navLinks}>
            <Link href="/history" className={styles.navLink}>
              📊 History
            </Link>
            <Link href="/profile" className={styles.navLink}>
              👤 Profile
            </Link>
          </div>
        </nav>
      </header>

      {/* Main Content */}
      <main className={styles.main}>
        {/* Hero Section */}
        <section className={styles.hero}>
          <div className={styles.heroContent}>
            <div className={styles.heroIcon}>🏌️</div>
            <h2>Real-Time Swing Analysis</h2>
            <p>Upload, analyze, improve—all during your practice session</p>
          </div>
        </section>

        {/* Club Selection */}
        <section className={styles.section}>
          <label className={styles.label}>Select your club</label>
          <div className={styles.clubGrid}>
            {[
              { id: 'driver', label: 'Driver', emoji: '🏌️' },
              { id: 'iron', label: 'Iron', emoji: '🔨' },
              { id: 'wedge', label: 'Wedge', emoji: '✨' },
            ].map(club => (
              <button
                key={club.id}
                onClick={() => setSelectedClub(club.id)}
                className={`${styles.clubButton} ${selectedClub === club.id ? styles.clubButtonActive : ''}`}
              >
                <span className={styles.clubEmoji}>{club.emoji}</span>
                <span className={styles.clubLabel}>{club.label}</span>
              </button>
            ))}
          </div>
        </section>

        {/* Features */}
        <section className={styles.section}>
          <h3 className={styles.sectionTitle}>What you get</h3>
          <div className={styles.featureGrid}>
            <div className={styles.featureCard}>
              <span className={styles.featureIcon}>📹</span>
              <h4>Video Analysis</h4>
              <p>AI-powered swing biomechanics with MediaPipe pose detection</p>
            </div>
            <div className={styles.featureCard}>
              <span className={styles.featureIcon}>📊</span>
              <h4>Live Metrics</h4>
              <p>Accuracy %, streak counter, technical score, and trends</p>
            </div>
            <div className={styles.featureCard}>
              <span className={styles.featureIcon}>💡</span>
              <h4>Instant Tips</h4>
              <p>Real-time corrective feedback and drill suggestions</p>
            </div>
            <div className={styles.featureCard}>
              <span className={styles.featureIcon}>🎯</span>
              <h4>Error Detection</h4>
              <p>Heatmap of common mistakes with pattern analysis</p>
            </div>
            <div className={styles.featureCard}>
              <span className={styles.featureIcon}>📈</span>
              <h4>Progress Tracking</h4>
              <p>Session history and progression analytics</p>
            </div>
            <div className={styles.featureCard}>
              <span className={styles.featureIcon}>🎮</span>
              <h4>Gamification</h4>
              <p>Streaks, achievements, and performance scoring</p>
            </div>
          </div>
        </section>

        {/* CTA Button */}
        <section className={styles.ctaSection}>
          <button
            onClick={handleStartSession}
            disabled={isLoading}
            className={styles.ctaButton}
          >
            {isLoading ? (
              <>
                <span className={styles.spinner}></span>
                Starting...
              </>
            ) : (
              <>
                <span>▶</span>
                Start Practice Session
              </>
            )}
          </button>
          <p className={styles.ctaHint}>
            Position your phone on a tripod for side and front views
          </p>
        </section>

        {/* How It Works */}
        <section className={styles.section}>
          <h3 className={styles.sectionTitle}>How it works</h3>
          <div className={styles.stepsGrid}>
            <div className={styles.step}>
              <div className={styles.stepNumber}>1</div>
              <h4>Record Video</h4>
              <p>Upload swing video from side and front angle</p>
            </div>
            <div className={styles.step}>
              <div className={styles.stepNumber}>2</div>
              <h4>Instant Analysis</h4>
              <p>AI analyzes swing mechanics and detects issues</p>
            </div>
            <div className={styles.step}>
              <div className={styles.stepNumber}>3</div>
              <h4>Get Feedback</h4>
              <p>Receive tips and see your technical score</p>
            </div>
            <div className={styles.step}>
              <div className={styles.stepNumber}>4</div>
              <h4>Log Result</h4>
              <p>Record shot outcome and how it felt</p>
            </div>
            <div className={styles.step}>
              <div className={styles.stepNumber}>5</div>
              <h4>Apply & Improve</h4>
              <p>Apply feedback immediately to next swing</p>
            </div>
            <div className={styles.step}>
              <div className={styles.stepNumber}>6</div>
              <h4>Track Progress</h4>
              <p>View session metrics and improve over time</p>
            </div>
          </div>
        </section>
      </main>

      {/* Footer */}
      <footer className={styles.footer}>
        <p>Built for golfers who want to improve during practice</p>
        <p className={styles.footerMeta}>
          v1.0.0 • <Link href="/about">About</Link> • <Link href="/docs">Docs</Link>
        </p>
      </footer>
    </div>
  )
}
