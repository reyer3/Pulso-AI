"""
📊 BIGQUERY ADAPTER - TELEFÓNICA PERÚ
====================================
Basic BigQuery adapter for Issue #19 - Pipeline ETL básico funcional

This adapter provides basic connectivity to BigQuery for Telefónica data sources.
Full ETL implementation will be completed in Issue #14.

Data Sources (Real tables identified):
- 6 Batch tables: asignacion, master_luna, master_contacto, tran_deuda, pagos, campanas
- 2 Operational tables: mibotair (CALL), voicebot (VOICEBOT)
"""

import logging
import os
from datetime import date, datetime
from typing import Dict, List, Optional, Any

import asyncio
from google.cloud import bigquery
import polars as pl

logger = logging.getLogger(__name__)

class TelefonicaBigQueryAdapter:
    """
    Basic BigQuery adapter for Telefónica del Perú data extraction.
    
    This is a minimal implementation for Issue #19 to demonstrate connectivity.
    Full dimensional ETL will be implemented in Issue #14.
    """
    
    def __init__(
        self,
        project_id: str,
        dataset: str,
        credentials_path: Optional[str] = None
    ):
        """
        Initialize BigQuery adapter.
        
        Args:
            project_id: Google Cloud project ID (mibot-222814)
            dataset: BigQuery dataset (BI_USA)
            credentials_path: Path to service account JSON file
        """
        self.project_id = project_id
        self.dataset = dataset
        self.credentials_path = credentials_path
        
        # Initialize client
        self._client = None
        self._setup_client()
    
    def _setup_client(self):
        """Setup BigQuery client with authentication."""
        try:
            if self.credentials_path and os.path.exists(self.credentials_path):
                self._client = bigquery.Client.from_service_account_json(
                    self.credentials_path,
                    project=self.project_id
                )
                logger.info(f"✅ BigQuery client initialized with service account")
            else:
                # Try default credentials (for Cloud Run, GCE, etc.)
                self._client = bigquery.Client(project=self.project_id)
                logger.info(f"✅ BigQuery client initialized with default credentials")
                
        except Exception as e:
            logger.error(f"❌ Failed to initialize BigQuery client: {e}")
            self._client = None
    
    async def test_connection(self) -> Dict[str, Any]:
        """
        Test BigQuery connection and return status.
        
        Returns:
            Dict with connection status and basic info
        """
        if not self._client:
            return {
                "connected": False,
                "error": "BigQuery client not initialized",
                "tables_available": 0
            }
        
        try:
            # Run a simple query to test connection
            query = f"""
                SELECT table_name, table_type, creation_time
                FROM `{self.project_id}.{self.dataset}.INFORMATION_SCHEMA.TABLES`
                WHERE table_name LIKE '%P3fV4dWNeMkN5RJMhV8e%'
                ORDER BY creation_time DESC
                LIMIT 10
            """
            
            query_job = self._client.query(query)
            results = list(query_job)
            
            table_names = [row.table_name for row in results]
            
            return {
                "connected": True,
                "project_id": self.project_id,
                "dataset": self.dataset,
                "tables_available": len(table_names),
                "telefonica_tables": table_names,
                "test_timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"❌ BigQuery connection test failed: {e}")
            return {
                "connected": False,
                "error": str(e),
                "tables_available": 0
            }
    
    async def get_available_tables(self) -> List[Dict[str, Any]]:
        """
        Get list of available Telefónica tables.
        
        Returns:
            List of table information dictionaries
        """
        if not self._client:
            logger.error("BigQuery client not initialized")
            return []
        
        try:
            query = f"""
                SELECT 
                    table_name,
                    table_type,
                    creation_time,
                    row_count,
                    size_bytes,
                    CASE 
                        WHEN table_name LIKE '%batch%' THEN 'BATCH'
                        WHEN table_name LIKE '%mibotair%' THEN 'CALL_OPERATIONAL'
                        WHEN table_name LIKE '%voicebot%' THEN 'VOICEBOT_OPERATIONAL'
                        ELSE 'OTHER'
                    END as table_category
                FROM `{self.project_id}.{self.dataset}.INFORMATION_SCHEMA.TABLES`
                WHERE table_name LIKE '%P3fV4dWNeMkN5RJMhV8e%'
                ORDER BY table_category, table_name
            """
            
            query_job = self._client.query(query)
            results = []
            
            for row in query_job:
                results.append({
                    "table_name": row.table_name,
                    "table_type": row.table_type,
                    "category": row.table_category,
                    "creation_time": row.creation_time.isoformat() if row.creation_time else None,
                    "row_count": row.row_count,
                    "size_bytes": row.size_bytes
                })
            
            logger.info(f"✅ Found {len(results)} Telefónica tables")
            return results
            
        except Exception as e:
            logger.error(f"❌ Failed to get available tables: {e}")
            return []
    
    async def extract_sample_data(
        self,
        table_name: str,
        limit: int = 100
    ) -> pl.DataFrame:
        """
        Extract sample data from a specific table.
        
        Args:
            table_name: Name of the table to sample
            limit: Number of rows to extract
            
        Returns:
            Polars DataFrame with sample data
        """
        if not self._client:
            logger.error("BigQuery client not initialized")
            return pl.DataFrame()
        
        try:
            query = f"""
                SELECT *
                FROM `{self.project_id}.{self.dataset}.{table_name}`
                LIMIT {limit}
            """
            
            query_job = self._client.query(query)
            
            # Convert to pandas first, then to polars
            df_pandas = query_job.to_dataframe()
            df_polars = pl.from_pandas(df_pandas)
            
            logger.info(f"✅ Extracted {len(df_polars)} rows from {table_name}")
            return df_polars
            
        except Exception as e:
            logger.error(f"❌ Failed to extract sample data from {table_name}: {e}")
            return pl.DataFrame()
    
    async def extract_gestiones_sample(
        self,
        fecha: Optional[date] = None,
        limit: int = 1000
    ) -> Dict[str, pl.DataFrame]:
        """
        Extract sample gestiones data from both CALL and VOICEBOT tables.
        
        This is a basic implementation for Issue #19 demonstration.
        Full ETL logic will be in Issue #14.
        
        Args:
            fecha: Date to extract (defaults to today)
            limit: Max rows per table
            
        Returns:
            Dict with 'call' and 'voicebot' DataFrames
        """
        if not self._client:
            logger.error("BigQuery client not initialized")
            return {"call": pl.DataFrame(), "voicebot": pl.DataFrame()}
        
        if fecha is None:
            fecha = date.today()
        
        results = {}
        
        # Extract CALL gestiones (mibotair)
        try:
            call_query = f"""
                SELECT 
                    fecha_gestion,
                    hora_gestion,
                    ejecutivo,
                    'CALL' as canal,
                    contactabilidad,
                    es_pdp,
                    cod_luna,
                    cliente,
                    telefono
                FROM `{self.project_id}.{self.dataset}.mibotair_P3fV4dWNeMkN5RJMhV8e`
                WHERE DATE(_PARTITIONTIME) >= DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY)
                ORDER BY fecha_gestion DESC, hora_gestion DESC
                LIMIT {limit}
            """
            
            call_job = self._client.query(call_query)
            call_df = pl.from_pandas(call_job.to_dataframe())
            results["call"] = call_df
            
            logger.info(f"✅ Extracted {len(call_df)} CALL gestiones")
            
        except Exception as e:
            logger.warning(f"⚠️  Failed to extract CALL gestiones: {e}")
            results["call"] = pl.DataFrame()
        
        # Extract VOICEBOT gestiones
        try:
            voicebot_query = f"""
                SELECT 
                    fecha_gestion,
                    hora_gestion,
                    'VOICEBOT' as ejecutivo,
                    'VOICEBOT' as canal,
                    contactabilidad,
                    es_pdp,
                    cod_luna,
                    cliente,
                    telefono
                FROM `{self.project_id}.{self.dataset}.voicebot_P3fV4dWNeMkN5RJMhV8e`
                WHERE DATE(_PARTITIONTIME) >= DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY)
                ORDER BY fecha_gestion DESC, hora_gestion DESC
                LIMIT {limit}
            """
            
            voicebot_job = self._client.query(voicebot_query)
            voicebot_df = pl.from_pandas(voicebot_job.to_dataframe())
            results["voicebot"] = voicebot_df
            
            logger.info(f"✅ Extracted {len(voicebot_df)} VOICEBOT gestiones")
            
        except Exception as e:
            logger.warning(f"⚠️  Failed to extract VOICEBOT gestiones: {e}")
            results["voicebot"] = pl.DataFrame()
        
        return results
    
    async def get_data_summary(self) -> Dict[str, Any]:
        """
        Get summary of available data for Telefónica.
        
        Returns:
            Summary statistics of available data
        """
        if not self._client:
            return {"error": "BigQuery client not initialized"}
        
        try:
            summary_query = f"""
                WITH table_stats AS (
                    SELECT 
                        table_name,
                        row_count,
                        size_bytes,
                        CASE 
                            WHEN table_name LIKE '%batch%' THEN 'BATCH'
                            WHEN table_name LIKE '%mibotair%' THEN 'CALL'
                            WHEN table_name LIKE '%voicebot%' THEN 'VOICEBOT'
                            ELSE 'OTHER'
                        END as category
                    FROM `{self.project_id}.{self.dataset}.INFORMATION_SCHEMA.TABLES`
                    WHERE table_name LIKE '%P3fV4dWNeMkN5RJMhV8e%'
                )
                SELECT 
                    category,
                    COUNT(*) as table_count,
                    SUM(row_count) as total_rows,
                    SUM(size_bytes) as total_bytes
                FROM table_stats
                GROUP BY category
                ORDER BY total_rows DESC
            """
            
            query_job = self._client.query(summary_query)
            results = {}
            
            for row in query_job:
                results[row.category] = {
                    "table_count": row.table_count,
                    "total_rows": row.total_rows,
                    "total_bytes": row.total_bytes,
                    "size_mb": round(row.total_bytes / 1024 / 1024, 2) if row.total_bytes else 0
                }
            
            return {
                "timestamp": datetime.now().isoformat(),
                "project_id": self.project_id,
                "dataset": self.dataset,
                "categories": results
            }
            
        except Exception as e:
            logger.error(f"❌ Failed to get data summary: {e}")
            return {"error": str(e)}

# =====================================================
# 🏭 FACTORY FUNCTION
# =====================================================

def create_telefonica_bigquery_adapter() -> TelefonicaBigQueryAdapter:
    """
    Factory function to create BigQuery adapter from environment variables.
    
    Returns:
        Configured TelefonicaBigQueryAdapter instance
    """
    project_id = os.getenv("BIGQUERY_PROJECT_ID", "mibot-222814")
    dataset = os.getenv("BIGQUERY_DATASET", "BI_USA")
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    
    return TelefonicaBigQueryAdapter(
        project_id=project_id,
        dataset=dataset,
        credentials_path=credentials_path
    )

# =====================================================
# 🧪 TESTING UTILITIES
# =====================================================

async def test_bigquery_connection():
    """Test BigQuery connection and log results."""
    logger.info("🔍 Testing BigQuery connection...")
    
    adapter = create_telefonica_bigquery_adapter()
    
    # Test connection
    connection_result = await adapter.test_connection()
    logger.info(f"Connection result: {connection_result}")
    
    if connection_result["connected"]:
        # Get available tables
        tables = await adapter.get_available_tables()
        logger.info(f"Found {len(tables)} tables")
        
        # Get data summary
        summary = await adapter.get_data_summary()
        logger.info(f"Data summary: {summary}")
    
    return connection_result

if __name__ == "__main__":
    # Quick test
    asyncio.run(test_bigquery_connection())