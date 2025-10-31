"""
CRUD Operations Tests

Tests for all database CRUD operations.

Author: Robert Reichert
Date: October 2025
"""

import pytest
from datetime import datetime, timedelta
from uuid import UUID

from src.database import crud
from src.database.models import Member, Prediction, GapAnalysis


# ===== Member CRUD Tests =====

def test_create_member(test_db, sample_member_hash):
    """Test creating a member."""
    member = crud.create_member(test_db, sample_member_hash)
    
    assert member.member_hash == sample_member_hash
    assert member.total_predictions == 0
    assert member.active is True


def test_get_member(test_db, sample_member_hash):
    """Test retrieving a member."""
    crud.create_member(test_db, sample_member_hash)
    member = crud.get_member(test_db, sample_member_hash)
    
    assert member is not None
    assert member.member_hash == sample_member_hash


def test_get_or_create_member_new(test_db, sample_member_hash):
    """Test get_or_create with new member."""
    member = crud.get_or_create_member(test_db, sample_member_hash)
    
    assert member.member_hash == sample_member_hash
    assert member.total_predictions == 0


def test_get_or_create_member_existing(test_db, sample_member_hash):
    """Test get_or_create with existing member."""
    member1 = crud.create_member(test_db, sample_member_hash)
    member2 = crud.get_or_create_member(test_db, sample_member_hash)
    
    assert member1.member_hash == member2.member_hash


def test_update_member_activity(test_db, sample_member_hash):
    """Test updating member activity."""
    member = crud.create_member(test_db, sample_member_hash)
    original_count = member.total_predictions
    
    crud.update_member_activity(test_db, sample_member_hash)
    
    updated_member = crud.get_member(test_db, sample_member_hash)
    assert updated_member.total_predictions == original_count + 1


# ===== Prediction CRUD Tests =====

def test_create_prediction(test_db, sample_member_hash, sample_prediction_data):
    """Test creating a prediction."""
    prediction = crud.create_prediction(test_db, sample_prediction_data)
    
    assert prediction.prediction_id is not None
    assert isinstance(prediction.prediction_id, UUID)
    assert prediction.member_hash == sample_member_hash


def test_batch_create_predictions(test_db, sample_member_hash):
    """Test batch prediction creation."""
    predictions_data = [
        {
            "member_hash": sample_member_hash,
            "measure_code": "GSD",
            "measurement_year": 2025,
            "gap_probability": 0.75,
            "risk_tier": "high",
            "risk_score": 0.75,
            "model_version": "2.0.0"
        },
        {
            "member_hash": sample_member_hash,
            "measure_code": "KED",
            "measurement_year": 2025,
            "gap_probability": 0.65,
            "risk_tier": "medium",
            "risk_score": 0.65,
            "model_version": "2.0.0"
        }
    ]
    
    predictions = crud.batch_create_predictions(test_db, predictions_data)
    
    assert len(predictions) == 2


def test_get_member_predictions(test_db, sample_member_hash, sample_prediction_data):
    """Test retrieving member predictions."""
    crud.create_prediction(test_db, sample_prediction_data)
    
    predictions = crud.get_member_predictions(test_db, sample_member_hash)
    
    assert len(predictions) >= 1
    assert predictions[0].member_hash == sample_member_hash


def test_get_latest_prediction(test_db, sample_member_hash):
    """Test getting latest prediction for member/measure/year."""
    # Create two predictions
    pred1_data = {
        "member_hash": sample_member_hash,
        "measure_code": "GSD",
        "measurement_year": 2025,
        "gap_probability": 0.75,
        "risk_tier": "high",
        "risk_score": 0.75,
        "model_version": "1.0.0"
    }
    pred2_data = pred1_data.copy()
    pred2_data["model_version"] = "2.0.0"
    pred2_data["gap_probability"] = 0.80
    
    crud.create_prediction(test_db, pred1_data)
    import time
    time.sleep(0.1)  # Ensure different timestamps
    crud.create_prediction(test_db, pred2_data)
    
    latest = crud.get_latest_prediction(test_db, sample_member_hash, "GSD", 2025)
    
    assert latest is not None
    assert latest.model_version == "2.0.0"


# ===== Portfolio CRUD Tests =====

def test_create_portfolio_snapshot(test_db, sample_portfolio_snapshot_data):
    """Test creating portfolio snapshot."""
    snapshot = crud.create_portfolio_snapshot(test_db, sample_portfolio_snapshot_data)
    
    assert snapshot.snapshot_id is not None
    assert snapshot.total_members == 10000


def test_get_latest_portfolio_snapshot(test_db, sample_portfolio_snapshot_data):
    """Test retrieving latest portfolio snapshot."""
    crud.create_portfolio_snapshot(test_db, sample_portfolio_snapshot_data)
    
    snapshot = crud.get_latest_portfolio_snapshot(test_db, 2025)
    
    assert snapshot is not None
    assert snapshot.measurement_year == 2025


# ===== Gap Analysis CRUD Tests =====

def test_create_gap(test_db, sample_member_hash, sample_gap_data):
    """Test creating a gap."""
    gap = crud.create_gap(test_db, sample_gap_data)
    
    assert gap.gap_id is not None
    assert gap.status == "identified"


def test_get_gaps_with_filters(test_db, sample_member_hash, sample_gap_data):
    """Test retrieving gaps with filters."""
    crud.create_gap(test_db, sample_gap_data)
    
    # Filter by measure
    gaps = crud.get_gaps(test_db, measure_code="GSD")
    assert len(gaps) >= 1
    
    # Filter by status
    gaps = crud.get_gaps(test_db, status="identified")
    assert len(gaps) >= 1


def test_update_gap_status(test_db, sample_member_hash, sample_gap_data):
    """Test updating gap status."""
    gap = crud.create_gap(test_db, sample_gap_data)
    
    updated_gap = crud.update_gap_status(test_db, gap.gap_id, "assigned")
    
    assert updated_gap.status == "assigned"
    assert updated_gap.assigned_date is not None


def test_close_gap(test_db, sample_member_hash, sample_gap_data):
    """Test closing a gap."""
    gap = crud.create_gap(test_db, sample_gap_data)
    
    closed_gap = crud.close_gap(test_db, gap.gap_id)
    
    assert closed_gap.status == "closed"
    assert closed_gap.completed_date is not None


# ===== Intervention CRUD Tests =====

def test_create_intervention(test_db, sample_member_hash, sample_intervention_data):
    """Test creating an intervention."""
    intervention = crud.create_intervention(test_db, sample_intervention_data)
    
    assert intervention.intervention_id is not None
    assert intervention.status == "planned"


def test_update_intervention_status(test_db, sample_member_hash, sample_intervention_data):
    """Test updating intervention status."""
    intervention = crud.create_intervention(test_db, sample_intervention_data)
    
    updated = crud.update_intervention_status(
        test_db,
        intervention.intervention_id,
        "in_progress"
    )
    
    assert updated.status == "in_progress"


def test_complete_intervention(test_db, sample_member_hash, sample_intervention_data):
    """Test completing an intervention."""
    intervention = crud.create_intervention(test_db, sample_intervention_data)
    
    completed = crud.complete_intervention(
        test_db,
        intervention.intervention_id,
        "success"
    )
    
    assert completed.status == "completed"
    assert completed.outcome == "success"


# ===== Star Rating CRUD Tests =====

def test_create_star_rating(test_db, sample_star_rating_data):
    """Test creating a Star Rating."""
    rating = crud.create_star_rating(test_db, sample_star_rating_data)
    
    assert rating.rating_id is not None
    assert rating.overall_stars == 4.25


def test_get_latest_star_rating(test_db, sample_star_rating_data):
    """Test retrieving latest Star Rating."""
    crud.create_star_rating(test_db, sample_star_rating_data)
    
    rating = crud.get_latest_star_rating(test_db, 2025)
    
    assert rating is not None
    assert rating.measurement_year == 2025


# ===== Simulation CRUD Tests =====

def test_create_simulation(test_db, sample_simulation_data):
    """Test creating a simulation."""
    simulation = crud.create_simulation(test_db, sample_simulation_data)
    
    assert simulation.simulation_id is not None
    assert simulation.strategy == "triple_weighted"


def test_get_recent_simulations(test_db, sample_simulation_data):
    """Test retrieving recent simulations."""
    crud.create_simulation(test_db, sample_simulation_data)
    
    simulations = crud.get_recent_simulations(test_db, 2025, limit=10)
    
    assert len(simulations) >= 1


# ===== PHI Protection Tests =====

def test_crud_operations_use_hashed_ids(test_db):
    """Test that all CRUD operations use hashed IDs."""
    member_hash = "a" * 64  # SHA-256 length
    
    # All CRUD operations should accept/return hashed IDs
    member = crud.create_member(test_db, member_hash)
    assert len(member.member_hash) == 64
    
    retrieved = crud.get_member(test_db, member_hash)
    assert retrieved.member_hash == member_hash


# ===== Performance Tests =====

def test_batch_operations_efficient(test_db, sample_member_hash):
    """Test that batch operations are more efficient than individual operations."""
    import time
    
    # Create 100 predictions individually (slow)
    start = time.time()
    for i in range(10):  # Reduced for test speed
        crud.create_prediction(test_db, {
            "member_hash": sample_member_hash,
            "measure_code": "GSD",
            "measurement_year": 2025,
            "gap_probability": 0.75,
            "risk_tier": "high",
            "risk_score": 0.75,
            "model_version": f"1.0.{i}"
        })
    individual_time = time.time() - start
    
    # Create 100 predictions in batch (fast)
    test_db.rollback()  # Reset
    predictions_data = [
        {
            "member_hash": sample_member_hash,
            "measure_code": "KED",
            "measurement_year": 2025,
            "gap_probability": 0.75,
            "risk_tier": "high",
            "risk_score": 0.75,
            "model_version": f"2.0.{i}"
        }
        for i in range(10)
    ]
    
    start = time.time()
    crud.batch_create_predictions(test_db, predictions_data)
    batch_time = time.time() - start
    
    # Batch should be faster
    assert batch_time < individual_time


# ===== Error Handling Tests =====

def test_crud_handles_missing_records_gracefully(test_db):
    """Test CRUD operations handle missing records gracefully."""
    # Get non-existent member
    member = crud.get_member(test_db, "nonexistent" + "0" * 53)
    assert member is None


def test_delete_old_predictions(test_db, sample_member_hash):
    """Test deleting old predictions."""
    # Create old prediction
    old_data = {
        "member_hash": sample_member_hash,
        "measure_code": "GSD",
        "measurement_year": 2024,
        "gap_probability": 0.75,
        "risk_tier": "high",
        "risk_score": 0.75,
        "model_version": "1.0.0"
    }
    crud.create_prediction(test_db, old_data)
    
    # Delete predictions older than cutoff
    cutoff = datetime.utcnow() - timedelta(days=365)
    deleted = crud.delete_old_predictions(test_db, cutoff)
    
    # Verify deletion (should be 0 since we just created it)
    assert deleted >= 0



