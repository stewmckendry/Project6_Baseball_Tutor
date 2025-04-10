from src.models.llm_openai import call_openai_chat

from src.utils.logging.logging import setup_logger
logger = setup_logger()

def generate_llm_question(position, game_state, related_knowledge):
    system_prompt = (
        "You're a smart, friendly youth baseball coach. "
        "You ask kids thoughtful questions to help them understand plays. "
        "Use the context to ask a clear, age-appropriate question that encourages reasoning."
    )

    user_prompt = build_llm_prompt_from_context(position, game_state, related_knowledge)
    
    logger.info("Generating LLM question...")

    # Call the OpenAI API
    try:
        response = call_openai_chat(system_prompt, user_prompt)
    except Exception as e:
        logger.error(f"💥 OpenAI API call failed: {e}")
        raise

    logger.info("LLM question generated successfully.")
    logger.info("Returning generated question.")
    return response

def build_llm_prompt_from_context(position, game_state, context: dict) -> str:
    return f"""
The player is a {position} in the situation: {game_state}.
The play is: {context['play']}.

Recommended actions (in order):
{', '.join([a['action'] for a in context.get('recommended_actions', [])])}

Key concepts:
{', '.join(context.get('key_concepts', []))}

Explanation of the play:
{context.get('explanation', 'No explanation available.')}

Ask one thoughtful, age-appropriate Socratic question to guide the player’s decision-making.
""".strip()

