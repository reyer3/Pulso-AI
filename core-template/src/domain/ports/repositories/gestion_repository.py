"""Gestion repository interface.

Defines the contract for Gestion entity persistence operations,
focused on debt collection activity tracking and analysis.
"""

from abc import abstractmethod
from typing import List, Optional, Dict, Any
from datetime import datetime, date

from .base_repository import BaseRepository
from ...entities.gestion import Gestion
from ...value_objects.enums import CanalContacto, TipificacionHomologada


class GestionRepository(BaseRepository[Gestion]):
    """Repository interface for Gestion entity operations.
    
    This interface defines all data access operations needed for
    collection activity management. Methods support performance
    analytics, agent productivity, and business intelligence use cases.
    
    Examples:
        >>> # Find successful collection activities
        >>> exitosas = await repo.find_gestiones_exitosas(
        ...     fecha_inicio=datetime(2025, 6, 1)
        ... )
        >>> 
        >>> # Get agent performance for specific date
        >>> gestiones = await repo.find_by_ejecutivo_and_date(
        ...     ejecutivo="Ana García",
        ...     fecha=date.today()
        ... )
    """
    
    @abstractmethod
    async def save_gestion(self, gestion: Gestion) -> str:
        """Save new collection activity.
        
        Args:
            gestion: Gestion entity to save
            
        Returns:
            Generated unique ID for the saved gestion
            
        Examples:
            >>> nueva_gestion = Gestion(...)
            >>> gestion_id = await repo.save_gestion(nueva_gestion)
            >>> print(f"Saved with ID: {gestion_id}")
        """
        pass
    
    @abstractmethod
    async def find_by_cliente(
        self,
        documento_cliente: str,
        limit: Optional[int] = None,
        order_by_fecha: bool = True
    ) -> List[Gestion]:
        """Find all collection activities for specific client.
        
        Args:
            documento_cliente: Client's document number
            limit: Maximum number of gestiones to return
            order_by_fecha: Whether to order by date (newest first)
            
        Returns:
            List of gestiones for the client
            
        Examples:
            >>> # Last 10 activities for client
            >>> gestiones = await repo.find_by_cliente(
            ...     "12345678",
            ...     limit=10
            ... )
        """
        pass
    
    @abstractmethod
    async def find_by_ejecutivo_and_date_range(
        self,
        ejecutivo: str,
        fecha_inicio: datetime,
        fecha_fin: datetime
    ) -> List[Gestion]:
        """Find agent's activities within date range.
        
        Args:
            ejecutivo: Agent name
            fecha_inicio: Start datetime (inclusive)
            fecha_fin: End datetime (inclusive)
            
        Returns:
            List of gestiones for agent in date range
            
        Examples:
            >>> # Agent's activities for today
            >>> today_start = datetime.combine(date.today(), datetime.min.time())
            >>> today_end = datetime.combine(date.today(), datetime.max.time())
            >>> gestiones = await repo.find_by_ejecutivo_and_date_range(
            ...     "Ana García",
            ...     today_start,
            ...     today_end
            ... )
        """
        pass
    
    @abstractmethod
    async def find_by_ejecutivo_and_date(
        self,
        ejecutivo: str,
        fecha: date
    ) -> List[Gestion]:
        """Find agent's activities for specific date.
        
        Args:
            ejecutivo: Agent name
            fecha: Specific date
            
        Returns:
            List of gestiones for agent on specified date
            
        Examples:
            >>> # Agent's today activities
            >>> gestiones = await repo.find_by_ejecutivo_and_date(
            ...     "Ana García",
            ...     date.today()
            ... )
        """
        pass
    
    @abstractmethod
    async def find_gestiones_exitosas(
        self,
        fecha_inicio: datetime,
        fecha_fin: Optional[datetime] = None
    ) -> List[Gestion]:
        """Find successful collection activities.
        
        Args:
            fecha_inicio: Start datetime
            fecha_fin: End datetime (if None, uses current time)
            
        Returns:
            List of successful gestiones (es_gestion_exitosa() == True)
            
        Examples:
            >>> # Successful activities in last 7 days
            >>> from datetime import timedelta
            >>> week_ago = datetime.now() - timedelta(days=7)
            >>> exitosas = await repo.find_gestiones_exitosas(week_ago)
        """
        pass
    
    @abstractmethod
    async def count_by_canal(
        self,
        canal: CanalContacto,
        fecha_inicio: Optional[datetime] = None,
        fecha_fin: Optional[datetime] = None
    ) -> int:
        """Count activities by communication channel.
        
        Args:
            canal: Communication channel to count
            fecha_inicio: Optional start datetime filter
            fecha_fin: Optional end datetime filter
            
        Returns:
            Number of gestiones using specified channel
            
        Examples:
            >>> # Total phone calls today
            >>> today_start = datetime.combine(date.today(), datetime.min.time())
            >>> calls_today = await repo.count_by_canal(
            ...     CanalContacto.CALL,
            ...     fecha_inicio=today_start
            ... )
        """
        pass
    
    @abstractmethod
    async def count_by_tipificacion(
        self,
        tipificacion: TipificacionHomologada,
        fecha_inicio: Optional[datetime] = None,
        fecha_fin: Optional[datetime] = None
    ) -> int:
        """Count activities by result tipification.
        
        Args:
            tipificacion: Result tipification to count
            fecha_inicio: Optional start datetime filter
            fecha_fin: Optional end datetime filter
            
        Returns:
            Number of gestiones with specified tipification
            
        Examples:
            >>> # Payment promises this month
            >>> month_start = datetime(2025, 6, 1)
            >>> promises = await repo.count_by_tipificacion(
            ...     TipificacionHomologada.COMPROMISO_PAGO,
            ...     fecha_inicio=month_start
            ... )
        """
        pass
    
    @abstractmethod
    async def get_ejecutivo_productivity(
        self,
        ejecutivo: str,
        fecha: date
    ) -> Dict[str, Any]:
        """Get comprehensive productivity metrics for agent.
        
        Args:
            ejecutivo: Agent name
            fecha: Date for metrics calculation
            
        Returns:
            Dictionary with productivity metrics
            
        Examples:
            >>> metrics = await repo.get_ejecutivo_productivity(
            ...     "Ana García",
            ...     date.today()
            ... )
            >>> # Returns: {
            >>> #     "total_gestiones": 45,
            >>> #     "contactos_efectivos": 32,
            >>> #     "compromisos": 18,
            >>> #     "tasa_contactabilidad": 71.1,
            >>> #     "tasa_conversion": 40.0,
            >>> #     "canales_usados": ["CALL", "WHATSAPP"]
            >>> # }
        """
        pass
    
    @abstractmethod
    async def find_by_tipificacion_homologada(
        self,
        tipificacion: TipificacionHomologada,
        fecha_inicio: datetime,
        fecha_fin: Optional[datetime] = None,
        limit: Optional[int] = None
    ) -> List[Gestion]:
        """Find activities by standardized tipification.
        
        Args:
            tipificacion: Standardized tipification
            fecha_inicio: Start datetime
            fecha_fin: End datetime (if None, uses current time)
            limit: Maximum number of gestiones to return
            
        Returns:
            List of gestiones with specified tipification
            
        Examples:
            >>> # All payment promises from last week
            >>> week_ago = datetime.now() - timedelta(days=7)
            >>> promises = await repo.find_by_tipificacion_homologada(
            ...     TipificacionHomologada.COMPROMISO_PAGO,
            ...     week_ago
            ... )
        """
        pass
    
    @abstractmethod
    async def get_daily_summary(
        self,
        fecha: date,
        ejecutivo: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get daily activity summary.
        
        Args:
            fecha: Date for summary
            ejecutivo: Optional agent filter
            
        Returns:
            Dictionary with daily metrics
            
        Examples:
            >>> # Overall daily summary
            >>> summary = await repo.get_daily_summary(date.today())
            >>> 
            >>> # Agent-specific summary
            >>> ana_summary = await repo.get_daily_summary(
            ...     date.today(),
            ...     ejecutivo="Ana García"
            ... )
        """
        pass
    
    @abstractmethod
    async def find_requiring_followup(
        self,
        fecha_limite: datetime,
        ejecutivo: Optional[str] = None
    ) -> List[Gestion]:
        """Find activities requiring follow-up action.
        
        Args:
            fecha_limite: Maximum date for follow-up
            ejecutivo: Optional agent filter
            
        Returns:
            List of gestiones needing follow-up
            
        Examples:
            >>> # Activities needing follow-up by end of week
            >>> friday = datetime(2025, 6, 6, 23, 59, 59)
            >>> followups = await repo.find_requiring_followup(friday)
        """
        pass
    
    @abstractmethod
    async def get_channel_performance(
        self,
        fecha_inicio: datetime,
        fecha_fin: Optional[datetime] = None
    ) -> Dict[str, Dict[str, Any]]:
        """Get performance metrics by communication channel.
        
        Args:
            fecha_inicio: Start datetime
            fecha_fin: End datetime (if None, uses current time)
            
        Returns:
            Dictionary with channel performance metrics
            
        Examples:
            >>> performance = await repo.get_channel_performance(
            ...     datetime(2025, 6, 1)
            ... )
            >>> # Returns: {
            >>> #     "CALL": {
            >>> #         "total_gestiones": 1500,
            >>> #         "contactos_efectivos": 1050,
            >>> #         "compromisos": 420,
            >>> #         "tasa_contactabilidad": 70.0,
            >>> #         "tasa_conversion": 28.0
            >>> #     },
            >>> #     "WHATSAPP": {...}
            >>> # }
        """
        pass
    
    @abstractmethod
    async def find_batch_by_cliente_list(
        self,
        documentos_clientes: List[str],
        fecha_inicio: Optional[datetime] = None,
        limit_per_cliente: Optional[int] = None
    ) -> Dict[str, List[Gestion]]:
        """Find activities for multiple clients efficiently.
        
        Args:
            documentos_clientes: List of client document numbers
            fecha_inicio: Optional start datetime filter
            limit_per_cliente: Maximum gestiones per client
            
        Returns:
            Dictionary mapping documento to list of gestiones
            
        Examples:
            >>> docs = ["12345678", "87654321"]
            >>> gestiones_map = await repo.find_batch_by_cliente_list(docs)
            >>> # Returns: {
            >>> #     "12345678": [gestion1, gestion2, ...],
            >>> #     "87654321": [gestion3, gestion4, ...]
            >>> # }
        """
        pass
