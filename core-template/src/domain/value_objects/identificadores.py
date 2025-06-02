"""Domain identifiers and value objects.

This module contains value objects that represent
identifiers and other immutable concepts in the domain.
"""

from dataclasses import dataclass
from typing import Optional
import re


@dataclass(frozen=True)  # Immutable value object
class DocumentoIdentidad:
    """Value object representing customer identity document.
    
    This value object encapsulates document validation rules
    and formatting that may vary by country/client.
    
    Examples:
        >>> doc = DocumentoIdentidad("12345678", "DNI", "PE")
        >>> doc.es_valido()
        True
        >>> doc.formato_display()
        'DNI: 12345678 (PE)'
    """
    
    numero: str  # Document number
    tipo: str  # Document type (DNI, CC, RUT, etc.)
    pais: Optional[str] = None  # Country code (PE, CO, GT, etc.)
    
    def __post_init__(self) -> None:
        """Validate document invariants."""
        if not self.numero.strip():
            raise ValueError("Número de documento no puede estar vacío")
        if not self.tipo.strip():
            raise ValueError("Tipo de documento no puede estar vacío")
        
        # Remove spaces and special characters for validation
        numero_limpio = re.sub(r'[^0-9A-Za-z]', '', self.numero)
        if not numero_limpio:
            raise ValueError("Documento debe contener caracteres alfanuméricos")
    
    def es_valido(self) -> bool:
        """Validate document based on country rules.
        
        Returns:
            True if document format is valid
            
        Note:
            This is a basic validation. Real implementation
            would include country-specific validation rules.
        """
        numero_limpio = re.sub(r'[^0-9A-Za-z]', '', self.numero)
        
        # Basic length validation by country
        if self.pais == "PE":  # Peru DNI
            return len(numero_limpio) == 8 and numero_limpio.isdigit()
        elif self.pais == "CO":  # Colombia CC
            return 6 <= len(numero_limpio) <= 11 and numero_limpio.isdigit()
        elif self.pais == "GT":  # Guatemala DPI
            return len(numero_limpio) == 13 and numero_limpio.isdigit()
        else:
            # Generic validation - at least 6 characters
            return len(numero_limpio) >= 6
    
    def numero_normalizado(self) -> str:
        """Get normalized document number.
        
        Returns:
            Document number without spaces or special characters
        """
        return re.sub(r'[^0-9A-Za-z]', '', self.numero)
    
    def formato_display(self) -> str:
        """Format document for display.
        
        Returns:
            Formatted string for UI display
            
        Examples:
            >>> doc = DocumentoIdentidad("12345678", "DNI", "PE")
            >>> doc.formato_display()
            'DNI: 12345678 (PE)'
        """
        base = f"{self.tipo}: {self.numero}"
        if self.pais:
            base += f" ({self.pais})"
        return base
    
    def es_tipo_cedula(self) -> bool:
        """Check if document is a national ID.
        
        Returns:
            True for national identity documents
        """
        tipos_cedula = ["DNI", "CC", "DPI", "CI", "RUT"]
        return self.tipo.upper() in tipos_cedula
    
    def __str__(self) -> str:
        """String representation."""
        return self.numero_normalizado()


@dataclass(frozen=True)
class CodigoCliente:
    """Value object for client identification codes.
    
    Used to identify different clients in the multi-tenant system.
    
    Examples:
        >>> codigo = CodigoCliente("movistar-peru")
        >>> codigo.es_valido()
        True
        >>> codigo.pais
        'PE'
    """
    
    codigo: str  # Client code (e.g., "movistar-peru")
    
    def __post_init__(self) -> None:
        """Validate client code format."""
        if not self.codigo:
            raise ValueError("Código de cliente no puede estar vacío")
        
        # Client codes should be lowercase with hyphens
        if not re.match(r'^[a-z0-9-]+$', self.codigo):
            raise ValueError(
                "Código de cliente debe contener solo letras minúsculas, "
                "números y guiones"
            )
    
    def es_valido(self) -> bool:
        """Validate client code format.
        
        Returns:
            True if code format is valid
        """
        return bool(re.match(r'^[a-z0-9-]+$', self.codigo))
    
    @property
    def empresa(self) -> str:
        """Extract company name from code.
        
        Returns:
            Company name portion of the code
            
        Examples:
            >>> CodigoCliente("movistar-peru").empresa
            'movistar'
        """
        return self.codigo.split('-')[0]
    
    @property
    def pais(self) -> Optional[str]:
        """Extract country from code.
        
        Returns:
            Country code if present in client code
            
        Examples:
            >>> CodigoCliente("movistar-peru").pais
            'PE'
        """
        parts = self.codigo.split('-')
        if len(parts) >= 2:
            pais_map = {
                'peru': 'PE',
                'colombia': 'CO', 
                'guatemala': 'GT',
                'chile': 'CL',
                'ecuador': 'EC'
            }
            return pais_map.get(parts[1])
        return None
    
    def __str__(self) -> str:
        """String representation."""
        return self.codigo
