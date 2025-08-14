import asyncio
import mcp
from mcp.client.streamable_http import streamablehttp_client
import traceback

TAVILY_MCP_URL = "https://server.smithery.ai/@Jeetanshu18/tavily-mcp/mcp?api_key=f1f6c5a8-b3d0-4815-81c3-8fa253314e6b&profile=cautious-peafowl-9gzmmK"

async def debug_tavily():
    print("Debugging Tavily MCP...")
    try:
        async with streamablehttp_client(TAVILY_MCP_URL) as (read_stream, write_stream, _):
            async with mcp.ClientSession(read_stream, write_stream) as session:
                await session.initialize()
                tools_result = await session.list_tools()
                print(f"Available tools: {[t.name for t in tools_result.tools]}")
                
                # Try to call the search tool with different parameters
                tool_name = "tavily-search"
                print(f"Calling {tool_name}...")
                
                # Try different argument formats
                test_args = [
                    {"query": "What is quantum computing?"},
                    {"query": "What is quantum computing?", "search_depth": "basic"},
                    {"query": "What is quantum computing?", "include_answer": True},
                    {"query": "What is quantum computing?", "include_raw_content": True}
                ]
                
                for i, args in enumerate(test_args):
                    try:
                        print(f"\nTrying args {i+1}: {args}")
                        result = await session.call_tool(tool_name, args)
                        print(f"SUCCESS! Result: {result}")
                        if hasattr(result, 'content') and result.content:
                            for part in result.content:
                                if hasattr(part, 'text') and part.text:
                                    print(f"Content: {part.text}")
                        break
                    except Exception as e:
                        print(f"Failed with args {i+1}: {e}")
                        print(f"Traceback: {traceback.format_exc()}")
                        
    except Exception as e:
        print(f"Connection error: {e}")
        print(f"Full traceback: {traceback.format_exc()}")

if __name__ == "__main__":
    asyncio.run(debug_tavily())
