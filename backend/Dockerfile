FROM python:3.11-slim

WORKDIR /app

# Copy backend requirements
COPY backend/requirements.txt ./requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/ ./

# Copy existing data for migration
COPY data/ ../data/

# Initialize database and migrate data
RUN python init_db.py && python migrate_data.py

# Copy built frontend
COPY website/dist/ ../website/dist/

# Expose port
EXPOSE 8080

# Run the application
CMD ["python", "run.py"]