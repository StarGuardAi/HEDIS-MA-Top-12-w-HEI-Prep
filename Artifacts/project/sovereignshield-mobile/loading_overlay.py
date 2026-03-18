"""
Loading overlay for Shiny apps — branded cold-start / heavy-computation feedback.
Shows a pulsing message and progress bar. Uses shiny:idle for page_fillable apps to avoid blank flash.
"""
from shiny import ui


def loading_overlay_css() -> ui.HTML:
    """CSS for the loading overlay. Add to ui.tags.head() or ui.head_content()."""
    return ui.HTML("""
<style id="loading-overlay-styles">
#loading-overlay {
    position: fixed; top: 0; left: 0; right: 0; bottom: 0;
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    display: flex; align-items: center; justify-content: center;
    z-index: 99999; transition: opacity 0.4s ease-out;
}
#loading-overlay.dismissed { opacity: 0; pointer-events: none; }
#loading-overlay .overlay-inner {
    text-align: center; color: #fff; padding: 2rem; max-width: 400px;
}
#loading-overlay .overlay-inner h2 {
    font-size: 1.5rem; font-weight: 600; margin-bottom: 0.5rem; letter-spacing: -0.02em;
}
#loading-overlay .overlay-inner .tagline {
    font-size: 0.95rem; opacity: 0.9; margin-bottom: 1.5rem; animation: pulse 1.8s ease-in-out infinite;
}
@keyframes pulse { 0%, 100% { opacity: 0.85; } 50% { opacity: 1; } }
#loading-overlay .progress-track {
    height: 4px; background: rgba(255,255,255,0.2); border-radius: 2px; overflow: hidden;
}
#loading-overlay .progress-fill {
    height: 100%; width: 0%; background: #40B5AD; border-radius: 2px;
    transition: width 0.35s ease-out;
}
#loading-overlay .progress-fill.complete { width: 100%; }
</style>
""")


def loading_overlay_ui(app_name: str, tagline: str) -> ui.Tag:
    """Overlay UI — shows branded message, auto-dismisses on shiny:connected."""
    return ui.div(
        ui.div(
            ui.h2(app_name),
            ui.p(tagline, class_="tagline"),
            ui.div(
                ui.div(class_="progress-fill", id_="loading-progress-fill"),
                class_="progress-track",
            ),
            class_="overlay-inner",
        ),
        id="loading-overlay",
        ui.HTML("""
<script>
(function() {
    var overlay = document.getElementById('loading-overlay');
    var fill = document.getElementById('loading-progress-fill');
    if (!overlay) return;
    function dismiss() {
        if (fill) fill.classList.add('complete');
        setTimeout(function() {
            overlay.classList.add('dismissed');
            setTimeout(function() {
                overlay.remove();
                var styles = document.getElementById('loading-overlay-styles');
                if (styles) styles.remove();
            }, 450);
        }, 350);
    }
    document.addEventListener('shiny:connected', dismiss);
    document.addEventListener('shiny:sessioninitialized', dismiss);
    document.addEventListener('shiny:idle', dismiss);
    if (typeof Shiny !== 'undefined' && Shiny.addCustomMessageHandler) {
        try {
            Shiny.addCustomMessageHandler('loading_overlay_dismiss', dismiss);
        } catch(e) {}
    }
    setTimeout(dismiss, 6000);
})();
</script>
"""),
    )


def loading_overlay_ui_fillable(app_name: str, tagline: str) -> ui.Tag:
    """
    Overlay for page_fillable — dismisses on shiny:idle (after first render).
    Prevents blank-content flash on cold start; use instead of loading_overlay_ui for fillable layouts.
    """
    return ui.div(
        ui.div(
            ui.h2(app_name),
            ui.p(tagline, class_="tagline"),
            ui.div(
                ui.div(class_="progress-fill", id_="loading-progress-fill-fillable"),
                class_="progress-track",
            ),
            class_="overlay-inner",
        ),
        id="loading-overlay",
        ui.HTML("""
<script>
(function() {
    var overlay = document.getElementById('loading-overlay');
    var fill = document.getElementById('loading-progress-fill-fillable');
    if (!overlay) return;
    function dismiss() {
        if (fill) fill.classList.add('complete');
        setTimeout(function() {
            overlay.classList.add('dismissed');
            setTimeout(function() {
                overlay.style.visibility = 'hidden';
                overlay.style.display = 'none';
                overlay.remove();
                var styles = document.getElementById('loading-overlay-styles');
                if (styles) styles.remove();
            }, 450);
        }, 350);
    }
    document.addEventListener('shiny:idle', dismiss);
    document.addEventListener('shiny:connected', dismiss);
    document.addEventListener('shiny:sessioninitialized', dismiss);
    if (typeof Shiny !== 'undefined' && Shiny.addCustomMessageHandler) {
        try { Shiny.addCustomMessageHandler('loading_overlay_dismiss', dismiss); } catch(e) {}
    }
    setTimeout(dismiss, 6000);
})();
</script>
"""),
    )
