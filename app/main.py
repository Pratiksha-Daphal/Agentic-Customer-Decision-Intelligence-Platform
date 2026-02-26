from fastapi import FastAPI
from app.api.routes import router
import os
os.environ["PYTHONIOENCODING"] = "utf-8"
app = FastAPI(
    title="Agentic Customer Decision Platform",
    version="0.1.0"
)

app.include_router(router)