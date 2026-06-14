from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import SearchQuery, SearchResult
from app.services.rag import search_semantic

router = APIRouter()

@router.post("/semantic", response_model=list[SearchResult])
async def semantic_search(
    search_query: SearchQuery,
    db: Session = Depends(get_db)
):
    """Semantic search across all content"""
    results = await search_semantic(
        query=search_query.query,
        limit=search_query.limit,
        content_type=search_query.content_type
    )
    return results

@router.post("/characters")
async def search_characters(
    query: str,
    db: Session = Depends(get_db)
):
    """Find similar characters"""
    # TODO: Implement semantic character search
    return {"message": "Character search coming soon"}

@router.post("/plots")
async def search_plots(
    query: str,
    db: Session = Depends(get_db)
):
    """Find related plot points"""
    # TODO: Implement semantic plot search
    return {"message": "Plot search coming soon"}
