import asyncio
import mcp
from mcp.client.streamable_http import streamablehttp_client
import traceback

# Try different authentication approaches
TAVILY_BASE_URL = "https://server.smithery.ai/@Jeetanshu18/tavily-mcp/mcp"
API_KEY = "f1f6c5a8-b3d0-4815-81c3-8fa253314e6b"
PROFILE = "cautious-peafowl-9gzmmK"

# Different URL combinations
TAVILY_URLS = [
    f"{TAVILY_BASE_URL}?api_key={API_KEY}&profile={PROFILE}",
    f"{TAVILY_BASE_URL}?api_key={API_KEY}",
    f"{TAVILY_BASE_URL}?profile={PROFILE}&api_key={API_KEY}",
    f"{TAVILY_BASE_URL}?key={API_KEY}&profile={PROFILE}",
    f"{TAVILY_BASE_URL}?token={API_KEY}&profile={PROFILE}",
    f"{TAVILY_BASE_URL}?auth={API_KEY}&profile={PROFILE}"
]

async def test_tavily_auth():
    for i, url in enumerate(TAVILY_URLS):
        print(f"\n=== Testing URL {i+1}: {url} ===")
        try:
            async with streamablehttp_client(url) as (read_stream, write_stream, _):
                async with mcp.ClientSession(read_stream, write_stream) as session:
                    await session.initialize()
                    tools_result = await session.list_tools()
                    print(f"✅ Available tools: {[t.name for t in tools_result.tools]}")
                    
                    # Try the simplest possible call
                    try:
                        result = await session.call_tool("tavily-search", {"query": "test"})
                        print(f"✅ SUCCESS! Result: {result}")
                        if hasattr(result, 'content') and result.content:
                            for part in result.content:
                                if hasattr(part, 'text') and part.text:
                                    print(f"Content: {part.text[:200]}...")
                        return True
                    except Exception as e:
                        print(f"❌ Failed: {e}")
                        if "Invalid API key" in str(e):
                            print(f"❌ API key issue with URL {i+1}")
                        continue
                        
        except Exception as e:
            print(f"❌ Connection error: {e}")
            continue
    
    return False

if __name__ == "__main__":
    success = asyncio.run(test_tavily_auth())
    if success:
        print("\n🎉 Tavily search is working!")
    else:
        print("\n❌ All authentication methods failed")
        print("\n💡 Suggestion: Please check if you have a different API key or if the server requires different authentication.")

