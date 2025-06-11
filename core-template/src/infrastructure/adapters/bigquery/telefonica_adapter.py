"""
BigQuery Adapter for Telefónica del Perú.

Implements data extraction from the 8 identified BigQuery tables:
- 6 Batch tables (masters + transactional)
- 2 Operational tables (CALL + VOICEBOT)
"""

import asyncio
from datetime import date, datetime
from typing import List, Dict, Any, Optional
import logging

from google.cloud import bigquery
from google.cloud.bigquery import Client, QueryJob
import polars as pl

from src.domain.entities import Cliente, Gestion
from src.domain.value_objects import TipificacionHomologada, CanalContacto

logger = logging.getLogger(__name__)


class TelefonicaBigQueryAdapter:
    """
    Adapter for extracting data from Telefónica's BigQuery tables.
    
    Handles the 8 real tables identified in Issue #12:
    - batch_P3fV4dWNeMkN5RJMhV8e_asignacion
    - batch_P3fV4dWNeMkN5RJMhV8e_master_luna  
    - batch_P3fV4dWNeMkN5RJMhV8e_master_contacto
    - batch_P3fV4dWNeMkN5RJMhV8e_tran_deuda
    - batch_P3fV4dWNeMkN5RJMhV8e_pagos
    - batch_P3fV4dWNeMkN5RJMhV8e_campanas
    - mibotair_P3fV4dWNeMkN5RJMhV8e (CALL)
    - voicebot_P3fV4dWNeMkN5RJMhV8e (VOICEBOT)
    """
    
    def __init__(
        self, 
        project_id: str = "mibot-222814",
        dataset: str = "BI_USA",
        credentials_path: Optional[str] = None
    ):
        self.project_id = project_id
        self.dataset = dataset
        
        # Initialize BigQuery client
        if credentials_path:
            self.client = bigquery.Client.from_service_account_json(credentials_path)
        else:
            self.client = bigquery.Client(project=project_id)
        
        logger.info(f"Initialized BigQuery adapter for {project_id}.{dataset}")
    
    async def extract_gestiones(self, fecha_proceso: date) -> List[Gestion]:
        """
        Extract gestiones from both CALL and VOICEBOT tables.
        
        Combines:
        - mibotair_P3fV4dWNeMkN5RJMhV8e (human agents)
        - voicebot_P3fV4dWNeMkN5RJMhV8e (bot interactions)
        """
        query = f"""
        -- CALL gestiones (human agents)
        SELECT 
            fecha_gestion,
            hora_gestion,
            ejecutivo,
            'CALL' as canal,
            contactabilidad,
            CASE 
                WHEN es_pdp = true THEN 'COMPROMISO_PAGO'
                WHEN contactabilidad = 'CONTACTO EFECTIVO' THEN 'CONTACTO_EFECTIVO'
                ELSE 'NO_CONTACTO'
            END as tipificacion_homologada,
            cod_luna,
            servicio,
            cartera,
            monto_exigible
        FROM `{self.project_id}.{self.dataset}.mibotair_P3fV4dWNeMkN5RJMhV8e`
        WHERE DATE(_PARTITIONTIME) = '{fecha_proceso}'
          AND fecha_gestion = '{fecha_proceso}'
        
        UNION ALL
        
        -- VOICEBOT gestiones (automated)
        SELECT 
            fecha_gestion,
            hora_gestion,
            'VOICEBOT' as ejecutivo,
            'VOICEBOT' as canal,
            contactabilidad,
            CASE 
                WHEN es_pdp = true THEN 'COMPROMISO_PAGO'
                WHEN contactabilidad = 'CONTACTO EFECTIVO' THEN 'CONTACTO_EFECTIVO'
                ELSE 'NO_CONTACTO'
            END as tipificacion_homologada,
            cod_luna,
            servicio,
            cartera,
            monto_exigible
        FROM `{self.project_id}.{self.dataset}.voicebot_P3fV4dWNeMkN5RJMhV8e`
        WHERE DATE(_PARTITIONTIME) = '{fecha_proceso}'
          AND fecha_gestion = '{fecha_proceso}'
        
        ORDER BY fecha_gestion, hora_gestion
        """
        
        logger.info(f"Extracting gestiones for {fecha_proceso}")
        
        # Execute query asynchronously
        query_job: QueryJob = self.client.query(query)
        results = query_job.result()
        
        # Convert to domain entities
        gestiones = []
        for row in results:
            try:
                gestion = Gestion(
                    gestion_id=f"{row.cod_luna}_{row.fecha_gestion}_{row.hora_gestion}",
                    fecha_gestion=row.fecha_gestion,
                    hora_gestion=row.hora_gestion,
                    cliente_documento=str(row.cod_luna),
                    ejecutivo=row.ejecutivo or "SISTEMA",
                    canal=CanalContacto.CALL if row.canal == 'CALL' else CanalContacto.VOICEBOT,
                    contactabilidad=row.contactabilidad,
                    tipificacion_original=row.contactabilidad,
                    tipificacion_homologada=getattr(
                        TipificacionHomologada, 
                        row.tipificacion_homologada, 
                        TipificacionHomologada.CONTACTO_EFECTIVO
                    ),
                    duracion_segundos=0,  # Not available in source
                    observaciones=""
                )
                gestiones.append(gestion)
                
            except Exception as e:
                logger.error(f"Error creating Gestion from row {row}: {e}")
                continue
        
        logger.info(f"Extracted {len(gestiones)} gestiones")
        return gestiones
    
    async def extract_clientes(self, fecha_proceso: date) -> List[Cliente]:
        """
        Extract clients from master_luna table.
        """
        query = f"""
        SELECT DISTINCT
            cod_luna,
            cliente as nombre,
            dni as documento,
            servicio,
            cartera,
            monto_exigible,
            zona
        FROM `{self.project_id}.{self.dataset}.batch_P3fV4dWNeMkN5RJMhV8e_master_luna`
        WHERE DATE(_PARTITIONTIME) = '{fecha_proceso}'
          AND cod_luna IS NOT NULL
          AND dni IS NOT NULL
        ORDER BY cod_luna
        """
        
        logger.info(f"Extracting clientes for {fecha_proceso}")
        
        query_job: QueryJob = self.client.query(query)
        results = query_job.result()
        
        # Convert to domain entities
        clientes = []
        for row in results:
            try:
                cliente = Cliente(
                    cod_luna=row.cod_luna,
                    nombre=row.nombre or f"Cliente {row.cod_luna}",
                    documento=str(row.dni),
                    servicio=row.servicio or "MOVIL",
                    cartera=row.cartera or "Regular",
                    deuda_total=float(row.monto_exigible or 0),
                    zona=row.zona or "LIMA"
                )
                clientes.append(cliente)
                
            except Exception as e:
                logger.error(f"Error creating Cliente from row {row}: {e}")
                continue
        
        logger.info(f"Extracted {len(clientes)} clientes")
        return clientes
    
    async def extract_daily_data(self, fecha_proceso: date) -> Dict[str, Any]:
        """
        Extract complete daily data for Telefónica.
        
        Returns:
            Dict containing gestiones, clientes, and metadata
        """
        logger.info(f"Starting daily extraction for {fecha_proceso}")
        
        # Extract data in parallel
        gestiones_task = asyncio.create_task(self.extract_gestiones(fecha_proceso))
        clientes_task = asyncio.create_task(self.extract_clientes(fecha_proceso))
        
        gestiones, clientes = await asyncio.gather(
            gestiones_task, 
            clientes_task,
            return_exceptions=True
        )
        
        # Handle exceptions
        if isinstance(gestiones, Exception):
            logger.error(f"Error extracting gestiones: {gestiones}")
            gestiones = []
        
        if isinstance(clientes, Exception):
            logger.error(f"Error extracting clientes: {clientes}")
            clientes = []
        
        result = {
            "fecha_proceso": fecha_proceso,
            "gestiones": gestiones,
            "clientes": clientes,
            "metadata": {
                "total_gestiones": len(gestiones),
                "total_clientes": len(clientes),
                "extraction_timestamp": datetime.now().isoformat(),
                "source": "BigQuery",
                "project": self.project_id,
                "dataset": self.dataset
            }
        }
        
        logger.info(
            f"Extraction completed: {len(gestiones)} gestiones, "
            f"{len(clientes)} clientes"
        )
        
        return result
    
    async def test_connection(self) -> bool:
        """
        Test BigQuery connection and table availability.
        """
        try:
            # Test basic connection
            datasets = list(self.client.list_datasets())
            logger.info(f"Connected to BigQuery. Available datasets: {len(datasets)}")
            
            # Test specific tables
            tables_to_check = [
                f"{self.project_id}.{self.dataset}.mibotair_P3fV4dWNeMkN5RJMhV8e",
                f"{self.project_id}.{self.dataset}.voicebot_P3fV4dWNeMkN5RJMhV8e",
                f"{self.project_id}.{self.dataset}.batch_P3fV4dWNeMkN5RJMhV8e_master_luna"
            ]
            
            for table_id in tables_to_check:
                try:
                    table = self.client.get_table(table_id)
                    logger.info(f"✅ Table {table_id} exists ({table.num_rows} rows)")
                except Exception as e:
                    logger.error(f"❌ Table {table_id} not accessible: {e}")
                    return False
            
            return True
            
        except Exception as e:
            logger.error(f"BigQuery connection test failed: {e}")
            return False
