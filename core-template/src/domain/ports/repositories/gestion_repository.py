"""Gestion repository interface.

Defines contracts for Gestion entity persistence and queries.
Focused on collection management actions and productivity tracking.
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from datetime import datetime, date

from ...entities.gestion import Gestion
from ...value_objects.enums import CanalContacto, TipificacionHomologada
from .base_repository import BaseRepository


class GestionRepository(BaseRepository[Gestion, str], ABC):
    """Repository interface for Gestion entity persistence.
    
    This interface defines all data access operations needed
    for collection management tracking and productivity analysis.
    
    Key Features:
        - Collection activity tracking
        - Productivity metrics calculation
        - Multi-dimensional filtering (ejecutivo, canal, fecha)
        - Real-time dashboard support
    
    Examples:
        >>> # Daily productivity tracking
        >>> gestiones_hoy = await repo.find_by_ejecutivo_and_date_range(
        ...     "Ana García", datetime.today(), datetime.today()
        ... )
        >>> 
        >>> # Success rate analysis
        >>> exitosas = await repo.find_gestiones_exitosas(
        ...     datetime.now() - timedelta(days=30)
        ... )
    """
    
    @abstractmethod
    async def save_gestion(self, gestion: Gestion) -> str:
        """Save new collection management action.
        
        Persists a new collection activity record.
        Generates unique ID for tracking purposes.
        
        Args:
            gestion: Management action to save
            
        Returns:
            Generated ID for the saved gestion
            
        Raises:
            RepositoryError: If save operation fails
            ValidationError: If gestion data is invalid
            
        Examples:
            >>> gestion = Gestion(
            ...     documento_cliente="12345678",
            ...     fecha=datetime.now(),
            ...     canal=CanalContacto.CALL,
            ...     ejecutivo="Ana García",
            ...     tipificacion_original="CONT_COMP",
            ...     tipificacion_homologada=TipificacionHomologada.COMPROMISO_PAGO,
            ...     es_contacto=True,
            ...     es_compromiso=True
            ... )
            >>> gestion_id = await repo.save_gestion(gestion)
        """
        pass
    
    @abstractmethod
    async def find_by_cliente(self, documento_cliente: str) -> List[Gestion]:
        """Get all management actions for a customer.
        
        Returns complete history of collection activities
        for a specific customer, ordered by fecha DESC.
        
        Args:
            documento_cliente: Customer document number
            
        Returns:
            List of management actions for customer
            
        Examples:
            >>> # Customer interaction history
            >>> historial = await repo.find_by_cliente("12345678")
            >>> ultima_gestion = historial[0] if historial else None
        """
        pass
        
    @abstractmethod
    async def find_by_ejecutivo_and_date_range(
        self, 
        ejecutivo: str, 
        fecha_inicio: datetime, 
        fecha_fin: datetime
    ) -> List[Gestion]:
        """Get management actions by agent and date range.
        
        Critical query for productivity tracking and daily reports.
        Returns all activities performed by specific agent in date range.
        
        Args:
            ejecutivo: Name of the collection agent
            fecha_inicio: Start date (inclusive)
            fecha_fin: End date (inclusive)
            
        Returns:
            List of management actions in date range
            
        Business Rules:
            - Includes all tipification types
            - Ordered by fecha ASC (chronological)
            - Used for daily/weekly productivity reports
            
        Examples:
            >>> # Today's work for Ana García
            >>> hoy = datetime.now().date()
            >>> gestiones_hoy = await repo.find_by_ejecutivo_and_date_range(
            ...     "Ana García", 
            ...     datetime.combine(hoy, datetime.min.time()),
            ...     datetime.combine(hoy, datetime.max.time())
            ... )
            >>> 
            >>> # Weekly performance
            >>> semana_pasada = await repo.find_by_ejecutivo_and_date_range(
            ...     "Carlos López", 
            ...     datetime.now() - timedelta(days=7),
            ...     datetime.now()
            ... )
        """
        pass
        
    @abstractmethod
    async def find_gestiones_exitosas(
        self, 
        fecha_inicio: datetime,
        ejecutivo: Optional[str] = None
    ) -> List[Gestion]:
        """Find successful management actions since date.
        
        Returns management actions that resulted in customer
        commitment or payment. Used for success rate calculation.
        
        Args:
            fecha_inicio: Start date for search
            ejecutivo: Optional agent filter
            
        Returns:
            List of successful management actions
            
        Business Rules:
            - Success = es_contacto AND es_compromiso
            - Includes COMPROMISO_PAGO, PAGO_INMEDIATO, ACUERDO_PAGO
            - Excludes NO_CONTACTO, NO_INTERESADO
            
        Examples:
            >>> # All successful actions this month
            >>> mes_inicio = datetime.now().replace(day=1)
            >>> exitosas = await repo.find_gestiones_exitosas(mes_inicio)
            >>> 
            >>> # Ana's successful actions
            >>> ana_exitosas = await repo.find_gestiones_exitosas(
            ...     mes_inicio, ejecutivo="Ana García"
            ... )
        """
        pass
        
    @abstractmethod
    async def count_by_canal(self, canal: CanalContacto) -> int:
        """Count management actions by communication channel.
        
        Returns total number of activities performed via
        specific communication channel.
        
        Args:
            canal: Communication channel to count
            
        Returns:
            Number of actions via specified channel
            
        Examples:
            >>> # How many calls were made?
            >>> total_calls = await repo.count_by_canal(CanalContacto.CALL)
            >>> 
            >>> # Digital channel usage
            >>> emails = await repo.count_by_canal(CanalContacto.EMAIL)
            >>> sms = await repo.count_by_canal(CanalContacto.SMS)
        """
        pass
    
    @abstractmethod
    async def find_by_tipificacion(
        self,
        tipificacion: TipificacionHomologada,
        fecha_inicio: Optional[datetime] = None,
        fecha_fin: Optional[datetime] = None
    ) -> List[Gestion]:
        """Find management actions by tipification.
        
        Returns actions with specific homologated tipification.
        Used for outcome analysis and process improvement.
        
        Args:
            tipificacion: Homologated tipification to filter by
            fecha_inicio: Optional start date filter
            fecha_fin: Optional end date filter
            
        Returns:
            List of actions with specified tipification
            
        Examples:
            >>> # All payment commitments this week
            >>> compromisos = await repo.find_by_tipificacion(
            ...     TipificacionHomologada.COMPROMISO_PAGO,
            ...     datetime.now() - timedelta(days=7)
            ... )
        """
        pass
    
    @abstractmethod
    async def get_estadisticas_productividad(
        self,
        ejecutivo: Optional[str] = None,
        fecha_inicio: Optional[datetime] = None,
        fecha_fin: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """Get productivity statistics.
        
        Returns comprehensive productivity metrics for
        dashboard and performance analysis.
        
        Args:
            ejecutivo: Optional agent filter
            fecha_inicio: Optional start date
            fecha_fin: Optional end date
            
        Returns:
            Dictionary with productivity stats:
            - total_gestiones: Total management actions
            - gestiones_exitosas: Successful actions count
            - tasa_exito: Success rate percentage
            - contactos_efectivos: Effective contacts count
            - tasa_contactabilidad: Contact rate percentage
            - distribucion_canales: Actions by channel
            - distribucion_tipificaciones: Actions by tipification
            - promedio_gestiones_diarias: Daily average
            
        Examples:
            >>> # Overall team performance this month
            >>> stats = await repo.get_estadisticas_productividad(
            ...     fecha_inicio=datetime.now().replace(day=1)
            ... )
            >>> print(f"Success rate: {stats['tasa_exito']:.1f}%")
            >>> 
            >>> # Individual agent performance
            >>> ana_stats = await repo.get_estadisticas_productividad(
            ...     ejecutivo="Ana García",
            ...     fecha_inicio=datetime.now() - timedelta(days=30)
            ... )
        """
        pass
    
    @abstractmethod
    async def find_compromisos_vencidos(
        self,
        fecha_corte: Optional[datetime] = None
    ) -> List[Gestion]:
        """Find overdue payment commitments.
        
        Returns management actions where customer committed
        to payment but the commitment date has passed.
        
        Args:
            fecha_corte: Cut-off date (default: now)
            
        Returns:
            List of overdue commitments requiring follow-up
            
        Business Rules:
            - Must have es_compromiso = True
            - fecha_compromiso < fecha_corte
            - No subsequent payment recorded
            
        Examples:
            >>> # All overdue commitments
            >>> vencidos = await repo.find_compromisos_vencidos()
            >>> 
            >>> # Commitments overdue as of yesterday
            >>> ayer = datetime.now() - timedelta(days=1)
            >>> vencidos_ayer = await repo.find_compromisos_vencidos(ayer)
        """
        pass
    
    @abstractmethod
    async def find_by_multiple_criteria(
        self,
        ejecutivo: Optional[str] = None,
        canal: Optional[CanalContacto] = None,
        es_contacto: Optional[bool] = None,
        es_compromiso: Optional[bool] = None,
        fecha_inicio: Optional[datetime] = None,
        fecha_fin: Optional[datetime] = None,
        limit: Optional[int] = None
    ) -> List[Gestion]:
        """Find management actions by multiple criteria.
        
        Flexible query method supporting multiple filters
        for complex dashboard requirements and analysis.
        
        Args:
            ejecutivo: Agent name filter
            canal: Communication channel filter
            es_contacto: Contact made filter
            es_compromiso: Commitment obtained filter
            fecha_inicio: Start date filter
            fecha_fin: End date filter
            limit: Maximum results
            
        Returns:
            List of filtered management actions
            
        Examples:
            >>> # Ana's successful calls this week
            >>> ana_calls = await repo.find_by_multiple_criteria(
            ...     ejecutivo="Ana García",
            ...     canal=CanalContacto.CALL,
            ...     es_contacto=True,
            ...     fecha_inicio=datetime.now() - timedelta(days=7)
            ... )
        """
        pass
    
    @abstractmethod
    async def get_metricas_tiempo_real(self) -> Dict[str, Any]:
        """Get real-time metrics for live dashboard.
        
        Returns current day metrics that update in real-time
        for operational dashboards and monitoring.
        
        Returns:
            Dictionary with real-time metrics:
            - gestiones_hoy: Today's total actions
            - contactos_hoy: Today's effective contacts
            - compromisos_hoy: Today's commitments obtained
            - ejecutivos_activos: Number of active agents
            - ultima_actualizacion: Last update timestamp
            
        Examples:
            >>> # Live dashboard update
            >>> metricas = await repo.get_metricas_tiempo_real()
            >>> print(f"Today: {metricas['gestiones_hoy']} actions, "
            ...       f"{metricas['compromisos_hoy']} commitments")
        """
        pass
