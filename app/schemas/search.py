from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class SearchRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=500)

class SearchResult(BaseModel):
    title: Optional[str] = None
    url: Optional[str] = None
    summary: Optional[str] = None
    content: Optional[str] = None

class SearchResponse(BaseModel):
    query: str
    results: List[SearchResult] = []
    summary: Optional[str] = None
    timestamp: Optional[str] = None
    saved_item_id: Optional[int] = None
    total_results: int = 0 
