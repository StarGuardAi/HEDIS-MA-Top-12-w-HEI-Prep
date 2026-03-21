"""
Sprint 3: FAB wiring — Bootstrap tab switch for Mock Audit tab, scroll, gold pulse.
Mobile: hamburger opens #rsi-drawer, a dedicated nav panel built from navbar tab links (no Shiny
sidebar aside). Filters stay in each tab's main content. Desktop sidebar unchanged.
"""

from shiny import ui

# Shown in mobile nav drawer footer (mailto only — no Shiny binding).
_DRAWER_CONTACT_EMAIL = "contact@starguardai.com"


def fab_wiring_script(
    *,
    main_tabs_id: str = "main_nav",
    audit_tab_id: str = "Mock Audit",
    run_audit_btn_id: str = "run_mock_audit",
    fab_id: str = "nav_mobile_fab",
) -> ui.Tag:
    """
    Wire the Run Audit FAB; inject mobile hamburger, backdrop, and rsi-nav-drawer from navbar tabs.

    main_tabs_id is kept for call-site compatibility; it is not passed to the client (no setInputValue).
    """
    _ = main_tabs_id
    contact = _DRAWER_CONTACT_EMAIL
    return ui.tags.script(
        f"""
(function(){{
'use strict';
var AT = '{audit_tab_id}';
var RB = '{run_audit_btn_id}';
var FID = '{fab_id}';
var CONTACT = '{contact}';

function applyDrawerOpen(open) {{
  if (open) document.body.classList.add('rsi-drawer-open');
  else document.body.classList.remove('rsi-drawer-open');
  var hb = document.getElementById('rsi-hamburger');
  if (hb) hb.setAttribute('aria-expanded', open ? 'true' : 'false');
  var dr = document.getElementById('rsi-drawer');
  if (dr) dr.setAttribute('aria-hidden', open ? 'false' : 'true');
}}

function ensureBackdrop() {{
  if (document.getElementById('rsi-drawer-backdrop')) return;
  var bd = document.createElement('div');
  bd.id = 'rsi-drawer-backdrop';
  bd.setAttribute('aria-hidden', 'true');
  document.body.appendChild(bd);
  bd.addEventListener('click', function() {{ applyDrawerOpen(false); }});
}}

function ensureNavDrawerShell() {{
  if (document.getElementById('rsi-drawer')) return;
  var aside = document.createElement('aside');
  aside.id = 'rsi-drawer';
  aside.className = 'rsi-nav-drawer';
  aside.setAttribute('aria-label', 'Main navigation');
  aside.setAttribute('aria-hidden', 'true');
  aside.innerHTML = ''
    + '<div class="rsi-nav-drawer-header">AuditShield</div>'
    + '<div class="rsi-nav-drawer-list" role="navigation"></div>'
    + '<div class="rsi-nav-drawer-footer">'
    + '<a class="rsi-nav-drawer-email" href="mailto:' + CONTACT + '">' + CONTACT + '</a>'
    + '</div>';
  document.body.appendChild(aside);
}}

function collectNavbarTabAnchors() {{
  var nav = document.querySelector('nav.navbar');
  if (!nav) return [];
  var out = [];
  nav.querySelectorAll('a.nav-link').forEach(function(a) {{
    var toggle = a.getAttribute('data-bs-toggle') || a.getAttribute('data-toggle');
    if (toggle !== 'tab') return;
    if (a.closest('.dropdown-menu')) return;
    out.push(a);
  }});
  return out;
}}

function populateNavDrawer() {{
  var drawer = document.getElementById('rsi-drawer');
  if (!drawer) return;
  var list = drawer.querySelector('.rsi-nav-drawer-list');
  if (!list) return;
  list.innerHTML = '';
  var anchors = collectNavbarTabAnchors();
  anchors.forEach(function(a) {{
    var label = (a.textContent || '').replace(/\\s+/g, ' ').trim();
    if (!label) return;
    var btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'rsi-nav-drawer-btn';
    if (a.classList.contains('active')) btn.classList.add('active');
    btn.textContent = label;
    btn.addEventListener('click', function(ev) {{
      ev.preventDefault();
      applyDrawerOpen(false);
      if (typeof bootstrap !== 'undefined' && bootstrap.Tab) {{
        try {{
          bootstrap.Tab.getOrCreateInstance(a).show();
        }} catch (e) {{
          a.click();
        }}
      }} else {{
        a.click();
      }}
    }});
    list.appendChild(btn);
  }});
}}

function toggleDrawer() {{
  if (document.body.classList.contains('rsi-drawer-open')) {{
    applyDrawerOpen(false);
    return;
  }}
  populateNavDrawer();
  applyDrawerOpen(true);
}}

function ensureMobileHamburger() {{
  var mq = window.matchMedia('(max-width: 768px)');
  if (!mq.matches) {{
    var rm = document.getElementById('rsi-hamburger');
    if (rm) rm.remove();
    var bd = document.getElementById('rsi-drawer-backdrop');
    if (bd) bd.remove();
    var dr = document.getElementById('rsi-drawer');
    if (dr) dr.remove();
    document.body.classList.remove('rsi-drawer-open');
    return;
  }}
  ensureBackdrop();
  ensureNavDrawerShell();
  populateNavDrawer();
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
  document.querySelectorAll('.offcanvas.show').forEach(function(el){{
    if (typeof bootstrap !== 'undefined') {{
      var inst = bootstrap.Offcanvas.getInstance(el);
      if (inst) inst.hide();
    }}
  }});
  var tabEl = document.querySelector('[data-bs-target="#' + AT + '"], [data-value="' + AT + '"], [href="#' + AT + '"]');
  if (tabEl) {{
    if (typeof bootstrap !== 'undefined') {{
      try {{ new bootstrap.Tab(tabEl).show(); }} catch (e) {{ tabEl.click(); }}
    }} else {{
      tabEl.click();
    }}
  }}
  window.scrollTo({{ top: 0, behavior: 'smooth' }});
  setTimeout(function(){{
    var runBtn = document.getElementById(RB) || document.querySelector('[id$="' + RB + '"]');
    if (runBtn) {{
      runBtn.classList.add('fab-pulse-gold');
      setTimeout(function(){{ runBtn.classList.remove('fab-pulse-gold'); }}, 2000);
    }}
  }}, 400);
}}

function setupFab() {{
  var fab = document.getElementById(FID);
  if (fab && !fab.dataset.fabWired) {{
    fab.dataset.fabWired = '1';
    fab.addEventListener('click', function(e){{ e.preventDefault(); doFabAction(); }});
  }}
}}

function tick() {{
  ensureMobileHamburger();
  setupFab();
}}

document.addEventListener('shown.bs.tab', function() {{
  applyDrawerOpen(false);
  populateNavDrawer();
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
