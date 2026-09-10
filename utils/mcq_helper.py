from pathlib import Path
import json


def load_mcq_prompt() -> dict:
    prompt_path = Path(__file__).resolve().parent / "prompts" / "mcq_generator_prompt.json"

    if not prompt_path.exists():
        raise FileNotFoundError(f"MCQ prompt JSON not found at: {prompt_path}")

    with open(prompt_path, "r", encoding="utf-8") as f:
        return json.load(f)


def build_mcq_prompt(topic: str, level: str) -> str:
    prompt_json = load_mcq_prompt()

    system_instruction = prompt_json["system_instruction"]
    template = prompt_json["user_prompt_template"]

    return (
        system_instruction + "\n\n" +
        template.replace("{{TOPIC}}", topic.strip())
                .replace("{{LEVEL}}", level.strip())
    )
