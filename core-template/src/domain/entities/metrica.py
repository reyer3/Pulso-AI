"""Metrica value object.

Represents calculated metrics used in dashboards and reports.
This value object encapsulates metric calculation results
with their context and validation rules.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Any, Optional
from enum import Enum


class UnidadMetrica(Enum):
    """Units for metric values."""
    PORCENTAJE = "%"
    CANTIDAD = "count"
    HORAS = "hours"
    MINUTOS = "minutes"
    PESOS = "currency"
    RATIO = "ratio"
    SCORE = "score"


class PeriodoMetrica(Enum):
    """Time periods for metric calculation."""
    DIARIO = "daily"
    SEMANAL = "weekly"
    MENSUAL = "monthly"
    TRIMESTRAL = "quarterly"
    ANUAL = "yearly"
    TIEMPO_REAL = "real_time"


@dataclass(frozen=True)  # Immutable value object
class Metrica:
    """Value object representing a calculated metric.
    
    This value object contains the result of a metric calculation
    along with its context, validation thresholds, and metadata.
    
    Examples:
        >>> from datetime import datetime
        >>> metrica = Metrica(
        ...     nombre="tasa_contactabilidad",
        ...     valor=65.5,
        ...     unidad=UnidadMetrica.PORCENTAJE,
        ...     periodo=PeriodoMetrica.DIARIO,
        ...     fecha_calculo=datetime.now()
        ... )
        >>> metrica.esta_en_rango_optimo(60.0, 80.0)
        True
        >>> metrica.calcular_nivel_rendimiento()
        'BUENO'
    """
    
    nombre: str  # Metric identifier (e.g., "tasa_contactabilidad")
    valor: float  # Calculated metric value
    unidad: UnidadMetrica  # Unit of measurement
    periodo: PeriodoMetrica  # Time period for calculation
    fecha_calculo: datetime  # When metric was calculated
    filtros_aplicados: Optional[Dict[str, Any]] = None  # Context filters
    threshold_warning: Optional[float] = None  # Warning threshold
    threshold_critical: Optional[float] = None  # Critical threshold
    target_value: Optional[float] = None  # Target/goal value
    metadata: Optional[Dict[str, Any]] = None  # Additional context
    
    def __post_init__(self) -> None:
        """Validate metric invariants."""
        if not self.nombre.strip():
            raise ValueError("Nombre de métrica no puede estar vacío")
        
        # Validate percentage values
        if self.unidad == UnidadMetrica.PORCENTAJE:
            if not (0 <= self.valor <= 100):
                raise ValueError("Valor de porcentaje debe estar entre 0 y 100")
        
        # Validate score values
        if self.unidad == UnidadMetrica.SCORE:
            if not (0 <= self.valor <= 1):
                raise ValueError("Valor de score debe estar entre 0 y 1")
        
        # Validate threshold relationships
        if (self.threshold_warning is not None and 
            self.threshold_critical is not None):
            if self.threshold_critical <= self.threshold_warning:
                raise ValueError(
                    "Threshold crítico debe ser mayor al de warning"
                )
    
    def esta_en_rango_optimo(
        self, 
        minimo: float, 
        maximo: float
    ) -> bool:
        """Check if metric value is within optimal range.
        
        Args:
            minimo: Minimum acceptable value
            maximo: Maximum acceptable value
            
        Returns:
            True if value is within range
            
        Examples:
            >>> metrica = Metrica("test", 75.0, UnidadMetrica.PORCENTAJE, ...)
            >>> metrica.esta_en_rango_optimo(60.0, 80.0)
            True
        """
        return minimo <= self.valor <= maximo
    
    def calcular_nivel_rendimiento(self) -> str:
        """Calculate performance level based on thresholds.
        
        Returns:
            Performance level: "EXCELENTE", "BUENO", "WARNING", "CRITICO"
            
        Examples:
            >>> metrica = Metrica(
            ...     "test", 85.0, UnidadMetrica.PORCENTAJE, 
            ...     PeriodoMetrica.DIARIO, datetime.now(),
            ...     threshold_warning=70.0, threshold_critical=50.0
            ... )
            >>> metrica.calcular_nivel_rendimiento()
            'EXCELENTE'
        """
        if self.target_value and self.valor >= self.target_value:
            return "EXCELENTE"
        elif (self.threshold_warning is not None and 
              self.valor >= self.threshold_warning):
            return "BUENO"
        elif (self.threshold_critical is not None and 
              self.valor >= self.threshold_critical):
            return "WARNING"
        else:
            return "CRITICO"
    
    def porcentaje_del_target(self) -> Optional[float]:
        """Calculate percentage achievement of target value.
        
        Returns:
            Percentage of target achieved, or None if no target set
        """
        if self.target_value is None or self.target_value == 0:
            return None
        
        return (self.valor / self.target_value) * 100
    
    def formato_display(self) -> str:
        """Format metric for display in UI.
        
        Returns:
            Formatted string with value and unit
            
        Examples:
            >>> metrica = Metrica("test", 65.5, UnidadMetrica.PORCENTAJE, ...)
            >>> metrica.formato_display()
            '65.5%'
        """
        if self.unidad == UnidadMetrica.PORCENTAJE:
            return f"{self.valor:.1f}%"
        elif self.unidad == UnidadMetrica.CANTIDAD:
            return f"{int(self.valor)}"
        elif self.unidad == UnidadMetrica.PESOS:
            return f"${self.valor:,.2f}"
        elif self.unidad == UnidadMetrica.HORAS:
            return f"{self.valor:.1f}h"
        elif self.unidad == UnidadMetrica.MINUTOS:
            return f"{int(self.valor)}min"
        elif self.unidad == UnidadMetrica.SCORE:
            return f"{self.valor:.2f}"
        else:
            return f"{self.valor:.2f} {self.unidad.value}"
    
    def es_metrica_temporal(self) -> bool:
        """Check if metric is time-based.
        
        Returns:
            True if metric period is not real-time
        """
        return self.periodo != PeriodoMetrica.TIEMPO_REAL
    
    def dias_desde_calculo(self) -> int:
        """Calculate days since metric was calculated.
        
        Returns:
            Number of days since calculation
        """
        return (datetime.now() - self.fecha_calculo).days
    
    def necesita_actualizacion(self, max_days: int = 1) -> bool:
        """Check if metric needs to be recalculated.
        
        Args:
            max_days: Maximum days before recalculation needed
            
        Returns:
            True if metric should be recalculated
        """
        return self.dias_desde_calculo() > max_days
    
    def __str__(self) -> str:
        """String representation of the metric."""
        return (
            f"Metrica({self.nombre}={self.formato_display()}, "
            f"periodo={self.periodo.value})"
        )
