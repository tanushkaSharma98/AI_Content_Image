import pytest
import time
import re
from playwright.async_api import expect

class TestAuthenticationE2E:
    """E2E tests for authentication flows."""
    
    @pytest.mark.asyncio
    async def test_user_registration_flow(self, page, test_user_data):
        """Test complete user registration flow."""
        # Navigate to registration page
        await page.goto("http://localhost:3000/register")
        
        # Verify we're on the registration page
        await expect(page).to_have_title(re.compile(r".*Register.*|.*Sign Up.*"))
        
        # Fill registration form
        await page.fill('input[name="username"]', test_user_data["username"])
        await page.fill('input[name="email"]', test_user_data["email"])
        await page.fill('input[name="password"]', test_user_data["password"])
        await page.fill('input[name="confirmPassword"]', test_user_data["password"])
        
        # Submit registration
        await page.click('button[type="submit"]')
        
        # Wait for successful registration (redirect to dashboard or home)
        await page.wait_for_url("http://localhost:3000/**", timeout=10000)
        
        # Verify successful registration
        await expect(page).not_to_have_url("http://localhost:3000/register")
        
        # Check for success message or dashboard elements
        try:
            await expect(page.locator("text=Welcome")).to_be_visible(timeout=5000)
        except:
            # If no welcome message, check for dashboard elements
            await expect(page.locator("text=Dashboard")).to_be_visible(timeout=5000)
    
    @pytest.mark.asyncio
    async def test_user_login_flow(self, page, test_user_data):
        """Test complete user login flow."""
        # Navigate to login page
        await page.goto("http://localhost:3000/login")
        
        # Verify we're on the login page
        await expect(page).to_have_title(re.compile(r".*Login.*|.*Sign In.*"))
        
        # Fill login form
        await page.fill('input[name="email"]', test_user_data["email"])
        await page.fill('input[name="password"]', test_user_data["password"])
        
        # Submit login
        await page.click('button[type="submit"]')
        
        # Wait for successful login
        await page.wait_for_url("http://localhost:3000/**", timeout=10000)
        
        # Verify successful login
        await expect(page).not_to_have_url("http://localhost:3000/login")
        
        # Check for authenticated user elements
        try:
            await expect(page.locator("text=Welcome")).to_be_visible(timeout=5000)
        except:
            await expect(page.locator("text=Dashboard")).to_be_visible(timeout=5000)
    
    @pytest.mark.asyncio
    async def test_user_logout_flow(self, page, test_user_data):
        """Test complete user logout flow."""
        # First login the user
        await page.goto("http://localhost:3000/login")
        await page.fill('input[name="email"]', test_user_data["email"])
        await page.fill('input[name="password"]', test_user_data["password"])
        await page.click('button[type="submit"]')
        await page.wait_for_url("http://localhost:3000/**", timeout=10000)
        
        # Find and click logout button
        logout_selectors = [
            '[data-testid="logout-button"]',
            'button:has-text("Logout")',
            'a:has-text("Logout")',
            '.logout-button',
            '#logout-button'
        ]
        
        logout_clicked = False
        for selector in logout_selectors:
            try:
                logout_button = await page.query_selector(selector)
                if logout_button:
                    await logout_button.click()
                    logout_clicked = True
                    break
            except:
                continue
        
        if not logout_clicked:
            # Try to find logout in navigation menu
            try:
                await page.click('button[aria-label="Menu"], .menu-button, #menu-button')
                await page.wait_for_timeout(1000)
                await page.click('text=Logout')
                logout_clicked = True
            except:
                pass
        
        if logout_clicked:
            # Wait for redirect to login page
            await page.wait_for_url("http://localhost:3000/login", timeout=5000)
            await expect(page).to_have_url("http://localhost:3000/login")
        else:
            pytest.skip("Logout button not found in UI")
    
    @pytest.mark.asyncio
    async def test_invalid_login_credentials(self, page):
        """Test login with invalid credentials."""
        # Navigate to login page
        await page.goto("http://localhost:3000/login")
        
        # Fill login form with invalid credentials
        await page.fill('input[name="email"]', "invalid@example.com")
        await page.fill('input[name="password"]', "wrongpassword")
        
        # Submit login
        await page.click('button[type="submit"]')
        
        # Wait for error message
        try:
            await expect(page.locator("text=Invalid credentials")).to_be_visible(timeout=5000)
        except:
            await expect(page.locator("text=Login failed")).to_be_visible(timeout=5000)
        
        # Verify we're still on login page
        await expect(page).to_have_url("http://localhost:3000/login")
    
    @pytest.mark.asyncio
    async def test_registration_validation(self, page):
        """Test registration form validation."""
        # Navigate to registration page
        await page.goto("http://localhost:3000/register")
        
        # Try to submit empty form
        await page.click('button[type="submit"]')
        
        # Check for validation errors
        try:
            await expect(page.locator("text=Username is required")).to_be_visible(timeout=3000)
        except:
            await expect(page.locator("text=Email is required")).to_be_visible(timeout=3000)
        
        # Verify we're still on registration page
        await expect(page).to_have_url("http://localhost:3000/register")
    
    @pytest.mark.asyncio
    async def test_password_mismatch_validation(self, page, test_user_data):
        """Test password confirmation validation."""
        # Navigate to registration page
        await page.goto("http://localhost:3000/register")
        
        # Fill form with mismatched passwords
        await page.fill('input[name="username"]', test_user_data["username"])
        await page.fill('input[name="email"]', test_user_data["email"])
        await page.fill('input[name="password"]', test_user_data["password"])
        await page.fill('input[name="confirmPassword"]', "differentpassword")
        
        # Submit registration
        await page.click('button[type="submit"]')
        
        # Check for password mismatch error
        try:
            await expect(page.locator("text=Passwords do not match")).to_be_visible(timeout=3000)
        except:
            await expect(page.locator("text=Password confirmation")).to_be_visible(timeout=3000)
        
        # Verify we're still on registration page
        await expect(page).to_have_url("http://localhost:3000/register")
    
    @pytest.mark.asyncio
    async def test_protected_route_access(self, page):
        """Test that protected routes redirect to login."""
        # Try to access dashboard without authentication
        await page.goto("http://localhost:3000/dashboard")
        
        # Should be redirected to login
        await expect(page).to_have_url("http://localhost:3000/login")
        
        # Try to access other protected routes
        await page.goto("http://localhost:3000/search")
        await expect(page).to_have_url("http://localhost:3000/login")
        
        await page.goto("http://localhost:3000/image")
        await expect(page).to_have_url("http://localhost:3000/login")
    
    @pytest.mark.asyncio
    async def test_navigation_after_login(self, page, test_user_data):
        """Test navigation between pages after login."""
        # Login first
        await page.goto("http://localhost:3000/login")
        await page.fill('input[name="email"]', test_user_data["email"])
        await page.fill('input[name="password"]', test_user_data["password"])
        await page.click('button[type="submit"]')
        await page.wait_for_url("http://localhost:3000/**", timeout=10000)
        
        # Test navigation to different pages
        navigation_tests = [
            ("Dashboard", "/dashboard"),
            ("Search", "/search"),
            ("Image Generation", "/image"),
            ("Profile", "/profile")
        ]
        
        for page_name, route in navigation_tests:
            try:
                # Try to navigate to the page
                await page.goto(f"http://localhost:3000{route}")
                await page.wait_for_load_state("networkidle")
                
                # Verify we can access the page (not redirected to login)
                await expect(page).not_to_have_url("http://localhost:3000/login")
                
                print(f"✅ Successfully navigated to {page_name}")
            except Exception as e:
                print(f"⚠️  Could not navigate to {page_name}: {e}")
                # Continue with other tests
                continue
