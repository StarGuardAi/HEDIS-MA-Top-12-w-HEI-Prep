"""
StarGuard AI Mobile - Medicare Advantage Intelligence Platform
Main application entry point with hamburger menu sidebar navigation
"""

from shiny import App, ui, render
from .utils.theme_config import get_theme, get_mobile_css, get_mobile_meta
from .pages.star_predictor import star_predictor_ui, star_predictor_server
from .pages.hedis_analyzer import hedis_analyzer_ui, hedis_analyzer_server
from .pages.ai_validation import ai_validation_ui, ai_validation_server


def navigation_bar():
    """
    Create mobile-optimized navigation header with hamburger menu sidebar.

    Returns:
        Navigation UI component with header and sidebar
    """
    return ui.div(
        # Top header bar with branding
        ui.div(
            ui.div(
                ui.h1(
                    "StarGuard AI",
                    style="color: white; font-size: 1.5rem; margin: 0; font-weight: 700; letter-spacing: -0.5px;"
                ),
                ui.p(
                    "Medicare Advantage Intelligence",
                    style="color: rgba(255,255,255,0.85); font-size: 0.875rem; margin: 0.25rem 0 0 0; font-weight: 400;"
                ),
            ),
            class_="navbar"
        ),
        # Hamburger menu button (mobile only)
        ui.div(
            ui.div(
                ui.tags.span(),
                ui.tags.span(),
                ui.tags.span(),
                class_="hamburger-icon"
            ),
            id="menu-toggle",
            class_="menu-toggle",
            onclick="toggleSidebar()"
        ),
        # Sidebar overlay (darkens background when open)
        ui.div(
            id="sidebar-overlay",
            class_="sidebar-overlay",
            onclick="toggleSidebar()"
        ),
        # Sidebar navigation
        ui.div(
            ui.div(
                ui.tags.h2("Navigation"),
                ui.tags.p("Select a page"),
                class_="sidebar-header"
            ),
            ui.div(
                ui.div(
                    "⭐ Star Rating Predictor",
                    class_="sidebar-nav-item active",
                    id="nav-star",
                    onclick="navigateTo('star')"
                ),
                ui.div(
                    "📊 HEDIS Gap Analyzer",
                    class_="sidebar-nav-item",
                    id="nav-hedis",
                    onclick="navigateTo('hedis')"
                ),
                ui.div(
                    "🤖 AI Validation Dashboard",
                    class_="sidebar-nav-item",
                    id="nav-ai",
                    onclick="navigateTo('ai')"
                ),
                class_="sidebar-nav"
            ),
            ui.div(
                ui.tags.hr(style="margin: 1rem 1.5rem; border-color: #e0e0e0;"),
                ui.div(
                    ui.tags.small(
                        "StarGuard AI v1.0",
                        style="display: block; text-align: center; color: #999; font-size: 0.75rem;"
                    ),
                    style="padding: 0 1.5rem 1rem 1.5rem;"
                )
            ),
            id="nav-sidebar",
            class_="nav-sidebar"
        ),
        # Navigation tabs (desktop only - hidden on mobile)
        ui.div(
            ui.input_radio_buttons(
                "page_nav",
                "",
                choices={
                    "star": "⭐ Star Ratings",
                    "hedis": "📊 HEDIS Gaps",
                    "ai": "🤖 AI Validation"
                },
                selected="star",
                inline=True
            ),
            class_="nav-tabs-container"
        ),
        # JavaScript for sidebar functionality
        ui.tags.script("""
            function toggleSidebar() {
                const sidebar = document.getElementById('nav-sidebar');
                const overlay = document.getElementById('sidebar-overlay');
                const toggle = document.getElementById('menu-toggle');

                sidebar.classList.toggle('active');
                overlay.classList.toggle('active');
                toggle.classList.toggle('active');
            }

            function navigateTo(page) {
                if (typeof Shiny !== 'undefined') {
                    Shiny.setInputValue('page_nav', page);
                }
                document.querySelectorAll('.sidebar-nav-item').forEach(item => {
                    item.classList.remove('active');
                });
                const navEl = document.getElementById('nav-' + page);
                if (navEl) navEl.classList.add('active');
                toggleSidebar();
            }
        """)
    )


def footer():
    """Footer with contact info."""
    return ui.div(
        ui.tags.hr(style="margin: 2rem 0 1rem 0; border-color: #e0e0e0;"),
        ui.div(
            ui.markdown("""
            **StarGuard AI** | Built by Robert Reichert  
            [LinkedIn](https://linkedin.com/in/robert-reichert) | [Portfolio](https://tinyurl.com/bdevpdz5)
            """),
            style="text-align: center; padding: 1rem; color: #666; font-size: 0.875rem;"
        )
    )


# Placeholder page content until real pages are added
def placeholder_page(title, emoji):
    return ui.div(
        ui.div(title, class_="card-header"),
        ui.div(
            ui.p(f"{emoji} {title} - Page content will go here when implemented."),
            class_="card-body"
        ),
        class_="card"
    )


app_ui = ui.page_fluid(
    ui.tags.head(
        ui.HTML(get_mobile_meta()),
        ui.HTML(get_mobile_css())
    ),
    navigation_bar(),
    ui.output_ui("page_content"),
    footer(),
    theme=get_theme(),
    title="StarGuard AI - Medicare Advantage Intelligence"
)


def server(input, output, session):
    get_page = lambda: input.page_nav()
    star_predictor_server(input, output, session, get_current_page=get_page)
    hedis_analyzer_server(input, output, session, get_current_page=get_page)
    ai_validation_server(input, output, session, get_current_page=get_page)

    @output
    @render.ui
    def page_content():
        page = input.page_nav()
        if page == "star":
            return ui.div(star_predictor_ui(), id="star-predictor-page")
        elif page == "hedis":
            return ui.div(hedis_analyzer_ui(), id="hedis-analyzer-page")
        elif page == "ai":
            return ui.div(ai_validation_ui(), id="ai-validation-page")
        return ui.div(star_predictor_ui(), id="star-predictor-page")


app = App(app_ui, server)
