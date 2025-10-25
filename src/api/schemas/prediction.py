"""
Prediction Schema Definitions
Request/response models for prediction endpoints.
"""

from datetime import datetime
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field, validator
from uuid import uuid4


class PredictionRequest(BaseModel):
    """
    Request schema for single member prediction.
    """
    member_id: str = Field(..., description="Member identifier (will be hashed for PHI protection)", min_length=1)
    measurement_year: int = Field(default=2025, description="HEDIS measurement year", ge=2020, le=2030)
    features: Optional[Dict[str, Any]] = Field(None, description="Custom features (optional, will be extracted if not provided)")
    include_shap: bool = Field(default=True, description="Include SHAP values in response")
    
    class Config:
        json_schema_extra = {
            "example": {
                "member_id": "M123456",
                "measurement_year": 2025,
                "include_shap": True
            }
        }


class PredictionResponse(BaseModel):
    """
    Response schema for single member prediction.
    """
    prediction_id: str = Field(default_factory=lambda: str(uuid4()), description="Unique prediction identifier")
    member_hash: str = Field(..., description="Hashed member ID (SHA-256, PHI-protected)")
    measure_code: str = Field(..., description="HEDIS measure code (e.g., GSD, KED)")
    risk_score: float = Field(..., description="Risk score (0-1, probability of gap)", ge=0.0, le=1.0)
    risk_tier: str = Field(..., description="Risk tier: high, medium, or low")
    gap_probability: float = Field(..., description="Probability of quality gap (0-1)", ge=0.0, le=1.0)
    shap_values: Optional[Dict[str, float]] = Field(None, description="SHAP values for top features")
    top_features: List[Dict[str, Any]] = Field(default_factory=list, description="Top influential features")
    recommendation: str = Field(..., description="Action recommendation")
    model_version: str = Field(..., description="Model version used")
    prediction_date: datetime = Field(default_factory=datetime.now, description="Prediction timestamp")
    
    class Config:
        json_schema_extra = {
            "example": {
                "prediction_id": "pred-abc123",
                "member_hash": "a1b2c3d4e5f6g7h8",
                "measure_code": "GSD",
                "risk_score": 0.78,
                "risk_tier": "high",
                "gap_probability": 0.78,
                "shap_values": {
                    "age": 0.15,
                    "hba1c_last_value": 0.42,
                    "ed_visits_count": 0.08
                },
                "top_features": [
                    {"name": "hba1c_last_value", "value": 8.5, "impact": 0.42},
                    {"name": "age", "value": 68, "impact": 0.15}
                ],
                "recommendation": "Member has high risk for HbA1c gap. Recommend PCP visit and lab order.",
                "model_version": "2.0.0",
                "prediction_date": "2025-10-24T10:30:00"
            }
        }


class BatchPredictionRequest(BaseModel):
    """
    Request schema for batch predictions.
    """
    member_ids: List[str] = Field(..., description="List of member identifiers", min_length=1, max_length=1000)
    measurement_year: int = Field(default=2025, description="HEDIS measurement year", ge=2020, le=2030)
    include_shap: bool = Field(default=False, description="Include SHAP values (only for high-risk members)")
    
    @validator('member_ids')
    def validate_batch_size(cls, v):
        if len(v) > 1000:
            raise ValueError("Batch size cannot exceed 1000 members")
        if len(v) == 0:
            raise ValueError("Batch must contain at least 1 member")
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "member_ids": ["M123456", "M789012", "M345678"],
                "measurement_year": 2025,
                "include_shap": False
            }
        }


class BatchPredictionResponse(BaseModel):
    """
    Response schema for batch predictions.
    """
    predictions: List[PredictionResponse] = Field(..., description="List of predictions")
    total_processed: int = Field(..., description="Total members processed")
    total_high_risk: int = Field(..., description="Count of high-risk members")
    total_medium_risk: int = Field(default=0, description="Count of medium-risk members")
    total_low_risk: int = Field(default=0, description="Count of low-risk members")
    processing_time_ms: float = Field(..., description="Processing time in milliseconds")
    measure_code: str = Field(..., description="HEDIS measure code")
    
    class Config:
        json_schema_extra = {
            "example": {
                "predictions": [],  # Truncated for brevity
                "total_processed": 100,
                "total_high_risk": 35,
                "total_medium_risk": 40,
                "total_low_risk": 25,
                "processing_time_ms": 450.5,
                "measure_code": "GSD"
            }
        }


class PortfolioPredictionRequest(BaseModel):
    """
    Request schema for portfolio prediction (all measures for one member).
    """
    member_id: str = Field(..., description="Member identifier", min_length=1)
    measures: Optional[List[str]] = Field(
        None,
        description="List of measure codes to predict (default: all 12)"
    )
    include_shap: bool = Field(default=True, description="Include SHAP values")
    measurement_year: int = Field(default=2025, description="HEDIS measurement year", ge=2020, le=2030)
    
    class Config:
        json_schema_extra = {
            "example": {
                "member_id": "M123456",
                "measures": ["GSD", "KED", "EED", "BPD"],
                "include_shap": True,
                "measurement_year": 2025
            }
        }


class PortfolioPredictionResponse(BaseModel):
    """
    Response schema for portfolio prediction.
    """
    member_hash: str = Field(..., description="Hashed member ID")
    predictions: Dict[str, PredictionResponse] = Field(..., description="Predictions by measure code")
    total_gaps: int = Field(..., description="Total predicted gaps")
    gap_measures: List[str] = Field(default_factory=list, description="List of measures with gaps")
    priority_score: float = Field(..., description="Overall priority score (0-100)", ge=0.0, le=100.0)
    priority_tier: str = Field(..., description="Priority tier: critical, high, medium, low")
    recommended_interventions: List[str] = Field(default_factory=list, description="Recommended interventions")
    estimated_value: float = Field(..., description="Estimated value of closing gaps ($)")
    processing_time_ms: float = Field(..., description="Processing time in milliseconds")
    
    class Config:
        json_schema_extra = {
            "example": {
                "member_hash": "a1b2c3d4e5f6g7h8",
                "predictions": {
                    "GSD": {},  # Truncated
                    "KED": {},
                    "EED": {}
                },
                "total_gaps": 3,
                "gap_measures": ["GSD", "KED", "EED"],
                "priority_score": 85.5,
                "priority_tier": "high",
                "recommended_interventions": [
                    "Schedule PCP visit for diabetes management",
                    "Order lab tests (HbA1c, eGFR, ACR)",
                    "Refer to ophthalmology for retinal exam"
                ],
                "estimated_value": 600.0,
                "processing_time_ms": 180.3
            }
        }

