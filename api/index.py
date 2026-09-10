from fastapi import FastAPI

from api.routes import router

app = FastAPI(title="AI Quiz Generator API")
app.include_router(router)
