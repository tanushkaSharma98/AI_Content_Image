#!/usr/bin/env python3
"""
Test Different API Key Formats
==============================

This script tests different ways to send the API key to Tavily.
"""

import asyncio
import aiohttp
import json

# Your API key
API_KEY = "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"
API_KEY_CLEAN = "mChb5rlxbMJCDtCb5aLot0lpIwKFPBLL"  # Without prefix

async def test_api_key_format(description, headers):
    """Test a specific API key format"""
    print(f"\n🔍 Testing: {description}")
    print(f"📄 Headers: {headers}")
    
    url = "https://api.tavily.com/search"
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
                
                if response.status == 200:
                    data = await response.json()
                    print("✅ SUCCESS!")
                    print(f"📝 Answer: {data.get('answer', 'No answer')[:100]}...")
                    return True
                else:
                    error_text = await response.text()
                    print(f"❌ Failed: {error_text}")
                    return False
                    
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

async def main():
    """Test different API key formats"""
    print("🧪 Testing Different API Key Formats")
    print("=" * 60)
    
    # Test different formats
    formats_to_test = [
        {
            "description": "api-key header with full key",
            "headers": {
                "api-key": API_KEY,
                "Content-Type": "application/json"
            }
        },
        {
            "description": "api-key header with clean key (no prefix)",
            "headers": {
                "api-key": API_KEY_CLEAN,
                "Content-Type": "application/json"
            }
        },
        {
            "description": "Authorization Bearer with full key",
            "headers": {
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            }
        },
        {
            "description": "Authorization Bearer with clean key",
            "headers": {
                "Authorization": f"Bearer {API_KEY_CLEAN}",
                "Content-Type": "application/json"
            }
        },
        {
            "description": "X-API-Key header with full key",
            "headers": {
                "X-API-Key": API_KEY,
                "Content-Type": "application/json"
            }
        },
        {
            "description": "X-API-Key header with clean key",
            "headers": {
                "X-API-Key": API_KEY_CLEAN,
                "Content-Type": "application/json"
            }
        }
    ]
    
    results = []
    for format_test in formats_to_test:
        success = await test_api_key_format(
            format_test["description"], 
            format_test["headers"]
        )
        results.append((format_test["description"], success))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 FORMAT TEST SUMMARY")
    print("=" * 60)
    
    for description, success in results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{description}: {status}")
    
    # Check if any worked
    if any(success for _, success in results):
        print("\n🎉 Found a working format!")
        working_formats = [desc for desc, success in results if success]
        print(f"✅ Working formats: {working_formats}")
    else:
        print("\n❌ No format worked. The API key might be:")
        print("   1. Not activated in your Tavily dashboard")
        print("   2. Expired or invalid")
        print("   3. From a different account")
        print("   4. Missing required permissions")

if __name__ == "__main__":
    asyncio.run(main())
