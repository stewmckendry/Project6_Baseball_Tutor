import os
from openai import OpenAI, OpenAIError
from dotenv import load_dotenv
from src.utils.logging.logging import setup_logger

logger = setup_logger()

# Load environment
logger.info("🔧 Loading environment variables...")
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    logger.error("❌ OPENAI_API_KEY not found in environment.")
    raise OpenAIError("❌ OPENAI_API_KEY is required but not set.")

client = OpenAI(api_key=api_key)
logger.info("✅ OpenAI client initialized.")

def call_openai_chat(system_prompt, user_prompt, model="gpt-3.5-turbo", temperature=0.7):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=temperature,
        )
        content = response.choices[0].message.content.strip()

        # Log usage if available
        usage = getattr(response, "usage", None)
        if usage:
            logger.info(f"[OpenAI] Tokens used - Prompt: {usage.prompt_tokens}, "
                        f"Completion: {usage.completion_tokens}, Total: {usage.total_tokens}")

        return content

    except Exception as e:
        logger.error(f"💥 OpenAI API call failed: {e}")
        raise
