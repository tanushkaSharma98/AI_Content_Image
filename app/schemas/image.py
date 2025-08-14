from pydantic import BaseModel, Field
from typing import Optional

class ImageRequest(BaseModel):
    prompt: str = Field(..., min_length=1, max_length=1000)

class ImageResponse(BaseModel):
    prompt: str
    image_url: Optional[str] = None
    timestamp: Optional[str] = None
    saved_item_id: Optional[int] = None 
