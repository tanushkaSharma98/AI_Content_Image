#!/usr/bin/env python3
"""
Test Direct Tavily API Integration
==================================

This script tests direct Tavily API integration as an alternative to MCP.
"""

import asyncio
import aiohttp
import json

# Your Tavily API key
TAVILY_API_KEY = "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"

async def test_tavily_direct_api():
    """Test direct Tavily API integration"""
    print("🔍 Testing Direct Tavily API...")
    print(f"API Key: {TAVILY_API_KEY}")
    
    url = "https://api.tavily.com/search"
    headers = {
        "api-key": TAVILY_API_KEY,
        "Content-Type": "application/json"
    }
    
    payload = {
        "query": "Who was the first president of India?",
        "search_depth": "basic",
        "include_answer": True,
        "include_raw_content": False,
        "max_results": 5
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=payload) as response:
                if response.status == 200:
                    data = await response.json()
                    print("✅ Tavily API call successful!")
                    print(f"📄 Response type: {type(data)}")
                    print(f"📝 Answer: {data.get('answer', 'No answer provided')}")
                    print(f"🔗 Results count: {len(data.get('results', []))}")
                    
                    # Show first result
                    if data.get('results'):
                        first_result = data['results'][0]
                        print(f"📰 First result title: {first_result.get('title', 'No title')}")
                        print(f"🔗 First result URL: {first_result.get('url', 'No URL')}")
                    
                    return True
                else:
                    error_text = await response.text()
                    print(f"❌ Tavily API call failed with status {response.status}")
                    print(f"📄 Error response: {error_text}")
                    return False
                    
    except Exception as e:
        print(f"❌ Tavily API call failed: {e}")
        return False

async def main():
    """Main test function"""
    print("🧪 Direct Tavily API Test")
    print("=" * 50)
    
    success = await test_tavily_direct_api()
    
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)
    print(f"Direct Tavily API: {'✅ PASSED' if success else '❌ FAILED'}")
    
    if success:
        print("\n🎉 Direct Tavily API working!")
        print("✅ We can use direct API integration instead of MCP")
    else:
        print("\n⚠️  Direct API also failed. Check the API key.")

if __name__ == "__main__":
    asyncio.run(main())
