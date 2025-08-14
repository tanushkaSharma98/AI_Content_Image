import asyncio
import mcp
from mcp.client.streamable_http import streamablehttp_client
import traceback

# Try different URL formats and approaches
TAVILY_URLS = [
    "https://server.smithery.ai/@Jeetanshu18/tavily-mcp/mcp?api_key=f1f6c5a8-b3d0-4815-81c3-8fa253314e6b&profile=cautious-peafowl-9gzmmK",
    "https://server.smithery.ai/@Jeetanshu18/tavily-mcp/mcp?api_key=f1f6c5a8-b3d0-4815-81c3-8fa253314e6b",
    "https://server.smithery.ai/@Jeetanshu18/tavily-mcp/mcp"
]

async def test_tavily_alternative():
    for i, url in enumerate(TAVILY_URLS):
        print(f"\n=== Testing URL {i+1}: {url} ===")
        try:
            async with streamablehttp_client(url) as (read_stream, write_stream, _):
                async with mcp.ClientSession(read_stream, write_stream) as session:
                    await session.initialize()
                    tools_result = await session.list_tools()
                    print(f"✅ Available tools: {[t.name for t in tools_result.tools]}")
                    
                    # Try minimal parameters first
                    search_args = {"query": "What is quantum computing?"}
                    print(f"Trying minimal args: {search_args}")
                    
                    try:
                        result = await session.call_tool("tavily-search", search_args)
                        print(f"✅ SUCCESS with minimal args! Result: {result}")
                        if hasattr(result, 'content') and result.content:
                            for part in result.content:
                                if hasattr(part, 'text') and part.text:
                                    print(f"Content: {part.text[:300]}...")
                        return True
                    except Exception as e:
                        print(f"❌ Failed with minimal args: {e}")
                        
                        # Try with different parameter combinations
                        test_args_list = [
                            {"query": "What is quantum computing?", "search_depth": "basic"},
                            {"query": "What is quantum computing?", "max_results": 1},
                            {"query": "What is quantum computing?", "topic": "general"},
                            {"query": "What is quantum computing?", "search_depth": "basic", "max_results": 1}
                        ]
                        
                        for j, args in enumerate(test_args_list):
                            try:
                                print(f"  Trying args {j+1}: {args}")
                                result = await session.call_tool("tavily-search", args)
                                print(f"  ✅ SUCCESS! Result: {result}")
                                if hasattr(result, 'content') and result.content:
                                    for part in result.content:
                                        if hasattr(part, 'text') and part.text:
                                            print(f"  Content: {part.text[:300]}...")
                                return True
                            except Exception as e2:
                                print(f"  ❌ Failed with args {j+1}: {e2}")
                                if "Invalid API key" in str(e2):
                                    print(f"  ❌ API key issue with URL {i+1}")
                                    break
                        
        except Exception as e:
            print(f"❌ Connection error: {e}")
            if "Invalid API key" in str(e):
                print(f"❌ API key issue with URL {i+1}")
            continue
    
    return False

if __name__ == "__main__":
    success = asyncio.run(test_tavily_alternative())
    if success:
        print("\n🎉 Tavily search is working!")
    else:
        print("\n❌ All Tavily URLs failed")

