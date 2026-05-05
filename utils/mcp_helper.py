from pathlib import Path
import json


def load_mcp_prompt() -> dict:
    prompt_path = Path(__file__).resolve().parent / "prompts" / "mcp_generator_prompt.json"
    
    if not prompt_path.exists():
        raise FileNotFoundError(f"MCP prompt JSON not found at: {prompt_path}")
    
    with open(prompt_path, "r", encoding="utf-8") as f:
        return json.load(f)
    
def build_mcp_prompt(topic: str, level: str) -> str:
    prompt_json = load_mcp_prompt()

    system_instruction = prompt_json["system_instruction"]
    template = prompt_json["user_prompt_template"]    

    final_prompt = (
        system_instruction + "\n\n" + 
        template.replace("{{TOPIC}}", topic.strip())
                .replace("{{LEVEL}}", level.strip())
    )

    return final_prompt
