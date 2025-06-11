"""
Process Daily ETL Use Case for Telefónica del Perú.

Orchestrates the complete daily ETL pipeline:
1. Extract data from BigQuery
2. Transform and validate data 
3. Load to PostgreSQL datamart
4. Refresh aggregated metrics
"""

import asyncio
from datetime import date, datetime
from typing import Dict, Any, Optional
import logging

from src.infrastructure.adapters.bigquery.telefonica_adapter import TelefonicaBigQueryAdapter
from src.infrastructure.adapters.postgresql.datamart_adapter import TelefonicaDatamartAdapter

logger = logging.getLogger(__name__)


class ProcessDailyETLUseCase:
    """
    Main ETL orchestrator for Telefónica daily data processing.
    
    Implements the complete pipeline following Issue #19 requirements:
    - Extract from 8 BigQuery tables
    - Load to PostgreSQL datamart
    - Generate dashboard-ready aggregations
    """
    
    def __init__(
        self,
        bigquery_adapter: TelefonicaBigQueryAdapter,
        datamart_adapter: TelefonicaDatamartAdapter
    ):
        self.bigquery = bigquery_adapter
        self.datamart = datamart_adapter
        
        logger.info("Initialized ProcessDailyETLUseCase")
    
    async def execute(self, fecha_proceso: date) -> Dict[str, Any]:
        """
        Execute complete daily ETL pipeline.
        
        Args:
            fecha_proceso: Date to process
            
        Returns:
            Dict with execution results and metrics
        """
        start_time = datetime.now()
        
        logger.info(f"🚀 Starting daily ETL for {fecha_proceso}")
        
        try:
            # Step 1: Test connections
            await self._test_connections()
            
            # Step 2: Ensure datamart schema exists
            await self.datamart.ensure_schema_exists()
            
            # Step 3: Extract data from BigQuery
            extraction_result = await self._extract_data(fecha_proceso)
            
            # Step 4: Load data to datamart
            loading_result = await self._load_data(
                extraction_result['clientes'],
                extraction_result['gestiones']
            )
            
            # Step 5: Refresh aggregated metrics
            await self._refresh_metrics(fecha_proceso)
            
            # Step 6: Generate execution summary
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            result = {
                "status": "success",
                "fecha_proceso": fecha_proceso,
                "execution_time_seconds": duration,
                "extraction": extraction_result['metadata'],
                "loading": loading_result,
                "summary": {
                    "total_clientes": len(extraction_result['clientes']),
                    "total_gestiones": len(extraction_result['gestiones']),
                    "clientes_loaded": loading_result['clientes_loaded'],
                    "gestiones_loaded": loading_result['gestiones_loaded']
                }
            }
            
            logger.info(
                f"✅ ETL completed successfully in {duration:.1f}s. "
                f"Processed {result['summary']['total_gestiones']} gestiones, "
                f"{result['summary']['total_clientes']} clientes"
            )
            
            return result
            
        except Exception as e:
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            logger.error(f"❌ ETL failed after {duration:.1f}s: {e}")
            
            return {
                "status": "error",
                "fecha_proceso": fecha_proceso,
                "execution_time_seconds": duration,
                "error": str(e),
                "error_type": type(e).__name__
            }
    
    async def _test_connections(self) -> None:
        """Test all required connections."""
        logger.info("Testing connections...")
        
        # Test BigQuery connection
        bigquery_ok = await self.bigquery.test_connection()
        if not bigquery_ok:
            raise ConnectionError("BigQuery connection failed")
        
        # Test PostgreSQL connection
        postgres_ok = await self.datamart.test_connection()
        if not postgres_ok:
            raise ConnectionError("PostgreSQL connection failed")
        
        logger.info("✅ All connections tested successfully")
    
    async def _extract_data(self, fecha_proceso: date) -> Dict[str, Any]:
        """Extract data from BigQuery."""
        logger.info(f"📥 Extracting data from BigQuery for {fecha_proceso}")
        
        # Extract data using BigQuery adapter
        extraction_result = await self.bigquery.extract_daily_data(fecha_proceso)
        
        clientes = extraction_result['clientes']
        gestiones = extraction_result['gestiones']
        
        # Validate extraction
        if not clientes:
            logger.warning(f"No clientes found for {fecha_proceso}")
        
        if not gestiones:
            logger.warning(f"No gestiones found for {fecha_proceso}")
        
        logger.info(
            f"📥 Extracted {len(gestiones)} gestiones, {len(clientes)} clientes"
        )
        
        return extraction_result
    
    async def _load_data(self, clientes, gestiones) -> Dict[str, Any]:
        """Load data to PostgreSQL datamart."""
        logger.info("📤 Loading data to PostgreSQL datamart")
        
        # Load clientes first (needed for gestiones foreign keys)
        clientes_loaded = 0
        if clientes:
            clientes_loaded = await self.datamart.load_clientes(clientes)
        
        # Load gestiones with denormalized client data
        gestiones_loaded = 0
        if gestiones:
            gestiones_loaded = await self.datamart.load_gestiones(gestiones)
        
        result = {
            "clientes_loaded": clientes_loaded,
            "gestiones_loaded": gestiones_loaded
        }
        
        logger.info(
            f"📤 Loaded {clientes_loaded} clientes, {gestiones_loaded} gestiones"
        )
        
        return result
    
    async def _refresh_metrics(self, fecha_proceso: date) -> None:
        """Refresh aggregated metrics for dashboard performance."""
        logger.info(f"🔄 Refreshing daily metrics for {fecha_proceso}")
        
        await self.datamart.refresh_daily_metrics(fecha_proceso)
        
        logger.info("🔄 Daily metrics refreshed successfully")
    
    async def get_processing_status(self, fecha_proceso: date) -> Dict[str, Any]:
        """Get processing status for a specific date."""
        try:
            dashboard_data = await self.datamart.get_dashboard_data(
                fecha_proceso, fecha_proceso
            )
            
            if dashboard_data['summary'].get('total_gestiones', 0) > 0:
                return {
                    "status": "completed",
                    "fecha_proceso": fecha_proceso,
                    "data_available": True,
                    "summary": dashboard_data['summary']
                }
            else:
                return {
                    "status": "no_data",
                    "fecha_proceso": fecha_proceso,
                    "data_available": False
                }
                
        except Exception as e:
            return {
                "status": "error",
                "fecha_proceso": fecha_proceso,
                "error": str(e)
            }
    
    async def cleanup_resources(self) -> None:
        """Cleanup resources (connection pools, etc.)."""
        try:
            await self.datamart.close_pool()
            logger.info("🧹 Resources cleaned up successfully")
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")


# Factory function for easy dependency injection
async def create_daily_etl_use_case(
    bigquery_project_id: str = "mibot-222814",
    bigquery_dataset: str = "BI_USA",
    bigquery_credentials_path: Optional[str] = None,
    postgres_database_url: str = None,
    postgres_schema: str = "telefonica"
) -> ProcessDailyETLUseCase:
    """
    Factory function to create configured ETL use case.
    
    Args:
        bigquery_project_id: BigQuery project ID
        bigquery_dataset: BigQuery dataset name
        bigquery_credentials_path: Path to BigQuery credentials JSON
        postgres_database_url: PostgreSQL connection URL
        postgres_schema: PostgreSQL schema name
        
    Returns:
        Configured ProcessDailyETLUseCase instance
    """
    
    # Create adapters
    bigquery_adapter = TelefonicaBigQueryAdapter(
        project_id=bigquery_project_id,
        dataset=bigquery_dataset,
        credentials_path=bigquery_credentials_path
    )
    
    datamart_adapter = TelefonicaDatamartAdapter(
        database_url=postgres_database_url,
        schema=postgres_schema
    )
    
    # Create and return use case
    use_case = ProcessDailyETLUseCase(
        bigquery_adapter=bigquery_adapter,
        datamart_adapter=datamart_adapter
    )
    
    logger.info("✅ Daily ETL use case created successfully")
    
    return use_case
