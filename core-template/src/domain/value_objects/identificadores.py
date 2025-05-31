"""Domain identifier value objects.

Value objects for handling different types of identifiers used across
the multi-client system with proper validation.
"""

from dataclasses import dataclass
from typing import Optional
import re


@dataclass(frozen=True)
class DocumentoIdentidad:
    """Value object para documentos de identidad.
    
    Maneja diferentes tipos de documentos de identidad con validación
    específica por país/cliente, manteniendo compatibilidad cross-client.
    
    Attributes:
        numero: Número del documento
        tipo: Tipo de documento ("DNI", "CC", "DPI", "CI", "PASSPORT")
        pais: Código de país ISO ("PE", "CO", "GT")
        
    Examples:
        >>> doc = DocumentoIdentidad("12345678", "DNI", "PE")
        >>> doc.es_valido()
        True
        >>> doc.formato_display()
        'DNI: 12345678 (PE)'
    """
    
    numero: str
    tipo: str
    pais: str
    
    def __post_init__(self):
        """Validate documento constraints."""
        if not self.numero or not self.numero.strip():
            raise ValueError("El número de documento no puede estar vacío")
            
        if not self.tipo or not self.tipo.strip():
            raise ValueError("El tipo de documento no puede estar vacío")
            
        if not self.pais or not self.pais.strip():
            raise ValueError("El país no puede estar vacío")
            
        # Validate tipo values
        tipos_validos = {"DNI", "CC", "DPI", "CI", "PASSPORT", "RUT", "RUN"}
        if self.tipo.upper() not in tipos_validos:
            raise ValueError(
                f"Tipo de documento inválido: {self.tipo}. "
                f"Válidos: {tipos_validos}"
            )
            
        # Validate pais codes
        paises_validos = {"PE", "CO", "GT", "CL", "AR", "MX", "EC"}
        if self.pais.upper() not in paises_validos:
            raise ValueError(
                f"Código de país inválido: {self.pais}. "
                f"Válidos: {paises_validos}"
            )
            
        # Normalize values
        object.__setattr__(self, 'tipo', self.tipo.upper())
        object.__setattr__(self, 'pais', self.pais.upper())
        object.__setattr__(self, 'numero', self.numero.strip())
    
    def es_valido(self) -> bool:
        """Valida formato del documento según tipo y país.
        
        Returns:
            True si el formato es válido
            
        Examples:
            >>> DocumentoIdentidad("12345678", "DNI", "PE").es_valido()
            True
            >>> DocumentoIdentidad("abc", "DNI", "PE").es_valido()
            False
        """
        try:
            return self._validar_formato_por_tipo()
        except Exception:
            return False
    
    def _validar_formato_por_tipo(self) -> bool:
        """Validación específica por tipo de documento."""
        if self.tipo == "DNI" and self.pais == "PE":
            # DNI Perú: 8 dígitos
            return re.match(r'^\d{8}$', self.numero) is not None
            
        elif self.tipo == "CC" and self.pais == "CO":
            # Cédula Colombia: 6-10 dígitos
            return re.match(r'^\d{6,10}$', self.numero) is not None
            
        elif self.tipo == "DPI" and self.pais == "GT":
            # DPI Guatemala: 13 dígitos
            return re.match(r'^\d{13}$', self.numero) is not None
            
        elif self.tipo == "PASSPORT":
            # Passport: formato alfanumérico internacional
            return re.match(r'^[A-Z0-9]{6,12}$', self.numero.upper()) is not None
            
        else:
            # Validación genérica: al menos debe ser alfanumérico
            return re.match(r'^[A-Z0-9]{4,15}$', self.numero.upper()) is not None
    
    def formato_display(self) -> str:
        """Formato legible para mostrar en UI.
        
        Returns:
            String formateado para display
            
        Examples:
            >>> doc = DocumentoIdentidad("12345678", "DNI", "PE")
            >>> doc.formato_display()
            'DNI: 12345678 (PE)'
        """
        return f"{self.tipo}: {self.numero} ({self.pais})"
    
    def formato_busqueda(self) -> str:
        """Formato normalizado para búsquedas en base de datos.
        
        Returns:
            String normalizado sin espacios ni caracteres especiales
            
        Examples:
            >>> doc = DocumentoIdentidad(" 123-456-78 ", "DNI", "PE")
            >>> doc.formato_busqueda()
            '12345678'
        """
        # Remove spaces, hyphens, and other common separators
        return re.sub(r'[\s\-\.]+', '', self.numero)
    
    def obtener_digito_verificador(self) -> Optional[str]:
        """Calcula dígito verificador si aplica para el tipo de documento.
        
        Returns:
            Dígito verificador o None si no aplica
        """
        if self.tipo == "CC" and self.pais == "CO":
            # Algoritmo para cédula colombiana
            return self._calcular_dv_colombia()
        elif self.tipo == "DPI" and self.pais == "GT":
            # Algoritmo para DPI guatemalteco
            return self._calcular_dv_guatemala()
        else:
            return None
    
    def _calcular_dv_colombia(self) -> str:
        """Calcula dígito verificador para cédula colombiana."""
        # Simplified algorithm - in production would use official algorithm
        if not self.numero.isdigit():
            return "0"
            
        total = sum(
            int(digit) * (i + 1) 
            for i, digit in enumerate(reversed(self.numero))
        )
        return str(total % 10)
    
    def _calcular_dv_guatemala(self) -> str:
        """Calcula dígito verificador para DPI guatemalteco."""
        # Simplified algorithm - in production would use official algorithm
        if not self.numero.isdigit() or len(self.numero) < 13:
            return "0"
            
        # Use last digit as verification
        return self.numero[-1]
