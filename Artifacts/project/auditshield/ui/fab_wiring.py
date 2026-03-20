"""
Sprint 3: FAB wiring — Bootstrap tab switch for Mock Audit tab, scroll, gold pulse.
FAB uses DOM-only tab activation (no Shiny.setInputValue) to avoid server reactives crashing the UI.
Mobile: #rsi-hamburger toggles body.rsi-drawer-open; the active tab's live .sidebar is #rsi-drawer
(pure CSS transform — no bslib Sidebar, Offcanvas, or collapse-toggle). Cloning sidebar markup would
duplicate node ids and break Shiny bindings, so the drawer surface is the real sidebar element.
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
    Wire the Run Audit FAB; inject mobile hamburger (#rsi-hamburger) and drawer backdrop.

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

function getActiveSidebar() {{
  var pane = document.querySelector('.tab-pane.active');
  if (pane) {{
    var sb = pane.querySelector('.bslib-sidebar-layout > .sidebar');
    if (sb) return sb;
  }}
  return document.querySelector('.bslib-sidebar-layout > .sidebar');
}}

function syncDrawerSidebarId() {{
  var active = getActiveSidebar();
  document.querySelectorAll('#rsi-drawer').forEach(function(el) {{
    el.removeAttribute('id');
  }});
  if (active) active.id = 'rsi-drawer';
}}

function ensureDrawerChrome() {{
  if (document.getElementById('rsi-drawer-backdrop')) return;
  var bd = document.createElement('div');
  bd.id = 'rsi-drawer-backdrop';
  bd.setAttribute('aria-hidden', 'true');
  document.body.appendChild(bd);
  bd.addEventListener('click', function() {{
    document.body.classList.remove('rsi-drawer-open');
    var hb = document.getElementById('rsi-hamburger');
    if (hb) hb.setAttribute('aria-expanded', 'false');
  }});
}}

function toggleDrawer() {{
  syncDrawerSidebarId();
  if (!getActiveSidebar()) return;
  var on = document.body.classList.toggle('rsi-drawer-open');
  var hb = document.getElementById('rsi-hamburger');
  if (hb) hb.setAttribute('aria-expanded', on ? 'true' : 'false');
}}

function ensureMobileHamburger() {{
  var mq = window.matchMedia('(max-width: 768px)');
  if (!mq.matches) {{
    var rm = document.getElementById('rsi-hamburger');
    if (rm) rm.remove();
    var bd = document.getElementById('rsi-drawer-backdrop');
    if (bd) bd.remove();
    document.body.classList.remove('rsi-drawer-open');
    document.querySelectorAll('#rsi-drawer').forEach(function(el) {{ el.removeAttribute('id'); }});
    return;
  }}
  ensureDrawerChrome();
  syncDrawerSidebarId();
  if (document.getElementById('rsi-hamburger')) return;
  var btn = document.createElement('button');
  btn.id = 'rsi-hamburger';
  btn.type = 'button';
  btn.setAttribute('aria-label', 'Open navigation');
  btn.setAttribute('aria-expanded', 'false');
  btn.setAttribute('aria-controls', 'rsi-drawer');
  btn.innerHTML = '<span class="rsi-bar"></span><span class="rsi-bar"></span><span class="rsi-bar"></span>';
  btn.addEventListener('click', function(e) {{
    e.preventDefault();
    e.stopPropagation();
    toggleDrawer();
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

document.addEventListener('shown.bs.tab', function() {{
  document.body.classList.remove('rsi-drawer-open');
  var hb = document.getElementById('rsi-hamburger');
  if (hb) hb.setAttribute('aria-expanded', 'false');
  syncDrawerSidebarId();
}});

if (document.readyState === 'loading') {{
  document.addEventListener('DOMContentLoaded', tick);
}} else {{ tick(); }}
setTimeout(tick, 500);
setTimeout(tick, 2000);
window.addEventListener('resize', function() {{ ensureMobileHamburger(); }});
}})();
"""
    )
