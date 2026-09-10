from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from api.routes import router

app = FastAPI(title="AI Quiz Generator")
app.include_router(router)

# Mounted last so /api/* is matched by the router above first.
app.mount("/", StaticFiles(directory="public", html=True), name="public")
