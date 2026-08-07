from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.exceptions import ApplicationException


async def application_exception_handler(
    request: Request,
    exc: ApplicationException
):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.message
        }
    )