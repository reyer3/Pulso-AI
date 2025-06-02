"""Base repository interface with common patterns.

Defines common repository operations that most entities need,
following Repository pattern best practices.
"""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List, Optional, Dict, Any
from datetime import datetime

# Generic type for entity
T = TypeVar('T')


class BaseRepository(ABC, Generic[T]):
    """Base repository interface with common CRUD operations.
    
    This interface provides standard repository methods that most
    entities will need. Specific repositories can extend this and
    add domain-specific methods.
    
    Type Parameters:
        T: The entity type this repository manages
        
    Examples:
        >>> class ClienteRepository(BaseRepository[Cliente]):
        ...     # Inherits common methods, adds specific ones
        ...     async def find_by_documento(self, documento: str) -> Optional[Cliente]:
        ...         pass
    """
    
    @abstractmethod
    async def save(self, entity: T) -> T:
        """Save or update an entity.
        
        Args:
            entity: The entity to save
            
        Returns:
            The saved entity (may include generated IDs, timestamps)
            
        Raises:
            RepositoryError: If save operation fails
        """
        pass
    
    @abstractmethod
    async def find_by_id(self, entity_id: str) -> Optional[T]:
        """Find entity by its unique identifier.
        
        Args:
            entity_id: Unique identifier of the entity
            
        Returns:
            Entity if found, None otherwise
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
    async def count(self, filters: Optional[Dict[str, Any]] = None) -> int:
        """Count entities matching optional filters.
        
        Args:
            filters: Optional filtering criteria
            
        Returns:
            Number of matching entities
        """
        pass
    
    @abstractmethod
    async def delete_by_id(self, entity_id: str) -> bool:
        """Delete entity by its unique identifier.
        
        Args:
            entity_id: Unique identifier of entity to delete
            
        Returns:
            True if entity was deleted, False if not found
        """
        pass
    
    @abstractmethod
    async def exists(self, entity_id: str) -> bool:
        """Check if entity exists by its unique identifier.
        
        Args:
            entity_id: Unique identifier to check
            
        Returns:
            True if entity exists, False otherwise
        """
        pass
    
    @abstractmethod
    async def find_by_criteria(
        self,
        criteria: Dict[str, Any],
        limit: Optional[int] = None,
        offset: Optional[int] = None
    ) -> List[T]:
        """Find entities matching complex criteria.
        
        Args:
            criteria: Dictionary of field/value pairs to match
            limit: Maximum number of entities to return
            offset: Number of entities to skip
            
        Returns:
            List of matching entities
            
        Examples:
            >>> criteria = {"status": "active", "amount_gte": 1000}
            >>> entities = await repo.find_by_criteria(criteria, limit=10)
        """
        pass
    
    @abstractmethod
    async def save_batch(self, entities: List[T]) -> List[T]:
        """Save multiple entities in a single operation.
        
        Args:
            entities: List of entities to save
            
        Returns:
            List of saved entities
            
        Note:
            Should be transactional when possible
        """
        pass
    
    @abstractmethod
    async def find_created_after(self, timestamp: datetime) -> List[T]:
        """Find entities created after specified timestamp.
        
        Args:
            timestamp: Minimum creation timestamp
            
        Returns:
            List of entities created after timestamp
        """
        pass
    
    @abstractmethod
    async def find_updated_after(self, timestamp: datetime) -> List[T]:
        """Find entities updated after specified timestamp.
        
        Args:
            timestamp: Minimum update timestamp
            
        Returns:
            List of entities updated after timestamp
        """
        pass
