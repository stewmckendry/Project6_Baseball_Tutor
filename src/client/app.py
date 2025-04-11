import streamlit as st
import sys
import os
import requests
from dotenv import load_dotenv

# Local imports
sys.path.append(os.path.abspath('.'))
from src.utils.kg.kg_loader import load_kg_from_yaml
from src.utils.output.graph_viz import visualize_graph
from src.models.socratic_engine import get_rich_context
from src.models.llm_socratic import build_llm_prompt_from_context
from src.utils.players.player_tracker import load_player, save_player
from src.utils.output.formatting import pretty_game_state
from src.models.evaluate_answers import evaluate_answer
from src.utils.logging.logging import setup_logger

logger = setup_logger()
load_dotenv()

API_URL = "http://localhost:8000"

st.title("⚾ Socratic Sports Coach")

# Initialize session state
if "asked" not in st.session_state:
    st.session_state.asked = False
if "llm_question" not in st.session_state:
    st.session_state.llm_question = ""
if "context" not in st.session_state:
    st.session_state.context = {}

# Player setup
player_name = st.text_input("Enter Player Name:", value="alex")
player_data = load_player(player_name)

# Load KG
graph = load_kg_from_yaml("batch_situations.yaml")

# Position and game state selectors
positions = sorted({
    u for u, v, d in graph.edges(data=True)
    if d.get("predicate") == "hasResponsibilityIn"
})
raw_game_states = sorted({
    v for u, v, d in graph.edges(data=True)
    if d.get("predicate") == "hasResponsibilityIn"
})
game_state_map = {
    pretty_game_state(gs): gs for gs in sorted(raw_game_states)
}

position = st.selectbox("Select Your Position", sorted(p.title() for p in positions))
pretty_gs = st.selectbox("Select the Game Situation", sorted(game_state_map.keys()))
game_state = game_state_map[pretty_gs]

# Ask Question
if st.button("Ask Me a Question!"):
    try:
        payload = {
            "player_name": player_name,
            "position": position,
            "game_state": game_state,
        }
        res = requests.post(f"{API_URL}/question", json=payload)
        res.raise_for_status()
        data = res.json()

        st.session_state.asked = True
        st.session_state.llm_question = data["llm_question"]
        st.session_state.context = get_rich_context(position, game_state, graph)
    
    except requests.RequestException as e:
        logger.error(f"API error: {e}")
        st.error("There was an issue connecting to the backend.")
    except Exception as e:
        logger.exception("Unexpected error")
        st.error(f"An error occurred: {e}")

# Show question + answer box after question has been asked
if st.session_state.asked:
        st.subheader("🧠 Smart Coach Says...")
        st.markdown(f"**{st.session_state.llm_question}**")

        # Answer input
        player_answer = st.text_input("Your answer:")

        if st.button("Submit Answer"):
            if not player_answer.strip():
                st.warning("Please enter an answer.")
            else:
                actions = [a["action"] for a in st.session_state.context["recommended_actions"]]
                result = evaluate_answer(player_answer, actions)

                if result["is_correct"]:
                    st.success("✅ Nice play! That’s a solid decision.")
                else:
                    st.info(f"🤔 Hmm... What about: **{result['best_match']}**?")
                    st.caption("Tip: Consider the base runners and number of outs.")
