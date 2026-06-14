from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import init_db
from app.api import chat, books, characters, plots, search

# Initialize FastAPI app
app = FastAPI(
    title="Book Series AI Planner API",
    description="Advanced AI environment for planning and writing book series",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database
@app.on_event("startup")
async def startup():
    init_db()

# Include routers
app.include_router(chat.router, prefix="/api/chat", tags=["Chat"])
app.include_router(books.router, prefix="/api/books", tags=["Books"])
app.include_router(characters.router, prefix="/api/characters", tags=["Characters"])
app.include_router(plots.router, prefix="/api/plots", tags=["Plots"])
app.include_router(search.router, prefix="/api/search", tags=["Search"])

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Book Series AI Planner API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health():
    return {"status": "healthy"}
