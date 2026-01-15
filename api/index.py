"""
FastAPI entry point for Vercel deployment
This file serves the Flask app through FastAPI for serverless deployment
"""
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os
import sys

# Add the parent directory to the path to import app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app

# Create FastAPI app
api = FastAPI(title="Campus Connect API", version="1.0.0")

# Enable CORS
api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create Flask app
flask_app = create_app()

# Mount static files
static_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")
if os.path.exists(static_path):
    api.mount("/static", StaticFiles(directory=static_path), name="static")

@api.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Campus Connect API is running", "version": "1.0.0"}

@api.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy", "service": "campus-connect"}

# Handle all Flask routes through FastAPI
@api.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def catch_all(request: Request, path: str):
    """Forward all requests to Flask app"""
    try:
        # Create WSGI environ from FastAPI request
        with flask_app.test_client() as client:
            # Get request data
            body = await request.body()
            
            # Forward request to Flask
            response = client.open(
                path=f"/{path}",
                method=request.method,
                data=body,
                headers=dict(request.headers),
                query_string=str(request.url.query).encode() if request.url.query else b""
            )
            
            # Return Flask response with proper content type handling
            if response.content_type and 'application/json' in response.content_type:
                content = response.get_json()
            elif response.content_type and 'text/html' in response.content_type:
                content = response.get_data(as_text=True)
            else:
                content = response.get_data(as_text=True)
            
            return Response(
                content=content if isinstance(content, str) else str(content),
                status_code=response.status_code,
                headers=dict(response.headers),
                media_type=response.content_type or 'text/html'
            )
    except Exception as e:
        return JSONResponse(
            content={"error": str(e)},
            status_code=500
        )

# For local development
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(api, host="0.0.0.0", port=8000)
