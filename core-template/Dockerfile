# =====================================================
# 🐳 DOCKERFILE - PULSO-AI CORE TEMPLATE
# =====================================================
# Multi-stage build for optimized production image
# Supports: FastAPI + GraphQL + BigQuery + PostgreSQL

# =====================================================
# 📦 BUILD STAGE - Dependencies & Requirements
# =====================================================
FROM python:3.11-slim as builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies for building
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Create and set work directory
WORKDIR /app

# Copy requirements files
COPY requirements/ requirements/

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install --user -r requirements/base.txt

# =====================================================
# 🚀 RUNTIME STAGE - Production Image
# =====================================================
FROM python:3.11-slim as runtime

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    PATH=/root/.local/bin:$PATH

# Install runtime system dependencies
RUN apt-get update && apt-get install -y \
    libpq5 \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Create app user for security
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Create directories
WORKDIR /app
RUN mkdir -p /app/logs /app/config /app/secrets && \
    chown -R appuser:appuser /app

# Copy Python packages from builder stage
COPY --from=builder /root/.local /root/.local

# Copy application source code
COPY src/ src/
COPY pyproject.toml pytest.ini ./

# Create entrypoint script
RUN cat > /app/entrypoint.sh << 'EOF'
#!/bin/bash
set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Starting Pulso-AI Core Template${NC}"
echo -e "${BLUE}📋 Issue #19: Pipeline ETL básico funcional${NC}"
echo -e "${BLUE}🏢 Cliente: Telefónica del Perú${NC}"

# Check environment variables
echo -e "${YELLOW}🔍 Verificando configuración...${NC}"

if [ -z "$POSTGRES_DATABASE_URL" ]; then
    echo -e "${RED}❌ ERROR: POSTGRES_DATABASE_URL no está configurada${NC}"
    exit 1
fi

if [ -z "$BIGQUERY_PROJECT_ID" ]; then
    echo -e "${RED}❌ ERROR: BIGQUERY_PROJECT_ID no está configurada${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Variables de entorno configuradas${NC}"

# Check if secrets exist
if [ ! -f "$GOOGLE_APPLICATION_CREDENTIALS" ]; then
    echo -e "${YELLOW}⚠️  WARNING: BigQuery credentials no encontradas en $GOOGLE_APPLICATION_CREDENTIALS${NC}"
    echo -e "${YELLOW}   ETL no funcionará hasta que se proporcionen credenciales válidas${NC}"
fi

# Wait for database
echo -e "${YELLOW}⏳ Esperando PostgreSQL...${NC}"
max_attempts=30
attempt=1

while [ $attempt -le $max_attempts ]; do
    if python -c "
import psycopg2
import os
try:
    conn = psycopg2.connect(os.environ['POSTGRES_DATABASE_URL'])
    conn.close()
    print('✅ PostgreSQL conectado')
    exit(0)
except:
    exit(1)
" 2>/dev/null; then
        echo -e "${GREEN}✅ PostgreSQL disponible${NC}"
        break
    fi
    
    echo -e "${YELLOW}   Intento $attempt/$max_attempts - PostgreSQL no disponible, esperando...${NC}"
    sleep 2
    attempt=$((attempt + 1))
done

if [ $attempt -gt $max_attempts ]; then
    echo -e "${RED}❌ ERROR: No se pudo conectar a PostgreSQL después de $max_attempts intentos${NC}"
    exit 1
fi

# Run application
echo -e "${BLUE}🌐 Iniciando servidor FastAPI...${NC}"
echo -e "${BLUE}   Host: ${HOST:-0.0.0.0}:${PORT:-8000}${NC}"
echo -e "${BLUE}   Environment: ${ENVIRONMENT:-development}${NC}"

exec python -m src.api.main "$@"
EOF

# Make entrypoint executable
RUN chmod +x /app/entrypoint.sh

# Health check script
RUN cat > /app/healthcheck.py << 'EOF'
#!/usr/bin/env python3
import asyncio
import aiohttp
import sys
import os

async def health_check():
    """Check if the application is healthy."""
    try:
        host = os.getenv('HOST', '0.0.0.0')
        port = os.getenv('PORT', '8000')
        url = f"http://{host}:{port}/health"
        
        timeout = aiohttp.ClientTimeout(total=5)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(url) as response:
                if response.status == 200:
                    print("✅ Health check passed")
                    return True
                else:
                    print(f"❌ Health check failed: HTTP {response.status}")
                    return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

if __name__ == "__main__":
    result = asyncio.run(health_check())
    sys.exit(0 if result else 1)
EOF

# Make healthcheck executable
RUN chmod +x /app/healthcheck.py

# Set ownership
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python /app/healthcheck.py

# Default command
ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["--host", "0.0.0.0", "--port", "8000"]

# =====================================================
# 📝 BUILD METADATA
# =====================================================
LABEL org.opencontainers.image.title="Pulso-AI Core Template" \
      org.opencontainers.image.description="FastAPI + GraphQL backend for Telefónica ETL pipeline" \
      org.opencontainers.image.version="1.0.0" \
      org.opencontainers.image.vendor="Pulso-AI" \
      org.opencontainers.image.source="https://github.com/reyer3/Pulso-AI" \
      org.opencontainers.image.documentation="https://github.com/reyer3/Pulso-AI/blob/main/core-template/README.md"

# =====================================================
# 🚀 USAGE EXAMPLES
# =====================================================
# Build: docker build -t pulso-ai-core ./core-template
# Run:   docker run -p 8000:8000 --env-file .env pulso-ai-core
# Debug: docker run -it pulso-ai-core /bin/bash