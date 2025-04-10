def pretty_game_state(gs: str) -> str:
    # Capitalize first letter of each segment
    parts = gs.split(", ")
    parts = [part.capitalize() for part in parts]
    return ", ".join(parts)
