from functools import wraps

# FastAPI
from fastapi import HTTPException

def handler_exceptions(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=500, detail="Internal Server Error")
    return wrapper