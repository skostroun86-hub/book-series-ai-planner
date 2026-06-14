from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # LLM Configuration
    llm_model: str = "llama2"
    ollama_api_url: str = "http://localhost:11434"
    context_window: int = 4096
    temperature: float = 0.7
    
    # Database
    database_url: str = "sqlite:///./book_planner.db"
    
    # Embeddings
    embedding_model: str = "all-MiniLM-L6-v2"
    embedding_batch_size: int = 32
    
    # Memory Management
    max_memory_turns: int = 20
    memory_chunk_size: int = 1000
    memory_summarization_threshold: int = 10
    
    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_debug: bool = False
    
    # Security
    secret_key: str = "your-secret-key-here-change-in-production"
    
    # Logging
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
