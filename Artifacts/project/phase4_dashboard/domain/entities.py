"""
Domain Entities

Core business entities with rich domain logic.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List, Dict, Any
from enum import Enum


class GapStatus(Enum):
    """Gap status enumeration"""
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    CLOSED = "closed"
    EXCLUDED = "excluded"


class InterventionType(Enum):
    """Intervention type enumeration"""
    PHONE_CALL = "phone_call"
    EMAIL = "email"
    SMS = "sms"
    APPOINTMENT = "appointment"
    LAB_ORDER = "lab_order"
    REFERRAL = "referral"


class ReportStatus(Enum):
    """Report status enumeration"""
    DRAFT = "draft"
    PENDING_APPROVAL = "pending_approval"
    APPROVED = "approved"
    SUBMITTED = "submitted"
    ARCHIVED = "archived"


@dataclass
class Member:
    """Member entity"""
    member_id: str
    first_name: str
    last_name: str
    date_of_birth: datetime
    gender: str
    risk_score: float
    state: str
    zip_code: str
    
    # Optional fields
    phone: Optional[str] = None
    email: Optional[str] = None
    preferred_language: Optional[str] = None
    preferred_contact_method: Optional[str] = None
    
    # Metadata
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def full_name(self) -> str:
        """Get member's full name"""
        return f"{self.first_name} {self.last_name}"
    
    def age(self) -> int:
        """Calculate member's age"""
        today = datetime.now()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
        )


@dataclass
class Measure:
    """HEDIS measure entity"""
    measure_id: str
    measure_name: str
    measure_code: str
    description: str
    numerator_definition: str
    denominator_definition: str
    exclusion_criteria: List[str] = field(default_factory=list)
    
    # Star Rating info
    star_rating_weight: int = 1
    domain: str = "Process"
    
    # Metadata
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def is_outcome_measure(self) -> bool:
        """Check if measure is an outcome measure"""
        return self.domain == "Outcome"


@dataclass
class Gap:
    """Care gap entity"""
    gap_id: str
    member_id: str
    measure_id: str
    gap_type: str
    identified_date: datetime
    status: GapStatus
    
    # Gap details
    days_since_identified: int = 0
    priority_score: float = 0.0
    closure_probability: float = 0.0
    
    # Optional fields
    target_closure_date: Optional[datetime] = None
    assigned_coordinator: Optional[str] = None
    notes: Optional[str] = None
    
    # Metadata
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def is_urgent(self) -> bool:
        """Check if gap is urgent"""
        return self.priority_score >= 0.8
    
    def days_until_target(self) -> Optional[int]:
        """Calculate days until target closure date"""
        if not self.target_closure_date:
            return None
        delta = self.target_closure_date - datetime.now()
        return delta.days


@dataclass
class Intervention:
    """Intervention entity"""
    intervention_id: str
    gap_id: str
    member_id: str
    intervention_type: InterventionType
    intervention_date: datetime
    
    # Intervention details
    outcome: str
    notes: Optional[str] = None
    cost: float = 0.0
    
    # Metadata
    created_by: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    
    def is_successful(self) -> bool:
        """Check if intervention was successful"""
        return self.outcome.lower() in ['success', 'closed', 'scheduled']


@dataclass
class Report:
    """Report entity"""
    report_id: str
    report_type: str
    report_name: str
    generated_by: str
    generated_at: datetime
    data_as_of: datetime
    status: ReportStatus
    
    # Report data
    data: Dict[str, Any] = field(default_factory=dict)
    assumptions: Dict[str, Any] = field(default_factory=dict)
    filter_criteria: Dict[str, Any] = field(default_factory=dict)
    
    # Approval workflow
    approved_by: Optional[str] = None
    approved_at: Optional[datetime] = None
    submitted_at: Optional[datetime] = None
    
    # Metadata
    version: int = 1
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def can_be_approved(self) -> bool:
        """Check if report can be approved"""
        return self.status == ReportStatus.PENDING_APPROVAL
    
    def can_be_submitted(self) -> bool:
        """Check if report can be submitted"""
        return self.status in [ReportStatus.APPROVED, ReportStatus.DRAFT]

