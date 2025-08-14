from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base


class History(Base):
    __tablename__ = "history"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    type = Column(String(20), nullable=False)  # 'search' or 'image'
    prompt = Column(Text, nullable=False)  # user input
    result_title = Column(Text, nullable=True)  # for search results
    result_summary = Column(Text, nullable=True)  # for search results
    result_url = Column(Text, nullable=True)  # search link or image URL
    extra_data = Column(JSON, nullable=True)  # extra MCP data
    is_hidden = Column(Boolean, default=False)  # for soft delete
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now()) 