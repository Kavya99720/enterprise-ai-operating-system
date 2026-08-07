from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
def health_check():
    return {
        "status": "healthy",
        "version": "v1",
        "service": "Enterprise AI Operating System"
    }