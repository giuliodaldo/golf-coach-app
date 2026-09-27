# SwingCoach Live - Frontend

Next.js 14 React application for real-time golf swing analysis.

## 🚀 Quick Start

```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Open browser
# http://localhost:3000
```

## 📁 Project Structure

```
frontend/
├── app/                    # Next.js App Router
│   ├── layout.tsx         # Root layout
│   ├── page.tsx           # Home page
│   ├── globals.css        # Global styles
│   └── page.module.css    # Page-specific styles
│
├── components/            # Reusable React components
│   ├── SessionCamera.tsx  # Video upload & preview
│   ├── SwingAnalysis.tsx  # Analysis display
│   ├── SessionDashboard.tsx # Metrics & charts
│   ├── LoadingSpinner.tsx # Loading indicator
│   └── Toast.tsx          # Notifications
│
├── lib/                   # Utilities
│   ├── api-client.ts      # API communication
│   ├── hooks.ts           # Custom React hooks
│   ├── constants.ts       # App constants
│   └── utils.ts           # Helper functions
│
├── types/                 # TypeScript types
│   └── index.ts           # All type definitions
│
├── public/               # Static assets
│   └── favicon.ico
│
├── package.json
├── next.config.js
├── tsconfig.json
└── README.md
```

## 🛠️ Development

### Commands

```bash
# Development server with hot reload
npm run dev

# Build for production
npm run build

# Start production server
npm start

# Run tests
npm run test

# Run tests in watch mode
npm run test:watch

# Lint code
npm run lint

# Format code
npm run format

# Type check
npm run type-check
```

### File Organization

- **Components:** Reusable UI components
- **Pages:** Next.js route pages
- **Lib:** Utilities, hooks, API client
- **Public:** Static assets
- **Styles:** CSS modules for scoped styling

## 🎨 Styling

This project uses:
- CSS Modules for component scoping
- CSS Variables for theming
- Responsive design (mobile-first)
- Dark mode support (system preference)

### CSS Variables

```css
--primary-green: #0f4c2f
--primary-gold: #ffd700
--text-primary: #ffffff
--text-secondary: rgba(255, 255, 255, 0.7)
```

## 🔗 API Integration

### API Client

```typescript
import { apiClient } from '@/lib/api-client'

// GET request
const sessions = await apiClient.get('/api/sessions')

// POST request
const analysis = await apiClient.post('/api/analyze/video', formData)

// With error handling
try {
  const result = await apiClient.post('/api/sessions', data)
} catch (error) {
  console.error('Failed:', error)
}
```

### Environment Variables

```bash
NEXT_PUBLIC_API_URL=http://localhost:5000
NEXT_PUBLIC_AI_WORKER_URL=http://localhost:8000
```

## 📊 State Management

Using React Context + Hooks for simple state:

```typescript
import { useSession } from '@/lib/hooks'

export function MyComponent() {
  const { session, setSession } = useSession()
  // ...
}
```

## 🎯 Key Pages

### Home (/)
- Club selection
- Session overview
- Quick start button

### Session (/session/[id])
- Video upload interface
- Live analysis display
- Metrics dashboard
- Shot logging

### History (/history)
- Session list
- Progress charts
- Session details

### Profile (/profile)
- User info
- Stats overview
- Settings

## 📱 Responsive Design

Breakpoints:
- Mobile: < 480px
- Tablet: 480px - 768px
- Desktop: > 768px

## ♿ Accessibility

- Semantic HTML
- ARIA labels where needed
- Keyboard navigation
- High contrast colors
- Focus indicators

## 🚀 Building for Production

```bash
# Build
npm run build

# The .next folder is ready to deploy
# Size should be < 100MB

# Deploy to Vercel
npm install -g vercel
vercel
```

## 🧪 Testing

```bash
# Run all tests
npm run test

# Run specific test file
npm run test -- __tests__/api.test.ts

# Update snapshots
npm run test -- -u

# Coverage report
npm run test:coverage
```

## 🐛 Debugging

### Browser DevTools
- React DevTools extension
- Network tab for API calls
- Console for logs

### VS Code Debugging
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Next.js",
      "type": "node",
      "request": "launch",
      "program": "${workspaceFolder}/node_modules/.bin/next",
      "args": ["dev"]
    }
  ]
}
```

## 📚 Dependencies

### Core
- **next**: React framework
- **react**: UI library
- **typescript**: Type safety

### UI & Styling
- **framer-motion**: Animations
- **react-hot-toast**: Notifications
- **chart.js**: Charts & graphs

### Utilities
- **axios**: HTTP client
- **zustand**: State management (optional)
- **date-fns**: Date formatting
- **uuid**: ID generation

### Development
- **jest**: Testing framework
- **eslint**: Code linting
- **prettier**: Code formatting

## 🔒 Security

- No secrets in code
- API calls use HTTPS in production
- CSRF protection via Next.js
- Content Security Policy headers
- Input sanitization

## 🤝 Contributing

1. Create feature branch: `git checkout -b feature/amazing-feature`
2. Commit changes: `git commit -m 'Add amazing feature'`
3. Push: `git push origin feature/amazing-feature`
4. Open Pull Request

## 📖 Resources

- [Next.js Docs](https://nextjs.org/docs)
- [React Docs](https://react.dev)
- [TypeScript Handbook](https://www.typescriptlang.org/docs)
- [CSS Modules](https://github.com/css-modules/css-modules)

## 📝 License

MIT License - see LICENSE file
