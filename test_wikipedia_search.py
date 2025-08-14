import asyncio
import httpx
import json

async def test_wikipedia_search():
    print("Testing real Wikipedia search...")
    
    # Test queries
    test_queries = [
        "who is anil ambani",
        "what is quantum computing",
        "capital of gujarat"
    ]
    
    async with httpx.AsyncClient() as client:
        for query in test_queries:
            print(f"\n=== Testing query: {query} ===")
            
            # Use Wikipedia API to get real information
            url = "https://en.wikipedia.org/api/rest_v1/page/summary/"
            search_query = query.replace(" ", "_")
            
            try:
                response = await client.get(f"{url}{search_query}")
                
                if response.status_code == 200:
                    data = response.json()
                    extract = data.get("extract", "")
                    title = data.get("title", query)
                    content_url = data.get("content_urls", {}).get("desktop", {}).get("page", "")
                    
                    print(f"✅ Title: {title}")
                    print(f"✅ URL: {content_url}")
                    print(f"✅ Summary: {extract[:300]}...")
                    
                    # Create structured response
                    search_content = {
                        "query": query,
                        "results": [
                            {
                                "title": title,
                                "url": content_url,
                                "summary": extract,
                                "content": extract
                            }
                        ],
                        "summary": extract,
                        "timestamp": "2024-01-01T12:00:00Z"
                    }
                    
                    print(f"✅ Structured response created successfully")
                    
                else:
                    print(f"❌ Direct search failed, trying general search...")
                    
                    # Try general search
                    search_url = f"https://en.wikipedia.org/w/api.php?action=opensearch&search={query}&limit=3&namespace=0&format=json"
                    search_response = await client.get(search_url)
                    
                    if search_response.status_code == 200:
                        search_data = search_response.json()
                        titles = search_data[1] if len(search_data) > 1 else []
                        urls = search_data[3] if len(search_data) > 3 else []
                        
                        if titles:
                            first_title = titles[0]
                            first_url = urls[0] if urls else f"https://en.wikipedia.org/wiki/{first_title.replace(' ', '_')}"
                            
                            print(f"✅ Found via search: {first_title}")
                            print(f"✅ URL: {first_url}")
                            
                            # Get detailed info
                            detail_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{first_title.replace(' ', '_')}"
                            detail_response = await client.get(detail_url)
                            
                            if detail_response.status_code == 200:
                                detail_data = detail_response.json()
                                detail_extract = detail_data.get("extract", "")
                                print(f"✅ Summary: {detail_extract[:300]}...")
                            else:
                                print(f"❌ Could not get detailed info")
                        else:
                            print(f"❌ No search results found")
                    else:
                        print(f"❌ Search failed")
                        
            except Exception as e:
                print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_wikipedia_search())


