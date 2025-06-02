"""Configuration service interface.

Defines contracts for multi-client configuration management.
Handles client-specific settings, field mappings, and business rules.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from dataclasses import dataclass


@dataclass
class ClientConfig:
    """Client configuration data structure.
    
    Contains all client-specific configuration including
    data mappings, business rules, and customizations.
    """
    client_id: str
    name: str
    database_config: Dict[str, Any]
    field_mappings: Dict[str, str]
    dimension_config: Dict[str, Any]
    metric_config: Dict[str, Any]
    homologation_rules: Dict[str, str]
    thresholds: Dict[str, float]
    ui_customization: Dict[str, Any]
    

class ConfigurationService(ABC):
    """Service interface for client configuration management.
    
    This service handles all aspects of multi-client configuration,
    enabling the same codebase to work with different clients
    through configuration rather than code changes.
    
    Key Features:
        - Client-specific data source configuration
        - Field mapping between client schema and domain model
        - Business rule customization per client
        - UI customization and branding
        - Homologation rule management
    
    Examples:
        >>> # Get Movistar configuration
        >>> config = await config_service.get_client_config("movistar-peru")
        >>> print(f"Database: {config.database_config['type']}")
        >>> 
        >>> # Map client field to domain field
        >>> mappings = await config_service.get_field_mappings("claro-colombia")
        >>> domain_field = mappings.get("agente", "ejecutivo")
    """
    
    @abstractmethod
    async def get_client_config(self, client_id: str) -> ClientConfig:
        """Get complete configuration for client.
        
        Retrieves all configuration data needed to operate
        the system for a specific client.
        
        Args:
            client_id: Unique client identifier
            
        Returns:
            Complete client configuration
            
        Raises:
            ConfigurationError: If client not found or config invalid
            
        Examples:
            >>> # Movistar Peru configuration
            >>> config = await service.get_client_config("movistar-peru")
            >>> assert config.database_config["type"] == "bigquery"
            >>> 
            >>> # Claro Colombia configuration
            >>> config = await service.get_client_config("claro-colombia")
            >>> assert config.database_config["type"] == "postgresql"
        """
        pass
        
    @abstractmethod
    async def get_field_mappings(self, client_id: str) -> Dict[str, str]:
        """Get field mappings for client.
        
        Returns mapping from client-specific field names
        to standardized domain field names.
        
        Args:
            client_id: Client identifier
            
        Returns:
            Dictionary mapping client fields to domain fields
            
        Examples:
            >>> # Movistar uses "ejecutivo", others use different names
            >>> movistar_mappings = await service.get_field_mappings("movistar-peru")
            >>> assert movistar_mappings["ejecutivo"] == "ejecutivo"
            >>> 
            >>> claro_mappings = await service.get_field_mappings("claro-colombia")
            >>> assert claro_mappings["agente"] == "ejecutivo"  # Maps "agente" -> "ejecutivo"
            >>> 
            >>> tigo_mappings = await service.get_field_mappings("tigo-guatemala")
            >>> assert tigo_mappings["asesor"] == "ejecutivo"  # Maps "asesor" -> "ejecutivo"
        """
        pass
        
    @abstractmethod
    async def get_homologation_rules(self, client_id: str) -> Dict[str, str]:
        """Get tipification homologation rules.
        
        Returns mapping from client-specific tipifications
        to standardized TipificacionHomologada values.
        
        Args:
            client_id: Client identifier
            
        Returns:
            Dictionary mapping client tipifications to homologated values
            
        Business Context:
            Each client uses different terminology for the same concepts:
            - Movistar: "CONT_COMP" -> "COMPROMISO_PAGO"
            - Claro: "PROMESA_PAGO" -> "COMPROMISO_PAGO"
            - Tigo: "ACEPTA_PAGAR" -> "COMPROMISO_PAGO"
            
        Examples:
            >>> # Movistar homologation
            >>> rules = await service.get_homologation_rules("movistar-peru")
            >>> assert rules["CONT_COMP"] == "COMPROMISO_PAGO"
            >>> assert rules["NO_CONT"] == "NO_CONTACTO"
            >>> 
            >>> # Claro homologation
            >>> rules = await service.get_homologation_rules("claro-colombia")
            >>> assert rules["PROMESA_PAGO"] == "COMPROMISO_PAGO"
            >>> assert rules["SIN_RESPUESTA"] == "NO_CONTACTO"
        """
        pass
        
    @abstractmethod
    async def validate_client_config(self, config: ClientConfig) -> bool:
        """Validate client configuration.
        
        Checks that client configuration is complete and valid
        before applying it to the system.
        
        Args:
            config: Client configuration to validate
            
        Returns:
            True if configuration is valid
            
        Raises:
            ValidationError: If configuration is invalid with details
            
        Validation Rules:
            - Required fields present
            - Database connection valid
            - Field mappings cover all required domain fields
            - Homologation rules cover common tipifications
            - Thresholds within acceptable ranges
            - UI customization follows schema
            
        Examples:
            >>> config = ClientConfig(
            ...     client_id="test-client",
            ...     name="Test Client",
            ...     database_config={"type": "postgresql", "host": "localhost"},
            ...     field_mappings={"agente": "ejecutivo"},
            ...     # ... other required fields
            ... )
            >>> is_valid = await service.validate_client_config(config)
            >>> assert is_valid
        """
        pass
    
    @abstractmethod
    async def get_dimension_config(self, client_id: str) -> Dict[str, Any]:
        """Get dimension configuration for dashboards.
        
        Returns configuration for dashboard dimensions including
        display names, valid values, and cross-filtering rules.
        
        Args:
            client_id: Client identifier
            
        Returns:
            Dimension configuration dictionary
            
        Configuration Structure:
            {
                "ejecutivo": {
                    "display_name": "Ejecutivo de Cobranza",
                    "type": "categorical",
                    "affects_dimensions": ["cartera", "servicio"],
                    "source_field": "ejecutivo"
                },
                "cartera": {
                    "display_name": "Cartera de Gestión",
                    "valid_values": ["Gestión Temprana", "Altas Nuevas"],
                    "source_field": "tipo_cartera"
                }
            }
            
        Examples:
            >>> # Movistar dimension config
            >>> dims = await service.get_dimension_config("movistar-peru")
            >>> ejecutivo_config = dims["ejecutivo"]
            >>> assert ejecutivo_config["display_name"] == "Ejecutivo de Cobranza"
        """
        pass
    
    @abstractmethod
    async def get_metric_config(self, client_id: str) -> Dict[str, Any]:
        """Get metric configuration for calculations.
        
        Returns configuration for metric calculations including
        formulas, thresholds, and display settings.
        
        Args:
            client_id: Client identifier
            
        Returns:
            Metric configuration dictionary
            
        Configuration Structure:
            {
                "tasa_contactabilidad": {
                    "display_name": "Tasa de Contactabilidad",
                    "formula": "(contactos / total_gestiones) * 100",
                    "unit": "percentage",
                    "thresholds": {"warning": 60, "good": 75, "excellent": 85},
                    "target": 80
                },
                "pdps_por_hora": {
                    "display_name": "PDPs por Hora",
                    "formula": "pdp_count / horas_trabajadas",
                    "unit": "rate",
                    "thresholds": {"warning": 1.5, "good": 2.5, "excellent": 4.0}
                }
            }
            
        Examples:
            >>> # Movistar metric config
            >>> metrics = await service.get_metric_config("movistar-peru")
            >>> contactabilidad = metrics["tasa_contactabilidad"]
            >>> assert contactabilidad["target"] == 80
        """
        pass
    
    @abstractmethod
    async def get_database_config(self, client_id: str) -> Dict[str, Any]:
        """Get database connection configuration.
        
        Returns database-specific configuration for connecting
        to client's data source.
        
        Args:
            client_id: Client identifier
            
        Returns:
            Database configuration dictionary
            
        Configuration Examples:
            # BigQuery (Movistar)
            {
                "type": "bigquery",
                "project_id": "mibot-222814",
                "dataset": "BI_USA",
                "credentials_path": "/path/to/service-account.json"
            }
            
            # PostgreSQL (Claro)
            {
                "type": "postgresql",
                "host": "claro-db.amazonaws.com",
                "port": 5432,
                "database": "collection_db",
                "schema": "public"
            }
            
            # MySQL (Tigo)
            {
                "type": "mysql",
                "host": "tigo-mysql.azure.com",
                "port": 3306,
                "database": "cobranza"
            }
            
        Examples:
            >>> # Get BigQuery config for Movistar
            >>> db_config = await service.get_database_config("movistar-peru")
            >>> assert db_config["type"] == "bigquery"
            >>> assert db_config["project_id"] == "mibot-222814"
        """
        pass
    
    @abstractmethod
    async def update_client_config(
        self, 
        client_id: str, 
        updates: Dict[str, Any]
    ) -> bool:
        """Update client configuration.
        
        Updates specific parts of client configuration
        without requiring full config replacement.
        
        Args:
            client_id: Client identifier
            updates: Dictionary with configuration updates
            
        Returns:
            True if update successful
            
        Examples:
            >>> # Update metric thresholds
            >>> updates = {
            ...     "metric_config": {
            ...         "tasa_contactabilidad": {
            ...             "thresholds": {"warning": 65, "good": 80}
            ...         }
            ...     }
            ... }
            >>> success = await service.update_client_config(
            ...     "movistar-peru", updates
            ... )
        """
        pass
    
    @abstractmethod
    async def list_available_clients(self) -> List[str]:
        """List all configured clients.
        
        Returns list of client IDs that have valid configurations.
        
        Returns:
            List of client identifiers
            
        Examples:
            >>> clients = await service.list_available_clients()
            >>> assert "movistar-peru" in clients
            >>> assert "claro-colombia" in clients
            >>> assert "tigo-guatemala" in clients
        """
        pass
