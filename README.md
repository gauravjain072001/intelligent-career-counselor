# Intelligent Career Counselor

A career exploration app with optional OpenAI-compatible LLM recommendations and a transparent keyword-based fallback when no API key is configured. Recommendations are exploratory, not professional assessments.

## Features
- Skill and goal assessment form
- LLM-generated role rationale and roadmap when configured
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

To enable LLM recommendations, set `OPENAI_API_KEY` before starting the app. Optionally set `OPENAI_MODEL` (defaults to `gpt-4o-mini`). Never commit API keys.
