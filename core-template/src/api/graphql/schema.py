"""
GraphQL Schema for Telefónica Dashboard.

Provides types and resolvers for dashboard data queries.
"""

from datetime import date, datetime
from typing import List, Optional
import strawberry

from src.api.dependencies import get_dashboard_use_case


@strawberry.type
class KPISummary:
    """Main KPIs for dashboard header."""
    total_gestiones: int
    clientes_gestionados: int
    contactos_efectivos: int
    gestiones_pdp: int
    tasa_contactabilidad: float
    tasa_pdp: float
    productividad_diaria: float
    efectividad: float
    
    # Channel breakdown
    gestiones_call: int
    gestiones_voicebot: int
    
    # Service breakdown
    gestiones_movil: int
    gestiones_fija: int


@strawberry.type
class PeriodInfo:
    """Period information for queries."""
    fecha_inicio: str
    fecha_fin: str
    dias: int


@strawberry.type
class DashboardSummary:
    """Complete dashboard summary."""
    period: PeriodInfo
    kpis: KPISummary
    generated_at: str


@strawberry.type
class EjecutivoPerformance:
    """Performance metrics by ejecutivo."""
    ejecutivo: str
    total_gestiones: int
    clientes_gestionados: int
    contactos_efectivos: int
    gestiones_pdp: int
    tasa_contactabilidad: float
    tasa_pdp: float
    gestiones_por_dia: float


@strawberry.type
class DailyTrend:
    """Daily trend data for charts."""
    fecha: str
    total_gestiones: int
    contactos_efectivos: int
    gestiones_pdp: int
    clientes_gestionados: int
    gestiones_call: int
    gestiones_voicebot: int
    tasa_contactabilidad: float


@strawberry.type
class ChannelMetrics:
    """Metrics by channel."""
    canal: str
    total_gestiones: int
    clientes_gestionados: int
    contactos_efectivos: int
    gestiones_pdp: int
    tasa_contactabilidad: float
    tasa_pdp: float


@strawberry.type
class ChannelComparison:
    """Channel comparison with insights."""
    call: Optional[ChannelMetrics]
    voicebot: Optional[ChannelMetrics]
    call_vs_voicebot_volume: Optional[float]
    call_vs_voicebot_effectiveness: Optional[float]


@strawberry.type
class CompleteDashboard:
    """Complete dashboard data."""
    summary: DashboardSummary
    ejecutivos: List[EjecutivoPerformance]
    daily_trends: List[DailyTrend]
    channel_comparison: ChannelComparison
    generated_at: str


@strawberry.type
class Query:
    """GraphQL root query."""
    
    @strawberry.field
    async def dashboard_summary(
        self,
        fecha_inicio: Optional[str] = None,
        fecha_fin: Optional[str] = None
    ) -> DashboardSummary:
        """Get dashboard summary for date range."""
        
        # Parse dates or use defaults
        if fecha_inicio and fecha_fin:
            fecha_inicio_date = date.fromisoformat(fecha_inicio)
            fecha_fin_date = date.fromisoformat(fecha_fin)
        else:
            # Default to last 30 days
            from datetime import timedelta
            fecha_fin_date = date.today()
            fecha_inicio_date = fecha_fin_date - timedelta(days=30)
        
        # Get dashboard use case
        dashboard_use_case = await get_dashboard_use_case()
        
        # Get data
        summary_data = await dashboard_use_case.get_dashboard_summary(
            fecha_inicio_date, fecha_fin_date
        )
        
        # Convert to GraphQL types
        return DashboardSummary(
            period=PeriodInfo(
                fecha_inicio=summary_data["period"]["fecha_inicio"],
                fecha_fin=summary_data["period"]["fecha_fin"],
                dias=summary_data["period"]["dias"]
            ),
            kpis=KPISummary(
                total_gestiones=summary_data["kpis"].get("total_gestiones", 0),
                clientes_gestionados=summary_data["kpis"].get("clientes_gestionados", 0),
                contactos_efectivos=summary_data["kpis"].get("contactos_efectivos", 0),
                gestiones_pdp=summary_data["kpis"].get("gestiones_pdp", 0),
                tasa_contactabilidad=summary_data["kpis"].get("tasa_contactabilidad", 0.0),
                tasa_pdp=summary_data["kpis"].get("tasa_pdp", 0.0),
                productividad_diaria=summary_data["kpis"].get("productividad_diaria", 0.0),
                efectividad=summary_data["kpis"].get("efectividad", 0.0),
                gestiones_call=summary_data["kpis"].get("gestiones_call", 0),
                gestiones_voicebot=summary_data["kpis"].get("gestiones_voicebot", 0),
                gestiones_movil=summary_data["kpis"].get("gestiones_movil", 0),
                gestiones_fija=summary_data["kpis"].get("gestiones_fija", 0)
            ),
            generated_at=summary_data["generated_at"]
        )
    
    @strawberry.field
    async def ejecutivos_performance(
        self,
        fecha_inicio: Optional[str] = None,
        fecha_fin: Optional[str] = None,
        limit: int = 20
    ) -> List[EjecutivoPerformance]:
        """Get ejecutivos performance ranking."""
        
        # Parse dates or use defaults
        if fecha_inicio and fecha_fin:
            fecha_inicio_date = date.fromisoformat(fecha_inicio)
            fecha_fin_date = date.fromisoformat(fecha_fin)
        else:
            # Default to last 7 days
            from datetime import timedelta
            fecha_fin_date = date.today()
            fecha_inicio_date = fecha_fin_date - timedelta(days=7)
        
        # Get dashboard use case
        dashboard_use_case = await get_dashboard_use_case()
        
        # Get data
        ejecutivos_data = await dashboard_use_case.get_ejecutivos_performance(
            fecha_inicio_date, fecha_fin_date, limit
        )
        
        # Convert to GraphQL types
        return [
            EjecutivoPerformance(
                ejecutivo=ej["ejecutivo"],
                total_gestiones=ej["total_gestiones"],
                clientes_gestionados=ej["clientes_gestionados"],
                contactos_efectivos=ej["contactos_efectivos"],
                gestiones_pdp=ej["gestiones_pdp"],
                tasa_contactabilidad=ej["tasa_contactabilidad"] or 0.0,
                tasa_pdp=ej["tasa_pdp"] or 0.0,
                gestiones_por_dia=ej["gestiones_por_dia"] or 0.0
            )
            for ej in ejecutivos_data
        ]
    
    @strawberry.field
    async def daily_trends(
        self,
        fecha_inicio: Optional[str] = None,
        fecha_fin: Optional[str] = None
    ) -> List[DailyTrend]:
        """Get daily trends for charts."""
        
        # Parse dates or use defaults
        if fecha_inicio and fecha_fin:
            fecha_inicio_date = date.fromisoformat(fecha_inicio)
            fecha_fin_date = date.fromisoformat(fecha_fin)
        else:
            # Default to last 14 days
            from datetime import timedelta
            fecha_fin_date = date.today()
            fecha_inicio_date = fecha_fin_date - timedelta(days=14)
        
        # Get dashboard use case
        dashboard_use_case = await get_dashboard_use_case()
        
        # Get data
        trends_data = await dashboard_use_case.get_daily_trends(
            fecha_inicio_date, fecha_fin_date
        )
        
        # Convert to GraphQL types
        return [
            DailyTrend(
                fecha=trend["fecha"].isoformat() if hasattr(trend["fecha"], 'isoformat') else str(trend["fecha"]),
                total_gestiones=trend["total_gestiones"],
                contactos_efectivos=trend["contactos_efectivos"],
                gestiones_pdp=trend["gestiones_pdp"],
                clientes_gestionados=trend["clientes_gestionados"],
                gestiones_call=trend["gestiones_call"],
                gestiones_voicebot=trend["gestiones_voicebot"],
                tasa_contactabilidad=trend["tasa_contactabilidad"] or 0.0
            )
            for trend in trends_data
        ]
    
    @strawberry.field
    async def channel_comparison(
        self,
        fecha_inicio: Optional[str] = None,
        fecha_fin: Optional[str] = None
    ) -> ChannelComparison:
        """Get channel comparison (CALL vs VOICEBOT)."""
        
        # Parse dates or use defaults
        if fecha_inicio and fecha_fin:
            fecha_inicio_date = date.fromisoformat(fecha_inicio)
            fecha_fin_date = date.fromisoformat(fecha_fin)
        else:
            # Default to last 7 days
            from datetime import timedelta
            fecha_fin_date = date.today()
            fecha_inicio_date = fecha_fin_date - timedelta(days=7)
        
        # Get dashboard use case
        dashboard_use_case = await get_dashboard_use_case()
        
        # Get data
        comparison_data = await dashboard_use_case.get_channel_comparison(
            fecha_inicio_date, fecha_fin_date
        )
        
        # Convert to GraphQL types
        call_data = comparison_data["channels"].get("CALL")
        voicebot_data = comparison_data["channels"].get("VOICEBOT")
        
        return ChannelComparison(
            call=ChannelMetrics(
                canal=call_data["canal"],
                total_gestiones=call_data["total_gestiones"],
                clientes_gestionados=call_data["clientes_gestionados"],
                contactos_efectivos=call_data["contactos_efectivos"],
                gestiones_pdp=call_data["gestiones_pdp"],
                tasa_contactabilidad=call_data["tasa_contactabilidad"] or 0.0,
                tasa_pdp=call_data["tasa_pdp"] or 0.0
            ) if call_data else None,
            
            voicebot=ChannelMetrics(
                canal=voicebot_data["canal"],
                total_gestiones=voicebot_data["total_gestiones"],
                clientes_gestionados=voicebot_data["clientes_gestionados"],
                contactos_efectivos=voicebot_data["contactos_efectivos"],
                gestiones_pdp=voicebot_data["gestiones_pdp"],
                tasa_contactabilidad=voicebot_data["tasa_contactabilidad"] or 0.0,
                tasa_pdp=voicebot_data["tasa_pdp"] or 0.0
            ) if voicebot_data else None,
            
            call_vs_voicebot_volume=comparison_data["insights"].get("call_vs_voicebot_volume"),
            call_vs_voicebot_effectiveness=comparison_data["insights"].get("call_vs_voicebot_effectiveness")
        )
    
    @strawberry.field
    async def complete_dashboard(
        self,
        fecha_inicio: Optional[str] = None,
        fecha_fin: Optional[str] = None
    ) -> CompleteDashboard:
        """Get complete dashboard data in single query."""
        
        # Parse dates or use defaults
        if fecha_inicio and fecha_fin:
            fecha_inicio_date = date.fromisoformat(fecha_inicio)
            fecha_fin_date = date.fromisoformat(fecha_fin)
        else:
            # Default to last 7 days
            from datetime import timedelta
            fecha_fin_date = date.today()
            fecha_inicio_date = fecha_fin_date - timedelta(days=7)
        
        # Get dashboard use case
        dashboard_use_case = await get_dashboard_use_case()
        
        # Get complete data
        complete_data = await dashboard_use_case.get_complete_dashboard(
            fecha_inicio_date, fecha_fin_date
        )
        
        # Convert summary
        summary = DashboardSummary(
            period=PeriodInfo(
                fecha_inicio=complete_data["summary"]["period"]["fecha_inicio"],
                fecha_fin=complete_data["summary"]["period"]["fecha_fin"],
                dias=complete_data["summary"]["period"]["dias"]
            ),
            kpis=KPISummary(
                total_gestiones=complete_data["summary"]["kpis"].get("total_gestiones", 0),
                clientes_gestionados=complete_data["summary"]["kpis"].get("clientes_gestionados", 0),
                contactos_efectivos=complete_data["summary"]["kpis"].get("contactos_efectivos", 0),
                gestiones_pdp=complete_data["summary"]["kpis"].get("gestiones_pdp", 0),
                tasa_contactabilidad=complete_data["summary"]["kpis"].get("tasa_contactabilidad", 0.0),
                tasa_pdp=complete_data["summary"]["kpis"].get("tasa_pdp", 0.0),
                productividad_diaria=complete_data["summary"]["kpis"].get("productividad_diaria", 0.0),
                efectividad=complete_data["summary"]["kpis"].get("efectividad", 0.0),
                gestiones_call=complete_data["summary"]["kpis"].get("gestiones_call", 0),
                gestiones_voicebot=complete_data["summary"]["kpis"].get("gestiones_voicebot", 0),
                gestiones_movil=complete_data["summary"]["kpis"].get("gestiones_movil", 0),
                gestiones_fija=complete_data["summary"]["kpis"].get("gestiones_fija", 0)
            ),
            generated_at=complete_data["summary"]["generated_at"]
        )
        
        # Convert ejecutivos
        ejecutivos = [
            EjecutivoPerformance(
                ejecutivo=ej["ejecutivo"],
                total_gestiones=ej["total_gestiones"],
                clientes_gestionados=ej["clientes_gestionados"],
                contactos_efectivos=ej["contactos_efectivos"],
                gestiones_pdp=ej["gestiones_pdp"],
                tasa_contactabilidad=ej["tasa_contactabilidad"] or 0.0,
                tasa_pdp=ej["tasa_pdp"] or 0.0,
                gestiones_por_dia=ej["gestiones_por_dia"] or 0.0
            )
            for ej in complete_data["ejecutivos"]
        ]
        
        # Convert trends
        daily_trends = [
            DailyTrend(
                fecha=trend["fecha"].isoformat() if hasattr(trend["fecha"], 'isoformat') else str(trend["fecha"]),
                total_gestiones=trend["total_gestiones"],
                contactos_efectivos=trend["contactos_efectivos"],
                gestiones_pdp=trend["gestiones_pdp"],
                clientes_gestionados=trend["clientes_gestionados"],
                gestiones_call=trend["gestiones_call"],
                gestiones_voicebot=trend["gestiones_voicebot"],
                tasa_contactabilidad=trend["tasa_contactabilidad"] or 0.0
            )
            for trend in complete_data["daily_trends"]
        ]
        
        # Convert channel comparison
        call_data = complete_data["channel_comparison"]["channels"].get("CALL")
        voicebot_data = complete_data["channel_comparison"]["channels"].get("VOICEBOT")
        
        channel_comparison = ChannelComparison(
            call=ChannelMetrics(
                canal=call_data["canal"],
                total_gestiones=call_data["total_gestiones"],
                clientes_gestionados=call_data["clientes_gestionados"],
                contactos_efectivos=call_data["contactos_efectivos"],
                gestiones_pdp=call_data["gestiones_pdp"],
                tasa_contactabilidad=call_data["tasa_contactabilidad"] or 0.0,
                tasa_pdp=call_data["tasa_pdp"] or 0.0
            ) if call_data else None,
            
            voicebot=ChannelMetrics(
                canal=voicebot_data["canal"],
                total_gestiones=voicebot_data["total_gestiones"],
                clientes_gestionados=voicebot_data["clientes_gestionados"],
                contactos_efectivos=voicebot_data["contactos_efectivos"],
                gestiones_pdp=voicebot_data["gestiones_pdp"],
                tasa_contactabilidad=voicebot_data["tasa_contactabilidad"] or 0.0,
                tasa_pdp=voicebot_data["tasa_pdp"] or 0.0
            ) if voicebot_data else None,
            
            call_vs_voicebot_volume=complete_data["channel_comparison"]["insights"].get("call_vs_voicebot_volume"),
            call_vs_voicebot_effectiveness=complete_data["channel_comparison"]["insights"].get("call_vs_voicebot_effectiveness")
        )
        
        return CompleteDashboard(
            summary=summary,
            ejecutivos=ejecutivos,
            daily_trends=daily_trends,
            channel_comparison=channel_comparison,
            generated_at=complete_data["generated_at"]
        )


# Create schema
schema = strawberry.Schema(query=Query)
