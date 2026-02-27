"""
Database Test Fixtures

Provides test database, sample data, and utilities for database testing.

Author: Robert Reichert
Date: October 2025
"""

import pytest
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from src.database.models import Base, Member, Prediction, GapAnalysis, Intervention
from src.database.connection import get_db


# ===== Test Database Setup =====

@pytest.fixture(scope="function")
def test_db():
    """
    Create an in-memory SQLite database for testing.
    
    Notes:
        - Uses SQLite in-memory for fast tests
        - Isolated per test function
        - Automatically cleaned up after test
    """
    # Create in-memory SQLite database
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    # Create session
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = TestingSessionLocal()
    
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def test_db_with_data(test_db):
    """
    Test database pre-populated with sample data.
    """
    # Create sample members
    member1 = Member(
        member_hash="a" * 64,  # SHA-256 hash length
        first_seen=datetime.utcnow() - timedelta(days=365),
        total_predictions=5,
        active=True
    )
    member2 = Member(
        member_hash="b" * 64,
        first_seen=datetime.utcnow() - timedelta(days=180),
        total_predictions=3,
        active=True
    )
    
    test_db.add_all([member1, member2])
    test_db.commit()
    
    yield test_db


# ===== Sample Data Fixtures =====

@pytest.fixture
def sample_member_hash():
    """Sample SHA-256 hashed member ID."""
    return "a1b2c3d4e5f6" + "0" * 52  # 64 characters


@pytest.fixture
def sample_member_data(sample_member_hash):
    """Sample member data for testing."""
    return {
        "member_hash": sample_member_hash,
        "first_seen": datetime.utcnow(),
        "total_predictions": 0,
        "active": True
    }


@pytest.fixture
def sample_prediction_data(sample_member_hash):
    """Sample prediction data for testing."""
    return {
        "member_hash": sample_member_hash,
        "measure_code": "GSD",
        "measurement_year": 2025,
        "gap_probability": 0.75,
        "risk_tier": "high",
        "risk_score": 0.75,
        "shap_values": {
            "age": 0.15,
            "hba1c_last": 0.25,
            "comorbidity_count": 0.10
        },
        "top_features": [
            {"name": "hba1c_last", "value": 9.2, "impact": 0.25},
            {"name": "age", "value": 68, "impact": 0.15}
        ],
        "recommendation": "High risk for Glycemic Status gap. Urgent: Schedule PCP visit and order HbA1c test.",
        "model_version": "2.0.0"
    }


@pytest.fixture
def sample_gap_data(sample_member_hash):
    """Sample gap analysis data for testing."""
    return {
        "member_hash": sample_member_hash,
        "measure_code": "GSD",
        "measurement_year": 2025,
        "gap_probability": 0.80,
        "priority_score": 0.85,
        "intervention_type": "lab_bundle",
        "estimated_cost": 150.00,
        "estimated_value": 615.00,
        "status": "identified"
    }


@pytest.fixture
def sample_intervention_data(sample_member_hash):
    """Sample intervention data for testing."""
    return {
        "member_hash": sample_member_hash,
        "measure_codes": ["GSD", "KED"],
        "intervention_type": "lab_bundle",
        "description": "Schedule lab tests for HbA1c, eGFR, and ACR",
        "estimated_cost": 200.00,
        "estimated_value": 1230.00,
        "roi": 6.15,
        "status": "planned",
        "scheduled_date": datetime.utcnow().date() + timedelta(days=7)
    }


@pytest.fixture
def sample_portfolio_snapshot_data():
    """Sample portfolio snapshot data for testing."""
    return {
        "measurement_year": 2025,
        "snapshot_date": datetime.utcnow(),
        "total_members": 10000,
        "total_gaps": 2500,
        "gaps_by_measure": {
            "GSD": 500,
            "KED": 450,
            "EED": 350,
            "PDC-DR": 300,
            "BPD": 250,
            "CBP": 200,
            "SUPD": 150,
            "PDC-RASA": 100,
            "PDC-STA": 100,
            "BCS": 50,
            "COL": 50
        },
        "gaps_by_tier": {
            "1": 950,
            "2": 550,
            "3": 100,
            "4": 900
        },
        "star_rating_current": 4.0,
        "star_rating_projected": 4.5,
        "estimated_value": 15000000.00
    }


@pytest.fixture
def sample_star_rating_data():
    """Sample Star Rating data for testing."""
    return {
        "measurement_year": 2025,
        "calculation_date": datetime.utcnow(),
        "overall_stars": 4.25,
        "total_points": 85.5,
        "measure_stars": {
            "GSD": 4.5,
            "KED": 4.0,
            "EED": 4.0,
            "PDC-DR": 4.5,
            "BPD": 4.0,
            "CBP": 4.5,
            "SUPD": 4.0,
            "PDC-RASA": 4.0,
            "PDC-STA": 4.5,
            "BCS": 4.0,
            "COL": 4.5
        },
        "measure_rates": {
            "GSD": 0.85,
            "KED": 0.80,
            "EED": 0.75,
            "PDC-DR": 0.82,
            "BPD": 0.78,
            "CBP": 0.83,
            "SUPD": 0.76,
            "PDC-RASA": 0.79,
            "PDC-STA": 0.84,
            "BCS": 0.72,
            "COL": 0.81
        },
        "hei_factor": None,
        "hei_adjusted": False,
        "revenue_estimate": 25000000.00,
        "bonus_tier": "4.5"
    }


@pytest.fixture
def sample_simulation_data():
    """Sample simulation data for testing."""
    return {
        "measurement_year": 2025,
        "simulation_date": datetime.utcnow(),
        "strategy": "triple_weighted",
        "closure_rate": 0.30,
        "baseline_stars": 4.0,
        "projected_stars": 4.5,
        "revenue_impact": 5000000.00,
        "investment_required": 500000.00,
        "roi": 10.0,
        "gaps_closed": 750,
        "members_impacted": 2500,
        "scenario_details": {
            "focus": "triple_weighted",
            "measures": ["GSD", "KED", "CBP"],
            "closure_target": 0.30
        }
    }


# ===== Test Utilities =====

@pytest.fixture
def create_test_member(test_db, sample_member_hash):
    """
    Factory fixture to create test members.
    
    Usage:
        member = create_test_member()
        member = create_test_member(member_hash="custom_hash")
    """
    def _create_member(member_hash=None, **kwargs):
        member = Member(
            member_hash=member_hash or sample_member_hash,
            first_seen=kwargs.get("first_seen", datetime.utcnow()),
            total_predictions=kwargs.get("total_predictions", 0),
            active=kwargs.get("active", True)
        )
        test_db.add(member)
        test_db.commit()
        test_db.refresh(member)
        return member
    
    return _create_member


@pytest.fixture
def create_test_prediction(test_db, sample_member_hash):
    """
    Factory fixture to create test predictions.
    """
    def _create_prediction(member_hash=None, measure_code="GSD", **kwargs):
        from src.database.models import Prediction
        
        prediction = Prediction(
            member_hash=member_hash or sample_member_hash,
            measure_code=measure_code,
            measurement_year=kwargs.get("measurement_year", 2025),
            gap_probability=kwargs.get("gap_probability", 0.75),
            risk_tier=kwargs.get("risk_tier", "high"),
            risk_score=kwargs.get("risk_score", 0.75),
            shap_values=kwargs.get("shap_values"),
            top_features=kwargs.get("top_features"),
            recommendation=kwargs.get("recommendation", "Test recommendation"),
            model_version=kwargs.get("model_version", "2.0.0")
        )
        test_db.add(prediction)
        test_db.commit()
        test_db.refresh(prediction)
        return prediction
    
    return _create_prediction


# ===== Cleanup Utilities =====

@pytest.fixture(autouse=True)
def cleanup_after_test(test_db):
    """
    Automatically cleanup after each test.
    
    Notes:
        - Rolls back any uncommitted transactions
        - Ensures clean state for next test
    """
    yield
    test_db.rollback()



