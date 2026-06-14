from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import ChatMessage, ChatResponse, ConversationCreate, Message
from app.models import Conversation, Message as MessageModel
from app.services.llm import get_llm_response
from app.services.memory import MemoryManager
import uuid
from datetime import datetime

router = APIRouter()
memory_manager = MemoryManager()

@router.post("/message", response_model=ChatResponse)
async def send_message(
    chat_msg: ChatMessage,
    db: Session = Depends(get_db)
):
    """Send a message and get AI response with conversation memory"""
    try:
        # Get or create conversation
        conversation = db.query(Conversation).filter(
            Conversation.id == chat_msg.conversation_id
        ).first()
        
        if not conversation:
            conversation = Conversation(
                id=chat_msg.conversation_id,
                book_id=chat_msg.book_id,
                role="story_architect"
            )
            db.add(conversation)
            db.commit()
        
        # Get conversation history
        history = db.query(MessageModel).filter(
            MessageModel.conversation_id == chat_msg.conversation_id
        ).order_by(MessageModel.created_at).all()
        
        # Build context from memory
        context = memory_manager.build_context(history)
        
        # Get AI response
        response, tokens = await get_llm_response(
            user_message=chat_msg.message,
            context=context,
            role=conversation.role
        )
        
        # Store user message
        user_msg = MessageModel(
            id=str(uuid.uuid4()),
            conversation_id=chat_msg.conversation_id,
            role="user",
            content=chat_msg.message,
            tokens_used=0
        )
        db.add(user_msg)
        
        # Store assistant response
        assistant_msg = MessageModel(
            id=str(uuid.uuid4()),
            conversation_id=chat_msg.conversation_id,
            role="assistant",
            content=response,
            tokens_used=tokens
        )
        db.add(assistant_msg)
        db.commit()
        
        return ChatResponse(
            message_id=assistant_msg.id,
            response=response,
            tokens_used=tokens,
            role=conversation.role
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history/{conversation_id}")
async def get_history(
    conversation_id: str,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """Get conversation history"""
    messages = db.query(MessageModel).filter(
        MessageModel.conversation_id == conversation_id
    ).order_by(MessageModel.created_at).limit(limit).all()
    return {"messages": messages}

@router.post("/role")
async def switch_role(
    conversation_id: str,
    role: str,
    db: Session = Depends(get_db)
):
    """Switch AI role"""
    valid_roles = [
        "story_architect",
        "character_psychologist",
        "worldbuilder",
        "editor",
        "brainstormer",
        "writing_coach"
    ]
    
    if role not in valid_roles:
        raise HTTPException(status_code=400, detail=f"Invalid role. Must be one of: {valid_roles}")
    
    conversation = db.query(Conversation).filter(
        Conversation.id == conversation_id
    ).first()
    
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    conversation.role = role
    db.commit()
    
    return {"role": role, "message": f"Switched to {role} role"}

@router.post("/clear")
async def clear_conversation(
    conversation_id: str,
    db: Session = Depends(get_db)
):
    """Clear conversation memory"""
    db.query(MessageModel).filter(
        MessageModel.conversation_id == conversation_id
    ).delete()
    db.commit()
    return {"message": "Conversation cleared"}

@router.post("/new")
async def create_conversation(
    conv_create: ConversationCreate,
    db: Session = Depends(get_db)
):
    """Create new conversation"""
    conversation = Conversation(
        id=str(uuid.uuid4()),
        book_id=conv_create.book_id,
        role=conv_create.role
    )
    db.add(conversation)
    db.commit()
    return {
        "conversation_id": conversation.id,
        "role": conversation.role,
        "book_id": conversation.book_id
    }
