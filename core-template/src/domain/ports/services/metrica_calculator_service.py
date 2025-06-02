"""Metrica calculator service interface.

Defines contracts for dynamic metric calculations used in dashboards.
Handles complex business logic for KPI computation and analysis.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from datetime import datetime, date

from ...entities.metrica import Metrica, PeriodoMetrica
from ...value_objects.enums import CanalContacto


class MetricaCalculatorService(ABC):
    """Service interface for calculating business metrics.
    
    This service handles complex metric calculations that require
    data from multiple sources and sophisticated business logic.
    
    Key Features:
        - Dynamic metric computation
        - Cross-filtering support
        - Performance-optimized calculations
        - Client-specific formula customization
    
    Examples:
        >>> # Calculate individual agent productivity
        >>> tasa = await calculator.calcular_tasa_contactabilidad(
        ...     "Ana García", datetime(2024, 1, 1), datetime(2024, 1, 31)
        ... )
        >>> 
        >>> # Dashboard metrics for filtered view
        >>> filtros = {"servicio": "MOVIL", "cartera": "Gestión Temprana"}
        >>> metricas = await calculator.calcular_productividad_general(
        ...     filtros
        ... )
    """
    
    @abstractmethod
    async def calcular_tasa_contactabilidad(
        self, 
        ejecutivo: str, 
        fecha_inicio: datetime, 
        fecha_fin: datetime
    ) -> Metrica:
        """Calculate contact effectiveness rate for agent.
        
        Calculates the percentage of management actions that
        resulted in effective customer contact.
        
        Formula: (contactos_efectivos / total_gestiones) * 100
        
        Args:
            ejecutivo: Collection agent name
            fecha_inicio: Start date for calculation
            fecha_fin: End date for calculation
            
        Returns:
            Metrica with contact rate percentage
            
        Business Rules:
            - Effective contact excludes: NO_CONTACTO, NUMERO_ERRADO, 
              TELEFONO_APAGADO, BUZON_VOZ
            - Includes all channels (CALL, EMAIL, SMS, etc.)
            - Minimum 10 attempts required for reliable calculation
            
        Examples:
            >>> # Ana's contact rate this month
            >>> tasa = await calculator.calcular_tasa_contactabilidad(
            ...     "Ana García", 
            ...     datetime(2024, 6, 1), 
            ...     datetime(2024, 6, 30)
            ... )
            >>> print(f"Contact rate: {tasa.formato_display()}")
        """
        pass
        
    @abstractmethod
    async def calcular_pdps_por_hora(
        self, 
        ejecutivo: str, 
        fecha: date
    ) -> Metrica:
        """Calculate Promesas de Pago (PDPs) per hour.
        
        Calculates agent productivity in terms of payment
        commitments obtained per working hour.
        
        Formula: total_compromisos / horas_trabajadas
        
        Args:
            ejecutivo: Collection agent name
            fecha: Specific date for calculation
            
        Returns:
            Metrica with PDPs per hour rate
            
        Business Rules:
            - Counts only TipificacionHomologada.COMPROMISO_PAGO
            - Working hours calculated from first to last activity
            - Minimum 2 hours worked required for calculation
            - Excludes lunch breaks (automatic 1-hour deduction)
            
        Examples:
            >>> # Carlos's productivity today
            >>> pdps = await calculator.calcular_pdps_por_hora(
            ...     "Carlos López", date.today()
            ... )
            >>> if pdps.valor >= 2.0:
            ...     print("Excellent productivity!")
        """
        pass
        
    @abstractmethod
    async def calcular_productividad_general(
        self, 
        filtros: Dict[str, Any]
    ) -> List[Metrica]:
        """Calculate comprehensive productivity metrics.
        
        Calculates multiple productivity metrics based on
        applied filters for dashboard display.
        
        Args:
            filtros: Filtering criteria (ejecutivo, servicio, cartera, etc.)
            
        Returns:
            List of calculated metrics
            
        Standard Metrics Returned:
            - tasa_contactabilidad: Contact effectiveness rate
            - tasa_exito: Success rate (compromises / attempts)
            - pdps_totales: Total payment commitments
            - gestiones_totales: Total management actions
            - promedio_tiempo_gestion: Average action duration
            - distribucion_canales: Channel usage distribution
            
        Examples:
            >>> # Team performance for mobile service
            >>> filtros = {
            ...     "servicio": "MOVIL",
            ...     "fecha_inicio": datetime(2024, 6, 1),
            ...     "fecha_fin": datetime(2024, 6, 30)
            ... }
            >>> metricas = await calculator.calcular_productividad_general(
            ...     filtros
            ... )
            >>> for metrica in metricas:
            ...     print(f"{metrica.nombre}: {metrica.formato_display()}")
        """
        pass
    
    @abstractmethod
    async def calcular_efectividad_canal(
        self,
        canal: CanalContacto,
        fecha_inicio: datetime,
        fecha_fin: datetime
    ) -> Metrica:
        """Calculate channel effectiveness rate.
        
        Measures how effective each communication channel
        is at obtaining customer commitments.
        
        Formula: (compromisos_canal / gestiones_canal) * 100
        
        Args:
            canal: Communication channel to analyze
            fecha_inicio: Start date for calculation
            fecha_fin: End date for calculation
            
        Returns:
            Metrica with channel effectiveness rate
            
        Examples:
            >>> # WhatsApp effectiveness this month
            >>> efectividad = await calculator.calcular_efectividad_canal(
            ...     CanalContacto.WHATSAPP,
            ...     datetime(2024, 6, 1),
            ...     datetime(2024, 6, 30)
            ... )
        """
        pass
    
    @abstractmethod
    async def calcular_metricas_comparativas(
        self,
        periodo_actual: PeriodoMetrica,
        periodo_anterior: PeriodoMetrica,
        filtros: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Dict[str, Any]]:
        """Calculate comparative metrics between periods.
        
        Compares current period performance against previous
        period for trend analysis and performance monitoring.
        
        Args:
            periodo_actual: Current period configuration
            periodo_anterior: Previous period configuration
            filtros: Optional additional filters
            
        Returns:
            Dictionary with current vs previous metrics and changes
            
        Returns Structure:
            {
                "actual": {metric_name: value, ...},
                "anterior": {metric_name: value, ...},
                "cambios": {metric_name: percentage_change, ...},
                "tendencias": {metric_name: "up"|"down"|"stable", ...}
            }
            
        Examples:
            >>> # Month-over-month comparison
            >>> comparativa = await calculator.calcular_metricas_comparativas(
            ...     PeriodoMetrica.MENSUAL,
            ...     PeriodoMetrica.MENSUAL  # Previous month
            ... )
            >>> 
            >>> cambio_contactabilidad = comparativa["cambios"]["tasa_contactabilidad"]
            >>> if cambio_contactabilidad > 0:
            ...     print(f"Contact rate improved by {cambio_contactabilidad:.1f}%")
        """
        pass
    
    @abstractmethod
    async def calcular_ranking_ejecutivos(
        self,
        metrica: str,
        fecha_inicio: datetime,
        fecha_fin: datetime,
        limite: int = 10
    ) -> List[Dict[str, Any]]:
        """Calculate agent ranking by specific metric.
        
        Creates performance ranking of collection agents
        based on specified metric for competitive analysis.
        
        Args:
            metrica: Metric name for ranking ("tasa_contactabilidad", 
                    "pdps_totales", "tasa_exito")
            fecha_inicio: Start date for calculation
            fecha_fin: End date for calculation
            limite: Maximum number of agents in ranking
            
        Returns:
            List of agent performance data ordered by metric
            
        Return Structure:
            [
                {
                    "ejecutivo": "Agent Name",
                    "valor_metrica": 85.5,
                    "posicion": 1,
                    "gestiones_totales": 150,
                    "percentil": 95.2
                },
                ...
            ]
            
        Examples:
            >>> # Top 5 agents by contact rate this quarter
            >>> ranking = await calculator.calcular_ranking_ejecutivos(
            ...     "tasa_contactabilidad",
            ...     datetime(2024, 4, 1),
            ...     datetime(2024, 6, 30),
            ...     limite=5
            ... )
            >>> 
            >>> print("Top Performers:")
            >>> for agent in ranking:
            ...     print(f"{agent['posicion']}. {agent['ejecutivo']}: "
            ...           f"{agent['valor_metrica']:.1f}%")
        """
        pass
    
    @abstractmethod
    async def calcular_metricas_tiempo_real(self) -> Dict[str, Metrica]:
        """Calculate real-time metrics for live dashboards.
        
        Provides current-day metrics that update frequently
        for operational monitoring and live dashboards.
        
        Returns:
            Dictionary of real-time metrics
            
        Standard Real-time Metrics:
            - gestiones_hoy: Today's total actions
            - contactos_hoy: Today's effective contacts
            - compromisos_hoy: Today's commitments
            - tasa_exito_hoy: Today's success rate
            - ejecutivos_activos: Currently active agents
            - ultima_gestion: Time of last action
            
        Examples:
            >>> # Live dashboard update
            >>> metricas_live = await calculator.calcular_metricas_tiempo_real()
            >>> 
            >>> gestiones_hoy = metricas_live["gestiones_hoy"]
            >>> print(f"Actions today: {gestiones_hoy.formato_display()}")
        """
        pass
