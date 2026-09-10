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
main.py                    # FastAPI app entrypoint (local dev: uvicorn main:app)
api/index.py                # FastAPI app entrypoint for Vercel's serverless runtime
api/routes.py                # Shared router: POST /api/generate
utils/llm_client.py          # Groq API wrapper
utils/mcq_helper.py          # Builds the quiz-generation prompt
utils/quiz_parser.py         # Parses the model's output into structured questions
utils/prompts/               # Prompt templates (JSON)
config/                      # Typed app config (config.yaml + model_config.py)
public/                      # Frontend (HTML/CSS/JS)
```

`main.py` and `api/index.py` both build a FastAPI app around the same
`api/routes.py` router — `main.py` additionally mounts `public/` as static
files for local dev, since Vercel serves `public/` itself.

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

`vercel.json` rewrites `/api/*` requests to the `api/index.py` serverless
function; everything else is served as static content from `public/`.
