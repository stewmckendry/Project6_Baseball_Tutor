from src.utils.kg.kg_loader import load_kg_from_yaml
from src.utils.kg.socratic_engine import get_rich_context
from src.models.llm_socratic import build_llm_prompt_from_context

def test_context_and_prompt(position: str, game_state: str, yaml_path="data/kg_situations.yaml"):
    graph = load_kg_from_yaml(yaml_path)
    context = get_rich_context(position, game_state, graph)

    print("\n📊 Context Extracted:")
    for k, v in context.items():
        print(f"{k}: {v}")

    print("\n📝 LLM Prompt:")
    prompt = build_llm_prompt_from_context(context)
    print(prompt)
