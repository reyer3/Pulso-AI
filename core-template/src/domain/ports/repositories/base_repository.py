"""Base repository interface with common patterns.

Provides common repository operations that can be inherited
by specific entity repositories. Follows Repository pattern
with async support for high-performance data access.
"""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List, Optional, Dict, Any
from datetime import datetime

# Generic type for entities
T = TypeVar('T')
ID = TypeVar('ID')


class BaseRepository(Generic[T, ID], ABC):
    """Base repository interface with common CRUD operations.
    
    This interface provides standard data access patterns
    that can be inherited by entity-specific repositories.
    
    Type Parameters:
        T: Entity type (e.g., Cliente, Gestion)
        ID: Identifier type (e.g., str, int)
    
    Examples:
        >>> class ClienteRepository(BaseRepository[Cliente, str]):
        ...     # Inherits common methods, adds specific ones
        ...     async def find_by_documento(self, doc: str) -> Optional[Cliente]:
        ...         # Specific implementation
        ...         pass
    """
    
    @abstractmethod
    async def find_by_id(self, entity_id: ID) -> Optional[T]:
        """Find entity by its primary identifier.
        
        Args:
            entity_id: Primary key of the entity
            
        Returns:
            Entity if found, None otherwise
            
        Raises:
            RepositoryError: If data access fails
        """
        pass
    
    @abstractmethod
    async def find_all(
        self, 
        limit: Optional[int] = None,
        offset: Optional[int] = None
    ) -> List[T]:
        """Find all entities with optional pagination.
        
        Args:
            limit: Maximum number of entities to return
            offset: Number of entities to skip
            
        Returns:
            List of entities
        """
        pass
    
    @abstractmethod
    async def save(self, entity: T) -> ID:
        """Save entity (create or update).
        
        Args:
            entity: Entity to save
            
        Returns:
            ID of saved entity
            
        Raises:
            RepositoryError: If save operation fails
            ValidationError: If entity is invalid
        """
        pass
    
    @abstractmethod
    async def delete_by_id(self, entity_id: ID) -> bool:
        """Delete entity by ID.
        
        Args:
            entity_id: Primary key of entity to delete
            
        Returns:
            True if entity was deleted, False if not found
        """
        pass
    
    @abstractmethod
    async def exists(self, entity_id: ID) -> bool:
        """Check if entity exists.
        
        Args:
            entity_id: Primary key to check
            
        Returns:
            True if entity exists
        """
        pass
    
    @abstractmethod
    async def count(self, filters: Optional[Dict[str, Any]] = None) -> int:
        """Count entities matching optional filters.
        
        Args:
            filters: Optional filtering criteria
            
        Returns:
            Number of matching entities
        """
        pass
    
    @abstractmethod
    async def find_by_criteria(
        self, 
        criteria: Dict[str, Any],
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        order_by: Optional[str] = None
    ) -> List[T]:
        """Find entities matching criteria.
        
        Args:
            criteria: Filtering criteria as key-value pairs
            limit: Maximum results to return
            offset: Number of results to skip
            order_by: Field to order by
            
        Returns:
            List of matching entities
        """
        pass
    
    @abstractmethod
    async def find_created_between(
        self, 
        start_date: datetime, 
        end_date: datetime
    ) -> List[T]:
        """Find entities created within date range.
        
        Args:
            start_date: Start of date range (inclusive)
            end_date: End of date range (inclusive)
            
        Returns:
            List of entities created in range
        """
        pass
