"""
Generate Dashboard Data Use Case for Telefónica del Perú.

Provides dashboard-ready data with optimized queries and aggregations.
"""

from datetime import date, datetime, timedelta
from typing import Dict, Any, List, Optional
import logging

from src.infrastructure.adapters.postgresql.datamart_adapter import TelefonicaDatamartAdapter

logger = logging.getLogger(__name__)


class GenerateDashboardDataUseCase:
    """
    Generate dashboard data for Telefónica del Perú.
    
    Provides optimized data queries for the frontend dashboard,
    implementing the KPIs and metrics defined in Issue #12.
    """
    
    def __init__(self, datamart_adapter: TelefonicaDatamartAdapter):
        self.datamart = datamart_adapter
        
        logger.info("Initialized GenerateDashboardDataUseCase")
    
    async def get_dashboard_summary(
        self, 
        fecha_inicio: date, 
        fecha_fin: date
    ) -> Dict[str, Any]:
        """
        Get main dashboard summary with KPIs.
        
        Returns key metrics for the dashboard header.
        """
        logger.info(f"Generating dashboard summary for {fecha_inicio} to {fecha_fin}")
        
        await self.datamart.initialize_pool()
        
        async with self.datamart._pool.acquire() as conn:
            # Main KPIs
            summary = await conn.fetchrow(f"""
                SELECT 
                    COUNT(*) as total_gestiones,
                    COUNT(DISTINCT cod_luna) as clientes_gestionados,
                    COUNT(*) FILTER (WHERE contactabilidad = 'CONTACTO EFECTIVO') as contactos_efectivos,
                    COUNT(*) FILTER (WHERE tipificacion_homologada = 'COMPROMISO_PAGO') as gestiones_pdp,
                    
                    -- Calculated KPIs
                    ROUND(
                        COUNT(*) FILTER (WHERE contactabilidad = 'CONTACTO EFECTIVO') * 100.0 / 
                        NULLIF(COUNT(*), 0), 
                        1
                    ) as tasa_contactabilidad,
                    
                    ROUND(
                        COUNT(*) FILTER (WHERE tipificacion_homologada = 'COMPROMISO_PAGO') * 100.0 / 
                        NULLIF(COUNT(*) FILTER (WHERE contactabilidad = 'CONTACTO EFECTIVO'), 0), 
                        1
                    ) as tasa_pdp,
                    
                    -- Channel distribution
                    COUNT(*) FILTER (WHERE canal = 'CALL') as gestiones_call,
                    COUNT(*) FILTER (WHERE canal = 'VOICEBOT') as gestiones_voicebot,
                    
                    -- Service distribution
                    COUNT(*) FILTER (WHERE servicio = 'MOVIL') as gestiones_movil,
                    COUNT(*) FILTER (WHERE servicio = 'FIJA') as gestiones_fija
                    
                FROM {self.datamart.schema}.fact_gestiones
                WHERE fecha_gestion BETWEEN $1 AND $2
            """, fecha_inicio, fecha_fin)
            
            result = {
                "period": {
                    "fecha_inicio": fecha_inicio.isoformat(),
                    "fecha_fin": fecha_fin.isoformat(),
                    "dias": (fecha_fin - fecha_inicio).days + 1
                },
                "kpis": dict(summary) if summary else {},
                "generated_at": datetime.now().isoformat()
            }
            
            # Calculate productivity metrics
            if summary and summary['total_gestiones'] > 0:
                result["kpis"]["productividad_diaria"] = round(
                    summary['total_gestiones'] / result["period"]["dias"], 1
                )
                
                result["kpis"]["efectividad"] = round(
                    (summary['gestiones_pdp'] / summary['total_gestiones']) * 100, 1
                ) if summary['total_gestiones'] > 0 else 0
            
            logger.info(f"Generated summary with {result['kpis'].get('total_gestiones', 0)} gestiones")
            
            return result
    
    async def get_ejecutivos_performance(
        self, 
        fecha_inicio: date, 
        fecha_fin: date,
        limit: int = 20
    ) -> List[Dict[str, Any]]:
        """Get performance data by ejecutivo."""
        
        await self.datamart.initialize_pool()
        
        async with self.datamart._pool.acquire() as conn:
            ejecutivos = await conn.fetch(f"""
                SELECT 
                    ejecutivo,
                    COUNT(*) as total_gestiones,
                    COUNT(DISTINCT cod_luna) as clientes_gestionados,
                    COUNT(*) FILTER (WHERE contactabilidad = 'CONTACTO EFECTIVO') as contactos_efectivos,
                    COUNT(*) FILTER (WHERE tipificacion_homologada = 'COMPROMISO_PAGO') as gestiones_pdp,
                    
                    -- Performance metrics
                    ROUND(
                        COUNT(*) FILTER (WHERE contactabilidad = 'CONTACTO EFECTIVO') * 100.0 / 
                        NULLIF(COUNT(*), 0), 
                        1
                    ) as tasa_contactabilidad,
                    
                    ROUND(
                        COUNT(*) FILTER (WHERE tipificacion_homologada = 'COMPROMISO_PAGO') * 100.0 / 
                        NULLIF(COUNT(*) FILTER (WHERE contactabilidad = 'CONTACTO EFECTIVO'), 0), 
                        1
                    ) as tasa_pdp,
                    
                    -- Productivity
                    ROUND(COUNT(*) * 1.0 / $3, 1) as gestiones_por_dia
                    
                FROM {self.datamart.schema}.fact_gestiones
                WHERE fecha_gestion BETWEEN $1 AND $2
                  AND ejecutivo != 'VOICEBOT'  -- Exclude automated
                GROUP BY ejecutivo
                HAVING COUNT(*) > 0
                ORDER BY total_gestiones DESC
                LIMIT $4
            """, fecha_inicio, fecha_fin, (fecha_fin - fecha_inicio).days + 1, limit)
            
            return [dict(row) for row in ejecutivos]
    
    async def get_daily_trends(
        self, 
        fecha_inicio: date, 
        fecha_fin: date
    ) -> List[Dict[str, Any]]:
        """Get daily trend data for charts."""
        
        await self.datamart.initialize_pool()
        
        async with self.datamart._pool.acquire() as conn:
            trends = await conn.fetch(f"""
                SELECT 
                    fecha_gestion as fecha,
                    COUNT(*) as total_gestiones,
                    COUNT(*) FILTER (WHERE contactabilidad = 'CONTACTO EFECTIVO') as contactos_efectivos,
                    COUNT(*) FILTER (WHERE tipificacion_homologada = 'COMPROMISO_PAGO') as gestiones_pdp,
                    COUNT(DISTINCT cod_luna) as clientes_gestionados,
                    
                    -- Channel breakdown
                    COUNT(*) FILTER (WHERE canal = 'CALL') as gestiones_call,
                    COUNT(*) FILTER (WHERE canal = 'VOICEBOT') as gestiones_voicebot,
                    
                    -- Calculate rates
                    ROUND(
                        COUNT(*) FILTER (WHERE contactabilidad = 'CONTACTO EFECTIVO') * 100.0 / 
                        NULLIF(COUNT(*), 0), 
                        1
                    ) as tasa_contactabilidad
                    
                FROM {self.datamart.schema}.fact_gestiones
                WHERE fecha_gestion BETWEEN $1 AND $2
                GROUP BY fecha_gestion
                ORDER BY fecha_gestion
            """, fecha_inicio, fecha_fin)
            
            return [dict(row) for row in trends]
    
    async def get_channel_comparison(
        self, 
        fecha_inicio: date, 
        fecha_fin: date
    ) -> Dict[str, Any]:
        """Compare CALL vs VOICEBOT performance."""
        
        await self.datamart.initialize_pool()
        
        async with self.datamart._pool.acquire() as conn:
            comparison = await conn.fetch(f"""
                SELECT 
                    canal,
                    COUNT(*) as total_gestiones,
                    COUNT(DISTINCT cod_luna) as clientes_gestionados,
                    COUNT(*) FILTER (WHERE contactabilidad = 'CONTACTO EFECTIVO') as contactos_efectivos,
                    COUNT(*) FILTER (WHERE tipificacion_homologada = 'COMPROMISO_PAGO') as gestiones_pdp,
                    
                    -- Performance metrics
                    ROUND(
                        COUNT(*) FILTER (WHERE contactabilidad = 'CONTACTO EFECTIVO') * 100.0 / 
                        NULLIF(COUNT(*), 0), 
                        1
                    ) as tasa_contactabilidad,
                    
                    ROUND(
                        COUNT(*) FILTER (WHERE tipificacion_homologada = 'COMPROMISO_PAGO') * 100.0 / 
                        NULLIF(COUNT(*) FILTER (WHERE contactabilidad = 'CONTACTO EFECTIVO'), 0), 
                        1
                    ) as tasa_pdp
                    
                FROM {self.datamart.schema}.fact_gestiones
                WHERE fecha_gestion BETWEEN $1 AND $2
                GROUP BY canal
                ORDER BY total_gestiones DESC
            """, fecha_inicio, fecha_fin)
            
            channels = {row['canal']: dict(row) for row in comparison}
            
            # Add comparison insights
            call_data = channels.get('CALL', {})
            voicebot_data = channels.get('VOICEBOT', {})
            
            comparison_insights = {}
            if call_data and voicebot_data:
                comparison_insights = {
                    "call_vs_voicebot_volume": round(
                        call_data.get('total_gestiones', 0) / 
                        max(voicebot_data.get('total_gestiones', 1), 1), 2
                    ),
                    "call_vs_voicebot_effectiveness": round(
                        call_data.get('tasa_contactabilidad', 0) - 
                        voicebot_data.get('tasa_contactabilidad', 0), 1
                    )
                }
            
            return {
                "channels": channels,
                "insights": comparison_insights
            }
    
    async def get_complete_dashboard(
        self, 
        fecha_inicio: date, 
        fecha_fin: date
    ) -> Dict[str, Any]:
        """Get complete dashboard data in single call."""
        
        logger.info(f"Generating complete dashboard for {fecha_inicio} to {fecha_fin}")
        
        # Run all queries in parallel for performance
        tasks = [
            self.get_dashboard_summary(fecha_inicio, fecha_fin),
            self.get_ejecutivos_performance(fecha_inicio, fecha_fin),
            self.get_daily_trends(fecha_inicio, fecha_fin),
            self.get_channel_comparison(fecha_inicio, fecha_fin)
        ]
        
        try:
            summary, ejecutivos, trends, channels = await asyncio.gather(*tasks)
            
            result = {
                "summary": summary,
                "ejecutivos": ejecutivos,
                "daily_trends": trends,
                "channel_comparison": channels,
                "generated_at": datetime.now().isoformat()
            }
            
            logger.info("Complete dashboard data generated successfully")
            
            return result
            
        except Exception as e:
            logger.error(f"Error generating complete dashboard: {e}")
            raise


# Factory function
async def create_dashboard_use_case(
    postgres_database_url: str,
    postgres_schema: str = "telefonica"
) -> GenerateDashboardDataUseCase:
    """Create configured dashboard use case."""
    
    datamart_adapter = TelefonicaDatamartAdapter(
        database_url=postgres_database_url,
        schema=postgres_schema
    )
    
    return GenerateDashboardDataUseCase(datamart_adapter)
