# ============================================================================
# Build stage
# ============================================================================
FROM python:3.11-slim AS builder

WORKDIR /app

# Install system dependencies for MediaPipe and OpenCV
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libopencv-dev \
    python3-opencv \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --user -r requirements.txt

# ============================================================================
# Production stage
# ============================================================================
FROM python:3.11-slim

WORKDIR /app

# Install runtime dependencies only
RUN apt-get update && apt-get install -y --no-install-recommends \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy Python dependencies from builder
COPY --from=builder /root/.local /root/.local
COPY --from=builder /app/requirements.txt .

# Copy application code
COPY main.py .
COPY pose_detector.py .
COPY swing_analyzer.py .

# Create uploads directory
RUN mkdir -p uploads/videos

# Set PATH for pip packages
ENV PATH=/root/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1

# Create non-root user
RUN useradd -m -u 1001 aiworker
RUN chown -R aiworker:aiworker /app

USER aiworker

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
  CMD python -c "import requests; requests.get('http://localhost:8000/health')" || exit 1

# Start the application
CMD ["python", "main.py"]
