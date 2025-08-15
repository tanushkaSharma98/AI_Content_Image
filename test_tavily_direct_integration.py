#!/usr/bin/env python3
"""
Test Direct Tavily API Integration
==================================

This script tests the direct Tavily API integration.
"""

import asyncio
import sys
import os

# Add the backend directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

async def test_tavily_direct_integration():
    """Test the direct Tavily API integration"""
    print("🔍 Testing Direct Tavily API Integration...")
    
    try:
        from app.services.tavily_service import tavily_service
        
        # Test search
        query = "What is artificial intelligence?"
        print(f"📡 Testing search for: {query}")
        
        result = await tavily_service.search(query)
        
        print("✅ Tavily direct API integration successful!")
        print(f"📄 Query: {result.get('query')}")
        print(f"📝 Summary: {result.get('summary', 'No summary')[:200]}...")
        print(f"🔗 Results count: {len(result.get('results', []))}")
        
        if result.get('results'):
            first_result = result['results'][0]
            print(f"📰 First result title: {first_result.get('title', 'No title')}")
            print(f"🔗 First result URL: {first_result.get('url', 'No URL')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Tavily direct API integration failed: {e}")
        return False

async def test_fallback_service():
    """Test the fallback service"""
    print("\n🔄 Testing Fallback Service...")
    
    try:
        from app.services.search_service import fallback_search_service
        
        query = "India"
        result = await fallback_search_service.search_with_wikipedia(query)
        
        print("✅ Fallback service working!")
        print(f"📄 Query: {result.get('query')}")
        print(f"📝 Summary: {result.get('summary', 'No summary')[:200]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Fallback service failed: {e}")
        return False

async def main():
    """Main test function"""
    print("🧪 Direct Tavily API Integration Test")
    print("=" * 60)
    
    # Test direct Tavily integration
    tavily_success = await test_tavily_direct_integration()
    
    # Test fallback service
    fallback_success = await test_fallback_service()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    print(f"Direct Tavily API: {'✅ PASSED' if tavily_success else '❌ FAILED'}")
    print(f"Fallback Service: {'✅ PASSED' if fallback_success else '❌ FAILED'}")
    
    if tavily_success:
        print("\n🎉 Direct Tavily API integration working!")
        print("✅ You can now test the search in your application")
    elif fallback_success:
        print("\n⚠️  Tavily API failed, but fallback service is working")
        print("✅ Users will still get search results via Wikipedia")
    else:
        print("\n❌ Both services failed. Check the configuration.")

if __name__ == "__main__":
    asyncio.run(main())
