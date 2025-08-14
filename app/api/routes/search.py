from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List
import json

from app.db.base import get_db
from app.db.models.user import User
from app.db.models.history import History
from app.api.deps import get_current_active_user
from app.schemas.search import SearchRequest, SearchResponse, SearchResult
from app.services.mcp_gateway import call_tavily_search, MCPGatewayError

router = APIRouter(prefix="/search", tags=["search"])

@router.post("/", response_model=SearchResponse)
async def search_web(
    payload: SearchRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    try:
        raw = await call_tavily_search(payload.query)
        print(f"DEBUG: Search raw response: {raw}")
        
        # Normalize to SearchResponse shape
        results: List[SearchResult] = []
        summary = None
        timestamp = datetime.utcnow().isoformat()

        # Try known shapes first
        if isinstance(raw, dict):
            # Try to parse content if it's a JSON string
            if raw.get("content"):
                try:
                    content_data = json.loads(raw.get("content"))
                    if isinstance(content_data, dict):
                        # Extract results from the parsed content
                        if "results" in content_data and isinstance(content_data["results"], list):
                            for r in content_data["results"]:
                                results.append(SearchResult(
                                    title=r.get("title", ""),
                                    url=r.get("url", ""),
                                    summary=r.get("summary", ""),
                                    content=r.get("content", ""),
                                ))
                        if "summary" in content_data:
                            summary = content_data.get("summary")
                except (json.JSONDecodeError, TypeError):
                    pass
            
            # Also try direct fields
            if "results" in raw and isinstance(raw["results"], list):
                for r in raw["results"]:
                    results.append(SearchResult(
                        title=r.get("title", ""),
                        url=r.get("url", ""),
                        summary=r.get("summary", ""),
                        content=r.get("content", ""),
                    ))
            if "summary" in raw:
                summary = raw.get("summary")
            if "timestamp" in raw:
                timestamp = raw.get("timestamp") or timestamp
            # If text blob present (from MCP content), use as summary
            if not summary and raw.get("text"):
                summary = raw.get("text")

        # Extract proper result_title and result_summary from the response
        result_title = None
        result_summary = None
        result_url = ""
        
        if isinstance(raw, dict):
            # Try to get title from response
            if "title" in raw:
                result_title = raw.get("title")
            elif "name" in raw:
                result_title = raw.get("name")
            elif "query" in raw:
                result_title = f"Search: {raw.get('query')}"
            else:
                result_title = f"Search: {payload.query}"
            
            # Try to get summary from response
            if "summary" in raw:
                result_summary = raw.get("summary")
            elif "description" in raw:
                result_summary = raw.get("description")
            elif "text" in raw:
                result_summary = raw.get("text")
            elif "content" in raw:
                result_summary = str(raw.get("content"))
            else:
                result_summary = f"Search results for: {payload.query}"
            
            # Try to get URL from response
            if "url" in raw:
                result_url = raw.get("url")
            elif "link" in raw:
                result_url = raw.get("link")
            elif results and results[0].url:
                result_url = results[0].url

        # Save to history with extracted data
        item = History(
            user_id=current_user.id,
            type="search",
            prompt=payload.query,
            result_title=result_title or f"Search: {payload.query}",
            result_summary=result_summary or f"Search results for: {payload.query}",
            result_url=result_url,
            extra_data=raw,
        )
        db.add(item)
        db.commit()
        db.refresh(item)

        return SearchResponse(
            query=payload.query,
            results=results,
            summary=summary,
            timestamp=timestamp,
        )
    except MCPGatewayError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Tool call failed: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Search failed: {str(e)}"
        )

@router.get("/models")
async def get_search_models():
    """Get available search models"""
    return {
        "models": [
            {
                "id": "tavily-search",
                "name": "Tavily Web Search",
                "description": "Search the web for information using Tavily MCP server"
            }
        ]
    }
