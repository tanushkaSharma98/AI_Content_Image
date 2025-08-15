"""
Fallback Search Service
=======================

This service provides search functionality as a fallback when Tavily API is not available.
"""

import asyncio
import json
from typing import Dict, List, Any
from datetime import datetime

class FallbackSearchService:
    """Fallback search service that provides basic search functionality"""
    
    @staticmethod
    async def search_web(query: str) -> Dict[str, Any]:
        """
        Perform a web search using fallback methods
        """
        print(f"🔍 Fallback search for: {query}")
        
        # For now, return a structured response that matches our expected format
        # In a real implementation, you could use:
        # - DuckDuckGo API
        # - Google Custom Search API
        # - Bing Search API
        # - Wikipedia API
        # - Or any other search service
        
        # Create a mock response that matches our SearchResponse schema
        mock_results = [
            {
                "title": f"Search Results for: {query}",
                "url": f"https://example.com/search?q={query}",
                "summary": f"This is a fallback search result for '{query}'. The actual Tavily API is currently unavailable.",
                "content": f"Search query: {query}. This is a placeholder result while we resolve the API authentication issues."
            },
            {
                "title": "Search Service Status",
                "url": "https://example.com/status",
                "summary": "Tavily API authentication is being resolved. Using fallback search service.",
                "content": "The search functionality is temporarily using a fallback service while we fix the API authentication."
            }
        ]
        
        return {
            "success": True,
            "query": query,
            "results": mock_results,
            "summary": f"Fallback search results for '{query}'. Tavily API authentication is being resolved.",
            "timestamp": datetime.utcnow().isoformat(),
            "source": "fallback_service"
        }
    
    @staticmethod
    async def search_with_wikipedia(query: str) -> Dict[str, Any]:
        """
        Search using Wikipedia API as a fallback
        """
        try:
            import aiohttp
            
            # Wikipedia API endpoint
            url = "https://en.wikipedia.org/api/rest_v1/page/summary/" + query.replace(" ", "_")
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        results = [{
                            "title": data.get("title", query),
                            "url": data.get("content_urls", {}).get("desktop", {}).get("page", ""),
                            "summary": data.get("extract", f"Wikipedia article about {query}"),
                            "content": data.get("extract", "")
                        }]
                        
                        return {
                            "success": True,
                            "query": query,
                            "results": results,
                            "summary": data.get("extract", f"Wikipedia results for {query}"),
                            "timestamp": datetime.utcnow().isoformat(),
                            "source": "wikipedia_api"
                        }
                    else:
                        # Fall back to basic search
                        return await FallbackSearchService.search_web(query)
                        
        except Exception as e:
            print(f"Wikipedia search failed: {e}")
            # Fall back to basic search
            return await FallbackSearchService.search_web(query)

# Global instance
fallback_search_service = FallbackSearchService()
