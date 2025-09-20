from fastapi import Request, HTTPException

from utils import get_response_schema
from global_constants import ErrorMessage

def register_exception_handlers(app):
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        schema = exc.detail if isinstance(exc.detail, dict) else {"detail": [exc.detail]}
        # Use a generic envelope message; specific error lives in schema.detail
        message = ErrorMessage.SOMETHING_WENT_WRONG.value
        return get_response_schema(schema, message, exc.status_code)
