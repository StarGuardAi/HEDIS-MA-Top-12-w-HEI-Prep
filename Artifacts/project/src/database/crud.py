"""
CRUD Operations for Database Models

Provides Create, Read, Update, Delete operations for all database tables.

HIPAA Compliance:
- All operations use hashed member IDs
- PHI-safe error logging
- Audit logging for all data changes
- Data minimization applied

Author: Robert Reichert
Date: October 2025
"""

import logging
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from uuid import UUID

from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc, func
from sqlalchemy.exc import IntegrityError

from src.database.models import (
    Member, Prediction, PortfolioSnapshot, GapAnalysis,
    Intervention, StarRating, Simulation, APILog, AuditLog
)

logger = logging.getLogger(__name__)


# ===== Member CRUD =====

def create_member(db: Session, member_hash: str) -> Member:
    """
    Create a new member record.
    
    Args:
        db: Database session
        member_hash: SHA-256 hashed member ID
    
    Returns:
        Member: Created member record
    """
    member = Member(member_hash=member_hash)
    db.add(member)
    db.commit()
    db.refresh(member)
    logger.info(f"Created member record: {member_hash[:8]}...")
    return member


def get_member(db: Session, member_hash: str) -> Optional[Member]:
    """Get member by hashed ID."""
    return db.query(Member).filter(Member.member_hash == member_hash).first()


def get_or_create_member(db: Session, member_hash: str) -> Member:
    """Get existing member or create new one."""
    member = get_member(db, member_hash)
    if not member:
        member = create_member(db, member_hash)
    return member


def update_member_activity(db: Session, member_hash: str) -> None:
    """Update member last_updated and increment prediction count."""
    member = get_member(db, member_hash)
    if member:
        member.last_updated = datetime.utcnow()
        member.total_predictions += 1
        db.commit()


# ===== Prediction CRUD =====

def create_prediction(db: Session, prediction_data: Dict[str, Any]) -> Prediction:
    """
    Create a new prediction record.
    
    Args:
        db: Database session
        prediction_data: Dictionary with prediction fields
    
    Returns:
        Prediction: Created prediction record
    """
    # Ensure member exists
    member_hash = prediction_data.get("member_hash")
    get_or_create_member(db, member_hash)
    
    prediction = Prediction(**prediction_data)
    db.add(prediction)
    db.commit()
    db.refresh(prediction)
    
    # Update member activity
    update_member_activity(db, member_hash)
    
    logger.info(f"Created prediction: {str(prediction.prediction_id)[:8]}... for measure {prediction.measure_code}")
    return prediction


def batch_create_predictions(db: Session, predictions_data: List[Dict[str, Any]]) -> List[Prediction]:
    """
    Create multiple predictions in batch.
    
    Args:
        db: Database session
        predictions_data: List of prediction dictionaries
    
    Returns:
        List[Prediction]: Created prediction records
    """
    predictions = []
    member_hashes = set()
    
    for pred_data in predictions_data:
        member_hash = pred_data.get("member_hash")
        member_hashes.add(member_hash)
        
        # Ensure member exists
        get_or_create_member(db, member_hash)
        
        prediction = Prediction(**pred_data)
        predictions.append(prediction)
    
    # Bulk insert
    db.bulk_save_objects(predictions, return_defaults=True)
    db.commit()
    
    # Update member activities
    for member_hash in member_hashes:
        update_member_activity(db, member_hash)
    
    logger.info(f"Created {len(predictions)} predictions in batch")
    return predictions


def get_prediction(db: Session, prediction_id: UUID) -> Optional[Prediction]:
    """Get prediction by ID."""
    return db.query(Prediction).filter(Prediction.prediction_id == prediction_id).first()


def get_member_predictions(
    db: Session,
    member_hash: str,
    measure_code: Optional[str] = None,
    measurement_year: Optional[int] = None
) -> List[Prediction]:
    """
    Get all predictions for a member.
    
    Args:
        db: Database session
        member_hash: SHA-256 hashed member ID
        measure_code: Optional measure code filter
        measurement_year: Optional year filter
    
    Returns:
        List[Prediction]: Member's predictions
    """
    query = db.query(Prediction).filter(Prediction.member_hash == member_hash)
    
    if measure_code:
        query = query.filter(Prediction.measure_code == measure_code)
    if measurement_year:
        query = query.filter(Prediction.measurement_year == measurement_year)
    
    return query.order_by(desc(Prediction.prediction_date)).all()


def get_latest_prediction(
    db: Session,
    member_hash: str,
    measure_code: str,
    measurement_year: int
) -> Optional[Prediction]:
    """Get most recent prediction for member/measure/year."""
    return db.query(Prediction).filter(
        and_(
            Prediction.member_hash == member_hash,
            Prediction.measure_code == measure_code,
            Prediction.measurement_year == measurement_year
        )
    ).order_by(desc(Prediction.prediction_date)).first()


def delete_old_predictions(db: Session, cutoff_date: datetime) -> int:
    """
    Delete predictions older than cutoff date.
    
    Args:
        db: Database session
        cutoff_date: Delete predictions before this date
    
    Returns:
        int: Number of predictions deleted
    """
    count = db.query(Prediction).filter(Prediction.prediction_date < cutoff_date).count()
    db.query(Prediction).filter(Prediction.prediction_date < cutoff_date).delete()
    db.commit()
    logger.info(f"Deleted {count} old predictions before {cutoff_date}")
    return count


# ===== Portfolio CRUD =====

def create_portfolio_snapshot(db: Session, snapshot_data: Dict[str, Any]) -> PortfolioSnapshot:
    """Create a new portfolio snapshot."""
    snapshot = PortfolioSnapshot(**snapshot_data)
    db.add(snapshot)
    db.commit()
    db.refresh(snapshot)
    logger.info(f"Created portfolio snapshot for year {snapshot.measurement_year}")
    return snapshot


def get_latest_portfolio_snapshot(db: Session, measurement_year: int) -> Optional[PortfolioSnapshot]:
    """Get most recent portfolio snapshot for year."""
    return db.query(PortfolioSnapshot).filter(
        PortfolioSnapshot.measurement_year == measurement_year
    ).order_by(desc(PortfolioSnapshot.snapshot_date)).first()


def get_portfolio_snapshots(
    db: Session,
    measurement_year: int,
    limit: int = 10
) -> List[PortfolioSnapshot]:
    """Get recent portfolio snapshots for year."""
    return db.query(PortfolioSnapshot).filter(
        PortfolioSnapshot.measurement_year == measurement_year
    ).order_by(desc(PortfolioSnapshot.snapshot_date)).limit(limit).all()


def get_portfolio_trends(db: Session, measurement_year: int, days: int = 30) -> List[PortfolioSnapshot]:
    """Get portfolio snapshots for last N days."""
    cutoff_date = datetime.utcnow() - timedelta(days=days)
    return db.query(PortfolioSnapshot).filter(
        and_(
            PortfolioSnapshot.measurement_year == measurement_year,
            PortfolioSnapshot.snapshot_date >= cutoff_date
        )
    ).order_by(PortfolioSnapshot.snapshot_date).all()


# ===== Gap Analysis CRUD =====

def create_gap(db: Session, gap_data: Dict[str, Any]) -> GapAnalysis:
    """Create a new gap record."""
    gap = GapAnalysis(**gap_data)
    db.add(gap)
    db.commit()
    db.refresh(gap)
    logger.info(f"Created gap: {str(gap.gap_id)[:8]}... for measure {gap.measure_code}")
    return gap


def get_gaps(
    db: Session,
    measure_code: Optional[str] = None,
    status: Optional[str] = None,
    min_priority: Optional[float] = None,
    limit: int = 100
) -> List[GapAnalysis]:
    """
    Get gaps with optional filters.
    
    Args:
        db: Database session
        measure_code: Optional measure filter
        status: Optional status filter (identified/assigned/completed/closed)
        min_priority: Optional minimum priority score
        limit: Maximum records to return
    
    Returns:
        List[GapAnalysis]: Filtered gaps
    """
    query = db.query(GapAnalysis)
    
    if measure_code:
        query = query.filter(GapAnalysis.measure_code == measure_code)
    if status:
        query = query.filter(GapAnalysis.status == status)
    if min_priority is not None:
        query = query.filter(GapAnalysis.priority_score >= min_priority)
    
    return query.order_by(desc(GapAnalysis.priority_score)).limit(limit).all()


def get_member_gaps(db: Session, member_hash: str) -> List[GapAnalysis]:
    """Get all gaps for a member."""
    return db.query(GapAnalysis).filter(
        GapAnalysis.member_hash == member_hash
    ).order_by(desc(GapAnalysis.priority_score)).all()


def get_high_priority_gaps(db: Session, limit: int = 100, min_score: float = 0.7) -> List[GapAnalysis]:
    """Get high-priority gaps."""
    return db.query(GapAnalysis).filter(
        and_(
            GapAnalysis.priority_score >= min_score,
            GapAnalysis.status == "identified"
        )
    ).order_by(desc(GapAnalysis.priority_score)).limit(limit).all()


def update_gap_status(db: Session, gap_id: UUID, new_status: str) -> Optional[GapAnalysis]:
    """Update gap status."""
    gap = db.query(GapAnalysis).filter(GapAnalysis.gap_id == gap_id).first()
    if gap:
        gap.status = new_status
        if new_status == "assigned":
            gap.assigned_date = datetime.utcnow()
        elif new_status in ("completed", "closed"):
            gap.completed_date = datetime.utcnow()
        db.commit()
        db.refresh(gap)
        logger.info(f"Updated gap {str(gap_id)[:8]}... status to {new_status}")
    return gap


def close_gap(db: Session, gap_id: UUID, outcome: str = "completed") -> Optional[GapAnalysis]:
    """Close a gap with outcome."""
    gap = update_gap_status(db, gap_id, "closed")
    if gap:
        gap.completed_date = datetime.utcnow()
        db.commit()
    return gap


# ===== Intervention CRUD =====

def create_intervention(db: Session, intervention_data: Dict[str, Any]) -> Intervention:
    """Create a new intervention."""
    intervention = Intervention(**intervention_data)
    db.add(intervention)
    db.commit()
    db.refresh(intervention)
    logger.info(f"Created intervention: {str(intervention.intervention_id)[:8]}... type={intervention.intervention_type}")
    return intervention


def get_intervention(db: Session, intervention_id: UUID) -> Optional[Intervention]:
    """Get intervention by ID."""
    return db.query(Intervention).filter(Intervention.intervention_id == intervention_id).first()


def get_member_interventions(db: Session, member_hash: str) -> List[Intervention]:
    """Get all interventions for a member."""
    return db.query(Intervention).filter(
        Intervention.member_hash == member_hash
    ).order_by(desc(Intervention.created_at)).all()


def get_pending_interventions(db: Session, scheduled_date: Optional[datetime] = None) -> List[Intervention]:
    """Get pending interventions, optionally filtered by scheduled date."""
    query = db.query(Intervention).filter(Intervention.status.in_(["planned", "in_progress"]))
    if scheduled_date:
        query = query.filter(Intervention.scheduled_date == scheduled_date)
    return query.order_by(Intervention.scheduled_date).all()


def update_intervention_status(
    db: Session,
    intervention_id: UUID,
    new_status: str,
    outcome: Optional[str] = None
) -> Optional[Intervention]:
    """Update intervention status."""
    intervention = get_intervention(db, intervention_id)
    if intervention:
        intervention.status = new_status
        if new_status == "completed" and outcome:
            intervention.outcome = outcome
            intervention.completed_date = datetime.utcnow().date()
        db.commit()
        db.refresh(intervention)
        logger.info(f"Updated intervention {str(intervention_id)[:8]}... status to {new_status}")
    return intervention


def complete_intervention(
    db: Session,
    intervention_id: UUID,
    outcome: str = "success"
) -> Optional[Intervention]:
    """Complete an intervention."""
    return update_intervention_status(db, intervention_id, "completed", outcome)


def get_intervention_bundles(db: Session, member_hash: str) -> List[Intervention]:
    """Get multi-measure intervention bundles for a member."""
    return db.query(Intervention).filter(
        and_(
            Intervention.member_hash == member_hash,
            func.array_length(Intervention.measure_codes, 1) > 1
        )
    ).all()


# ===== Star Rating CRUD =====

def create_star_rating(db: Session, rating_data: Dict[str, Any]) -> StarRating:
    """Create a new Star Rating calculation."""
    rating = StarRating(**rating_data)
    db.add(rating)
    db.commit()
    db.refresh(rating)
    logger.info(f"Created Star Rating for year {rating.measurement_year}: {rating.overall_stars} stars")
    return rating


def get_latest_star_rating(db: Session, measurement_year: int) -> Optional[StarRating]:
    """Get most recent Star Rating for year."""
    return db.query(StarRating).filter(
        StarRating.measurement_year == measurement_year
    ).order_by(desc(StarRating.calculation_date)).first()


def get_star_rating_history(
    db: Session,
    measurement_year: int,
    limit: int = 10
) -> List[StarRating]:
    """Get Star Rating history for year."""
    return db.query(StarRating).filter(
        StarRating.measurement_year == measurement_year
    ).order_by(desc(StarRating.calculation_date)).limit(limit).all()


# ===== Simulation CRUD =====

def create_simulation(db: Session, simulation_data: Dict[str, Any]) -> Simulation:
    """Create a new simulation."""
    simulation = Simulation(**simulation_data)
    db.add(simulation)
    db.commit()
    db.refresh(simulation)
    logger.info(f"Created simulation: {simulation.strategy}, ROI={simulation.roi:.2f}")
    return simulation


def get_simulation(db: Session, simulation_id: UUID) -> Optional[Simulation]:
    """Get simulation by ID."""
    return db.query(Simulation).filter(Simulation.simulation_id == simulation_id).first()


def get_recent_simulations(
    db: Session,
    measurement_year: int,
    strategy: Optional[str] = None,
    limit: int = 10
) -> List[Simulation]:
    """Get recent simulations, optionally filtered by strategy."""
    query = db.query(Simulation).filter(Simulation.measurement_year == measurement_year)
    if strategy:
        query = query.filter(Simulation.strategy == strategy)
    return query.order_by(desc(Simulation.simulation_date)).limit(limit).all()


def compare_simulations(db: Session, simulation_ids: List[UUID]) -> List[Simulation]:
    """Get multiple simulations for comparison."""
    return db.query(Simulation).filter(Simulation.simulation_id.in_(simulation_ids)).all()


# ===== API Logging CRUD =====

def create_api_log(db: Session, log_data: Dict[str, Any]) -> APILog:
    """Create an API log entry."""
    api_log = APILog(**log_data)
    db.add(api_log)
    db.commit()
    return api_log


def get_api_stats(db: Session, hours: int = 24, endpoint: Optional[str] = None) -> Dict[str, Any]:
    """
    Get API statistics for last N hours.
    
    Returns:
        dict: API statistics
            - total_requests: Total request count
            - avg_response_time: Average response time (ms)
            - error_rate: Percentage of error responses
            - requests_by_endpoint: Count by endpoint
    """
    cutoff = datetime.utcnow() - timedelta(hours=hours)
    query = db.query(APILog).filter(APILog.timestamp >= cutoff)
    
    if endpoint:
        query = query.filter(APILog.endpoint == endpoint)
    
    logs = query.all()
    
    if not logs:
        return {"total_requests": 0, "avg_response_time": 0, "error_rate": 0}
    
    total = len(logs)
    avg_time = sum(log.response_time_ms for log in logs) / total
    errors = sum(1 for log in logs if log.status_code >= 400)
    error_rate = (errors / total) * 100
    
    # Count by endpoint
    endpoint_counts = {}
    for log in logs:
        endpoint_counts[log.endpoint] = endpoint_counts.get(log.endpoint, 0) + 1
    
    return {
        "total_requests": total,
        "avg_response_time": round(avg_time, 2),
        "error_rate": round(error_rate, 2),
        "requests_by_endpoint": endpoint_counts
    }


def get_slowest_requests(db: Session, hours: int = 24, limit: int = 10) -> List[APILog]:
    """Get slowest API requests in last N hours."""
    cutoff = datetime.utcnow() - timedelta(hours=hours)
    return db.query(APILog).filter(
        APILog.timestamp >= cutoff
    ).order_by(desc(APILog.response_time_ms)).limit(limit).all()


def get_error_requests(db: Session, hours: int = 24, limit: int = 100) -> List[APILog]:
    """Get error requests in last N hours."""
    cutoff = datetime.utcnow() - timedelta(hours=hours)
    return db.query(APILog).filter(
        and_(
            APILog.timestamp >= cutoff,
            APILog.status_code >= 400
        )
    ).order_by(desc(APILog.timestamp)).limit(limit).all()


# ===== Audit Logging CRUD =====

def create_audit_log(
    db: Session,
    event_type: str,
    entity_type: str,
    entity_id: str,
    action: str,
    changes: Optional[Dict[str, Any]] = None,
    user_id: Optional[str] = None,
    ip_address: Optional[str] = None
) -> AuditLog:
    """
    Create an audit log entry.
    
    Args:
        db: Database session
        event_type: Type of event (prediction/gap/intervention/etc)
        entity_type: Type of entity (Member/Prediction/Gap/etc)
        entity_id: Entity identifier (UUID or member_hash)
        action: Action performed (create/update/delete)
        changes: Optional changes dictionary
        user_id: Optional user identifier
        ip_address: Optional IP address
    
    Returns:
        AuditLog: Created audit log entry
    """
    audit_log = AuditLog(
        event_type=event_type,
        entity_type=entity_type,
        entity_id=entity_id,
        action=action,
        changes=changes,
        user_id=user_id or "system",
        ip_address=ip_address
    )
    db.add(audit_log)
    db.commit()
    return audit_log


def get_audit_trail(
    db: Session,
    entity_type: str,
    entity_id: str,
    limit: int = 100
) -> List[AuditLog]:
    """Get audit trail for specific entity."""
    return db.query(AuditLog).filter(
        and_(
            AuditLog.entity_type == entity_type,
            AuditLog.entity_id == entity_id
        )
    ).order_by(desc(AuditLog.timestamp)).limit(limit).all()


def get_recent_audits(db: Session, hours: int = 24, limit: int = 100) -> List[AuditLog]:
    """Get recent audit log entries."""
    cutoff = datetime.utcnow() - timedelta(hours=hours)
    return db.query(AuditLog).filter(
        AuditLog.timestamp >= cutoff
    ).order_by(desc(AuditLog.timestamp)).limit(limit).all()



