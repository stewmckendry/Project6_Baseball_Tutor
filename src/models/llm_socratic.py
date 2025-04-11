import re
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


def evaluate_answer_with_llm(payload: dict) -> dict:
    system_prompt = "You are a smart and encouraging baseball coach helping a young player reason through a defensive play."
    concepts = payload.get("concepts", [])
    user_prompt = f"""
The player is a {payload['position']}.
The situation is: {payload['game_state']}.
Relevant concepts: {', '.join(concepts)}

Here is the conversation so far:
{payload['conversation_history']}

They just gave this answer: "{payload['player_answer']}"

Recommended actions:
{', '.join(payload['recommended_actions'])}

Explanation:
{payload['explanation']}

Evaluate the player's latest answer. Either confirm if it's correct, or guide them with a helpful Socratic question.

Be sure to carry forward the original intent of the play. Give credit if the player's answer aligns with either the original or your follow-up prompts.

End your response with: [CORRECT], [PARTIAL], or [INCORRECT]
""".strip()
    
    logger.info("Evaluating answer with LLM...")
    logger.debug(f"LLM Evaluation User prompt: {user_prompt}")
    feedback = call_openai_chat(system_prompt, user_prompt, model="gpt-4")
    logger.info("LLM evaluation completed successfully.")
    
    # Extract tag
    match = re.search(r"\[(CORRECT|PARTIAL|INCORRECT)\]", feedback.upper())
    evaluation = match.group(1).lower() if match else "unknown"

    return {
        "evaluation": evaluation,  
        "llm_feedback": feedback
    }

