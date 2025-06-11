# Infrastructure Adapters
# Implementations of domain ports for external systems

from .bigquery.telefonica_adapter import TelefonicaBigQueryAdapter
from .postgresql.datamart_adapter import TelefonicaDatamartAdapter

__all__ = [
    "TelefonicaBigQueryAdapter",
    "TelefonicaDatamartAdapter",
]
