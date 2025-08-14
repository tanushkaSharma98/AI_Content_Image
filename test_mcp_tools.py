import asyncio
import mcp
from mcp.client.streamable_http import streamablehttp_client

# MCP server URLs
TAVILY_MCP_URL = "https://server.smithery.ai/@Jeetanshu18/tavily-mcp/mcp?api_key=f1f6c5a8-b3d0-4815-81c3-8fa253314e6b&profile=cautious-peafowl-9gzmmK"
FLUX_MCP_URL = "https://server.smithery.ai/@falahgs/flux-imagegen-mcp-server/mcp?api_key=f1f6c5a8-b3d0-4815-81c3-8fa253314e6b"

async def test_tavily_tools():
    print("Testing Tavily MCP tools...")
    try:
        async with streamablehttp_client(TAVILY_MCP_URL) as (read_stream, write_stream, _):
            async with mcp.ClientSession(read_stream, write_stream) as session:
                await session.initialize()
                tools_result = await session.list_tools()
                print(f"Available Tavily tools: {[t.name for t in tools_result.tools]}")
                
                # Try to call the search tool
                if tools_result.tools:
                    tool_name = tools_result.tools[0].name
                    print(f"Trying to call tool: {tool_name}")
                    result = await session.call_tool(tool_name, {"query": "What is quantum computing?"})
                    print(f"Result: {result}")
                    if hasattr(result, 'content') and result.content:
                        for part in result.content:
                            if hasattr(part, 'text') and part.text:
                                print(f"Content: {part.text}")
    except Exception as e:
        print(f"Tavily error: {e}")

async def test_flux_tools():
    print("\nTesting Flux MCP tools...")
    try:
        async with streamablehttp_client(FLUX_MCP_URL) as (read_stream, write_stream, _):
            async with mcp.ClientSession(read_stream, write_stream) as session:
                await session.initialize()
                tools_result = await session.list_tools()
                print(f"Available Flux tools: {[t.name for t in tools_result.tools]}")
                
                # Try to call the image generation tool
                if tools_result.tools:
                    tool_name = tools_result.tools[0].name
                    print(f"Trying to call tool: {tool_name}")
                    result = await session.call_tool(tool_name, {"prompt": "a beautiful sunset"})
                    print(f"Result: {result}")
                    if hasattr(result, 'content') and result.content:
                        for part in result.content:
                            if hasattr(part, 'text') and part.text:
                                print(f"Content: {part.text}")
    except Exception as e:
        print(f"Flux error: {e}")

if __name__ == "__main__":
    asyncio.run(test_tavily_tools())
    asyncio.run(test_flux_tools())

