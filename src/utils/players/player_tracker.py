import os
import json
from datetime import datetime

from src.utils.logging.logging import setup_logger
logger = setup_logger()

logger.info("Initializing player tracker...")
PLAYER_DIR = "data/players"
os.makedirs(PLAYER_DIR, exist_ok=True)

def load_player(player_name):
    path = os.path.join(PLAYER_DIR, f"{player_name}.json")
    if os.path.exists(path):
        logger.info(f"Loading player data for {player_name} from {path}")
        with open(path, "r") as f:
            logger.info("Player data loaded successfully.")
            return json.load(f)
    else:
        logger.warning(f"Player {player_name} not found, creating new player data.")
        logger.info("Creating new player data for player: {}".format(player_name))
        return {
            "name": player_name,
            "history": [],
            "mastered_concepts": [],
            "struggled_concepts": [],
            "last_active": None,
        }

def save_player(player_data):
    logger.info(f"Saving player data for {player_data['name']} to {PLAYER_DIR}")
    player_data["last_active"] = datetime.utcnow().isoformat()
    path = os.path.join(PLAYER_DIR, f"{player_data['name']}.json")
    with open(path, "w") as f:
        json.dump(player_data, f, indent=2)
        logger.info("Player data saved successfully.")

def log_concepts(player_data, game_state, position, concepts):
    logger.info(f"Logging concepts for player {player_data['name']}...")
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "game_state": game_state,
        "position": position,
        "concepts": concepts
    }
    player_data["history"].append(entry)
    logger.info(f"Logged concepts: {entry}")

    # Optional: update mastery/trouble logic
    for concept in concepts:
        if concept not in player_data["mastered_concepts"]:
            player_data["mastered_concepts"].append(concept)
    logger.info(f"Updated mastered concepts: {player_data['mastered_concepts']}")
    
    return player_data

