"""
Direct Tavily API Service
=========================

This service provides direct integration with Tavily API without using MCP.
"""

import aiohttp
import json
from typing import Dict, List, Any
from datetime import datetime
from app.core.config import settings

class TavilyService:
    """Direct Tavily API integration service"""
    
    def __init__(self):
        self.api_key = settings.mcp_tavily_api_key
        self.base_url = "https://api.tavily.com"
    
    async def search(self, query: str, search_depth: str = "basic", max_results: int = 10) -> Dict[str, Any]:
        """
        Perform a web search using Tavily API directly
        
        Args:
            query: Search query
            search_depth: "basic" or "advanced"
            max_results: Maximum number of results to return
            
        Returns:
            Dictionary containing search results
        """
        try:
            url = f"{self.base_url}/search"
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "query": query,
                "search_depth": search_depth,
                "include_answer": True,
                "include_raw_content": False,
                "max_results": max_results
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, json=payload) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        # Transform Tavily response to match our expected format
                        results = []
                        for result in data.get("results", []):
                            results.append({
                                "title": result.get("title", ""),
                                "url": result.get("url", ""),
                                "summary": result.get("content", ""),
                                "content": result.get("content", "")
                            })
                        
                        return {
                            "success": True,
                            "query": query,
                            "results": results,
                            "summary": data.get("answer", f"Search results for: {query}"),
                            "timestamp": datetime.utcnow().isoformat(),
                            "source": "tavily_direct_api"
                        }
                    else:
                        error_text = await response.text()
                        print(f"Tavily API error: {response.status} - {error_text}")
                        raise Exception(f"Tavily API error: {response.status}")
                        
        except Exception as e:
            print(f"Tavily service error: {e}")
            raise Exception(f"Tavily search failed: {str(e)}")

# Global instance
tavily_service = TavilyService()
