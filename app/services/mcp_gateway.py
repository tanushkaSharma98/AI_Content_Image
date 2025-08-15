import json
import traceback
from typing import Any, Dict, List
import mcp
from mcp.client.streamable_http import streamablehttp_client
from mcp.shared.exceptions import McpError

class MCPGatewayError(Exception):
    pass

# MCP server URLs - Updated with new API keys
# Using the new Tavily API key for the Tavily service (profile removed)
TAVILY_MCP_URL = "https://server.smithery.ai/@Jeetanshu18/tavily-mcp/mcp?api_key=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"
FLUX_MCP_URL = "https://server.smithery.ai/@falahgs/flux-imagegen-mcp-server/mcp?api_key=f1f6c5a8-b3d0-4815-81c3-8fa253314e6b"

async def _call_mcp_tool_sdk(server_url: str, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
    """Call an MCP tool using the official MCP SDK"""
    try:
        print(f"DEBUG: Connecting to {server_url}")
        print(f"DEBUG: Tool: {tool_name}, Arguments: {arguments}")
        
        async with streamablehttp_client(server_url) as (read_stream, write_stream, _):
            async with mcp.ClientSession(read_stream, write_stream) as session:
                # Initialize the connection
                await session.initialize()
                
                # List available tools to verify
                tools_result = await session.list_tools()
                available_tools = [t.name for t in tools_result.tools]
                print(f"DEBUG: Available tools: {available_tools}")
                
                # Call the specific tool
                if tool_name in available_tools:
                    result = await session.call_tool(tool_name, arguments)
                    print(f"DEBUG: Tool call result: {result}")
                    
                    # Extract content from the result
                    if hasattr(result, 'content') and result.content:
                        content_parts = []
                        for part in result.content:
                            if hasattr(part, 'text') and part.text:
                                content_parts.append(part.text)
                            elif hasattr(part, 'data') and part.data:
                                content_parts.append(str(part.data))
                        
                        if content_parts:
                            return {
                                "success": True,
                                "content": "\n".join(content_parts),
                                "raw_result": str(result)
                            }
                    
                    return {
                        "success": True,
                        "content": str(result),
                        "raw_result": str(result)
                    }
                else:
                    raise MCPGatewayError(f"Tool '{tool_name}' not found. Available tools: {available_tools}")
                                    
    except McpError as e:
        print(f"DEBUG: MCP Error: {e}")
        if "Invalid API key" in str(e):
            raise MCPGatewayError("Invalid API key")
        else:
            raise MCPGatewayError(f"MCP Error: {e}")
    except Exception as e:
        print(f"DEBUG: MCP SDK call failed: {e}")
        print(f"DEBUG: Traceback: {traceback.format_exc()}")
        
        # Check if it's an API key error in the exception chain
        error_str = str(e)
        if "Invalid API key" in error_str:
            raise MCPGatewayError("Invalid API key")
        
        # Check if it's a TaskGroup exception that might contain the real error
        if "TaskGroup" in error_str and hasattr(e, '__cause__') and e.__cause__:
            cause_str = str(e.__cause__)
            if "Invalid API key" in cause_str:
                raise MCPGatewayError("Invalid API key")
        
        # Check if it's an ExceptionGroup
        if hasattr(e, 'exceptions') and e.exceptions:
            for sub_exception in e.exceptions:
                sub_str = str(sub_exception)
                if "Invalid API key" in sub_str:
                    raise MCPGatewayError("Invalid API key")
        
        raise MCPGatewayError(f"MCP SDK call failed: {e}")

async def _call_mcp_tool(server_url: str, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
    """Call an MCP tool - use SDK approach"""
    try:
        return await _call_mcp_tool_sdk(server_url, tool_name, arguments)
    except McpError as e:
        # Re-raise McpError directly to preserve the "Invalid API key" message
        if "Invalid API key" in str(e):
            raise MCPGatewayError("Invalid API key")
        else:
            raise MCPGatewayError(f"MCP Error: {e}")
    except Exception as e:
        raise MCPGatewayError(f"Tool call failed: {e}")

async def call_tavily_search(query: str) -> Dict[str, Any]:
    """Call Tavily API directly for web search"""
    print(f"DEBUG: Calling Tavily search with dynamic query: {query}")
    try:
        # Use direct Tavily API service
        from app.services.tavily_service import tavily_service
        return await tavily_service.search(query)
    except Exception as e:
        print(f"DEBUG: Tavily direct API failed: {e}")
        print("DEBUG: Falling back to fallback search service...")
        
        # Import and use fallback service
        from app.services.search_service import fallback_search_service
        return await fallback_search_service.search_with_wikipedia(query)

async def call_flux_generate_image_url(prompt: str) -> Dict[str, Any]:
    """Call Flux MCP server for image generation"""
    print(f"DEBUG: Calling Flux image generation with prompt: {prompt}")
    return await _call_mcp_tool(FLUX_MCP_URL, "generateImageUrl", {"prompt": prompt})
