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
main.py                    # FastAPI app entrypoint — used locally AND by Vercel
api/routes.py                # Router: POST /api/generate
utils/llm_client.py          # Groq API wrapper
utils/mcq_helper.py          # Builds the quiz-generation prompt
utils/quiz_parser.py         # Parses the model's output into structured questions
utils/prompts/               # Prompt templates (JSON)
config/                      # Typed app config (config.yaml + model_config.py)
public/                      # Frontend (HTML/CSS/JS)
```

`main.py` mounts `public/` as static files only when that directory exists
on disk — true for local dev, but not inside Vercel's deployed function,
where Vercel serves `public/` itself via its own static layer and routes
everything else (like `/api/generate`) straight to this same FastAPI app.

## Configuration

Model settings (name, temperature, max tokens) live in `config/config.yaml`.

## Deploying to Vercel

1. Install the [Vercel CLI](https://vercel.com/docs/cli) and log in:

   ```bash
   npm i -g vercel
   vercel login
   ```

2. From the project root, link and deploy:

   ```bash
   vercel
   ```

3. Add `GROQ_API_KEY` as an environment variable in the Vercel project
   settings (Settings → Environment Variables) — `.env` is not deployed.

4. Deploy to production:

   ```bash
   vercel --prod
   ```

Vercel auto-detects the FastAPI app in `main.py` and deploys it as a
serverless function, serving `public/` directly as static content and
routing everything else to that function — no extra routing config needed.
