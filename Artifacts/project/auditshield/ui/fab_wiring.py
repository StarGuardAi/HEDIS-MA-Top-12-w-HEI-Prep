"""
Sprint 3: FAB wiring — Bootstrap tab switch for Mock Audit tab, sidebar close, scroll, gold pulse.
FAB uses DOM-only tab activation (no Shiny.setInputValue) to avoid server reactives crashing the UI.
Mobile: injects #rsi-hamburger when viewport ≤768px — clicks native collapse-toggle or Offcanvas API.
"""
from shiny import ui


def fab_wiring_script(
    *,
    main_tabs_id: str = "main_nav",
    audit_tab_id: str = "Mock Audit",
    run_audit_btn_id: str = "run_mock_audit",
    fab_id: str = "nav_mobile_fab",
) -> ui.Tag:
    """
    Wire the Run Audit FAB; inject mobile hamburger (#rsi-hamburger).

    main_tabs_id is kept for call-site compatibility; it is not passed to the client (no setInputValue).
    """
    _ = main_tabs_id  # unused — server nav input sync removed for mobile FAB path
    return ui.tags.script(
        f"""
(function(){{
'use strict';
var AT = '{audit_tab_id}';
var RB = '{run_audit_btn_id}';
var FID = '{fab_id}';

function injectHamburgerStyles() {{
  if (document.getElementById('rsi-hamburger-styles')) return;
  var s = document.createElement('style');
  s.id = 'rsi-hamburger-styles';
  s.textContent = '#rsi-hamburger{{position:fixed!important;top:10px!important;left:12px!important;'
    + 'z-index:1062!important;width:44px!important;height:44px!important;padding:0!important;margin:0!important;'
    + 'border:none!important;border-radius:8px!important;background:#4A3E8F!important;'
    + 'box-shadow:0 2px 8px rgba(74,62,143,0.45)!important;display:flex!important;flex-direction:column!important;'
    + 'align-items:center!important;justify-content:center!important;gap:5px!important;'
    + 'cursor:pointer!important;-webkit-tap-highlight-color:transparent!important;}}'
    + '#rsi-hamburger .rsi-bar{{display:block;width:20px;height:2px;background:#D4AF37!important;'
    + 'border-radius:1px;}}';
  document.head.appendChild(s);
}}

function toggleNativeSidebar() {{
  var t = document.querySelector('button.collapse-toggle');
  if (t) {{ t.click(); return; }}
  var off = document.querySelector('.offcanvas');
  if (off && typeof bootstrap !== 'undefined') {{
    try {{
      bootstrap.Offcanvas.getOrCreateInstance(off).toggle();
    }} catch (e) {{}}
  }}
}}

function ensureMobileHamburger() {{
  var mq = window.matchMedia('(max-width: 768px)');
  if (!mq.matches) {{
    var rm = document.getElementById('rsi-hamburger');
    if (rm) rm.remove();
    return;
  }}
  if (document.getElementById('rsi-hamburger')) return;
  injectHamburgerStyles();
  var btn = document.createElement('button');
  btn.id = 'rsi-hamburger';
  btn.type = 'button';
  btn.setAttribute('aria-label', 'Toggle sidebar');
  btn.innerHTML = '<span class="rsi-bar"></span><span class="rsi-bar"></span><span class="rsi-bar"></span>';
  btn.addEventListener('click', function(e) {{
    e.preventDefault();
    e.stopPropagation();
    toggleNativeSidebar();
  }});
  document.body.appendChild(btn);
}}

function doFabAction() {{
  var fab = document.getElementById(FID);
  if (!fab) return;

  var open = document.querySelectorAll('.offcanvas.show');
  open.forEach(function(el){{
    if (typeof bootstrap !== 'undefined') {{
      var inst = bootstrap.Offcanvas.getInstance(el);
      if (inst) inst.hide();
    }}
  }});

  var tabEl = document.querySelector('[data-bs-target="#' + AT + '"], [data-value="' + AT + '"], [href="#' + AT + '"]');
  if (tabEl) {{
    if (typeof bootstrap !== 'undefined') {{
      var tab = new bootstrap.Tab(tabEl);
      tab.show();
    }} else {{
      tabEl.click();
    }}
  }}

  window.scrollTo({{ top: 0, behavior: 'smooth' }});

  setTimeout(function(){{
    var runBtn = document.getElementById(RB) || document.querySelector('[id$="' + RB + '"]');
    if (runBtn) {{
      runBtn.classList.add('fab-pulse-gold');
      setTimeout(function(){{
        runBtn.classList.remove('fab-pulse-gold');
      }}, 2000);
    }}
  }}, 400);
}}

function setupFab() {{
  var fab = document.getElementById(FID);
  if (fab && !fab.dataset.fabWired) {{
    fab.dataset.fabWired = '1';
    fab.addEventListener('click', function(e){{
      e.preventDefault();
      doFabAction();
    }});
  }}
}}

function tick() {{
  ensureMobileHamburger();
  setupFab();
}}

if (document.readyState === 'loading') {{
  document.addEventListener('DOMContentLoaded', tick);
}} else {{ tick(); }}
setTimeout(tick, 500);
setTimeout(tick, 2000);
window.addEventListener('resize', function() {{ ensureMobileHamburger(); }});
}})();
"""
    )
