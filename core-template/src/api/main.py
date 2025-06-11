"""
Main FastAPI Application for Pulso-AI Telefónica.

Provides:
- GraphQL API for dashboard data
- REST endpoints for ETL management
- Health checks and monitoring
"""

import asyncio
import logging
from datetime import date, datetime, timedelta
from typing import Dict, Any, Optional
import os

from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends
from fastapi.middleware.cors import CORSMiddleware
from strawberry.fastapi import GraphQLRouter
import uvicorn

from src.api.graphql.schema import schema
from src.api.dependencies import (
    get_etl_use_case,
    get_dashboard_use_case,
    get_settings
)
from src.application.use_cases.etl.process_daily_etl import ProcessDailyETLUseCase
from src.application.use_cases.dashboard.generate_dashboard_data import GenerateDashboardDataUseCase

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Pulso-AI Telefónica API",
    description="Dashboard and ETL API for Telefónica del Perú",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add GraphQL router
graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")


@app.on_event("startup")
async def startup_event():
    """Initialize application on startup."""
    logger.info("🚀 Starting Pulso-AI Telefónica API")
    
    # Test connections on startup
    try:
        settings = get_settings()
        logger.info(f"Database URL: {settings.postgres_database_url[:50]}...")
        logger.info(f"BigQuery Project: {settings.bigquery_project_id}")
        logger.info("✅ Application started successfully")
    except Exception as e:
        logger.error(f"❌ Startup error: {e}")
        raise


@app.on_event("shutdown") 
async def shutdown_event():
    """Cleanup resources on shutdown."""
    logger.info("🛑 Shutting down Pulso-AI Telefónica API")


# Health check endpoints
@app.get("/health")
async def health_check():
    """Basic health check."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "pulso-ai-telefonica"
    }


@app.get("/health/detailed")
async def detailed_health_check(
    etl_use_case: ProcessDailyETLUseCase = Depends(get_etl_use_case),
    dashboard_use_case: GenerateDashboardDataUseCase = Depends(get_dashboard_use_case)
):
    """Detailed health check with dependency tests."""
    
    health_status = {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "checks": {}
    }
    
    try:
        # Test BigQuery connection
        bigquery_ok = await etl_use_case.bigquery.test_connection()
        health_status["checks"]["bigquery"] = "healthy" if bigquery_ok else "unhealthy"
        
        # Test PostgreSQL connection
        postgres_ok = await etl_use_case.datamart.test_connection()
        health_status["checks"]["postgresql"] = "healthy" if postgres_ok else "unhealthy"
        
        # Overall status
        if not (bigquery_ok and postgres_ok):
            health_status["status"] = "degraded"
            
    except Exception as e:
        health_status["status"] = "unhealthy"
        health_status["error"] = str(e)
    
    return health_status


# ETL Management endpoints
@app.post("/etl/run/{fecha_proceso}")
async def run_etl(
    fecha_proceso: date,
    background_tasks: BackgroundTasks,
    etl_use_case: ProcessDailyETLUseCase = Depends(get_etl_use_case)
):
    """Trigger ETL processing for specific date."""
    
    logger.info(f"ETL requested for {fecha_proceso}")
    
    # Run ETL in background
    background_tasks.add_task(
        _run_etl_background,
        etl_use_case,
        fecha_proceso
    )
    
    return {
        "message": f"ETL processing started for {fecha_proceso}",
        "fecha_proceso": fecha_proceso,
        "status": "started",
        "timestamp": datetime.now().isoformat()
    }


@app.get("/etl/status/{fecha_proceso}")
async def get_etl_status(
    fecha_proceso: date,
    etl_use_case: ProcessDailyETLUseCase = Depends(get_etl_use_case)
):
    """Get ETL processing status for specific date."""
    
    try:
        status = await etl_use_case.get_processing_status(fecha_proceso)
        return status
    except Exception as e:
        logger.error(f"Error getting ETL status: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/etl/run-range")
async def run_etl_date_range(
    request: Dict[str, str],  # {"fecha_inicio": "2024-01-01", "fecha_fin": "2024-01-31"}
    background_tasks: BackgroundTasks,
    etl_use_case: ProcessDailyETLUseCase = Depends(get_etl_use_case)
):
    """Run ETL for date range."""
    
    try:
        fecha_inicio = date.fromisoformat(request["fecha_inicio"])
        fecha_fin = date.fromisoformat(request["fecha_fin"])
        
        if (fecha_fin - fecha_inicio).days > 31:
            raise HTTPException(
                status_code=400, 
                detail="Date range cannot exceed 31 days"
            )
        
        # Schedule background processing
        background_tasks.add_task(
            _run_etl_range_background,
            etl_use_case,
            fecha_inicio,
            fecha_fin
        )
        
        return {
            "message": f"ETL processing started for range {fecha_inicio} to {fecha_fin}",
            "fecha_inicio": fecha_inicio,
            "fecha_fin": fecha_fin,
            "status": "started",
            "estimated_duration_minutes": (fecha_fin - fecha_inicio).days * 2
        }
        
    except KeyError as e:
        raise HTTPException(status_code=400, detail=f"Missing field: {e}")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid date format: {e}")


# Dashboard data endpoints (REST)
@app.get("/dashboard/summary")
async def get_dashboard_summary(
    fecha_inicio: Optional[str] = None,
    fecha_fin: Optional[str] = None,
    dashboard_use_case: GenerateDashboardDataUseCase = Depends(get_dashboard_use_case)
):
    """Get dashboard summary data (REST endpoint)."""
    
    # Default to last 30 days
    if not fecha_inicio or not fecha_fin:
        fecha_fin_date = date.today()
        fecha_inicio_date = fecha_fin_date - timedelta(days=30)
    else:
        try:
            fecha_inicio_date = date.fromisoformat(fecha_inicio)
            fecha_fin_date = date.fromisoformat(fecha_fin)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=f"Invalid date format: {e}")
    
    try:
        summary = await dashboard_use_case.get_dashboard_summary(
            fecha_inicio_date, fecha_fin_date
        )
        return summary
    except Exception as e:
        logger.error(f"Error getting dashboard summary: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/dashboard/complete")
async def get_complete_dashboard(
    fecha_inicio: Optional[str] = None,
    fecha_fin: Optional[str] = None,
    dashboard_use_case: GenerateDashboardDataUseCase = Depends(get_dashboard_use_case)
):
    """Get complete dashboard data (REST endpoint)."""
    
    # Default to last 7 days
    if not fecha_inicio or not fecha_fin:
        fecha_fin_date = date.today()
        fecha_inicio_date = fecha_fin_date - timedelta(days=7)
    else:
        try:
            fecha_inicio_date = date.fromisoformat(fecha_inicio)
            fecha_fin_date = date.fromisoformat(fecha_fin)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=f"Invalid date format: {e}")
    
    try:
        dashboard_data = await dashboard_use_case.get_complete_dashboard(
            fecha_inicio_date, fecha_fin_date
        )
        return dashboard_data
    except Exception as e:
        logger.error(f"Error getting complete dashboard: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Background task functions
async def _run_etl_background(
    etl_use_case: ProcessDailyETLUseCase,
    fecha_proceso: date
):
    """Run ETL in background task."""
    try:
        logger.info(f"Background ETL started for {fecha_proceso}")
        result = await etl_use_case.execute(fecha_proceso)
        
        if result["status"] == "success":
            logger.info(f"✅ Background ETL completed for {fecha_proceso}")
        else:
            logger.error(f"❌ Background ETL failed for {fecha_proceso}: {result.get('error')}")
            
    except Exception as e:
        logger.error(f"Background ETL exception for {fecha_proceso}: {e}")
    finally:
        # Cleanup resources
        await etl_use_case.cleanup_resources()


async def _run_etl_range_background(
    etl_use_case: ProcessDailyETLUseCase,
    fecha_inicio: date,
    fecha_fin: date
):
    """Run ETL for date range in background."""
    try:
        logger.info(f"Background ETL range started: {fecha_inicio} to {fecha_fin}")
        
        current_date = fecha_inicio
        while current_date <= fecha_fin:
            logger.info(f"Processing {current_date}")
            
            result = await etl_use_case.execute(current_date)
            
            if result["status"] != "success":
                logger.error(f"ETL failed for {current_date}: {result.get('error')}")
                # Continue with next date
            
            current_date += timedelta(days=1)
        
        logger.info(f"✅ Background ETL range completed: {fecha_inicio} to {fecha_fin}")
        
    except Exception as e:
        logger.error(f"Background ETL range exception: {e}")
    finally:
        # Cleanup resources
        await etl_use_case.cleanup_resources()


# Development server
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    
    logger.info(f"Starting development server on {host}:{port}")
    
    uvicorn.run(
        "src.api.main:app",
        host=host,
        port=port,
        reload=True,
        log_level="info"
    )
