import asyncio
from app.services.mcp_gateway import call_tavily_search, call_flux_generate_image_url

async def test_search():
    print("Testing Tavily search...")
    try:
        result = await call_tavily_search("Where is Taj Mahal located?")
        print(f"Search result: {result}")
        return True
    except Exception as e:
        print(f"Search failed: {e}")
        return False

async def test_image():
    print("\nTesting Flux image generation...")
    try:
        result = await call_flux_generate_image_url("a beautiful sunset")
        print(f"Image result: {result}")
        return True
    except Exception as e:
        print(f"Image generation failed: {e}")
        return False

async def main():
    print("Testing MCP Gateway...")
    
    search_ok = await test_search()
    image_ok = await test_image()
    
    if search_ok and image_ok:
        print("\n✅ All tests passed!")
    else:
        print("\n❌ Some tests failed!")

if __name__ == "__main__":
    asyncio.run(main())
