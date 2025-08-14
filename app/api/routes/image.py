from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
import json

from app.db.base import get_db
from app.db.models.user import User
from app.db.models.history import History
from app.api.deps import get_current_active_user
from app.schemas.image import ImageRequest, ImageResponse
from app.services.mcp_gateway import call_flux_generate_image_url, MCPGatewayError

router = APIRouter(prefix="/image", tags=["image"]) 

@router.post("/generate", response_model=ImageResponse)
async def generate_image(
    payload: ImageRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    try:
        raw = await call_flux_generate_image_url(payload.prompt)
        image_url = None
        timestamp = datetime.utcnow().isoformat()
        
        print(f"DEBUG: Raw response: {raw}")
        
        # Extract data from the response
        if isinstance(raw, dict):
            # Try to get image URL from various possible locations
            image_url = raw.get("image_url") or raw.get("url") or raw.get("link")
            
            # If not found in direct fields, try to parse from content
            if not image_url and raw.get("content"):
                try:
                    # The content might be JSON string
                    content_data = json.loads(raw.get("content"))
                    if isinstance(content_data, dict):
                        image_url = content_data.get("imageUrl") or content_data.get("image_url")
                except (json.JSONDecodeError, TypeError):
                    # If not JSON, check if content itself is a URL
                    content = raw.get("content")
                    if content and ("http" in content and ".ai" in content):
                        image_url = content
            
            # If still no URL, try to extract from raw_result
            if not image_url and raw.get("raw_result"):
                raw_result = raw.get("raw_result")
                if "imageUrl" in raw_result:
                    # Extract URL from the raw result string
                    import re
                    url_match = re.search(r'"imageUrl":\s*"([^"]+)"', raw_result)
                    if url_match:
                        image_url = url_match.group(1)
            
            if raw.get("timestamp"):
                timestamp = raw.get("timestamp")

        # Extract proper result_title and result_summary from the response
        result_title = None
        result_summary = None
        
        if isinstance(raw, dict):
            # Try to get title from response
            if "title" in raw:
                result_title = raw.get("title")
            elif "name" in raw:
                result_title = raw.get("name")
            elif "prompt" in raw:
                result_title = f"Image: {raw.get('prompt')}"
            else:
                result_title = f"Image: {payload.prompt}"
            
            # Try to get summary from response
            if "summary" in raw:
                result_summary = raw.get("summary")
            elif "description" in raw:
                result_summary = raw.get("description")
            elif "text" in raw:
                result_summary = raw.get("text")
            elif "status" in raw:
                result_summary = f"Image generation: {raw.get('status')}"
            else:
                result_summary = "AI-generated image from prompt"

        item = History(
            user_id=current_user.id,
            type="image",
            prompt=payload.prompt,
            result_title=result_title or f"Image: {payload.prompt}",
            result_summary=result_summary or "AI-generated image from prompt",
            result_url=image_url or "",
            extra_data=raw,
        )
        db.add(item)
        db.commit()
        db.refresh(item)

        return ImageResponse(
            prompt=payload.prompt,
            image_url=image_url,
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
            detail=f"Image generation failed: {str(e)}"
        )

@router.get("/models")
async def get_image_models():
    """Get available image generation models"""
    return {
        "models": [
            {
                "id": "flux-imagegen",
                "name": "Flux Image Generation",
                "description": "Generate images from text prompts using Flux MCP server"
            }
        ]
    }
