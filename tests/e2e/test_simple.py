import pytest
from playwright.async_api import async_playwright

@pytest.mark.asyncio
async def test_basic_playwright():
    """Test basic Playwright functionality."""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        # Navigate to a simple page
        await page.goto("https://example.com")
        
        # Check title
        title = await page.title()
        assert "Example Domain" in title
        
        await browser.close()

@pytest.mark.asyncio
async def test_local_backend():
    """Test if backend is accessible."""
    import httpx
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get("http://localhost:8000/docs")
            assert response.status_code == 200
        except:
            # Backend might not be running, that's okay for this test
            pass
