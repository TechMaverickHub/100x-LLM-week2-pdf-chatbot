from fastapi import Request, HTTPException

from utils import get_response_schema

def register_exception_handlers(app):
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        schema = exc.detail if isinstance(exc.detail, dict) else {"detail": [exc.detail]}
        return get_response_schema(schema, "Error occurred", exc.status_code)
