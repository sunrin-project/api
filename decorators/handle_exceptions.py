from functools import wraps
from fastapi.responses import JSONResponse

from schemes.meal_scheme import ErrorScheme


def handle_exceptions(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            return JSONResponse(
                content=ErrorScheme(message=str(e)).dict(),
                status_code=500
            )
    return wrapper
