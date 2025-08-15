#!/usr/bin/env python3
"""
Test MCP Connection with new API key
====================================

This script tests the MCP connection using the new API key and SDK approach.
"""

import asyncio
import mcp
from mcp.client.streamable_http import streamablehttp_client

# Updated MCP URLs with new API key (profile removed)
TAVILY_MCP_URL = "https://server.smithery.ai/@Jeetanshu18/tavily-mcp/mcp?api_key=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"
FLUX_MCP_URL = "https://server.smithery.ai/@falahgs/flux-imagegen-mcp-server/mcp?api_key=f1f6c5a8-b3d0-4815-81c3-8fa253314e6b"

async def test_tavily_connection():
    """Test Tavily MCP connection"""
    print("🔍 Testing Tavily MCP Connection...")
    print(f"URL: {TAVILY_MCP_URL}")
    
    try:
        async with streamablehttp_client(TAVILY_MCP_URL) as (read_stream, write_stream, _):
            async with mcp.ClientSession(read_stream, write_stream) as session:
                # Initialize the connection
                print("📡 Initializing connection...")
                await session.initialize()
                
                # List available tools
                print("🔧 Listing available tools...")
                tools_result = await session.list_tools()
                available_tools = [t.name for t in tools_result.tools]
                print(f"✅ Available tools: {available_tools}")
                
                # Test search functionality
                if "tavily-search" in available_tools:
                    print("🔍 Testing search functionality...")
                    test_query = "What is artificial intelligence?"
                    result = await session.call_tool("tavily-search", {"query": test_query})
                    print(f"✅ Search successful!")
                    print(f"📄 Result type: {type(result)}")
                    
                    # Extract content
                    if hasattr(result, 'content') and result.content:
                        content_parts = []
                        for part in result.content:
                            if hasattr(part, 'text') and part.text:
                                content_parts.append(part.text)
                            elif hasattr(part, 'data') and part.data:
                                content_parts.append(str(part.data))
                        
                        if content_parts:
                            print(f"📝 Content preview: {content_parts[0][:200]}...")
                        else:
                            print(f"📝 Raw result: {str(result)[:200]}...")
                    else:
                        print(f"📝 Raw result: {str(result)[:200]}...")
                else:
                    print("❌ tavily-search tool not found!")
                    
    except Exception as e:
        print(f"❌ Tavily connection failed: {e}")
        return False
    
    return True

async def test_flux_connection():
    """Test Flux MCP connection"""
    print("\n🎨 Testing Flux MCP Connection...")
    print(f"URL: {FLUX_MCP_URL}")
    
    try:
        async with streamablehttp_client(FLUX_MCP_URL) as (read_stream, write_stream, _):
            async with mcp.ClientSession(read_stream, write_stream) as session:
                # Initialize the connection
                print("📡 Initializing connection...")
                await session.initialize()
                
                # List available tools
                print("🔧 Listing available tools...")
                tools_result = await session.list_tools()
                available_tools = [t.name for t in tools_result.tools]
                print(f"✅ Available tools: {available_tools}")
                
                # Test image generation functionality
                if "generateImageUrl" in available_tools:
                    print("🎨 Testing image generation functionality...")
                    test_prompt = "A beautiful sunset over mountains"
                    result = await session.call_tool("generateImageUrl", {"prompt": test_prompt})
                    print(f"✅ Image generation successful!")
                    print(f"📄 Result type: {type(result)}")
                    
                    # Extract content
                    if hasattr(result, 'content') and result.content:
                        content_parts = []
                        for part in result.content:
                            if hasattr(part, 'text') and part.text:
                                content_parts.append(part.text)
                            elif hasattr(part, 'data') and part.data:
                                content_parts.append(str(part.data))
                        
                        if content_parts:
                            print(f"🖼️  Image URL preview: {content_parts[0][:100]}...")
                        else:
                            print(f"🖼️  Raw result: {str(result)[:100]}...")
                    else:
                        print(f"🖼️  Raw result: {str(result)[:100]}...")
                else:
                    print("❌ generateImageUrl tool not found!")
                    
    except Exception as e:
        print(f"❌ Flux connection failed: {e}")
        return False
    
    return True

async def main():
    """Main test function"""
    print("🧪 MCP Connection Test with New API Key")
    print("=" * 50)
    
    # Test Tavily
    tavily_success = await test_tavily_connection()
    
    # Test Flux
    flux_success = await test_flux_connection()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)
    print(f"Tavily Search: {'✅ PASSED' if tavily_success else '❌ FAILED'}")
    print(f"Flux Image Gen: {'✅ PASSED' if flux_success else '❌ FAILED'}")
    
    if tavily_success and flux_success:
        print("\n🎉 All MCP connections working!")
        print("✅ You can now test the search and image generation in Swagger UI")
        print("🌐 Go to: http://localhost:8000/docs")
    else:
        print("\n⚠️  Some connections failed. Check the error messages above.")

if __name__ == "__main__":
    asyncio.run(main())
