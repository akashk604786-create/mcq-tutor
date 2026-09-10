from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from api.routes import router

app = FastAPI(title="AI Quiz Generator")
app.include_router(router)

# Local dev only: Vercel serves public/ itself and never bundles it into
# the function, so this mount must not run (or exist) there.
public_dir = Path(__file__).resolve().parent / "public"
if public_dir.is_dir():
    app.mount("/", StaticFiles(directory=str(public_dir), html=True), name="public")
