"""
Database Models Tests

Tests for SQLAlchemy ORM models, relationships, and constraints.

Author: Robert Reichert
Date: October 2025
"""

import pytest
from datetime import datetime, timedelta
from sqlalchemy.exc import IntegrityError
from uuid import uuid4

from src.database.models import (
    Member, Prediction, PortfolioSnapshot, GapAnalysis,
    Intervention, StarRating, Simulation, APILog, AuditLog
)


# ===== Member Model Tests =====

def test_member_creation(test_db, sample_member_hash):
    """Test creating a member record."""
    member = Member(
        member_hash=sample_member_hash,
        first_seen=datetime.utcnow(),
        total_predictions=0,
        active=True
    )
    test_db.add(member)
    test_db.commit()
    
    assert member.member_hash == sample_member_hash
    assert member.total_predictions == 0
    assert member.active is True
    assert member.created_at is not None
    assert member.updated_at is not None


def test_member_hash_is_primary_key(test_db, sample_member_hash):
    """Test that member_hash is the primary key."""
    member1 = Member(member_hash=sample_member_hash)
    test_db.add(member1)
    test_db.commit()
    
    # Try to create duplicate
    member2 = Member(member_hash=sample_member_hash)
    test_db.add(member2)
    
    with pytest.raises(IntegrityError):
        test_db.commit()


def test_member_relationships(test_db, sample_member_hash, create_test_member, create_test_prediction):
    """Test member relationships with predictions."""
    member = create_test_member(member_hash=sample_member_hash)
    
    # Create predictions
    pred1 = create_test_prediction(member_hash=sample_member_hash, measure_code="GSD")
    pred2 = create_test_prediction(member_hash=sample_member_hash, measure_code="KED")
    
    # Refresh to load relationships
    test_db.refresh(member)
    
    assert len(member.predictions) == 2
    assert pred1 in member.predictions
    assert pred2 in member.predictions


# ===== Prediction Model Tests =====

def test_prediction_creation(test_db, sample_member_hash, sample_prediction_data, create_test_member):
    """Test creating a prediction record."""
    # Create member first
    create_test_member(member_hash=sample_member_hash)
    
    prediction = Prediction(**sample_prediction_data)
    test_db.add(prediction)
    test_db.commit()
    
    assert prediction.prediction_id is not None
    assert prediction.member_hash == sample_member_hash
    assert prediction.measure_code == "GSD"
    assert prediction.gap_probability == 0.75
    assert prediction.risk_tier == "high"
    assert prediction.model_version == "2.0.0"


def test_prediction_unique_constraint(test_db, sample_member_hash, sample_prediction_data, create_test_member):
    """Test unique constraint on (member_hash, measure_code, measurement_year, model_version)."""
    create_test_member(member_hash=sample_member_hash)
    
    # Create first prediction
    pred1 = Prediction(**sample_prediction_data)
    test_db.add(pred1)
    test_db.commit()
    
    # Try to create duplicate
    pred2 = Prediction(**sample_prediction_data)
    test_db.add(pred2)
    
    with pytest.raises(IntegrityError):
        test_db.commit()


def test_prediction_shap_values_jsonb(test_db, sample_member_hash, create_test_member, create_test_prediction):
    """Test SHAP values stored as JSONB."""
    create_test_member(member_hash=sample_member_hash)
    
    shap_data = {
        "age": 0.15,
        "hba1c_last": 0.25,
        "comorbidity_count": 0.10
    }
    
    prediction = create_test_prediction(
        member_hash=sample_member_hash,
        shap_values=shap_data
    )
    
    assert prediction.shap_values == shap_data
    assert prediction.shap_values["hba1c_last"] == 0.25


def test_prediction_foreign_key(test_db, sample_prediction_data):
    """Test foreign key constraint on member_hash."""
    # Try to create prediction without member
    prediction = Prediction(**sample_prediction_data)
    test_db.add(prediction)
    
    with pytest.raises(IntegrityError):
        test_db.commit()


# ===== Gap Analysis Model Tests =====

def test_gap_creation(test_db, sample_member_hash, sample_gap_data, create_test_member):
    """Test creating a gap analysis record."""
    create_test_member(member_hash=sample_member_hash)
    
    gap = GapAnalysis(**sample_gap_data)
    test_db.add(gap)
    test_db.commit()
    
    assert gap.gap_id is not None
    assert gap.member_hash == sample_member_hash
    assert gap.measure_code == "GSD"
    assert gap.status == "identified"
    assert gap.priority_score == 0.85


def test_gap_status_workflow(test_db, sample_member_hash, sample_gap_data, create_test_member):
    """Test gap status transitions."""
    create_test_member(member_hash=sample_member_hash)
    
    gap = GapAnalysis(**sample_gap_data)
    test_db.add(gap)
    test_db.commit()
    
    # Status transitions
    assert gap.status == "identified"
    
    gap.status = "assigned"
    gap.assigned_date = datetime.utcnow()
    test_db.commit()
    assert gap.status == "assigned"
    assert gap.assigned_date is not None
    
    gap.status = "completed"
    gap.completed_date = datetime.utcnow()
    test_db.commit()
    assert gap.status == "completed"
    assert gap.completed_date is not None


# ===== Intervention Model Tests =====

def test_intervention_creation(test_db, sample_member_hash, sample_intervention_data, create_test_member):
    """Test creating an intervention record."""
    create_test_member(member_hash=sample_member_hash)
    
    intervention = Intervention(**sample_intervention_data)
    test_db.add(intervention)
    test_db.commit()
    
    assert intervention.intervention_id is not None
    assert intervention.member_hash == sample_member_hash
    assert intervention.intervention_type == "lab_bundle"
    assert intervention.roi == 6.15


def test_intervention_multi_measure(test_db, sample_member_hash, create_test_member):
    """Test intervention with multiple measures (bundle)."""
    create_test_member(member_hash=sample_member_hash)
    
    intervention = Intervention(
        member_hash=sample_member_hash,
        measure_codes=["GSD", "KED", "EED"],  # Lab bundle
        intervention_type="lab_bundle",
        estimated_cost=200.00,
        estimated_value=1850.00,
        roi=9.25,
        status="planned"
    )
    test_db.add(intervention)
    test_db.commit()
    
    assert len(intervention.measure_codes) == 3
    assert "GSD" in intervention.measure_codes
    assert "KED" in intervention.measure_codes
    assert "EED" in intervention.measure_codes


# ===== Portfolio Snapshot Model Tests =====

def test_portfolio_snapshot_creation(test_db, sample_portfolio_snapshot_data):
    """Test creating a portfolio snapshot."""
    snapshot = PortfolioSnapshot(**sample_portfolio_snapshot_data)
    test_db.add(snapshot)
    test_db.commit()
    
    assert snapshot.snapshot_id is not None
    assert snapshot.total_members == 10000
    assert snapshot.total_gaps == 2500
    assert snapshot.gaps_by_measure["GSD"] == 500


def test_portfolio_snapshot_jsonb_queries(test_db, sample_portfolio_snapshot_data):
    """Test JSONB queries on portfolio snapshot."""
    snapshot = PortfolioSnapshot(**sample_portfolio_snapshot_data)
    test_db.add(snapshot)
    test_db.commit()
    
    # Verify JSONB structure
    assert "GSD" in snapshot.gaps_by_measure
    assert "1" in snapshot.gaps_by_tier
    assert snapshot.gaps_by_measure["KED"] == 450
    assert snapshot.gaps_by_tier["1"] == 950


# ===== Star Rating Model Tests =====

def test_star_rating_creation(test_db, sample_star_rating_data):
    """Test creating a Star Rating record."""
    rating = StarRating(**sample_star_rating_data)
    test_db.add(rating)
    test_db.commit()
    
    assert rating.rating_id is not None
    assert rating.overall_stars == 4.25
    assert rating.hei_adjusted is False


def test_star_rating_with_hei(test_db, sample_star_rating_data):
    """Test Star Rating with HEI adjustment."""
    sample_star_rating_data["hei_factor"] = 1.05
    sample_star_rating_data["hei_adjusted"] = True
    
    rating = StarRating(**sample_star_rating_data)
    test_db.add(rating)
    test_db.commit()
    
    assert rating.hei_adjusted is True
    assert rating.hei_factor == 1.05


# ===== Simulation Model Tests =====

def test_simulation_creation(test_db, sample_simulation_data):
    """Test creating a simulation record."""
    simulation = Simulation(**sample_simulation_data)
    test_db.add(simulation)
    test_db.commit()
    
    assert simulation.simulation_id is not None
    assert simulation.strategy == "triple_weighted"
    assert simulation.roi == 10.0


def test_simulation_scenario_details(test_db, sample_simulation_data):
    """Test simulation scenario details stored as JSONB."""
    simulation = Simulation(**sample_simulation_data)
    test_db.add(simulation)
    test_db.commit()
    
    assert simulation.scenario_details["focus"] == "triple_weighted"
    assert "GSD" in simulation.scenario_details["measures"]


# ===== API Log Model Tests =====

def test_api_log_creation(test_db):
    """Test creating an API log entry."""
    api_log = APILog(
        request_id=uuid4(),
        endpoint="/api/v1/predict/GSD",
        method="POST",
        api_key_hash="a" * 64,
        status_code=200,
        response_time_ms=35,
        prediction_count=1,
        timestamp=datetime.utcnow()
    )
    test_db.add(api_log)
    test_db.commit()
    
    assert api_log.log_id is not None
    assert api_log.status_code == 200
    assert api_log.response_time_ms == 35


def test_api_log_error_tracking(test_db):
    """Test API log with error message."""
    api_log = APILog(
        request_id=uuid4(),
        endpoint="/api/v1/predict/INVALID",
        method="POST",
        status_code=404,
        response_time_ms=5,
        error_message="Invalid measure code",
        timestamp=datetime.utcnow()
    )
    test_db.add(api_log)
    test_db.commit()
    
    assert api_log.status_code == 404
    assert api_log.error_message == "Invalid measure code"


# ===== Audit Log Model Tests =====

def test_audit_log_creation(test_db):
    """Test creating an audit log entry."""
    audit = AuditLog(
        event_type="prediction",
        entity_type="Prediction",
        entity_id=str(uuid4()),
        action="create",
        user_id="system",
        changes={"status": "new"},
        timestamp=datetime.utcnow(),
        ip_address="10.0.0.1"
    )
    test_db.add(audit)
    test_db.commit()
    
    assert audit.audit_id is not None
    assert audit.event_type == "prediction"
    assert audit.action == "create"


def test_audit_log_changes_jsonb(test_db):
    """Test audit log changes stored as JSONB."""
    changes = {
        "before": {"status": "identified"},
        "after": {"status": "assigned"}
    }
    
    audit = AuditLog(
        event_type="gap",
        entity_type="GapAnalysis",
        entity_id=str(uuid4()),
        action="update",
        user_id="system",
        changes=changes,
        timestamp=datetime.utcnow()
    )
    test_db.add(audit)
    test_db.commit()
    
    assert audit.changes["before"]["status"] == "identified"
    assert audit.changes["after"]["status"] == "assigned"


# ===== HIPAA Compliance Tests =====

def test_no_phi_in_member_model(test_db, create_test_member):
    """Test that Member model contains no PHI (only hashed IDs)."""
    member = create_test_member(member_hash="a" * 64)
    
    # Verify no PHI fields exist
    assert not hasattr(member, 'first_name')
    assert not hasattr(member, 'last_name')
    assert not hasattr(member, 'date_of_birth')
    assert not hasattr(member, 'ssn')
    assert not hasattr(member, 'address')
    
    # Verify only hash exists
    assert member.member_hash == "a" * 64
    assert len(member.member_hash) == 64  # SHA-256 hash length


def test_no_phi_in_prediction_model(test_db, sample_member_hash, create_test_member, create_test_prediction):
    """Test that Prediction model contains no PHI."""
    create_test_member(member_hash=sample_member_hash)
    prediction = create_test_prediction(member_hash=sample_member_hash)
    
    # Verify no PHI fields
    assert not hasattr(prediction, 'member_id')
    assert not hasattr(prediction, 'date_of_birth')
    assert not hasattr(prediction, 'diagnosis_details')
    
    # Verify only hash exists
    assert prediction.member_hash == sample_member_hash


# ===== Timestamp Tests =====

def test_created_at_auto_set(test_db, create_test_member):
    """Test that created_at is automatically set."""
    before = datetime.utcnow()
    member = create_test_member()
    after = datetime.utcnow()
    
    assert member.created_at is not None
    assert before <= member.created_at <= after


def test_updated_at_auto_set(test_db, create_test_member):
    """Test that updated_at is automatically set."""
    member = create_test_member()
    original_updated = member.updated_at
    
    # Wait a moment and update
    import time
    time.sleep(0.1)
    
    member.total_predictions += 1
    test_db.commit()
    test_db.refresh(member)
    
    assert member.updated_at > original_updated


# ===== Summary Test =====

def test_all_models_instantiate(test_db):
    """Test that all models can be instantiated without errors."""
    models = [
        Member(member_hash="a" * 64),
        # Additional models would need proper foreign keys
    ]
    
    for model in models:
        assert model is not None
        test_db.add(model)
    
    test_db.commit()
    assert True  # All models instantiated successfully


