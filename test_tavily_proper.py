import asyncio
import mcp
from mcp.client.streamable_http import streamablehttp_client
import traceback

TAVILY_MCP_URL = "https://server.smithery.ai/@Jeetanshu18/tavily-mcp/mcp?api_key=f1f6c5a8-b3d0-4815-81c3-8fa253314e6b&profile=cautious-peafowl-9gzmmK"

async def test_tavily_proper():
    print("Testing Tavily MCP with proper parameters...")
    try:
        async with streamablehttp_client(TAVILY_MCP_URL) as (read_stream, write_stream, _):
            async with mcp.ClientSession(read_stream, write_stream) as session:
                await session.initialize()
                tools_result = await session.list_tools()
                print(f"Available tools: {[t.name for t in tools_result.tools]}")
                
                # Test with proper parameters from documentation
                search_args = {
                    "query": "What is quantum computing?",
                    "search_depth": "basic",
                    "max_results": 3,
                    "include_raw_content": True,
                    "topic": "general"
                }
                
                print(f"Calling tavily-search with args: {search_args}")
                result = await session.call_tool("tavily-search", search_args)
                print(f"SUCCESS! Result: {result}")
                
                if hasattr(result, 'content') and result.content:
                    for part in result.content:
                        if hasattr(part, 'text') and part.text:
                            print(f"Content: {part.text[:500]}...")
                            # Try to parse as JSON to see the structure
                            try:
                                import json
                                data = json.loads(part.text)
                                print(f"Parsed JSON structure: {list(data.keys()) if isinstance(data, dict) else 'Not a dict'}")
                            except:
                                print("Content is not JSON format")
                
                return True
                
    except Exception as e:
        print(f"Error: {e}")
        print(f"Traceback: {traceback.format_exc()}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_tavily_proper())
    if success:
        print("\n🎉 Tavily search is working!")
    else:
        print("\n❌ Tavily search failed")

