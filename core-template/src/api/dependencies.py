"""
Dependency injection for FastAPI application.

Manages creation and lifecycle of use cases and adapters.
"""

import os
from functools import lru_cache
from typing import Optional

from pydantic import BaseSettings

from src.application.use_cases.etl.process_daily_etl import create_daily_etl_use_case
from src.application.use_cases.dashboard.generate_dashboard_data import create_dashboard_use_case


class Settings(BaseSettings):
    """Application settings from environment variables."""
    
    # PostgreSQL settings
    postgres_database_url: str = "postgresql://pulso_ai:dev_password@localhost:5432/telefonica_datamart"
    postgres_schema: str = "telefonica"
    
    # BigQuery settings
    bigquery_project_id: str = "mibot-222814"
    bigquery_dataset: str = "BI_USA"
    bigquery_credentials_path: Optional[str] = None
    
    # Application settings
    environment: str = "development"
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    """Get cached application settings."""
    return Settings()


# Use case factories with dependency injection
async def get_etl_use_case():
    """Get configured ETL use case."""
    settings = get_settings()
    
    return await create_daily_etl_use_case(
        bigquery_project_id=settings.bigquery_project_id,
        bigquery_dataset=settings.bigquery_dataset,
        bigquery_credentials_path=settings.bigquery_credentials_path,
        postgres_database_url=settings.postgres_database_url,
        postgres_schema=settings.postgres_schema
    )


async def get_dashboard_use_case():
    """Get configured dashboard use case."""
    settings = get_settings()
    
    return await create_dashboard_use_case(
        postgres_database_url=settings.postgres_database_url,
        postgres_schema=settings.postgres_schema
    )
