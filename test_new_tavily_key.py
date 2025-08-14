import asyncio
import mcp
from mcp.client.streamable_http import streamablehttp_client
import traceback

# NEW API key and profile
TAVILY_MCP_URL = "https://server.smithery.ai/@Jeetanshu18/tavily-mcp/mcp?api_key=1096430b-be20-4c9a-8b78-3351cc188776&profile=shaky-stingray-GvJFoQ"

async def test_new_tavily_key():
    print("Testing NEW Tavily API key...")
    print(f"URL: {TAVILY_MCP_URL}")
    
    try:
        async with streamablehttp_client(TAVILY_MCP_URL) as (read_stream, write_stream, _):
            async with mcp.ClientSession(read_stream, write_stream) as session:
                await session.initialize()
                tools_result = await session.list_tools()
                print(f"✅ Available tools: {[t.name for t in tools_result.tools]}")
                
                # Test with the query you mentioned: "who is anil ambani"
                search_args = {
                    "query": "who is anil ambani",
                    "search_depth": "basic",
                    "max_results": 3,
                    "include_raw_content": True,
                    "topic": "general"
                }
                
                print(f"Calling tavily-search with args: {search_args}")
                result = await session.call_tool("tavily-search", search_args)
                print(f"✅ SUCCESS! Result: {result}")
                
                if hasattr(result, 'content') and result.content:
                    for part in result.content:
                        if hasattr(part, 'text') and part.text:
                            print(f"Content: {part.text}")
                            # Try to parse as JSON to see the structure
                            try:
                                import json
                                data = json.loads(part.text)
                                print(f"Parsed JSON structure: {list(data.keys()) if isinstance(data, dict) else 'Not a dict'}")
                                if isinstance(data, dict):
                                    print(f"Query: {data.get('query', 'N/A')}")
                                    print(f"Results count: {len(data.get('results', []))}")
                                    if data.get('results'):
                                        first_result = data['results'][0]
                                        print(f"First result title: {first_result.get('title', 'N/A')}")
                                        print(f"First result summary: {first_result.get('summary', 'N/A')[:200]}...")
                            except:
                                print("Content is not JSON format")
                
                return True
                
    except Exception as e:
        print(f"❌ Error: {e}")
        print(f"Traceback: {traceback.format_exc()}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_new_tavily_key())
    if success:
        print("\n🎉 NEW Tavily API key is working!")
    else:
        print("\n❌ NEW Tavily API key failed")

