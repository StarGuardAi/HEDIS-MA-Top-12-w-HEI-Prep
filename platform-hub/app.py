"""
MA Compliance Intelligence Platform Hub
Reichert Science & Intelligence — Platform entry point
HuggingFace Space: rreichert/reichert-platform-hub

Secrets: SUPABASE_URL + SUPABASE_ANON_KEY (or PLATFORM_SUPABASE_*).
Avatar: optional LinkedIn_Avatar_300PX.png; else GitHub raw / AVATAR_URL.
"""

import base64
import concurrent.futures
import os
from io import BytesIO

import pandas as pd
from dotenv import load_dotenv
from shiny import App, reactive, render, ui

load_dotenv()

_APP_DIR = os.path.dirname(os.path.abspath(__file__))

# Supabase: blocking calls use ThreadPoolExecutor deadlines below (HF + Shiny safe).
_QUERY_DEADLINE_SEC = 6.0
_LOG_SESSION_DEADLINE_SEC = 4.0

# ── HuggingFace Space URLs (env overrides) ───────────────────────────────────
HF_AUDITSHIELD = os.environ.get(
    "HF_AUDITSHIELD",
    "https://huggingface.co/spaces/rreichert/auditshield-live",
)
HF_STARGUARD = os.environ.get(
    "HF_STARGUARD",
    "https://huggingface.co/spaces/rreichert/starguard-desktop",
)
HF_SOVEREIGN = os.environ.get(
    "HF_SOVEREIGN",
    "https://huggingface.co/spaces/rreichert/sovereignshield",
)
AUDITSHIELD_URL = os.environ.get("AUDITSHIELD_URL", HF_AUDITSHIELD)
STARGUARD_URL = os.environ.get("STARGUARD_URL", HF_STARGUARD)
SOVEREIGNSHIELD_URL = os.environ.get("SOVEREIGNSHIELD_URL", HF_SOVEREIGN)
PORTFOLIO_URL = os.environ.get("PORTFOLIO_URL", "https://tinyurl.com/bdevpdz5")

_DEFAULT_AVATAR_RAW = (
    "https://raw.githubusercontent.com/StarGuardAi/HEDIS-MA-Top-12-w-HEI-Prep/"
    "main/platform-hub/LinkedIn_Avatar_300PX.png"
)

PURPLE = "#4A3E8F"
GOLD = "#D4AF37"
GREEN = "#10B981"
DARK = "#1A1633"

APPS = [
    {
        "id": "auditshield",
        "name": "AuditShield Live",
        "subtitle": "RADV Audit Defense",
        "description": (
            "AI-powered 3-source RAG coordinator covering NCQA HEDIS 2026, "
            "CMS audit protocols, and proprietary expertise. Defends HCC codes "
            "and supports RADV audit submissions."
        ),
        "url": AUDITSHIELD_URL,
        "color": PURPLE,
        "icon": "🛡️",
        "kpi_label": "Open Audit Flags",
        "kpi_key": "open_audit_flags",
        "kpi_color": GOLD,
    },
    {
        "id": "starguard",
        "name": "StarGuard Desktop",
        "subtitle": "Star Ratings Intelligence",
        "description": (
            "HEDIS gap analytics engine with HITL Admin Review, suppression "
            "logic, and real-time Star trajectory forecasting for Medicare "
            "Advantage plans."
        ),
        "url": STARGUARD_URL,
        "color": GOLD,
        "icon": "⭐",
        "kpi_label": "Open Star Gaps",
        "kpi_key": "open_star_gaps",
        "kpi_color": GOLD,
    },
    {
        "id": "sovereignshield",
        "name": "SovereignShield",
        "subtitle": "AI Governance & Compliance",
        "description": (
            "OPA policy-as-code governance engine with Terraform file upload, "
            "live policy editor, batch remediation, PDF export, and full "
            "Supabase audit logging."
        ),
        "url": SOVEREIGNSHIELD_URL,
        "color": GREEN,
        "icon": "⚖️",
        "kpi_label": "Policy Violations",
        "kpi_key": "open_policy_violations",
        "kpi_color": GREEN,
    },
]


def get_avatar_src() -> str:
    path = os.path.join(_APP_DIR, "LinkedIn_Avatar_300PX.png")
    if os.path.isfile(path):
        try:
            with open(path, "rb") as f:
                raw = f.read()
            return f"data:image/png;base64,{base64.b64encode(raw).decode()}"
        except OSError:
            pass
    return os.environ.get("AVATAR_URL", _DEFAULT_AVATAR_RAW)


AVATAR_SRC = get_avatar_src()


def make_qr_base64(url: str, size_px: int = 100, fill_color: str = "#1A1633") -> str:
    try:
        import qrcode

        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=8, border=2)
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image(fill_color=fill_color, back_color="white")
        img = img.resize((size_px, size_px))
        buf = BytesIO()
        img.save(buf, format="PNG")
        return f"data:image/png;base64,{base64.b64encode(buf.getvalue()).decode()}"
    except Exception:
        return ""


QR_PORTFOLIO = make_qr_base64(PORTFOLIO_URL, size_px=72)


def get_supabase_client():
    try:
        # Bare create_client: ClientOptions field names vary by supabase-py and can raise at init.
        from supabase import create_client

        url = os.environ.get("SUPABASE_URL") or os.environ.get("PLATFORM_SUPABASE_URL")
        key = (
            os.environ.get("SUPABASE_ANON_KEY")
            or os.environ.get("PLATFORM_SUPABASE_ANON_KEY")
            or os.environ.get("SUPABASE_KEY")
            or os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
        )
        if url and key:
            return create_client(url, key)
    except Exception:
        pass
    return None


def _run_with_deadline(fn, timeout_sec: float, default):
    """Run blocking Supabase call in a worker; return default on timeout or error."""
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as ex:
        fut = ex.submit(fn)
        try:
            return fut.result(timeout=timeout_sec)
        except concurrent.futures.TimeoutError:
            return default
        except Exception:
            return default


def _kpi_defaults() -> dict:
    return {
        "open_audit_flags": 0,
        "open_star_gaps": 0,
        "open_policy_violations": 0,
        "critical_open": 0,
        "remediated_total": 0,
        "sessions_today": 0,
    }


def _kpi_error_hint(exc: BaseException) -> str:
    """Map PostgREST / network errors to a single user-visible line."""
    try:
        from postgrest.exceptions import APIError as PostgrestAPIError

        if isinstance(exc, PostgrestAPIError):
            parts = " ".join(
                filter(
                    None,
                    [exc.message or "", exc.details or "", exc.hint or "", exc.code or ""],
                )
            ).lower()
            if any(
                s in parts
                for s in (
                    "platform_hub_kpis",
                    "does not exist",
                    "schema cache",
                    "could not find the table",
                    "undefined table",
                )
            ):
                return (
                    "Database view `platform_hub_kpis` is missing — run `platform_hub_schema.sql` "
                    "in the Supabase SQL Editor, then Refresh."
                )
            return "Supabase rejected the KPI query — check URL, anon key, and RLS on the view."
    except ImportError:
        pass
    text = str(exc).lower()
    if "platform_hub_kpis" in text or "does not exist" in text or "relation" in text:
        return (
            "Database view `platform_hub_kpis` is missing — run `platform_hub_schema.sql` "
            "in the Supabase SQL Editor, then Refresh."
        )
    return "Could not load KPIs (timeout or network). Try Refresh or check Supabase logs."


def fetch_kpis_dict_with_status(supabase) -> tuple[dict, str | None]:
    """Return (kpi dict, optional one-line status). Second item is None when load succeeded."""
    d = _kpi_defaults()
    if not supabase:
        return (
            d,
            "Supabase not configured — add SUPABASE_URL and SUPABASE_ANON_KEY in this Space's secrets.",
        )

    def _query():
        try:
            r = supabase.table("platform_hub_kpis").select("*").execute()
            if r.data:
                row = r.data[0]
                out = {**d, **{k: row.get(k, d.get(k, 0)) for k in d}}
                for k, v in row.items():
                    if k not in out:
                        out[k] = v
                return (out, None)
            return (d, None)
        except Exception as e:
            return (d, _kpi_error_hint(e))

    timeout_msg = "KPI query timed out — showing zeros. Check Supabase or click Refresh."
    return _run_with_deadline(_query, _QUERY_DEADLINE_SEC, (d, timeout_msg))


def fetch_kpis_dict(supabase) -> dict:
    """Backward-compatible: KPI values only."""
    return fetch_kpis_dict_with_status(supabase)[0]


def fetch_findings(supabase, limit: int = 20) -> pd.DataFrame:
    empty = pd.DataFrame()

    if not supabase:
        return empty

    def _query():
        try:
            r = (
                supabase.table("cross_app_findings")
                .select("*")
                .order("created_at", desc=True)
                .limit(limit)
                .execute()
            )
            if r.data:
                return pd.DataFrame(r.data)
        except Exception:
            pass
        return empty

    return _run_with_deadline(_query, _QUERY_DEADLINE_SEC, empty)


def log_session(supabase, app_name: str = "platform_hub") -> None:
    if not supabase:
        return

    def _insert():
        try:
            supabase.table("platform_sessions").insert({"app_name": app_name}).execute()
        except Exception:
            pass
        return None

    _run_with_deadline(_insert, _LOG_SESSION_DEADLINE_SEC, None)


CSS = f"""
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{
    background: {DARK};
    color: #fff;
    font-family: 'Segoe UI', system-ui, sans-serif;
    min-height: 100vh;
}}
.hub-header {{
    background: linear-gradient(135deg, {DARK} 0%, {PURPLE}BB 100%);
    padding: 1.25rem 2.5rem;
    border-bottom: 3px solid {GOLD};
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1.25rem;
    flex-wrap: wrap;
}}
.hub-header-main {{
    display: flex;
    align-items: center;
    gap: 1.25rem;
    flex: 1;
    min-width: 200px;
}}
.hub-avatar img {{
    width: 72px;
    height: 72px;
    border-radius: 50%;
    object-fit: cover;
    border: 3px solid {GOLD};
    box-shadow: 0 0 0 2px rgba(212,175,55,0.35);
}}
.hub-title {{ font-size: 1.75rem; font-weight: 700; letter-spacing: -0.5px; }}
.hub-subtitle {{ color: {GOLD}; font-size: 0.9rem; margin-top: 0.2rem; }}
.hub-header-right {{
    display: flex;
    align-items: center;
    gap: 1rem;
    flex-shrink: 0;
}}
.hub-badge {{
    background: {GREEN}22;
    border: 1px solid {GREEN};
    border-radius: 20px;
    padding: 0.35rem 0.85rem;
    font-size: 0.75rem;
    color: {GREEN};
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
}}
.hub-portfolio-qr img {{
    width: 72px;
    height: 72px;
    border-radius: 8px;
    border: 2px solid rgba(255,255,255,0.35);
}}
.kpi-strip {{
    display: flex;
    gap: 1px;
    background: rgba(255,255,255,0.06);
    border-bottom: 1px solid rgba(255,255,255,0.08);
    flex-wrap: wrap;
}}
.kpi-cell {{
    flex: 1;
    min-width: 120px;
    padding: 1rem 1.5rem;
    text-align: center;
    background: {DARK};
    transition: background 0.2s;
}}
.kpi-cell:hover {{ background: rgba(74,62,143,0.25); }}
.kpi-value {{ font-size: 2rem; font-weight: 800; line-height: 1; }}
.kpi-label {{
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: rgba(255,255,255,0.5);
    margin-top: 0.3rem;
}}
.apps-section {{ padding: 2rem 2.5rem; }}
.apps-grid {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1.5rem;
}}
@media (max-width: 992px) {{
    .apps-grid {{ grid-template-columns: 1fr; }}
}}
.app-card {{
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 14px;
    padding: 1.75rem;
    display: flex;
    flex-direction: column;
    transition: transform 0.2s, box-shadow 0.2s;
    position: relative;
    overflow: hidden;
}}
.app-card:hover {{
    transform: translateY(-5px);
    box-shadow: 0 12px 40px rgba(0,0,0,0.4);
}}
.app-icon {{ font-size: 2.25rem; margin-bottom: 0.75rem; }}
.app-status {{
    display: flex;
    align-items: center;
    gap: 0.4rem;
    font-size: 0.72rem;
    color: {GREEN};
    text-transform: uppercase;
    letter-spacing: 0.8px;
    margin-bottom: 0.5rem;
}}
.status-dot {{
    width: 7px; height: 7px;
    border-radius: 50%;
    background: {GREEN};
    animation: pulse 2s infinite;
}}
@keyframes pulse {{
    0%, 100% {{ opacity: 1; }}
    50% {{ opacity: 0.4; }}
}}
.app-name {{ font-size: 1.2rem; font-weight: 700; margin-bottom: 0.15rem; }}
.app-subtitle {{ font-size: 0.8rem; opacity: 0.6; margin-bottom: 0.75rem; }}
.app-description {{ font-size: 0.83rem; line-height: 1.55; opacity: 0.8; flex: 1; margin-bottom: 1.25rem; }}
.app-kpi {{
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.8rem;
    margin-bottom: 1.1rem;
    padding: 0.5rem 0.75rem;
    background: rgba(255,255,255,0.06);
    border-radius: 6px;
}}
.app-kpi-value {{ font-size: 1.2rem; font-weight: 800; }}
.app-btn {{
    display: block;
    text-align: center;
    padding: 0.65rem 1.25rem;
    border-radius: 8px;
    color: white;
    text-decoration: none;
    font-weight: 600;
    font-size: 0.875rem;
    transition: opacity 0.2s, transform 0.1s;
}}
.app-btn:hover {{ opacity: 0.85; transform: scale(0.98); }}
.alert-banner {{
    margin: 0 2.5rem 1.5rem;
    padding: 0.85rem 1.25rem;
    background: rgba(212,175,55,0.12);
    border: 1px solid {GOLD}66;
    border-radius: 8px;
    font-size: 0.85rem;
    display: flex;
    align-items: center;
    gap: 0.75rem;
}}
.hub-footer {{
    padding: 1.25rem 2.5rem;
    border-top: 1px solid rgba(255,255,255,0.07);
    text-align: center;
    font-size: 0.72rem;
    color: rgba(255,255,255,0.3);
}}
.findings-section {{
    padding: 0 2.5rem 2rem;
}}
.findings-section h4 {{
    color: {GOLD};
    margin-bottom: 0.75rem;
    font-size: 1rem;
}}
.findings-section .shiny-data-grid,
.findings-section table {{
    background: rgba(255,255,255,0.04) !important;
    color: #e8e8e8 !important;
    border-radius: 8px;
}}
.hub-kpi-hint {{
    margin: 0 2.5rem 0.75rem;
    padding: 0.5rem 0.85rem;
    font-size: 0.78rem;
    line-height: 1.45;
    color: rgba(255,255,255,0.72);
    border-left: 3px solid {GOLD};
    background: rgba(212,175,55,0.1);
    border-radius: 0 6px 6px 0;
}}
"""


def _app_card_ui(app: dict):
    return ui.div(
        ui.div(app["icon"], class_="app-icon"),
        ui.div(
            ui.span(class_="status-dot"),
            "Live on HuggingFace",
            class_="app-status",
        ),
        ui.h3(app["name"], class_="app-name", style=f"color: {app['color']};"),
        ui.p(app["subtitle"], class_="app-subtitle"),
        ui.p(app["description"], class_="app-description"),
        ui.output_ui(f"kpi_inline_{app['id']}"),
        ui.tags.a(
            f"Open {app['name']} →",
            href=app["url"],
            target="_blank",
            rel="noopener noreferrer",
            class_="app-btn",
            style=f"background: {app['color']};",
        ),
        class_="app-card",
        style=f"border-top: 3px solid {app['color']};",
    )


app_ui = ui.page_fluid(
    ui.tags.head(
        ui.tags.title("MA Compliance Intelligence Platform"),
        ui.tags.meta(name="viewport", content="width=device-width, initial-scale=1"),
        ui.tags.style(ui.HTML(CSS)),
    ),
    ui.div(
        ui.div(
            (
                ui.div(
                    ui.tags.img(src=AVATAR_SRC, alt="Profile"),
                    class_="hub-avatar",
                )
                if AVATAR_SRC
                else ui.div()
            ),
            ui.div(
                ui.h1("MA Compliance Intelligence Platform", class_="hub-title"),
                ui.p(
                    "Defend · Optimize · Govern  ·  Reichert Science & Intelligence",
                    class_="hub-subtitle",
                ),
            ),
            class_="hub-header-main",
        ),
        ui.div(
            ui.div("● 3 Apps Live", class_="hub-badge"),
            (
                ui.tags.a(
                    ui.tags.img(src=QR_PORTFOLIO, alt="Portfolio"),
                    href=PORTFOLIO_URL,
                    target="_blank",
                    rel="noopener noreferrer",
                    class_="hub-portfolio-qr",
                )
                if QR_PORTFOLIO
                else ui.div()
            ),
            class_="hub-header-right",
        ),
        class_="hub-header",
    ),
    ui.div(
        ui.div(ui.output_ui("kpi_strip_audit"), class_="kpi-cell"),
        ui.div(ui.output_ui("kpi_strip_star"), class_="kpi-cell"),
        ui.div(ui.output_ui("kpi_strip_policy"), class_="kpi-cell"),
        ui.div(ui.output_ui("kpi_strip_critical"), class_="kpi-cell"),
        ui.div(ui.output_ui("kpi_strip_remediated"), class_="kpi-cell"),
        class_="kpi-strip",
    ),
    ui.output_ui("kpi_status_bar"),
    ui.output_ui("alert_banner"),
    ui.div(
        ui.div(*[_app_card_ui(a) for a in APPS], class_="apps-grid"),
        class_="apps-section",
    ),
    ui.div(
        ui.input_action_button("refresh", "Refresh KPIs & findings", class_="btn btn-outline-light mb-3"),
        ui.output_data_frame("findings_table"),
        class_="findings-section",
    ),
    ui.div(
        "© 2026 Reichert Science & Intelligence · "
        "reichert.starguardai@email.com · +1 (480) 767-1337 · "
        "tinyurl.com/bdevpdz5",
        class_="hub-footer",
    ),
)


def server(input, output, session):
    supabase = reactive.Value(get_supabase_client())
    log_session(supabase())

    @reactive.Effect
    @reactive.event(input.refresh)
    def _():
        sb = get_supabase_client()
        supabase.set(sb)
        log_session(sb)

    @reactive.Calc
    def kpi_state():
        return fetch_kpis_dict_with_status(supabase())

    @reactive.Calc
    def kpis():
        return kpi_state()[0]

    @output
    @render.ui
    def kpi_status_bar():
        hint = kpi_state()[1]
        if not hint:
            return ui.div()
        return ui.div(hint, class_="hub-kpi-hint")

    def _kpi_div(value, label, color=GOLD):
        return ui.div(
            ui.div(str(value), class_="kpi-value", style=f"color:{color};"),
            ui.div(label, class_="kpi-label"),
        )

    @output
    @render.ui
    def kpi_strip_audit():
        return _kpi_div(kpis()["open_audit_flags"], "Open Audit Flags", GOLD)

    @output
    @render.ui
    def kpi_strip_star():
        return _kpi_div(kpis()["open_star_gaps"], "Open Star Gaps", GOLD)

    @output
    @render.ui
    def kpi_strip_policy():
        return _kpi_div(kpis()["open_policy_violations"], "Policy Violations", GREEN)

    @output
    @render.ui
    def kpi_strip_critical():
        return _kpi_div(kpis()["critical_open"], "Critical Open", "#EF4444")

    @output
    @render.ui
    def kpi_strip_remediated():
        return _kpi_div(kpis()["remediated_total"], "Remediated", GREEN)

    def _app_kpi_ui(app: dict):
        val = kpis().get(app["kpi_key"], "--")
        return ui.div(
            ui.span(str(val), class_="app-kpi-value", style=f"color:{app['kpi_color']};"),
            ui.span(f" {app['kpi_label']}", style="opacity:0.6;"),
            class_="app-kpi",
        )

    @output
    @render.ui
    def kpi_inline_auditshield():
        return _app_kpi_ui(APPS[0])

    @output
    @render.ui
    def kpi_inline_starguard():
        return _app_kpi_ui(APPS[1])

    @output
    @render.ui
    def kpi_inline_sovereignshield():
        return _app_kpi_ui(APPS[2])

    @output
    @render.ui
    def alert_banner():
        critical = kpis().get("critical_open", 0)
        if not critical or critical == "--":
            return ui.div()
        try:
            if int(critical) == 0:
                return ui.div()
        except (TypeError, ValueError):
            pass
        return ui.div(
            "⚠️",
            ui.span(
                f"{critical} critical finding(s) require cross-app review. "
                "Open AuditShield or SovereignShield to triage.",
                style="font-weight:500;",
            ),
            class_="alert-banner",
        )

    @output
    @render.data_frame
    def findings_table():
        df = fetch_findings(supabase())
        if df.empty:
            return pd.DataFrame({"message": ["No findings yet, or connect Supabase / run platform_hub_schema.sql."]})
        cols = ["title", "source_app", "severity", "status", "created_at"]
        return df[[c for c in cols if c in df.columns]]


app = App(app_ui, server=server)
