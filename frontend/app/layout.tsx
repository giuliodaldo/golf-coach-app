import type { Metadata } from 'next'
import './globals.css'
import { Toaster } from 'react-hot-toast'

export const metadata: Metadata = {
  title: 'SwingCoach Live - Golf Swing Analysis',
  description: 'Real-time AI-powered golf swing analysis during your practice session',
  viewport: 'width=device-width, initial-scale=1, viewport-fit=cover',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <head>
        <meta name="theme-color" content="#0f4c2f" />
        <meta name="mobile-web-app-capable" content="yes" />
        <meta name="apple-mobile-web-app-capable" content="yes" />
        <meta name="apple-mobile-web-app-status-bar-style" content="black" />
      </head>
      <body>
        <main className="app-container">
          {children}
        </main>
        <Toaster
          position="bottom-center"
          toastOptions={{
            duration: 4000,
            style: {
              background: '#0f4c2f',
              color: '#fff',
              borderRadius: '8px',
              border: '1px solid rgba(255,215,0,0.2)',
            },
          }}
        />
      </body>
    </html>
  )
}
