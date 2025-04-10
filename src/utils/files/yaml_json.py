import yaml
from pathlib import Path
import re
import json

# Get the project root (assumes this script is in src/ or notebooks/ folder)
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent  # Adjust as needed

def parse_yaml_output(yaml_text):
    # Step 1: Remove markdown code fences
    lines = yaml_text.strip().splitlines()
    lines = [line for line in lines if not line.strip().startswith("```")]

    # Step 2: Strip preamble before first list item
    match = re.search(r"^(-\s+.+)", "\n".join(lines), re.MULTILINE)
    if match:
        lines = lines[match.start():]

    cleaned_text = "\n".join(lines)

    # Step 3: Stop parsing at first non-YAML sentence (e.g. LLM summary line)
    cutoff_index = None
    for i, line in enumerate(cleaned_text.splitlines()):
        if line.strip().startswith("These are") or re.match(r"^[A-Z].*\.$", line.strip()):
            cutoff_index = i
            break

    if cutoff_index is not None:
        cleaned_text = "\n".join(cleaned_text.splitlines()[:cutoff_index])

    return yaml.safe_load(cleaned_text)

def save_yaml(data, filename=None):
    save_path = PROJECT_ROOT / "data/game_situations" / filename if filename else PROJECT_ROOT / "data/game_situations/kg_situations.yaml"
    save_path.parent.mkdir(parents=True, exist_ok=True)
    with open(save_path, "w") as f:
        yaml.dump(data, f, sort_keys=False)

def save_json(data, filename=None):
    save_path = PROJECT_ROOT / "data/game_situations" / filename if filename else PROJECT_ROOT / "data/game_situations/kg_situations.json"
    save_path.parent.mkdir(parents=True, exist_ok=True)
    with open(save_path, "w") as f:
        json.dump(data, f, indent=2)