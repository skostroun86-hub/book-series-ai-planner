import aiohttp
from app.config import settings
import json
from typing import Tuple

async def get_llm_response(
    user_message: str,
    context: str = "",
    role: str = "story_architect"
) -> Tuple[str, int]:
    """Get response from local LLM via Ollama"""
    
    # Build prompt based on role
    system_prompts = {
        "story_architect": "You are a master storyteller and plot architect. Help plan story structures, plot arcs, pacing, and narrative flow.",
        "character_psychologist": "You are an expert in character psychology. Help develop realistic, complex, and consistent characters.",
        "worldbuilder": "You are a worldbuilding expert. Help create rich, consistent, and detailed fictional worlds.",
        "editor": "You are a professional editor. Provide feedback on writing quality, clarity, grammar, and style.",
        "brainstormer": "You are a creative brainstormer. Generate fresh ideas, plot twists, and creative solutions.",
        "writing_coach": "You are a supportive writing coach. Encourage the writer and provide motivational guidance."
    }
    
    system_prompt = system_prompts.get(role, system_prompts["story_architect"])
    
    full_prompt = f"""{system_prompt}

Context from conversation history:
{context}

User message:
{user_message}"""
    
    try:
        async with aiohttp.ClientSession() as session:
            payload = {
                "model": settings.llm_model,
                "prompt": full_prompt,
                "temperature": settings.temperature,
                "stream": False
            }
            
            async with session.post(
                f"{settings.ollama_api_url}/api/generate",
                json=payload
            ) as response:
                if response.status != 200:
                    raise Exception(f"Ollama error: {response.status}")
                
                data = await response.json()
                response_text = data.get("response", "")
                tokens = data.get("eval_count", 0)
                
                return response_text, tokens
    except Exception as e:
        print(f"Error calling LLM: {e}")
        return f"Error: {str(e)}", 0
