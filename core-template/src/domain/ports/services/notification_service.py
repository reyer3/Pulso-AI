"""Notification service interface.

Defines the contract for sending notifications and alerts
related to collection activities, system events, and business
rule violations.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from datetime import datetime
from enum import Enum

from ...entities.cliente import Cliente
from ...entities.gestion import Gestion
from ...entities.metrica import Metrica


class NotificationChannel(Enum):
    """Channels available for sending notifications."""
    EMAIL = "email"
    SMS = "sms"
    SLACK = "slack"
    WEBHOOK = "webhook"
    PUSH = "push"
    IN_APP = "in_app"


class NotificationPriority(Enum):
    """Notification priority levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class NotificationService(ABC):
    """Service interface for sending notifications and alerts.
    
    This service handles communication with agents, supervisors,
    and administrators about important events, alerts, and
    system notifications in the debt collection process.
    
    Examples:
        >>> # Send critical client alert
        >>> await notification_service.send_client_alert(
        ...     cliente,
        ...     "High debt client requires immediate attention",
        ...     NotificationPriority.CRITICAL
        ... )
        >>> 
        >>> # Send daily performance summary
        >>> await notification_service.send_performance_summary(
        ...     "ana.garcia@company.com",
        ...     metricas_daily
        ... )
    """
    
    @abstractmethod
    async def send_client_alert(
        self,
        cliente: Cliente,
        message: str,
        priority: NotificationPriority,
        recipients: Optional[List[str]] = None,
        channels: Optional[List[NotificationChannel]] = None
    ) -> bool:
        """Send alert about specific client.
        
        Args:
            cliente: Client that triggered the alert
            message: Alert message content
            priority: Alert priority level
            recipients: Optional specific recipients
            channels: Optional specific channels to use
            
        Returns:
            True if alert was sent successfully
            
        Examples:
            >>> # Critical debt alert
            >>> success = await service.send_client_alert(
            ...     cliente,
            ...     "Client debt exceeded $50,000 - requires legal action",
            ...     NotificationPriority.CRITICAL,
            ...     recipients=["supervisor@company.com"],
            ...     channels=[NotificationChannel.EMAIL, NotificationChannel.SLACK]
            ... )
        """
        pass
    
    @abstractmethod
    async def send_performance_summary(
        self,
        recipient: str,
        metricas: List[Metrica],
        periodo: str = "daily",
        channel: NotificationChannel = NotificationChannel.EMAIL
    ) -> bool:
        """Send performance summary to agent or supervisor.
        
        Args:
            recipient: Email or user ID of recipient
            metricas: List of calculated metrics
            periodo: Period covered ("daily", "weekly", "monthly")
            channel: Communication channel to use
            
        Returns:
            True if summary was sent successfully
            
        Examples:
            >>> daily_metrics = [
            ...     tasa_contactabilidad,
            ...     pdps_por_hora,
            ...     tasa_conversion
            ... ]
            >>> await service.send_performance_summary(
            ...     "ana.garcia@company.com",
            ...     daily_metrics,
            ...     periodo="daily"
            ... )
        """
        pass
    
    @abstractmethod
    async def send_gestion_followup_reminder(
        self,
        gestion: Gestion,
        ejecutivo: str,
        dias_desde_gestion: int,
        channel: NotificationChannel = NotificationChannel.EMAIL
    ) -> bool:
        """Send follow-up reminder for collection activity.
        
        Args:
            gestion: Original collection activity
            ejecutivo: Agent responsible for follow-up
            dias_desde_gestion: Days since original activity
            channel: Communication channel to use
            
        Returns:
            True if reminder was sent successfully
            
        Examples:
            >>> # Remind about payment promise follow-up
            >>> await service.send_gestion_followup_reminder(
            ...     gestion_compromiso,
            ...     "ana.garcia@company.com",
            ...     dias_desde_gestion=3
            ... )
        """
        pass
    
    @abstractmethod
    async def send_threshold_alert(
        self,
        metric_name: str,
        current_value: float,
        threshold_value: float,
        threshold_type: str,  # "above", "below"
        context: Dict[str, Any],
        recipients: List[str]
    ) -> bool:
        """Send alert when metric threshold is violated.
        
        Args:
            metric_name: Name of the metric
            current_value: Current metric value
            threshold_value: Threshold that was violated
            threshold_type: Type of threshold violation
            context: Additional context information
            recipients: List of recipients for the alert
            
        Returns:
            True if alert was sent successfully
            
        Examples:
            >>> # Contactability below threshold
            >>> await service.send_threshold_alert(
            ...     "tasa_contactabilidad",
            ...     current_value=45.0,
            ...     threshold_value=50.0,
            ...     threshold_type="below",
            ...     context={"ejecutivo": "Carlos Ruiz", "fecha": "2025-06-01"},
            ...     recipients=["supervisor@company.com"]
            ... )
        """
        pass
    
    @abstractmethod
    async def send_daily_digest(
        self,
        recipient: str,
        summary_data: Dict[str, Any],
        date: datetime
    ) -> bool:
        """Send daily digest with key metrics and activities.
        
        Args:
            recipient: Recipient email or user ID
            summary_data: Dictionary with summary information
            date: Date for the digest
            
        Returns:
            True if digest was sent successfully
            
        Examples:
            >>> summary = {
            ...     "total_gestiones": 150,
            ...     "contactos_efectivos": 98,
            ...     "compromisos": 35,
            ...     "top_ejecutivo": "Ana García",
            ...     "metricas_destacadas": [metrica1, metrica2]
            ... }
            >>> await service.send_daily_digest(
            ...     "manager@company.com",
            ...     summary,
            ...     datetime.now()
            ... )
        """
        pass
    
    @abstractmethod
    async def send_system_alert(
        self,
        message: str,
        priority: NotificationPriority,
        error_details: Optional[Dict[str, Any]] = None,
        recipients: Optional[List[str]] = None
    ) -> bool:
        """Send system-level alert (errors, warnings, etc.).
        
        Args:
            message: Alert message
            priority: Alert priority level
            error_details: Optional error details
            recipients: Optional specific recipients (defaults to admins)
            
        Returns:
            True if alert was sent successfully
            
        Examples:
            >>> # Database connection error
            >>> await service.send_system_alert(
            ...     "BigQuery connection failed for Movistar client",
            ...     NotificationPriority.CRITICAL,
            ...     error_details={"client_id": "movistar-peru", "error_code": "AUTH_FAILED"}
            ... )
        """
        pass
    
    @abstractmethod
    async def schedule_notification(
        self,
        message: str,
        recipients: List[str],
        send_at: datetime,
        channel: NotificationChannel = NotificationChannel.EMAIL,
        priority: NotificationPriority = NotificationPriority.MEDIUM
    ) -> str:
        """Schedule notification to be sent at specific time.
        
        Args:
            message: Notification message
            recipients: List of recipients
            send_at: When to send the notification
            channel: Communication channel
            priority: Notification priority
            
        Returns:
            Unique ID for the scheduled notification
            
        Examples:
            >>> # Schedule weekly report
            >>> next_monday = datetime(2025, 6, 9, 9, 0)
            >>> notification_id = await service.schedule_notification(
            ...     "Weekly performance report available",
            ...     ["team@company.com"],
            ...     send_at=next_monday
            ... )
        """
        pass
    
    @abstractmethod
    async def cancel_scheduled_notification(self, notification_id: str) -> bool:
        """Cancel previously scheduled notification.
        
        Args:
            notification_id: ID of notification to cancel
            
        Returns:
            True if cancellation was successful
        """
        pass
    
    @abstractmethod
    async def get_notification_preferences(
        self,
        user_id: str
    ) -> Dict[str, Any]:
        """Get user's notification preferences.
        
        Args:
            user_id: User identifier
            
        Returns:
            Dictionary with user preferences
            
        Examples:
            >>> prefs = await service.get_notification_preferences("ana.garcia")
            >>> # Returns: {
            >>> #     "channels": ["email", "slack"],
            >>> #     "daily_digest": True,
            >>> #     "threshold_alerts": True,
            >>> #     "quiet_hours": {"start": "22:00", "end": "08:00"}
            >>> # }
        """
        pass
    
    @abstractmethod
    async def update_notification_preferences(
        self,
        user_id: str,
        preferences: Dict[str, Any]
    ) -> bool:
        """Update user's notification preferences.
        
        Args:
            user_id: User identifier
            preferences: New preferences
            
        Returns:
            True if update was successful
        """
        pass
