from __future__ import annotations

import re
from typing import TypedDict


class Question(TypedDict):
    number: int
    question: str
    options: dict[str, str]
    answer: str
    explanation: str


_QUESTION_BLOCK = re.compile(r"Q(\d+)\.\s*(.*?)(?=\nQ\d+\.|\Z)", re.DOTALL)
_OPTION_LINE = re.compile(r"^([A-D])\.\s*(.+)$", re.MULTILINE)
_ANSWER_LINE = re.compile(r"^Answer:\s*([A-D])", re.MULTILINE)
_EXPLANATION_LINE = re.compile(r"^Explanation:\s*(.+)$", re.MULTILINE | re.DOTALL)


def parse_quiz(raw_text: str) -> list[Question]:
    """Parse the model's plain-text MCQ output into structured questions.

    Tolerates minor formatting drift (extra blank lines, stray whitespace)
    since the model is not guaranteed to follow the prompt's format exactly.
    """
    questions: list[Question] = []

    for match in _QUESTION_BLOCK.finditer(raw_text.strip()):
        number = int(match.group(1))
        block = match.group(2).strip()

        first_option = _OPTION_LINE.search(block)
        question_text = block[: first_option.start()].strip() if first_option else block.strip()

        options = {label: text.strip() for label, text in _OPTION_LINE.findall(block)}

        answer_match = _ANSWER_LINE.search(block)
        answer = answer_match.group(1) if answer_match else ""

        explanation_match = _EXPLANATION_LINE.search(block)
        explanation = explanation_match.group(1).strip() if explanation_match else ""

        if question_text and options and answer:
            questions.append(
                {
                    "number": number,
                    "question": question_text,
                    "options": options,
                    "answer": answer,
                    "explanation": explanation,
                }
            )

    return questions
