"""
Prediction Router
Endpoints for member-level predictions across all 12 HEDIS measures.
"""

import time
import logging
from typing import Dict, List, Optional, Any
import hashlib

from fastapi import APIRouter, HTTPException, status, Depends, Request
from fastapi.responses import JSONResponse

from ..schemas.prediction import (
    PredictionRequest,
    PredictionResponse,
    BatchPredictionRequest,
    BatchPredictionResponse,
    PortfolioPredictionRequest,
    PortfolioPredictionResponse,
)
from ..dependencies import get_model_cache, hash_member_id, ModelCache
from ..config import get_settings, APISettings

# Import HEDIS utilities
import sys
sys.path.append(".")
from src.utils.hedis_specs import MEASURE_REGISTRY, get_measure_spec

logger = logging.getLogger(__name__)

router = APIRouter()


# ===== Helper Functions =====

def load_measure_model(measure_code: str, cache: ModelCache):
    """
    Load trained model for a specific measure.
    Models are cached after first load.
    """
    # Check cache first
    model = cache.get_model(measure_code)
    if model is not None:
        return model
    
    # Load from disk
    try:
        import joblib
        import os
        
        model_path = f"models/{measure_code.lower()}_model.pkl"
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found: {model_path}")
        
        model = joblib.load(model_path)
        cache.set_model(measure_code, model)
        
        logger.info(f"Loaded model for {measure_code}")
        return model
        
    except Exception as e:
        logger.error(f"Failed to load model for {measure_code}: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Model for measure {measure_code} is not available"
        )


def load_measure_scaler(measure_code: str, cache: ModelCache):
    """
    Load feature scaler for a specific measure.
    """
    # Check cache first
    scaler = cache.get_scaler(measure_code)
    if scaler is not None:
        return scaler
    
    # Load from disk
    try:
        import joblib
        import os
        
        scaler_path = f"models/{measure_code.lower()}_scaler.pkl"
        if not os.path.exists(scaler_path):
            logger.warning(f"Scaler not found for {measure_code}, using model without scaling")
            return None
        
        scaler = joblib.load(scaler_path)
        cache.set_scaler(measure_code, scaler)
        
        return scaler
        
    except Exception as e:
        logger.warning(f"Failed to load scaler for {measure_code}: {e}")
        return None


def extract_member_features(member_id: str, measure_code: str, measurement_year: int = 2025) -> Dict[str, Any]:
    """
    Extract features for a member for a specific measure.
    This is a placeholder - actual implementation would load from data pipeline.
    """
    # TODO: Implement actual feature extraction
    # For now, return dummy features for testing
    logger.warning(f"Using dummy features for {member_id} - implement actual feature extraction")
    
    import numpy as np
    
    # Generate consistent dummy features based on member_id hash
    seed = int(hashlib.md5(member_id.encode()).hexdigest()[:8], 16) % (2**32)
    np.random.seed(seed)
    
    # Basic features (25 features as in original model)
    features = {
        'age': np.random.randint(40, 85),
        'gender': np.random.choice([0, 1]),
        'diabetes_duration': np.random.randint(1, 20),
        'hba1c_last_value': np.random.uniform(6.0, 10.0),
        'egfr_last_value': np.random.uniform(30, 90),
        'ckd_flag': np.random.choice([0, 1]),
        'cvd_flag': np.random.choice([0, 1]),
        'retinopathy_flag': np.random.choice([0, 1]),
        'ed_visits_count': np.random.randint(0, 5),
        'inpatient_admissions': np.random.randint(0, 3),
        'pcp_visits': np.random.randint(0, 10),
        'specialist_visits': np.random.randint(0, 8),
    }
    
    return features


def calculate_shap_values(model: Any, features: Dict, feature_names: List[str]) -> Dict[str, float]:
    """
    Calculate SHAP values for model interpretability.
    """
    try:
        import shap
        import pandas as pd
        
        # Convert features to DataFrame
        feature_df = pd.DataFrame([features])
        
        # Calculate SHAP values
        explainer = shap.TreeExplainer(model)
        shap_values = explainer.shap_values(feature_df)
        
        # Get top 5 features by absolute SHAP value
        if len(shap_values.shape) > 1:
            shap_values = shap_values[0]  # For binary classification
        
        shap_dict = dict(zip(feature_names, shap_values))
        
        # Sort by absolute value and return top 5
        top_shap = dict(sorted(shap_dict.items(), key=lambda x: abs(x[1]), reverse=True)[:5])
        
        return top_shap
        
    except Exception as e:
        logger.warning(f"Failed to calculate SHAP values: {e}")
        return {}


def determine_risk_tier(probability: float) -> str:
    """
    Determine risk tier based on gap probability.
    """
    if probability >= 0.7:
        return "high"
    elif probability >= 0.4:
        return "medium"
    else:
        return "low"


def generate_recommendation(measure_code: str, probability: float, features: Dict) -> str:
    """
    Generate actionable recommendation based on prediction.
    """
    measure_spec = get_measure_spec(measure_code)
    
    if not measure_spec:
        return "Review member profile and schedule appropriate interventions"
    
    risk_tier = determine_risk_tier(probability)
    measure_name = measure_spec.name
    
    if risk_tier == "high":
        if measure_code in ["GSD", "KED", "BPD"]:
            return f"High risk for {measure_name} gap. Urgent: Schedule PCP visit and order lab tests (HbA1c, eGFR, ACR, BP check)."
        elif measure_code == "EED":
            return f"High risk for {measure_name} gap. Urgent: Refer to ophthalmology for dilated retinal exam."
        elif measure_code in ["PDC-DR", "PDC-RASA", "PDC-STA"]:
            return f"High risk for {measure_name} gap. Urgent: Contact member about medication adherence. Review refill history."
        elif measure_code in ["BCS", "COL"]:
            return f"High risk for {measure_name} gap. Urgent: Schedule screening appointment."
        else:
            return f"High risk for {measure_name} gap. Immediate intervention recommended."
    elif risk_tier == "medium":
        return f"Moderate risk for {measure_name} gap. Schedule follow-up and monitor closely."
    else:
        return f"Low risk for {measure_name} gap. Continue routine monitoring."


# ===== Prediction Endpoints =====

@router.post("/predict/{measure_code}", response_model=PredictionResponse, tags=["Predictions"])
async def predict_single_member(
    measure_code: str,
    request_data: PredictionRequest,
    request: Request,
    cache: ModelCache = Depends(get_model_cache),
    settings: APISettings = Depends(get_settings)
) -> PredictionResponse:
    """
    Generate prediction for a single member for a specific HEDIS measure.
    
    **Measure Codes:** GSD, KED, EED, PDC-DR, BPD, CBP, SUPD, PDC-RASA, PDC-STA, BCS, COL, HEI
    
    **Risk Tiers:**
    - **High:** Gap probability ≥ 0.7
    - **Medium:** Gap probability 0.4-0.7
    - **Low:** Gap probability < 0.4
    
    **Response Time Target:** < 50ms
    """
    start_time = time.time()
    request_id = getattr(request.state, 'request_id', 'unknown')
    
    # Validate measure code
    measure_code = measure_code.upper()
    if measure_code not in MEASURE_REGISTRY:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Invalid measure code: {measure_code}. Must be one of: {list(MEASURE_REGISTRY.keys())}"
        )
    
    try:
        # Hash member ID for PHI protection
        member_hash = hash_member_id(request_data.member_id)
        
        # Load model and scaler
        model = load_measure_model(measure_code, cache)
        scaler = load_measure_scaler(measure_code, cache)
        
        # Extract or use provided features
        if request_data.features:
            features = request_data.features
        else:
            features = extract_member_features(
                request_data.member_id,
                measure_code,
                request_data.measurement_year
            )
        
        # Prepare features for prediction
        import pandas as pd
        feature_df = pd.DataFrame([features])
        
        # Scale features if scaler available
        if scaler:
            feature_array = scaler.transform(feature_df)
        else:
            feature_array = feature_df.values
        
        # Generate prediction
        gap_probability = float(model.predict_proba(feature_array)[0][1])
        risk_tier = determine_risk_tier(gap_probability)
        
        # Calculate SHAP values if requested
        shap_values = None
        top_features = []
        if request_data.include_shap and hasattr(model, 'feature_importances_'):
            shap_values = calculate_shap_values(model, features, list(features.keys()))
            top_features = [
                {"name": name, "value": features.get(name), "impact": impact}
                for name, impact in shap_values.items()
            ]
        
        # Generate recommendation
        recommendation = generate_recommendation(measure_code, gap_probability, features)
        
        # Calculate processing time
        processing_time = (time.time() - start_time) * 1000
        
        # Log prediction (PHI-safe)
        logger.info(
            f"Prediction: {measure_code} | Member: {member_hash} | "
            f"Risk: {risk_tier} ({gap_probability:.3f}) | Time: {processing_time:.2f}ms | "
            f"Request-ID: {request_id}"
        )
        
        # Build response
        response = PredictionResponse(
            member_hash=member_hash,
            measure_code=measure_code,
            risk_score=gap_probability,
            risk_tier=risk_tier,
            gap_probability=gap_probability,
            shap_values=shap_values,
            top_features=top_features,
            recommendation=recommendation,
            model_version=settings.api_version
        )
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            f"Prediction failed: {measure_code} | Error: {e} | Request-ID: {request_id}",
            exc_info=True
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Prediction failed: {str(e)}"
        )


@router.post("/predict/batch/{measure_code}", response_model=BatchPredictionResponse, tags=["Predictions"])
async def predict_batch(
    measure_code: str,
    request_data: BatchPredictionRequest,
    request: Request,
    cache: ModelCache = Depends(get_model_cache),
    settings: APISettings = Depends(get_settings)
) -> BatchPredictionResponse:
    """
    Generate predictions for multiple members for a specific HEDIS measure.
    
    **Maximum batch size:** 1000 members
    
    **Response Time Target:** < 500ms for 100 members
    
    **Note:** SHAP values are only calculated for high-risk members when include_shap=True
    """
    start_time = time.time()
    request_id = getattr(request.state, 'request_id', 'unknown')
    
    # Validate measure code
    measure_code = measure_code.upper()
    if measure_code not in MEASURE_REGISTRY:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Invalid measure code: {measure_code}"
        )
    
    try:
        # Load model once for all predictions
        model = load_measure_model(measure_code, cache)
        scaler = load_measure_scaler(measure_code, cache)
        
        predictions = []
        high_risk_count = 0
        medium_risk_count = 0
        low_risk_count = 0
        
        # Process each member
        for member_id in request_data.member_ids:
            # Hash member ID
            member_hash = hash_member_id(member_id)
            
            # Extract features
            features = extract_member_features(member_id, measure_code, request_data.measurement_year)
            
            # Prepare and scale features
            import pandas as pd
            feature_df = pd.DataFrame([features])
            if scaler:
                feature_array = scaler.transform(feature_df)
            else:
                feature_array = feature_df.values
            
            # Predict
            gap_probability = float(model.predict_proba(feature_array)[0][1])
            risk_tier = determine_risk_tier(gap_probability)
            
            # Count by risk tier
            if risk_tier == "high":
                high_risk_count += 1
            elif risk_tier == "medium":
                medium_risk_count += 1
            else:
                low_risk_count += 1
            
            # Calculate SHAP only for high-risk if requested
            shap_values = None
            top_features = []
            if request_data.include_shap and risk_tier == "high":
                shap_values = calculate_shap_values(model, features, list(features.keys()))
                top_features = [
                    {"name": name, "value": features.get(name), "impact": impact}
                    for name, impact in shap_values.items()
                ]
            
            # Generate recommendation
            recommendation = generate_recommendation(measure_code, gap_probability, features)
            
            # Create prediction response
            pred = PredictionResponse(
                member_hash=member_hash,
                measure_code=measure_code,
                risk_score=gap_probability,
                risk_tier=risk_tier,
                gap_probability=gap_probability,
                shap_values=shap_values,
                top_features=top_features,
                recommendation=recommendation,
                model_version=settings.api_version
            )
            predictions.append(pred)
        
        # Calculate processing time
        processing_time = (time.time() - start_time) * 1000
        
        # Log batch stats (PHI-safe)
        logger.info(
            f"Batch Prediction: {measure_code} | Members: {len(request_data.member_ids)} | "
            f"High-Risk: {high_risk_count} | Time: {processing_time:.2f}ms | "
            f"Request-ID: {request_id}"
        )
        
        # Build response
        response = BatchPredictionResponse(
            predictions=predictions,
            total_processed=len(predictions),
            total_high_risk=high_risk_count,
            total_medium_risk=medium_risk_count,
            total_low_risk=low_risk_count,
            processing_time_ms=processing_time,
            measure_code=measure_code
        )
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            f"Batch prediction failed: {measure_code} | Error: {e} | Request-ID: {request_id}",
            exc_info=True
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Batch prediction failed: {str(e)}"
        )


@router.post("/predict/portfolio", response_model=PortfolioPredictionResponse, tags=["Predictions"])
async def predict_portfolio(
    request_data: PortfolioPredictionRequest,
    request: Request,
    cache: ModelCache = Depends(get_model_cache),
    settings: APISettings = Depends(get_settings)
) -> PortfolioPredictionResponse:
    """
    Generate predictions across all measures for a single member.
    
    **Efficiency:** Features are extracted once and reused across all measures.
    
    **Response Time Target:** < 200ms for all 12 measures
    
    **Priority Scoring:** Weighted by measure importance (3x for triple-weighted measures)
    """
    start_time = time.time()
    request_id = getattr(request.state, 'request_id', 'unknown')
    
    try:
        # Hash member ID
        member_hash = hash_member_id(request_data.member_id)
        
        # Determine which measures to predict
        measures_to_predict = request_data.measures or list(MEASURE_REGISTRY.keys())
        
        # Validate measures
        for m in measures_to_predict:
            if m not in MEASURE_REGISTRY:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail=f"Invalid measure code: {m}"
                )
        
        # Extract features once (reuse for all measures)
        # In production, this would extract shared features efficiently
        predictions_dict = {}
        total_gaps = 0
        gap_measures = []
        priority_score = 0.0
        estimated_value = 0.0
        
        # Generate prediction for each measure
        for measure_code in measures_to_predict:
            try:
                # Create individual prediction request
                pred_request = PredictionRequest(
                    member_id=request_data.member_id,
                    measurement_year=request_data.measurement_year,
                    include_shap=request_data.include_shap
                )
                
                # Get prediction (reuse prediction logic)
                model = load_measure_model(measure_code, cache)
                scaler = load_measure_scaler(measure_code, cache)
                
                features = extract_member_features(
                    request_data.member_id,
                    measure_code,
                    request_data.measurement_year
                )
                
                import pandas as pd
                feature_df = pd.DataFrame([features])
                if scaler:
                    feature_array = scaler.transform(feature_df)
                else:
                    feature_array = feature_df.values
                
                gap_probability = float(model.predict_proba(feature_array)[0][1])
                risk_tier = determine_risk_tier(gap_probability)
                
                # SHAP values
                shap_values = None
                top_features = []
                if request_data.include_shap:
                    shap_values = calculate_shap_values(model, features, list(features.keys()))
                    top_features = [
                        {"name": name, "value": features.get(name), "impact": impact}
                        for name, impact in shap_values.items()
                    ]
                
                recommendation = generate_recommendation(measure_code, gap_probability, features)
                
                pred = PredictionResponse(
                    member_hash=member_hash,
                    measure_code=measure_code,
                    risk_score=gap_probability,
                    risk_tier=risk_tier,
                    gap_probability=gap_probability,
                    shap_values=shap_values,
                    top_features=top_features,
                    recommendation=recommendation,
                    model_version=settings.api_version
                )
                
                predictions_dict[measure_code] = pred
                
                # Count gaps (risk tier high or medium)
                if risk_tier in ["high", "medium"]:
                    total_gaps += 1
                    gap_measures.append(measure_code)
                    
                    # Get measure spec for priority scoring
                    measure_spec = get_measure_spec(measure_code)
                    weight = measure_spec.weight if measure_spec else 1
                    
                    # Priority score: weighted by measure importance and probability
                    priority_score += gap_probability * weight * 100
                    
                    # Estimated value (simplified calculation)
                    estimated_value += 200.0 * weight  # Base value * weight
                    
            except Exception as e:
                logger.warning(f"Failed to predict {measure_code}: {e}")
                continue
        
        # Normalize priority score (0-100)
        if total_gaps > 0:
            priority_score = min(priority_score / len(measures_to_predict), 100.0)
        
        # Determine priority tier
        if priority_score >= 80:
            priority_tier = "critical"
        elif priority_score >= 60:
            priority_tier = "high"
        elif priority_score >= 40:
            priority_tier = "medium"
        else:
            priority_tier = "low"
        
        # Generate bundled interventions
        interventions = []
        if "GSD" in gap_measures or "KED" in gap_measures or "BPD" in gap_measures:
            interventions.append("Schedule PCP visit for diabetes management")
            interventions.append("Order lab tests (HbA1c, eGFR, ACR, BP)")
        if "EED" in gap_measures:
            interventions.append("Refer to ophthalmology for retinal exam")
        if any(m in gap_measures for m in ["PDC-DR", "PDC-RASA", "PDC-STA"]):
            interventions.append("Contact member about medication adherence")
        if any(m in gap_measures for m in ["BCS", "COL"]):
            interventions.append("Schedule cancer screening appointment")
        
        # Calculate processing time
        processing_time = (time.time() - start_time) * 1000
        
        # Log portfolio prediction (PHI-safe)
        logger.info(
            f"Portfolio Prediction | Member: {member_hash} | "
            f"Measures: {len(predictions_dict)} | Gaps: {total_gaps} | "
            f"Priority: {priority_tier} ({priority_score:.1f}) | "
            f"Time: {processing_time:.2f}ms | Request-ID: {request_id}"
        )
        
        # Build response
        response = PortfolioPredictionResponse(
            member_hash=member_hash,
            predictions=predictions_dict,
            total_gaps=total_gaps,
            gap_measures=gap_measures,
            priority_score=priority_score,
            priority_tier=priority_tier,
            recommended_interventions=interventions,
            estimated_value=estimated_value,
            processing_time_ms=processing_time
        )
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            f"Portfolio prediction failed | Error: {e} | Request-ID: {request_id}",
            exc_info=True
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Portfolio prediction failed: {str(e)}"
        )

