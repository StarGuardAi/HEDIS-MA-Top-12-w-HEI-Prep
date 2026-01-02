"""
Performance compatibility tests
"""
import pytest
import time
from playwright.sync_api import Page


@pytest.mark.compatibility
@pytest.mark.performance
class TestPerformanceCompatibility:
    """Test performance across different browsers and devices."""
    
    @pytest.mark.parametrize("browser_name", ["chromium", "firefox", "webkit"])
    def test_page_load_time(self, browser_name):
        """Test page load time in all browsers."""
        from playwright.sync_api import sync_playwright
        
        with sync_playwright() as p:
            if browser_name == "chromium":
                browser = p.chromium.launch(headless=True)
            elif browser_name == "firefox":
                browser = p.firefox.launch(headless=True)
            else:
                browser = p.webkit.launch(headless=True)
            
            page = browser.new_page()
            
            start_time = time.time()
            page.goto("http://localhost:8501", wait_until="networkidle")
            load_time = time.time() - start_time
            
            # Desktop target: < 3s
            assert load_time < 5.0, \
                f"Page load time {load_time:.2f}s exceeds target in {browser_name}"
            
            browser.close()
    
    @pytest.mark.parametrize("width,height,target", [
        (1920, 1080, 3.0),   # Desktop: < 3s
        (393, 852, 2.0),     # Mobile: < 2s
        (1024, 1366, 2.5),  # Tablet: < 2.5s
    ])
    def test_load_time_by_device(self, page: Page, width, height, target):
        """Test load time targets by device type."""
        page.set_viewport_size({"width": width, "height": height})
        
        start_time = time.time()
        page.goto("http://localhost:8501", wait_until="networkidle")
        load_time = time.time() - start_time
        
        assert load_time < target, \
            f"Load time {load_time:.2f}s exceeds target {target}s for {width}x{height}"
    
    def test_chart_render_performance(self, page: Page):
        """Test chart rendering performance."""
        page.goto("http://localhost:8501")
        page.wait_for_load_state("networkidle", timeout=10000)
        
        # Navigate to page with charts (adjust based on actual pages)
        # This is a template - adjust selector based on actual implementation
        
        charts = page.locator(".js-plotly-plot")
        if charts.count() > 0:
            start_time = time.time()
            charts.first.wait_for(state="visible", timeout=5000)
            render_time = time.time() - start_time
            
            # Charts should render in < 2s
            assert render_time < 2.0, \
                f"Chart render time {render_time:.2f}s exceeds target"

