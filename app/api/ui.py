from fastapi import APIRouter, Request, Query
from fastapi.responses import HTMLResponse
from app.services.session_store import load_response
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/result", response_class=HTMLResponse)
async def result_page(request: Request, session_id: str = Query(...)):
    html_output = load_response(session_id)
    if not html_output:
        html_output = "<p>No result found for this session.</p>"
    return templates.TemplateResponse("result.html", {"request": request, "html_output": html_output})
@router.get("/ui", response_class=HTMLResponse)
async def serve_ui(request: Request):
    return templates.TemplateResponse("ui.html", {"request": request})