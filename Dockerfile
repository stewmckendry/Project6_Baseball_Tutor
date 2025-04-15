# Stage 1: Builder
FROM python:3.11-slim AS builder

# Install system dependencies (minimum needed)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    git \
    libgl1 \
    libglib2.0-0 \
 && rm -rf /var/lib/apt/lists/*

# Set work directory and copy app
WORKDIR /app
COPY . /app

# Install Python dependencies into isolated folder
RUN pip install --upgrade pip \
 && pip install --prefix=/install -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim

# ✅ Install runtime dependencies (curl for health check)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
 && rm -rf /var/lib/apt/lists/*

# Copy Python dependencies from builder stage
COPY --from=builder /install /usr/local/

# Set work directory again
WORKDIR /app

# Copy application files
COPY . /app

# Expose port for Streamlit (UI)
EXPOSE 8000

# Start both FastAPI and Streamlit
CMD ["bash", "scripts/start.sh"]
