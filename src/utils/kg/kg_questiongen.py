import random

def get_random_situation(graph):
    """Return a random (position, game_state) pair based on KG edges."""
    edges = [
        (u, v) for u, v, d in graph.edges(data=True)
        if d.get("predicate") == "hasResponsibilityIn"
    ]
    return random.choice(edges)  # returns (position, game_state)
