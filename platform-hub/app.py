"""
Platform Hub — Cross-app KPI dashboard
QR codes: portfolio + all 3 apps (AuditShield, StarGuard, SovereignShield)
Supabase: platform_hub_kpis, cross_app_findings, platform_alerts
"""

from shiny import App, ui, render, reactive
import pandas as pd
import os
import base64
from io import BytesIO
from dotenv import load_dotenv

load_dotenv()

# QR code URLs (override via env for Spaces)
PORTFOLIO_URL = os.environ.get("PORTFOLIO_URL", "https://tinyurl.com/bdevpdz5")
AUDITSHIELD_URL = os.environ.get("AUDITSHIELD_URL", "https://auditshield-live.onrender.com")
STARGUARD_URL = os.environ.get("STARGUARD_URL", "https://starguard-desktop.onrender.com")
# Live Space slug is rreichert/sovereignshield (not sovereignshield-desktop).
SOVEREIGNSHIELD_URL = os.environ.get(
    "SOVEREIGNSHIELD_URL",
    "https://huggingface.co/spaces/rreichert/sovereignshield",
)

def make_qr_base64(url: str, size_px: int = 140, fill_color: str = "#1A1633", back_color: str = "white") -> str:
    """Generate QR code as base64 data URI (no external CDN, no disk I/O at runtime)."""
    try:
        import qrcode
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=8, border=2)
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image(fill_color=fill_color, back_color=back_color)
        img = img.resize((size_px, size_px))
        buf = BytesIO()
        img.save(buf, format="PNG")
        return f"data:image/png;base64,{base64.b64encode(buf.getvalue()).decode()}"
    except Exception:
        return ""

# Generate QR codes at startup
QR_PORTFOLIO = make_qr_base64(PORTFOLIO_URL, size_px=80)
QR_AUDITSHIELD = make_qr_base64(AUDITSHIELD_URL, size_px=100)
QR_STARGUARD = make_qr_base64(STARGUARD_URL, size_px=100)
QR_SOVEREIGNSHIELD = make_qr_base64(SOVEREIGNSHIELD_URL, size_px=100)

# Supabase connection (optional; app runs without it, shows demo data)
def get_supabase_client():
    try:
        from supabase import create_client
        url = os.environ.get("SUPABASE_URL") or os.environ.get("PLATFORM_SUPABASE_URL")
        key = os.environ.get("SUPABASE_ANON_KEY") or os.environ.get("PLATFORM_SUPABASE_ANON_KEY") or os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
        if url and key:
            return create_client(url, key)
    except Exception:
        pass
    return None

def fetch_kpis(supabase):
    """Fetch platform_hub_kpis view; return demo row if no Supabase."""
    if supabase:
        try:
            r = supabase.table("platform_hub_kpis").select("*").execute()
            if r.data and len(r.data) > 0:
                return pd.DataFrame(r.data)
        except Exception:
            pass
    return pd.DataFrame([{
        "open_findings_total": 0,
        "open_audit_flags": 0,
        "open_star_gaps": 0,
        "open_policy_violations": 0,
        "critical_open": 0,
        "remediated_total": 0,
    }])

def fetch_findings(supabase, limit=20):
    """Fetch recent cross_app_findings."""
    if supabase:
        try:
            r = supabase.table("cross_app_findings").select("*").order("created_at", desc=True).limit(limit).execute()
            if r.data:
                return pd.DataFrame(r.data)
        except Exception:
            pass
    return pd.DataFrame()

# App cards with QR codes
def app_card(title: str, description: str, qr_data: str, url: str):
    return ui.div(
        ui.div(
            ui.div(
                ui.h5(title, class_="mb-2"),
                ui.p(description, class_="text-muted small mb-0"),
                class_="flex-grow-1",
            ),
            ui.div(
                ui.tags.a(
                    ui.tags.img(src=qr_data, alt=f"QR for {title}", style="width:100px;height:100px;border-radius:6px;") if qr_data else "",
                    href=url,
                    target="_blank",
                    rel="noopener",
                ),
                class_="ms-auto",
            ) if qr_data else ui.div(),
            class_="d-flex align-items-start gap-3",
        ),
        class_="card-body",
    )

app_ui = ui.page_fluid(
    ui.tags.head(
        ui.tags.title("Platform Hub — MA Compliance Intelligence"),
        ui.tags.meta(name="viewport", content="width=device-width, initial-scale=1"),
    ),
    ui.div(
        ui.div(
            ui.h1("Platform Hub", class_="mb-2"),
            ui.p("Cross-app findings and KPIs from AuditShield, StarGuard, and SovereignShield.", class_="text-muted mb-0"),
            class_="flex-grow-1",
        ),
        ui.div(
            ui.span("3 Apps Live", class_="badge bg-success me-2"),
            ui.tags.a(
                ui.tags.img(src=QR_PORTFOLIO, alt="Portfolio", style="width:80px;height:80px;border-radius:6px;") if QR_PORTFOLIO else "",
                href=PORTFOLIO_URL,
                target="_blank",
                rel="noopener",
                title="Portfolio",
            ) if QR_PORTFOLIO else ui.div(),
            class_="d-flex align-items-center",
        ),
        class_="d-flex justify-content-between align-items-start flex-wrap gap-3 container py-4",
    ),
    ui.div(
        ui.div(
            ui.div(
                ui.div(
                    app_card(
                        "AuditShield",
                        "HEDIS audit prep, gap analysis, and remediation tracking.",
                        QR_AUDITSHIELD,
                        AUDITSHIELD_URL,
                    ),
                    class_="card h-100 col-md-4",
                ),
                ui.div(
                    app_card(
                        "StarGuard",
                        "STAR measures monitoring and gap closure.",
                        QR_STARGUARD,
                        STARGUARD_URL,
                    ),
                    class_="card h-100 col-md-4",
                ),
                ui.div(
                    app_card(
                        "SovereignShield",
                        "Policy compliance and violation management.",
                        QR_SOVEREIGNSHIELD,
                        SOVEREIGNSHIELD_URL,
                    ),
                    class_="card h-100 col-md-4",
                ),
                class_="row g-3 mb-4",
            ),
            class_="container",
        ),
    ),
    ui.layout_sidebar(
        ui.sidebar(
            ui.h5("Refresh"),
            ui.input_action_button("refresh", "Refresh KPIs"),
            width=250,
        ),
        ui.tags.main(
            ui.card(
                ui.card_header("Platform KPIs"),
                ui.output_data_frame("kpis_table"),
            ),
            ui.card(
                ui.card_header("Recent Findings"),
                ui.output_data_frame("findings_table"),
            ),
        ),
    ),
    ui.footer(
        ui.p("MA Compliance Intelligence Platform · AuditShield + StarGuard + SovereignShield", class_="text-muted small"),
        class_="container py-2",
    ),
)

def server(input, output, session):
    supabase = reactive.Value(get_supabase_client())

    @reactive.Effect
    @reactive.event(input.refresh)
    def _():
        supabase.set(get_supabase_client())

    @output
    @render.data_frame
    def kpis_table():
        kpis = fetch_kpis(supabase())
        cols = ["open_findings_total", "open_audit_flags", "open_star_gaps", "open_policy_violations", "critical_open", "remediated_total"]
        return kpis[[c for c in cols if c in kpis.columns]] if not kpis.empty else pd.DataFrame()

    @output
    @render.data_frame
    def findings_table():
        df = fetch_findings(supabase())
        if df.empty:
            return pd.DataFrame({"message": ["No findings yet. Connect Supabase and run platform_hub_schema.sql."]})
        cols = ["title", "source_app", "severity", "status", "created_at"]
        return df[[c for c in cols if c in df.columns]]

app = App(app_ui, server=server)
