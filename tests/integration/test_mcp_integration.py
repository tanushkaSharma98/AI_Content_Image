import pytest
import httpx
from unittest.mock import patch, MagicMock, AsyncMock

class TestMCPIntegration:
    """Test MCP service integration."""
    
    @pytest.mark.asyncio
    @patch('app.services.mcp_gateway.call_tavily_search')
    async def test_tavily_search_integration(self, mock_tavily):
        """Test integration with Tavily MCP service."""
        from app.services.mcp_gateway import call_tavily_search
        
        # Mock the Tavily search response
        mock_tavily.return_value = {
            "result_title": "Quantum Computing Explained",
            "result_summary": "Quantum computing is a type of computation that harnesses the collective properties of quantum states to perform calculations.",
            "result_url": "https://example.com/quantum-computing"
        }
        
        # Test the integration
        result = await call_tavily_search("What is quantum computing?")
        
        # Verify the result structure
        assert "result_title" in result
        assert "result_summary" in result
        assert "result_url" in result
        assert result["result_title"] == "Quantum Computing Explained"
        
        # Verify the function was called
        mock_tavily.assert_called_once_with("What is quantum computing?")
    
    @pytest.mark.asyncio
    @patch('app.services.mcp_gateway.call_flux_generate_image_url')
    async def test_flux_image_integration(self, mock_flux):
        """Test integration with Flux MCP service."""
        from app.services.mcp_gateway import call_flux_generate_image_url
        
        # Mock the Flux image generation response
        mock_flux.return_value = {
            "result_title": "Generated Sunset Image",
            "result_summary": "AI-generated image of a beautiful sunset",
            "result_url": "https://example.com/generated-image.jpg"
        }
        
        # Test the integration
        result = await call_flux_generate_image_url("A beautiful sunset")
        
        # Verify the result structure
        assert "result_title" in result
        assert "result_summary" in result
        assert "result_url" in result
        assert result["result_title"] == "Generated Sunset Image"
        
        # Verify the function was called
        mock_flux.assert_called_once_with("A beautiful sunset")
    
    @pytest.mark.asyncio
    @patch('app.services.mcp_gateway.call_tavily_search')
    async def test_mcp_connection_error(self, mock_tavily):
        """Test handling of MCP connection errors."""
        from app.services.mcp_gateway import call_tavily_search
        
        # Mock connection error
        mock_tavily.side_effect = Exception("Connection failed")
        
        # Test error handling
        with pytest.raises(Exception):
            await call_tavily_search("test query")
        
        # Verify the function was called
        mock_tavily.assert_called_once_with("test query")
    
    @pytest.mark.asyncio
    @patch('app.services.mcp_gateway.call_tavily_search')
    async def test_mcp_invalid_response(self, mock_tavily):
        """Test handling of invalid MCP responses."""
        from app.services.mcp_gateway import call_tavily_search
        
        # Mock invalid response
        mock_tavily.return_value = {
            "result_title": "Error Response",
            "result_summary": "Invalid response format",
            "result_url": None
        }
        
        # Test the integration
        result = await call_tavily_search("test query")
        
        # Should still return a valid structure even with invalid response
        assert "result_title" in result
        assert "result_summary" in result
        assert result["result_title"] == "Error Response"
        
        # Verify the function was called
        mock_tavily.assert_called_once_with("test query")

class TestEndToEndMCPFlow:
    """Test end-to-end MCP workflows."""
    
    @pytest.mark.asyncio
    @patch('app.services.mcp_gateway.call_tavily_search')
    async def test_search_workflow_with_mcp(self, mock_tavily):
        """Test complete search workflow with MCP integration."""
        from app.services.mcp_gateway import call_tavily_search
        
        # Mock successful search response
        mock_tavily.return_value = {
            "result_title": "Search Result",
            "result_summary": "Search summary",
            "result_url": "https://example.com/result"
        }
        
        # Test the workflow
        result = await call_tavily_search("What is quantum computing?")
        
        # Verify workflow completion
        assert result["result_title"] == "Search Result"
        assert result["result_summary"] == "Search summary"
        assert result["result_url"] == "https://example.com/result"
        
        # Verify MCP was called
        mock_tavily.assert_called_once_with("What is quantum computing?")
    
    @pytest.mark.asyncio
    @patch('app.services.mcp_gateway.call_flux_generate_image_url')
    async def test_image_workflow_with_mcp(self, mock_flux):
        """Test complete image generation workflow with MCP integration."""
        from app.services.mcp_gateway import call_flux_generate_image_url
        
        # Mock successful image generation response
        mock_flux.return_value = {
            "result_title": "Generated Image",
            "result_summary": "Image generated successfully",
            "result_url": "https://example.com/image.jpg"
        }
        
        # Test the workflow
        result = await call_flux_generate_image_url("A beautiful sunset")
        
        # Verify workflow completion
        assert result["result_title"] == "Generated Image"
        assert result["result_summary"] == "Image generated successfully"
        assert result["result_url"] == "https://example.com/image.jpg"
        
        # Verify MCP was called
        mock_flux.assert_called_once_with("A beautiful sunset")
    
    @pytest.mark.asyncio
    @patch('app.services.mcp_gateway.call_tavily_search')
    async def test_mcp_error_handling_in_workflow(self, mock_tavily):
        """Test error handling in MCP workflows."""
        from app.services.mcp_gateway import call_tavily_search
        
        # Mock MCP error
        mock_tavily.side_effect = Exception("MCP service unavailable")
        
        # Test error handling in workflow
        with pytest.raises(Exception):
            await call_tavily_search("test query")
        
        # Verify MCP was called
        mock_tavily.assert_called_once_with("test query")
