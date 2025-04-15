# ⚾ Socratic Sports Coach

An interactive, AI + Knowledge Graph-powered app that teaches kids to think like baseball players. Through Socratic questions, visual playbooks, and adaptive coaching, players learn situational awareness and baseball IQ.

---

## 🚀 Features

- 💬 Socratic Q&A based on real game scenarios
- 🧠 Knowledge graph models positions, plays, and concepts
- 👤 Player profiles track learning and history
- 🧩 Concepts like "Force Out", "Cutoff Throw", "Tag Up"
- 📈 Scoreboard gamifies learning (innings, outs, score)
- 💻 Runs locally or deploys to Azure with Docker

---

## 📦 Project Structure

```
src/
  client/        # Streamlit app (chat UI)
  server/        # FastAPI backend (coach APIs)
  models/        # LLM logic and prompts
  utils/         # KG builder, logger, player tracking
data/            # Structured KG YAML, player profiles
outputs/         # Game logs and session summaries
scripts/         # DevOps scripts (deploy, deactivate, etc.)
notebooks/       # Jupyter exploration and testing
test/            # Unit tests
```

---

## 🧠 Getting Started (Local Dev)

### 🔧 Set up environment

```bash
pip install -r requirements.txt
```

If using `.env` for OpenAI key:

```bash
echo "OPENAI_API_KEY=sk-..." > .env
```

---

### 🧪 Run the app locally

Start FastAPI backend:
```bash
uvicorn src.server.main:app --reload
```

Start Streamlit frontend:
```bash
streamlit run src/client/app.py
```

FastAPI runs at [http://localhost:8001](http://localhost:8001)  
Streamlit runs at [http://localhost:8000](http://localhost:8000)

---

### 🧪 Test API

- Health: [`/health`](http://localhost:8001/health)
- Swagger: [`/docs`](http://localhost:8001/docs)

Sample `/question` request:
```json
{
  "position": "Shortstop",
  "game_state": "GameState_2outs_Runner1"
}
```

**🧪 Run the test suite**
pytest
Make sure you're in the project root when running tests.

---

### 📝 Logging

- Live logs: `tail -f logs/app.log`
- Session logs: `logs/conversations/` — includes position, concepts, turn-by-turn chat, and outcome.

---

### 👤 Player Profiles

Stored at: `data/players/{player_name}.json`

Includes:
- History of game situations
- Concepts encountered
- Last active timestamp

---

## 🐳 Docker + Azure Deployment

This app runs in a single Docker container with both FastAPI and Streamlit.

### Build and run locally

```bash
docker build -t baseball-tutor .
docker run -p 8000:8000 baseball-tutor
```

### Deploy to Azure (via scripts)

```bash
# One-time setup of Azure resources
./scripts/setup.sh

# Build, tag, and deploy Docker image
./scripts/deploy.sh

# Stop or delete the app
./scripts/deactivate.sh

# Reactivate or re-create the app
./scripts/reactivate.sh

# Check logs, container image, and health
./scripts/status.sh

# For quick local dev push to ACR
./scripts/dev-push.sh
```

---

## 🧭 Roadmap

- ✅ Socratic Q&A engine
- ✅ Streamlit game interface
- ✅ FastAPI backend + scoring
- ✅ Logging + scoreboard
- ✅ Azure deployment (Docker)
- 🔜 Offensive situations + animations
- 🔜 Player leaderboard + coach dashboard
- 🔜 Hugging Face demo or QR-code play mode

---

## 🙌 Built With

- [Streamlit](https://streamlit.io/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [OpenAI API](https://platform.openai.com/)
- [NetworkX + PyVis](https://networkx.org/)
- [Azure App Service + ACR](https://azure.microsoft.com)

---

## 🧢 Author

Built by [Stewart McKendry](https://www.linkedin.com/in/stewartmckendry), technology strategist and youth baseball coach — combining AI + learning for good.

> _“Don’t just tell kids what to do. Teach them how to think.”_

---

## 🧠 Want to Play or Collaborate?

- [ ] Add your own KG situations in `data/batch_situations.yaml`
- [ ] Explore the Socratic engine in `src/models/llm_socratic.py`
- [ ] Share your ideas or fork the project!