# audit_trail_ui.py
# ─────────────────────────────────────────────────────────────
# RADV Audit Trail — UI Components for AuditShield-Live
# ─────────────────────────────────────────────────────────────

from shiny import ui


def audit_trail_css() -> ui.tags.style:
    return ui.tags.style("""
        .audit-panel {
            background: #0f0a2e;
            border: 1px solid #4A3E8F;
            border-radius: 10px;
            padding: 20px;
            margin-top: 16px;
        }
        .audit-panel-title {
            color: #D4AF37;
            font-size: 13px;
            font-weight: 700;
            letter-spacing: 1px;
            text-transform: uppercase;
            margin-bottom: 14px;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .audit-status-badge {
            display: inline-block;
            padding: 2px 10px;
            border-radius: 12px;
            font-size: 11px;
            font-weight: 700;
        }
        .status-open     { background:#1e3a5f; color:#60a5fa; }
        .status-reviewed { background:#1a3a2a; color:#10b981; }
        .status-closed   { background:#2a1a1a; color:#f87171; }
        .audit-push-success {
            color: #10b981;
            font-size: 12px;
            font-weight: 600;
            margin-top: 8px;
            display: flex;
            align-items: center;
            gap: 6px;
        }
        .audit-push-error {
            color: #f87171;
            font-size: 12px;
            margin-top: 8px;
        }
        .audit-sync-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 12px;
            font-size: 11px;
            color: #94a3b8;
        }
        .sync-live { color: #10b981; font-weight: 700; }
    """)


def audit_trail_panel() -> ui.div:
    """
    Full RADV Audit Trail panel — drop into any tab.
    Includes: push form, live table, status updater.
    """
    return ui.div(
        audit_trail_css(),

        # ── Header ──
        ui.div(
            ui.div("📋 RADV Audit Trail", class_="audit-panel-title"),
            ui.div(
                ui.output_text("audit_sync_status"),
                ui.input_action_button(
                    "btn_refresh_audits",
                    "↻ Refresh",
                    class_="btn btn-sm btn-outline-secondary"
                ),
                class_="audit-sync-row"
            )
        ),

        # ── Push New Audit Record ──
        ui.card(
            ui.card_header("Push New Audit to Cloud"),
            ui.layout_columns(
                ui.input_text(
                    "aud_measure_code", "Measure Code",
                    placeholder="e.g. CBP, CDC, W34"
                ),
                ui.input_text(
                    "aud_measure_name", "Measure Name",
                    placeholder="e.g. Controlling Blood Pressure"
                ),
                col_widths=[6, 6]
            ),
            ui.layout_columns(
                ui.input_text(
                    "aud_hcc_codes", "HCC Codes (comma-sep)",
                    placeholder="e.g. HCC18, HCC85"
                ),
                ui.input_numeric(
                    "aud_gaps", "Gaps Flagged", value=0, min=0
                ),
                col_widths=[6, 6]
            ),
            ui.layout_columns(
                ui.input_select(
                    "aud_meat_status", "M.E.A.T. Status",
                    choices=["PENDING", "VALIDATED", "FAILED", "PARTIAL"]
                ),
                ui.input_numeric(
                    "aud_risk_score", "RADV Risk Score",
                    value=0.0, min=0.0, max=1.0, step=0.01
                ),
                col_widths=[6, 6]
            ),
            ui.div(
                ui.input_action_button(
                    "btn_generate_summary",
                    "🤖 Generate Summary",
                    class_="btn btn-outline-primary btn-sm mb-2",
                    style="background:#4A3E8F; color:#fff; border-color:#D4AF37;"
                ),
                class_="audit-generate-row"
            ),
            ui.input_text_area(
                "aud_claude_summary", "Claude AI Summary",
                placeholder="Fill measure details above, click 🤖 Generate Summary — or paste manually.",
                rows=3
            ),
            ui.input_action_button(
                "btn_push_audit",
                "☁ Push to Cloud",
                class_="btn btn-primary w-100",
                style="background:#4A3E8F; border-color:#4A3E8F;"
            ),
            ui.output_ui("audit_push_result"),
        ),

        # ── Recent Audit Table ──
        ui.card(
            ui.card_header("Recent Cloud Audit Records"),
            ui.output_data_frame("audit_trail_table"),
        ),

        # ── Status Updater ──
        ui.card(
            ui.card_header("Update Audit Status"),
            ui.layout_columns(
                ui.input_text(
                    "aud_id_update", "Audit ID",
                    placeholder="e.g. AUD-20260304-104512"
                ),
                ui.input_select(
                    "aud_new_status", "New Status",
                    choices=["OPEN", "REVIEWED", "CLOSED"]
                ),
                col_widths=[7, 5]
            ),
            ui.input_action_button(
                "btn_update_status",
                "Update Status",
                class_="btn btn-warning btn-sm"
            ),
            ui.output_ui("audit_update_result"),
        ),

        class_="audit-panel"
    )
