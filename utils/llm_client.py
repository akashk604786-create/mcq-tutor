from __future__ import annotations

import os
from typing import Optional

from groq import Groq
from dotenv import load_dotenv

from config.model_config import load_config

load_dotenv()


class GroqClient:
    def __init__(
        self,
        api_key: Optional[str] = None,
        config_path: Optional[str] = None
    ):
        # Load YAML config
        self.app_config = load_config(config_path)
        self.model_cfg = self.app_config.model

        # Get API key
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not found in environment or passed explicitly.")

        # Initialize Groq client
        self.client = Groq(api_key=self.api_key)

        # Model name from config (or fallback)
        self.model_name = self.model_cfg.name or "openai/gpt-oss-20b"

    def ask(self, prompt: str) -> str:
        """
        Send a prompt to Groq and return the response text.
        Raises on failure so callers can decide how to surface the error.
        """
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=self.model_cfg.temperature,
            top_p=self.model_cfg.top_p,
            max_tokens=self.model_cfg.max_output_tokens,
        )

        return response.choices[0].message.content