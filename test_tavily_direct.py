import asyncio
import mcp
from mcp.client.streamable_http import streamablehttp_client
import traceback

# Test different URL formats
TAVILY_URLS = [
    "https://server.smithery.ai/@Jeetanshu18/tavily-mcp/mcp?api_key=f1f6c5a8-b3d0-4815-81c3-8fa253314e6b&profile=cautious-peafowl-9gzmmK",
    "https://server.smithery.ai/@Jeetanshu18/tavily-mcp/mcp?api_key=f1f6c5a8-b3d0-4815-81c3-8fa253314e6b",
    "https://server.smithery.ai/@Jeetanshu18/tavily-mcp/mcp"
]

async def test_tavily_urls():
    for i, url in enumerate(TAVILY_URLS):
        print(f"\n=== Testing URL {i+1}: {url} ===")
        try:
            async with streamablehttp_client(url) as (read_stream, write_stream, _):
                async with mcp.ClientSession(read_stream, write_stream) as session:
                    await session.initialize()
                    tools_result = await session.list_tools()
                    print(f"✅ Available tools: {[t.name for t in tools_result.tools]}")
                    
                    # Try to call the search tool
                    if "tavily-search" in [t.name for t in tools_result.tools]:
                        print("✅ tavily-search tool found, trying to call it...")
                        
                        # Try different argument combinations
                        test_args = [
                            {"query": "What is quantum computing?"},
                            {"query": "What is quantum computing?", "search_depth": "basic"},
                            {"query": "What is quantum computing?", "include_answer": True},
                            {"query": "What is quantum computing?", "include_raw_content": True},
                            {"query": "What is quantum computing?", "max_results": 5}
                        ]
                        
                        for j, args in enumerate(test_args):
                            try:
                                print(f"  Trying args {j+1}: {args}")
                                result = await session.call_tool("tavily-search", args)
                                print(f"  ✅ SUCCESS! Result: {result}")
                                if hasattr(result, 'content') and result.content:
                                    for part in result.content:
                                        if hasattr(part, 'text') and part.text:
                                            print(f"  Content: {part.text[:200]}...")
                                return True  # Success, no need to try more
                            except Exception as e:
                                print(f"  ❌ Failed with args {j+1}: {e}")
                                if "Invalid API key" in str(e):
                                    print(f"  ❌ API key issue with URL {i+1}")
                                    break  # Don't try more args with this URL
                    else:
                        print("❌ tavily-search tool not found")
                        
        except Exception as e:
            print(f"❌ Connection error: {e}")
            if "Invalid API key" in str(e):
                print(f"❌ API key issue with URL {i+1}")
            continue
    
    return False

if __name__ == "__main__":
    success = asyncio.run(test_tavily_urls())
    if success:
        print("\n🎉 Tavily search is working!")
    else:
        print("\n❌ All Tavily URLs failed")

