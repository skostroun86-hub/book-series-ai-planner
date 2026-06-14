from typing import List, Optional
from app.config import settings

class MemoryManager:
    """Manages conversation memory with intelligent context windowing"""
    
    def __init__(self):
        self.max_turns = settings.max_memory_turns
        self.chunk_size = settings.memory_chunk_size
    
    def build_context(self, messages: List) -> str:
        """Build context from conversation history"""
        if not messages:
            return ""
        
        # Keep recent messages within context window
        recent_messages = messages[-self.max_turns:]
        
        context_parts = []
        token_count = 0
        
        for msg in recent_messages:
            msg_text = f"{msg.role.upper()}: {msg.content}"
            token_count += len(msg_text.split())
            
            if token_count <= settings.context_window:
                context_parts.append(msg_text)
            else:
                break
        
        return "\n".join(context_parts)
    
    def summarize_old_messages(self, messages: List) -> str:
        """Summarize older messages that don't fit in context window"""
        # TODO: Implement LLM-based summarization
        return ""
    
    def extract_entities(self, text: str) -> dict:
        """Extract important entities from text"""
        # TODO: Extract character names, plot points, locations
        return {}
