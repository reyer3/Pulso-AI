"""Cliente repository interface.

Defines contracts for Cliente entity persistence and queries.
Focused on business needs for debt collection and customer management.
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from datetime import datetime, date

from ...entities.cliente import Cliente
from ...value_objects.enums import PrioridadCobranza
from .base_repository import BaseRepository


class ClienteRepository(BaseRepository[Cliente, str], ABC):
    """Repository interface for Cliente entity persistence.
    
    This interface defines all data access operations needed
    for customer management in the debt collection system.
    Each method reflects real business requirements.
    
    Key Features:
        - Business-focused query methods
        - Async operations for performance
        - Type-safe with full annotations
        - Client-agnostic (works with any data source)
    
    Examples:
        >>> # Usage in application layer
        >>> clientes_mora = await cliente_repo.find_clientes_en_mora(30)
        >>> clientes_alta_prioridad = await cliente_repo.find_by_prioridad(
        ...     PrioridadCobranza.ALTA
        ... )
        
        >>> # Multi-client usage (same interface, different adapters)
        >>> # Movistar (BigQuery)
        >>> movistar_clientes = await bigquery_repo.find_by_saldo_range(1000, 5000)
        >>> # Claro (PostgreSQL) 
        >>> claro_clientes = await postgres_repo.find_by_saldo_range(1000, 5000)
    """
    
    @abstractmethod
    async def find_by_documento(self, documento: str) -> Optional[Cliente]:
        """Find cliente by identity document.
        
        Primary method for customer lookup. Document number
        is the business key for customer identification.
        
        Args:
            documento: Customer identity document number
            
        Returns:
            Cliente if found, None otherwise
            
        Examples:
            >>> cliente = await repo.find_by_documento("12345678")
            >>> if cliente:
            ...     print(f"Found: {cliente.nombre}, debt: ${cliente.saldo_actual}")
        """
        pass
    
    @abstractmethod
    async def find_clientes_en_mora(
        self, 
        dias_minimos: int = 30,
        limit: Optional[int] = None
    ) -> List[Cliente]:
        """Find customers with overdue debt.
        
        Critical query for collection operations. Returns customers
        whose debt is overdue beyond the specified threshold.
        
        Args:
            dias_minimos: Minimum days overdue to include
            limit: Maximum number of results
            
        Returns:
            List of overdue customers
            
        Business Rules:
            - Default 30 days for standard mora definition
            - Results ordered by days_mora DESC (most urgent first)
            - Excludes customers with estado = EXCLUIDO or PAGADO
            
        Examples:
            >>> # Standard overdue customers
            >>> mora_30 = await repo.find_clientes_en_mora(30)
            >>> 
            >>> # Critical cases (90+ days)
            >>> criticos = await repo.find_clientes_en_mora(90, limit=100)
        """
        pass
        
    @abstractmethod
    async def find_by_saldo_range(
        self, 
        saldo_min: float, 
        saldo_max: float
    ) -> List[Cliente]:
        """Find customers within debt amount range.
        
        Used for segmentation and prioritization strategies.
        Helps identify high-value vs small-debt customers.
        
        Args:
            saldo_min: Minimum debt amount (inclusive)
            saldo_max: Maximum debt amount (inclusive)
            
        Returns:
            List of customers in debt range
            
        Examples:
            >>> # High-value customers
            >>> high_debt = await repo.find_by_saldo_range(5000.0, 50000.0)
            >>> 
            >>> # Small debt customers
            >>> small_debt = await repo.find_by_saldo_range(100.0, 1000.0)
        """
        pass
        
    @abstractmethod
    async def count_clientes_activos(self) -> int:
        """Count customers with active debt.
        
        Returns total number of customers currently in
        the collection process (excluding paid/excluded).
        
        Returns:
            Number of active customers
            
        Business Rules:
            - Includes only customers with saldo_actual > 0
            - Excludes PAGADO, CASTIGADO, EXCLUIDO statuses
            
        Examples:
            >>> total_activos = await repo.count_clientes_activos()
            >>> print(f"Managing {total_activos} active customers")
        """
        pass
    
    @abstractmethod
    async def find_by_prioridad(
        self, 
        prioridad: PrioridadCobranza,
        limit: Optional[int] = None
    ) -> List[Cliente]:
        """Find customers by collection priority.
        
        Returns customers matching specified priority level.
        Used for daily work assignment and resource allocation.
        
        Args:
            prioridad: Collection priority level
            limit: Maximum number of results
            
        Returns:
            List of customers with specified priority
            
        Examples:
            >>> # Today's high priority work
            >>> alta_prioridad = await repo.find_by_prioridad(
            ...     PrioridadCobranza.ALTA, limit=50
            ... )
        """
        pass
    
    @abstractmethod
    async def find_contactables(
        self,
        incluir_solo_telefono: bool = False
    ) -> List[Cliente]:
        """Find customers with valid contact information.
        
        Returns customers who can be contacted via phone or email.
        Critical for planning outbound campaigns.
        
        Args:
            incluir_solo_telefono: If True, require phone number
            
        Returns:
            List of contactable customers
            
        Business Rules:
            - Must have phone OR email (unless incluir_solo_telefono=True)
            - Contact info must be non-empty and properly formatted
            - Excludes customers who requested no contact
            
        Examples:
            >>> # All contactable customers
            >>> contactables = await repo.find_contactables()
            >>> 
            >>> # Only customers with phone for call campaigns
            >>> telefono_disponible = await repo.find_contactables(
            ...     incluir_solo_telefono=True
            ... )
        """
        pass
    
    @abstractmethod
    async def find_by_rango_dias_mora(
        self,
        dias_min: int,
        dias_max: int
    ) -> List[Cliente]:
        """Find customers within specific overdue days range.
        
        Used for creating targeted collection strategies
        based on debt age segmentation.
        
        Args:
            dias_min: Minimum days overdue (inclusive)
            dias_max: Maximum days overdue (inclusive)
            
        Returns:
            List of customers in overdue range
            
        Examples:
            >>> # Recent overdue (early intervention)
            >>> recientes = await repo.find_by_rango_dias_mora(1, 30)
            >>> 
            >>> # Medium term overdue
            >>> mediano_plazo = await repo.find_by_rango_dias_mora(31, 90)
            >>> 
            >>> # Long term overdue (pre-legal)
            >>> largo_plazo = await repo.find_by_rango_dias_mora(91, 180)
        """
        pass
    
    @abstractmethod
    async def find_top_deudores(
        self,
        limite: int = 100
    ) -> List[Cliente]:
        """Find customers with highest debt amounts.
        
        Returns top debtors ordered by saldo_actual DESC.
        Used for prioritizing high-value collection efforts.
        
        Args:
            limite: Maximum number of top debtors to return
            
        Returns:
            List of top debtors
            
        Examples:
            >>> # Top 50 debtors for management attention
            >>> top_deudores = await repo.find_top_deudores(50)
            >>> total_debt = sum(c.saldo_actual for c in top_deudores)
        """
        pass
    
    @abstractmethod
    async def find_sin_gestion_reciente(
        self,
        dias_sin_gestion: int = 30
    ) -> List[Cliente]:
        """Find customers without recent management actions.
        
        Returns customers who haven't been contacted recently.
        Important for ensuring comprehensive coverage.
        
        Args:
            dias_sin_gestion: Days since last management action
            
        Returns:
            List of customers without recent contact
            
        Examples:
            >>> # Customers not contacted in 30 days
            >>> sin_atencion = await repo.find_sin_gestion_reciente(30)
        """
        pass
    
    @abstractmethod
    async def update_ultimo_contacto(
        self,
        documento: str,
        fecha_contacto: datetime
    ) -> bool:
        """Update customer's last contact date.
        
        Updates the last contact timestamp for tracking
        recency of collection activities.
        
        Args:
            documento: Customer document number
            fecha_contacto: Date/time of last contact
            
        Returns:
            True if update successful
            
        Examples:
            >>> # Update after successful contact
            >>> await repo.update_ultimo_contacto(
            ...     "12345678", datetime.now()
            ... )
        """
        pass
    
    @abstractmethod
    async def get_estadisticas_mora(self) -> Dict[str, Any]:
        """Get overdue debt statistics.
        
        Returns comprehensive statistics about overdue customers
        for dashboard and reporting purposes.
        
        Returns:
            Dictionary with statistics:
            - total_clientes: Total active customers
            - clientes_en_mora: Customers with overdue debt
            - promedio_dias_mora: Average days overdue
            - total_saldo_mora: Total overdue debt amount
            - distribucion_mora: Distribution by mora ranges
            
        Examples:
            >>> stats = await repo.get_estadisticas_mora()
            >>> print(f"Overdue rate: {stats['clientes_en_mora'] / stats['total_clientes']:.1%}")
        """
        pass
