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
var DBG = '[rsi-drawer]';

function _visibleEl(el) {{
  if (!el) return false;
  var st = window.getComputedStyle(el);
  if (st.display === 'none' || st.visibility === 'hidden') return false;
  var r = el.getBoundingClientRect();
  return r.width > 0 && r.height > 0;
}}

function _sidebarCandidates() {{
  return document.querySelectorAll('.bslib-sidebar-layout > .sidebar');
}}

function getActiveSidebar() {{
  var p1 = document.querySelector('.tab-pane.active.show');
  var p2 = document.querySelector('.tab-pane.active');
  var p3 = document.querySelector('[role="tabpanel"].active');
  var tried = [
    {{ label: '.tab-pane.active.show', el: p1 }},
    {{ label: '.tab-pane.active', el: p2 }},
    {{ label: '[role=tabpanel].active', el: p3 }}
  ];
  var panePick = p1 || p2 || p3;
  if (panePick) {{
    var sb = panePick.querySelector('.bslib-sidebar-layout > .sidebar');
    if (sb) {{
      console.log(DBG, 'getActiveSidebar: via pane', panePick.className, 'sidebar=', sb.tagName, sb.className, 'visible=', _visibleEl(sb));
      return sb;
    }}
    console.log(DBG, 'getActiveSidebar: active pane has no sidebar (e.g. Executive View)', panePick.className);
    return null;
  }}
  console.log(DBG, 'getActiveSidebar: no active tab panel', tried.map(function(t) {{ return t.label + ':' + !!t.el; }}).join(', '));
  var all = _sidebarCandidates();
  console.log(DBG, 'getActiveSidebar: layout count=', document.querySelectorAll('.bslib-sidebar-layout').length, 'direct-child .sidebar count=', all.length);
  var listed = [];
  for (var i = 0; i < all.length; i++) {{
    var s = all[i];
    listed.push({{
      i: i,
      visible: _visibleEl(s),
      classes: s.className,
      id: s.id || '',
      layout: s.parentElement && s.parentElement.className
    }});
  }}
  console.log(DBG, 'getActiveSidebar: candidates', listed);
  for (var j = 0; j < all.length; j++) {{
    if (_visibleEl(all[j])) {{
      console.log(DBG, 'getActiveSidebar: fallback first visible in document', all[j].className);
      return all[j];
    }}
  }}
  console.log(DBG, 'getActiveSidebar: no sidebar resolved');
  return null;
}}

/** @returns {{ assigned: Element|null, previousIdsCleared: number, pickVisible: boolean }} */
function syncDrawerSidebarId() {{
  var prev = document.querySelectorAll('#rsi-drawer');
  var prevN = prev.length;
  prev.forEach(function(el) {{ el.removeAttribute('id'); }});
  var active = getActiveSidebar();
  if (active) active.id = 'rsi-drawer';
  var assigned = document.getElementById('rsi-drawer');
  var out = {{ assigned: assigned || null, previousIdsCleared: prevN, pickVisible: !!(active && _visibleEl(active)) }};
  console.log(DBG, 'syncDrawerSidebarId', out, assigned ? {{ tag: assigned.tagName, classes: assigned.className, visible: _visibleEl(assigned) }} : null);
  return out;
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
  var sync = syncDrawerSidebarId();
  var el = sync.assigned;
  if (!el) {{
    console.warn(DBG, 'toggleDrawer: abort — no #rsi-drawer assigned after sync');
    return;
  }}
  if (!_visibleEl(el)) {{
    console.warn(DBG, 'toggleDrawer: assigned sidebar is not visible (check tab/bslib DOM)', el);
  }}
  var on = document.body.classList.toggle('rsi-drawer-open');
  console.log(DBG, 'toggleDrawer: body.rsi-drawer-open=', on, 'drawerEl=', el, 'computedTransform=', window.getComputedStyle(el).transform);
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
