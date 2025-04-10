import os
from openai import OpenAI, OpenAIError
from dotenv import load_dotenv

from src.utils.logging.logging import setup_logger
logger = setup_logger()


# Load the .env file
logger.info("Loading environment variables...")
load_dotenv()

# Get the API key
my_openai_api_key = os.getenv("OPENAI_API_KEY")
logger.info("API key retrieved successfully.")

# Safety check
if not my_openai_api_key:
    logger.error("❌ OPENAI_API_KEY not set. Please check your .env file or environment variables.")    
    raise OpenAIError("❌ OPENAI_API_KEY not set. Please check your .env file or environment variables.")

# Create OpenAI client
client = OpenAI(api_key=my_openai_api_key)
logger.info("OpenAI client created successfully.")

def generate_llm_question(position, game_state, related_knowledge):
    system_prompt = (
        "You're a smart, friendly youth baseball coach. "
        "You ask kids thoughtful questions to help them understand plays. "
        "Use the context to ask a clear, age-appropriate question that encourages reasoning."
    )

    user_prompt = (
        f"The player is a {position}. The situation is: {game_state}.\n"
        f"Relevant knowledge: {related_knowledge}.\n"
        "Ask one great Socratic-style question."
    )
    
    logger.info("Generating LLM question...")
    
    response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
        )
    logger.info("LLM question generated successfully.")
    logger.info(f"Prompt tokens: {response.usage.prompt_tokens}")
    logger.info(f"Completion tokens: {response.usage.completion_tokens}")

    logger.info("Returning generated question.")
    return response.choices[0].message.content.strip()
