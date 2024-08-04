from domain.quiz import quiz_crud, quiz_schema
from fastapi import APIRouter, Depends, Request, status, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from sqlalchemy.orm import Session
from config.database import get_db
from fastapi.templating import Jinja2Templates

router = APIRouter(
    prefix="/api/quiz",
)

templates = Jinja2Templates(directory="domain/quiz/templates")


@router.get("/update/{quiz_id}", response_class=HTMLResponse)
def quiz_update_html(request: Request, quiz_id: int, db: Session = Depends(get_db)):
    quiz = quiz_crud.get_quiz(db, quiz_id=quiz_id)
    if not quiz:
        print("quiz not found")
        raise HTTPException(status_code=404, detail="Quiz not found")
    return templates.TemplateResponse("quiz_update.html", {"request": request, "quiz": quiz}, status_code=200)


@router.patch("/update/{quiz_id}", status_code=status.HTTP_204_NO_CONTENT)
def quiz_update(quiz_id: int, _quiz_update: quiz_schema.QuizUpdate, db: Session = Depends(get_db)):
    db_quiz = quiz_crud.get_quiz(db, quiz_id)
    if not db_quiz:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Quiz not found")
    quiz_crud.update_quiz(db=db, db_quiz=db_quiz, quiz_update=_quiz_update)


@router.get("/list", response_class=HTMLResponse)
def quiz_list_html(request: Request, db: Session = Depends(get_db)):
    quiz_list = quiz_crud.get_quiz_list(db)
    return templates.TemplateResponse("quiz_list.html", {"request": request, "quiz_list": quiz_list})


@router.get("/detail/{quiz_id}", response_class=HTMLResponse)
def quiz_detail_html(request: Request, quiz_id: int, db: Session = Depends(get_db)):
    quiz = quiz_crud.get_quiz(db, quiz_id)
    return JSONResponse(content=quiz)


@router.get("/create", response_class=HTMLResponse)
def quiz_create_html(request: Request):
    return templates.TemplateResponse("quiz_create.html", {"request": request})


@router.post("/create", status_code=status.HTTP_204_NO_CONTENT)
def quiz_create(_quiz_create: quiz_schema.QuizCreate, db: Session = Depends(get_db)):
    quiz_crud.create_quiz(db=db, quiz_create=_quiz_create)


@router.delete("/delete/{quiz_id}", status_code=status.HTTP_204_NO_CONTENT)
def quiz_delete(quiz_id: int, db: Session = Depends(get_db)):
    db_quiz = quiz_crud.get_quiz(db, quiz_id)
    if not db_quiz:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Quiz not found")
    quiz_crud.delete_quiz(db=db, db_quiz=db_quiz)
