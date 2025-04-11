import difflib

def evaluate_answer(player_answer: str, recommended_actions: list[str]) -> dict:
    normalized_answer = player_answer.strip().lower()

    # Score each recommended action by fuzzy match
    matches = [
        (action, difflib.SequenceMatcher(None, normalized_answer, action.lower()).ratio())
        for action in recommended_actions
    ]

    best_match, best_score = max(matches, key=lambda x: x[1]) if matches else ("", 0)

    return {
        "is_correct": best_score > 0.8,
        "best_match": best_match,
        "score": best_score,
        "all_matches": matches
    }
