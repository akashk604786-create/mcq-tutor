from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from utils.llm_client import GroqClient
from utils.mcq_helper import build_mcq_prompt
from utils.quiz_parser import parse_quiz

router = APIRouter(prefix="/api")

DIFFICULTY_LEVELS = {"Easy", "Medium", "Hard"}


class GenerateQuizRequest(BaseModel):
    topic: str = Field(min_length=1, max_length=200)
    level: str = "Easy"


@router.post("/generate")
def generate_quiz(request: GenerateQuizRequest):
    topic = request.topic.strip()
    if not topic:
        raise HTTPException(status_code=400, detail="Topic is required.")

    level = request.level if request.level in DIFFICULTY_LEVELS else "Easy"

    try:
        prompt = build_mcq_prompt(topic, level)
        raw_response = GroqClient().ask(prompt)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Failed to generate quiz: {exc}") from exc

    questions = parse_quiz(raw_response)
    if not questions:
        raise HTTPException(status_code=502, detail="The model returned an unexpected format. Please try again.")

    return {"topic": topic, "level": level, "questions": questions}
