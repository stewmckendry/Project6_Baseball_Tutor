from src.utils.logging.logging import setup_logger
logger = setup_logger()

def generate_question(position, game_state, graph):

    logger.info("Generating questions based on the position and game state using rules...")

    questions = []

    # u = source; v = target; d = data (edge attributes where predicate is defined in kg_builder.py)
    for u, v, d in graph.edges(data=True):
        pred = d.get("predicate")

        # Role responsibility
        if u == position and pred == "hasResponsibilityIn" and v == game_state:
            questions.append(f"As a {position}, what is your responsibility in {game_state}?")

        # Game state triggers play
        if u == game_state and pred == "triggers":
            questions.append(f"When it’s {game_state}, and the play is '{v}', what should the {position} do?")

        # Negative reasoning
        if pred == "isNotRecommended" and v == game_state:
            questions.append(f"Why might '{u}' not be the best option in {v}?")

        # Position covers base
        if u == position and pred == "covers":
            questions.append(f"Why does the {position} cover {v} in this situation?")

        # Required understanding
        if pred == "requiresUnderstandingOf":
            if u == position:
                questions.append(f"What does the {position} need to understand about '{v}'?")
            elif u == game_state:
                questions.append(f"What do you need to understand about '{v}' in the context of {game_state}?")

        if u == "GameState_2outs_Runner3" and pred == "triggers":
            questions.append(f"What should the {position} do when it's {game_state} and the play is '{v}'?")

    if not questions:
        questions.append(f"What should the {position} be thinking about in {game_state}?")

    logger.info(f"Generated {len(questions)} questions.")
    logger.info("Questions generated successfully.")

    return questions


def get_related_knowledge(position, game_state, graph):

    logger.info("Retrieving related knowledge from the graph...")

    facts = []

    for u, v, d in graph.edges(data=True):
        pred = d.get("predicate")
        if u in [position, game_state] or v in [position, game_state]:
            facts.append(f"{u} --[{pred}]--> {v}")

    logger.info(f"Found {len(facts)} related facts.")
    logger.info("Related knowledge retrieval complete.")
    
    return "; ".join(facts)


def get_rich_context(position, game_state, graph):
    context = {
        "position": position,
        "game_state": game_state,
        "play": None,
        "recommended_actions": [],
        "key_concepts": [],
        "explanation": None,
    }

    # 1. Find play node triggered by game_state
    play_node = None
    for _, v, d in graph.edges(game_state, data=True):
        if d.get("predicate") == "triggers":
            play_node = v
            context["play"] = play_node
            break

    if not play_node:
        return context  # no play found

    # 2. Get recommended actions (ordered if available)
    actions = []
    for _, v, d in graph.edges(play_node, data=True):
        if d.get("predicate") == "suggests":
            actions.append({
                "action": v,
                "order": d.get("order", 0)
            })
    context["recommended_actions"] = sorted(actions, key=lambda x: x["order"])

    # 3. Get key concepts
    concepts = [
        v for _, v, d in graph.edges(play_node, data=True)
        if d.get("predicate") == "requiresUnderstandingOf"
    ]
    context["key_concepts"] = concepts

    # 4. Get explanation + optional source
    play_attrs = graph.nodes.get(play_node, {})
    context["explanation"] = play_attrs.get("explanation")

    return context

