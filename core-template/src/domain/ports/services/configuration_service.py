"""Configuration service interface.

Defines the contract for client-specific configuration management.
This service handles multi-tenant configuration, field mappings,
and homologation rules that enable the same business logic to work
across different clients with different data structures.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

from ...value_objects.enums import TipificacionHomologada


@dataclass
class ClientConfig:
    """Complete client configuration.
    
    Contains all configuration needed to adapt the platform
    for a specific client's data structure and business rules.
    """
    client_id: str
    name: str
    field_mappings: Dict[str, str]  # standard_field -> client_field
    tipificacion_mappings: Dict[str, str]  # client_tip -> standard_tip
    business_rules: Dict[str, Any]  # client-specific rule overrides
    database_config: Dict[str, Any]  # connection and schema info
    dashboard_config: Dict[str, Any]  # UI customizations
    thresholds: Dict[str, float]  # metric thresholds
    active: bool = True


@dataclass
class FieldMapping:
    """Mapping between standard domain field and client-specific field."""
    standard_field: str
    client_field: str
    field_type: str  # "string", "number", "date", "boolean"
    transformation: Optional[str] = None  # optional data transformation
    validation_rules: Optional[Dict[str, Any]] = None


class ConfigurationService(ABC):
    """Service interface for client configuration management.
    
    This service enables multi-tenant operations by providing
    client-specific configurations that adapt the domain logic
    to work with different data structures and business rules.
    
    Examples:
        >>> # Get Movistar configuration
        >>> config = await service.get_client_config("movistar-peru")
        >>> print(config.name)  # "Movistar Perú"
        >>> 
        >>> # Get field mapping for ejecutivo
        >>> ejecutivo_field = config.field_mappings["ejecutivo"]
        >>> # For Movistar: "ejecutivo"
        >>> # For Claro: "agente"
        >>> # For Tigo: "asesor"
    """
    
    @abstractmethod
    async def get_client_config(self, client_id: str) -> ClientConfig:
        """Get complete configuration for specific client.
        
        Args:
            client_id: Unique client identifier
            
        Returns:
            Complete client configuration
            
        Raises:
            ClientNotFoundError: If client_id doesn't exist
            ConfigurationError: If configuration is invalid
            
        Examples:
            >>> config = await service.get_client_config("movistar-peru")
            >>> assert config.client_id == "movistar-peru"
            >>> assert config.name == "Movistar Perú"
        """
        pass
    
    @abstractmethod
    async def get_field_mappings(
        self,
        client_id: str,
        entity_type: Optional[str] = None
    ) -> Dict[str, FieldMapping]:
        """Get field mappings for client.
        
        Args:
            client_id: Client identifier
            entity_type: Optional entity filter ("cliente", "gestion")
            
        Returns:
            Dictionary mapping standard fields to client fields
            
        Examples:
            >>> mappings = await service.get_field_mappings("claro-colombia")
            >>> ejecutivo_mapping = mappings["ejecutivo"]
            >>> assert ejecutivo_mapping.client_field == "agente"
        """
        pass
    
    @abstractmethod
    async def get_homologation_rules(
        self,
        client_id: str,
        reverse: bool = False
    ) -> Dict[str, str]:
        """Get tipification homologation rules.
        
        Args:
            client_id: Client identifier
            reverse: If True, returns standard -> client mapping
            
        Returns:
            Dictionary mapping client tipifications to standard ones
            
        Examples:
            >>> # Client -> Standard mapping
            >>> rules = await service.get_homologation_rules("movistar-peru")
            >>> assert rules["CONT_COMP"] == "COMPROMISO_PAGO"
            >>> 
            >>> # Standard -> Client mapping
            >>> reverse_rules = await service.get_homologation_rules(
            ...     "movistar-peru",
            ...     reverse=True
            ... )
            >>> assert reverse_rules["COMPROMISO_PAGO"] == "CONT_COMP"
        """
        pass
    
    @abstractmethod
    async def homologate_tipification(
        self,
        client_id: str,
        client_tipification: str
    ) -> TipificacionHomologada:
        """Convert client tipification to standard enum.
        
        Args:
            client_id: Client identifier
            client_tipification: Client-specific tipification
            
        Returns:
            Standardized tipification enum
            
        Raises:
            HomologationError: If mapping doesn't exist
            
        Examples:
            >>> # Movistar "CONT_COMP" -> COMPROMISO_PAGO
            >>> standard = await service.homologate_tipification(
            ...     "movistar-peru",
            ...     "CONT_COMP"
            ... )
            >>> assert standard == TipificacionHomologada.COMPROMISO_PAGO
        """
        pass
    
    @abstractmethod
    async def validate_client_config(self, config: ClientConfig) -> bool:
        """Validate client configuration for correctness.
        
        Args:
            config: Client configuration to validate
            
        Returns:
            True if configuration is valid
            
        Raises:
            ConfigurationError: If configuration is invalid
            
        Examples:
            >>> config = ClientConfig(
            ...     client_id="test-client",
            ...     name="Test Client",
            ...     field_mappings={"ejecutivo": "agent"},
            ...     tipificacion_mappings={"SUCCESS": "COMPROMISO_PAGO"},
            ...     business_rules={},
            ...     database_config={"type": "postgresql"},
            ...     dashboard_config={},
            ...     thresholds={"contactability_min": 50.0}
            ... )
            >>> is_valid = await service.validate_client_config(config)
        """
        pass
    
    @abstractmethod
    async def get_business_rules(
        self,
        client_id: str,
        rule_category: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get client-specific business rule overrides.
        
        Args:
            client_id: Client identifier
            rule_category: Optional category filter
            
        Returns:
            Dictionary with business rules
            
        Examples:
            >>> rules = await service.get_business_rules("movistar-peru")
            >>> # Returns: {
            >>> #     "mora_days_critical": 90,
            >>> #     "debt_amount_significant": 1000.0,
            >>> #     "working_hours_start": 8,
            >>> #     "working_hours_end": 18
            >>> # }
        """
        pass
    
    @abstractmethod
    async def get_metric_thresholds(
        self,
        client_id: str,
        metric_name: Optional[str] = None
    ) -> Dict[str, Dict[str, float]]:
        """Get metric threshold configurations.
        
        Args:
            client_id: Client identifier
            metric_name: Optional metric filter
            
        Returns:
            Dictionary with metric thresholds
            
        Examples:
            >>> thresholds = await service.get_metric_thresholds("movistar-peru")
            >>> # Returns: {
            >>> #     "tasa_contactabilidad": {
            >>> #         "poor": 30.0,
            >>> #         "warning": 50.0,
            >>> #         "good": 70.0,
            >>> #         "excellent": 85.0
            >>> #     }
            >>> # }
        """
        pass
    
    @abstractmethod
    async def get_dashboard_config(
        self,
        client_id: str,
        dashboard_type: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get dashboard customization configuration.
        
        Args:
            client_id: Client identifier
            dashboard_type: Optional dashboard type filter
            
        Returns:
            Dictionary with dashboard configuration
            
        Examples:
            >>> config = await service.get_dashboard_config("movistar-peru")
            >>> # Returns: {
            >>> #     "theme": {
            >>> #         "primary_color": "#E60026",  # Movistar red
            >>> #         "logo_url": "/assets/movistar-logo.png"
            >>> #     },
            >>> #     "widgets": [
            >>> #         {"type": "metric_card", "metric": "tasa_contactabilidad"},
            >>> #         {"type": "chart", "chart_type": "line", "metric": "pdps_por_hora"}
            >>> #     ]
            >>> # }
        """
        pass
    
    @abstractmethod
    async def list_active_clients(self) -> List[str]:
        """List all active client IDs.
        
        Returns:
            List of active client identifiers
            
        Examples:
            >>> clients = await service.list_active_clients()
            >>> # Returns: ["movistar-peru", "claro-colombia", "tigo-guatemala"]
        """
        pass
    
    @abstractmethod
    async def save_client_config(self, config: ClientConfig) -> bool:
        """Save or update client configuration.
        
        Args:
            config: Client configuration to save
            
        Returns:
            True if save was successful
            
        Examples:
            >>> config = ClientConfig(...)
            >>> success = await service.save_client_config(config)
        """
        pass
    
    @abstractmethod
    async def delete_client_config(self, client_id: str) -> bool:
        """Delete client configuration.
        
        Args:
            client_id: Client identifier to delete
            
        Returns:
            True if deletion was successful
            
        Examples:
            >>> success = await service.delete_client_config("test-client")
        """
        pass
    
    @abstractmethod
    async def validate_field_mapping(
        self,
        mapping: FieldMapping,
        sample_data: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Validate field mapping against sample data.
        
        Args:
            mapping: Field mapping to validate
            sample_data: Optional sample data for validation
            
        Returns:
            True if mapping is valid
            
        Examples:
            >>> mapping = FieldMapping(
            ...     standard_field="ejecutivo",
            ...     client_field="agent_name",
            ...     field_type="string"
            ... )
            >>> is_valid = await service.validate_field_mapping(mapping)
        """
        pass
    
    @abstractmethod
    async def get_client_database_config(
        self,
        client_id: str
    ) -> Dict[str, Any]:
        """Get database connection configuration for client.
        
        Args:
            client_id: Client identifier
            
        Returns:
            Database configuration dictionary
            
        Examples:
            >>> db_config = await service.get_client_database_config("movistar-peru")
            >>> # Returns: {
            >>> #     "type": "bigquery",
            >>> #     "project_id": "mibot-222814",
            >>> #     "dataset": "BI_USA",
            >>> #     "credentials_path": "/path/to/service-account.json"
            >>> # }
        """
        pass
