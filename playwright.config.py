"""
Playwright Configuration for AI Content Explorer E2E Tests
=========================================================

This configuration file sets up Playwright for end-to-end testing
of the AI Content Explorer application.
"""

from playwright.sync_api import Playwright, sync_playwright, expect

def run(playwright: Playwright) -> None:
    """Run Playwright tests."""
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    
    # Test configuration
    page.goto("http://localhost:3000")
    page.wait_for_load_state("networkidle")
    
    # Close browser
    context.close()
    browser.close()

# Playwright configuration
PLAYWRIGHT_CONFIG = {
    "testDir": "tests/e2e",
    "timeout": 30000,
    "expect": {
        "timeout": 5000
    },
    "use": {
        "headless": False,
        "viewport": {
            "width": 1280,
            "height": 720
        },
        "ignore_https_errors": True,
        "video": "on-first-retry",
        "screenshot": "only-on-failure"
    },
    "projects": [
        {
            "name": "chromium",
            "use": {
                "browserName": "chromium"
            }
        },
        {
            "name": "firefox",
            "use": {
                "browserName": "firefox"
            }
        },
        {
            "name": "webkit",
            "use": {
                "browserName": "webkit"
            }
        }
    ],
    "reporter": [
        ["html", {"outputFolder": "reports/playwright"}],
        ["json", {"outputFile": "reports/playwright/results.json"}]
    ],
    "globalSetup": "tests/e2e/conftest.py",
    "globalTeardown": "tests/e2e/conftest.py"
}

if __name__ == "__main__":
    with sync_playwright() as playwright:
        run(playwright)
