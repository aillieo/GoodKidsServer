from fastapi import HTTPException
from starlette.responses import JSONResponse


async def handle_exception(request, err: Exception):
    if isinstance(err, HTTPException):
        return JSONResponse(
            status_code=err.status_code,
            content={"message": f"HTTP error: {err.detail}"},
        )
    elif isinstance(err, ValueError):
        return JSONResponse(
            status_code=400,
            content={"message": f"Value error: {str(err)}"},
        )
    else:
        return JSONResponse(
            status_code=500,
            content={"message": "An unexpected error occurred."},
        )
