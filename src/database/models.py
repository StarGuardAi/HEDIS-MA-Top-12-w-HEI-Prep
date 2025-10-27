"""
SQLAlchemy ORM Models

Defines database tables for HEDIS Star Rating Portfolio Optimizer:
- members: Member tracking (hashed IDs only)
- predictions: Individual measure predictions
- portfolio_snapshots: Portfolio-level summaries
- gap_analysis: Identified gaps and priorities
- interventions: Planned and completed interventions
- star_ratings: Star Rating calculations
- simulations: Scenario modeling results
- api_logs: API request logging
- audit_log: Comprehensive audit trail (7-year retention)

HIPAA Compliance:
- All member IDs are SHA-256 hashed
- No PHI stored in database
- Comprehensive audit logging
- 7-year retention for audit logs

Author: Robert Reichert
Date: October 2025
"""

from datetime import datetime
from typing import List, Optional
import uuid

from sqlalchemy import (
    Column, String, Integer, Float, Boolean, DateTime, Text,
    ForeignKey, UniqueConstraint, Index, ARRAY, JSON, BigInteger,
    Numeric, Date
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func

Base = declarative_base()


class TimestampMixin:
    """Mixin for created_at and updated_at timestamps"""
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class Member(Base, TimestampMixin):
    """
    Member tracking table.
    
    Notes:
        - member_hash is SHA-256 hashed member ID (no PHI)
        - Tracks prediction activity
        - Used for member history queries
    """
    __tablename__ = "members"
    
    member_hash = Column(String(64), primary_key=True, index=True)
    first_seen = Column(DateTime, default=datetime.utcnow, nullable=False)
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    total_predictions = Column(Integer, default=0, nullable=False)
    active = Column(Boolean, default=True, nullable=False)
    
    # Relationships
    predictions = relationship("Prediction", back_populates="member", cascade="all, delete-orphan")
    gaps = relationship("GapAnalysis", back_populates="member", cascade="all, delete-orphan")
    interventions = relationship("Intervention", back_populates="member", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Member(hash={self.member_hash[:8]}..., predictions={self.total_predictions})>"


class Prediction(Base, TimestampMixin):
    """
    Individual measure predictions.
    
    Notes:
        - One prediction per member per measure per year per model version
        - SHAP values stored as JSONB for explainability
        - Links to member via hashed ID
    """
    __tablename__ = "predictions"
    
    prediction_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    member_hash = Column(String(64), ForeignKey("members.member_hash"), nullable=False, index=True)
    measure_code = Column(String(10), nullable=False, index=True)
    measurement_year = Column(Integer, nullable=False, index=True)
    gap_probability = Column(Float, nullable=False)  # 0-1 probability of gap
    risk_tier = Column(String(10), nullable=False)  # high/medium/low
    risk_score = Column(Float, nullable=False)
    shap_values = Column(JSONB, nullable=True)  # SHAP explanation values
    top_features = Column(JSONB, nullable=True)  # Top contributing features
    recommendation = Column(Text, nullable=True)  # Intervention recommendation
    model_version = Column(String(20), nullable=False)
    prediction_date = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    
    # Relationships
    member = relationship("Member", back_populates="predictions")
    
    # Constraints
    __table_args__ = (
        UniqueConstraint('member_hash', 'measure_code', 'measurement_year', 'model_version',
                        name='uq_prediction_member_measure_year_version'),
        Index('ix_predictions_member_measure_year', 'member_hash', 'measure_code', 'measurement_year'),
        Index('ix_predictions_measure_year', 'measure_code', 'measurement_year'),
    )
    
    def __repr__(self):
        return f"<Prediction(id={str(self.prediction_id)[:8]}..., measure={self.measure_code}, prob={self.gap_probability:.2f})>"


class PortfolioSnapshot(Base, TimestampMixin):
    """
    Portfolio-level snapshots.
    
    Notes:
        - Captures portfolio state at point in time
        - Used for trend analysis
        - Generated hourly or on-demand
    """
    __tablename__ = "portfolio_snapshots"
    
    snapshot_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    measurement_year = Column(Integer, nullable=False, index=True)
    snapshot_date = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    total_members = Column(Integer, nullable=False)
    total_gaps = Column(Integer, nullable=False)
    gaps_by_measure = Column(JSONB, nullable=False)  # {"GSD": 100, "KED": 85, ...}
    gaps_by_tier = Column(JSONB, nullable=False)  # {1: 185, 2: 150, ...}
    star_rating_current = Column(Float, nullable=True)
    star_rating_projected = Column(Float, nullable=True)
    estimated_value = Column(Numeric(15, 2), nullable=True)  # Dollar value at risk
    
    # Index for querying recent snapshots
    __table_args__ = (
        Index('ix_portfolio_snapshot_year_date', 'measurement_year', 'snapshot_date'),
    )
    
    def __repr__(self):
        return f"<PortfolioSnapshot(year={self.measurement_year}, members={self.total_members}, gaps={self.total_gaps})>"


class GapAnalysis(Base, TimestampMixin):
    """
    Identified gaps and priorities.
    
    Notes:
        - One record per gap per member per measure
        - Tracks gap lifecycle (identified → assigned → completed/closed)
        - Priority scoring for intervention ranking
    """
    __tablename__ = "gap_analysis"
    
    gap_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    member_hash = Column(String(64), ForeignKey("members.member_hash"), nullable=False, index=True)
    measure_code = Column(String(10), nullable=False, index=True)
    measurement_year = Column(Integer, nullable=False, index=True)
    gap_probability = Column(Float, nullable=False)
    priority_score = Column(Float, nullable=False, index=True)  # For ranking
    intervention_type = Column(String(50), nullable=True)  # lab_bundle/pcp_visit/specialist/medication
    estimated_cost = Column(Numeric(10, 2), nullable=True)
    estimated_value = Column(Numeric(10, 2), nullable=True)
    status = Column(String(20), default="identified", nullable=False, index=True)  # identified/assigned/completed/closed
    assigned_date = Column(DateTime, nullable=True)
    completed_date = Column(DateTime, nullable=True)
    
    # Relationships
    member = relationship("Member", back_populates="gaps")
    interventions = relationship("Intervention", back_populates="gap")
    
    # Indexes for common queries
    __table_args__ = (
        Index('ix_gaps_member_measure', 'member_hash', 'measure_code'),
        Index('ix_gaps_status_priority', 'status', 'priority_score'),
        Index('ix_gaps_measure_year', 'measure_code', 'measurement_year'),
    )
    
    def __repr__(self):
        return f"<GapAnalysis(id={str(self.gap_id)[:8]}..., measure={self.measure_code}, priority={self.priority_score:.2f}, status={self.status})>"


class Intervention(Base, TimestampMixin):
    """
    Planned and completed interventions.
    
    Notes:
        - Can address multiple measures (intervention bundles)
        - Tracks ROI and outcomes
        - Links to gap_analysis for gap closure tracking
    """
    __tablename__ = "interventions"
    
    intervention_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    gap_id = Column(UUID(as_uuid=True), ForeignKey("gap_analysis.gap_id"), nullable=True)  # Nullable for multi-gap bundles
    member_hash = Column(String(64), ForeignKey("members.member_hash"), nullable=False, index=True)
    measure_codes = Column(ARRAY(String), nullable=False)  # Multiple measures for bundles
    intervention_type = Column(String(50), nullable=False)  # lab_bundle/pcp_visit/specialist/medication
    description = Column(Text, nullable=True)
    estimated_cost = Column(Numeric(10, 2), nullable=True)
    estimated_value = Column(Numeric(10, 2), nullable=True)  # Total value of all gaps
    roi = Column(Float, nullable=True)  # estimated_value / estimated_cost
    status = Column(String(20), default="planned", nullable=False, index=True)  # planned/in_progress/completed/cancelled
    scheduled_date = Column(Date, nullable=True, index=True)
    completed_date = Column(Date, nullable=True)
    outcome = Column(String(20), nullable=True)  # success/partial/failed
    
    # Relationships
    member = relationship("Member", back_populates="interventions")
    gap = relationship("GapAnalysis", back_populates="interventions")
    
    # Indexes
    __table_args__ = (
        Index('ix_interventions_member_status', 'member_hash', 'status'),
        Index('ix_interventions_scheduled_date', 'scheduled_date'),
    )
    
    def __repr__(self):
        return f"<Intervention(id={str(self.intervention_id)[:8]}..., type={self.intervention_type}, status={self.status}, roi={self.roi})>"


class StarRating(Base, TimestampMixin):
    """
    Star Rating calculations.
    
    Notes:
        - Stores historical Star Rating calculations
        - Includes HEI adjustment if applicable
        - Used for trend analysis
    """
    __tablename__ = "star_ratings"
    
    rating_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    measurement_year = Column(Integer, nullable=False, index=True)
    calculation_date = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    overall_stars = Column(Float, nullable=False)
    total_points = Column(Float, nullable=False)
    measure_stars = Column(JSONB, nullable=False)  # {"GSD": 4.5, "KED": 4.0, ...}
    measure_rates = Column(JSONB, nullable=False)  # {"GSD": 0.85, "KED": 0.80, ...}
    hei_factor = Column(Float, nullable=True)  # Health Equity Index factor
    hei_adjusted = Column(Boolean, default=False, nullable=False)
    revenue_estimate = Column(Numeric(15, 2), nullable=True)
    bonus_tier = Column(String(10), nullable=True)  # CMS bonus tier
    
    __table_args__ = (
        Index('ix_star_rating_year_date', 'measurement_year', 'calculation_date'),
    )
    
    def __repr__(self):
        return f"<StarRating(year={self.measurement_year}, stars={self.overall_stars}, hei_adjusted={self.hei_adjusted})>"


class Simulation(Base, TimestampMixin):
    """
    Scenario modeling results.
    
    Notes:
        - Stores simulation parameters and results
        - Used for strategy comparison
        - Enables "what-if" analysis
    """
    __tablename__ = "simulations"
    
    simulation_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    measurement_year = Column(Integer, nullable=False, index=True)
    simulation_date = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    strategy = Column(String(50), nullable=False, index=True)  # triple_weighted/new_2025/multi_measure/balanced
    closure_rate = Column(Float, nullable=False)  # Gap closure rate (0-1)
    baseline_stars = Column(Float, nullable=False)
    projected_stars = Column(Float, nullable=False)
    revenue_impact = Column(Numeric(15, 2), nullable=False)
    investment_required = Column(Numeric(15, 2), nullable=False)
    roi = Column(Float, nullable=False)
    gaps_closed = Column(Integer, nullable=False)
    members_impacted = Column(Integer, nullable=False)
    scenario_details = Column(JSONB, nullable=True)  # Full scenario parameters
    
    __table_args__ = (
        Index('ix_simulation_year_strategy', 'measurement_year', 'strategy'),
        Index('ix_simulation_date', 'simulation_date'),
    )
    
    def __repr__(self):
        return f"<Simulation(id={str(self.simulation_id)[:8]}..., strategy={self.strategy}, roi={self.roi:.2f})>"


class APILog(Base):
    """
    API request logging.
    
    Notes:
        - Tracks all API requests
        - PHI-safe (no member IDs logged)
        - Partitioned by month for performance
        - Used for monitoring and analytics
    """
    __tablename__ = "api_logs"
    
    log_id = Column(BigInteger, primary_key=True, autoincrement=True)
    request_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    endpoint = Column(String(200), nullable=False, index=True)
    method = Column(String(10), nullable=False)
    api_key_hash = Column(String(64), nullable=True, index=True)  # Hashed API key
    status_code = Column(Integer, nullable=False)
    response_time_ms = Column(Integer, nullable=False)
    prediction_count = Column(Integer, default=0, nullable=False)
    error_message = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    
    __table_args__ = (
        Index('ix_api_logs_timestamp', 'timestamp'),
        Index('ix_api_logs_endpoint_timestamp', 'endpoint', 'timestamp'),
    )
    
    def __repr__(self):
        return f"<APILog(endpoint={self.endpoint}, status={self.status_code}, time={self.response_time_ms}ms)>"


class AuditLog(Base):
    """
    Comprehensive audit trail.
    
    Notes:
        - Tracks all data changes
        - 7-year retention for HIPAA compliance
        - Partitioned by month for performance
        - PHI-safe (uses hashed IDs)
    """
    __tablename__ = "audit_log"
    
    audit_id = Column(BigInteger, primary_key=True, autoincrement=True)
    event_type = Column(String(50), nullable=False, index=True)  # prediction/gap/intervention/etc
    entity_type = Column(String(50), nullable=False, index=True)  # Member/Prediction/Gap/etc
    entity_id = Column(String(100), nullable=False)  # UUID or member_hash
    action = Column(String(50), nullable=False)  # create/update/delete
    user_id = Column(String(100), nullable=True)  # User/system that performed action
    changes = Column(JSONB, nullable=True)  # What changed (before/after)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    ip_address = Column(String(45), nullable=True)  # IPv6 compatible
    
    __table_args__ = (
        Index('ix_audit_log_timestamp', 'timestamp'),
        Index('ix_audit_log_event_type', 'event_type'),
        Index('ix_audit_log_entity', 'entity_type', 'entity_id'),
    )
    
    def __repr__(self):
        return f"<AuditLog(event={self.event_type}, entity={self.entity_type}, action={self.action})>"


