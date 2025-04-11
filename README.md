# ⚾ Socratic Sports Coach

An interactive, AI + Knowledge Graph-powered app to help kids learn situational baseball reasoning — powered by Socratic questions, visual playbooks, and adaptive coaching.

---

## 🚀 Getting Started

### 🔧 Set up environment

```bash
pip install -r requirements.txt

If using .env for OpenAI API key:

echo "OPENAI_API_KEY=sk-..." > .env

🧠 Run the Streamlit app
streamlit run src/client/app.py

🧠 Run the FastAPI backend

uvicorn src.server.main:app --reload
By default, the server runs at http://127.0.0.1:8000

Test it using:

Health check: http://127.0.0.1:8000/health
Swagger UI: http://127.0.0.1:8000/docs
Example request to /question:
{
  "player_name": "alex",
  "position": "Shortstop",
  "game_state": "GameState_2outs_Runner1"
}


📝 Logs
Logs are stored in logs/app.log
Tail logs in real time:
tail -f logs/app.log

Conversation logs are saved in:

logs/conversations/
Each file captures the full turn-by-turn flow of a single play session, including:

Position & game state
Concepts involved
All coach/player turns
Outcome (correct / 3 strikes)

🧪 Run the test suite
pytest
Make sure you're in the project root when running tests.

## 👤 Player Tracking

Player profiles are stored as JSON files in:

data/players/{player_name}.json

Each profile includes:

- History of situations seen
- Concepts logged (e.g., "Force Out", "Cutoff Throw")
- Last active time

This enables:
- Adaptive questioning in the future
- Progress visualization
- Coach insight into learning patterns

📁 Project Structure

src/
  client/        # Streamlit app
  server/        # FastAPI app
  utils/         # KG builder, logger, player tracking
  models/        # LLM question generation
  ...
data/            # Structured KG data, inputs
docs/            # Architecture, planning notes
notebooks/       # Jupyter exploration
outputs/         # Reports, future game logs
test/            # Unit tests

🧭 Roadmap

- Knowledge graph engine
- Socratic question generator
- Streamlit interactive UI
- Visualize KG
- Learning tracker (player model)
- FastAPI backend for coach/LLM APIs
- Deployment (Azure or Hugging Face Spaces)
