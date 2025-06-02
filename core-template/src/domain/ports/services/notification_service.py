"""Notification service interface.

Defines contracts for alerts, notifications, and real-time communication.
Handles operational alerts, performance notifications, and system events.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from datetime import datetime
from enum import Enum
from dataclasses import dataclass


class NotificationPriority(Enum):
    """Notification priority levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class NotificationChannel(Enum):
    """Notification delivery channels."""
    EMAIL = "email"
    SMS = "sms"
    SLACK = "slack"
    WEBHOOK = "webhook"
    IN_APP = "in_app"
    PUSH = "push"


@dataclass
class NotificationTemplate:
    """Notification message template."""
    id: str
    title: str
    message: str
    priority: NotificationPriority
    channels: List[NotificationChannel]
    variables: Dict[str, str]  # Template variables


@dataclass
class NotificationRequest:
    """Notification delivery request."""
    template_id: str
    recipient: str
    variables: Dict[str, Any]
    priority: NotificationPriority
    channels: List[NotificationChannel]
    scheduled_for: Optional[datetime] = None


class NotificationService(ABC):
    """Service interface for notifications and alerts.
    
    This service handles all types of notifications including
    operational alerts, performance notifications, and system events.
    
    Key Features:
        - Multi-channel delivery (email, SMS, Slack, etc.)
        - Template-based messages
        - Priority-based routing
        - Scheduled notifications
        - Performance alert automation
    
    Examples:
        >>> # Send performance alert
        >>> await notification_service.send_performance_alert(
        ...     "low_contact_rate",
        ...     "Ana García",
        ...     {"rate": 45.2, "threshold": 60.0}
        ... )
        >>> 
        >>> # Send daily summary
        >>> await notification_service.send_daily_summary(
        ...     "supervisor@company.com",
        ...     summary_data
        ... )
    """
    
    @abstractmethod
    async def send_notification(
        self, 
        request: NotificationRequest
    ) -> str:
        """Send notification through specified channels.
        
        Delivers notification using template and variables
        through one or more communication channels.
        
        Args:
            request: Notification delivery request
            
        Returns:
            Notification ID for tracking
            
        Raises:
            NotificationError: If delivery fails
            
        Examples:
            >>> request = NotificationRequest(
            ...     template_id="performance_alert",
            ...     recipient="manager@company.com",
            ...     variables={"agent": "Ana García", "metric": "contact_rate"},
            ...     priority=NotificationPriority.HIGH,
            ...     channels=[NotificationChannel.EMAIL, NotificationChannel.SLACK]
            ... )
            >>> notification_id = await service.send_notification(request)
        """
        pass
    
    @abstractmethod
    async def send_performance_alert(
        self,
        alert_type: str,
        ejecutivo: str,
        metric_data: Dict[str, Any],
        priority: NotificationPriority = NotificationPriority.MEDIUM
    ) -> str:
        """Send performance-related alert.
        
        Sends automated alert when agent performance
        falls below or exceeds defined thresholds.
        
        Args:
            alert_type: Type of performance alert
            ejecutivo: Agent name
            metric_data: Performance metric data
            priority: Alert priority level
            
        Returns:
            Notification ID
            
        Alert Types:
            - "low_contact_rate": Contact rate below threshold
            - "high_productivity": Exceptional performance
            - "missed_target": Daily/weekly target missed
            - "commitment_overdue": Payment commitments overdue
            
        Examples:
            >>> # Low contact rate alert
            >>> await service.send_performance_alert(
            ...     "low_contact_rate",
            ...     "Carlos López",
            ...     {
            ...         "current_rate": 45.2,
            ...         "threshold": 60.0,
            ...         "period": "today",
            ...         "total_attempts": 25
            ...     },
            ...     NotificationPriority.HIGH
            ... )
        """
        pass
    
    @abstractmethod
    async def send_daily_summary(
        self,
        recipient: str,
        summary_data: Dict[str, Any]
    ) -> str:
        """Send daily performance summary.
        
        Sends comprehensive daily summary report
        to supervisors and managers.
        
        Args:
            recipient: Email address of recipient
            summary_data: Daily performance data
            
        Returns:
            Notification ID
            
        Summary Data Structure:
            {
                "date": "2024-06-01",
                "team_metrics": {
                    "total_gestiones": 156,
                    "total_contactos": 89,
                    "total_compromisos": 34,
                    "tasa_exito": 21.8
                },
                "top_performers": [
                    {"ejecutivo": "Ana García", "compromisos": 8},
                    {"ejecutivo": "Carlos López", "compromisos": 6}
                ],
                "alerts": [
                    "Low contact rate: Juan Pérez (45%)"
                ]
            }
            
        Examples:
            >>> summary = {
            ...     "date": "2024-06-01",
            ...     "team_metrics": {"total_gestiones": 156, "tasa_exito": 21.8},
            ...     "top_performers": [{"ejecutivo": "Ana García", "compromisos": 8}]
            ... }
            >>> await service.send_daily_summary(
            ...     "supervisor@company.com", summary
            ... )
        """
        pass
    
    @abstractmethod
    async def send_system_alert(
        self,
        alert_type: str,
        message: str,
        priority: NotificationPriority = NotificationPriority.MEDIUM,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """Send system-level alert.
        
        Sends technical alerts about system status,
        errors, or operational issues.
        
        Args:
            alert_type: Type of system alert
            message: Alert message
            priority: Alert priority
            metadata: Additional alert context
            
        Returns:
            Notification ID
            
        System Alert Types:
            - "database_connection_error": DB connectivity issues
            - "high_error_rate": Increased error frequency
            - "slow_performance": System performance degradation
            - "data_sync_failure": ETL or sync process failure
            
        Examples:
            >>> # Database connection alert
            >>> await service.send_system_alert(
            ...     "database_connection_error",
            ...     "Unable to connect to BigQuery for client movistar-peru",
            ...     NotificationPriority.CRITICAL,
            ...     {"client_id": "movistar-peru", "error_code": "CONN_TIMEOUT"}
            ... )
        """
        pass
    
    @abstractmethod
    async def schedule_notification(
        self,
        request: NotificationRequest,
        scheduled_for: datetime
    ) -> str:
        """Schedule notification for future delivery.
        
        Schedules notification to be sent at specified time.
        Useful for reminders, follow-ups, and recurring reports.
        
        Args:
            request: Notification to schedule
            scheduled_for: When to send the notification
            
        Returns:
            Scheduled notification ID
            
        Examples:
            >>> # Schedule weekly report
            >>> next_monday = datetime.now() + timedelta(days=7)
            >>> request = NotificationRequest(
            ...     template_id="weekly_report",
            ...     recipient="manager@company.com",
            ...     variables={"week_ending": "2024-06-07"},
            ...     priority=NotificationPriority.LOW,
            ...     channels=[NotificationChannel.EMAIL]
            ... )
            >>> scheduled_id = await service.schedule_notification(
            ...     request, next_monday
            ... )
        """
        pass
    
    @abstractmethod
    async def cancel_notification(self, notification_id: str) -> bool:
        """Cancel scheduled notification.
        
        Cancels a previously scheduled notification
        before it is delivered.
        
        Args:
            notification_id: ID of notification to cancel
            
        Returns:
            True if cancellation successful
            
        Examples:
            >>> # Cancel scheduled notification
            >>> success = await service.cancel_notification("notif_12345")
            >>> assert success
        """
        pass
    
    @abstractmethod
    async def get_notification_templates(self) -> List[NotificationTemplate]:
        """Get available notification templates.
        
        Returns list of all available notification templates
        for different types of messages.
        
        Returns:
            List of notification templates
            
        Examples:
            >>> templates = await service.get_notification_templates()
            >>> performance_templates = [
            ...     t for t in templates 
            ...     if "performance" in t.id
            ... ]
        """
        pass
    
    @abstractmethod
    async def get_notification_history(
        self,
        recipient: Optional[str] = None,
        start_date: Optional[datetime] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """Get notification delivery history.
        
        Returns history of sent notifications with
        delivery status and metadata.
        
        Args:
            recipient: Filter by recipient
            start_date: Filter by send date
            limit: Maximum results
            
        Returns:
            List of notification history records
            
        Examples:
            >>> # Recent notifications for manager
            >>> history = await service.get_notification_history(
            ...     recipient="manager@company.com",
            ...     start_date=datetime.now() - timedelta(days=7)
            ... )
        """
        pass
