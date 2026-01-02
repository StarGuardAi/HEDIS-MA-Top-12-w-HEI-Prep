"""
UI test fixtures for Playwright
"""
import pytest
from playwright.sync_api import sync_playwright, Page, Browser


@pytest.fixture(scope="session")
def browser():
    """Create browser instance for UI tests."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        yield browser
        browser.close()


@pytest.fixture
def page(browser: Browser):
    """Create page instance for UI tests."""
    page = browser.new_page()
    yield page
    page.close()

