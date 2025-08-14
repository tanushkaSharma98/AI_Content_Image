import asyncio
import sys
import os

# Add the app directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from services.mcp_gateway import call_tavily_search

async def test_dynamic_search():
    print("🔍 Dynamic Tavily MCP Search Test")
    print("=" * 50)
    print("Enter any search query and get results from Tavily MCP!")
    print("Type 'quit' to exit")
    print("=" * 50)
    
    while True:
        try:
            # Get user input
            query = input("\n🔍 Enter your search query: ").strip()
            
            if query.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
            
            if not query:
                print("❌ Please enter a valid query!")
                continue
            
            print(f"\n🚀 Searching for: '{query}'")
            print("⏳ Please wait...")
            
            # Call Tavily MCP
            result = await call_tavily_search(query)
            
            if result.get("success"):
                print("✅ SUCCESS! Tavily MCP Response:")
                print("-" * 40)
                
                content = result.get("content", "")
                if content:
                    try:
                        # Try to parse as JSON for better formatting
                        import json
                        data = json.loads(content)
                        print(f"📝 Query: {data.get('query', 'N/A')}")
                        print(f"📊 Results count: {len(data.get('results', []))}")
                        
                        if data.get('results'):
                            for i, result_item in enumerate(data['results'][:3], 1):  # Show first 3 results
                                print(f"\n🔗 Result {i}:")
                                print(f"   📌 Title: {result_item.get('title', 'N/A')}")
                                print(f"   🌐 URL: {result_item.get('url', 'N/A')}")
                                summary = result_item.get('summary', 'N/A')
                                if len(summary) > 200:
                                    summary = summary[:200] + "..."
                                print(f"   📄 Summary: {summary}")
                    except json.JSONDecodeError:
                        # If not JSON, display as text
                        print(f"📄 Content: {content[:500]}...")
                else:
                    print("📄 Raw result:", result.get("raw_result", "No content"))
            else:
                print("❌ Search failed!")
                print(f"Error: {result.get('error', 'Unknown error')}")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_dynamic_search())
