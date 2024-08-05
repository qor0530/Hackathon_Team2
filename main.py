from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session
from config.database import init_db, SessionLocal
from api.models import Quiz, User, ComprehensionTask
from domain.quiz import quiz_router
from domain.lecture import lecture_router
from domain.user import user_router
from starlette import status
from domain.ranking import ranking_router
from domain import Gemini
from config.database import get_db
from starlette.status import HTTP_401_UNAUTHORIZED
from domain.user.user_router import get_current_user_from_token


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app.include_router(quiz_router.router)
app.include_router(user_router.router)
app.include_router(ranking_router.router)
app.include_router(lecture_router.router)
app.include_router(Gemini.router)

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


@app.get("/quiz/{quiz_id}", response_class=HTMLResponse)
async def quiz(request: Request, quiz_id: int, db: Session = Depends(get_db)):
    quiz_data = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz_data:
        return HTMLResponse(content="Quiz not found", status_code=404)

    # 사용자 정보 가져오기
    user = None
    try:
        user = get_current_user_from_token(request, db)
    except HTTPException as e:
        if e.status_code == status.HTTP_401_UNAUTHORIZED:
            # 인증되지 않은 사용자 처리 (예: 로그인 페이지로 리디렉션)
            user = None

    print(quiz_data, quiz_data.id)

    return templates.TemplateResponse("quiz.html", {"request": request, "quiz": quiz_data, "user": user})


@app.get("/quiz_result", response_class=HTMLResponse)
async def quiz_result(request: Request):
    return templates.TemplateResponse(request=request, name="quiz_result.html")


@app.get("/lecture", response_class=HTMLResponse)
async def lecture(request: Request):
    return templates.TemplateResponse(request=request, name="lecture.html")


@app.get("/lecture/subject", response_class=HTMLResponse)
async def subject_select(request: Request):
    return templates.TemplateResponse(request=request, name="subjectSelect.html")


@app.get("/lecture/write/1", response_class=HTMLResponse)
async def write(request: Request):
    return templates.TemplateResponse(request=request, name="studyWrite.html")


@app.get("/lecture/situation/{comprehension_tasks_id}", response_class=HTMLResponse)
async def situation(request: Request, comprehension_tasks_id: int, db: Session = Depends(get_db)):
    comprehension_task = db.query(ComprehensionTask).filter(
        ComprehensionTask.id == comprehension_tasks_id).first()

    if comprehension_task is None:
        return HTMLResponse(content="Comprehension Task not found", status_code=404)

    # `conversation` 내용을 `|` 기준으로 나누기
    if comprehension_task.conversation:
        conversation_parts = comprehension_task.conversation.split('|', 1)
        if len(conversation_parts) == 2:
            first_part, second_part = conversation_parts
        else:
            first_part, second_part = conversation_parts[0], ""
    else:
        first_part, second_part = "", ""

    # `options` 내용을 줄바꿈 기준으로 나누기
    options = {}
    if comprehension_task.options:
        options_list = comprehension_task.options.split('\n')
        for idx, option in enumerate(options_list):
            options[f'option{idx + 1}'] = option.strip()
    else:
        options = {f'option{i}': "" for i in range(1, 6)}  # 빈 값으로 초기화

       # 사용자 정보 가져오기
    user = None
    try:
        user = get_current_user_from_token(request, db)
    except HTTPException as e:
        if e.status_code == status.HTTP_401_UNAUTHORIZED:
            user = None

    # 템플릿에 데이터를 전달하여 렌더링
    return templates.TemplateResponse(
        "studySituation.html",
        {
            "request": request,
            "comprehension_task": comprehension_task,
            "first_part": first_part.strip(),
            "second_part": second_part.strip(),
            **options,
            "user": user  # 사용자 정보를 템플릿에 전달
        }
    )
