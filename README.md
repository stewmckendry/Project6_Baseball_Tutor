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

📝 Logs
Logs are stored in logs/app.log
Tail logs in real time:
tail -f logs/app.log

🧪 Run the test suite
pytest
Make sure you're in the project root when running tests.

📁 Project Structure

src/
  client/        # Streamlit UI
  server/        # (Coming soon) FastAPI backend
  utils/         # Knowledge graph, logger, etc.
  models/        # LLM wrappers and inference
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
