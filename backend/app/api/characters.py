from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import Character, CharacterCreate, CharacterUpdate
from app.models import Character as CharacterModel
from app.services.consistency import check_character_consistency
import uuid

router = APIRouter()

@router.get("/", response_model=list[Character])
async def list_characters(db: Session = Depends(get_db)):
    """List all characters"""
    characters = db.query(CharacterModel).all()
    return characters

@router.post("/", response_model=Character)
async def create_character(char: CharacterCreate, db: Session = Depends(get_db)):
    """Create new character"""
    db_char = CharacterModel(
        id=str(uuid.uuid4()),
        name=char.name,
        role=char.role,
        description=char.description,
        personality=char.personality,
        background=char.background,
        motivations=char.motivations
    )
    db.add(db_char)
    db.commit()
    db.refresh(db_char)
    return db_char

@router.get("/{char_id}", response_model=Character)
async def get_character(char_id: str, db: Session = Depends(get_db)):
    """Get character details"""
    character = db.query(CharacterModel).filter(CharacterModel.id == char_id).first()
    if not character:
        raise HTTPException(status_code=404, detail="Character not found")
    return character

@router.put("/{char_id}", response_model=Character)
async def update_character(
    char_id: str,
    char: CharacterUpdate,
    db: Session = Depends(get_db)
):
    """Update character"""
    db_char = db.query(CharacterModel).filter(CharacterModel.id == char_id).first()
    if not db_char:
        raise HTTPException(status_code=404, detail="Character not found")
    
    for field, value in char.dict(exclude_unset=True).items():
        setattr(db_char, field, value)
    
    db.commit()
    db.refresh(db_char)
    return db_char

@router.post("/check-consistency")
async def check_consistency(
    char_id: str,
    recent_context: str,
    db: Session = Depends(get_db)
):
    """Check character consistency"""
    character = db.query(CharacterModel).filter(CharacterModel.id == char_id).first()
    if not character:
        raise HTTPException(status_code=404, detail="Character not found")
    
    issues = await check_character_consistency(character, recent_context)
    return {"character_id": char_id, "consistency_issues": issues}
