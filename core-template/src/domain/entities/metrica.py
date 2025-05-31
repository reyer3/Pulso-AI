"""Metrica value object.

Value object for calculated metrics in the dashboard system.
Supports dynamic metric calculation with filtering context.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Any, Optional


@dataclass(frozen=True)
class Metrica:
    """Value object para métricas calculadas.
    
    Representa una métrica calculada del dashboard con su contexto completo.
    Es inmutable (frozen=True) siguiendo el patrón Value Object.
    
    Attributes:
        nombre: Identificador de la métrica (e.g., "tasa_contactabilidad")
        valor: Valor numérico calculado de la métrica
        unidad: Unidad de medida ("%", "count", "hours", "currency")
        periodo: Período de cálculo ("daily", "weekly", "monthly")
        fecha_calculo: Timestamp de cuando se calculó
        filtros_aplicados: Contexto de filtros que se usaron en el cálculo
        metadata: Información adicional sobre el cálculo
    
    Examples:
        >>> from datetime import datetime
        >>> metrica = Metrica(
        ...     nombre="tasa_contactabilidad",
        ...     valor=75.5,
        ...     unidad="%",
        ...     periodo="daily",
        ...     fecha_calculo=datetime.now(),
        ...     filtros_aplicados={"ejecutivo": "Ana García", "servicio": "MOVIL"}
        ... )
        >>> metrica.es_metrica_porcentual()
        True
        >>> metrica.supera_umbral(70.0)
        True
    """
    
    nombre: str
    valor: float
    unidad: str
    periodo: str
    fecha_calculo: datetime
    filtros_aplicados: Dict[str, Any]
    metadata: Optional[Dict[str, Any]] = None
    
    def __post_init__(self):
        """Validate value object constraints."""
        if not self.nombre or not self.nombre.strip():
            raise ValueError("El nombre de la métrica no puede estar vacío")
            
        if not self.unidad or not self.unidad.strip():
            raise ValueError("La unidad no puede estar vacía")
            
        if not self.periodo or not self.periodo.strip():
            raise ValueError("El período no puede estar vacío")
            
        # Validate unidad values
        unidades_validas = {"%", "count", "hours", "currency", "ratio", "days"}
        if self.unidad not in unidades_validas:
            raise ValueError(
                f"Unidad inválida: {self.unidad}. "
                f"Válidas: {unidades_validas}"
            )
            
        # Validate periodo values  
        periodos_validos = {"daily", "weekly", "monthly", "quarterly", "yearly"}
        if self.periodo not in periodos_validos:
            raise ValueError(
                f"Período inválido: {self.periodo}. "
                f"Válidos: {periodos_validos}"
            )
    
    def es_metrica_porcentual(self) -> bool:
        """Determina si la métrica es un porcentaje.
        
        Returns:
            True si la unidad es porcentual
        """
        return self.unidad == "%"
    
    def supera_umbral(self, umbral: float) -> bool:
        """Business rule: determina si métrica supera umbral dado.
        
        Args:
            umbral: Valor umbral para comparar
            
        Returns:
            True si el valor supera el umbral
            
        Examples:
            >>> metrica = Metrica("test", 75.0, "%", "daily", datetime.now(), {})
            >>> metrica.supera_umbral(70.0)
            True
        """
        return self.valor > umbral
    
    def esta_en_rango_optimo(self, minimo: float, maximo: float) -> bool:
        """Business rule: determina si métrica está en rango óptimo.
        
        Args:
            minimo: Valor mínimo del rango óptimo
            maximo: Valor máximo del rango óptimo
            
        Returns:
            True si el valor está dentro del rango
            
        Examples:
            >>> metrica = Metrica("test", 75.0, "%", "daily", datetime.now(), {})
            >>> metrica.esta_en_rango_optimo(70.0, 80.0)
            True
        """
        return minimo <= self.valor <= maximo
    
    def obtener_clasificacion_rendimiento(self) -> str:
        """Business rule: clasifica rendimiento basado en valor y unidad.
        
        Returns:
            Clasificación: "EXCELENTE", "BUENO", "REGULAR", "DEFICIENTE"
        """
        if self.es_metrica_porcentual():
            if self.valor >= 80:
                return "EXCELENTE"
            elif self.valor >= 60:
                return "BUENO"
            elif self.valor >= 40:
                return "REGULAR"
            else:
                return "DEFICIENTE"
        else:
            # For non-percentage metrics, use relative thresholds
            if self.valor >= 100:
                return "EXCELENTE"
            elif self.valor >= 50:
                return "BUENO"
            elif self.valor >= 25:
                return "REGULAR"
            else:
                return "DEFICIENTE"
    
    def tiene_filtros_aplicados(self) -> bool:
        """Determina si la métrica fue calculada con filtros.
        
        Returns:
            True si hay filtros aplicados en el cálculo
        """
        return bool(self.filtros_aplicados)
    
    def obtener_descripcion_filtros(self) -> str:
        """Genera descripción legible de los filtros aplicados.
        
        Returns:
            String descriptivo de los filtros, o "Sin filtros" si no hay
            
        Examples:
            >>> filtros = {"ejecutivo": "Ana García", "servicio": "MOVIL"}
            >>> metrica = Metrica("test", 75.0, "%", "daily", datetime.now(), filtros)
            >>> metrica.obtener_descripcion_filtros()
            'ejecutivo: Ana García, servicio: MOVIL'
        """
        if not self.tiene_filtros_aplicados():
            return "Sin filtros"
            
        filtros_str = ", ".join(
            f"{key}: {value}" for key, value in self.filtros_aplicados.items()
        )
        return filtros_str
