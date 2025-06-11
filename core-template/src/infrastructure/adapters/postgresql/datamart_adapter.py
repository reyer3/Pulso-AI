"""
PostgreSQL Datamart Adapter for Telefónica del Perú.

Implements data loading into PostgreSQL datamart with optimized schema
for dashboard queries and cross-filtering.
"""

import asyncio
from datetime import date, datetime
from typing import List, Dict, Any, Optional
import logging

import asyncpg
import polars as pl

from src.domain.entities import Cliente, Gestion

logger = logging.getLogger(__name__)


class TelefonicaDatamartAdapter:
    """
    Adapter for loading data into Telefónica's PostgreSQL datamart.
    
    Implements optimized schema for dashboard performance:
    - Fact tables for gestiones and clients
    - Dimensional lookups
    - Optimized indexes for cross-filtering
    """
    
    def __init__(
        self,
        database_url: str,
        schema: str = "telefonica"
    ):
        self.database_url = database_url
        self.schema = schema
        self._pool: Optional[asyncpg.Pool] = None
        
        logger.info(f"Initialized PostgreSQL datamart adapter for schema: {schema}")
    
    async def initialize_pool(self) -> None:
        """Initialize connection pool."""
        if not self._pool:
            self._pool = await asyncpg.create_pool(
                self.database_url,
                min_size=2,
                max_size=10,
                command_timeout=60
            )
            logger.info("PostgreSQL connection pool initialized")
    
    async def close_pool(self) -> None:
        """Close connection pool."""
        if self._pool:
            await self._pool.close()
            self._pool = None
            logger.info("PostgreSQL connection pool closed")
    
    async def ensure_schema_exists(self) -> None:
        """Create schema and tables if they don't exist."""
        await self.initialize_pool()
        
        async with self._pool.acquire() as conn:
            # Create schema
            await conn.execute(f"CREATE SCHEMA IF NOT EXISTS {self.schema}")
            
            # Create tables
            await self._create_tables(conn)
            await self._create_indexes(conn)
    
    async def _create_tables(self, conn: asyncpg.Connection) -> None:
        """Create optimized tables for dashboard queries."""
        
        # Fact table: gestiones
        await conn.execute(f"""
            CREATE TABLE IF NOT EXISTS {self.schema}.fact_gestiones (
                gestion_id VARCHAR(255) PRIMARY KEY,
                fecha_gestion DATE NOT NULL,
                hora_gestion TIME,
                cod_luna BIGINT NOT NULL,
                ejecutivo VARCHAR(100),
                canal VARCHAR(20) NOT NULL,
                contactabilidad VARCHAR(50),
                tipificacion_homologada VARCHAR(50),
                duracion_segundos INTEGER DEFAULT 0,
                observaciones TEXT,
                created_at TIMESTAMP DEFAULT NOW(),
                
                -- Denormalized fields for performance
                cliente_nombre VARCHAR(255),
                servicio VARCHAR(20),
                cartera VARCHAR(50),
                zona VARCHAR(100)
            )
        """)
        
        # Dimension table: clientes
        await conn.execute(f"""
            CREATE TABLE IF NOT EXISTS {self.schema}.dim_clientes (
                cod_luna BIGINT PRIMARY KEY,
                nombre VARCHAR(255) NOT NULL,
                documento VARCHAR(20) NOT NULL,
                servicio VARCHAR(20),
                cartera VARCHAR(50),
                deuda_total DECIMAL(15,2) DEFAULT 0,
                zona VARCHAR(100),
                created_at TIMESTAMP DEFAULT NOW(),
                updated_at TIMESTAMP DEFAULT NOW()
            )
        """)
        
        # Agregados diarios para performance
        await conn.execute(f"""
            CREATE TABLE IF NOT EXISTS {self.schema}.daily_metrics (
                fecha DATE NOT NULL,
                ejecutivo VARCHAR(100),
                canal VARCHAR(20),
                servicio VARCHAR(20),
                cartera VARCHAR(50),
                
                -- Métricas calculadas
                total_gestiones INTEGER DEFAULT 0,
                contactos_efectivos INTEGER DEFAULT 0,
                gestiones_pdp INTEGER DEFAULT 0,
                clientes_gestionados INTEGER DEFAULT 0,
                
                -- Ratios calculados
                tasa_contactabilidad DECIMAL(5,2) DEFAULT 0,
                tasa_pdp DECIMAL(5,2) DEFAULT 0,
                
                created_at TIMESTAMP DEFAULT NOW(),
                
                PRIMARY KEY (fecha, ejecutivo, canal, servicio, cartera)
            )
        """)
        
        logger.info(f"Tables created in schema {self.schema}")
    
    async def _create_indexes(self, conn: asyncpg.Connection) -> None:
        """Create optimized indexes for dashboard queries."""
        
        indexes = [
            # fact_gestiones indexes
            f"CREATE INDEX IF NOT EXISTS idx_gestiones_fecha ON {self.schema}.fact_gestiones(fecha_gestion)",
            f"CREATE INDEX IF NOT EXISTS idx_gestiones_ejecutivo ON {self.schema}.fact_gestiones(ejecutivo)",
            f"CREATE INDEX IF NOT EXISTS idx_gestiones_canal ON {self.schema}.fact_gestiones(canal)",
            f"CREATE INDEX IF NOT EXISTS idx_gestiones_cod_luna ON {self.schema}.fact_gestiones(cod_luna)",
            f"CREATE INDEX IF NOT EXISTS idx_gestiones_composite ON {self.schema}.fact_gestiones(fecha_gestion, ejecutivo, canal)",
            
            # dim_clientes indexes
            f"CREATE INDEX IF NOT EXISTS idx_clientes_documento ON {self.schema}.dim_clientes(documento)",
            f"CREATE INDEX IF NOT EXISTS idx_clientes_servicio ON {self.schema}.dim_clientes(servicio)",
            f"CREATE INDEX IF NOT EXISTS idx_clientes_cartera ON {self.schema}.dim_clientes(cartera)",
            
            # daily_metrics indexes
            f"CREATE INDEX IF NOT EXISTS idx_metrics_fecha ON {self.schema}.daily_metrics(fecha)",
            f"CREATE INDEX IF NOT EXISTS idx_metrics_ejecutivo ON {self.schema}.daily_metrics(ejecutivo)",
        ]
        
        for index_sql in indexes:
            try:
                await conn.execute(index_sql)
            except Exception as e:
                logger.warning(f"Index creation warning: {e}")
        
        logger.info(f"Indexes created in schema {self.schema}")
    
    async def load_clientes(self, clientes: List[Cliente]) -> int:
        """Load clientes with upsert logic."""
        if not clientes:
            return 0
        
        await self.initialize_pool()
        
        async with self._pool.acquire() as conn:
            # Prepare data
            records = [
                (
                    cliente.cod_luna,
                    cliente.nombre,
                    cliente.documento,
                    cliente.servicio,
                    cliente.cartera,
                    float(cliente.deuda_total),
                    cliente.zona,
                    datetime.now()  # updated_at
                )
                for cliente in clientes
            ]
            
            # Upsert clientes
            await conn.executemany(f"""
                INSERT INTO {self.schema}.dim_clientes 
                (cod_luna, nombre, documento, servicio, cartera, deuda_total, zona, updated_at)
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
                ON CONFLICT (cod_luna) 
                DO UPDATE SET
                    nombre = EXCLUDED.nombre,
                    documento = EXCLUDED.documento,
                    servicio = EXCLUDED.servicio,
                    cartera = EXCLUDED.cartera,
                    deuda_total = EXCLUDED.deuda_total,
                    zona = EXCLUDED.zona,
                    updated_at = EXCLUDED.updated_at
            """, records)
            
            logger.info(f"Loaded {len(records)} clientes")
            return len(records)
    
    async def load_gestiones(self, gestiones: List[Gestion]) -> int:
        """Load gestiones with denormalized client data."""
        if not gestiones:
            return 0
        
        await self.initialize_pool()
        
        async with self._pool.acquire() as conn:
            # Get client data for denormalization
            client_data = {}
            if gestiones:
                cod_lunas = [g.cliente_documento for g in gestiones]
                client_records = await conn.fetch(f"""
                    SELECT cod_luna, nombre, servicio, cartera, zona
                    FROM {self.schema}.dim_clientes
                    WHERE cod_luna = ANY($1::bigint[])
                """, cod_lunas)
                
                client_data = {
                    str(record['cod_luna']): {
                        'nombre': record['nombre'],
                        'servicio': record['servicio'],
                        'cartera': record['cartera'],
                        'zona': record['zona']
                    }
                    for record in client_records
                }
            
            # Prepare gestiones data with denormalization
            records = []
            for gestion in gestiones:
                client_info = client_data.get(gestion.cliente_documento, {})
                
                records.append((
                    gestion.gestion_id,
                    gestion.fecha_gestion,
                    gestion.hora_gestion,
                    int(gestion.cliente_documento),
                    gestion.ejecutivo,
                    gestion.canal.value,
                    gestion.contactabilidad,
                    gestion.tipificacion_homologada.value,
                    gestion.duracion_segundos,
                    gestion.observaciones,
                    client_info.get('nombre', ''),
                    client_info.get('servicio', ''),
                    client_info.get('cartera', ''),
                    client_info.get('zona', '')
                ))
            
            # Insert gestiones (replace if exists)
            await conn.executemany(f"""
                INSERT INTO {self.schema}.fact_gestiones 
                (gestion_id, fecha_gestion, hora_gestion, cod_luna, ejecutivo, canal,
                 contactabilidad, tipificacion_homologada, duracion_segundos, observaciones,
                 cliente_nombre, servicio, cartera, zona)
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14)
                ON CONFLICT (gestion_id) 
                DO UPDATE SET
                    contactabilidad = EXCLUDED.contactabilidad,
                    tipificacion_homologada = EXCLUDED.tipificacion_homologada,
                    observaciones = EXCLUDED.observaciones,
                    cliente_nombre = EXCLUDED.cliente_nombre,
                    servicio = EXCLUDED.servicio,
                    cartera = EXCLUDED.cartera,
                    zona = EXCLUDED.zona
            """, records)
            
            logger.info(f"Loaded {len(records)} gestiones")
            return len(records)
    
    async def refresh_daily_metrics(self, fecha: date) -> None:
        """Refresh daily aggregated metrics for performance."""
        await self.initialize_pool()
        
        async with self._pool.acquire() as conn:
            # Delete existing metrics for the date
            await conn.execute(f"""
                DELETE FROM {self.schema}.daily_metrics 
                WHERE fecha = $1
            """, fecha)
            
            # Calculate and insert new metrics
            await conn.execute(f"""
                INSERT INTO {self.schema}.daily_metrics 
                (fecha, ejecutivo, canal, servicio, cartera, 
                 total_gestiones, contactos_efectivos, gestiones_pdp, clientes_gestionados,
                 tasa_contactabilidad, tasa_pdp)
                SELECT 
                    fecha_gestion as fecha,
                    ejecutivo,
                    canal,
                    servicio,
                    cartera,
                    COUNT(*) as total_gestiones,
                    COUNT(*) FILTER (WHERE contactabilidad = 'CONTACTO EFECTIVO') as contactos_efectivos,
                    COUNT(*) FILTER (WHERE tipificacion_homologada = 'COMPROMISO_PAGO') as gestiones_pdp,
                    COUNT(DISTINCT cod_luna) as clientes_gestionados,
                    ROUND(
                        COUNT(*) FILTER (WHERE contactabilidad = 'CONTACTO EFECTIVO') * 100.0 / COUNT(*), 
                        2
                    ) as tasa_contactabilidad,
                    ROUND(
                        COUNT(*) FILTER (WHERE tipificacion_homologada = 'COMPROMISO_PAGO') * 100.0 / 
                        COUNT(*) FILTER (WHERE contactabilidad = 'CONTACTO EFECTIVO'), 
                        2
                    ) as tasa_pdp
                FROM {self.schema}.fact_gestiones
                WHERE fecha_gestion = $1
                GROUP BY fecha_gestion, ejecutivo, canal, servicio, cartera
            """, fecha)
            
            logger.info(f"Refreshed daily metrics for {fecha}")
    
    async def get_dashboard_data(self, fecha_inicio: date, fecha_fin: date) -> Dict[str, Any]:
        """Get aggregated data for dashboard."""
        await self.initialize_pool()
        
        async with self._pool.acquire() as conn:
            # Get summary metrics
            summary = await conn.fetchrow(f"""
                SELECT 
                    COUNT(*) as total_gestiones,
                    COUNT(DISTINCT cod_luna) as clientes_gestionados,
                    COUNT(*) FILTER (WHERE contactabilidad = 'CONTACTO EFECTIVO') as contactos_efectivos,
                    COUNT(*) FILTER (WHERE tipificacion_homologada = 'COMPROMISO_PAGO') as gestiones_pdp,
                    ROUND(AVG(duracion_segundos), 0) as duracion_promedio
                FROM {self.schema}.fact_gestiones
                WHERE fecha_gestion BETWEEN $1 AND $2
            """, fecha_inicio, fecha_fin)
            
            # Get top ejecutivos
            top_ejecutivos = await conn.fetch(f"""
                SELECT 
                    ejecutivo,
                    COUNT(*) as total_gestiones,
                    COUNT(*) FILTER (WHERE contactabilidad = 'CONTACTO EFECTIVO') as contactos_efectivos,
                    ROUND(
                        COUNT(*) FILTER (WHERE contactabilidad = 'CONTACTO EFECTIVO') * 100.0 / COUNT(*), 
                        1
                    ) as tasa_contactabilidad
                FROM {self.schema}.fact_gestiones
                WHERE fecha_gestion BETWEEN $1 AND $2
                  AND ejecutivo != 'VOICEBOT'
                GROUP BY ejecutivo
                ORDER BY total_gestiones DESC
                LIMIT 10
            """, fecha_inicio, fecha_fin)
            
            return {
                "summary": dict(summary) if summary else {},
                "top_ejecutivos": [dict(row) for row in top_ejecutivos],
                "fecha_inicio": fecha_inicio,
                "fecha_fin": fecha_fin
            }
    
    async def test_connection(self) -> bool:
        """Test PostgreSQL connection."""
        try:
            await self.initialize_pool()
            
            async with self._pool.acquire() as conn:
                result = await conn.fetchval("SELECT 1")
                
                # Test schema access
                tables = await conn.fetch(f"""
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema = $1
                """, self.schema)
                
                logger.info(f"✅ PostgreSQL connected. Schema {self.schema} has {len(tables)} tables")
                return True
                
        except Exception as e:
            logger.error(f"❌ PostgreSQL connection test failed: {e}")
            return False
