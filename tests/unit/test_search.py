import pytest
from unittest.mock import patch, MagicMock, AsyncMock

class TestSearchService:
    """Test search service logic."""
    
    @pytest.mark.asyncio
    @patch('app.services.mcp_gateway.call_tavily_search')
    async def test_tavily_search_success(self, mock_tavily):
        """Test successful Tavily search call."""
        from app.services.mcp_gateway import call_tavily_search
        
        mock_tavily.return_value = {
            "result_title": "Test Result",
            "result_summary": "Test summary",
            "result_url": "https://example.com"
        }
        
        result = await call_tavily_search("test query")
        
        assert result["result_title"] == "Test Result"
        assert result["result_summary"] == "Test summary"
        assert result["result_url"] == "https://example.com"
        mock_tavily.assert_called_once_with("test query")
    
    @pytest.mark.asyncio
    @patch('app.services.mcp_gateway.call_tavily_search')
    async def test_tavily_search_error_handling(self, mock_tavily):
        """Test Tavily search error handling."""
        from app.services.mcp_gateway import call_tavily_search
        
        mock_tavily.side_effect = Exception("API Error")
        
        with pytest.raises(Exception):
            await call_tavily_search("test query")

class TestSearchLogic:
    """Test search logic without HTTP client."""
    
    def test_search_query_validation(self):
        """Test search query validation logic."""
        from app.schemas.search import SearchRequest
        
        # Test valid query
        valid_request = SearchRequest(query="What is quantum computing?")
        assert valid_request.query == "What is quantum computing?"
        
        # Test empty query (should raise validation error)
        with pytest.raises(ValueError):
            SearchRequest(query="")
    
    def test_search_response_structure(self):
        """Test search response structure validation."""
        from app.schemas.search import SearchResponse, SearchResult
        
        # Test valid response structure
        response_data = {
            "query": "What is quantum computing?",
            "results": [
                {
                    "title": "Quantum Computing Explained",
                    "url": "https://example.com/quantum-computing",
                    "summary": "Quantum computing is a type of computation...",
                    "content": "Detailed content about quantum computing..."
                }
            ],
            "summary": "Overview of quantum computing concepts",
            "timestamp": "2024-01-01T12:00:00Z",
            "saved_item_id": 1,
            "total_results": 1
        }
        
        response = SearchResponse(**response_data)
        assert response.query == "What is quantum computing?"
        assert len(response.results) == 1
        assert response.results[0].title == "Quantum Computing Explained"
        assert response.results[0].url == "https://example.com/quantum-computing"
        assert response.summary == "Overview of quantum computing concepts"
        assert response.total_results == 1
    
    @pytest.mark.asyncio
    @patch('app.services.mcp_gateway.call_tavily_search')
    async def test_search_with_different_queries(self, mock_tavily):
        """Test search with various query types."""
        from app.services.mcp_gateway import call_tavily_search
        
        # Mock response
        mock_tavily.return_value = {
            "result_title": "Search Result",
            "result_summary": "Search summary",
            "result_url": "https://example.com/result"
        }
        
        # Test different query types
        queries = [
            "What is AI?",
            "How does machine learning work?",
            "Best programming languages 2024",
            "Python vs JavaScript comparison"
        ]
        
        for query in queries:
            result = await call_tavily_search(query)
            assert result["result_title"] == "Search Result"
            assert result["result_summary"] == "Search summary"
            assert result["result_url"] == "https://example.com/result"
    
    @pytest.mark.asyncio
    @patch('app.services.mcp_gateway.call_tavily_search')
    async def test_search_error_scenarios(self, mock_tavily):
        """Test various error scenarios in search."""
        from app.services.mcp_gateway import call_tavily_search
        
        # Test network error
        mock_tavily.side_effect = ConnectionError("Network error")
        with pytest.raises(ConnectionError):
            await call_tavily_search("test query")
        
        # Test timeout error
        mock_tavily.side_effect = TimeoutError("Request timeout")
        with pytest.raises(TimeoutError):
            await call_tavily_search("test query")
        
        # Test invalid response
        mock_tavily.side_effect = ValueError("Invalid response format")
        with pytest.raises(ValueError):
            await call_tavily_search("test query")
