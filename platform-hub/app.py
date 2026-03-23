"""
Platform Hub — Cross-app KPI dashboard
QR codes: portfolio + all 3 apps (AuditShield, StarGuard, SovereignShield)
Supabase: platform_hub_kpis, cross_app_findings, platform_alerts

Deploy: optional LinkedIn_Avatar_300PX.png next to this file (embedded as data URI).
Hugging Face Hub rejects raw PNGs in git unless Git Xet is used; the deploy script
omits the PNG from the Space repo — set AVATAR_URL or rely on the default GitHub raw URL below.
Update the three HuggingFace Space URLs (or env) if slugs change.
"""

from shiny import App, ui, render, reactive
import pandas as pd
import os
import base64
from io import BytesIO
from dotenv import load_dotenv

load_dotenv()

_APP_DIR = os.path.dirname(os.path.abspath(__file__))

# HuggingFace Space links (override with HF_AUDITSHIELD, HF_STARGUARD, HF_SOVEREIGN)
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

# Card + QR targets (env aliases for legacy / Render overrides)
AUDITSHIELD_URL = os.environ.get("AUDITSHIELD_URL", HF_AUDITSHIELD)
STARGUARD_URL = os.environ.get("STARGUARD_URL", HF_STARGUARD)
SOVEREIGNSHIELD_URL = os.environ.get("SOVEREIGNSHIELD_URL", HF_SOVEREIGN)

PORTFOLIO_URL = os.environ.get("PORTFOLIO_URL", "https://tinyurl.com/bdevpdz5")

# When PNG is not on disk (e.g. stripped for HF binary policy), use this URL as <img src>.
_DEFAULT_AVATAR_RAW = (
    "https://raw.githubusercontent.com/StarGuardAi/HEDIS-MA-Top-12-w-HEI-Prep/"
    "main/platform-hub/LinkedIn_Avatar_300PX.png"
)


def get_avatar_src() -> str:
    """Local PNG as data URI if present; else AVATAR_URL env or default GitHub raw URL."""
    path = os.path.join(_APP_DIR, "LinkedIn_Avatar_300PX.png")
    if os.path.isfile(path):
        try:
            with open(path, "rb") as f:
                raw = f.read()
            return f"data:image/png;base64,{base64.b64encode(raw).decode()}"
        except Exception:
            pass
    return os.environ.get("AVATAR_URL", _DEFAULT_AVATAR_RAW)


AVATAR_SRC = get_avatar_src()


def make_qr_base64(url: str, size_px: int = 140, fill_color: str = None, back_color: str = "white") -> str:
    """Generate QR code as base64 data URI (no external CDN, no disk I/O at runtime)."""
    if fill_color is None:
        fill_color = "#1A1633"
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


QR_PORTFOLIO = make_qr_base64(PORTFOLIO_URL, size_px=80)
QR_AUDITSHIELD = make_qr_base64(AUDITSHIELD_URL, size_px=100)
QR_STARGUARD = make_qr_base64(STARGUARD_URL, size_px=100)
QR_SOVEREIGNSHIELD = make_qr_base64(SOVEREIGNSHIELD_URL, size_px=100)


def get_supabase_client():
    try:
        from supabase import create_client

        # HF Space secrets: SUPABASE_URL + SUPABASE_ANON_KEY (standard names).
        # PLATFORM_SUPABASE_* matches AuditShield; SUPABASE_KEY is optional alias.
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


def fetch_kpis(supabase):
    """Fetch platform_hub_kpis view; return demo row if no Supabase."""
    if supabase:
        try:
            r = supabase.table("platform_hub_kpis").select("*").execute()
            if r.data and len(r.data) > 0:
                return pd.DataFrame(r.data)
        except Exception:
            pass
    return pd.DataFrame(
        [
            {
                "open_findings_total": 0,
                "open_audit_flags": 0,
                "open_star_gaps": 0,
                "open_policy_violations": 0,
                "critical_open": 0,
                "remediated_total": 0,
            }
        ]
    )


def fetch_findings(supabase, limit=20):
    """Fetch recent cross_app_findings."""
    if supabase:
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
    return pd.DataFrame()


def app_card(title: str, description: str, qr_data: str, url: str):
    """Single clickable card (entire surface links to HuggingFace); QR is non-nested img."""
    inner = ui.div(
        ui.div(
            ui.div(
                ui.h5(title, class_="mb-2 app-card-title"),
                ui.p(description, class_="app-card-desc small mb-0"),
                class_="flex-grow-1",
            ),
            ui.div(
                ui.tags.img(
                    src=qr_data,
                    alt=f"QR for {title}",
                    class_="app-card-qr",
                )
                if qr_data
                else ui.div(),
                class_="ms-auto flex-shrink-0",
            ),
            class_="d-flex align-items-start gap-3",
        ),
        class_="card-body",
    )
    return ui.tags.a(
        inner,
        href=url,
        target="_blank",
        rel="noopener noreferrer",
        class_="card h-100 app-card-link text-decoration-none text-reset",
    )


HUB_STYLES = """
:root {
  --brand-purple: #8b7bc8;
  --brand-purple-deep: #5c4d9d;
  --brand-gold: #e8c547;
  --brand-green: #2fb27a;
  --brand-dark: #1a1633;
}
body {
  background: linear-gradient(180deg, #f3f0fb 0%, #ffffff 45%);
  color: var(--brand-dark);
}
.hub-header-strip {
  background: linear-gradient(135deg, var(--brand-purple-deep), var(--brand-purple));
  color: #fff;
  border-radius: 0 0 1rem 1rem;
  padding: 1.25rem 1rem;
  margin-bottom: 1.5rem;
  box-shadow: 0 10px 28px rgba(26, 22, 51, 0.18);
}
.hub-header-strip h1 {
  color: #fff;
  font-weight: 700;
}
.hub-header-sub {
  color: rgba(255, 255, 255, 0.9) !important;
  max-width: 42rem;
}
.hub-avatar-wrap {
  flex-shrink: 0;
}
.hub-avatar-wrap img {
  width: 76px;
  height: 76px;
  border-radius: 50%;
  object-fit: cover;
  border: 3px solid var(--brand-gold);
  box-shadow:
    0 0 0 2px rgba(232, 197, 71, 0.4),
    0 8px 24px rgba(26, 22, 51, 0.45);
  display: block;
}
.hub-badge-live {
  background: var(--brand-green) !important;
  color: var(--brand-dark) !important;
  font-weight: 600;
  border: 1px solid rgba(26, 22, 51, 0.12);
}
.app-card-link {
  border: 2px solid var(--brand-purple) !important;
  border-radius: 0.5rem !important;
  transition: transform 0.15s ease, box-shadow 0.15s ease, border-color 0.15s ease;
  background: #fff;
}
.app-card-link:hover {
  border-color: var(--brand-gold) !important;
  box-shadow: 0 10px 28px rgba(92, 77, 157, 0.22);
  transform: translateY(-2px);
}
.app-card-title {
  color: var(--brand-dark);
}
.app-card-desc {
  color: #5a5470;
}
.app-card-qr {
  width: 100px;
  height: 100px;
  border-radius: 8px;
  border: 1px solid rgba(92, 77, 157, 0.25);
}
.hub-portfolio-qr {
  border-radius: 8px;
  border: 2px solid rgba(255, 255, 255, 0.5);
}
.card > .card-header,
.bslib-card .card-header {
  background: linear-gradient(90deg, var(--brand-purple-deep), var(--brand-purple)) !important;
  color: #fff !important;
  border: none !important;
  font-weight: 600;
}
table thead th {
  background: var(--brand-purple-deep) !important;
  color: #fff !important;
  border-color: rgba(255, 255, 255, 0.2) !important;
}
.bslib-sidebar-layout > .bslib-sidebar {
  border-right: 2px solid var(--brand-purple) !important;
  background: linear-gradient(180deg, #faf8ff, #ffffff) !important;
}
.hub-footer {
  border-top: 1px solid rgba(92, 77, 157, 0.2);
  margin-top: 2rem;
}
"""


app_ui = ui.page_fluid(
    ui.tags.head(
        ui.tags.title("Platform Hub — MA Compliance Intelligence"),
        ui.tags.meta(name="viewport", content="width=device-width, initial-scale=1"),
        ui.tags.style(ui.HTML(HUB_STYLES)),
    ),
    ui.div(
        ui.div(
            (
                ui.div(
                    ui.tags.img(
                        src=AVATAR_SRC,
                        alt="Profile",
                    ),
                    class_="hub-avatar-wrap me-3",
                )
                if AVATAR_SRC
                else ui.div()
            ),
            ui.div(
                ui.h1("Platform Hub", class_="mb-2"),
                ui.p(
                    "Cross-app findings and KPIs from AuditShield, StarGuard, and SovereignShield.",
                    class_="hub-header-sub mb-0 small",
                ),
                class_="flex-grow-1",
            ),
            ui.div(
                ui.span("3 Apps Live", class_="badge hub-badge-live me-2"),
                ui.tags.a(
                    ui.tags.img(
                        src=QR_PORTFOLIO,
                        alt="Portfolio QR",
                        class_="hub-portfolio-qr",
                        style="width:80px;height:80px;",
                    )
                    if QR_PORTFOLIO
                    else "",
                    href=PORTFOLIO_URL,
                    target="_blank",
                    rel="noopener noreferrer",
                    title="Portfolio",
                )
                if QR_PORTFOLIO
                else ui.div(),
                class_="d-flex align-items-center flex-shrink-0",
            ),
            class_="d-flex justify-content-between align-items-center flex-wrap gap-3 container py-4 hub-header-strip",
        ),
    ),
    ui.div(
        ui.div(
            ui.div(
                ui.div(app_card(
                    "AuditShield",
                    "HEDIS audit prep, gap analysis, and remediation tracking.",
                    QR_AUDITSHIELD,
                    AUDITSHIELD_URL,
                ), class_="col-md-4"),
                ui.div(app_card(
                    "StarGuard",
                    "STAR measures monitoring and gap closure.",
                    QR_STARGUARD,
                    STARGUARD_URL,
                ), class_="col-md-4"),
                ui.div(app_card(
                    "SovereignShield",
                    "Policy compliance and violation management.",
                    QR_SOVEREIGNSHIELD,
                    SOVEREIGNSHIELD_URL,
                ), class_="col-md-4"),
                class_="row g-3 mb-4",
            ),
            class_="container",
        ),
    ),
    ui.layout_sidebar(
        ui.sidebar(
            ui.h5("Refresh", class_="mb-2"),
            ui.input_action_button("refresh", "Refresh KPIs", class_="btn w-100"),
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
    ui.tags.footer(
        ui.p(
            "MA Compliance Intelligence Platform · AuditShield + StarGuard + SovereignShield",
            class_="text-muted small mb-0",
        ),
        class_="container py-3 hub-footer",
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
        cols = [
            "open_findings_total",
            "open_audit_flags",
            "open_star_gaps",
            "open_policy_violations",
            "critical_open",
            "remediated_total",
        ]
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
