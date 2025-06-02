"""Metrica calculator service interface.

Defines the contract for business metrics calculation operations.
This service handles complex calculations that require data from
multiple sources and business rule application.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from datetime import datetime, date

from ...entities.metrica import Metrica
from ...value_objects.enums import CanalContacto, TipificacionHomologada


class MetricaCalculatorService(ABC):
    """Service interface for business metrics calculation.
    
    This service encapsulates complex business logic for calculating
    key performance indicators (KPIs) used in debt collection dashboards.
    All calculations follow business rules defined in domain entities.
    
    Examples:
        >>> # Calculate agent performance for specific date
        >>> tasa = await calculator.calcular_tasa_contactabilidad(
        ...     ejecutivo="Ana García",
        ...     fecha_inicio=datetime(2025, 6, 1, 8, 0),
        ...     fecha_fin=datetime(2025, 6, 1, 18, 0)
        ... )
        >>> print(f"Contactability rate: {tasa.valor}%")
    """
    
    @abstractmethod
    async def calcular_tasa_contactabilidad(
        self,
        ejecutivo: str,
        fecha_inicio: datetime,
        fecha_fin: datetime,
        canales: Optional[List[CanalContacto]] = None
    ) -> Metrica:
        """Calculate contactability rate for agent in time period.
        
        Business Rule: (contactos_efectivos / total_gestiones) * 100
        
        Args:
            ejecutivo: Agent name
            fecha_inicio: Start datetime for calculation
            fecha_fin: End datetime for calculation  
            canales: Optional list of channels to include
            
        Returns:
            Metrica with contactability percentage
            
        Examples:
            >>> # Agent's contactability for today
            >>> today_start = datetime.combine(date.today(), datetime.min.time())
            >>> today_end = datetime.combine(date.today(), datetime.max.time())
            >>> tasa = await calculator.calcular_tasa_contactabilidad(
            ...     "Ana García",
            ...     today_start,
            ...     today_end
            ... )
            >>> assert tasa.nombre == "tasa_contactabilidad"
            >>> assert tasa.unidad == "%"
        """
        pass
    
    @abstractmethod
    async def calcular_pdps_por_hora(
        self,
        ejecutivo: str,
        fecha: date,
        horas_trabajadas: Optional[float] = None
    ) -> Metrica:
        """Calculate PDPs (Payment Promises) per hour for agent.
        
        Business Rule: total_compromisos / horas_trabajadas
        
        Args:
            ejecutivo: Agent name
            fecha: Date for calculation
            horas_trabajadas: Optional working hours (default: calculate from gestiones)
            
        Returns:
            Metrica with PDPs per hour rate
            
        Examples:
            >>> # Agent's PDPs/hour for today
            >>> pdps = await calculator.calcular_pdps_por_hora(
            ...     "Ana García",
            ...     date.today(),
            ...     horas_trabajadas=8.0
            ... )
            >>> assert pdps.nombre == "pdps_por_hora"
            >>> assert pdps.unidad == "count/hour"
        """
        pass
    
    @abstractmethod
    async def calcular_tasa_conversion(
        self,
        ejecutivo: str,
        fecha_inicio: datetime,
        fecha_fin: datetime,
        tipo_conversion: str = "compromiso"
    ) -> Metrica:
        """Calculate conversion rate for agent.
        
        Business Rule: (conversiones / contactos_efectivos) * 100
        
        Args:
            ejecutivo: Agent name
            fecha_inicio: Start datetime
            fecha_fin: End datetime
            tipo_conversion: Type of conversion ("compromiso", "pago", "acuerdo")
            
        Returns:
            Metrica with conversion percentage
            
        Examples:
            >>> # Promise conversion rate
            >>> conversion = await calculator.calcular_tasa_conversion(
            ...     "Ana García",
            ...     week_start,
            ...     week_end,
            ...     tipo_conversion="compromiso"
            ... )
        """
        pass
    
    @abstractmethod
    async def calcular_productividad_general(
        self,
        filtros: Dict[str, Any],
        metricas_requeridas: Optional[List[str]] = None
    ) -> List[Metrica]:
        """Calculate multiple productivity metrics with filters.
        
        Args:
            filtros: Dictionary with filtering criteria
            metricas_requeridas: Optional list of specific metrics to calculate
            
        Returns:
            List of calculated metrics
            
        Examples:
            >>> filtros = {
            ...     "ejecutivos": ["Ana García", "Carlos Ruiz"],
            ...     "fecha_inicio": datetime(2025, 6, 1),
            ...     "fecha_fin": datetime(2025, 6, 7),
            ...     "canales": [CanalContacto.CALL, CanalContacto.WHATSAPP]
            ... }
            >>> metricas = await calculator.calcular_productividad_general(filtros)
        """
        pass
    
    @abstractmethod
    async def calcular_metricas_por_canal(
        self,
        canal: CanalContacto,
        fecha_inicio: datetime,
        fecha_fin: datetime
    ) -> List[Metrica]:
        """Calculate performance metrics by communication channel.
        
        Args:
            canal: Communication channel
            fecha_inicio: Start datetime
            fecha_fin: End datetime
            
        Returns:
            List of channel-specific metrics
            
        Examples:
            >>> # WhatsApp performance metrics
            >>> metricas = await calculator.calcular_metricas_por_canal(
            ...     CanalContacto.WHATSAPP,
            ...     month_start,
            ...     month_end
            ... )
        """
        pass
    
    @abstractmethod
    async def calcular_metricas_cliente(
        self,
        documento_cliente: str,
        fecha_inicio: Optional[datetime] = None
    ) -> List[Metrica]:
        """Calculate metrics specific to a client.
        
        Args:
            documento_cliente: Client document number
            fecha_inicio: Optional start date (default: all time)
            
        Returns:
            List of client-specific metrics
            
        Examples:
            >>> # Client collection metrics
            >>> metricas = await calculator.calcular_metricas_cliente(
            ...     "12345678",
            ...     fecha_inicio=datetime(2025, 1, 1)
            ... )
        """
        pass
    
    @abstractmethod
    async def calcular_ranking_ejecutivos(
        self,
        metrica_nombre: str,
        fecha_inicio: datetime,
        fecha_fin: datetime,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Calculate ranking of agents by specific metric.
        
        Args:
            metrica_nombre: Name of metric to rank by
            fecha_inicio: Start datetime
            fecha_fin: End datetime
            limit: Number of top agents to return
            
        Returns:
            List of agent rankings with metric values
            
        Examples:
            >>> # Top 10 agents by contactability
            >>> ranking = await calculator.calcular_ranking_ejecutivos(
            ...     "tasa_contactabilidad",
            ...     week_start,
            ...     week_end,
            ...     limit=10
            ... )
            >>> # Returns: [
            >>> #     {"ejecutivo": "Ana García", "valor": 85.5, "posicion": 1},
            >>> #     {"ejecutivo": "Carlos Ruiz", "valor": 82.1, "posicion": 2},
            >>> #     ...
            >>> # ]
        """
        pass
    
    @abstractmethod
    async def calcular_tendencias(
        self,
        metrica_nombre: str,
        ejecutivo: Optional[str],
        dias_historicos: int = 30,
        agrupacion: str = "daily"
    ) -> List[Metrica]:
        """Calculate metric trends over time.
        
        Args:
            metrica_nombre: Name of metric to analyze
            ejecutivo: Optional agent filter
            dias_historicos: Number of historical days
            agrupacion: Grouping period ("daily", "weekly", "monthly")
            
        Returns:
            List of metrics showing trend over time
            
        Examples:
            >>> # Daily contactability trend for last 30 days
            >>> tendencia = await calculator.calcular_tendencias(
            ...     "tasa_contactabilidad",
            ...     ejecutivo="Ana García",
            ...     dias_historicos=30,
            ...     agrupacion="daily"
            ... )
        """
        pass
    
    @abstractmethod
    async def calcular_benchmarks(
        self,
        metrica_nombre: str,
        fecha_inicio: datetime,
        fecha_fin: datetime
    ) -> Dict[str, float]:
        """Calculate benchmark values for a metric.
        
        Args:
            metrica_nombre: Name of metric
            fecha_inicio: Start datetime
            fecha_fin: End datetime
            
        Returns:
            Dictionary with benchmark statistics
            
        Examples:
            >>> benchmarks = await calculator.calcular_benchmarks(
            ...     "tasa_contactabilidad",
            ...     month_start,
            ...     month_end
            ... )
            >>> # Returns: {
            >>> #     "promedio": 72.5,
            >>> #     "mediana": 74.0,
            >>> #     "percentil_75": 80.0,
            >>> #     "percentil_90": 85.0,
            >>> #     "maximo": 92.0,
            >>> #     "minimo": 45.0
            >>> # }
        """
        pass
    
    @abstractmethod
    async def validar_metrica(
        self,
        metrica: Metrica,
        reglas_negocio: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Validate calculated metric against business rules.
        
        Args:
            metrica: Calculated metric to validate
            reglas_negocio: Optional business rules override
            
        Returns:
            True if metric is valid, False otherwise
            
        Examples:
            >>> metrica = Metrica(
            ...     nombre="tasa_contactabilidad",
            ...     valor=95.0,
            ...     unidad="%",
            ...     periodo="daily",
            ...     fecha_calculo=datetime.now(),
            ...     filtros_aplicados={}
            ... )
            >>> is_valid = await calculator.validar_metrica(metrica)
        """
        pass
