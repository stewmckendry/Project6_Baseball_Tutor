import yaml
import networkx as nx
from pathlib import Path
from src.utils.logging.logging import setup_logger
logger = setup_logger()

# Get the project root (assumes this script is in src/ or notebooks/ folder)
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent  # Adjust as needed

def load_kg_from_yaml(filename=None) -> nx.DiGraph:

    load_path = PROJECT_ROOT / "data/game_situations" / filename if filename else PROJECT_ROOT / "data/game_situations/batch_situations.yaml"
    logger.info(f"📥 Loading knowledge graph from: {load_path}")
    
    G = nx.DiGraph()

    with open(load_path, "r") as f:
        situations = yaml.safe_load(f)
        logger.info(f"✅ Loaded {len(situations)} situations from YAML file.")
        logger.debug(f"Situations: {situations}")

    for s in situations:
        sid = s.get("situation_id", "unknown_id")
        position = s["position"]
        game_state = s["game_state"]
        play = s["play"]
        actions = s.get("recommended_actions", [])
        concepts = s.get("key_concepts", [])
        explanation = s.get("explanation", "")
        source = s.get("source", "llm") # Default to "llm" if not provided

        # Core structure
        G.add_edge(position, game_state, predicate="hasResponsibilityIn", source=source)
        G.add_edge(game_state, play, predicate="triggers", source=source)

        # Play-related edges
        for i, a in enumerate(actions):
            G.add_edge(play, a, predicate="suggests", source=source, order=i)

        for c in concepts:
            G.add_edge(play, c, predicate="requiresUnderstandingOf", source=source)

        # Set explanation on the play node
        if "explanation" in s:
            G.nodes[play]["explanation"] = explanation
        
        # Attach source of the situation
        G.nodes[play]["source"] = source

        logger.debug(f"✅ Loaded situation: {sid}")

    logger.info(f"✅ Graph loaded with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges")
    return G
