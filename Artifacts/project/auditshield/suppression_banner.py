# suppression_banner.py
# ─────────────────────────────────────────────────────────────
# Phase 2: Suppression Status Banner — AuditShield
# Shows active suppression count; wraps content with banner when rules exist
# Brand: Purple #4A3E8F | Gold #D4AF37
# ─────────────────────────────────────────────────────────────

from shiny import ui
from audit_trail import get_audit_suppressions


def suppression_banner_css() -> ui.tags.style:
    return ui.tags.style("""
        .suppression-banner {
            background: linear-gradient(135deg, #1a1240 0%, #2d1b4e 100%);
            border: 1px solid #4A3E8F;
            border-radius: 8px;
            padding: 12px 16px;
            margin-bottom: 16px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 10px;
        }
        .suppression-banner-icon { font-size: 18px; }
        .suppression-banner-text { color: #D4AF37; font-weight: 600; font-size: 13px; }
        .suppression-banner-count { color: #10b981; font-weight: 800; margin-left: 4px; }
    """)


def suppression_banner(app_type: str = "audit") -> ui.div:
    """
    Banner showing suppression status.
    app_type: "audit" (AuditShield) | "gap" (StarGuard)
    Drop above audit trail or HEDIS gap panel.
    """
    if app_type == "audit":
        rules = get_audit_suppressions()
    else:
        try:
            from hedis_gap_trail import get_gap_suppressions
            rules = get_gap_suppressions()
        except ImportError:
            rules = []

    count = len(rules)
    label = "Audit" if app_type == "audit" else "Gap"
    if count == 0:
        return ui.div()

    return ui.div(
        suppression_banner_css(),
        ui.div(
            ui.span("[!]", class_="suppression-banner-icon"),
            ui.span(
                f"{count} {label}(s) suppressed by active rules",
                class_="suppression-banner-text"
            ),
            style="display: flex; align-items: center; gap: 8px;"
        ),
        ui.a(
            "Manage in Admin View ->",
            href="#",
            style="color: #D4AF37; font-size: 12px; text-decoration: none;",
            id="suppression_manage_link"
        ),
        class_="suppression-banner"
    )
