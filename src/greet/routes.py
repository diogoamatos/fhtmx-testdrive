from fastapi import APIRouter, Header


greet_router = APIRouter()


@greet_router.get("/{name}")
async def greet_name(name: str | None):
    return {"message": f"Hello {name}"}


@greet_router.get('/get_headers')
async def get_headers(
    accept: str = Header(None),
    content_type: str = Header(None),
    user_agent: str = Header(None),
    host: str = Header(None)
):
    request_headers = {}

    request_headers["Accept"] = accept
    request_headers["Content-Type"] = content_type
    request_headers["User-Agent"] = user_agent
    request_headers["Host"] = host

    return request_headers
