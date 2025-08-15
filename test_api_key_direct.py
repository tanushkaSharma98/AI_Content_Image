#!/usr/bin/env python3
"""
Test API Key Directly
====================

This script tests the API key directly with Tavily API.
"""

import asyncio
import aiohttp
import json

# Your API key
API_KEY = "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"

async def test_api_key():
    """Test the API key directly"""
    print(f"🔑 Testing API Key: {API_KEY}")
    
    url = "https://api.tavily.com/search"
    headers = {
        "api-key": API_KEY,
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
                    print("✅ API Key is valid!")
                    print(f"📝 Answer: {data.get('answer', 'No answer')}")
                    return True
                else:
                    error_text = await response.text()
                    print(f"❌ API Key failed: {error_text}")
                    return False
                    
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

async def main():
    """Main function"""
    print("🧪 API Key Test")
    print("=" * 50)
    
    success = await test_api_key()
    
    if success:
        print("\n🎉 API Key is working!")
    else:
        print("\n❌ API Key is not working. Please check:")
        print("   1. Is the key activated in your Tavily dashboard?")
        print("   2. Is the key format correct?")
        print("   3. Do you have sufficient credits/quota?")

if __name__ == "__main__":
    asyncio.run(main())
