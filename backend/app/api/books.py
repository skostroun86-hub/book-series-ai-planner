from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import Book, BookCreate, BookUpdate
from app.models import Book as BookModel
import uuid

router = APIRouter()

@router.get("/", response_model=list[Book])
async def list_books(db: Session = Depends(get_db)):
    """List all books"""
    books = db.query(BookModel).all()
    return books

@router.post("/", response_model=Book)
async def create_book(book: BookCreate, db: Session = Depends(get_db)):
    """Create new book"""
    db_book = BookModel(
        id=str(uuid.uuid4()),
        title=book.title,
        description=book.description,
        genre=book.genre,
        target_word_count=book.target_word_count
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

@router.get("/{book_id}", response_model=Book)
async def get_book(book_id: str, db: Session = Depends(get_db)):
    """Get book details"""
    book = db.query(BookModel).filter(BookModel.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.put("/{book_id}", response_model=Book)
async def update_book(
    book_id: str,
    book: BookUpdate,
    db: Session = Depends(get_db)
):
    """Update book"""
    db_book = db.query(BookModel).filter(BookModel.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    for field, value in book.dict(exclude_unset=True).items():
        setattr(db_book, field, value)
    
    db.commit()
    db.refresh(db_book)
    return db_book

@router.delete("/{book_id}")
async def delete_book(book_id: str, db: Session = Depends(get_db)):
    """Delete book"""
    db_book = db.query(BookModel).filter(BookModel.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    db.delete(db_book)
    db.commit()
    return {"message": "Book deleted"}
