"""
🗄️ POSTGRESQL ADAPTER - TELEFÓNICA DATAMART
===========================================
Basic PostgreSQL adapter for Issue #19 - Pipeline ETL básico funcional

This adapter provides connectivity to the Telefónica dimensional datamart.
Supports both read and write operations for the dimensional model.

Schema: telefonica
- Dimensions: tiempo, cliente, ejecutivo, canal, cartera, servicio
- Facts: gestiones, gestiones_agregadas
"""

import logging
import os
from datetime import date, datetime
from typing import Dict, List, Optional, Any, Tuple

import asyncio
import asyncpg
import polars as pl

logger = logging.getLogger(__name__)

class TelefonicaPostgreSQLAdapter:
    """
    Basic PostgreSQL adapter for Telefónica dimensional datamart.
    
    This is a minimal implementation for Issue #19 to demonstrate connectivity
    and basic CRUD operations. Full ETL loading will be in Issue #14.
    """
    
    def __init__(self, database_url: str, schema: str = "telefonica"):
        """
        Initialize PostgreSQL adapter.
        
        Args:
            database_url: PostgreSQL connection URL
            schema: Database schema name (default: telefonica)
        """
        self.database_url = database_url
        self.schema = schema
        self._pool = None
    
    async def initialize_pool(self, min_size: int = 5, max_size: int = 20):
        """
        Initialize connection pool.
        
        Args:
            min_size: Minimum pool size
            max_size: Maximum pool size
        """
        try:
            self._pool = await asyncpg.create_pool(
                self.database_url,
                min_size=min_size,
                max_size=max_size,
                command_timeout=30
            )
            logger.info(f"✅ PostgreSQL connection pool initialized (min={min_size}, max={max_size})")
        except Exception as e:
            logger.error(f"❌ Failed to initialize PostgreSQL pool: {e}")
            raise
    
    async def close_pool(self):
        """Close connection pool."""
        if self._pool:
            await self._pool.close()
            logger.info("📪 PostgreSQL connection pool closed")
    
    async def test_connection(self) -> Dict[str, Any]:
        """
        Test PostgreSQL connection and return status.
        
        Returns:
            Dict with connection status and database info
        """
        if not self._pool:
            await self.initialize_pool()
        
        try:
            async with self._pool.acquire() as conn:
                # Test basic connection
                version = await conn.fetchval("SELECT version()")
                
                # Check if telefonica schema exists
                schema_exists = await conn.fetchval(
                    "SELECT EXISTS(SELECT 1 FROM information_schema.schemata WHERE schema_name = $1)",
                    self.schema
                )
                
                # Count tables in telefonica schema
                table_count = await conn.fetchval(
                    """
                    SELECT COUNT(*)
                    FROM information_schema.tables 
                    WHERE table_schema = $1
                    """,
                    self.schema
                )
                
                return {
                    "connected": True,
                    "database_url": self._mask_database_url(),
                    "schema": self.schema,
                    "schema_exists": schema_exists,
                    "table_count": table_count,
                    "postgresql_version": version[:50] + "..." if len(version) > 50 else version,
                    "test_timestamp": datetime.now().isoformat()
                }
                
        except Exception as e:
            logger.error(f"❌ PostgreSQL connection test failed: {e}")
            return {
                "connected": False,
                "error": str(e),
                "database_url": self._mask_database_url()
            }
    
    def _mask_database_url(self) -> str:
        """Mask sensitive information in database URL for logging."""
        if "://" in self.database_url:
            parts = self.database_url.split("://")
            if len(parts) == 2:
                protocol = parts[0]
                rest = parts[1]
                if "@" in rest:
                    auth_part, host_part = rest.split("@", 1)
                    return f"{protocol}://***:***@{host_part}"
        return "***masked***"
    
    async def get_schema_info(self) -> Dict[str, Any]:
        """
        Get detailed information about the telefonica schema.
        
        Returns:
            Dict with schema structure and statistics
        """
        if not self._pool:
            await self.initialize_pool()
        
        try:
            async with self._pool.acquire() as conn:
                # Get tables and their row counts
                tables_query = f"""
                    SELECT 
                        t.table_name,
                        t.table_type,
                        CASE 
                            WHEN t.table_name LIKE 'dim_%' THEN 'DIMENSION'
                            WHEN t.table_name LIKE 'fact_%' THEN 'FACT'
                            WHEN t.table_name LIKE 'v_%' THEN 'VIEW'
                            ELSE 'OTHER'
                        END as table_category,
                        pg_size_pretty(pg_total_relation_size(quote_ident(t.table_schema)||'.'||quote_ident(t.table_name))) as table_size
                    FROM information_schema.tables t
                    WHERE t.table_schema = '{self.schema}'
                    ORDER BY table_category, t.table_name
                """
                
                tables_data = await conn.fetch(tables_query)
                
                tables_info = []
                for row in tables_data:
                    # Get row count for each table
                    try:
                        row_count = await conn.fetchval(
                            f'SELECT COUNT(*) FROM {self.schema}.{row["table_name"]}'
                        )
                    except:
                        row_count = 0
                    
                    tables_info.append({
                        "table_name": row["table_name"],
                        "table_type": row["table_type"],
                        "category": row["table_category"],
                        "row_count": row_count,
                        "table_size": row["table_size"]
                    })
                
                # Summary by category
                summary = {}
                for table in tables_info:
                    category = table["category"]
                    if category not in summary:
                        summary[category] = {
                            "table_count": 0,
                            "total_rows": 0
                        }
                    summary[category]["table_count"] += 1
                    summary[category]["total_rows"] += table["row_count"]
                
                return {
                    "schema": self.schema,
                    "tables": tables_info,
                    "summary": summary,
                    "timestamp": datetime.now().isoformat()
                }
                
        except Exception as e:
            logger.error(f"❌ Failed to get schema info: {e}")
            return {"error": str(e)}
    
    async def insert_sample_data(self) -> Dict[str, Any]:
        """
        Insert sample data for testing dimensional model.
        
        This creates basic test data to validate the schema works.
        
        Returns:
            Dict with insertion results
        """
        if not self._pool:
            await self.initialize_pool()
        
        results = {"inserted": {}, "errors": []}
        
        try:
            async with self._pool.acquire() as conn:
                async with conn.transaction():
                    
                    # Insert sample ejecutivos
                    ejecutivos_data = [
                        ("Ana García", "HUMANO", "Equipo A", "Supervisor 1"),
                        ("Carlos López", "HUMANO", "Equipo B", "Supervisor 2"),
                        ("VOICEBOT", "VOICEBOT", "Automatico", "Sistema"),
                        ("María Fernández", "HUMANO", "Equipo A", "Supervisor 1"),
                        ("DISCADOR", "HUMANO", "Equipo C", "Supervisor 3")
                    ]
                    
                    for ejecutivo_data in ejecutivos_data:
                        await conn.execute(
                            f"""
                            INSERT INTO {self.schema}.dim_ejecutivo (ejecutivo, tipo_agente, equipo, supervisor)
                            VALUES ($1, $2, $3, $4)
                            ON CONFLICT (ejecutivo) DO UPDATE SET
                                tipo_agente = EXCLUDED.tipo_agente,
                                equipo = EXCLUDED.equipo,
                                supervisor = EXCLUDED.supervisor
                            """,
                            *ejecutivo_data
                        )
                    
                    results["inserted"]["dim_ejecutivo"] = len(ejecutivos_data)
                    
                    # Insert sample clientes
                    clientes_data = [
                        (12345001, "Cliente Test 1", "12345678", "DNI", "MOVIL"),
                        (12345002, "Cliente Test 2", "87654321", "DNI", "FIJA"),
                        (12345003, "Cliente Test 3", "11111111", "DNI", "MOVIL"),
                        (12345004, "Cliente Test 4", "22222222", "DNI", "FIJA"),
                        (12345005, "Cliente Test 5", "33333333", "DNI", "MOVIL")
                    ]
                    
                    for cliente_data in clientes_data:
                        await conn.execute(
                            f"""
                            INSERT INTO {self.schema}.dim_cliente (cod_luna, cliente, documento_identidad, tipo_documento, linea_servicio)
                            VALUES ($1, $2, $3, $4, $5)
                            ON CONFLICT (cod_luna) DO UPDATE SET
                                cliente = EXCLUDED.cliente,
                                documento_identidad = EXCLUDED.documento_identidad,
                                linea_servicio = EXCLUDED.linea_servicio
                            """,
                            *cliente_data
                        )
                    
                    results["inserted"]["dim_cliente"] = len(clientes_data)
                    
                    # Insert sample gestiones
                    today = date.today()
                    fecha_id = await conn.fetchval(
                        f"SELECT fecha_id FROM {self.schema}.dim_tiempo WHERE fecha = $1",
                        today
                    )
                    
                    if fecha_id:
                        # Get some dimension IDs
                        ejecutivo_ids = await conn.fetch(
                            f"SELECT ejecutivo_id, ejecutivo FROM {self.schema}.dim_ejecutivo LIMIT 3"
                        )
                        cliente_ids = await conn.fetch(
                            f"SELECT cliente_id, cod_luna FROM {self.schema}.dim_cliente LIMIT 3"
                        )
                        canal_ids = await conn.fetch(
                            f"SELECT canal_id, canal FROM {self.schema}.dim_canal WHERE canal IN ('CALL', 'VOICEBOT') LIMIT 2"
                        )
                        cartera_id = await conn.fetchval(
                            f"SELECT cartera_id FROM {self.schema}.dim_cartera WHERE tipo_cartera = 'Gestión Temprana'"
                        )
                        servicio_id = await conn.fetchval(
                            f"SELECT servicio_id FROM {self.schema}.dim_servicio WHERE servicio = 'MOVIL'"
                        )
                        
                        gestion_count = 0
                        for ej in ejecutivo_ids[:2]:  # Solo 2 ejecutivos
                            for cl in cliente_ids[:2]:  # Solo 2 clientes
                                for cn in canal_ids:  # Ambos canales
                                    await conn.execute(
                                        f"""
                                        INSERT INTO {self.schema}.fact_gestiones 
                                        (fecha_id, cliente_id, ejecutivo_id, canal_id, cartera_id, servicio_id, 
                                         hora_gestion, contactabilidad, tipificacion_homologada, es_pdp, duracion_segundos)
                                        VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
                                        ON CONFLICT (fecha_id, ejecutivo_id, canal_id, cliente_id, hora_gestion) DO NOTHING
                                        """,
                                        fecha_id, cl["cliente_id"], ej["ejecutivo_id"], cn["canal_id"],
                                        cartera_id, servicio_id, "10:30:00", "CONTACTO EFECTIVO",
                                        "COMPROMISO_PAGO", True, 180
                                    )
                                    gestion_count += 1
                        
                        results["inserted"]["fact_gestiones"] = gestion_count
                    
                    logger.info(f"✅ Sample data inserted successfully: {results['inserted']}")
                    
        except Exception as e:
            error_msg = f"Failed to insert sample data: {e}"
            logger.error(f"❌ {error_msg}")
            results["errors"].append(error_msg)
        
        return results
    
    async def get_sample_gestiones(self, limit: int = 50) -> pl.DataFrame:
        """
        Get sample gestiones data with dimensional information.
        
        Args:
            limit: Number of records to retrieve
            
        Returns:
            Polars DataFrame with gestiones data
        """
        if not self._pool:
            await self.initialize_pool()
        
        try:
            async with self._pool.acquire() as conn:
                query = f"""
                    SELECT 
                        dt.fecha,
                        fg.hora_gestion,
                        de.ejecutivo,
                        dc.canal,
                        dcl.cod_luna,
                        dcl.cliente,
                        dcar.tipo_cartera,
                        ds.servicio,
                        fg.contactabilidad,
                        fg.tipificacion_homologada,
                        fg.es_pdp,
                        fg.duracion_segundos
                    FROM {self.schema}.fact_gestiones fg
                    JOIN {self.schema}.dim_tiempo dt ON fg.fecha_id = dt.fecha_id
                    JOIN {self.schema}.dim_ejecutivo de ON fg.ejecutivo_id = de.ejecutivo_id
                    JOIN {self.schema}.dim_canal dc ON fg.canal_id = dc.canal_id
                    JOIN {self.schema}.dim_cliente dcl ON fg.cliente_id = dcl.cliente_id
                    JOIN {self.schema}.dim_cartera dcar ON fg.cartera_id = dcar.cartera_id
                    JOIN {self.schema}.dim_servicio ds ON fg.servicio_id = ds.servicio_id
                    ORDER BY dt.fecha DESC, fg.hora_gestion DESC
                    LIMIT {limit}
                """
                
                rows = await conn.fetch(query)
                
                if rows:
                    # Convert to list of dicts for Polars
                    data = [dict(row) for row in rows]
                    df = pl.DataFrame(data)
                    logger.info(f"✅ Retrieved {len(df)} gestiones records")
                    return df
                else:
                    logger.info("ℹ️  No gestiones data found")
                    return pl.DataFrame()
                    
        except Exception as e:
            logger.error(f"❌ Failed to get sample gestiones: {e}")
            return pl.DataFrame()

# =====================================================
# 🏭 FACTORY FUNCTION
# =====================================================

def create_telefonica_postgresql_adapter() -> TelefonicaPostgreSQLAdapter:
    """
    Factory function to create PostgreSQL adapter from environment variables.
    
    Returns:
        Configured TelefonicaPostgreSQLAdapter instance
    """
    database_url = os.getenv("POSTGRES_DATABASE_URL")
    if not database_url:
        raise ValueError("POSTGRES_DATABASE_URL environment variable is required")
    
    schema = os.getenv("POSTGRES_SCHEMA", "telefonica")
    
    return TelefonicaPostgreSQLAdapter(
        database_url=database_url,
        schema=schema
    )

# =====================================================
# 🧪 TESTING UTILITIES
# =====================================================

async def test_postgresql_connection():
    """Test PostgreSQL connection and log results."""
    logger.info("🔍 Testing PostgreSQL connection...")
    
    adapter = create_telefonica_postgresql_adapter()
    
    try:
        # Test connection
        connection_result = await adapter.test_connection()
        logger.info(f"Connection result: {connection_result}")
        
        if connection_result["connected"]:
            # Get schema info
            schema_info = await adapter.get_schema_info()
            logger.info(f"Schema info: {schema_info}")
            
            # Insert sample data
            insert_result = await adapter.insert_sample_data()
            logger.info(f"Sample data insert: {insert_result}")
            
            # Get sample gestiones
            sample_data = await adapter.get_sample_gestiones(10)
            logger.info(f"Sample gestiones: {len(sample_data)} rows")
    
    finally:
        await adapter.close_pool()
    
    return connection_result

if __name__ == "__main__":
    # Quick test
    asyncio.run(test_postgresql_connection())