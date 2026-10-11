import json
import os
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


def score_role(role, skills, interests, goals):
    score = 0
    text = " ".join([skills, interests, goals]).lower()
    role_keywords = {
        "AI Engineer": ["python", "ml", "ai", "machine learning", "data", "model"],
        "Product Manager": ["product", "strategy", "planning", "research", "ux", "roadmap"],
        "Data Analyst": ["analysis", "sql", "dashboard", "data", "reporting", "insights"],
        "Frontend Engineer": ["ui", "ux", "design", "javascript", "react", "frontend", "web"],
        "Backend Engineer": ["api", "database", "system design", "backend", "scalability", "server"],
    }
    for keyword in role_keywords.get(role, []):
        if keyword in text:
            score += 2
    if role in ["Product Manager", "AI Engineer"] and "leadership" in text:
        score += 2
    return score


def generate_llm_plan(skills, interests, goals):
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return None

    payload = {
        "model": os.environ.get("OPENAI_MODEL", "gpt-4o-mini"),
        "response_format": {"type": "json_object"},
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a career exploration assistant. Return JSON with keys "
                    "recommended_role (string), rationale (string), and roadmap "
                    "(array of 3 practical steps). Treat this as exploratory guidance, "
                    "not a guarantee or professional assessment."
                ),
            },
            {
                "role": "user",
                "content": f"Skills: {skills}\nInterests: {interests}\nGoals: {goals}",
            },
        ],
    }
    req = Request(
        "https://api.openai.com/v1/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode("utf-8"))
        plan = json.loads(result["choices"][0]["message"]["content"])
        if not isinstance(plan.get("recommended_role"), str) or not isinstance(plan.get("roadmap"), list):
            return None
        return plan
    except (HTTPError, URLError, KeyError, IndexError, TypeError, json.JSONDecodeError):
        return None


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/career-plan", methods=["POST"])
def career_plan():
    payload = request.get_json(force=True) or {}
    skills = payload.get("skills", "")
    interests = payload.get("interests", "")
    goals = payload.get("goals", "")

    llm_plan = generate_llm_plan(skills, interests, goals)
    if llm_plan:
        return jsonify({**llm_plan, "mode": "llm"})

    roles = [
        "AI Engineer",
        "Product Manager",
        "Data Analyst",
        "Frontend Engineer",
        "Backend Engineer",
    ]
    ranking = [(role, score_role(role, skills, interests, goals)) for role in roles]
    ranking.sort(key=lambda item: item[1], reverse=True)
    top_role, top_score = ranking[0]

    roadmap = {
        "AI Engineer": [
            "Strengthen Python and statistics fundamentals",
            "Build small LLM or ML projects",
            "Learn model evaluation and production deployment",
        ],
        "Product Manager": [
            "Understand user research and product workflows",
            "Create roadmaps and prioritize features",
            "Learn experimentation and stakeholder communication",
        ],
        "Data Analyst": [
            "Improve SQL and data cleaning workflows",
            "Practice dashboard building and insights generation",
            "Learn A/B testing and decision-making frameworks",
        ],
        "Frontend Engineer": [
            "Master modern JavaScript and UI patterns",
            "Practice responsive design and accessibility",
            "Build interactive portfolio projects",
        ],
        "Backend Engineer": [
            "Deepen APIs, system design, and databases",
            "Build scalable services and authentication flows",
            "Learn deployment and observability",
        ],
    }

    return jsonify({
        "recommended_role": top_role,
        "rationale": "This demo recommendation is based on keyword overlap with your skills, interests, and goals.",
        "score": top_score,
        "roadmap": roadmap.get(top_role, ["Keep learning and practicing consistently"]),
        "all_roles": [{"role": role, "score": score} for role, score in ranking],
        "mode": "rules",
    })


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5002)
