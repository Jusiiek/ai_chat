from fastapi import Response
from starlette.requests import Request


async def security_headers_middleware(request: Request, call_next):
    response = await call_next(request)
    response.headers["Cache-Control"] = "no-store"
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    response.headers["X-Frame-Options"] = "deny"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-XSS-Protection"] = "1"
    response.headers[
        "Strict-Transport-Security"
    ] = "max-age=63072000; includeSubDomains"
    return response


def get_token(headers):
    token = headers["Authorization"]
    token = token.replace("Bearer ", "")
    token = token.replace("JWT ", "")
    return token


async def jwt_middleware(request: Request, call_next):
    if "Authorization" not in request.headers or "auth" in str(
        request.url.path
    ):
        return await call_next(request)
    token = get_token(request.headers)
    from ai_chat_api.api.models.blacklisted_token import BlacklistedToken

    if BlacklistedToken.objects(token=token).first():
        return Response("JWT Token Invalid", status_code=401)
    return await call_next(request)
