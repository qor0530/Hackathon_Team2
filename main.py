from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from starlette.middleware.cors import CORSMiddleware

from config.database import init_db

from domain.quiz import quiz_router
from domain.lecture import lecture_router
from domain.user import user_router
from domain.ranking import ranking_router
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(quiz_router.router)
app.include_router(user_router.router)
app.include_router(ranking_router.router)
app.include_router(lecture_router.router)

# static 폴더 연결
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# templates 폴더 연결
templates = Jinja2Templates(directory="templates")


@app.on_event("startup")
def on_startup():
    init_db()

# HTML 연결
@ app.get("/", response_class=HTMLResponse)
async def main(request: Request):
    return templates.TemplateResponse(request=request, name="main.html")


@ app.get("/my_page", response_class=HTMLResponse)
async def my_page(request: Request):
    return templates.TemplateResponse(request=request, name="my_page.html")


@ app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse(request=request, name="dashboard.html")


@ app.get("/login", response_class=HTMLResponse)
async def my_page(request: Request):
    return templates.TemplateResponse(request=request, name="login.html")


@ app.get("/signup", response_class=HTMLResponse)
async def my_page(request: Request):
    return templates.TemplateResponse(request=request, name="signup.html")


@app.get("/test", response_class=HTMLResponse)
async def my_page(request: Request):
    return templates.TemplateResponse(request=request, name="test.html")


@app.get("/ranking", response_class=HTMLResponse)
async def my_page(request: Request):
    return templates.TemplateResponse(request=request, name="ranking.html")


@app.get("/quiz_main", response_class=HTMLResponse)
async def quiz_main(request: Request):
    return templates.TemplateResponse(request=request, name="quiz_main.html")


@app.get("/quiz", response_class=HTMLResponse)
async def quiz(request: Request):
    return templates.TemplateResponse(request=request, name="quiz.html")

@app.get("/lecture", response_class=HTMLResponse)
async def lecture(request: Request):
    return templates.TemplateResponse(request=request, name="lecture.html")

@app.get("/lecture/subject", response_class=HTMLResponse)
async def subject_select(request: Request):
    return templates.TemplateResponse(request=request, name="subjectSelect.html")

@app.get("/lecture/write/1", response_class=HTMLResponse)
async def write(request: Request):
    return templates.TemplateResponse(request=request, name="studyWrite.html")

@app.get("/lecture/situation/1", response_class=HTMLResponse)
async def situation(request: Request):
    return templates.TemplateResponse(request=request, name="studySituation.html")
# API 연결
# (추후 개발)
