from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from datetime import datetime, timedelta
from typing import List, Optional
import json

from app.db.base import get_db
from app.db.models.user import User
from app.db.models.history import History
from app.api.deps import get_current_active_user
from app.schemas.dashboard import (
    HistoryResponse, 
    HistoryUpdate, 
    HistoryFilter,
    DashboardStats
)

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

@router.get("/history", response_model=List[HistoryResponse])
async def get_user_history(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    type_filter: Optional[str] = Query(None, description="Filter by type: 'search' or 'image'"),
    date_from: Optional[str] = Query(None, description="Filter from date (YYYY-MM-DD)"),
    date_to: Optional[str] = Query(None, description="Filter to date (YYYY-MM-DD)"),
    keyword: Optional[str] = Query(None, description="Search in prompt or result_title"),
    include_hidden: bool = Query(False, description="Include hidden/deleted items")
):
    """
    Get user's search and image generation history with filtering
    """
    # Build query
    query = db.query(History).filter(History.user_id == current_user.id)
    
    # Apply type filter
    if type_filter and type_filter in ['search', 'image']:
        query = query.filter(History.type == type_filter)
    
    # Apply date filters
    if date_from:
        try:
            from_date = datetime.strptime(date_from, "%Y-%m-%d")
            query = query.filter(History.created_at >= from_date)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid date_from format. Use YYYY-MM-DD"
            )
    
    if date_to:
        try:
            to_date = datetime.strptime(date_to, "%Y-%m-%d") + timedelta(days=1)
            query = query.filter(History.created_at < to_date)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid date_to format. Use YYYY-MM-DD"
            )
    
    # Apply keyword search
    if keyword:
        query = query.filter(
            or_(
                History.prompt.ilike(f"%{keyword}%"),
                History.result_title.ilike(f"%{keyword}%"),
                History.result_summary.ilike(f"%{keyword}%")
            )
        )
    
    # Apply hidden filter
    if not include_hidden:
        query = query.filter(History.is_hidden == False)
    
    # Order by created_at descending and apply pagination
    history_items = query.order_by(History.created_at.desc()).offset(skip).limit(limit).all()
    
    return history_items

@router.get("/stats", response_model=DashboardStats)
async def get_dashboard_stats(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
    days: int = Query(30, ge=1, le=365, description="Number of days to include in stats")
):
    """
    Get dashboard statistics for the user
    """
    # Calculate date range
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)
    
    # Get total counts
    total_searches = db.query(History).filter(
        and_(
            History.user_id == current_user.id,
            History.type == "search",
            History.is_hidden == False,
            History.created_at >= start_date
        )
    ).count()
    
    total_images = db.query(History).filter(
        and_(
            History.user_id == current_user.id,
            History.type == "image",
            History.is_hidden == False,
            History.created_at >= start_date
        )
    ).count()
    
    # Get recent activity (last 7 days)
    recent_start = end_date - timedelta(days=7)
    recent_searches = db.query(History).filter(
        and_(
            History.user_id == current_user.id,
            History.type == "search",
            History.is_hidden == False,
            History.created_at >= recent_start
        )
    ).count()
    
    recent_images = db.query(History).filter(
        and_(
            History.user_id == current_user.id,
            History.type == "image",
            History.is_hidden == False,
            History.created_at >= recent_start
        )
    ).count()
    
    return DashboardStats(
        total_searches=total_searches,
        total_images=total_images,
        recent_searches=recent_searches,
        recent_images=recent_images,
        period_days=days
    )

@router.get("/history/{item_id}", response_model=HistoryResponse)
async def get_history_item(
    item_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get a specific history item by ID
    """
    history_item = db.query(History).filter(
        and_(
            History.id == item_id,
            History.user_id == current_user.id
        )
    ).first()
    
    if not history_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="History item not found"
        )
    
    return history_item

@router.put("/history/{item_id}", response_model=HistoryResponse)
async def update_history_item(
    item_id: int,
    update_data: HistoryUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Update a history item (soft update - only certain fields)
    """
    history_item = db.query(History).filter(
        and_(
            History.id == item_id,
            History.user_id == current_user.id
        )
    ).first()
    
    if not history_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="History item not found"
        )
    
    # Update allowed fields
    if update_data.prompt is not None:
        history_item.prompt = update_data.prompt
    
    if update_data.result_title is not None:
        history_item.result_title = update_data.result_title
    
    if update_data.result_summary is not None:
        history_item.result_summary = update_data.result_summary
    
    if update_data.is_hidden is not None:
        history_item.is_hidden = update_data.is_hidden
    
    history_item.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(history_item)
    
    return history_item

@router.delete("/history/{item_id}")
async def delete_history_item(
    item_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Soft delete a history item (mark as hidden)
    """
    history_item = db.query(History).filter(
        and_(
            History.id == item_id,
            History.user_id == current_user.id
        )
    ).first()
    
    if not history_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="History item not found"
        )
    
    # Soft delete
    history_item.is_hidden = True
    history_item.updated_at = datetime.utcnow()
    
    db.commit()
    
    return {"message": "History item deleted successfully"}

@router.delete("/history/bulk")
async def bulk_delete_history(
    item_ids: List[int],
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Bulk soft delete history items
    """
    if not item_ids:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No item IDs provided"
        )
    
    # Get items that belong to the user
    history_items = db.query(History).filter(
        and_(
            History.id.in_(item_ids),
            History.user_id == current_user.id
        )
    ).all()
    
    if not history_items:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No valid history items found"
        )
    
    # Soft delete all items
    for item in history_items:
        item.is_hidden = True
        item.updated_at = datetime.utcnow()
    
    db.commit()
    
    return {
        "message": f"Successfully deleted {len(history_items)} history items",
        "deleted_count": len(history_items)
    }
