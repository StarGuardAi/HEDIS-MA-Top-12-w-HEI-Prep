# Sprint 2 — Integration Guide (read, then delete after wiring)
# ============================================================
# ui/mobile/ subpackage. All imports flow through ui.mobile so app.py stays clean.
#
# Import once in app.py:
#   from ui.mobile import (
#       mobile_kpi_strip,
#       mobile_dashboard_card,
#       mobile_source_accordion,
#       mobile_prompt_panel,
#       mobile_response_panel,
#       mobile_audit_stepper,
#       mobile_hedis_table,
#   )
#
# --- Call signatures per page ---
#
# 1. DASHBOARD PAGE (Executive View / KPI Overview)
# ------------------------------------------------
#   kpis = [
#       ("Star Rating", "4.2"),
#       ("HEDIS Gaps", "3"),
#       ("HCC RAF", "1.24"),
#       ("RADV Risk", "Low"),
#   ]
#   ui.div(
#       mobile_kpi_strip(kpis, id_prefix="exec_kpi"),
#       mobile_dashboard_card("Provider Risk", ui.output_ui("risk_chart"), id="risk_card"),
#       mobile_dashboard_card("Compliance Forecast", ui.output_ui("forecast_chart"), id="fc_card"),
#       ...
#   )
#
# 2. RAG / INTELLIGENCE PAGE
# --------------------------
#   sources = [
#       ("NCQA", ui.div(...)),
#       ("CMS", ui.div(...)),
#       ("Proprietary", ui.div(...)),
#   ]
#   ui.div(
#       mobile_source_accordion(sources, id_prefix="rag_src"),
#       mobile_prompt_panel("rag_prompt", placeholder="Ask a question..."),
#       mobile_response_panel("rag_response"),
#   )
#
# 3. AUDIT STEPPER PAGE (RADV flow, Documentation, etc.)
# -----------------------------------------------------
#   steps = [
#       ("Overview", ui.div(...existing overview UI...)),
#       ("Documentation", ui.div(...existing doc UI...)),
#       ("Review", ui.div(...existing review UI...)),
#       ("Submit", ui.div(...existing submit UI...)),
#       ("Complete", ui.div(...existing complete UI...)),
#   ]
#   mobile_audit_stepper(steps, id="radv_stepper")
#
# 4. HEDIS TABLE PAGE
# -------------------
#   mobile_hedis_table(
#       table_ui=ui.output_data_frame("hedis_table"),
#       filter_ui=ui.div(ui.input_select(...), ui.input_text(...)),
#       id="hedis_mobile",
#   )
#
# --- CSS ---
# Add to mobile.css (Sprint 1) or a new mobile_sprint2.css:
#   .mobile-kpi-strip, .mobile-kpi-item, .mobile-dashboard-card,
#   .stepper-progress-bar, .stepper-dots, .mobile-table-scroll-wrap,
#   .mobile-filter-toggle, .mobile-scroll-hint, .rag-prompt-input (font-size: 16px)
#
# Delete this file after integration.
