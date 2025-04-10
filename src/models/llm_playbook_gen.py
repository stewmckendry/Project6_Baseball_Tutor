from src.models.llm_openai import call_openai_chat
from src.utils.files.yaml_json import parse_yaml_output, save_json, save_yaml
from src.utils.logging.logging import setup_logger
logger = setup_logger()


def call_gpt_for_situations(user_prompt):
    logger.info("Generating LLM game situations...")
    system_prompt = "You're a smart, friendly youth baseball coach. "
    # call open AI
    try:
        response = call_openai_chat(system_prompt, user_prompt)
    except Exception as e:
        logger.error(f"💥 OpenAI API call failed: {e}")
        raise
    logger.info("Response received from OpenAI.")
    return response

def batch_generate_situations(positions, prompt_template):
    all_situations = []

    for pos in positions:
        print(f"⚾ Generating for: {pos}...")
        prompt = prompt_template.format(position=pos)
        yaml_text = call_gpt_for_situations(prompt)
        try:
            parsed = parse_yaml_output(yaml_text)
            all_situations.extend(parsed)
        except Exception as e:
            print(f"❌ Error parsing YAML for {pos}: {e}")
            continue

    return all_situations