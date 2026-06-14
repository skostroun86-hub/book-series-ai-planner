from app.models import Character
from app.services.llm import get_llm_response
from typing import List

async def check_character_consistency(character: Character, recent_context: str) -> List[str]:
    """Check character consistency against recent context"""
    
    prompt = f"""
    Check the following character for consistency issues based on their established traits and the recent context.
    
    Character Profile:
    Name: {character.name}
    Role: {character.role}
    Personality: {character.personality}
    Background: {character.background}
    Motivations: {character.motivations}
    
    Recent context from story:
    {recent_context}
    
    List any inconsistencies or violations of established character traits.
    """
    
    response, _ = await get_llm_response(
        user_message=prompt,
        role="character_psychologist"
    )
    
    # Parse response for issues
    issues = response.split("\n")
    return [issue for issue in issues if issue.strip()]
