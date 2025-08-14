import asyncio
import mcp
from mcp.client.streamable_http import streamablehttp_client
import traceback

# The web interface URL you provided
WEB_INTERFACE_URL = "https://smithery.ai/server/@Jeetanshu18/tavily-mcp?code=ef8f4049-0048-42b5-95b9-209a812c3e6c"

# Try different MCP URLs based on the web interface
TAVILY_URLS = [
    # Original URL
    "https://server.smithery.ai/@Jeetanshu18/tavily-mcp/mcp?api_key=f1f6c5a8-b3d0-4815-81c3-8fa253314e6b&profile=cautious-peafowl-9gzmmK",
    
    # Try with the code from web interface
    "https://server.smithery.ai/@Jeetanshu18/tavily-mcp/mcp?code=ef8f4049-0048-42b5-95b9-209a812c3e6c",
    
    # Try combining both
    "https://server.smithery.ai/@Jeetanshu18/tavily-mcp/mcp?api_key=f1f6c5a8-b3d0-4815-81c3-8fa253314e6b&code=ef8f4049-0048-42b5-95b9-209a812c3e6c",
    
    # Try without profile
    "https://server.smithery.ai/@Jeetanshu18/tavily-mcp/mcp?api_key=f1f6c5a8-b3d0-4815-81c3-8fa253314e6b&code=ef8f4049-0048-42b5-95b9-209a812c3e6c&profile=cautious-peafowl-9gzmmK"
]

async def test_smithery_web_interface():
    print(f"Testing based on Smithery.ai web interface: {WEB_INTERFACE_URL}")
    
    for i, url in enumerate(TAVILY_URLS):
        print(f"\n=== Testing URL {i+1}: {url} ===")
        try:
            async with streamablehttp_client(url) as (read_stream, write_stream, _):
                async with mcp.ClientSession(read_stream, write_stream) as session:
                    await session.initialize()
                    tools_result = await session.list_tools()
                    print(f"✅ Available tools: {[t.name for t in tools_result.tools]}")
                    
                    # Try the exact query you tested: "what is capital of gujrat?"
                    search_args = {"query": "what is capital of gujrat?"}
                    print(f"Trying query: {search_args}")
                    
                    try:
                        result = await session.call_tool("tavily-search", search_args)
                        print(f"✅ SUCCESS! Result: {result}")
                        if hasattr(result, 'content') and result.content:
                            for part in result.content:
                                if hasattr(part, 'text') and part.text:
                                    print(f"Content: {part.text}")
                                    # Try to parse as JSON
                                    try:
                                        import json
                                        data = json.loads(part.text)
                                        print(f"Parsed JSON keys: {list(data.keys()) if isinstance(data, dict) else 'Not a dict'}")
                                    except:
                                        print("Content is not JSON format")
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
    success = asyncio.run(test_smithery_web_interface())
    if success:
        print("\n🎉 Tavily search is working!")
    else:
        print("\n❌ All URLs failed")
        print("\n💡 The web interface might be using a different authentication method.")

