import asyncio
import httpx
import json

# Try direct HTTP calls to understand the authentication
TAVILY_BASE_URL = "https://server.smithery.ai/@Jeetanshu18/tavily-mcp/mcp"

async def test_direct_http():
    print("Testing direct HTTP calls to Tavily MCP server...")
    
    # Test different authentication headers and methods
    test_configs = [
        {
            "url": f"{TAVILY_BASE_URL}?api_key=f1f6c5a8-b3d0-4815-81c3-8fa253314e6b&profile=cautious-peafowl-9gzmmK",
            "headers": {"Accept": "application/json"}
        },
        {
            "url": f"{TAVILY_BASE_URL}?api_key=f1f6c5a8-b3d0-4815-81c3-8fa253314e6b&profile=cautious-peafowl-9gzmmK",
            "headers": {"Accept": "application/json, text/event-stream"}
        },
        {
            "url": f"{TAVILY_BASE_URL}?api_key=f1f6c5a8-b3d0-4815-81c3-8fa253314e6b&profile=cautious-peafowl-9gzmmK",
            "headers": {"Authorization": "Bearer f1f6c5a8-b3d0-4815-81c3-8fa253314e6b"}
        }
    ]
    
    async with httpx.AsyncClient() as client:
        for i, config in enumerate(test_configs):
            print(f"\n=== Testing HTTP config {i+1} ===")
            print(f"URL: {config['url']}")
            print(f"Headers: {config['headers']}")
            
            try:
                # Try a simple GET request first
                response = await client.get(config['url'], headers=config['headers'])
                print(f"GET Response Status: {response.status_code}")
                print(f"GET Response Headers: {dict(response.headers)}")
                print(f"GET Response Body: {response.text[:500]}...")
                
                # Try a POST request with MCP-like payload
                mcp_payload = {
                    "jsonrpc": "2.0",
                    "id": 1,
                    "method": "tools/list",
                    "params": {}
                }
                
                post_response = await client.post(
                    config['url'], 
                    headers={**config['headers'], "Content-Type": "application/json"},
                    json=mcp_payload
                )
                print(f"POST Response Status: {post_response.status_code}")
                print(f"POST Response Body: {post_response.text[:500]}...")
                
            except Exception as e:
                print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_direct_http())


