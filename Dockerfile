# Multi-stage Docker build for Casa Vazquez FastAPI backend

# Stage 1: Build frontend
FROM node:20-alpine AS frontend-builder

WORKDIR /app/website

# Copy website package files
COPY website/package*.json ./

# Install dependencies
RUN npm ci

# Copy website source
COPY website/ ./

# Build the frontend
RUN npm run build

# Stage 2: Python backend
FROM python:3.11-slim AS backend

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy backend requirements
COPY backend/requirements.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend source
COPY backend/ ./

# Copy existing data for migration
COPY data/ ../data/

# Copy built frontend from previous stage
COPY --from=frontend-builder /app/website/dist/ ../website/dist/

# Export TypeScript data to JSON and migrate
RUN python export_ts_data.py && python init_db.py && python migrate_data.py

# Set environment variable to indicate Cloud Run
ENV CLOUD_RUN=true

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8080/health')" || exit 1

# Run the application
CMD ["python", "run.py"]