import pytest
from src.utils.kg.kg_builder import build_baseball_kg
from src.models.socratic_engine import generate_question

# --------- Test Cases ---------
def test_question_generation():
    G = build_baseball_kg()
    questions = generate_question("Shortstop", "GameState_2outs_Runner1", G)
    assert any("responsibility" in q.lower() for q in questions)
