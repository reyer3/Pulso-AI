"""
🚀 PULSO-AI CORE TEMPLATE - MAIN APPLICATION
=============================================
FastAPI + GraphQL application for Telefónica ETL Pipeline
Issue #19: Pipeline ETL básico funcional

This module provides:
- FastAPI application with health checks
- GraphQL endpoint using Strawberry
- ETL trigger endpoints
- CORS configuration for frontend
- Error handling and logging
"""

import asyncio
import logging
import os
import sys
from contextlib import asynccontextmanager
from datetime import date, datetime
from typing import Any, Dict, Optional

import uvicorn
from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from strawberry.fastapi import GraphQLRouter
import strawberry

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("/app/logs/app.log") if os.path.exists("/app/logs") else logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# =====================================================
# 🏗️ APPLICATION LIFECYCLE
# =====================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan context manager."""
    logger.info("🚀 Starting Pulso-AI Core Template")
    logger.info("📋 Issue #19: Pipeline ETL básico funcional")
    logger.info("🏢 Cliente: Telefónica del Perú")
    
    # Startup
    await startup_event()
    
    yield
    
    # Shutdown
    await shutdown_event()
    logger.info("👋 Pulso-AI Core Template shutdown complete")

async def startup_event():
    """Initialize application on startup."""
    try:
        # Verify environment variables
        required_env = [
            "POSTGRES_DATABASE_URL",
            "BIGQUERY_PROJECT_ID",
            "BIGQUERY_DATASET"
        ]
        
        missing_env = [var for var in required_env if not os.getenv(var)]
        if missing_env:
            logger.error(f"❌ Missing environment variables: {missing_env}")
            raise RuntimeError(f"Missing required environment variables: {missing_env}")
        
        # Test database connection
        await test_database_connection()
        
        logger.info("✅ Application startup complete")
        
    except Exception as e:
        logger.error(f"❌ Startup failed: {e}")
        raise

async def test_database_connection():
    """Test PostgreSQL database connection."""
    try:
        import asyncpg
        
        database_url = os.getenv("POSTGRES_DATABASE_URL")
        conn = await asyncpg.connect(database_url)
        
        # Test query
        result = await conn.fetchval("SELECT version()")
        logger.info(f"✅ PostgreSQL connected: {result[:50]}...")
        
        await conn.close()
        
    except Exception as e:
        logger.error(f"❌ Database connection failed: {e}")
        raise

async def shutdown_event():
    """Cleanup on application shutdown."""
    logger.info("🛑 Starting application shutdown...")
    # Add cleanup tasks here
    await asyncio.sleep(0.1)  # Give time for final log messages

# =====================================================
# 🌐 FASTAPI APPLICATION
# =====================================================

app = FastAPI(
    title="Pulso-AI Core Template",
    description="FastAPI + GraphQL backend for Telefónica ETL Pipeline",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# =====================================================
# 🔧 MIDDLEWARE CONFIGURATION
# =====================================================

# CORS configuration for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Frontend
        "http://localhost:5173",  # Vite dev
        "http://frontend:80",     # Docker frontend
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# =====================================================
# 📊 BASIC GRAPHQL SCHEMA (MINIMAL FOR ISSUE #19)
# =====================================================

@strawberry.type
class HealthStatus:
    """Health status type."""
    status: str
    timestamp: datetime
    database_connected: bool
    etl_configured: bool

@strawberry.type
class SystemInfo:
    """System information type."""
    version: str
    environment: str
    client: str
    uptime: str

@strawberry.type
class Query:
    """GraphQL query root."""
    
    @strawberry.field
    async def health(self) -> HealthStatus:
        """Get system health status."""
        try:
            # Test database connection
            import asyncpg
            database_url = os.getenv("POSTGRES_DATABASE_URL")
            conn = await asyncpg.connect(database_url)
            await conn.fetchval("SELECT 1")
            await conn.close()
            db_connected = True
        except:
            db_connected = False
        
        return HealthStatus(
            status="healthy" if db_connected else "degraded",
            timestamp=datetime.now(),
            database_connected=db_connected,
            etl_configured=bool(os.getenv("BIGQUERY_PROJECT_ID"))
        )
    
    @strawberry.field
    async def system_info(self) -> SystemInfo:
        """Get system information."""
        import time
        
        return SystemInfo(
            version="1.0.0",
            environment=os.getenv("ENVIRONMENT", "development"),
            client="Telefónica del Perú",
            uptime=f"{time.time():.0f} seconds"
        )

@strawberry.type
class Mutation:
    """GraphQL mutation root."""
    
    @strawberry.field
    async def trigger_etl(self, fecha: Optional[str] = None) -> str:
        """Trigger ETL process for specific date."""
        # This is a placeholder for Issue #19
        # Full ETL implementation will be added in Issue #14
        target_date = fecha or str(date.today())
        logger.info(f"🔄 ETL trigger requested for date: {target_date}")
        
        return f"ETL process queued for {target_date}. Full implementation pending Issue #14."

# Create GraphQL schema
schema = strawberry.Schema(
    query=Query,
    mutation=Mutation
)

# Add GraphQL endpoint
graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")

# =====================================================
# 🛡️ HEALTH CHECK ENDPOINTS
# =====================================================

@app.get("/health")
async def health_check():
    """Basic health check endpoint."""
    try:
        # Test database connection
        import asyncpg
        database_url = os.getenv("POSTGRES_DATABASE_URL")
        conn = await asyncpg.connect(database_url)
        await conn.fetchval("SELECT 1")
        await conn.close()
        
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "service": "pulso-ai-core",
            "version": "1.0.0",
            "client": "telefonica-peru",
            "database": "connected",
            "environment": os.getenv("ENVIRONMENT", "development")
        }
    
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "timestamp": datetime.now().isoformat(),
                "error": str(e),
                "service": "pulso-ai-core"
            }
        )

@app.get("/health/detailed")
async def detailed_health_check():
    """Detailed health check with component status."""
    health_data = {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "components": {}
    }
    
    overall_healthy = True
    
    # Check database
    try:
        import asyncpg
        database_url = os.getenv("POSTGRES_DATABASE_URL")
        conn = await asyncpg.connect(database_url)
        await conn.fetchval("SELECT 1")
        await conn.close()
        
        health_data["components"]["database"] = {
            "status": "healthy",
            "type": "postgresql",
            "response_time_ms": 10
        }
    except Exception as e:
        overall_healthy = False
        health_data["components"]["database"] = {
            "status": "unhealthy",
            "error": str(e),
            "type": "postgresql"
        }
    
    # Check BigQuery configuration
    try:
        project_id = os.getenv("BIGQUERY_PROJECT_ID")
        dataset = os.getenv("BIGQUERY_DATASET")
        credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        
        if project_id and dataset:
            health_data["components"]["bigquery"] = {
                "status": "configured",
                "project_id": project_id,
                "dataset": dataset,
                "credentials_configured": bool(credentials_path and os.path.exists(credentials_path))
            }
        else:
            health_data["components"]["bigquery"] = {
                "status": "not_configured",
                "message": "BigQuery environment variables missing"
            }
    except Exception as e:
        health_data["components"]["bigquery"] = {
            "status": "error",
            "error": str(e)
        }
    
    health_data["status"] = "healthy" if overall_healthy else "degraded"
    
    return health_data

# =====================================================
# 🔄 ETL ENDPOINTS (BASIC FOR ISSUE #19)
# =====================================================

@app.post("/etl/trigger")
async def trigger_etl_endpoint(
    background_tasks: BackgroundTasks,
    fecha: Optional[str] = None
):
    """Trigger ETL process via REST endpoint."""
    target_date = fecha or str(date.today())
    
    logger.info(f"🔄 ETL trigger via REST API for date: {target_date}")
    
    # Add background task (placeholder)
    background_tasks.add_task(simulate_etl_process, target_date)
    
    return {
        "message": f"ETL process started for {target_date}",
        "status": "processing",
        "timestamp": datetime.now().isoformat(),
        "note": "This is a basic implementation for Issue #19. Full ETL will be in Issue #14."
    }

async def simulate_etl_process(fecha: str):
    """Simulate ETL process for demonstration."""
    logger.info(f"📊 Starting simulated ETL for {fecha}")
    await asyncio.sleep(2)  # Simulate processing time
    logger.info(f"✅ Simulated ETL completed for {fecha}")

# =====================================================
# 📈 METRICS ENDPOINTS
# =====================================================

@app.get("/metrics")
async def get_basic_metrics():
    """Get basic application metrics."""
    return {
        "timestamp": datetime.now().isoformat(),
        "client": "telefonica-peru",
        "environment": os.getenv("ENVIRONMENT", "development"),
        "uptime": "running",
        "status": "operational",
        "issue": "#19 - Pipeline ETL básico funcional"
    }

# =====================================================
# 🚀 APPLICATION RUNNER
# =====================================================

def create_app() -> FastAPI:
    """Factory function to create FastAPI app."""
    return app

if __name__ == "__main__":
    # Configuration from environment
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    log_level = os.getenv("LOG_LEVEL", "info").lower()
    reload = os.getenv("ENVIRONMENT", "development") == "development"
    
    logger.info(f"🚀 Starting server at {host}:{port}")
    logger.info(f"📝 Log level: {log_level}")
    logger.info(f"🔄 Reload: {reload}")
    
    # Run the application
    uvicorn.run(
        "src.api.main:app",
        host=host,
        port=port,
        log_level=log_level,
        reload=reload,
        access_log=True
    )