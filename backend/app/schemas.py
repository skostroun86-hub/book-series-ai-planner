from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

# Book Schemas
class BookBase(BaseModel):
    title: str
    description: Optional[str] = None
    genre: Optional[str] = None
    target_word_count: Optional[int] = None

class BookCreate(BookBase):
    pass

class BookUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    genre: Optional[str] = None
    status: Optional[str] = None
    word_count: Optional[int] = None
    target_word_count: Optional[int] = None

class Book(BookBase):
    id: str
    status: str
    word_count: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Character Schemas
class CharacterBase(BaseModel):
    name: str
    role: Optional[str] = None
    description: Optional[str] = None
    personality: Optional[str] = None
    background: Optional[str] = None
    motivations: Optional[str] = None

class CharacterCreate(CharacterBase):
    pass

class CharacterUpdate(BaseModel):
    name: Optional[str] = None
    role: Optional[str] = None
    description: Optional[str] = None
    personality: Optional[str] = None
    background: Optional[str] = None
    motivations: Optional[str] = None
    arc: Optional[str] = None

class Character(CharacterBase):
    id: str
    arc: Optional[str]
    relationships: Optional[Dict[str, Any]]
    appearance: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Plot Schemas
class PlotPointBase(BaseModel):
    description: str
    significance: str = "medium"
    plot_thread: Optional[str] = None

class PlotPointCreate(PlotPointBase):
    book_id: str
    chapter_number: Optional[int] = None
    sequence_order: Optional[int] = None

class PlotPoint(PlotPointBase):
    id: str
    book_id: str
    chapter_number: Optional[int]
    sequence_order: Optional[int]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Message Schemas
class MessageBase(BaseModel):
    role: str  # user or assistant
    content: str

class Message(MessageBase):
    id: str
    conversation_id: str
    tokens_used: int
    created_at: datetime

    class Config:
        from_attributes = True

# Conversation Schemas
class ConversationBase(BaseModel):
    role: str = "story_architect"

class ConversationCreate(ConversationBase):
    book_id: Optional[str] = None

class Conversation(ConversationBase):
    id: str
    book_id: Optional[str]
    created_at: datetime
    updated_at: datetime
    messages: List[Message]

    class Config:
        from_attributes = True

# Chat Schemas
class ChatMessage(BaseModel):
    conversation_id: str
    message: str
    book_id: Optional[str] = None

class ChatResponse(BaseModel):
    message_id: str
    response: str
    tokens_used: int
    role: str

# Search Schemas
class SearchQuery(BaseModel):
    query: str
    limit: int = 5
    content_type: Optional[str] = None  # Filter by type

class SearchResult(BaseModel):
    content_id: str
    content_type: str
    content_text: str
    relevance_score: float
