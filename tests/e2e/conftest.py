import pytest
import asyncio
import subprocess
import time
import os
from playwright.async_api import async_playwright
from typing import AsyncGenerator

# Test configuration
BACKEND_URL = "http://localhost:8000"
FRONTEND_URL = "http://localhost:3000"

class TestConfig:
    """Configuration for E2E tests."""
    BACKEND_URL = BACKEND_URL
    FRONTEND_URL = FRONTEND_URL
    TEST_USER_EMAIL = "e2e-test@example.com"
    TEST_USER_PASSWORD = "testpassword123"
    TEST_USER_USERNAME = "e2e_test_user"

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
async def backend_server():
    """Start the backend server for E2E tests."""
    print("🚀 Starting backend server for E2E tests...")
    
    # Start the backend server
    process = subprocess.Popen([
        os.path.join(".venv", "Scripts", "python.exe"),
        "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # Wait for server to start
    time.sleep(5)
    
    yield process
    
    # Cleanup
    print("🛑 Stopping backend server...")
    process.terminate()
    process.wait()

@pytest.fixture(scope="session")
async def frontend_server():
    """Start the frontend server for E2E tests."""
    print("🚀 Starting frontend server for E2E tests...")
    
    # Navigate to frontend directory
    frontend_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "auth-ui")
    
    if os.path.exists(frontend_dir):
        # Start the frontend server
        process = subprocess.Popen([
            "npm", "start"
        ], cwd=frontend_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait for server to start
        time.sleep(10)
        
        yield process
        
        # Cleanup
        print("🛑 Stopping frontend server...")
        process.terminate()
        process.wait()
    else:
        print("⚠️  Frontend directory not found, skipping frontend tests")
        yield None

@pytest.fixture
async def browser():
    """Create a browser instance for E2E tests."""
    async with async_playwright() as p:
        # Launch browser in headless mode for CI, headed for local development
        headless = os.getenv("CI", "false").lower() == "true"
        
        browser = await p.chromium.launch(
            headless=headless,
            args=["--no-sandbox", "--disable-setuid-sandbox"]
        )
        yield browser
        await browser.close()

@pytest.fixture
async def page(browser):
    """Create a new page for E2E tests."""
    page = await browser.new_page()
    
    # Set viewport size
    await page.set_viewport_size({"width": 1280, "height": 720})
    
    # Add test utilities
    await page.add_init_script("""
        window.testUtils = {
            waitForElement: async (selector, timeout = 5000) => {
                const start = Date.now();
                while (Date.now() - start < timeout) {
                    const element = document.querySelector(selector);
                    if (element) return element;
                    await new Promise(resolve => setTimeout(resolve, 100));
                }
                throw new Error(`Element ${selector} not found within ${timeout}ms`);
            },
            waitForText: async (text, timeout = 5000) => {
                const start = Date.now();
                while (Date.now() - start < timeout) {
                    const element = document.evaluate(
                        `//*[contains(text(), '${text}')]`,
                        document,
                        null,
                        XPathResult.FIRST_ORDERED_NODE_TYPE,
                        null
                    ).singleNodeValue;
                    if (element) return element;
                    await new Promise(resolve => setTimeout(resolve, 100));
                }
                throw new Error(`Text "${text}" not found within ${timeout}ms`);
            }
        };
    """)
    
    yield page
    await page.close()

@pytest.fixture
async def authenticated_page(page):
    """Create a page with authenticated user for E2E tests."""
    # Navigate to login page
    await page.goto(f"{TestConfig.FRONTEND_URL}/login")
    
    # Fill login form
    await page.fill('input[name="email"]', TestConfig.TEST_USER_EMAIL)
    await page.fill('input[name="password"]', TestConfig.TEST_USER_PASSWORD)
    
    # Click login button
    await page.click('button[type="submit"]')
    
    # Wait for successful login (redirect to dashboard or home)
    await page.wait_for_url(f"{TestConfig.FRONTEND_URL}/**", timeout=10000)
    
    yield page

@pytest.fixture
async def test_user_data():
    """Test user data for E2E tests."""
    return {
        "email": TestConfig.TEST_USER_EMAIL,
        "username": TestConfig.TEST_USER_USERNAME,
        "password": TestConfig.TEST_USER_PASSWORD
    }

# Helper functions for E2E tests
async def create_test_user(page, user_data):
    """Create a test user for E2E tests."""
    # Navigate to registration page
    await page.goto(f"{TestConfig.FRONTEND_URL}/register")
    
    # Fill registration form
    await page.fill('input[name="username"]', user_data["username"])
    await page.fill('input[name="email"]', user_data["email"])
    await page.fill('input[name="password"]', user_data["password"])
    await page.fill('input[name="confirmPassword"]', user_data["password"])
    
    # Submit registration
    await page.click('button[type="submit"]')
    
    # Wait for successful registration
    await page.wait_for_url(f"{TestConfig.FRONTEND_URL}/**", timeout=10000)

async def login_user(page, user_data):
    """Login a user for E2E tests."""
    # Navigate to login page
    await page.goto(f"{TestConfig.FRONTEND_URL}/login")
    
    # Fill login form
    await page.fill('input[name="email"]', user_data["email"])
    await page.fill('input[name="password"]', user_data["password"])
    
    # Submit login
    await page.click('button[type="submit"]')
    
    # Wait for successful login
    await page.wait_for_url(f"{TestConfig.FRONTEND_URL}/**", timeout=10000)

async def logout_user(page):
    """Logout a user for E2E tests."""
    # Find and click logout button
    logout_button = await page.query_selector('[data-testid="logout-button"], button:has-text("Logout")')
    if logout_button:
        await logout_button.click()
        await page.wait_for_url(f"{TestConfig.FRONTEND_URL}/login", timeout=5000)
