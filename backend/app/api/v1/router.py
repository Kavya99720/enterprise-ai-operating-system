from fastapi import APIRouter

from app.api.v1.health import router as health_router
from app.api.v1.tasks import router as task_router
from app.api.v1.agents import router as agent_router
from app.api.v1.execution import router as execution_router
from app.api.v1.documents import router as document_router


router = APIRouter(prefix="/api/v1")

router.include_router(health_router)
router.include_router(task_router)
router.include_router(agent_router)
router.include_router(execution_router)
router.include_router(document_router)
