import os
import json
from datetime import datetime
from pathlib import Path

# Get the project root (assumes this script is in src/ or notebooks/ folder)
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent  # Adjust as needed
LOG_DIR = PROJECT_ROOT / "logs/conversations"
LOG_DIR.mkdir(parents=True, exist_ok=True)

def log_conversation_turn(position: str, game_state: str, turn_data: dict, recommended_actions: list[str]):
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    filename = LOG_DIR / f"{timestamp}.jsonl"

    entry = {
        "timestamp": timestamp,
        "position": position,
        "game_state": game_state,
        "recommended_actions": recommended_actions,
        **turn_data  # includes turn number, question, answer, feedback, eval
    }

    with open(filename, "a") as f:
        f.write(json.dumps(entry) + "\n")

def print_latest_log(max_lines: int = 10):
    logs = sorted(LOG_DIR.glob(f"*.jsonl"), reverse=True)
    if not logs:
        print("No logs found for player.")
        return

    latest_log = logs[0]
    print(f"\n🧾 Log File: {latest_log.name}\n")

    with open(latest_log) as f:
        for i, line in enumerate(f):
            if i >= max_lines:
                break
            data = json.loads(line)
            print(f"Turn {data['turn']}:")
            print(f"  🧠 Question: {data['question']}")
            print(f"  🧒 Answer: {data['answer']}")
            print(f"  ✅ Eval: {data['eval']}")
            print(f"  🔁 Feedback: {data['feedback']}")
            print(f"  📋 Recommended: {data['recommended_actions']}")
            print("")


def log_conversation_session(position: str, game_state: str, recommended_actions: list[str], conversation: list[dict], concepts: list[str], outcome: str):
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    filename = LOG_DIR / f"{timestamp}.json"

    log_data = {
        "timestamp": timestamp,
        "position": position,
        "game_state": game_state,
        "recommended_actions": recommended_actions,
        "conversation": conversation,
        "concepts": concepts,
        "outcome": outcome  # "correct" or "3 strikes"
    }

    with open(filename, "w") as f:
        json.dump(log_data, f, indent=2)