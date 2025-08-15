#!/usr/bin/env python3
"""
Detailed Tavily Debug Script
============================

This script will help us understand exactly why the Tavily API is failing.
"""

import asyncio
import aiohttp
import json
import traceback
from mcp.client.streamable_http import streamablehttp_client
import mcp

# Test different API key formats
API_KEYS_TO_TEST = [
    "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",  # With tvly-dev prefix
    "jkM1m4hGUOScYrlxEpzZ89Uo0tyumn9z",            # Without prefix
    "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",       # With tvly prefix
]

# Test different Smithery profiles
PROFILES_TO_TEST = [
    "cautious-peafowl-9gzmmK",
    "shaky-stingray-GvJFoQ",
    "default"
]

async def test_direct_tavily_api(api_key):
    """Test direct Tavily API with different key formats"""
    print(f"\n🔍 Testing Direct Tavily API with key: {api_key[:20]}...")
    
    url = "https://api.tavily.com/search"
    headers = {
        "api-key": api_key,
        "Content-Type": "application/json"
    }
    
    payload = {
        "query": "test",
        "search_depth": "basic",
        "include_answer": True,
        "include_raw_content": False,
        "max_results": 1
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=payload) as response:
                print(f"📡 Status: {response.status}")
                print(f"📄 Headers: {dict(response.headers)}")
                
                if response.status == 200:
                    data = await response.json()
                    print("✅ Direct API SUCCESS!")
                    return True
                else:
                    error_text = await response.text()
                    print(f"❌ Direct API failed: {error_text}")
                    return False
                    
    except Exception as e:
        print(f"❌ Direct API exception: {e}")
        print(f"📄 Traceback: {traceback.format_exc()}")
        return False

async def test_smithery_mcp(api_key, profile):
    """Test Smithery MCP with different configurations"""
    print(f"\n🔍 Testing Smithery MCP with key: {api_key[:20]}... and profile: {profile}")
    
    url = f"https://server.smithery.ai/@Jeetanshu18/tavily-mcp/mcp?api_key={api_key}&profile={profile}"
    
    try:
        async with streamablehttp_client(url) as (read_stream, write_stream, _):
            async with mcp.ClientSession(read_stream, write_stream) as session:
                print("📡 Initializing connection...")
                await session.initialize()
                
                print("🔧 Listing tools...")
                tools_result = await session.list_tools()
                available_tools = [t.name for t in tools_result.tools]
                print(f"✅ Available tools: {available_tools}")
                
                if "tavily-search" in available_tools:
                    print("🔍 Testing search...")
                    result = await session.call_tool("tavily-search", {"query": "test"})
                    print("✅ Smithery MCP SUCCESS!")
                    return True
                else:
                    print("❌ tavily-search tool not found")
                    return False
                    
    except Exception as e:
        print(f"❌ Smithery MCP failed: {e}")
        print(f"📄 Error type: {type(e).__name__}")
        print(f"📄 Error message: {str(e)}")
        
        # Check for specific error types
        if "Invalid API key" in str(e):
            print("🔑 This looks like an API key authentication error")
        elif "TaskGroup" in str(e):
            print("🔄 This looks like a connection/async error")
        elif "timeout" in str(e).lower():
            print("⏰ This looks like a timeout error")
        elif "connection" in str(e).lower():
            print("🌐 This looks like a network connection error")
        
        return False

async def test_network_connectivity():
    """Test basic network connectivity"""
    print("\n🌐 Testing Network Connectivity...")
    
    test_urls = [
        "https://api.tavily.com",
        "https://server.smithery.ai",
        "https://google.com"
    ]
    
    for url in test_urls:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=10) as response:
                    print(f"✅ {url}: {response.status}")
        except Exception as e:
            print(f"❌ {url}: {e}")

async def main():
    """Main debug function"""
    print("🧪 Detailed Tavily Debug")
    print("=" * 60)
    
    # Test network connectivity first
    await test_network_connectivity()
    
    # Test direct API with different key formats
    print("\n" + "=" * 60)
    print("🔑 Testing Direct Tavily API with different key formats")
    print("=" * 60)
    
    direct_results = []
    for api_key in API_KEYS_TO_TEST:
        success = await test_direct_tavily_api(api_key)
        direct_results.append((api_key, success))
    
    # Test Smithery MCP with different configurations
    print("\n" + "=" * 60)
    print("🔧 Testing Smithery MCP with different configurations")
    print("=" * 60)
    
    mcp_results = []
    for api_key in API_KEYS_TO_TEST:
        for profile in PROFILES_TO_TEST:
            success = await test_smithery_mcp(api_key, profile)
            mcp_results.append((api_key, profile, success))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 DEBUG SUMMARY")
    print("=" * 60)
    
    print("\n🔑 Direct API Results:")
    for api_key, success in direct_results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"  {api_key[:20]}...: {status}")
    
    print("\n🔧 Smithery MCP Results:")
    for api_key, profile, success in mcp_results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"  {api_key[:20]}... + {profile}: {status}")
    
    # Recommendations
    print("\n💡 Recommendations:")
    if any(success for _, success in direct_results):
        print("  ✅ Direct API works - use direct integration instead of MCP")
    elif any(success for _, _, success in mcp_results):
        print("  ✅ Smithery MCP works - use the working configuration")
    else:
        print("  ❌ All methods failed - check API key validity and network")

if __name__ == "__main__":
    asyncio.run(main())
