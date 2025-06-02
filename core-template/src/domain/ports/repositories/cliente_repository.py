"""Cliente repository interface.

Defines the contract for Cliente entity persistence operations,
focused on debt collection and customer management use cases.
"""

from abc import abstractmethod
from typing import List, Optional, Dict, Any
from datetime import datetime

from .base_repository import BaseRepository
from ...entities.cliente import Cliente
from ...value_objects.enums import PrioridadCobranza


class ClienteRepository(BaseRepository[Cliente]):
    """Repository interface for Cliente entity operations.
    
    This interface defines all data access operations needed for
    cliente management in the debt collection domain. The methods
    are designed to support common business use cases.
    
    Examples:
        >>> # Find clients with high debt and overdue status
        >>> clientes_criticos = await repo.find_clientes_en_mora(
        ...     dias_minimos=90,
        ...     saldo_minimo=5000.0
        ... )
        >>> 
        >>> # Get client by business key (documento)
        >>> cliente = await repo.find_by_documento("12345678")
    """
    
    @abstractmethod
    async def find_by_documento(self, documento: str) -> Optional[Cliente]:
        """Find cliente by identity document (business key).
        
        Args:
            documento: Client's identity document number
            
        Returns:
            Cliente if found, None otherwise
            
        Examples:
            >>> cliente = await repo.find_by_documento("12345678")
            >>> if cliente:
            ...     print(f"Found: {cliente.nombre}")
        """
        pass
    
    @abstractmethod
    async def find_clientes_en_mora(
        self,
        dias_minimos: int = 30,
        saldo_minimo: Optional[float] = None,
        limit: Optional[int] = None
    ) -> List[Cliente]:
        """Find clients with overdue debt.
        
        Args:
            dias_minimos: Minimum days overdue (default: 30)
            saldo_minimo: Minimum debt amount to include
            limit: Maximum number of clients to return
            
        Returns:
            List of clients matching criteria
            
        Examples:
            >>> # Critical clients: >90 days, >$5000 debt
            >>> criticos = await repo.find_clientes_en_mora(
            ...     dias_minimos=90,
            ...     saldo_minimo=5000.0
            ... )
        """
        pass
    
    @abstractmethod
    async def find_by_saldo_range(
        self,
        saldo_min: float,
        saldo_max: float,
        include_zero: bool = False
    ) -> List[Cliente]:
        """Find clients within specific debt amount range.
        
        Args:
            saldo_min: Minimum debt amount (inclusive)
            saldo_max: Maximum debt amount (inclusive)
            include_zero: Whether to include clients with zero debt
            
        Returns:
            List of clients with debt in specified range
            
        Examples:
            >>> # Medium debt clients: $1000-$5000
            >>> medios = await repo.find_by_saldo_range(1000.0, 5000.0)
        """
        pass
    
    @abstractmethod
    async def find_by_prioridad(
        self,
        prioridad: PrioridadCobranza,
        limit: Optional[int] = None
    ) -> List[Cliente]:
        """Find clients by collection priority level.
        
        Args:
            prioridad: Priority level to filter by
            limit: Maximum number of clients to return
            
        Returns:
            List of clients with specified priority
            
        Note:
            Priority is calculated using cliente.calcular_prioridad_cobranza()
        """
        pass
    
    @abstractmethod
    async def find_contactables(self, only_with_phone: bool = False) -> List[Cliente]:
        """Find clients with available contact information.
        
        Args:
            only_with_phone: If True, only include clients with phone numbers
            
        Returns:
            List of contactable clients
            
        Examples:
            >>> # All contactable clients (phone or email)
            >>> contactables = await repo.find_contactables()
            >>> 
            >>> # Only clients with phone numbers
            >>> con_telefono = await repo.find_contactables(only_with_phone=True)
        """
        pass
    
    @abstractmethod
    async def count_clientes_activos(self) -> int:
        """Count total active clients (with current debt).
        
        Returns:
            Number of clients with saldo_actual > 0
            
        Examples:
            >>> total = await repo.count_clientes_activos()
            >>> print(f"Active clients: {total}")
        """
        pass
    
    @abstractmethod
    async def count_by_mora_ranges(self) -> Dict[str, int]:
        """Count clients grouped by overdue day ranges.
        
        Returns:
            Dictionary with ranges as keys and counts as values
            
        Examples:
            >>> ranges = await repo.count_by_mora_ranges()
            >>> # Returns: {
            >>> #     "0-30": 1500,
            >>> #     "31-60": 800, 
            >>> #     "61-90": 400,
            >>> #     "90+": 200
            >>> # }
        """
        pass
    
    @abstractmethod
    async def find_top_debtors(
        self,
        limit: int = 100,
        min_amount: Optional[float] = None
    ) -> List[Cliente]:
        """Find clients with highest debt amounts.
        
        Args:
            limit: Maximum number of clients to return
            min_amount: Minimum debt amount to consider
            
        Returns:
            List of clients ordered by debt amount (descending)
            
        Examples:
            >>> # Top 50 debtors with at least $10,000 debt
            >>> top_debtors = await repo.find_top_debtors(
            ...     limit=50,
            ...     min_amount=10000.0
            ... )
        """
        pass
    
    @abstractmethod
    async def find_recently_updated(
        self,
        hours: int = 24,
        limit: Optional[int] = None
    ) -> List[Cliente]:
        """Find clients updated within specified time frame.
        
        Args:
            hours: Number of hours to look back
            limit: Maximum number of clients to return
            
        Returns:
            List of recently updated clients
            
        Examples:
            >>> # Clients updated in last 6 hours
            >>> recent = await repo.find_recently_updated(hours=6)
        """
        pass
    
    @abstractmethod
    async def search_by_name(
        self,
        name_pattern: str,
        limit: Optional[int] = None
    ) -> List[Cliente]:
        """Search clients by name pattern.
        
        Args:
            name_pattern: Name pattern to search (supports wildcards)
            limit: Maximum number of clients to return
            
        Returns:
            List of clients matching name pattern
            
        Examples:
            >>> # Find all clients named "Juan"
            >>> juanes = await repo.search_by_name("Juan%")
        """
        pass
    
    @abstractmethod
    async def get_portfolio_summary(self) -> Dict[str, Any]:
        """Get overall portfolio summary statistics.
        
        Returns:
            Dictionary with portfolio metrics
            
        Examples:
            >>> summary = await repo.get_portfolio_summary()
            >>> # Returns: {
            >>> #     "total_clients": 10000,
            >>> #     "total_debt": 50000000.0,
            >>> #     "avg_debt": 5000.0,
            >>> #     "clients_in_mora": 3500,
            >>> #     "contactable_clients": 8500
            >>> # }
        """
        pass
    
    @abstractmethod
    async def find_batch_by_documentos(
        self,
        documentos: List[str]
    ) -> List[Cliente]:
        """Find multiple clients by their documents in single query.
        
        Args:
            documentos: List of document numbers to find
            
        Returns:
            List of found clients (may be fewer than requested)
            
        Examples:
            >>> docs = ["12345678", "87654321", "11111111"]
            >>> clientes = await repo.find_batch_by_documentos(docs)
        """
        pass
