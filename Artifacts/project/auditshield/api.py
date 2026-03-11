"""
AuditShield API — Starlette wrapper adding /request-trial endpoint.
Run: uvicorn api:app --host 0.0.0.0 --port 8000
Or: python -m uvicorn api:app
"""
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse, RedirectResponse
from starlette.routing import Mount, Route


async def request_trial_post(request: Request):
    """
    POST /request-trial — capture lead with auto trial, fire webhook.
    Supports ?source=organic|docs|conda|sponsors.
    responses:
      200:
        description: Lead captured; check email for trial key.
        examples:
          {"ok": true, "message": "Check your email for your trial key.", "email": "user@example.com"}
      400:
        description: Valid email required
      500:
        description: Capture unavailable or error
    """
    try:
        # Source from query (e.g. ?source=organic from MkDocs links) or body/form
        q = dict(request.query_params)
        source = (q.get("source") or "").strip() or "web"
        if source not in ("web", "organic", "docs", "referral", "conda", "sponsors"):
            source = "web"

        body = await request.json() if request.headers.get("content-type", "").startswith("application/json") else {}
        if not body:
            form = await request.form()
            email = form.get("email", "").strip().lower() if form else ""
            src = form.get("source", "").strip() or source
        else:
            email = (body.get("email") or "").strip().lower()
            src = (body.get("source") or source).strip() or source
        if src not in ("web", "organic", "docs", "referral", "conda", "sponsors"):
            src = "web"

        if not email or "@" not in email:
            return JSONResponse({"ok": False, "error": "Valid email required"}, status_code=400)
        from starguard_core.auth.capture import capture_lead
        rec = capture_lead(email, source=src, auto_provision_trial=True)
        if not rec:
            return JSONResponse({"ok": False, "error": "Capture unavailable"}, status_code=500)
        return JSONResponse({
            "ok": True,
            "message": "Check your email for your trial key.",
            "email": rec.email,
        })
    except Exception as e:
        return JSONResponse({"ok": False, "error": str(e)}, status_code=500)


async def request_trial_get(request: Request):
    """
    GET /request-trial — redirect to trial form page.
    responses:
      302:
        description: Redirect to /request_trial.html
    """
    return RedirectResponse(url="/request_trial.html", status_code=302)


async def audit_trail_get(request: Request):
    """
    GET /audit-trail — Enterprise-only REST endpoint backed by immutable audit_log.
    Requires X-Api-Key header. Returns 404 when tier lacks audit_trail feature.
    v3.3.0.
    """
    api_key = request.headers.get("X-Api-Key") or request.headers.get("Authorization", "").replace("Bearer ", "")
    from starguard_core.auth.validator import validate_api_key, is_feature_enabled, get_tier_config

    auth = await validate_api_key(api_key, feature="audit_trail")
    if not auth.is_valid:
        return JSONResponse({"error": "Invalid API key or rate limited"}, status_code=401)
    tier_config = get_tier_config(api_key)
    if not is_feature_enabled("audit_trail", tier_config):
        return JSONResponse({"error": "audit_trail is Enterprise only"}, status_code=404)

    limit = 100
    try:
        q = dict(request.query_params)
        if "limit" in q:
            limit = min(500, max(1, int(q["limit"])))
    except (ValueError, TypeError):
        pass

    from starguard_core.audit.soc2 import get_audit_trail
    summary = get_audit_trail(limit=limit)
    return JSONResponse(summary.to_dict())


# Import Shiny app after routes defined to avoid circular import
from app import app as shiny_app

# OpenAPI schema — Phase 26 Obj 3; Postman import
from starlette.schemas import SchemaGenerator

schemas = SchemaGenerator(
    {
        "openapi": "3.0.0",
        "info": {"title": "AuditShield API", "version": "1.0"},
    }
)

api_routes = [
    Route("/request-trial", request_trial_post, methods=["POST"]),
    Route("/request-trial", request_trial_get, methods=["GET"]),
    Route("/audit-trail", audit_trail_get, methods=["GET"]),
]


async def openapi_json(request: Request):
    """GET /openapi.json — OpenAPI 3.0 spec for Postman import."""
    schema = schemas.get_schema(routes=api_routes)
    return JSONResponse(schema)


routes = [
    Route("/openapi.json", openapi_json, methods=["GET"]),
    *api_routes,
    Mount("/", app=shiny_app),
]

app = Starlette(routes=routes)
