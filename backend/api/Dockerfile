# ============================================================================
# Build stage
# ============================================================================
FROM node:18-alpine AS builder

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci

# ============================================================================
# Production stage
# ============================================================================
FROM node:18-alpine

WORKDIR /app

# Set environment
ENV NODE_ENV=production
ENV NODE_OPTIONS=--max-old-space-size=512

# Copy from builder
COPY --from=builder /app/node_modules ./node_modules
COPY . .

# Create non-root user
RUN addgroup -g 1001 -S nodejs
RUN adduser -S nodejs -u 1001
USER nodejs

# Create uploads directory
RUN mkdir -p uploads/videos

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD node -e "fetch('http://localhost:5000/health').catch(() => process.exit(1))"

# Start the server
CMD ["node", "server.js"]
