from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime

class HistoryResponse(BaseModel):
    """Schema for history item response"""
    id: int
    user_id: int
    type: str  # 'search' or 'image'
    prompt: str
    result_title: Optional[str] = None
    result_summary: Optional[str] = None
    result_url: Optional[str] = None
    extra_data: Optional[Dict[str, Any]] = None
    is_hidden: bool = False
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class HistoryUpdate(BaseModel):
    """Schema for updating history items"""
    result_title: Optional[str] = None
    result_summary: Optional[str] = None
    is_hidden: Optional[bool] = None

class HistoryFilter(BaseModel):
    """Schema for filtering history items"""
    type_filter: Optional[str] = Field(None, description="Filter by type: 'search' or 'image'")
    date_from: Optional[str] = Field(None, description="Filter from date (YYYY-MM-DD)")
    date_to: Optional[str] = Field(None, description="Filter to date (YYYY-MM-DD)")
    keyword: Optional[str] = Field(None, description="Search in prompt or result_title")
    include_hidden: bool = False

class DashboardStats(BaseModel):
    """Schema for dashboard statistics"""
    total_searches: int
    total_images: int
    recent_searches: int  # Last 7 days
    recent_images: int    # Last 7 days
    period_days: int      # Total period for stats
