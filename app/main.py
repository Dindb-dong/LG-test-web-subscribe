"""Application entrypoint for the webOS subscription practice dashboard."""

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.api import api_router

app = FastAPI(title="webOS Subscription Service", version="1.0.0")
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")
app.include_router(api_router, prefix="/api/v1")


@app.get("/", response_class=HTMLResponse)
def read_dashboard(request: Request) -> HTMLResponse:
    """Render the dashboard shell.

    Args:
        request: Incoming FastAPI request used by the template engine.

    Returns:
        The HTML dashboard page.
    """
    return templates.TemplateResponse(request=request, name="index.html")


@app.get("/health")
def health() -> dict[str, str]:
    """Expose a lightweight health check.

    Args:
        None.

    Returns:
        A small JSON payload that confirms the app is reachable.
    """
    return {"status": "ok"}
