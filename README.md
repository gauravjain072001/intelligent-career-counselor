# Intelligent Career Counselor

A career exploration app with local Ollama recommendations, optional OpenAI API support, and a transparent keyword-based fallback. Recommendations are exploratory, not professional assessments.

## Features
- Skill and goal assessment form
- Local LLM-generated role rationale and roadmap through Ollama
- Optional OpenAI API recommendations
- Rule-based fallback for local testing
- Personalized roadmap suggestions

## Run locally
```bash
cd career-counselor-portfolio
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Open http://localhost:5002

Install [Ollama](https://ollama.com/download/windows), then download the local model once:

```powershell
ollama pull qwen2.5:3b
```

Copy `.env.example` to `.env`, keep `LLM_PROVIDER=ollama`, and start the app. Ollama must be running locally. To use the optional paid OpenAI API instead, set `LLM_PROVIDER=openai` and add `OPENAI_API_KEY` in `.env`. The `.env` file is ignored by Git.
