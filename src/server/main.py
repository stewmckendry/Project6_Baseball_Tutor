from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

from src.utils.kg.kg_builder import build_baseball_kg
from src.models.socratic_engine import generate_question, get_related_knowledge
from src.models.llm_socratic import generate_llm_question
from src.utils.players.player_tracker import load_player, save_player, log_concepts

from src.utils.logging.logging import setup_logger
logger = setup_logger()

logger.info("FastAPI app starting...")

app = FastAPI()
logger.info("FastAPI app started")

graph = build_baseball_kg()
logger.info("Baseball knowledge graph built successfully")


class QuestionRequest(BaseModel):
    """Request model for generating questions.  What the client sends to the server."""
    player_name: str
    position: str
    game_state: str


class LogConceptsRequest(BaseModel):
    """Request model for logging concepts.  What the client sends to the server."""
    player_name: str
    position: str
    game_state: str
    concepts: List[str]


@app.get("/health")
def health():
    logger.info("Health check endpoint called")
    return {"status": "ok"}


@app.post("/question")
def get_question(req: QuestionRequest):
    logger.info(f"Received question request for player: {req.player_name}, position: {req.position}, game_state: {req.game_state}")
    related_knowledge = get_related_knowledge(req.position, req.game_state, graph)
    static_questions = generate_question(req.position, req.game_state, graph)
    llm_question = generate_llm_question(req.position, req.game_state, related_knowledge)
    
    logger.info("Question generation completed successfully.")

    return {
        "player": req.player_name,
        "position": req.position,
        "game_state": req.game_state,
        "related_knowledge": related_knowledge,
        "questions": static_questions,
        "llm_question": llm_question,
    }


@app.post("/player/log")
def log_player(req: LogConceptsRequest):
    logger.info(f"Logging concepts for player: {req.player_name}, position: {req.position}, game_state: {req.game_state}")
    player_data = load_player(req.player_name)
    updated = log_concepts(player_data, req.game_state, req.position, req.concepts)
    save_player(updated)
    logger.info("Player concepts logged successfully.")
    return {"message": "Logged", "player": req.player_name, "concepts": req.concepts}


@app.get("/player/{name}")
def get_player(name: str):
    logger.info(f"Fetching player data for {name}")
    if not name:
        raise HTTPException(status_code=400, detail="Player name is required")
    try:
        data = load_player(name)
        logger.info("Player data fetched successfully.")
        return data
    except Exception:
        raise HTTPException(status_code=404, detail="Player not found")
