from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

# static 폴더 연결
app.mount("/static", StaticFiles(directory="static"), name="static")

# templates 폴더 연결
templates = Jinja2Templates(directory="templates")


# HTML 연결
@app.get("/", response_class=HTMLResponse)
async def main(request: Request):
    return templates.TemplateResponse(request=request, name="main.html")


@app.get("/my_page", response_class=HTMLResponse)
async def my_page(request: Request):
    return templates.TemplateResponse(request=request, name="my_page.html")

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse(request=request, name="dashboard.html")


@app.get("/login", response_class=HTMLResponse)
async def my_page(request: Request):
    return templates.TemplateResponse(request=request, name="login.html")


@app.get("/signup", response_class=HTMLResponse)
async def my_page(request: Request):
    return templates.TemplateResponse(request=request, name="signup.html")

@app.get("/ranking", response_class=HTMLResponse)
async def my_page(request: Request):
    return templates.TemplateResponse(request=request, name="ranking.html")

@app.get("/quiz_select", response_class=HTMLResponse)
async def quiz_select(request: Request):
    return templates.TemplateResponse(request=request, name="quiz_select.html")

@app.get("/quiz_main", response_class=HTMLResponse)
async def quiz_main(request: Request):
    return templates.TemplateResponse(request=request, name="quiz_main.html")

@app.get("/learning", response_class=HTMLResponse)
async def learning(request: Request):
    return templates.TemplateResponse(request=request, name="learning.html")

@app.get("/writing_learning", response_class=HTMLResponse)
async def learning(request: Request):
    return templates.TemplateResponse(request=request, name="writing_learning.html")
# API 연결
# (추후 개발)
