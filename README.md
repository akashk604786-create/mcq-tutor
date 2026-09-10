# AI Quiz Generator

Generate a 15-question multiple-choice quiz on any topic and difficulty using the
Groq API, then take the quiz in the browser and get scored at the end.

## Stack

- **Backend:** FastAPI (Python), Groq for quiz generation
- **Frontend:** static HTML/CSS/JS, served directly by FastAPI

## Setup

1. Create a virtual environment and install dependencies:

   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. Add your Groq API key to a `.env` file in the project root:

   ```
   GROQ_API_KEY=your_key_here
   ```

3. Run the app:

   ```bash
   uvicorn main:app --reload
   ```

4. Open [http://localhost:8000](http://localhost:8000).

## Project structure

```
main.py                    # FastAPI app entrypoint
api/routes.py               # POST /api/generate endpoint
utils/llm_client.py          # Groq API wrapper
utils/mcq_helper.py          # Builds the quiz-generation prompt
utils/quiz_parser.py         # Parses the model's output into structured questions
utils/prompts/               # Prompt templates (JSON)
config/                      # Typed app config (config.yaml + model_config.py)
static/                      # Frontend (HTML/CSS/JS)
```

## Configuration

Model settings (name, temperature, max tokens) live in `config/config.yaml`.
