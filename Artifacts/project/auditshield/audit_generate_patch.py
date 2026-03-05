#!/usr/bin/env python3
"""
audit_generate_patch.py — Apply AI Summary Generation to Audit Trail

Patches:
1. audit_trail_ui.py — add "🤖 Generate Summary" button before textarea
2. app.py — add JS handler in head_content for loading + set-summary
3. app.py — add generate server handler that calls Claude

Run from auditshield dir:
    python audit_generate_patch.py
"""
from pathlib import Path

BASE = Path(__file__).resolve().parent

# ─── 1. audit_trail_ui.py: textarea + button ─────────────────────────────────
AUDIT_TRAIL_UI_OLD = '''            ui.input_text_area(
                "aud_claude_summary", "Claude AI Summary",
                placeholder="Paste Claude-generated audit summary here...",
                rows=3
            ),'''

AUDIT_TRAIL_UI_NEW = '''            ui.div(
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
            ),'''

# ─── 2. app.py: JS handler — insert before cloud_status_css() ─────────────────
JS_SCRIPT_BLOCK = r'''        ui.tags.script("""
            (function(){
                if (typeof Shiny !== 'undefined') {
                    Shiny.addCustomMessageHandler('audit_show_loading', function(msg) {
                        var ta = document.getElementById('aud_claude_summary') || document.querySelector('textarea[id$="aud_claude_summary"]');
                        if (ta) ta.value = '⏳ Claude is generating...';
                    });
                    Shiny.addCustomMessageHandler('audit_set_summary', function(msg) {
                        var v = (msg && msg.value) || msg || '';
                        var ta = document.getElementById('aud_claude_summary') || document.querySelector('textarea[id$="aud_claude_summary"]');
                        if (ta) ta.value = v;
                        try { Shiny.setInputValue('aud_claude_summary', v); } catch(e) {}
                    });
                }
            })();
        """),
        cloud_status_css(),'''

# ─── 3. app.py: generate server handler ─────────────────────────────────────
# Insert before _audit_trail_push
APP_SERVER_ANCHOR = '''    @reactive.Effect
    @reactive.event(input.btn_push_audit)
    def _audit_trail_push():'''

APP_SERVER_INSERT = '''
    @reactive.Effect
    @reactive.event(input.btn_generate_summary)
    def _audit_generate_summary():
        session.send_custom_message("audit_show_loading", {})
        try:
            from app_config import get_anthropic_client
            client = get_anthropic_client()
            measure_code = input.aud_measure_code() or "N/A"
            measure_name = input.aud_measure_name() or "N/A"
            hcc_codes = (input.aud_hcc_codes() or "").strip() or "N/A"
            meat_status = input.aud_meat_status() or "PENDING"
            risk_score = input.aud_risk_score() or 0.0
            prompt = f"""Generate a concise RADV compliance-grade audit summary (2-4 sentences) for:
Measure: {measure_code} — {measure_name}
HCC Codes: {hcc_codes}
M.E.A.T. Status: {meat_status}
RADV Risk Score: {risk_score}

Write a professional summary suitable for audit documentation. Be specific and compliance-focused. Return only the summary text, no preamble."""
            resp = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=300,
                messages=[{"role": "user", "content": prompt}],
            )
            summary = resp.content[0].text.strip() if resp.content else ""
            session.send_custom_message("audit_set_summary", {"value": summary})
        except Exception as e:
            err_msg = f"Error: {str(e)}"
            if "ANTHROPIC_API_KEY" in str(e) or "api_key" in str(e).lower():
                err_msg = "ANTHROPIC_API_KEY not set. Add to .env or Space secrets."
            session.send_custom_message("audit_set_summary", {"value": err_msg})

    @reactive.Effect
    @reactive.event(input.btn_push_audit)
    def _audit_trail_push():'''


def main():
    print("Applying Audit Generate patches...")

    # 1. audit_trail_ui.py
    ui_path = BASE / "audit_trail_ui.py"
    if not ui_path.exists():
        print("[FAIL] audit_trail_ui.py not found")
        return
    ui_text = ui_path.read_text(encoding="utf-8")
    if AUDIT_TRAIL_UI_NEW.strip() in ui_text:
        print("[OK] textarea + button: already patched")
    elif AUDIT_TRAIL_UI_OLD.strip() in ui_text:
        ui_text = ui_text.replace(AUDIT_TRAIL_UI_OLD, AUDIT_TRAIL_UI_NEW)
        ui_path.write_text(ui_text, encoding="utf-8")
        print("[OK] textarea + button: patched")
    else:
        print("[WARN] textarea + button: not found (manual edit needed)")

    # 2. app.py — JS handler
    app_path = BASE / "app.py"
    if not app_path.exists():
        print("[FAIL] app.py not found")
        return
    app_text = app_path.read_text(encoding="utf-8")

    if 'audit_show_loading' in app_text and 'audit_set_summary' in app_text:
        print("[OK] JS handler in head_content: already patched")
    elif "        cloud_status_css()," in app_text:
        old = "        cloud_status_css(),"
        if JS_SCRIPT_BLOCK not in app_text:
            app_text = app_text.replace(old, JS_SCRIPT_BLOCK, 1)
            app_path.write_text(app_text, encoding="utf-8")
            print("[OK] JS handler in head_content: patched")
        else:
            print("[OK] JS handler in head_content: already patched")
    else:
        print("[WARN] JS handler: cloud_status_css anchor not found")

    # 3. app.py — generate server handler
    if 'def _audit_generate_summary():' in app_text:
        print("[OK] generate server handler: already patched")
    elif APP_SERVER_ANCHOR.strip() in app_text:
        app_text = app_text.replace(APP_SERVER_ANCHOR, APP_SERVER_INSERT)
        app_path.write_text(app_text, encoding="utf-8")
        print("[OK] generate server handler: inserted")
    else:
        print("[WARN] generate server handler: anchor not found (manual edit needed)")

    print("\nDone. Restart: shiny run app.py --reload")


if __name__ == "__main__":
    main()
