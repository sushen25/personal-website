"""
FastAPI application entry point for serverless deployment.
Handles AI chat requests, blog queries, and portfolio information.
"""

from fastapi import FastAPI
from mangum import Mangum
import os

from src.handlers import chat, blog
from src.middleware.error_handler import add_exception_handlers

# Initialize FastAPI app
app = FastAPI(
    title="Portfolio Backend API",
    description="Serverless backend for portfolio website with AI chatbot",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    redirect_slashes=False,  # Disable automatic slash redirects
)

# Note: CORS is handled by Lambda Function URL configuration in serverless.yml
# No need for FastAPI CORSMiddleware when using Lambda Function URLs

# Add exception handlers
add_exception_handlers(app)

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring."""
    return {
        "status": "healthy",
        "service": "portfolio-backend",
        "version": "1.0.0",
        "environment": os.getenv("STAGE", "dev"),
    }

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Portfolio Backend API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
    }

# Include routers
app.include_router(chat.router, prefix="/api/chat", tags=["chat"])
app.include_router(blog.router, prefix="/api/blog", tags=["blog"])

# Mangum handler for AWS Lambda
handler = Mangum(app, lifespan="off")
