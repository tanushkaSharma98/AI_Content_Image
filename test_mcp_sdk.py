import asyncio
import mcp
from mcp.client.streamable_http import streamablehttp_client

# Test URLs with API keys
TAVILY_URL = "https://server.smithery.ai/@Jeetanshu18/tavily-mcp/mcp?api_key=f1f6c5a8-b3d0-4815-81c3-8fa253314e6b&profile=cautious-peafowl-9gzmmK"
FLUX_URL = "https://server.smithery.ai/@falahgs/flux-imagegen-mcp-server/mcp?api_key=f1f6c5a8-b3d0-4815-81c3-8fa253314e6b"

async def test_tavily():
    print("Testing Tavily MCP...")
    try:
        async with streamablehttp_client(TAVILY_URL) as (read_stream, write_stream, _):
            async with mcp.ClientSession(read_stream, write_stream) as session:
                await session.initialize()
                tools_result = await session.list_tools()
                print(f"Available tools: {[t.name for t in tools_result.tools]}")
                
                # Try to call the search tool
                if any(t.name == "tavily-search" for t in tools_result.tools):
                    result = await session.call_tool("tavily-search", {"query": "What is quantum computing?"})
                    print(f"Search result: {result}")
                    if hasattr(result, 'content') and result.content:
                        for part in result.content:
                            if hasattr(part, 'text') and part.text:
                                print(f"Content: {part.text}")
                else:
                    print("tavily-search tool not found")
    except Exception as e:
        print(f"Tavily test failed: {e}")

async def test_flux():
    print("\nTesting Flux MCP...")
    try:
        async with streamablehttp_client(FLUX_URL) as (read_stream, write_stream, _):
            async with mcp.ClientSession(read_stream, write_stream) as session:
                await session.initialize()
                tools_result = await session.list_tools()
                print(f"Available tools: {[t.name for t in tools_result.tools]}")
                
                # Try to call the image generation tool
                if any(t.name == "generateImageUrl" for t in tools_result.tools):
                    result = await session.call_tool("generateImageUrl", {"prompt": "a beautiful sunset"})
                    print(f"Image generation result: {result}")
                    if hasattr(result, 'content') and result.content:
                        for part in result.content:
                            if hasattr(part, 'text') and part.text:
                                print(f"Content: {part.text}")
                else:
                    print("generateImageUrl tool not found")
    except Exception as e:
        print(f"Flux test failed: {e}")

async def main():
    await test_tavily()
    await test_flux()

if __name__ == "__main__":
    asyncio.run(main())
