from fastapi import Request, APIRouter
from fastapi.responses import HTMLResponse

from src.config import templates


root_router = APIRouter()


@root_router.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    context = {}
    return templates.TemplateResponse(
        request=request, name="index.html", context=context
    )
