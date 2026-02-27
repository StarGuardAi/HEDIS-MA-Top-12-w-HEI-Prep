"""
Care Gap Closure Workflow System
End-to-end workflow management for gap closure
"""
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import pandas as pd

# Optional ML integration
try:
    from utils.ml_prediction_service import GapClosurePredictionService
    ML_AVAILABLE = True
except ImportError:
    ML_AVAILABLE = False
    GapClosurePredictionService = None


class GapStatus(Enum):
    """Gap status enumeration."""
    IDENTIFIED = "Identified"
    ASSIGNED = "Assigned"
    OUTREACH_PLANNED = "Outreach Planned"
    CONTACT_ATTEMPTED = "Contact Attempted"
    INTERVENTION_IN_PROGRESS = "Intervention In Progress"
    PENDING_VERIFICATION = "Pending Verification"
    CLOSED = "Closed"
    EXCLUDED = "Excluded"
    LOST_TO_FOLLOWUP = "Lost to Follow-up"


class Urgency(Enum):
    """Gap urgency levels."""
    CRITICAL = "Critical"  # < 30 days to deadline
    HIGH = "High"  # 30-60 days
    MEDIUM = "Medium"  # 60-90 days
    LOW = "Low"  # > 90 days


class Priority(Enum):
    """Gap priority levels."""
    P1 = "P1"  # Highest value, highest urgency
    P2 = "P2"  # High value or high urgency
    P3 = "P3"  # Medium value and urgency
    P4 = "P4"  # Low value or low urgency


@dataclass
class Gap:
    """Care gap data structure."""
    gap_id: str
    member_id: str
    measure_id: str
    gap_reason: str
    identified_date: datetime
    deadline_date: datetime
    urgency: Urgency
    priority: Priority
    priority_score: float
    assigned_coordinator: Optional[str] = None
    status: GapStatus = GapStatus.IDENTIFIED
    value_score: float = 0.0
    closure_probability: float = 0.0
    metadata: Dict = field(default_factory=dict)


@dataclass
class OutreachPlan:
    """Outreach planning data structure."""
    gap_id: str
    optimal_contact_time: datetime
    preferred_channel: str  # Phone, SMS, Email, Mail
    language_preference: str
    script_template: str
    prior_contact_history: List[Dict] = field(default_factory=list)
    barriers: List[str] = field(default_factory=list)
    notes: str = ""


@dataclass
class Intervention:
    """Intervention tracking data structure."""
    intervention_id: str
    gap_id: str
    coordinator_id: str
    contact_date: datetime
    contact_method: str
    contact_outcome: str  # Reached, Voicemail, No Answer, Busy
    conversation_notes: str
    barriers_identified: List[str] = field(default_factory=list)
    follow_up_date: Optional[datetime] = None
    follow_up_reason: Optional[str] = None
    escalation_triggered: bool = False
    escalation_reason: Optional[str] = None


@dataclass
class ClosureVerification:
    """Closure verification data structure."""
    gap_id: str
    closure_date: datetime
    closure_method: str  # Claims, Lab Results, Manual
    verification_source: str
    verified_by: str
    supervisor_approval: bool = False
    exclusion_applied: bool = False
    exclusion_reason: Optional[str] = None
    notes: str = ""


class GapWorkflowManager:
    """
    End-to-end care gap closure workflow manager.
    Handles all stages from identification to closure.
    """
    
    def __init__(self):
        self.gaps: Dict[str, Gap] = {}
        self.outreach_plans: Dict[str, OutreachPlan] = {}
        self.interventions: Dict[str, List[Intervention]] = {}
        self.verifications: Dict[str, ClosureVerification] = {}
        
        # ML prediction service (optional)
        self.prediction_service = None
        if ML_AVAILABLE:
            try:
                self.prediction_service = GapClosurePredictionService()
            except:
                pass
    
    def identify_gap(
        self,
        member_id: str,
        measure_id: str,
        gap_reason: str,
        deadline_date: datetime,
        metadata: Optional[Dict] = None
    ) -> Gap:
        """
        Stage 1: Gap Identification
        Auto-detect and classify gaps.
        """
        gap_id = f"GAP_{member_id}_{measure_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # Calculate urgency
        days_to_deadline = (deadline_date - datetime.now()).days
        if days_to_deadline < 30:
            urgency = Urgency.CRITICAL
        elif days_to_deadline < 60:
            urgency = Urgency.HIGH
        elif days_to_deadline < 90:
            urgency = Urgency.MEDIUM
        else:
            urgency = Urgency.LOW
        
        # Calculate priority score (value + urgency)
        value_score = self._calculate_value_score(measure_id, member_id, metadata or {})
        urgency_score = self._calculate_urgency_score(urgency, days_to_deadline)
        priority_score = (value_score * 0.6) + (urgency_score * 0.4)
        
        # Assign priority
        if priority_score >= 0.8:
            priority = Priority.P1
        elif priority_score >= 0.6:
            priority = Priority.P2
        elif priority_score >= 0.4:
            priority = Priority.P3
        else:
            priority = Priority.P4
        
        # Calculate closure probability (use ML if available)
        if self.prediction_service:
            try:
                # Use ML prediction
                prediction = self.prediction_service.predict_single(
                    member_id=member_id,
                    gap_data={
                        'measure_id': measure_id,
                        'gap_reason': gap_reason,
                        'deadline_date': deadline_date
                    },
                    member_data=metadata.get('member_data', {}),
                    engagement_data=metadata.get('engagement_data', {}),
                    operational_data=metadata.get('operational_data', {})
                )
                closure_probability = prediction['closure_probability'] / 100.0
            except:
                closure_probability = self._estimate_closure_probability(member_id, measure_id, gap_reason)
        else:
            closure_probability = self._estimate_closure_probability(member_id, measure_id, gap_reason)
        
        gap = Gap(
            gap_id=gap_id,
            member_id=member_id,
            measure_id=measure_id,
            gap_reason=gap_reason,
            identified_date=datetime.now(),
            deadline_date=deadline_date,
            urgency=urgency,
            priority=priority,
            priority_score=priority_score,
            status=GapStatus.IDENTIFIED,
            value_score=value_score,
            closure_probability=closure_probability,
            metadata=metadata or {}
        )
        
        self.gaps[gap_id] = gap
        
        # Auto-assign to coordinator
        coordinator = self._auto_assign_coordinator(gap)
        if coordinator:
            gap.assigned_coordinator = coordinator
            gap.status = GapStatus.ASSIGNED
        
        return gap
    
    def plan_outreach(self, gap_id: str, member_data: Dict) -> OutreachPlan:
        """
        Stage 2: Outreach Planning
        Create optimal outreach plan.
        """
        if gap_id not in self.gaps:
            raise ValueError(f"Gap {gap_id} not found")
        
        gap = self.gaps[gap_id]
        
        # Predict optimal contact time
        optimal_time = self._predict_optimal_contact_time(member_data)
        
        # Determine preferred channel
        preferred_channel = self._determine_preferred_channel(member_data)
        
        # Get language preference
        language = member_data.get("language_preference", "English")
        
        # Get script template
        script_template = self._get_script_template(gap.measure_id, gap.gap_reason)
        
        # Get prior contact history
        prior_history = self._get_prior_contact_history(gap.member_id)
        
        # Identify barriers
        barriers = self._identify_barriers(member_data)
        
        plan = OutreachPlan(
            gap_id=gap_id,
            optimal_contact_time=optimal_time,
            preferred_channel=preferred_channel,
            language_preference=language,
            script_template=script_template,
            prior_contact_history=prior_history,
            barriers=barriers
        )
        
        self.outreach_plans[gap_id] = plan
        gap.status = GapStatus.OUTREACH_PLANNED
        
        return plan
    
    def log_intervention(
        self,
        gap_id: str,
        coordinator_id: str,
        contact_method: str,
        contact_outcome: str,
        conversation_notes: str,
        barriers: Optional[List[str]] = None
    ) -> Intervention:
        """
        Stage 3: Intervention Tracking
        Log contact attempts and outcomes.
        """
        if gap_id not in self.gaps:
            raise ValueError(f"Gap {gap_id} not found")
        
        gap = self.gaps[gap_id]
        
        intervention_id = f"INT_{gap_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # Determine follow-up
        follow_up_date, follow_up_reason = self._determine_follow_up(
            contact_outcome, gap.deadline_date
        )
        
        # Check escalation triggers
        escalation_triggered, escalation_reason = self._check_escalation_triggers(
            gap, contact_outcome, barriers or []
        )
        
        intervention = Intervention(
            intervention_id=intervention_id,
            gap_id=gap_id,
            coordinator_id=coordinator_id,
            contact_date=datetime.now(),
            contact_method=contact_method,
            contact_outcome=contact_outcome,
            conversation_notes=conversation_notes,
            barriers_identified=barriers or [],
            follow_up_date=follow_up_date,
            follow_up_reason=follow_up_reason,
            escalation_triggered=escalation_triggered,
            escalation_reason=escalation_reason
        )
        
        if gap_id not in self.interventions:
            self.interventions[gap_id] = []
        self.interventions[gap_id].append(intervention)
        
        gap.status = GapStatus.CONTACT_ATTEMPTED
        
        if contact_outcome == "Reached":
            gap.status = GapStatus.INTERVENTION_IN_PROGRESS
        
        return intervention
    
    def verify_closure(
        self,
        gap_id: str,
        closure_method: str,
        verification_source: str,
        verified_by: str,
        supervisor_approval: bool = False,
        exclusion_applied: bool = False,
        exclusion_reason: Optional[str] = None
    ) -> ClosureVerification:
        """
        Stage 4: Closure Verification
        Verify gap closure with evidence.
        """
        if gap_id not in self.gaps:
            raise ValueError(f"Gap {gap_id} not found")
        
        gap = self.gaps[gap_id]
        
        # Auto-close if evidence is strong
        auto_close = closure_method in ["Claims", "Lab Results"] and not exclusion_applied
        
        if not auto_close and not supervisor_approval:
            gap.status = GapStatus.PENDING_VERIFICATION
            return None
        
        verification = ClosureVerification(
            gap_id=gap_id,
            closure_date=datetime.now(),
            closure_method=closure_method,
            verification_source=verification_source,
            verified_by=verified_by,
            supervisor_approval=supervisor_approval,
            exclusion_applied=exclusion_applied,
            exclusion_reason=exclusion_reason
        )
        
        self.verifications[gap_id] = verification
        
        if exclusion_applied:
            gap.status = GapStatus.EXCLUDED
        else:
            gap.status = GapStatus.CLOSED
        
        return verification
    
    def get_workflow_status(self, gap_id: str) -> Dict:
        """Get complete workflow status for a gap."""
        if gap_id not in self.gaps:
            return {}
        
        gap = self.gaps[gap_id]
        outreach_plan = self.outreach_plans.get(gap_id)
        interventions = self.interventions.get(gap_id, [])
        verification = self.verifications.get(gap_id)
        
        return {
            "gap": gap,
            "outreach_plan": outreach_plan,
            "interventions": interventions,
            "verification": verification,
            "current_stage": gap.status.value,
            "days_in_workflow": (datetime.now() - gap.identified_date).days
        }
    
    # Helper methods
    
    def _calculate_value_score(self, measure_id: str, member_id: str, metadata: Dict) -> float:
        """Calculate value score for gap (0-1)."""
        # Factors: Star Rating impact, quality bonus, member risk
        base_score = 0.5
        
        # Star Rating weight
        star_weights = {"HBA1C": 0.15, "BP": 0.12, "COL": 0.10}
        star_weight = star_weights.get(measure_id, 0.08)
        base_score += star_weight * 2
        
        # Member risk
        risk_score = metadata.get("risk_score", 0.5)
        base_score += risk_score * 0.2
        
        return min(1.0, base_score)
    
    def _calculate_urgency_score(self, urgency: Urgency, days_to_deadline: int) -> float:
        """Calculate urgency score (0-1)."""
        urgency_scores = {
            Urgency.CRITICAL: 1.0,
            Urgency.HIGH: 0.75,
            Urgency.MEDIUM: 0.5,
            Urgency.LOW: 0.25
        }
        return urgency_scores.get(urgency, 0.5)
    
    def _estimate_closure_probability(self, member_id: str, measure_id: str, gap_reason: str) -> float:
        """Estimate closure probability based on historical data."""
        # Simplified - would use ML model in production
        base_probability = 0.6
        
        # Gap reason factors
        reason_factors = {
            "Lab Pending": 0.2,
            "Not Scheduled": 0.1,
            "Missed Appointment": -0.1,
            "Provider Delay": -0.15
        }
        base_probability += reason_factors.get(gap_reason, 0)
        
        return max(0.0, min(1.0, base_probability))
    
    def _auto_assign_coordinator(self, gap: Gap) -> Optional[str]:
        """Auto-assign gap to appropriate coordinator."""
        # Simplified - would use workload balancing algorithm
        # Consider: coordinator capacity, expertise, geography
        coordinators = ["COORD001", "COORD002", "COORD003"]
        
        # Assign based on priority
        if gap.priority == Priority.P1:
            return coordinators[0]  # Senior coordinator
        elif gap.priority == Priority.P2:
            return coordinators[1]
        else:
            return coordinators[2]
    
    def _predict_optimal_contact_time(self, member_data: Dict) -> datetime:
        """Predict optimal contact time."""
        # Simplified - would use ML model
        # Consider: time zone, historical contact patterns, member preferences
        base_time = datetime.now().replace(hour=10, minute=0, second=0)
        
        # Adjust based on time zone
        timezone_offset = member_data.get("timezone_offset", 0)
        base_time += timedelta(hours=timezone_offset)
        
        return base_time
    
    def _determine_preferred_channel(self, member_data: Dict) -> str:
        """Determine preferred communication channel."""
        # Check member preferences
        if member_data.get("prefers_sms"):
            return "SMS"
        elif member_data.get("prefers_email"):
            return "Email"
        elif member_data.get("prefers_mail"):
            return "Mail"
        else:
            return "Phone"
    
    def _get_script_template(self, measure_id: str, gap_reason: str) -> str:
        """Get script template for measure and gap reason."""
        templates = {
            ("HBA1C", "Not Scheduled"): "Hi, this is [Name] from [Plan]. We'd like to help you schedule your HbA1c test...",
            ("BP", "Missed Appointment"): "Hi, we noticed you missed your blood pressure check appointment...",
            ("COL", "Lab Pending"): "Hi, we're following up on your colorectal cancer screening..."
        }
        return templates.get((measure_id, gap_reason), "Standard outreach script")
    
    def _get_prior_contact_history(self, member_id: str) -> List[Dict]:
        """Get prior contact history for member."""
        # Would query database
        return []
    
    def _identify_barriers(self, member_data: Dict) -> List[str]:
        """Identify potential barriers."""
        barriers = []
        
        if member_data.get("transportation_issues"):
            barriers.append("Transportation")
        if member_data.get("language_barrier"):
            barriers.append("Language")
        if member_data.get("financial_concerns"):
            barriers.append("Financial")
        if member_data.get("health_literacy"):
            barriers.append("Health Literacy")
        
        return barriers
    
    def _determine_follow_up(self, contact_outcome: str, deadline: datetime) -> Tuple[Optional[datetime], Optional[str]]:
        """Determine if follow-up is needed."""
        if contact_outcome == "Reached":
            return None, None
        elif contact_outcome == "Voicemail":
            return datetime.now() + timedelta(days=2), "Voicemail left, follow up in 2 days"
        elif contact_outcome == "No Answer":
            return datetime.now() + timedelta(days=1), "No answer, try again tomorrow"
        else:
            return datetime.now() + timedelta(days=3), "Follow up in 3 days"
    
    def _check_escalation_triggers(
        self,
        gap: Gap,
        contact_outcome: str,
        barriers: List[str]
    ) -> Tuple[bool, Optional[str]]:
        """Check if escalation is needed."""
        # Escalate if critical and multiple failed attempts
        if gap.urgency == Urgency.CRITICAL and contact_outcome != "Reached":
            return True, "Critical gap, multiple failed contact attempts"
        
        # Escalate if multiple barriers
        if len(barriers) >= 3:
            return True, "Multiple barriers identified, requires supervisor support"
        
        return False, None

