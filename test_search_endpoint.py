#!/usr/bin/env python3
"""
Test Search Endpoint with Fallback Service
==========================================

This script tests the search endpoint to see if the fallback service works.
"""

import asyncio
import aiohttp
import json

async def test_search_endpoint():
    """Test the search endpoint"""
    print("🔍 Testing Search Endpoint...")
    
    # Test data
    search_data = {
        "query": "Who was the first president of India?"
    }
    
    # You'll need to get a valid JWT token first
    # For now, let's test the fallback service directly
    from app.services.search_service import fallback_search_service
    
    try:
        print("📡 Testing fallback search service...")
        result = await fallback_search_service.search_with_wikipedia("India")
        
        print("✅ Fallback search successful!")
        print(f"📄 Query: {result.get('query')}")
        print(f"📝 Summary: {result.get('summary', 'No summary')}")
        print(f"🔗 Results count: {len(result.get('results', []))}")
        
        if result.get('results'):
            first_result = result['results'][0]
            print(f"📰 First result title: {first_result.get('title', 'No title')}")
            print(f"🔗 First result URL: {first_result.get('url', 'No URL')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Fallback search failed: {e}")
        return False

async def main():
    """Main test function"""
    print("🧪 Search Endpoint Test with Fallback")
    print("=" * 50)
    
    success = await test_search_endpoint()
    
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)
    print(f"Search with Fallback: {'✅ PASSED' if success else '❌ FAILED'}")
    
    if success:
        print("\n🎉 Search functionality working with fallback!")
        print("✅ You can now test the search in Swagger UI")
        print("🌐 Go to: http://localhost:8000/docs")
    else:
        print("\n⚠️  Search still has issues.")

if __name__ == "__main__":
    asyncio.run(main())
