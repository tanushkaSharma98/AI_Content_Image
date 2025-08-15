from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db.base import get_db, engine
from app.db.models import user, history
from app.api.routes import auth, search, image, dashboard

# Create tables
user.Base.metadata.create_all(bind=engine)
history.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Content Explorer API",
    description="A full-stack AI tool for web search and image generation",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "http://127.0.0.1:5173", "http://127.0.0.1:3000"],  # Frontend URLs
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# Include routers
app.include_router(auth.router)
app.include_router(search.router)
app.include_router(image.router)
app.include_router(dashboard.router)

@app.get("/")
async def root():
    return {"message": "AI Content Explorer API is running!"}

@app.get("/health")
async def health_check(db: Session = Depends(get_db)):
    try:
        # Test database connection
        db.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": "disconnected", "error": str(e)}

@app.get("/test-db")
async def test_db(db: Session = Depends(get_db)):
    """Test endpoint to verify database models are working"""
    try:
        # Test if we can query the database
        result = db.execute(text("SELECT version()")).fetchone()
        return {
            "message": "Database connection successful",
            "postgres_version": result[0] if result else "Unknown"
        }
    except Exception as e:
        return {"error": f"Database error: {str(e)}"}

@app.get("/debug/history")
async def debug_history(db: Session = Depends(get_db)):
    """Debug endpoint to see what's stored in the history table"""
    try:
        # Get the last 5 history entries
        history_items = db.query(history.History).order_by(history.History.created_at.desc()).limit(5).all()
        
        debug_data = []
        for item in history_items:
            debug_data.append({
                "id": item.id,
                "type": item.type,
                "prompt": item.prompt,
                "result_title": item.result_title,
                "result_summary": item.result_summary,
                "result_url": item.result_url,
                "created_at": item.created_at.isoformat() if item.created_at else None,
                "extra_data_keys": list(item.extra_data.keys()) if item.extra_data else []
            })
        
        return {
            "message": "Last 5 history entries",
            "count": len(debug_data),
            "items": debug_data
        }
    except Exception as e:
        return {"error": f"Debug error: {str(e)}"}

@app.get("/test/mcp-tavily")
async def test_mcp_tavily():
    """Test endpoint to directly call Tavily MCP and see raw response"""
    try:
        from app.services.mcp_gateway import call_tavily_search
        raw_response = await call_tavily_search("What language do indian speak?")
        return {
            "message": "Direct MCP Tavily test",
            "raw_response": raw_response,
            "response_type": type(raw_response).__name__,
            "response_keys": list(raw_response.keys()) if isinstance(raw_response, dict) else "Not a dict"
        }
    except Exception as e:
        return {"error": f"MCP test failed: {str(e)}"}

@app.get("/test/mcp-flux")
async def test_mcp_flux():
    """Test endpoint to directly call Flux MCP and see raw response"""
    try:
        from app.services.mcp_gateway import call_flux_generate_image_url
        raw_response = await call_flux_generate_image_url("a beautiful sunset")
        return {
            "message": "Direct MCP Flux test",
            "raw_response": raw_response,
            "response_type": type(raw_response).__name__,
            "response_keys": list(raw_response.keys()) if isinstance(raw_response, dict) else "Not a dict"
        }
    except Exception as e:
        return {"error": f"MCP test failed: {str(e)}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
