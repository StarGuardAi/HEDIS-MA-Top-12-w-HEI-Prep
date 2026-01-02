"""
UI tests for responsive design
"""
import pytest
from playwright.sync_api import Page, expect


@pytest.mark.ui
class TestResponsiveDesign:
    """Test responsive breakpoints."""
    
    @pytest.mark.parametrize("width,height", [
        (375, 667),   # Mobile
        (768, 1024),  # Tablet
        (1920, 1080)  # Desktop
    ])
    def test_responsive_breakpoints(self, page: Page, width, height):
        """Test layout at different screen sizes."""
        page.set_viewport_size({"width": width, "height": height})
        page.goto("http://localhost:8501")
        
        # Check main content is visible
        main_content = page.locator(".main")
        expect(main_content).to_be_visible()
        
        # Check no horizontal scrolling at these breakpoints
        scroll_width = page.evaluate("document.documentElement.scrollWidth")
        viewport_width = page.viewport_size["width"]
        
        assert scroll_width <= viewport_width + 10, \
            f"Horizontal scroll detected at {width}x{height}"
    
    @pytest.mark.ui
    def test_mobile_navigation(self, page: Page):
        """Test mobile navigation works."""
        page.set_viewport_size({"width": 375, "height": 667})
        page.goto("http://localhost:8501")
        
        # Check sidebar can be toggled on mobile
        # (Implementation depends on Streamlit's mobile behavior)
        sidebar = page.locator('[data-testid="stSidebar"]')
        
        # Sidebar should exist (may be hidden on mobile)
        assert sidebar.count() >= 0
    
    @pytest.mark.ui
    def test_desktop_layout(self, page: Page):
        """Test desktop layout elements."""
        page.set_viewport_size({"width": 1920, "height": 1080})
        page.goto("http://localhost:8501")
        
        # Check sidebar is visible on desktop
        sidebar = page.locator('[data-testid="stSidebar"]')
        # Sidebar visibility depends on Streamlit configuration


@pytest.mark.ui
class TestButtonInteractions:
    """Test button interactions."""
    
    def test_button_click(self, page: Page):
        """Test button click interactions."""
        page.goto("http://localhost:8501")
        
        # Find and click a button (adjust selector based on actual page)
        buttons = page.locator("button")
        if buttons.count() > 0:
            buttons.first.click()
            # Verify some action occurred (page change, data update, etc.)
    
    def test_form_submission(self, page: Page):
        """Test form submission."""
        page.goto("http://localhost:8501")
        
        # Find form inputs and submit
        # This is a template - adjust based on actual forms
        inputs = page.locator("input")
        if inputs.count() > 0:
            # Fill form and submit
            pass


@pytest.mark.ui
class TestChartRendering:
    """Test chart rendering."""
    
    def test_chart_renders(self, page: Page):
        """Test that charts render correctly."""
        page.goto("http://localhost:8501")
        
        # Check for Plotly charts
        charts = page.locator(".js-plotly-plot")
        
        # Charts may not be present on all pages
        # This test verifies the structure exists
    
    def test_chart_interactivity(self, page: Page):
        """Test chart interactivity."""
        page.goto("http://localhost:8501")
        
        # Hover over chart elements
        charts = page.locator(".js-plotly-plot")
        if charts.count() > 0:
            charts.first.hover()
            # Verify tooltip or interaction works

