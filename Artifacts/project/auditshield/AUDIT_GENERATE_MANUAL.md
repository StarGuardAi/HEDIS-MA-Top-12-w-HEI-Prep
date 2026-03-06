# Audit Generate — Manual Patch Guide

Use this when `python audit_generate_patch.py` reports "not found" or "manual edit needed."

---

## 1. audit_trail_ui.py — Add Generate Summary Button

**Location:** Before the `aud_claude_summary` textarea (around line 121)

**Find:**
```python
            ui.input_text_area(
                "aud_claude_summary", "Claude AI Summary",
                placeholder="Paste Claude-generated audit summary here...",
                rows=3
            ),
```

**Replace with:**
```python
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
```

---

## 2. app.py — JS Handler in head_content

**Location:** Inside `ui.tags.head(...)`, before `cloud_status_css(),` (around line 207)

**Find:**
```python
        cloud_status_css(),
```

**Replace with:**
```python
        ui.tags.script("""
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
        cloud_status_css(),
```

---

## 3. app.py — Generate Server Handler

**Location:** In the server function, just before `def _audit_trail_push():` (around line 1228)

**Find:**
```python
    @reactive.Effect
    @reactive.event(input.btn_push_audit)
    def _audit_trail_push():
```

**Replace with:**
```python
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
    def _audit_trail_push():
```

---

## After Applying

1. Ensure `ANTHROPIC_API_KEY` is set in `.env` or HuggingFace Space secrets.
2. Restart: `shiny run app.py --reload`
3. In Audit Trail tab: fill Measure Code, Name, HCC Codes, M.E.A.T., Risk Score → click **🤖 Generate Summary** → wait 2–3 sec → textarea fills → click **☁ Push to Cloud**.
