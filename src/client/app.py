import streamlit as st

import sys
import os
sys.path.append(os.path.abspath('.'))
from src.utils.kg.kg_builder import build_baseball_kg
from src.models.socratic_engine import generate_question, get_related_knowledge
from src.utils.output.graph_viz import visualize_graph
from src.models.llm_socratic import generate_llm_question
from src.utils.players.player_tracker import load_player, save_player, log_concepts

from src.utils.logging.logging import setup_logger
logger = setup_logger()
logger.info("Streamlit app started")

import requests
API_URL = "http://localhost:8000"

# Title
st.title("⚾ Socratic Sports Coach")

# Player name input
player_name = st.text_input("Enter Player Name:", value="alex")
player_data = load_player(player_name)
logger.info(f"Loaded player data for {player_name}")

# Load KG
graph = build_baseball_kg()
logger.info("Knowledge graph built successfully")

# Choose position and game state
logger.info("Choosing position and game state")
positions = sorted({u for u, _ in graph.edges() if "Base" not in u and "GameState" not in u})
game_states = sorted({v for _, v, _ in graph.edges(data=True) if "GameState" in v})

position = st.selectbox("Select Your Position", positions)
game_state = st.selectbox("Select the Game Situation", game_states)

if st.button("Ask Me a Question!"):
    logger.info(f"Generating questions for player: {player_name}, position: {position}, game_state: {game_state}")

    st.subheader("🤔 Guided Questions")
    payload = {
        "player_name": player_name,
        "position": position,
        "game_state": game_state,
    }

    try:
        logger.info(f"Sending request to API: {API_URL}/question")

        res = requests.post(f"{API_URL}/question", json=payload)
        res.raise_for_status()
        data = res.json()
        logger.info("Received response from API")
        logger.info("Guided questions generated successfully")
        for q in data["questions"]:
            st.markdown(f"• {q}")

        st.subheader("🧠 Smart Coach Says...")
        st.markdown(f"**{data['llm_question']}**")
        logger.info("LLM question generated successfully")

        # Optional: auto-log concepts (if backend exposes them in future)

        if st.button("📥 Log Concept Exposure"):
            logger.info("Logging concept exposure")
            context = data["related_knowledge"]
            concepts = [fact.split("-->")[-1].strip() for fact in context.split(";") if "requiresUnderstandingOf" in fact]
            log_payload = {
                "player_name": player_name,
                "position": position,
                "game_state": game_state,
                "concepts": concepts,
            }
            try:
                logger.info(f"Sending log request to API: {API_URL}/player/log")
                r = requests.post(f"{API_URL}/player/log", json=log_payload)
                r.raise_for_status()
                st.success("Concepts logged successfully ✅")
                logger.info("Concepts logged successfully")
            except Exception as e:
                st.error(f"Logging failed: {e}")
    
        if st.checkbox("📊 Show Player Progress"):
            try:
                logger.info(f"Fetching player data from API: {API_URL}/player/{player_name}")
                r = requests.get(f"{API_URL}/player/{player_name}")
                r.raise_for_status()
                pdata = r.json()
                st.markdown(f"**Concepts Mastered:** {pdata['mastered_concepts']}")
                st.markdown(f"**History:** Seen {len(pdata['history'])} situations")
                logger.info("Player data fetched successfully")
            except Exception as e:
                st.error(f"Failed to load player data: {e}")

    except Exception as e:
        st.error(f"Failed to get question: {e}")




