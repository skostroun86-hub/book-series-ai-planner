from sqlalchemy import Column, String, Text, DateTime, Integer, Float, Boolean, ForeignKey, Table, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
from datetime import datetime

# Association table for many-to-many relationships
book_character_association = Table(
    'book_character',
    Base.metadata,
    Column('book_id', String, ForeignKey('books.id')),
    Column('character_id', String, ForeignKey('characters.id'))
)

class Book(Base):
    __tablename__ = "books"
    
    id = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    genre = Column(String)
    status = Column(String, default="planning")  # planning, writing, editing, published
    word_count = Column(Integer, default=0)
    target_word_count = Column(Integer)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    
    # Relationships
    chapters = relationship("Chapter", back_populates="book", cascade="all, delete-orphan")
    characters = relationship("Character", secondary=book_character_association, back_populates="books")
    plot_points = relationship("PlotPoint", back_populates="book", cascade="all, delete-orphan")
    conversations = relationship("Conversation", back_populates="book", cascade="all, delete-orphan")

class Chapter(Base):
    __tablename__ = "chapters"
    
    id = Column(String, primary_key=True)
    book_id = Column(String, ForeignKey('books.id'), nullable=False)
    chapter_number = Column(Integer)
    title = Column(String)
    content = Column(Text)
    word_count = Column(Integer, default=0)
    notes = Column(Text)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    
    # Relationships
    book = relationship("Book", back_populates="chapters")

class Character(Base):
    __tablename__ = "characters"
    
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    role = Column(String)  # protagonist, antagonist, supporting, etc.
    description = Column(Text)
    personality = Column(Text)
    background = Column(Text)
    motivations = Column(Text)
    arc = Column(Text)
    relationships = Column(JSON)  # Store relationships with other characters
    appearance = Column(Text)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    
    # Relationships
    books = relationship("Book", secondary=book_character_association, back_populates="characters")

class PlotPoint(Base):
    __tablename__ = "plot_points"
    
    id = Column(String, primary_key=True)
    book_id = Column(String, ForeignKey('books.id'), nullable=False)
    chapter_number = Column(Integer)
    description = Column(Text)
    significance = Column(String)  # low, medium, high, critical
    plot_thread = Column(String)  # main, subplot, character_arc, etc.
    sequence_order = Column(Integer)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    
    # Relationships
    book = relationship("Book", back_populates="plot_points")

class Conversation(Base):
    __tablename__ = "conversations"
    
    id = Column(String, primary_key=True)
    book_id = Column(String, ForeignKey('books.id'))
    role = Column(String, default="story_architect")  # Role of AI
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    
    # Relationships
    book = relationship("Book", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")

class Message(Base):
    __tablename__ = "messages"
    
    id = Column(String, primary_key=True)
    conversation_id = Column(String, ForeignKey('conversations.id'), nullable=False)
    role = Column(String)  # user, assistant
    content = Column(Text)
    tokens_used = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())
    
    # Relationships
    conversation = relationship("Conversation", back_populates="messages")

class Embedding(Base):
    __tablename__ = "embeddings"
    
    id = Column(String, primary_key=True)
    content_id = Column(String)  # Reference to original content
    content_type = Column(String)  # chapter, note, character, plot_point
    content_text = Column(Text)
    embedding = Column(JSON)  # Store as JSON array
    created_at = Column(DateTime, server_default=func.now())
