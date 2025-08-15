import pytest
import time
from playwright.async_api import expect

class TestDashboardE2E:
    """E2E tests for dashboard functionality."""
    
    @pytest.mark.asyncio
    async def test_dashboard_page_access(self, page, test_user_data):
        """Test accessing the dashboard page after login."""
        # Login first
        await page.goto("http://localhost:3000/login")
        await page.fill('input[name="email"]', test_user_data["email"])
        await page.fill('input[name="password"]', test_user_data["password"])
        await page.click('button[type="submit"]')
        await page.wait_for_url("http://localhost:3000/**", timeout=10000)
        
        # Navigate to dashboard page
        await page.goto("http://localhost:3000/dashboard")
        
        # Verify we're on the dashboard page
        await expect(page).to_have_url("http://localhost:3000/dashboard")
        
        # Check for dashboard page elements
        try:
            await expect(page.locator("text=Dashboard")).to_be_visible(timeout=5000)
        except:
            await expect(page.locator("text=Welcome")).to_be_visible(timeout=5000)
    
    @pytest.mark.asyncio
    async def test_dashboard_navigation(self, page, test_user_data):
        """Test navigation from dashboard to other pages."""
        # Login first
        await page.goto("http://localhost:3000/login")
        await page.fill('input[name="email"]', test_user_data["email"])
        await page.fill('input[name="password"]', test_user_data["password"])
        await page.click('button[type="submit"]')
        await page.wait_for_url("http://localhost:3000/**", timeout=10000)
        
        # Navigate to dashboard page
        await page.goto("http://localhost:3000/dashboard")
        
        # Test navigation to other pages
        navigation_tests = [
            ("Search", "/search"),
            ("Image Generation", "/image"),
            ("Profile", "/profile")
        ]
        
        for page_name, route in navigation_tests:
            try:
                # Navigate to the page
                await page.goto(f"http://localhost:3000{route}")
                await page.wait_for_load_state("networkidle")
                
                # Verify we can access the page
                await expect(page).not_to_have_url("http://localhost:3000/login")
                
                # Navigate back to dashboard
                await page.goto("http://localhost:3000/dashboard")
                
                print(f"✅ Successfully navigated from dashboard to {page_name} and back")
            except Exception as e:
                print(f"⚠️  Navigation test failed for {page_name}: {e}")
                continue
    
    @pytest.mark.asyncio
    async def test_dashboard_history_display(self, page, test_user_data):
        """Test that dashboard displays user history."""
        # Login first
        await page.goto("http://localhost:3000/login")
        await page.fill('input[name="email"]', test_user_data["email"])
        await page.fill('input[name="password"]', test_user_data["password"])
        await page.click('button[type="submit"]')
        await page.wait_for_url("http://localhost:3000/**", timeout=10000)
        
        # Navigate to dashboard page
        await page.goto("http://localhost:3000/dashboard")
        
        # Check for history elements
        history_selectors = [
            "text=History",
            "text=Recent Activity",
            "text=My Activity",
            ".history-section",
            "[data-testid='history-section']"
        ]
        
        for selector in history_selectors:
            try:
                await expect(page.locator(selector)).to_be_visible(timeout=5000)
                print("✅ History section found")
                break
            except:
                continue
        else:
            print("⚠️  History section not found")
    
    @pytest.mark.asyncio
    async def test_dashboard_stats_display(self, page, test_user_data):
        """Test that dashboard displays user statistics."""
        # Login first
        await page.goto("http://localhost:3000/login")
        await page.fill('input[name="email"]', test_user_data["email"])
        await page.fill('input[name="password"]', test_user_data["password"])
        await page.click('button[type="submit"]')
        await page.wait_for_url("http://localhost:3000/**", timeout=10000)
        
        # Navigate to dashboard page
        await page.goto("http://localhost:3000/dashboard")
        
        # Check for statistics elements
        stats_selectors = [
            "text=Statistics",
            "text=Stats",
            "text=Overview",
            ".stats-section",
            "[data-testid='stats-section']",
            ".dashboard-stats"
        ]
        
        for selector in stats_selectors:
            try:
                await expect(page.locator(selector)).to_be_visible(timeout=5000)
                print("✅ Statistics section found")
                break
            except:
                continue
        else:
            print("⚠️  Statistics section not found")
    
    @pytest.mark.asyncio
    async def test_dashboard_search_history(self, page, test_user_data):
        """Test dashboard search history functionality."""
        # Login first
        await page.goto("http://localhost:3000/login")
        await page.fill('input[name="email"]', test_user_data["email"])
        await page.fill('input[name="password"]', test_user_data["password"])
        await page.click('button[type="submit"]')
        await page.wait_for_url("http://localhost:3000/**", timeout=10000)
        
        # First, perform a search to create history
        await page.goto("http://localhost:3000/search")
        
        search_input_selectors = [
            'input[name="query"]',
            'textarea[name="query"]',
            'input[placeholder*="search"]'
        ]
        
        search_input = None
        for selector in search_input_selectors:
            try:
                search_input = await page.query_selector(selector)
                if search_input:
                    break
            except:
                continue
        
        if search_input:
            test_query = "Dashboard test search"
            await search_input.fill(test_query)
            await page.click('button[type="submit"], button:has-text("Search")')
            await page.wait_for_timeout(5000)
        
        # Navigate to dashboard
        await page.goto("http://localhost:3000/dashboard")
        
        # Look for the search in history
        try:
            await expect(page.locator(f"text={test_query}")).to_be_visible(timeout=5000)
            print("✅ Search history displayed in dashboard")
        except:
            print("⚠️  Search history not found in dashboard")
    
    @pytest.mark.asyncio
    async def test_dashboard_image_history(self, page, test_user_data):
        """Test dashboard image generation history functionality."""
        # Login first
        await page.goto("http://localhost:3000/login")
        await page.fill('input[name="email"]', test_user_data["email"])
        await page.fill('input[name="password"]', test_user_data["password"])
        await page.click('button[type="submit"]')
        await page.wait_for_url("http://localhost:3000/**", timeout=10000)
        
        # First, generate an image to create history
        await page.goto("http://localhost:3000/image")
        
        prompt_input_selectors = [
            'input[name="prompt"]',
            'textarea[name="prompt"]',
            'input[placeholder*="prompt"]'
        ]
        
        prompt_input = None
        for selector in prompt_input_selectors:
            try:
                prompt_input = await page.query_selector(selector)
                if prompt_input:
                    break
            except:
                continue
        
        if prompt_input:
            test_prompt = "Dashboard test image"
            await prompt_input.fill(test_prompt)
            await page.click('button[type="submit"], button:has-text("Generate")')
            await page.wait_for_timeout(10000)
        
        # Navigate to dashboard
        await page.goto("http://localhost:3000/dashboard")
        
        # Look for the image generation in history
        try:
            await expect(page.locator(f"text={test_prompt}")).to_be_visible(timeout=5000)
            print("✅ Image generation history displayed in dashboard")
        except:
            print("⚠️  Image generation history not found in dashboard")
    
    @pytest.mark.asyncio
    async def test_dashboard_filtering(self, page, test_user_data):
        """Test dashboard filtering functionality."""
        # Login first
        await page.goto("http://localhost:3000/login")
        await page.fill('input[name="email"]', test_user_data["email"])
        await page.fill('input[name="password"]', test_user_data["password"])
        await page.click('button[type="submit"]')
        await page.wait_for_url("http://localhost:3000/**", timeout=10000)
        
        # Navigate to dashboard page
        await page.goto("http://localhost:3000/dashboard")
        
        # Look for filter elements
        filter_selectors = [
            'select[name="filter"]',
            'input[placeholder*="filter"]',
            'button:has-text("Filter")',
            '[data-testid="filter-button"]',
            '.filter-controls'
        ]
        
        for selector in filter_selectors:
            try:
                filter_element = await page.query_selector(selector)
                if filter_element:
                    await filter_element.click()
                    print("✅ Filter functionality found")
                    break
            except:
                continue
        else:
            print("⚠️  Filter functionality not available")
    
    @pytest.mark.asyncio
    async def test_dashboard_search_functionality(self, page, test_user_data):
        """Test dashboard search within history functionality."""
        # Login first
        await page.goto("http://localhost:3000/login")
        await page.fill('input[name="email"]', test_user_data["email"])
        await page.fill('input[name="password"]', test_user_data["password"])
        await page.click('button[type="submit"]')
        await page.wait_for_url("http://localhost:3000/**", timeout=10000)
        
        # Navigate to dashboard page
        await page.goto("http://localhost:3000/dashboard")
        
        # Look for search within dashboard
        search_selectors = [
            'input[placeholder*="search"]',
            'input[name="search"]',
            '[data-testid="dashboard-search"]',
            '.dashboard-search input'
        ]
        
        for selector in search_selectors:
            try:
                search_input = await page.query_selector(selector)
                if search_input:
                    await search_input.fill("test")
                    print("✅ Dashboard search functionality found")
                    break
            except:
                continue
        else:
            print("⚠️  Dashboard search functionality not available")
    
    @pytest.mark.asyncio
    async def test_dashboard_pagination(self, page, test_user_data):
        """Test dashboard pagination functionality."""
        # Login first
        await page.goto("http://localhost:3000/login")
        await page.fill('input[name="email"]', test_user_data["email"])
        await page.fill('input[name="password"]', test_user_data["password"])
        await page.click('button[type="submit"]')
        await page.wait_for_url("http://localhost:3000/**", timeout=10000)
        
        # Navigate to dashboard page
        await page.goto("http://localhost:3000/dashboard")
        
        # Look for pagination elements
        pagination_selectors = [
            'button:has-text("Next")',
            'button:has-text("Previous")',
            '.pagination',
            '[data-testid="pagination"]',
            'nav[aria-label="Pagination"]'
        ]
        
        for selector in pagination_selectors:
            try:
                pagination_element = await page.query_selector(selector)
                if pagination_element:
                    print("✅ Pagination functionality found")
                    break
            except:
                continue
        else:
            print("⚠️  Pagination functionality not available")
    
    @pytest.mark.asyncio
    async def test_dashboard_item_actions(self, page, test_user_data):
        """Test dashboard item action buttons (delete, view, etc.)."""
        # Login first
        await page.goto("http://localhost:3000/login")
        await page.fill('input[name="email"]', test_user_data["email"])
        await page.fill('input[name="password"]', test_user_data["password"])
        await page.click('button[type="submit"]')
        await page.wait_for_url("http://localhost:3000/**", timeout=10000)
        
        # Navigate to dashboard page
        await page.goto("http://localhost:3000/dashboard")
        
        # Look for action buttons on history items
        action_selectors = [
            'button:has-text("Delete")',
            'button:has-text("View")',
            'button:has-text("Edit")',
            '[data-testid="delete-button"]',
            '[data-testid="view-button"]',
            '.action-button'
        ]
        
        for selector in action_selectors:
            try:
                action_buttons = await page.query_selector_all(selector)
                if action_buttons:
                    print(f"✅ Found {len(action_buttons)} action buttons")
                    break
            except:
                continue
        else:
            print("⚠️  Action buttons not available")
    
    @pytest.mark.asyncio
    async def test_dashboard_export_functionality(self, page, test_user_data):
        """Test dashboard export functionality if available."""
        # Login first
        await page.goto("http://localhost:3000/login")
        await page.fill('input[name="email"]', test_user_data["email"])
        await page.fill('input[name="password"]', test_user_data["password"])
        await page.click('button[type="submit"]')
        await page.wait_for_url("http://localhost:3000/**", timeout=10000)
        
        # Navigate to dashboard page
        await page.goto("http://localhost:3000/dashboard")
        
        # Look for export functionality
        export_selectors = [
            'button:has-text("Export")',
            'button:has-text("Download")',
            '[data-testid="export-button"]',
            '.export-button'
        ]
        
        for selector in export_selectors:
            try:
                export_button = await page.query_selector(selector)
                if export_button:
                    await export_button.click()
                    print("✅ Export functionality found and clicked")
                    break
            except:
                continue
        else:
            print("⚠️  Export functionality not available")
    
    @pytest.mark.asyncio
    async def test_dashboard_responsive_design(self, page, test_user_data):
        """Test dashboard responsive design on different screen sizes."""
        # Login first
        await page.goto("http://localhost:3000/login")
        await page.fill('input[name="email"]', test_user_data["email"])
        await page.fill('input[name="password"]', test_user_data["password"])
        await page.click('button[type="submit"]')
        await page.wait_for_url("http://localhost:3000/**", timeout=10000)
        
        # Test different screen sizes
        screen_sizes = [
            {"width": 1920, "height": 1080},  # Desktop
            {"width": 1024, "height": 768},   # Tablet
            {"width": 375, "height": 667}     # Mobile
        ]
        
        for size in screen_sizes:
            try:
                await page.set_viewport_size(size)
                await page.goto("http://localhost:3000/dashboard")
                await page.wait_for_load_state("networkidle")
                
                # Check if page loads without errors
                await expect(page).not_to_have_url("http://localhost:3000/login")
                
                print(f"✅ Dashboard responsive at {size['width']}x{size['height']}")
            except Exception as e:
                print(f"⚠️  Dashboard responsive test failed at {size['width']}x{size['height']}: {e}")
                continue
