from fastapi import FastAPI
from app.core.config import settings
from app.api.health import router as health_router
from app.api.v1.router import router as v1_router
from app.core.exception_handler import application_exception_handler
from app.core.exceptions import ApplicationException

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI platform with RAG and autonomous agents"
)
app.add_exception_handler(
    ApplicationException,
    application_exception_handler
)
app.include_router(health_router)
app.include_router(v1_router)


@app.get("/")
def home():
    return {
        "message": "Enterprise AI Operating System is running",
        "environment": settings.ENVIRONMENT
    }