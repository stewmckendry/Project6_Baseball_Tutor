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
from src.utils.kg.kg_questiongen import get_random_situation
from src.utils.logging.convo_logging import log_conversation_turn, log_conversation_session

logger = setup_logger()
load_dotenv()

API_URL = "http://localhost:8001"

# Initialize session state
if "asked" not in st.session_state:
    st.session_state.asked = False
if "llm_question" not in st.session_state:
    st.session_state.llm_question = ""
if "context" not in st.session_state:
    st.session_state.context = {}
if "strike_count" not in st.session_state:
    st.session_state.strike_count = 0
if "conversation" not in st.session_state:
    st.session_state.conversation = []
if "evaluation_done" not in st.session_state:
    st.session_state.evaluation_done = False
if "position" not in st.session_state:
    st.session_state.position = None
if "game_state" not in st.session_state:
    st.session_state.game_state = None
if "outcome" not in st.session_state:
    st.session_state.outcome = None
if "logged_this_turn" not in st.session_state:
    st.session_state.logged_this_turn = False
if "inning" not in st.session_state:
    st.session_state.inning = 1
if "outs" not in st.session_state:
    st.session_state.outs = 0
if "score" not in st.session_state:
    st.session_state.score = 0
if "game_over" not in st.session_state:
    st.session_state.game_over = False
if "concepts" not in st.session_state:
    st.session_state.concepts = []
if "concepts_all" not in st.session_state:
    st.session_state.concepts_all = set()


st.title("⚾ Socratic Sports Coach")

# Game in progress scoreboard
if not st.session_state.game_over:
    st.markdown(f"### 🧢 Inning: {st.session_state.inning} &nbsp;&nbsp;&nbsp; ⚾ Score: {st.session_state.score} &nbsp;&nbsp;&nbsp; ❌ Outs: {st.session_state.outs}/3")
else:
    st.markdown("## 🏁 Game Over!")
    st.markdown(f"### 🧢 Final Score: {st.session_state.score} out of {st.session_state.score + st.session_state.outs} plays")
    st.markdown(f"- ✅ Correct: {st.session_state.score}")
    st.markdown(f"- ❌ Outs: {st.session_state.outs}")
    accuracy = 100 * st.session_state.score / max(1, st.session_state.score + st.session_state.outs)
    st.markdown(f"- 🎯 Accuracy: {accuracy:.1f}%")
    if st.session_state.concepts_all:
        st.markdown("### 🧠 Concepts Practiced:")
        for concept in sorted(st.session_state.concepts_all):
            st.markdown(f"- {concept}")
    st.markdown("### 📘 Want to try again?")
    if st.button("Play Again"):
        # Reset everything
        st.session_state.asked = False
        st.session_state.llm_question = ""
        st.session_state.context = {}
        st.session_state.conversation = []
        st.session_state.evaluation_done = False
        st.session_state.position = None
        st.session_state.game_state = None
        st.session_state.outcome = None
        st.session_state.concepts = []
        st.session_state.concepts_all = set()
        st.session_state.logged_this_turn = False
        st.session_state.inning = 1
        st.session_state.outs = 0
        st.session_state.score = 0
        st.session_state.game_over = False
        st.session_state.strike_count = 0
        st.rerun()


# Player setup
#player_name = st.text_input("Enter Player Name:", value="alex")
#player_data = load_player(player_name)

# Get a random question from the baseball KG
if not st.session_state.asked:
    
    try:
         # Randomly pick new (position, game_state) by calling FastAPI route
        res = requests.get(f"{API_URL}/random-situation")
        res.raise_for_status()
        data = res.json()
        st.session_state.position = data["position"]
        st.session_state.game_state = data["game_state"]

        # Get Socratic question from LLM for the given (position, game_state)
        payload = {
            #"player_name": player_name,
            "position": st.session_state.position,
            "game_state": st.session_state.game_state,
        }
        res = requests.post(f"{API_URL}/question", json=payload)
        res.raise_for_status()
        data = res.json()

        # Update session state
        st.session_state.asked = True
        st.session_state.llm_question = data["llm_question"]
        st.session_state.context = data["related_knowledge"]
        st.session_state.concepts = data["related_knowledge"].get("key_concepts", [])
        st.session_state.concepts_all.update(st.session_state.concepts)
        st.session_state.strike_count = 0
        st.session_state.evaluation_done = False

        st.session_state.conversation = [{
            "turn": 1,
            "question": data["llm_question"],
            "answer": None,
            "feedback": None,
            "eval": None
        }]
    except Exception as e:
        st.error(f"Error generating question: {e}")

# show game situation + posiiton for context of question
if st.session_state.asked:
    st.markdown("### 🧾 Here's the Situation:")
    st.markdown(f"- **Position:** {st.session_state.position}")
    st.markdown(f"- **Game State:** {st.session_state.game_state}")

    # Show chat
    st.markdown("### 💬 Conversation")
    for i, turn in enumerate(st.session_state.conversation, 1):
        logger.info(f"Turn {i}: {turn}")
        if turn.get("question"):
            st.markdown(
                f"<div style='background-color:#e8f0fe; padding:10px; border-radius:10px; margin-bottom:5px;'>"
                f"<b>🧠 Coach:</b> {turn['question']}</div>",
                unsafe_allow_html=True,
            )
        if turn.get("answer"):
            st.markdown(
                f"<div style='background-color:#fbeec1; padding:10px; border-radius:10px; margin-bottom:5px;'>"
                f"<b>🧒 You:</b> {turn['answer']}</div>",
                unsafe_allow_html=True,
            )
        if turn.get("feedback"):
            st.markdown(
                f"<div style='background-color:#dcefe2; padding:10px; border-radius:10px; margin-bottom:15px;'>"
                f"<b>🧠 Coach:</b> {turn['feedback']}</div>",
                unsafe_allow_html=True,
            )

    # Get player answer and evaluate with API call  
    if not st.session_state.evaluation_done:
        logger.info("Waiting for player answer...")
        with st.form("answer_form", clear_on_submit=True):
            player_answer = st.text_input("Your answer:", key="player_answer_input")
            submitted = st.form_submit_button("Submit Answer")

            if submitted and not st.session_state.evaluation_done:
                logger.info("Submit button clicked.")
                logger.debug(f"Player answer: {player_answer}")
                if not player_answer.strip():
                    logger.warning("Player answer is empty.")
                    st.warning("Please enter an answer.")
                else:
                    try:
                        # Compilet conversation history to feed to LLM
                        conversation_history = ""
                        for turn in st.session_state.conversation:
                            if turn.get("question"):
                                conversation_history += f"Coach: {turn['question']}\n"
                            if turn.get("answer"):
                                conversation_history += f"Player: {turn['answer']}\n"
                            if turn.get("feedback"):
                                conversation_history += f"Coach: {turn['feedback']}\n"

                        # Build payload for LLM evaluation
                        payload = {
                            #"player_name": player_name,
                            "position": st.session_state.position,
                            "game_state": st.session_state.game_state,
                            "player_answer": player_answer,
                            "recommended_actions": [a["action"] for a in st.session_state.context["recommended_actions"]],
                            "explanation": st.session_state.context["explanation"],
                            "conversation_history": conversation_history,
                            "concepts": st.session_state.concepts
                        }  

                        logger.debug(f"Payload for evaluation: {payload}")

                        response = requests.post(f"{API_URL}/evaluate_answer", json=payload)
                        response.raise_for_status()
                        result = response.json()
                        logger.info(f"Evaluation result: {result}")

                        # ⛏️ Store the answer and feedback in the conversation session variable (to be loaded into the chat)
                        st.session_state.conversation.append({
                            "turn": len(st.session_state.conversation) + 1,
                            "question": "",  # no new Socratic Q, but still a turn
                            "answer": player_answer,
                            "feedback": result["llm_feedback"],
                            "eval": result["evaluation"]
                        })

                        # Strike handling
                        if result["evaluation"] != "correct":
                            st.session_state.strike_count += 1
                            logger.info(f"Strike count: {st.session_state.strike_count}")
                        
                        # End of question-answer handling
                        if result["evaluation"] == "correct":
                            st.success("✅ You got it right!")
                            st.session_state.outcome = "correct"
                            st.session_state.evaluation_done = True
                            st.session_state.score += 1
                            logger.info("Correct answer.")
                            logger.info(f"Player answer is correct. Strike count: {st.session_state.strike_count}")
                        elif st.session_state.strike_count >= 3:
                            st.error("☠️ 3 strikes! Here's what you could have done:")
                            st.markdown(f"**Coach Explains:** {st.session_state.context['explanation']}")
                            st.session_state.evaluation_done = True
                            st.session_state.outcome = "3 strikes"
                            st.session_state.outs += 1
                            logger.info("3 strikes reached.")
                            logger.info(f"Player answer is incorrect, no more attempts. Strike count: {st.session_state.strike_count}")
                        else:
                            st.warning("Keep trying! You can do it!")
                            logger.info("Incorrect answer, but keep trying.")
                            logger.info(f"Player answer is incorrect, still more attempts. Strike count: {st.session_state.strike_count}")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error evaluating answer: {e}")


    if st.session_state.evaluation_done and not st.session_state.logged_this_turn:
        final_outcome = st.session_state.outcome
        st.markdown("### 📘 Coach Debrief")
        recommended = [a["action"] for a in st.session_state.context["recommended_actions"]]
        if recommended:
            st.markdown("**✅ Recommended Play:**")
            for action in recommended:
                st.markdown(f"- {action}")
        st.markdown(f"Why? {st.session_state.context['explanation']}")
        log_conversation_session(
            position=st.session_state.position,
            game_state=st.session_state.game_state,
            recommended_actions=[a["action"] for a in st.session_state.context["recommended_actions"]],
            conversation=st.session_state.conversation,
            concepts=st.session_state.concepts,
            outcome=final_outcome
        )
        st.session_state.logged_this_turn = True

    if st.session_state.evaluation_done:
        if st.button("Next Play"):
            # Reset session state for the next question
            st.session_state.asked = False
            st.session_state.evaluation_done = False
            st.session_state.logged_this_turn = False
            st.session_state.strike_count = 0
            st.session_state.conversation = []
            st.session_state.llm_question = ""
            st.session_state.context = {}
            st.session_state.concepts = []
            st.session_state.position = None
            st.session_state.game_state = None
            st.session_state.outcome = None

            # Check for outs and innings (3 wrong answers per inning; up to 9 innings)
            if st.session_state.outs >= 3:
                st.session_state.outs = 0
                st.session_state.inning += 1
                if st.session_state.inning > 9:
                    st.session_state.game_over = True
            
            # Get a new question
            st.rerun()




